"""JWT token creation and validation."""
import os
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jose import JWTError, jwt

_KEY_FILE = Path(__file__).parent / "secret.key"

def _get_secret() -> str:
    key = os.environ.get("EDUNOTAS_SECRET")
    if key:
        return key
    if _KEY_FILE.exists():
        return _KEY_FILE.read_text().strip()
    key = secrets.token_hex(32)
    _KEY_FILE.write_text(key)
    return key

SECRET_KEY = _get_secret()
ALGORITHM  = "HS256"
EXPIRE_HOURS = 8


def create_token(user_id: int, role: str, nome: str, email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=EXPIRE_HOURS)
    payload = {
        "sub":   str(user_id),
        "role":  role,
        "nome":  nome,
        "email": email,
        "exp":   expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Returns payload dict or raises JWTError."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
