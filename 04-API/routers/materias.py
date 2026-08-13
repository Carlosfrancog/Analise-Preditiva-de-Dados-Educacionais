from fastapi import APIRouter
from pydantic import BaseModel
import cads

router = APIRouter(tags=["materias"])

DEFAULT_MATERIAS = [
    "Português", "Matemática", "História", "Geografia", "Ciências",
    "Física", "Química", "Biologia", "Inglês", "Filosofia",
    "Sociologia", "Educação Física", "Arte",
]


class MateriaCreate(BaseModel):
    nome: str


@router.get("/materias")
def list_materias():
    return cads.get_materias()


@router.post("/materias")
def create_materia(body: MateriaCreate):
    cads.adicionar_materia(body.nome.strip().title())
    return {"ok": True}


@router.post("/materias/default")
def create_default():
    for m in DEFAULT_MATERIAS:
        cads.adicionar_materia(m)
    return {"criadas": len(DEFAULT_MATERIAS)}


@router.delete("/materias/{materia_id}")
def delete_materia(materia_id: int):
    conn = cads.get_conn()
    conn.execute("DELETE FROM notas WHERE materia_id=?", (materia_id,))
    conn.execute("DELETE FROM materias WHERE id=?", (materia_id,))
    conn.commit()
    conn.close()
    return {"ok": True}
