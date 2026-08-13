from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import cads

router = APIRouter(tags=["alunos"])


@router.get("/alunos/{aluno_id}")
def get_aluno(aluno_id: int):
    conn = cads.get_conn()
    row = conn.execute(
        """SELECT a.id, a.nome, a.matricula, a.sala_id,
                  s.nome AS sala_nome, s.codigo AS sala_codigo
           FROM alunos a LEFT JOIN salas s ON a.sala_id = s.id
           WHERE a.id = ?""",
        (aluno_id,),
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Aluno não encontrado")
    return dict(row)


class AlunoCreate(BaseModel):
    nome: str
    sala_id: int


@router.get("/alunos")
def list_alunos(sala_id: int | None = None):
    return cads.get_alunos(sala_id)


@router.post("/alunos")
def create_aluno(body: AlunoCreate):
    cads.adicionar_aluno(body.nome.strip().title(), body.sala_id)
    return {"ok": True}


@router.post("/alunos/genericos")
def create_genericos(sala_id: int, quantidade: int = 200):
    n = cads.gerar_alunos_genericos(quantidade, sala_id)
    return {"criados": n}


@router.post("/alunos/atribuir-materias")
def atribuir_materias():
    n = cads.atribuir_materias_todos()
    return {"registros": n}


@router.delete("/alunos/{aluno_id}")
def delete_aluno(aluno_id: int):
    conn = cads.get_conn()
    conn.execute("DELETE FROM notas WHERE aluno_id=?", (aluno_id,))
    conn.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))
    conn.commit()
    conn.close()
    return {"ok": True}
