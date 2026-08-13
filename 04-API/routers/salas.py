from fastapi import APIRouter
from pydantic import BaseModel
import cads

router = APIRouter(tags=["salas"])


class SalaCreate(BaseModel):
    nome: str
    codigo: str


@router.get("/salas")
def list_salas():
    conn = cads.get_conn()
    salas = cads.get_salas()
    result = []
    for s in salas:
        cnt = conn.execute(
            "SELECT COUNT(*) FROM alunos WHERE sala_id=?", (s["id"],)
        ).fetchone()[0]
        result.append({**s, "alunos": cnt})
    conn.close()
    return result


@router.post("/salas")
def create_sala(body: SalaCreate):
    cads.adicionar_sala(body.nome.strip(), body.codigo.strip().upper())
    return {"ok": True}


@router.delete("/salas/{sala_id}")
def delete_sala(sala_id: int):
    cads.remover_sala(sala_id)
    return {"ok": True}
