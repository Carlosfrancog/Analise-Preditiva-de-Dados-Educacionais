#!/usr/bin/env python3
"""Executa o primeiro benchmark reproduzível da pesquisa."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    log_loss,
    recall_score,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from research.features.temporal_snapshots import SNAPSHOT_FEATURES, build_snapshot


def _models() -> dict[str, Pipeline]:
    models: dict[str, Pipeline] = {
        "majority": Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("model", DummyClassifier(strategy="most_frequent")),
        ]),
        "logistic_regression": Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]),
        "random_forest": Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", RandomForestClassifier(
                n_estimators=200,
                random_state=20261004,
                class_weight="balanced_subsample",
                n_jobs=-1,
            )),
        ]),
    }

    try:
        from xgboost import XGBClassifier  # type: ignore
    except ImportError:
        XGBClassifier = None

    if XGBClassifier is not None:
        models["xgboost"] = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", XGBClassifier(
                n_estimators=250,
                max_depth=5,
                learning_rate=0.05,
                subsample=0.85,
                colsample_bytree=0.85,
                objective="multi:softprob",
                num_class=3,
                eval_metric="mlogloss",
                random_state=20261004,
                n_jobs=4,
            )),
        ])
    return models


def _multiclass_brier(y_true: np.ndarray, probabilities: np.ndarray) -> float:
    expected = np.eye(3)[y_true.astype(int)]
    return float(np.mean(np.sum((probabilities - expected) ** 2, axis=1)))


def _run_one(
    snapshot: pd.DataFrame,
    cutoff: str,
    features: list[str],
    model_name: str,
    split_name: str,
) -> dict[str, Any]:
    clean = snapshot.dropna(subset=["target"]).copy()
    clean["target"] = clean["target"].astype(int)

    if split_name == "temporal":
        years = sorted(pd.to_numeric(clean["academic_year"], errors="coerce").unique())
        if len(years) < 2:
            raise ValueError("validação temporal exige pelo menos dois anos acadêmicos")
        test_year = years[-1]
        train = clean[clean["academic_year"] < test_year]
        test = clean[clean["academic_year"] == test_year]
    elif split_name == "grouped":
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=20261004)
        train_idx, test_idx = next(splitter.split(clean, clean["target"], groups=clean["student_id"]))
        train = clean.iloc[train_idx]
        test = clean.iloc[test_idx]
    else:
        raise ValueError(f"divisão desconhecida: {split_name}")

    estimator = _models()[model_name]
    estimator.fit(train[features], train["target"])
    predicted = estimator.predict(test[features])
    probabilities = estimator.predict_proba(test[features])

    recalls = recall_score(test["target"], predicted, labels=[0, 1, 2], average=None, zero_division=0)
    return {
        "model": model_name,
        "cutoff": cutoff,
        "split": split_name,
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "test_year": int(test["academic_year"].iloc[0]) if split_name == "temporal" else None,
        "accuracy": float(accuracy_score(test["target"], predicted)),
        "balanced_accuracy": float(balanced_accuracy_score(test["target"], predicted)),
        "f1_macro": float(f1_score(test["target"], predicted, average="macro")),
        "f1_weighted": float(f1_score(test["target"], predicted, average="weighted")),
        "recall_reprovado": float(recalls[0]),
        "recall_recuperacao": float(recalls[1]),
        "recall_aprovado": float(recalls[2]),
        "log_loss": float(log_loss(test["target"], probabilities, labels=[0, 1, 2])),
        "brier_multiclass": _multiclass_brier(test["target"].to_numpy(), probabilities),
        "confusion_matrix": confusion_matrix(test["target"], predicted, labels=[0, 1, 2]).tolist(),
        "features": features,
    }


def run_benchmark(input_path: Path, output_path: Path) -> dict[str, Any]:
    data = pd.read_csv(input_path)
    results: list[dict[str, Any]] = []

    for cutoff, features in SNAPSHOT_FEATURES.items():
        snapshot = build_snapshot(data, cutoff)
        for split in ("temporal", "grouped"):
            for model_name in _models():
                results.append(_run_one(snapshot, cutoff, features, model_name, split))

    report = {
        "input": str(input_path),
        "seed": 20261004,
        "protocol": {
            "target": "status_encoded: 0=reprovado, 1=recuperação, 2=aprovado",
            "cutoffs": list(SNAPSHOT_FEATURES),
            "forbidden_in_features": ["n4", "final_score", "media_pond_norm", "target", "status"],
            "official_status": "initial_experiment; not yet final article result",
        },
        "results": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=root / "research/reports/initial_benchmark.json")
    args = parser.parse_args()

    report = run_benchmark(args.input, args.output)
    print(f"resultados={len(report['results'])}")
    print(f"output={args.output}")
    for result in report["results"]:
        print(
            f"{result['split']:8} {result['cutoff']:6} {result['model']:20} "
            f"F1_macro={result['f1_macro']:.4f} recall_reprovado={result['recall_reprovado']:.4f}"
        )


if __name__ == "__main__":
    main()
