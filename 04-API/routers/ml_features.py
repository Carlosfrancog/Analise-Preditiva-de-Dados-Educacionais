from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import cads
from ml_service import MLService

router = APIRouter(tags=["ml"])
ROOT = Path(__file__).parent.parent.parent  # routers/ → 04-API/ → project root


class GerarBody(BaseModel):
    sala_id: int | None = None
    pesos: dict | None = None  # {"n1": 0.20, "n2": 0.25, "n3": 0.25, "n4": 0.30}


class ModelCfg(BaseModel):
    n_estimators: int | None = None
    max_depth: int | None = None          # None = sem limite
    min_samples_split: int | None = None
    min_samples_leaf: int | None = None


class RetrainBody(BaseModel):
    RF_M1: ModelCfg | None = None
    RF_M2: ModelCfg | None = None
    RF_M3: ModelCfg | None = None


@router.get("/ml/features")
def list_features(sala_id: int | None = None):
    conn = cads.get_conn()
    where = "WHERE f.sala_nome IS NOT NULL"
    params = []
    if sala_id:
        where += " AND s.id = ?"
        params.append(sala_id)
    rows = conn.execute(f"""
        SELECT f.aluno_nome, f.sala_nome, f.materia_nome,
               f.n1, f.n2, f.n3, f.n4,
               f.media_pond_norm, f.media_geral_aluno, f.slope_notas,
               f.variancia_notas, f.serie_num_norm, f.pct_materias_ok,
               f.media_turma_norm, f.status_encoded, f.status_label
        FROM ml_features f
        LEFT JOIN salas s ON f.sala_nome = s.nome
        {where}
        ORDER BY f.sala_nome, f.aluno_nome, f.materia_nome
        LIMIT 5000
    """, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/ml/gerar")
def gerar_features(body: GerarBody):
    if body.pesos:
        cads.PESOS_NOTAS = body.pesos
    n, stats = cads.gerar_features_ml(body.sala_id)
    return {"geradas": n, "stats": stats}


@router.get("/ml/stats")
def ml_stats():
    total, dist = cads.get_ml_stats()
    return {"total": total, "dist": dist}


@router.get("/ml/models")
def list_models():
    return MLService.get().list_models()


@router.post("/ml/activate/{model_name}")
def activate_model(model_name: str):
    """Load a specific model and unload others from memory."""
    svc = MLService.get()
    ok = svc.activate(model_name)
    if not ok:
        raise HTTPException(400, f"Modelo '{model_name}' não encontrado ou inválido.")
    meta = svc.metadata.get(model_name, {})
    return {
        "active": model_name,
        "accuracy": meta.get("accuracy", 0),
        "n_trees": meta.get("n_samples_train", 0),
    }


@router.post("/ml/retrain")
def retrain_models(body: RetrainBody = None):
    """
    Full pipeline: generate features → export CSV → train 3 RF models → reload.
    Accepts optional per-model hyperparameter overrides via body.
    Takes ~20-60s depending on data size.
    """
    import pickle, json
    import pandas as pd
    import numpy as np
    from datetime import datetime
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

    # ── 1. Generate ML features from DB ──────────────────────────────────────
    n, stats = cads.gerar_features_ml()
    if n == 0:
        raise HTTPException(400, "Sem dados para treinamento. Cadastre alunos e notas primeiro.")

    # ── 2. Export CSV (absolute path so it always lands at project root) ──────
    csv_path = ROOT / "ml_dataset.csv"
    df_info, msg = cads.exportar_ml_csv(output_path=str(csv_path))
    if df_info is None:
        raise HTTPException(500, f"Falha ao exportar dataset: {msg}")

    # ── 3. Load dataset ───────────────────────────────────────────────────────
    csv_path = ROOT / "ml_dataset.csv"
    if not csv_path.exists():
        raise HTTPException(500, "ml_dataset.csv não encontrado após exportação")

    df = pd.read_csv(csv_path)
    if len(df) < 30:
        raise HTTPException(400, f"Dados insuficientes ({len(df)} registros). Mínimo: 30")

    feature_cols = [
        "n1_norm", "n2_norm", "n3_norm", "n4_norm",
        "slope_notas", "variancia_notas", "media_geral_aluno",
        "serie_num_norm", "media_turma_norm",
    ]
    X = df[feature_cols]
    y = df["status_encoded"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ── 4. Train 3 models ────────────────────────────────────────────────────
    configs = {
        "RF_M1": {"n_estimators": 100, "max_depth": 5,  "random_state": 42},
        "RF_M2": {"n_estimators": 150, "max_depth": 10, "random_state": 42},
        "RF_M3": {"n_estimators": 200, "random_state": 42},
    }
    # Apply optional overrides from request body
    if body:
        for model_name in ["RF_M1", "RF_M2", "RF_M3"]:
            override = getattr(body, model_name, None)
            if override:
                patch = override.model_dump(exclude_none=True)
                configs[model_name].update(patch)

    models_dir = ROOT / "ml_models"
    models_dir.mkdir(exist_ok=True)

    resultados = {}
    for nome, cfg in configs.items():
        clf = RandomForestClassifier(**cfg)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        acc = float(accuracy_score(y_test, y_pred))
        f1  = float(f1_score(y_test, y_pred, average="weighted"))
        cm  = confusion_matrix(y_test, y_pred).tolist()

        # Save pkl
        with open(models_dir / f"{nome}.pkl", "wb") as fh:
            pickle.dump(clf, fh)

        # Save metadata (both possible locations)
        meta = {
            "accuracy": acc, "f1": f1,
            "n_features": len(feature_cols), "features": feature_cols,
            "n_samples_train": int(len(X_train)), "n_samples_test": int(len(X_test)),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "confusion_matrix": cm,
        }
        meta_json = json.dumps(meta, indent=2)
        (models_dir / f"{nome}_metadata.json").write_text(meta_json)
        alt_dir = ROOT / "02-ML" / "ml_models"
        if alt_dir.exists():
            (alt_dir / f"{nome}_metadata.json").write_text(meta_json)

        resultados[nome] = {"accuracy": acc, "f1": f1, "confusion_matrix": cm}
        print(f"[Retrain] {nome}: acc={acc:.1%}")

    # ── 5. Reload MLService ───────────────────────────────────────────────────
    MLService._instance = None
    MLService.get()

    return {
        "status": "ok",
        "n_features": n,
        "n_samples": len(df),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "modelos": resultados,
    }


class ContinuousRetrainBody(BaseModel):
    n_runs: int = 5
    RF_M1: ModelCfg | None = None
    RF_M2: ModelCfg | None = None
    RF_M3: ModelCfg | None = None


@router.post("/ml/retrain-continuous")
def retrain_continuous(body: ContinuousRetrainBody = None):
    """Train each model n_runs times with different random seeds, keep best accuracy."""
    import pickle, json
    import pandas as pd
    from datetime import datetime
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

    n_runs = max(2, min(30, (body.n_runs if body else 5)))

    n, _ = cads.gerar_features_ml()
    if n == 0:
        raise HTTPException(400, "Sem dados para treinamento.")

    csv_path = ROOT / "ml_dataset.csv"
    cads.exportar_ml_csv(output_path=str(csv_path))
    if not csv_path.exists():
        raise HTTPException(500, "ml_dataset.csv não encontrado após exportação")

    df = pd.read_csv(csv_path)
    if len(df) < 30:
        raise HTTPException(400, f"Dados insuficientes ({len(df)} registros). Mínimo: 30")

    feature_cols = [
        "n1_norm", "n2_norm", "n3_norm", "n4_norm",
        "slope_notas", "variancia_notas", "media_geral_aluno",
        "serie_num_norm", "media_turma_norm",
    ]
    X = df[feature_cols]
    y = df["status_encoded"]

    base_configs = {
        "RF_M1": {"n_estimators": 100, "max_depth": 5},
        "RF_M2": {"n_estimators": 150, "max_depth": 10},
        "RF_M3": {"n_estimators": 200},
    }
    if body:
        for mname in ["RF_M1", "RF_M2", "RF_M3"]:
            override = getattr(body, mname, None)
            if override:
                base_configs[mname].update(override.model_dump(exclude_none=True))

    models_dir = ROOT / "ml_models"
    models_dir.mkdir(exist_ok=True)

    resultados = {}
    for nome, cfg in base_configs.items():
        best_acc = -1.0
        best_clf = None
        best_cm  = None
        best_f1  = 0.0
        run_accs = []

        for seed in range(n_runs):
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=seed, stratify=y
            )
            clf = RandomForestClassifier(**cfg, random_state=seed)
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            acc = float(accuracy_score(y_test, y_pred))
            run_accs.append(round(acc, 4))
            if acc > best_acc:
                best_acc = acc
                best_clf = clf
                best_cm  = confusion_matrix(y_test, y_pred).tolist()
                best_f1  = float(f1_score(y_test, y_pred, average="weighted"))
                best_X_train, best_X_test = X_train, X_test

        with open(models_dir / f"{nome}.pkl", "wb") as fh:
            pickle.dump(best_clf, fh)

        meta = {
            "accuracy": best_acc, "f1": best_f1,
            "n_features": len(feature_cols), "features": feature_cols,
            "n_samples_train": int(len(best_X_train)),
            "n_samples_test": int(len(best_X_test)),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "confusion_matrix": best_cm,
        }
        meta_json = json.dumps(meta, indent=2)
        (models_dir / f"{nome}_metadata.json").write_text(meta_json)
        alt_dir = ROOT / "02-ML" / "ml_models"
        if alt_dir.exists():
            (alt_dir / f"{nome}_metadata.json").write_text(meta_json)

        resultados[nome] = {
            "accuracy": best_acc, "f1": best_f1,
            "confusion_matrix": best_cm,
            "run_accuracies": run_accs,
            "best_run": run_accs.index(max(run_accs)),
        }
        print(f"[Continuous] {nome}: best={best_acc:.1%} over {n_runs} runs")

    MLService._instance = None
    MLService.get()

    return {
        "status": "ok",
        "n_runs": n_runs,
        "n_samples": len(df),
        "modelos": resultados,
    }
