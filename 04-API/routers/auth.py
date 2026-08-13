"""Auth router — login, me, policies."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import cads
from auth.jwt_handler import create_token
from auth.dependencies import get_current_user, require_role
from auth.casbin_enforcer import list_policies, add_policy, remove_policy
from auth.bcrypt_helper import verify_password

router = APIRouter(tags=["auth"])


class LoginBody(BaseModel):
    email: str
    senha: str


class PolicyBody(BaseModel):
    sub: str
    obj: str
    act: str


@router.post("/auth/login")
def login(body: LoginBody):
    conn = cads.get_conn()
    user = conn.execute(
        "SELECT * FROM usuarios WHERE email = ? AND ativo = 1",
        (body.email.strip().lower(),),
    ).fetchone()
    conn.close()

    if not user or not verify_password(body.senha, user["senha_hash"]):
        raise HTTPException(401, "E-mail ou senha incorretos.")

    token = create_token(user["id"], user["role"], user["nome"], user["email"])
    return {
        "access_token": token,
        "token_type":   "bearer",
        "role":         user["role"],
        "nome":         user["nome"],
        "email":        user["email"],
        "id":           user["id"],
    }


@router.get("/auth/me")
def me(user: dict = Depends(get_current_user)):
    return user


@router.get("/auth/policies")
def get_policies(user: dict = Depends(require_role("desenvolvedor"))):
    return list_policies()


@router.post("/auth/policies")
def create_policy(body: PolicyBody, user: dict = Depends(require_role("desenvolvedor"))):
    ok = add_policy(body.sub, body.obj, body.act)
    if not ok:
        raise HTTPException(400, "Política já existe ou inválida.")
    return {"ok": True}


@router.delete("/auth/policies")
def delete_policy(body: PolicyBody, user: dict = Depends(require_role("desenvolvedor"))):
    ok = remove_policy(body.sub, body.obj, body.act)
    if not ok:
        raise HTTPException(400, "Política não encontrada.")
    return {"ok": True}
