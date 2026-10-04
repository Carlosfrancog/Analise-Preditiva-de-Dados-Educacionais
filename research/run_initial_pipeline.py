#!/usr/bin/env python3
"""Executa a primeira pipeline de pesquisa sem alterar o sistema legado."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from research.data.audit_dataset import audit_dataset
from research.data.generate_dataset import DatasetConfig, write_dataset
from research.evaluation.benchmark import run_benchmark
from research.features.temporal_snapshots import build_all_snapshots
from research.models.artifacts import train_and_save_artifacts
import pandas as pd
import json


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"


def main() -> None:
    generated = RESEARCH / "data/generated/experimental_dataset.csv"
    legacy_csv = ROOT / "02-ML/ml_dataset.csv"
    reports = RESEARCH / "reports"
    snapshots = RESEARCH / "data/snapshots"
    reports.mkdir(parents=True, exist_ok=True)
    snapshots.mkdir(parents=True, exist_ok=True)

    dataset, manifest = write_dataset(DatasetConfig(), generated)
    legacy_report = audit_dataset(legacy_csv)
    (reports / "legacy_audit.json").write_text(
        json.dumps(legacy_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    data = pd.read_csv(dataset)
    for name, snapshot in build_all_snapshots(data).items():
        snapshot.to_csv(snapshots / f"experimental_dataset_{name}.csv", index=False)

    artifacts = train_and_save_artifacts(snapshots, RESEARCH / "artifacts")
    benchmark = run_benchmark(dataset, reports / "initial_benchmark.json")
    lines = [
        "# Primeiro experimento da pipeline de pesquisa",
        "",
        "> Este relatório é uma verificação técnica inicial. Ele não deve ser",
        "> transcrito como resultado final do Full Paper antes do congelamento do",
        "> protocolo, da calibração e da revisão do orientador.",
        "",
        "## Execução",
        "",
        f"- Registros sintéticos: **{len(data):,}**".replace(",", "."),
        f"- Registros legados auditados: **{legacy_report['rows']:,}**".replace(",", "."),
        f"- Resultados gerados: **{len(benchmark['results'])}**",
        f"- Artefatos para a API: **{len(artifacts)} modelos temporais**",
        f"- Seed: **{benchmark['seed']}**",
        "- Fonte sintética: dados gerados localmente, sem estudantes reais.",
        "",
        "## Observação sobre o legado",
        "",
        f"O dataset legado possui `status` como alvo: {', '.join(legacy_report['target_columns']) or 'não identificado'}.",
        f"Features suspeitas para auditoria: {', '.join(legacy_report['leakage_suspect_columns']) or 'nenhuma' }.",
        "A presença de `n4_norm` e `media_pond_norm` impede usar as métricas antigas como resultado oficial sem reconstrução temporal.",
        "",
        "## Próxima validação",
        "",
        "1. revisar os rótulos e as faixas de aprovação;",
        "2. adicionar calibração e validação cruzada agrupada;",
        "3. instalar e avaliar o candidato XGBoost ou CatBoost;",
        "4. integrar o snapshot versionado à API;",
        "5. repetir o experimento com o protocolo aprovado para o artigo.",
        "6. consumir os endpoints `/api/research` pela interface, mantendo a distinção entre demonstração e resultado oficial.",
    ]
    (reports / "initial_pipeline_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    summary = {
        "generated_dataset": str(dataset),
        "manifest": str(manifest),
        "generated_rows": int(len(data)),
        "legacy_rows": legacy_report["rows"],
        "legacy_suspect_columns": legacy_report["leakage_suspect_columns"],
        "benchmark_results": len(benchmark["results"]),
        "research_artifacts": [item["cutoff"] for item in artifacts],
        "status": "initial_experiment_complete",
    }
    (reports / "initial_pipeline_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
