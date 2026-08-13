#!/usr/bin/env python3
"""
EduNotas Desktop Launcher
FastAPI backend + PyWebView native window
"""
import sys
import threading
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
PORT = 7654

# Invalidate stale .pyc caches so edits always take effect on first run
import importlib, py_compile
for _pycache in ROOT.rglob("__pycache__"):
    for _pyc in _pycache.glob("*.pyc"):
        _py = _pycache.parent / _pyc.stem.rsplit(".", 1)[0]
        _py = _py.with_suffix(".py")
        if _py.exists() and _py.stat().st_mtime > _pyc.stat().st_mtime:
            _pyc.unlink(missing_ok=True)

sys.path.insert(0, str(ROOT / "04-API"))
sys.path.insert(0, str(ROOT / "01-CORE"))
sys.path.insert(0, str(ROOT / "02-ML"))


def start_api():
    import uvicorn
    from main import app  # 04-API/main.py
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")


def wait_for_server(timeout: int = 10) -> bool:
    for _ in range(timeout * 5):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/api/health", timeout=0.5)
            return True
        except Exception:
            time.sleep(0.2)
    return False


if __name__ == "__main__":
    threading.Thread(target=start_api, daemon=True).start()

    if not wait_for_server():
        print("[ERRO] API não iniciou a tempo. Verifique dependências.")
        sys.exit(1)

    try:
        import webview
    except ImportError:
        print("pywebview não instalado. Execute: pip install pywebview")
        print(f"Acesse manualmente: http://127.0.0.1:{PORT}")
        input("Pressione Enter para sair...")
        sys.exit(1)

    webview.create_window(
        "EduNotas — Sistema Escolar",
        f"http://127.0.0.1:{PORT}",
        width=1280,
        height=800,
        min_size=(1100, 680),
        background_color="#0F172A",
    )
    webview.start()
