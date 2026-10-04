from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from research.models.artifacts import (
    clear_artifact_cache,
    load_artifact,
    train_and_save_artifacts,
)
from research.services.research_service import ResearchService, ResearchServiceError


def _write_snapshots(root: Path) -> None:
    snapshot_dir = root / "research" / "data" / "snapshots"
    snapshot_dir.mkdir(parents=True)
    rows = []
    for index, target in enumerate([0, 1, 2]):
        rows.append({
            "student_id": f"stu_{index}",
            "school_id": "school_1",
            "subject_id": "subject_1",
            "academic_year": 2024,
            "target": target,
            "n1_norm": [0.2, 0.55, 0.85][index],
            "n2_norm": [0.25, 0.60, 0.90][index],
            "n3_norm": [0.30, 0.65, 0.95][index],
            "attendance_n1": [0.65, 0.80, 0.95][index],
            "attendance_n2": [0.66, 0.81, 0.96][index],
            "attendance_n3": [0.67, 0.82, 0.97][index],
            "serie_num_norm": [0.0, 0.5, 1.0][index],
            "slope_n1_n2": 0.05,
            "slope_n1_n3": 0.05,
            "variance_n1_n2": 0.01,
            "variance_n1_n3": 0.01,
        })
    frame = pd.DataFrame(rows)
    for cutoff in ("M1", "M2", "M3"):
        frame.to_csv(snapshot_dir / f"experimental_dataset_{cutoff}.csv", index=False)


def test_research_service_reads_catalog_and_predicts(tmp_path):
    clear_artifact_cache()
    _write_snapshots(tmp_path)
    train_and_save_artifacts(
        tmp_path / "research" / "data" / "snapshots",
        tmp_path / "research" / "artifacts",
    )

    service = ResearchService(tmp_path)
    catalog = service.catalog()
    assert [(item["cutoff"], item["model_available"]) for item in catalog] == [
        ("M1", True), ("M2", True), ("M3", True)
    ]
    assert all(item["source"] == "synthetic" for item in catalog)

    first_model, _ = load_artifact(service.artifact_dir, "M2")
    second_model, _ = load_artifact(service.artifact_dir, "M2")
    assert first_model is second_model

    with patch(
        "research.services.research_service.load_artifact",
        wraps=load_artifact,
    ) as artifact_loader:
        samples = service.samples("M2", limit=3)

    assert artifact_loader.call_count == 1
    assert all("prediction" in item for item in samples)
    sample = samples[0]
    assert sample["student_id"] == "stu_0"
    assert sample["prediction"]["cutoff"] == "M2"
    assert set(sample["prediction"]["features"]) == {
        "n1_norm", "n2_norm", "slope_n1_n2", "variance_n1_n2",
        "attendance_n2", "serie_num_norm",
    }

    (service.artifact_dir / "M3.pkl").unlink()
    refreshed = service.catalog()
    assert next(item for item in refreshed if item["cutoff"] == "M3")[
        "model_available"
    ] is False


def test_manual_prediction_rejects_invalid_feature_contract(tmp_path):
    clear_artifact_cache()
    _write_snapshots(tmp_path)
    train_and_save_artifacts(
        tmp_path / "research" / "data" / "snapshots",
        tmp_path / "research" / "artifacts",
    )
    service = ResearchService(tmp_path)
    valid = {
        "n1_norm": 0.7,
        "attendance_n1": 0.9,
        "serie_num_norm": 0.5,
    }

    with pytest.raises(ResearchServiceError, match="features ausentes"):
        service.predict_features("M1", {"n1_norm": 0.7})
    with pytest.raises(ResearchServiceError, match="features inválidas"):
        service.predict_features("M1", {**valid, "n4_norm": 0.8})
    with pytest.raises(ResearchServiceError, match="fora do intervalo"):
        service.predict_features("M1", {**valid, "n1_norm": 1.2})
    with pytest.raises(ResearchServiceError, match="deve ser finita"):
        service.predict_features("M1", {**valid, "n1_norm": float("nan")})


def test_samples_preserve_missing_values_for_the_ui(tmp_path):
    clear_artifact_cache()
    _write_snapshots(tmp_path)
    train_and_save_artifacts(
        tmp_path / "research" / "data" / "snapshots",
        tmp_path / "research" / "artifacts",
    )
    snapshot_path = (
        tmp_path / "research" / "data" / "snapshots" / "experimental_dataset_M2.csv"
    )
    snapshot = pd.read_csv(snapshot_path)
    snapshot.loc[0, "n2_norm"] = float("nan")
    snapshot.to_csv(snapshot_path, index=False)

    sample = ResearchService(tmp_path).samples("M2", limit=1)[0]
    assert sample["n2_norm"] is None
    assert sample["prediction"]["features"]["n2_norm"] is None
