import pandas as pd

from research.features.temporal_snapshots import SNAPSHOT_FEATURES, build_all_snapshots


def sample_data() -> pd.DataFrame:
    return pd.DataFrame({
        "student_id": ["stu_1", "stu_2"],
        "school_id": ["school_1", "school_1"],
        "academic_year": [2025, 2025],
        "serie_num": [6, 7],
        "n1": [4.0, 8.0], "n2": [5.0, 8.5], "n3": [5.5, 8.0], "n4": [4.0, 9.0],
        "attendance_n1": [0.70, 0.95], "attendance_n2": [0.72, 0.94], "attendance_n3": [0.75, 0.93],
        "status_encoded": [0, 2],
    })


def test_snapshots_do_not_include_future_or_target_columns():
    snapshots = build_all_snapshots(sample_data())
    for name, frame in snapshots.items():
        assert set(SNAPSHOT_FEATURES[name]).issubset(frame.columns)
        assert "n4" not in frame.columns
        assert "target" in frame.columns
        assert "status_encoded" not in frame.columns
        assert "final_score" not in frame.columns


def test_snapshots_keep_expected_progression():
    snapshots = build_all_snapshots(sample_data())
    assert snapshots["M1"].iloc[0]["n1_norm"] == 0.4
    assert snapshots["M2"].iloc[0]["n2_norm"] == 0.5
    assert snapshots["M3"].iloc[0]["n3_norm"] == 0.55

