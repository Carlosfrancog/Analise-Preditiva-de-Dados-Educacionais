from fastapi import APIRouter
from pydantic import BaseModel
import cads

router = APIRouter(tags=["notas"])


class NotaSave(BaseModel):
    aluno_id: int
    materia_id: int
    n1: float | None = None
    n2: float | None = None
    n3: float | None = None
    n4: float | None = None


@router.get("/notas/turma/{sala_id}")
def get_notas_turma(sala_id: int):
    """All grades for every student in a class, joined with student and subject names."""
    conn = cads.get_conn()
    rows = conn.execute(
        """SELECT n.aluno_id, a.nome AS aluno_nome,
                  n.materia_id, m.nome AS materia_nome,
                  n.n1, n.n2, n.n3, n.n4
           FROM notas n
           JOIN alunos a ON n.aluno_id = a.id
           JOIN materias m ON n.materia_id = m.id
           WHERE a.sala_id = ?
           ORDER BY a.nome, m.nome""",
        (sala_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


class NotaBatchSave(BaseModel):
    notas: list[NotaSave]


@router.put("/notas/batch")
def save_notas_batch(body: NotaBatchSave):
    for n in body.notas:
        cads.salvar_nota(n.aluno_id, n.materia_id, n.n1, n.n2, n.n3, n.n4)
    return {"ok": True, "saved": len(body.notas)}


@router.get("/notas/{aluno_id}")
def get_notas(aluno_id: int):
    return cads.get_notas(aluno_id)


@router.put("/notas")
def save_nota(body: NotaSave):
    cads.salvar_nota(body.aluno_id, body.materia_id, body.n1, body.n2, body.n3, body.n4)
    return {"ok": True}


@router.post("/notas/gerar/aluno/{aluno_id}")
def gerar_aluno(aluno_id: int):
    n = cads.gerar_notas_aleatorias(aluno_ids=[aluno_id])
    return {"geradas": n}


@router.post("/notas/gerar/turma/{sala_id}")
def gerar_turma(sala_id: int):
    alunos = cads.get_alunos(sala_id)
    ids = [a["id"] for a in alunos]
    n = cads.gerar_notas_aleatorias(aluno_ids=ids)
    return {"geradas": n}


@router.post("/notas/gerar/todos")
def gerar_todos():
    n = cads.gerar_notas_aleatorias()
    return {"geradas": n}
