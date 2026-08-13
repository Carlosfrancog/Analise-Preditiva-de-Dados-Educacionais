"""Casbin policy enforcer — singleton."""
import casbin
from pathlib import Path

_AUTH_DIR = Path(__file__).parent
_enforcer: casbin.Enforcer | None = None


def get_enforcer() -> casbin.Enforcer:
    global _enforcer
    if _enforcer is None:
        _enforcer = casbin.Enforcer(
            str(_AUTH_DIR / "model.conf"),
            str(_AUTH_DIR / "policy.csv"),
        )
    return _enforcer


def check_permission(role: str, resource: str, action: str) -> bool:
    """Returns True if role can perform action on resource."""
    return get_enforcer().enforce(role, resource, action)


def list_policies() -> list[dict]:
    e = get_enforcer()
    return [
        {"sub": p[0], "obj": p[1], "act": p[2]}
        for p in e.get_policy()
    ]


def add_policy(sub: str, obj: str, act: str) -> bool:
    return get_enforcer().add_policy(sub, obj, act)


def remove_policy(sub: str, obj: str, act: str) -> bool:
    return get_enforcer().remove_policy(sub, obj, act)
