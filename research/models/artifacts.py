#!/usr/bin/env python3
"""Treina e carrega os artefatos usados pela interface de pesquisa.

Os artefatos deste módulo são modelos operacionais para demonstração e
integração da interface. Eles não substituem os resultados do benchmark:
as métricas oficiais continuam sendo calculadas pelos cortes temporal e
agrupado em ``research.evaluation.benchmark``.
"""

from __future__ import annotations

import json
import pickle
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from research.features.temporal_snapshots import SNAPSHOT_FEATURES


SEED = 20261004
LABELS = {0: "Reprovado", 1: "Recuperação", 2: "Aprovado"}
ARTIFACT_VERSION = "research-rf-v1"


def _estimator() -> Pipeline:
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestClassifier(
            n_estimators=200,
            random_state=SEED,
            class_weight="balanced_subsample",
            n_jobs=-1,
        )),
    ])


def _paths(artifact_dir: Path, cutoff: str) -> tuple[Path, Path]:
    name = cutoff.upper()
    return artifact_dir / f"{name}.pkl", artifact_dir / f"{name}.json"


def train_and_save_artifacts(
    snapshot_dir: Path,
    artifact_dir: Path,
    source_prefix: str = "experimental_dataset",
) -> list[dict[str, Any]]:
    """Treina um Random Forest por corte e grava modelo + metadados."""
    artifact_dir.mkdir(parents=True, exist_ok=True)
    summaries: list[dict[str, Any]] = []

    for cutoff, features in SNAPSHOT_FEATURES.items():
        snapshot_path = snapshot_dir / f"{source_prefix}_{cutoff}.csv"
        if not snapshot_path.exists():
            raise FileNotFoundError(f"snapshot não encontrado: {snapshot_path}")

        data = pd.read_csv(snapshot_path).dropna(subset=["target"]).copy()
        data["target"] = pd.to_numeric(data["target"], errors="coerce").astype(int)
        estimator = _estimator()
        estimator.fit(data[features], data["target"])

        model_path, metadata_path = _paths(artifact_dir, cutoff)
        with model_path.open("wb") as model_file:
            pickle.dump(estimator, model_file, protocol=pickle.HIGHEST_PROTOCOL)
        metadata = {
            "artifact_version": ARTIFACT_VERSION,
            "model_name": "random_forest",
            "cutoff": cutoff,
            "features": features,
            "classes": [0, 1, 2],
            "labels": LABELS,
            "trained_rows": int(len(data)),
            "source_snapshot": snapshot_path.name,
            "seed": SEED,
            "purpose": "interactive_research_api",
            "evaluation_warning": (
                "artefato treinado no snapshot completo para alimentar a interface; "
                "não usar este ajuste como métrica oficial"
            ),
        }
        metadata_path.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        summaries.append(metadata)

    return summaries


def load_artifact(artifact_dir: Path, cutoff: str) -> tuple[Any, dict[str, Any]]:
    """Carrega modelo e metadados, reutilizando-os enquanto os arquivos não mudarem."""
    cutoff = cutoff.upper()
    model_path, metadata_path = _paths(artifact_dir, cutoff)
    if not model_path.exists() or not metadata_path.exists():
        raise FileNotFoundError(
            f"artefato {cutoff} ausente; execute research.run_initial_pipeline"
        )
    model_stat = model_path.stat()
    metadata_stat = metadata_path.stat()
    return _load_artifact_cached(
        str(model_path.resolve()),
        str(metadata_path.resolve()),
        model_stat.st_mtime_ns,
        model_stat.st_size,
        metadata_stat.st_mtime_ns,
        metadata_stat.st_size,
    )


@lru_cache(maxsize=12)
def _load_artifact_cached(
    model_path: str,
    metadata_path: str,
    model_mtime_ns: int,
    model_size: int,
    metadata_mtime_ns: int,
    metadata_size: int,
) -> tuple[Any, dict[str, Any]]:
    """Mantém em memória somente versões identificadas pela assinatura dos arquivos."""
    del model_mtime_ns, model_size, metadata_mtime_ns, metadata_size
    with Path(model_path).open("rb") as model_file:
        model = pickle.load(model_file)
    metadata = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
    return model, metadata


def clear_artifact_cache() -> None:
    """Limpa o cache após retreino ou em testes isolados."""
    _load_artifact_cached.cache_clear()


def list_artifacts(artifact_dir: Path) -> list[dict[str, Any]]:
    """Lista os metadados disponíveis sem carregar os modelos."""
    result = []
    for cutoff in SNAPSHOT_FEATURES:
        model_path, metadata_path = _paths(artifact_dir, cutoff)
        if model_path.exists() and metadata_path.exists():
            result.append(json.loads(metadata_path.read_text(encoding="utf-8")))
    return result
