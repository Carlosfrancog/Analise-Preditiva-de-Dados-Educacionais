#!/usr/bin/env python3
"""EduNotas FastAPI backend"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "01-CORE"))
sys.path.insert(0, str(ROOT / "02-ML"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import cads
from ml_service import MLService

from routers import dashboard, alunos, salas, materias, notas, predicoes, relatorio, ml_features, auth, users, atividades, presencas, exportar, importar, research

app = FastAPI(title="EduNotas API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise DB and pre-load ML models at startup
@app.on_event("startup")
def on_startup():
    cads.init_db()
    cads.init_usuarios()
    MLService.get()  # warm up singleton (loads active model only)

# API routes
for router in [
    dashboard.router,
    alunos.router,
    salas.router,
    materias.router,
    notas.router,
    predicoes.router,
    relatorio.router,
    ml_features.router,
    auth.router,
    users.router,
    atividades.router,
    presencas.router,
    exportar.router,
    importar.router,
    research.router,
]:
    app.include_router(router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Serve built React app in production (after `npm run build`)
_dist = ROOT / "05-WEB" / "dist"
if _dist.exists():
    app.mount("/assets", StaticFiles(directory=str(_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        return FileResponse(str(_dist / "index.html"))
