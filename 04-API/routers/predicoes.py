"""
Predições — análise de desempenho por aluno + extração de árvore de decisão.
"""
import numpy as np
from collections import defaultdict
from fastapi import APIRouter, HTTPException
import cads
from ml_service import MLService

router = APIRouter(tags=["predicoes"])

SERIE_MAP = {
    "6f": 0.00, "6": 0.00,
    "7f": 0.17, "7": 0.17,
    "8f": 0.33, "8": 0.33,
    "9f": 0.50, "9": 0.50,
    "1m": 0.67, "em1": 0.67,
    "2m": 0.83, "em2": 0.83,
    "3m": 1.00, "em3": 1.00,
}


def _serie_norm(codigo: str) -> float:
    c = str(codigo or "").lower().replace("º", "").replace("°", "").strip()
    for k, v in SERIE_MAP.items():
        if k in c:
            return v
    return 0.5


def _calc_media(n1, n2, n3, n4, tipo_media: str = 'ponderada', arredondamento: bool = False) -> float | None:
    if tipo_media == 'simples':
        vals = [n for n in [n1, n2, n3, n4] if n > 0]
        if not vals:
            return None
        m = sum(vals) / len(vals)
    else:
        filled = [(n, w) for n, w in [(n1, 0.20), (n2, 0.25), (n3, 0.25), (n4, 0.30)] if n > 0]
        if not filled:
            return None
        total_w = sum(w for _, w in filled)
        m = sum(n * w for n, w in filled) / total_w
    return 6.0 if arredondamento and m >= 5.75 else m


def _fetch_disciplinas(
    aluno_id: int,
    conn,
    tipo_media: str = 'ponderada',
    arredondamento: bool = False,
) -> tuple[dict, list]:
    """Returns (aluno_row, disciplinas_list). disciplinas include per-norm fields."""
    aluno = conn.execute(
        """SELECT a.id, a.nome, a.matricula,
                  s.nome AS sala_nome, s.codigo AS sala_codigo
           FROM alunos a LEFT JOIN salas s ON a.sala_id = s.id
           WHERE a.id = ?""",
        (aluno_id,),
    ).fetchone()
    if not aluno:
        return None, []

    rows = conn.execute(
        """SELECT m.id, m.nome, n.n1, n.n2, n.n3, n.n4
           FROM notas n JOIN materias m ON n.materia_id = m.id
           WHERE n.aluno_id = ?
           ORDER BY m.nome""",
        (aluno_id,),
    ).fetchall()

    disciplinas = []
    for r in rows:
        n1, n2, n3, n4 = (float(r[i] or 0) for i in range(2, 6))
        media = _calc_media(n1, n2, n3, n4, tipo_media, arredondamento)
        if media is None:
            continue

        values = [n for n in [n1, n2, n3, n4] if n > 0]
        slope = (n2 - n1) / 10.0 if n1 > 0 and n2 > 0 else 0.0
        variancia = float(np.std(values) / 5.0) if len(values) > 1 else 0.0
        status = 0 if media < 5 else (1 if media < 6 else 2)
        notas_count = len(values)

        disciplinas.append({
            "id": r[0],
            "nome": r[1],
            "n1": n1, "n2": n2, "n3": n3, "n4": n4,
            "n1_norm": round(n1 / 10, 3),
            "n2_norm": round(n2 / 10, 3),
            "n3_norm": round(n3 / 10, 3),
            "n4_norm": round(n4 / 10, 3),
            "media": round(media, 2),
            "slope_notas": round(slope, 4),
            "variancia_notas": round(variancia, 4),
            "status": status,
            "status_name": {0: "Reprovado", 1: "Recuperação", 2: "Aprovado"}[status],
            "notas_count": notas_count,
            "completa": n4 > 0,
        })

    return aluno, disciplinas


def _feature_vector_for(disc: dict, media_geral: float, serie: float, media_turma: float) -> list:
    return [
        disc["n1_norm"], disc["n2_norm"], disc["n3_norm"], disc["n4_norm"],
        disc["slope_notas"], disc["variancia_notas"],
        round(media_geral, 4),
        round(serie, 4),
        round(media_turma, 4),
    ]


def _feature_dict_for(disc: dict, media_geral: float, serie: float, media_turma: float) -> dict:
    return {
        "n1_norm": disc["n1_norm"],
        "n2_norm": disc["n2_norm"],
        "n3_norm": disc["n3_norm"],
        "n4_norm": disc["n4_norm"],
        "slope_notas": disc["slope_notas"],
        "variancia_notas": disc["variancia_notas"],
        "media_geral_aluno": round(media_geral, 4),
        "serie_num_norm": round(serie, 4),
        "media_turma_norm": round(media_turma, 4),
    }


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/predicoes/salas")
def get_salas():
    return cads.get_salas()


@router.get("/predicoes/alunos/{sala_id}")
def get_alunos(sala_id: int):
    return cads.get_alunos(sala_id)


@router.get("/predicoes/turma-rapida/{sala_id}")
def turma_rapida(sala_id: int):
    """
    Lightweight batch stats for the Alunos list page.
    Grade-math only (no ML) — runs in a single DB query, no per-student ML inference.
    Returns per-student: media_geral, n_risco, n_atencao, grade-based status.
    """
    conn = cads.get_conn()

    alunos_list = conn.execute(
        "SELECT id, nome, matricula FROM alunos WHERE sala_id = ? ORDER BY nome",
        (sala_id,),
    ).fetchall()

    if not alunos_list:
        conn.close()
        return []

    aluno_ids = [a["id"] for a in alunos_list]
    placeholders = ",".join("?" * len(aluno_ids))

    notas_rows = conn.execute(
        f"""SELECT n.aluno_id, n.n1, n.n2, n.n3, n.n4
            FROM notas n
            WHERE n.aluno_id IN ({placeholders})""",
        aluno_ids,
    ).fetchall()
    conn.close()

    notas_by_aluno: dict = defaultdict(list)
    for r in notas_rows:
        n1, n2, n3, n4 = (float(r[i] or 0) for i in range(1, 5))
        filled = [(n, w) for n, w in [(n1, 0.20), (n2, 0.25), (n3, 0.25), (n4, 0.30)] if n > 0]
        if filled:
            total_w = sum(w for _, w in filled)
            media = sum(n * w for n, w in filled) / total_w
            notas_by_aluno[r["aluno_id"]].append(media)

    CLS = {
        0: ("Reprovado",   "#EF4444"),
        1: ("Recuperação", "#F59E0B"),
        2: ("Aprovado",    "#10B981"),
    }

    result = []
    for a in alunos_list:
        medias = notas_by_aluno[a["id"]]
        if not medias:
            result.append({
                "id": a["id"], "nome": a["nome"], "matricula": a["matricula"],
                "media_geral": None, "n_disciplinas": 0,
                "n_risco": 0, "n_atencao": 0, "status": None,
            })
            continue

        mg = float(np.mean(medias))
        n_risco   = sum(1 for m in medias if m < 5.0)
        n_atencao = sum(1 for m in medias if 5.0 <= m < 6.0)
        cv = 2 if mg >= 6.0 else (1 if mg >= 5.0 else 0)

        result.append({
            "id": a["id"],
            "nome": a["nome"],
            "matricula": a["matricula"],
            "media_geral": round(mg, 2),
            "n_disciplinas": len(medias),
            "n_risco": n_risco,
            "n_atencao": n_atencao,
            "status": {"class_value": cv, "class_name": CLS[cv][0], "class_color": CLS[cv][1]},
        })

    return result


@router.get("/predicoes/analyze/{aluno_id}")
def analyze_student(
    aluno_id: int,
    model: str = "RF_M3",
    tipo_media: str = "ponderada",
    arredondamento: bool = False,
):
    """
    Returns all disciplines with their stats + per-discipline ML prediction +
    aggregate ensemble prediction (mean feature vector across all disciplines).
    """
    conn = cads.get_conn()
    aluno, disciplinas = _fetch_disciplinas(aluno_id, conn, tipo_media, arredondamento)
    conn.close()

    if not aluno or not disciplinas:
        raise HTTPException(404, "Aluno não encontrado ou sem notas lançadas")

    serie = _serie_norm(aluno["sala_codigo"])
    media_geral = float(np.mean([d["media"] for d in disciplinas])) / 10.0
    media_turma = media_geral  # approximation

    svc = MLService.get()

    # Per-discipline prediction
    for d in disciplinas:
        fv = _feature_vector_for(d, media_geral, serie, media_turma)
        if svc.is_available(model):
            try:
                pred = svc.predict_ensemble(model, fv)
                d["predicao"] = pred
            except Exception as e:
                print(f"[pred] {e}")
                d["predicao"] = None
        else:
            d["predicao"] = None

    # Aggregate ensemble — mean feature vector across ALL disciplines
    ensemble = None
    if svc.is_available(model):
        try:
            fv_agg = [
                float(np.mean([d["n1_norm"]         for d in disciplinas])),
                float(np.mean([d["n2_norm"]         for d in disciplinas])),
                float(np.mean([d["n3_norm"]         for d in disciplinas])),
                float(np.mean([d["n4_norm"]         for d in disciplinas])),
                float(np.mean([d["slope_notas"]     for d in disciplinas])),
                float(np.mean([d["variancia_notas"] for d in disciplinas])),
                media_geral,
                serie,
                media_turma,
            ]
            ensemble = svc.predict_ensemble(model, fv_agg)
        except Exception as e:
            print(f"[Ensemble] {e}")

    worst = min(disciplinas, key=lambda d: d["media"])

    return {
        "aluno": {
            "id": aluno["id"],
            "nome": aluno["nome"],
            "matricula": aluno["matricula"],
            "sala": aluno["sala_nome"],
        },
        "disciplinas": disciplinas,
        "ensemble": ensemble,
        "media_geral": round(float(np.mean([d["media"] for d in disciplinas])), 2),
        "pct_ok": round(len([d for d in disciplinas if d["status"] == 2]) / len(disciplinas), 3),
        "worst_materia_id": worst["id"],
        "tipo_media": tipo_media,
        "arredondamento": arredondamento,
    }


@router.get("/predicoes/tree/{aluno_id}")
def get_decision_tree(
    aluno_id: int,
    materia_id: int = None,
    model: str = "RF_M3",
    tree_idx: int = 0,
):
    """
    Returns the D3-ready decision tree path for a student + specific discipline.
    If materia_id is omitted, uses the worst-performing discipline.
    """
    conn = cads.get_conn()
    aluno, disciplinas = _fetch_disciplinas(aluno_id, conn)
    conn.close()

    if not aluno or not disciplinas:
        raise HTTPException(404, "Aluno não encontrado ou sem notas lançadas")

    svc = MLService.get()
    if not svc.is_available(model):
        raise HTTPException(404, f"Modelo {model} não disponível.")

    serie = _serie_norm(aluno["sala_codigo"])
    media_geral = float(np.mean([d["media"] for d in disciplinas])) / 10.0
    media_turma = media_geral

    # Pick target discipline
    if materia_id:
        disc = next((d for d in disciplinas if d["id"] == materia_id), None)
        if not disc:
            raise HTTPException(404, f"Disciplina {materia_id} não encontrada para este aluno")
    else:
        disc = min(disciplinas, key=lambda d: d["media"])

    fv = _feature_vector_for(disc, media_geral, serie, media_turma)
    fd = _feature_dict_for(disc, media_geral, serie, media_turma)

    result = svc.extract_decision_path(model, fv, tree_idx)
    if not result:
        raise HTTPException(500, "Falha ao extrair caminho da árvore")

    return {
        "aluno": {
            "id": aluno["id"],
            "nome": aluno["nome"],
            "matricula": aluno["matricula"],
            "sala": aluno["sala_nome"],
        },
        "features": fd,
        "focus_disciplina": disc["nome"],
        "focus_materia_id": disc["id"],
        "media_geral": round(float(np.mean([d["media"] for d in disciplinas])), 2),
        **result,
    }


@router.get("/predicoes/timelapse/{aluno_id}")
def get_timelapse(
    aluno_id: int,
    materia_id: int = None,
    model: str = "RF_M3",
):
    """
    Returns the per-estimator vote sequence for the ensemble timelapse animation.
    Each element is the class (0/1/2) predicted by one individual tree.
    """
    conn = cads.get_conn()
    aluno, disciplinas = _fetch_disciplinas(aluno_id, conn)
    conn.close()

    if not aluno or not disciplinas:
        raise HTTPException(404, "Aluno não encontrado ou sem notas lançadas")

    svc = MLService.get()
    if not svc.is_available(model):
        # Try loading it on the fly
        if not svc.load_model(model):
            raise HTTPException(404, f"Modelo {model} não disponível.")

    serie       = _serie_norm(aluno["sala_codigo"])
    media_geral = float(np.mean([d["media"] for d in disciplinas])) / 10.0
    media_turma = media_geral

    if materia_id:
        disc = next((d for d in disciplinas if d["id"] == materia_id), None)
        if not disc:
            raise HTTPException(404, f"Disciplina {materia_id} não encontrada para este aluno")
    else:
        disc = min(disciplinas, key=lambda d: d["media"])

    fv = _feature_vector_for(disc, media_geral, serie, media_turma)
    votes_seq = svc.get_ensemble_votes_sequence(model, fv)

    # Final prediction from ensemble
    ensemble = svc.predict_ensemble(model, fv)

    return {
        "votes_sequence": votes_seq,
        "n_trees": len(votes_seq),
        "focus_disciplina": disc["nome"],
        "final": {
            "class_value": ensemble["class_value"],
            "class_name":  ensemble["class_name"],
            "class_color": ensemble["class_color"],
            "confidence":  ensemble["confidence"],
        } if ensemble else None,
    }


@router.get("/predicoes/turma/{sala_id}")
def analyze_turma(sala_id: int, model: str = "RF_M3"):
    """
    Full ML batch predictions for all students in a class.
    Slow for large classes — prefer /predicoes/turma-rapida for list views.
    """
    alunos_list = cads.get_alunos(sala_id)
    svc = MLService.get()
    result = []

    for a in alunos_list:
        conn = cads.get_conn()
        aluno_row, disciplinas = _fetch_disciplinas(a["id"], conn)
        conn.close()

        if not disciplinas:
            result.append({
                "id": a["id"], "nome": a["nome"], "matricula": a["matricula"],
                "media_geral": None, "n_disciplinas": 0,
                "n_risco": 0, "n_atencao": 0, "prediction": None,
            })
            continue

        serie = _serie_norm(aluno_row["sala_codigo"])
        medias = [d["media"] for d in disciplinas]
        media_geral = float(np.mean(medias)) / 10.0

        # Aggregate feature vector
        fv_agg = [
            float(np.mean([d["n1_norm"]         for d in disciplinas])),
            float(np.mean([d["n2_norm"]         for d in disciplinas])),
            float(np.mean([d["n3_norm"]         for d in disciplinas])),
            float(np.mean([d["n4_norm"]         for d in disciplinas])),
            float(np.mean([d["slope_notas"]     for d in disciplinas])),
            float(np.mean([d["variancia_notas"] for d in disciplinas])),
            media_geral, serie, media_geral,
        ]

        prediction = None
        if svc.is_available(model):
            try:
                prediction = svc.predict_ensemble(model, fv_agg)
            except Exception as e:
                print(f"[turma] {a['nome']}: {e}")

        result.append({
            "id": a["id"],
            "nome": a["nome"],
            "matricula": a["matricula"],
            "media_geral": round(float(np.mean(medias)), 2),
            "n_disciplinas": len(disciplinas),
            "n_risco": sum(1 for d in disciplinas if d["media"] < 5.0),
            "n_atencao": sum(1 for d in disciplinas if 5.0 <= d["media"] < 6.0),
            "prediction": prediction,
        })

    return result
