"""Exportar dados em CSV ou HTML/PDF."""
import io, csv, json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
import cads

router = APIRouter(tags=["exportar"])


def _csv_response(rows: list[dict], filename: str) -> StreamingResponse:
    if not rows:
        return StreamingResponse(iter([""]), media_type="text/csv",
                                 headers={"Content-Disposition": f'attachment; filename="{filename}"'})
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/exportar/alunos")
def exportar_alunos(sala_id: int | None = None):
    conn = cads.get_conn()
    q = """
        SELECT a.matricula, a.nome as aluno, s.nome as turma, s.codigo
        FROM alunos a JOIN salas s ON a.sala_id = s.id
    """
    params = []
    if sala_id:
        q += " WHERE a.sala_id=?"
        params.append(sala_id)
    q += " ORDER BY s.id, a.nome"
    rows = [dict(r) for r in conn.execute(q, params).fetchall()]
    conn.close()
    return _csv_response(rows, "alunos.csv")


@router.get("/exportar/notas")
def exportar_notas(sala_id: int | None = None):
    conn = cads.get_conn()
    q = """
        SELECT a.matricula, a.nome as aluno, s.nome as turma,
               m.nome as materia, n.n1, n.n2, n.n3, n.n4
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN salas s ON a.sala_id = s.id
        JOIN materias m ON n.materia_id = m.id
    """
    params = []
    if sala_id:
        q += " WHERE a.sala_id=?"
        params.append(sala_id)
    q += " ORDER BY s.id, a.nome, m.nome"
    rows = [dict(r) for r in conn.execute(q, params).fetchall()]
    conn.close()
    return _csv_response(rows, "notas.csv")


@router.get("/exportar/relatorio")
def exportar_relatorio(sala_id: int | None = None):
    dados = cads.get_relatorio(sala_id)
    rows = []
    for d in dados:
        vals = [d.get(k) for k in ("n1", "n2", "n3", "n4")]
        valid = [v for v in vals if v is not None]
        media = round(sum(valid) / len(valid), 2) if valid else None
        if media is None:
            status = "—"
        elif media >= 6:
            status = "Aprovado"
        elif media >= 5:
            status = "Recuperação"
        else:
            status = "Reprovado"
        rows.append({
            "turma":   d.get("sala_nome"),
            "aluno":   d.get("aluno_nome"),
            "materia": d.get("materia_nome"),
            "n1": d.get("n1"), "n2": d.get("n2"),
            "n3": d.get("n3"), "n4": d.get("n4"),
            "media":   media,
            "status":  status,
        })
    return _csv_response(rows, "relatorio.csv")


@router.get("/exportar/ia-raw")
def exportar_ia_raw(sala_id: int | None = None):
    conn = cads.get_conn()
    q = """
        SELECT f.aluno_nome, f.sala_nome, f.materia_nome,
               f.n1, f.n2, f.n3, f.n4,
               ROUND(f.n1_norm,4) as n1_norm, ROUND(f.n2_norm,4) as n2_norm,
               ROUND(f.n3_norm,4) as n3_norm, ROUND(f.n4_norm,4) as n4_norm,
               ROUND(f.media_pond_norm,4) as media_pond_norm,
               ROUND(f.slope_notas,4) as slope_notas,
               ROUND(f.variancia_notas,4) as variancia_notas,
               ROUND(f.media_geral_aluno,4) as media_geral_aluno,
               ROUND(f.serie_num_norm,4) as serie_num_norm,
               ROUND(f.media_turma_norm,4) as media_turma_norm,
               f.status_encoded, f.status_label
        FROM ml_features f
        LEFT JOIN salas s ON f.sala_nome = s.nome
    """
    params = []
    if sala_id:
        q += " WHERE s.id=?"
        params.append(sala_id)
    q += " ORDER BY f.sala_nome, f.aluno_nome, f.materia_nome"
    rows = [dict(r) for r in conn.execute(q, params).fetchall()]
    conn.close()
    return _csv_response(rows, "ia_raw.csv")


@router.get("/exportar/salas")
def exportar_salas():
    conn = cads.get_conn()
    rows = conn.execute("""
        SELECT s.nome, s.codigo,
               COUNT(DISTINCT a.id) as total_alunos,
               COUNT(DISTINCT n.materia_id) as materias_com_notas
        FROM salas s
        LEFT JOIN alunos a ON a.sala_id = s.id
        LEFT JOIN notas n ON n.aluno_id = a.id
        GROUP BY s.id ORDER BY s.id
    """).fetchall()
    conn.close()
    return _csv_response([dict(r) for r in rows], "salas.csv")
