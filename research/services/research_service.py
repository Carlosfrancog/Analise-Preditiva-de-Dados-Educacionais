#!/usr/bin/env python3
"""Serviço de leitura dos snapshots e inferência dos modelos de pesquisa."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from research.features.temporal_snapshots import SNAPSHOT_FEATURES
from research.models.artifacts import LABELS, list_artifacts, load_artifact


class ResearchServiceError(RuntimeError):
    """Erro de domínio traduzido pela camada HTTP em resposta 4xx/5xx."""


class ResearchService:
    def __init__(self, root: Path | None = None):
        project_root = root or Path(__file__).resolve().parents[2]
        self.snapshot_dir = project_root / "research" / "data" / "snapshots"
        self.artifact_dir = project_root / "research" / "artifacts"

    @staticmethod
    def normalize_cutoff(cutoff: str) -> str:
        normalized = str(cutoff).upper().strip()
        if normalized not in SNAPSHOT_FEATURES:
            raise ResearchServiceError(
                f"corte inválido: {cutoff}; use um destes: {', '.join(SNAPSHOT_FEATURES)}"
            )
        return normalized

    def _snapshot_path(self, cutoff: str) -> Path:
        cutoff = self.normalize_cutoff(cutoff)
        path = self.snapshot_dir / f"experimental_dataset_{cutoff}.csv"
        if not path.exists():
            raise ResearchServiceError(
                "snapshots ausentes; execute research.run_initial_pipeline antes de iniciar a API"
            )
        return path

    def read_snapshot(self, cutoff: str) -> pd.DataFrame:
        return pd.read_csv(self._snapshot_path(cutoff))

    def catalog(self) -> list[dict[str, Any]]:
        artifacts = {item["cutoff"]: item for item in list_artifacts(self.artifact_dir)}
        result = []
        for cutoff, features in SNAPSHOT_FEATURES.items():
            path = self.snapshot_dir / f"experimental_dataset_{cutoff}.csv"
            rows = int(pd.read_csv(path, nrows=0).shape[0]) if path.exists() else 0
            if path.exists():
                rows = sum(1 for _ in path.open("r", encoding="utf-8")) - 1
            result.append({
                "cutoff": cutoff,
                "features": features,
                "rows": max(rows, 0),
                "model_available": cutoff in artifacts,
                "model": artifacts.get(cutoff),
            })
        return result

    def _prediction(
        self,
        cutoff: str,
        values: dict[str, Any],
        artifact: tuple[Any, dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        cutoff = self.normalize_cutoff(cutoff)
        model, metadata = artifact or load_artifact(self.artifact_dir, cutoff)
        features = metadata["features"]
        missing = [name for name in features if name not in values]
        if missing:
            raise ResearchServiceError(f"features ausentes para {cutoff}: {', '.join(missing)}")

        frame = pd.DataFrame([{name: values[name] for name in features}])
        predicted = int(model.predict(frame)[0])
        probabilities_array = model.predict_proba(frame)[0]
        return self._prediction_result(
            cutoff, values, model, metadata, predicted, probabilities_array
        )

    @staticmethod
    def _prediction_result(
        cutoff: str,
        values: dict[str, Any],
        model: Any,
        metadata: dict[str, Any],
        predicted: int,
        probabilities_array: Any,
    ) -> dict[str, Any]:
        features = metadata["features"]
        model_step = model.named_steps.get("model") if hasattr(model, "named_steps") else model
        model_classes = getattr(model_step, "classes_", [0, 1, 2])
        probabilities = {
            LABELS[int(class_value)]: round(float(probability), 6)
            for class_value, probability in zip(model_classes, probabilities_array)
        }
        return {
            "cutoff": cutoff,
            "model": metadata["model_name"],
            "predicted_class": predicted,
            "predicted_label": LABELS.get(predicted, str(predicted)),
            "confidence": round(float(max(probabilities.values())), 6),
            "probabilities": probabilities,
            "features": {name: float(values[name]) for name in features},
            "artifact": {
                "version": metadata["artifact_version"],
                "trained_rows": metadata["trained_rows"],
                "source_snapshot": metadata["source_snapshot"],
            },
        }

    def predict_features(self, cutoff: str, values: dict[str, Any]) -> dict[str, Any]:
        return self._prediction(cutoff, values)

    def samples(
        self,
        cutoff: str,
        limit: int = 25,
        student_id: str | None = None,
        academic_year: int | None = None,
        include_prediction: bool = True,
    ) -> list[dict[str, Any]]:
        cutoff = self.normalize_cutoff(cutoff)
        if limit < 1 or limit > 200:
            raise ResearchServiceError("limit deve estar entre 1 e 200")

        data = self.read_snapshot(cutoff)
        if student_id:
            data = data[data["student_id"].astype(str) == str(student_id)]
        if academic_year is not None:
            data = data[pd.to_numeric(data["academic_year"], errors="coerce") == academic_year]
        data = data.head(limit)

        records = []
        for raw in data.to_dict(orient="records"):
            record = {
                key: (None if pd.isna(value) else value.item() if isinstance(value, np.generic) else value)
                for key, value in raw.items()
            }
            records.append(record)

        if include_prediction and records:
            model, metadata = load_artifact(self.artifact_dir, cutoff)
            features = metadata["features"]
            missing = [name for name in features if name not in records[0]]
            if missing:
                raise ResearchServiceError(
                    f"features ausentes para {cutoff}: {', '.join(missing)}"
                )
            frame = pd.DataFrame(
                [{name: record[name] for name in features} for record in records]
            )
            predicted_values = model.predict(frame)
            probabilities = model.predict_proba(frame)
            for record, predicted, probability_values in zip(
                records, predicted_values, probabilities
            ):
                record["prediction"] = self._prediction_result(
                    cutoff,
                    record,
                    model,
                    metadata,
                    int(predicted),
                    probability_values,
                )
        return records
