"""Presenças diárias por aluno/matéria."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import cads

router = APIRouter(tags=["presencas"])


class PresencaBody(BaseModel):
    aluno_id:   int
    materia_id: int
    data:       str   # YYYY-MM-DD
    status:     str   # P | F | J


@router.get("/presencas/{aluno_id}/{materia_id}")
def get_presencas(aluno_id: int, materia_id: int):
    conn = cads.get_conn()
    rows = conn.execute(
        "SELECT * FROM presencas WHERE aluno_id=? AND materia_id=? ORDER BY data",
        (aluno_id, materia_id),
    ).fetchall()
    conn.close()
    return {r["data"]: {"id": r["id"], "status": r["status"]} for r in rows}


@router.post("/presencas/upsert")
def upsert_presenca(body: PresencaBody):
    if body.status not in ("P", "F", "J"):
        raise HTTPException(400, "Status inválido — use P, F ou J.")
    conn = cads.get_conn()
    conn.execute(
        """INSERT INTO presencas (aluno_id, materia_id, data, status) VALUES (?,?,?,?)
           ON CONFLICT(aluno_id, materia_id, data) DO UPDATE SET status=excluded.status""",
        (body.aluno_id, body.materia_id, body.data, body.status),
    )
    pid = conn.execute(
        "SELECT id FROM presencas WHERE aluno_id=? AND materia_id=? AND data=?",
        (body.aluno_id, body.materia_id, body.data),
    ).fetchone()["id"]
    conn.commit()
    conn.close()
    return {"id": pid, "ok": True}


@router.delete("/presencas/{pid}")
def delete_presenca(pid: int):
    conn = cads.get_conn()
    conn.execute("DELETE FROM presencas WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return {"ok": True}
