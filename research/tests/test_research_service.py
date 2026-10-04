from pathlib import Path
from unittest.mock import patch

import pandas as pd

from research.models.artifacts import load_artifact, train_and_save_artifacts
from research.services.research_service import ResearchService


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
