"""Atividades por bimestre — sub-notas que compõem N1..N4."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import cads

router = APIRouter(tags=["atividades"])


class AtividadeBody(BaseModel):
    aluno_id:   int
    materia_id: int
    bimestre:   int
    nome:       str
    nota:       float


@router.get("/atividades/{aluno_id}/{materia_id}")
def get_atividades(aluno_id: int, materia_id: int):
    conn = cads.get_conn()
    rows = conn.execute(
        "SELECT * FROM atividades WHERE aluno_id=? AND materia_id=? ORDER BY bimestre, criado_em",
        (aluno_id, materia_id),
    ).fetchall()
    conn.close()
    result = {1: [], 2: [], 3: [], 4: []}
    for r in rows:
        result[r["bimestre"]].append(dict(r))
    return result


@router.post("/atividades")
def create_atividade(body: AtividadeBody):
    if not 1 <= body.bimestre <= 4:
        raise HTTPException(400, "Bimestre deve ser 1, 2, 3 ou 4.")
    if not 0 <= body.nota <= 10:
        raise HTTPException(400, "Nota deve estar entre 0 e 10.")
    if not body.nome.strip():
        raise HTTPException(400, "Nome da atividade é obrigatório.")
    conn = cads.get_conn()
    conn.execute(
        "INSERT INTO atividades (aluno_id, materia_id, bimestre, nome, nota) VALUES (?,?,?,?,?)",
        (body.aluno_id, body.materia_id, body.bimestre, body.nome.strip(), body.nota),
    )
    new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    cads.recalc_nota_from_atividades(conn, body.aluno_id, body.materia_id, body.bimestre)
    conn.commit()
    conn.close()
    return {"id": new_id, "ok": True}


@router.put("/atividades/{aid}")
def update_atividade(aid: int, body: AtividadeBody):
    if not 0 <= body.nota <= 10:
        raise HTTPException(400, "Nota deve estar entre 0 e 10.")
    conn = cads.get_conn()
    row = conn.execute("SELECT * FROM atividades WHERE id=?", (aid,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(404, "Atividade não encontrada.")
    conn.execute(
        "UPDATE atividades SET nome=?, nota=? WHERE id=?",
        (body.nome.strip(), body.nota, aid),
    )
    cads.recalc_nota_from_atividades(conn, row["aluno_id"], row["materia_id"], row["bimestre"])
    conn.commit()
    conn.close()
    return {"ok": True}


@router.delete("/atividades/{aid}")
def delete_atividade(aid: int):
    conn = cads.get_conn()
    row = conn.execute("SELECT * FROM atividades WHERE id=?", (aid,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(404, "Atividade não encontrada.")
    conn.execute("DELETE FROM atividades WHERE id=?", (aid,))
    cads.recalc_nota_from_atividades(conn, row["aluno_id"], row["materia_id"], row["bimestre"])
    conn.commit()
    conn.close()
    return {"ok": True}
