"""FastAPI dependencies for JWT authentication and Casbin authorization."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from auth.jwt_handler import decode_token
from auth.casbin_enforcer import check_permission

bearer = HTTPBearer(auto_error=False)

ROLES = {"desenvolvedor", "admin", "coordenador", "professor", "aluno"}


async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict:
    """Decode JWT → return user dict. Raises 401 if invalid/missing."""
    if not creds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(creds.credentials)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "id":    int(payload["sub"]),
        "role":  payload["role"],
        "nome":  payload.get("nome", ""),
        "email": payload.get("email", ""),
    }


def require_role(*roles: str):
    """Dependency factory: require user to have one of the specified roles."""
    async def dep(user: dict = Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso restrito. Requer: {', '.join(roles)}.",
            )
        return user
    return dep


def require_permission(resource: str, action: str):
    """Dependency factory: require Casbin permission check."""
    async def dep(user: dict = Depends(get_current_user)):
        if not check_permission(user["role"], resource, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Sem permissão para {action} em '{resource}'.",
            )
        return user
    return dep
