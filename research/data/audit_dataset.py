#!/usr/bin/env python3
"""Audita o dataset legado antes que ele seja usado no artigo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


LEAKAGE_NAMES = {
    "n4", "n4_norm", "media_pond_norm", "media_final", "final_score",
    "status", "status_encoded", "status_label", "target", "label",
}
TEMPORAL_NAMES = {"academic_year", "period", "period_id", "cutoff_at", "observed_at"}


def audit_dataset(path: Path) -> dict:
    df = pd.read_csv(path)
    columns_lower = {str(c).lower(): str(c) for c in df.columns}
    numeric = df.select_dtypes(include="number")

    target_columns = [
        original for lower, original in columns_lower.items()
        if lower in {"status_encoded", "status_label", "target", "label"}
    ]
    leakage_columns = [
        original for lower, original in columns_lower.items()
        if (lower in LEAKAGE_NAMES or lower.startswith("n4") or "final" in lower)
        and original not in target_columns
    ]
    temporal_columns = [
        original for lower, original in columns_lower.items()
        if lower in TEMPORAL_NAMES or any(token in lower for token in ("year", "period", "date", "time"))
    ]

    correlations = {}
    if "status_encoded" in df.columns:
        for column in numeric.columns:
            if column == "status_encoded":
                continue
            correlations[column] = float(df[[column, "status_encoded"]].corr().iloc[0, 1])

    result = {
        "path": str(path),
        "rows": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "duplicate_rows": int(df.duplicated().sum()),
        "null_counts": {str(k): int(v) for k, v in df.isna().sum().items() if v},
        "class_distribution": (
            df["status_label"].value_counts(dropna=False).to_dict()
            if "status_label" in df.columns else {}
        ),
        "target_columns": target_columns,
        "leakage_suspect_columns": leakage_columns,
        "temporal_columns": temporal_columns,
        "has_temporal_fields": bool(temporal_columns),
        "feature_target_correlations": correlations,
        "official_use": "reference_only_until_revalidated",
    }
    return result


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, nargs="?", default=root / "02-ML/ml_dataset.csv")
    parser.add_argument("--output", type=Path, default=root / "research/reports/legacy_audit.json")
    args = parser.parse_args()

    report = audit_dataset(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
