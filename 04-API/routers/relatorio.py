from fastapi import APIRouter
import cads

router = APIRouter(tags=["relatorio"])


@router.get("/relatorio")
def get_relatorio(sala_id: int | None = None):
    dados = cads.get_relatorio(sala_id)
    rows = []
    aprov = recup = reprov = 0
    for d in dados:
        vals = [d.get(k) for k in ("n1", "n2", "n3", "n4")]
        valid = [v for v in vals if v is not None]
        media = round(sum(valid) / len(valid), 2) if valid else None
        if media is not None:
            if media >= 6:
                status, aprov = "Aprovado", aprov + 1
            elif media >= 5:
                status, recup = "Recuperação", recup + 1
            else:
                status, reprov = "Reprovado", reprov + 1
        else:
            status = "-"
        rows.append({**d, "media": media, "status": status})

    total = aprov + recup + reprov
    return {
        "rows": rows,
        "stats": {
            "total": total,
            "aprovado": aprov,
            "recuperacao": recup,
            "reprovado": reprov,
            "taxa": round(aprov / total * 100, 1) if total else 0,
        },
    }
