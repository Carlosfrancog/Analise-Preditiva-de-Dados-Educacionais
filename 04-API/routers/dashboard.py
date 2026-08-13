from fastapi import APIRouter
import cads

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
def get_dashboard():
    conn = cads.get_conn()

    # Basic counts
    na = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
    nm = conn.execute("SELECT COUNT(*) FROM materias").fetchone()[0]
    nn = conn.execute("SELECT COUNT(*) FROM notas WHERE n1 IS NOT NULL OR n2 IS NOT NULL OR n3 IS NOT NULL OR n4 IS NOT NULL").fetchone()[0]
    n_salas = conn.execute("SELECT COUNT(*) FROM salas").fetchone()[0]

    try:
        n_risco = conn.execute(
            "SELECT COUNT(DISTINCT aluno_id) FROM ml_features WHERE status_encoded IN (0,1)"
        ).fetchone()[0]
    except Exception:
        n_risco = 0

    # Approval stats from notas (compute per-row status for all notas with enough data)
    try:
        nota_rows = conn.execute(
            "SELECT n1,n2,n3,n4 FROM notas WHERE n1 IS NOT NULL"
        ).fetchall()
        aprov = recup = reprov = 0
        for r in nota_rows:
            vals = [v for v in [r[0], r[1], r[2], r[3]] if v is not None]
            if not vals: continue
            media = sum(vals) / len(vals)
            if media >= 6: aprov += 1
            elif media >= 5: recup += 1
            else: reprov += 1
        total_notas = aprov + recup + reprov
    except Exception:
        aprov = recup = reprov = total_notas = 0

    # Salas with risk %, approval %, student count, quick navigate info
    salas = conn.execute("""
        SELECT s.id, s.nome, s.codigo,
               COUNT(DISTINCT a.id) as alunos,
               SUM(CASE WHEN f.status_encoded = 0 THEN 1 ELSE 0 END) as reprovados,
               SUM(CASE WHEN f.status_encoded = 1 THEN 1 ELSE 0 END) as recuperacao,
               SUM(CASE WHEN f.status_encoded = 2 THEN 1 ELSE 0 END) as aprovados,
               COUNT(f.aluno_id) as com_predicao
        FROM salas s
        LEFT JOIN alunos a ON a.sala_id = s.id
        LEFT JOIN ml_features f ON f.aluno_id = a.id
        GROUP BY s.id ORDER BY s.id
    """).fetchall()

    # Recent activity: last 5 notas inserted/updated
    try:
        recent = conn.execute("""
            SELECT a.nome as aluno_nome, m.nome as materia_nome, s.nome as sala_nome,
                   n.n1, n.n2, n.n3, n.n4
            FROM notas n
            JOIN alunos a ON n.aluno_id=a.id
            JOIN materias m ON n.materia_id=m.id
            JOIN salas s ON a.sala_id=s.id
            WHERE n.n1 IS NOT NULL
            ORDER BY n.rowid DESC LIMIT 5
        """).fetchall()
        recent_list = [dict(r) for r in recent]
    except Exception:
        recent_list = []

    conn.close()

    sala_list = []
    for r in salas:
        total_pred = int(r["com_predicao"] or 0)
        rep  = int(r["reprovados"]  or 0)
        rec  = int(r["recuperacao"] or 0)
        apv  = int(r["aprovados"]   or 0)
        risco_pct = round((rep + rec) / total_pred * 100) if total_pred else 0
        aprov_pct = round(apv / total_pred * 100) if total_pred else 0
        sala_list.append({
            "id": r["id"],
            "nome": r["nome"],
            "codigo": r["codigo"],
            "alunos": int(r["alunos"] or 0),
            "reprovados": rep,
            "recuperacao": rec,
            "aprovados": apv,
            "risco_pct": risco_pct,
            "aprov_pct": aprov_pct,
            "com_predicao": total_pred,
        })

    return {
        "kpis": {
            "alunos": na,
            "materias": nm,
            "notas_lancadas": nn,
            "em_risco": n_risco,
            "salas": n_salas,
        },
        "notas_stats": {
            "aprovado": aprov,
            "recuperacao": recup,
            "reprovado": reprov,
            "total": total_notas,
            "taxa_aprov": round(aprov / total_notas * 100, 1) if total_notas else 0,
        },
        "salas": sala_list,
        "recent_notas": recent_list,
    }
