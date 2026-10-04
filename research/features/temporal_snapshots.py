#!/usr/bin/env python3
"""Constrói os snapshots M1/M2/M3 com features disponíveis no corte."""

from __future__ import annotations

from pathlib import Path
import argparse

import numpy as np
import pandas as pd


SNAPSHOT_FEATURES = {
    "M1": ["n1_norm", "attendance_n1", "serie_num_norm"],
    "M2": ["n1_norm", "n2_norm", "slope_n1_n2", "variance_n1_n2", "attendance_n2", "serie_num_norm"],
    "M3": ["n1_norm", "n2_norm", "n3_norm", "slope_n1_n3", "variance_n1_n3", "attendance_n3", "serie_num_norm"],
}

FORBIDDEN_FEATURE_TOKENS = (
    "n4", "final", "target", "status", "label", "media_pond", "future"
)


def _norm(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").clip(0, 10).div(10.0)


def _series_norm(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    return ((values - 6.0) / 6.0).clip(0, 1)


def _variance(frame: pd.DataFrame) -> pd.Series:
    return frame.std(axis=1, ddof=0).fillna(0.0).clip(0, 10).div(10.0)


def build_snapshot(df: pd.DataFrame, model_name: str) -> pd.DataFrame:
    if model_name not in SNAPSHOT_FEATURES:
        raise ValueError(f"modelo temporal desconhecido: {model_name}")

    required = {"n1", "n2", "n3", "n4", "status_encoded"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"colunas obrigatórias ausentes: {missing}")

    data = df.copy()
    for column in ("n1", "n2", "n3", "n4", "status_encoded", "serie_num"):
        if column in data:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    result = pd.DataFrame(index=data.index)
    result["student_id"] = data.get("student_id", data.get("aluno", "unknown"))
    result["school_id"] = data.get("school_id", data.get("turma", "unknown"))
    result["subject_id"] = data.get("subject_id", data.get("materia", "unknown"))
    result["academic_year"] = data.get("academic_year", 0)
    result["target"] = data["status_encoded"].astype("Int64")
    result["cutoff"] = model_name

    result["n1_norm"] = _norm(data["n1"])
    result["n2_norm"] = _norm(data["n2"])
    result["n3_norm"] = _norm(data["n3"])
    result["serie_num_norm"] = _series_norm(data.get("serie_num", pd.Series(6, index=data.index)))

    if "attendance_n1" in data:
        result["attendance_n1"] = pd.to_numeric(data["attendance_n1"], errors="coerce").clip(0, 1)
        result["attendance_n2"] = pd.to_numeric(data.get("attendance_n2"), errors="coerce").clip(0, 1)
        result["attendance_n3"] = pd.to_numeric(data.get("attendance_n3"), errors="coerce").clip(0, 1)
    else:
        result[["attendance_n1", "attendance_n2", "attendance_n3"]] = np.nan

    result["slope_n1_n2"] = result["n2_norm"] - result["n1_norm"]
    result["slope_n1_n3"] = (result["n3_norm"] - result["n1_norm"]) / 2.0
    result["variance_n1_n2"] = _variance(result[["n1_norm", "n2_norm"]])
    result["variance_n1_n3"] = _variance(result[["n1_norm", "n2_norm", "n3_norm"]])

    features = SNAPSHOT_FEATURES[model_name]
    forbidden = [f for f in features if any(token in f.lower() for token in FORBIDDEN_FEATURE_TOKENS)]
    if forbidden:
        raise AssertionError(f"features proibidas no snapshot {model_name}: {forbidden}")

    return result[["student_id", "school_id", "subject_id", "academic_year", "cutoff", "target", *features]]


def build_all_snapshots(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {name: build_snapshot(df, name) for name in SNAPSHOT_FEATURES}


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path, default=root / "research/data/snapshots")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, snapshot in build_all_snapshots(df).items():
        output = args.output_dir / f"{args.input.stem}_{name}.csv"
        snapshot.to_csv(output, index=False)
        print(f"{name}: {len(snapshot)} linhas -> {output}")


if __name__ == "__main__":
    main()
