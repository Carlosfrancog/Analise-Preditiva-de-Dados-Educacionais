"""Usuários router — CRUD de contas do sistema."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import cads
from auth.dependencies import get_current_user, require_role
from auth.bcrypt_helper import hash_password

router = APIRouter(tags=["usuarios"])

VALID_ROLES = {"desenvolvedor", "admin", "coordenador", "professor", "aluno"}


class UsuarioBody(BaseModel):
    nome:  str
    email: str
    senha: str | None = None
    role:  str
    ativo: int = 1


@router.get("/usuarios")
def list_usuarios(user: dict = Depends(require_role("desenvolvedor", "coordenador", "admin"))):
    conn = cads.get_conn()
    rows = conn.execute(
        "SELECT id, nome, email, role, ativo, criado_em FROM usuarios ORDER BY nome"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/usuarios")
def create_usuario(
    body: UsuarioBody,
    user: dict = Depends(require_role("desenvolvedor", "coordenador", "admin")),
):
    if body.role not in VALID_ROLES:
        raise HTTPException(400, f"Role inválido: {body.role}")
    # Coordenador/admin não pode criar desenvolvedor
    if body.role == "desenvolvedor" and user["role"] != "desenvolvedor":
        raise HTTPException(403, "Apenas desenvolvedor pode criar outro desenvolvedor.")
    if not body.senha:
        raise HTTPException(400, "Senha obrigatória para novo usuário.")

    hashed = hash_password(body.senha)
    conn = cads.get_conn()
    try:
        conn.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, role, ativo) VALUES (?,?,?,?,?)",
            (body.nome, body.email.strip().lower(), hashed, body.role, body.ativo),
        )
        conn.commit()
        new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    except Exception as e:
        conn.close()
        raise HTTPException(400, f"Erro ao criar usuário: {e}")
    conn.close()
    return {"id": new_id, "ok": True}


@router.put("/usuarios/{uid}")
def update_usuario(
    uid: int,
    body: UsuarioBody,
    user: dict = Depends(require_role("desenvolvedor", "coordenador", "admin")),
):
    if body.role not in VALID_ROLES:
        raise HTTPException(400, f"Role inválido: {body.role}")

    conn = cads.get_conn()
    target = conn.execute("SELECT * FROM usuarios WHERE id = ?", (uid,)).fetchone()
    if not target:
        conn.close()
        raise HTTPException(404, "Usuário não encontrado.")
    # Protect: only dev can edit a dev account
    if target["role"] == "desenvolvedor" and user["role"] != "desenvolvedor":
        conn.close()
        raise HTTPException(403, "Sem permissão para editar conta de desenvolvedor.")
    if body.role == "desenvolvedor" and user["role"] != "desenvolvedor":
        conn.close()
        raise HTTPException(403, "Apenas desenvolvedor pode promover para este role.")

    if body.senha:
        hashed = hash_password(body.senha)
        conn.execute(
            "UPDATE usuarios SET nome=?, email=?, senha_hash=?, role=?, ativo=? WHERE id=?",
            (body.nome, body.email.strip().lower(), hashed, body.role, body.ativo, uid),
        )
    else:
        conn.execute(
            "UPDATE usuarios SET nome=?, email=?, role=?, ativo=? WHERE id=?",
            (body.nome, body.email.strip().lower(), body.role, body.ativo, uid),
        )
    conn.commit()
    conn.close()
    return {"ok": True}


@router.delete("/usuarios/{uid}")
def delete_usuario(
    uid: int,
    user: dict = Depends(require_role("desenvolvedor", "coordenador", "admin")),
):
    conn = cads.get_conn()
    target = conn.execute("SELECT * FROM usuarios WHERE id = ?", (uid,)).fetchone()
    if not target:
        conn.close()
        raise HTTPException(404, "Usuário não encontrado.")
    if target["role"] == "desenvolvedor":
        conn.close()
        raise HTTPException(403, "Não é possível deletar uma conta de desenvolvedor.")
    if target["id"] == user["id"]:
        conn.close()
        raise HTTPException(400, "Você não pode deletar sua própria conta.")
    conn.execute("DELETE FROM usuarios WHERE id = ?", (uid,))
    conn.commit()
    conn.close()
    return {"ok": True}
