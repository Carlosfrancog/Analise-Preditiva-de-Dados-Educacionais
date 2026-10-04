#!/usr/bin/env python3
"""Gera uma base sintética temporal para os experimentos do artigo.

A base é deliberadamente parametrizável e reproduzível. O resultado não é
apresentado como dado real: ele serve para validar o pipeline, os testes de
leakage e o fluxo completo da aplicação sem expor estudantes.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from pathlib import Path
import json

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DatasetConfig:
    seed: int = 20261004
    students: int = 1200
    schools: int = 6
    subjects: int = 13
    years: int = 4

    @property
    def rows(self) -> int:
        return self.students * self.subjects * self.years


def _status(score: float) -> int:
    if score < 5.0:
        return 0  # reprovado
    if score < 6.0:
        return 1  # recuperação
    return 2  # aprovado


def generate_dataset(config: DatasetConfig) -> pd.DataFrame:
    rng = np.random.default_rng(config.seed)

    student_ids = np.arange(1, config.students + 1)
    school_by_student = rng.integers(1, config.schools + 1, size=config.students)
    student_ability = np.clip(rng.normal(6.3, 1.25, size=config.students), 2.0, 9.2)
    student_attendance = np.clip(rng.normal(0.88, 0.08, size=config.students), 0.45, 1.0)

    rows: list[dict] = []
    for year in range(1, config.years + 1):
        year_drift = (year - 1) * rng.normal(0.04, 0.02)
        for student_idx, student_id in enumerate(student_ids):
            school_id = int(school_by_student[student_idx])
            ability = student_ability[student_idx] + year_drift
            attendance_base = student_attendance[student_idx]

            for subject_id in range(1, config.subjects + 1):
                difficulty = rng.normal(0.0, 0.48)
                base = ability - difficulty
                progression = rng.normal(0.08, 0.18)

                notes = []
                attendance = []
                for bimester in range(1, 5):
                    score = base + progression * (bimester - 1) + rng.normal(0, 0.72)
                    notes.append(float(np.clip(score, 0.0, 10.0)))
                    rate = attendance_base + rng.normal(0, 0.025) - max(0, 5.8 - base) * 0.012
                    attendance.append(float(np.clip(rate, 0.30, 1.0)))

                final_score = (0.20 * notes[0] + 0.25 * notes[1] +
                               0.25 * notes[2] + 0.30 * notes[3])
                rows.append({
                    "student_id": f"stu_{student_id:05d}",
                    "school_id": f"school_{school_id:02d}",
                    "academic_year": 2022 + year,
                    "subject_id": f"subject_{subject_id:02d}",
                    "serie_num": int(6 + ((student_idx + year - 1) % 7)),
                    "n1": round(notes[0], 4),
                    "n2": round(notes[1], 4),
                    "n3": round(notes[2], 4),
                    "n4": round(notes[3], 4),
                    "attendance_n1": round(attendance[0], 4),
                    "attendance_n2": round(np.mean(attendance[:2]), 4),
                    "attendance_n3": round(np.mean(attendance[:3]), 4),
                    "attendance_n4": round(np.mean(attendance), 4),
                    "final_score": round(final_score, 4),
                    "status_encoded": _status(final_score),
                    "status_label": {
                        0: "Reprovado", 1: "Recuperação", 2: "Aprovado"
                    }[_status(final_score)],
                })

    return pd.DataFrame(rows)


def write_dataset(config: DatasetConfig, output: Path) -> tuple[Path, Path]:
    output.parent.mkdir(parents=True, exist_ok=True)
    df = generate_dataset(config)
    df.to_csv(output, index=False)

    manifest_path = output.with_suffix(".manifest.json")
    manifest = {
        "dataset": output.name,
        "generator": "research.data.generate_dataset",
        "config": asdict(config),
        "rows": int(len(df)),
        "classes": df["status_label"].value_counts().to_dict(),
        "privacy": "synthetic; no real student records",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return output, manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("research/data/generated/experimental_dataset.csv"))
    parser.add_argument("--seed", type=int, default=DatasetConfig.seed)
    parser.add_argument("--students", type=int, default=DatasetConfig.students)
    parser.add_argument("--schools", type=int, default=DatasetConfig.schools)
    parser.add_argument("--subjects", type=int, default=DatasetConfig.subjects)
    parser.add_argument("--years", type=int, default=DatasetConfig.years)
    args = parser.parse_args()

    config = DatasetConfig(args.seed, args.students, args.schools, args.subjects, args.years)
    output, manifest = write_dataset(config, args.output)
    print(f"dataset={output} rows={config.rows}")
    print(f"manifest={manifest}")


if __name__ == "__main__":
    main()

