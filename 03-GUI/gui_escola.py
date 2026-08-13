#!/usr/bin/env python3
"""
Interface Gráfica - Sistema de Cadastro Escolar
Gerencia alunos, matérias e notas por turma
Design: Academy B (dark sidebar, indigo accent, clean cards)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import random
import sys
from pathlib import Path

# Adicionar pastas ao path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "01-CORE"))
sys.path.insert(0, str(project_root / "02-ML"))
sys.path.insert(0, str(project_root / "03-GUI"))

import cads

from gui_predicoes_improved import PredictionPageImproved as PredictionPage
from gui_predicoes import SalasPage

# ── Design Tokens — Academy B ─────────────────────────────────────────────────
BG          = "#F4F6FA"
SIDEBAR     = "#0F172A"
SIDEBAR_H   = "#1E293B"
ACCENT      = "#4F46E5"
ACCENT2     = "#818CF8"
SUCCESS     = "#10B981"
WARN        = "#F59E0B"
DANGER      = "#EF4444"
INFO        = "#0EA5E9"
CARD        = "#FFFFFF"
TEXT        = "#0F172A"
TEXT2       = "#1E293B"
MUTED       = "#64748B"
MUTED2      = "#94A3B8"
BORDER      = "#E5E9F0"
HEADER_BG   = "#F8FAFC"
ROW_ALT     = "#F8FAFC"
RED_L       = "#FEE2E2"
GRN_L       = "#D1FAE5"
WARN_L      = "#FEF3C7"
BLUE_L      = "#E0F2FE"
SB_TEXT     = "#94A3B8"
SB_SECTION  = "#475569"

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_HEAD   = ("Segoe UI", 13, "bold")
FONT_SUB    = ("Segoe UI", 11)
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_TINY   = ("Segoe UI", 8)
FONT_BTN    = ("Segoe UI", 10, "bold")
FONT_NUM    = ("Segoe UI", 26, "bold")
FONT_NAV    = ("Segoe UI", 11)
FONT_CAP    = ("Segoe UI", 8, "bold")


# ── Sidebar nav config ────────────────────────────────────────────────────────
NAV_ITEMS = [
    ("dashboard", "  Dashboard",     "🏠", None),
    ("alunos",    "  Alunos",        "👤", None),
    ("salas",     "  Salas/Turmas",  "🏫", "7"),
    ("materias",  "  Matérias",      "📖", "13"),
    ("notas",     "  Notas",         "✏️",  None),
    ("predicoes", "  Predições",     "🎯", "IA"),
    ("relatorio", "  Relatório",     "📊", None),
    ("ml",        "  Machine Learning","🤖", None),
]
IO_ITEMS = [
    ("importar",  "  Importar Excel",  "📤"),
    ("exportar",  "  Exportar Excel",  "📥"),
]
PAGE_META = {
    "dashboard": ("Dashboard", "Visão geral do sistema"),
    "alunos":    ("Alunos", "Gestão de alunos e turmas"),
    "salas":     ("Salas / Turmas", "Gestão de turmas"),
    "materias":  ("Matérias", "Currículo e disciplinas"),
    "notas":     ("Notas", "Lançamento e edição de notas"),
    "predicoes": ("Predições", "Análise de desempenho por IA"),
    "relatorio": ("Relatório", "Visão completa de notas"),
    "ml":        ("Machine Learning", "Treinamento e análise de modelos"),
    "importar":  ("Importar Excel", "Importar dados de planilha"),
    "exportar":  ("Exportar Excel", "Exportar dados para planilha"),
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        cads.init_db()
        self.title("EduNotas — Sistema Escolar")
        self.geometry("1280x800")
        self.minsize(1100, 680)
        self.configure(bg=SIDEBAR)
        self._build_ui()
        self._show_page("dashboard")

    # ── Layout ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Sidebar ──────────────────────────────────────────────────────────
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_f = tk.Frame(self.sidebar, bg=SIDEBAR)
        logo_f.pack(fill="x", padx=16, pady=(16, 14))
        logo_icon = tk.Label(logo_f,
            text="E",
            font=("Segoe UI", 15, "bold"),
            bg=ACCENT, fg="white",
            width=2, height=1)
        logo_icon.pack(side="left", padx=(0, 10))
        logo_txt = tk.Frame(logo_f, bg=SIDEBAR)
        logo_txt.pack(side="left")
        tk.Label(logo_txt, text="EduNotas", font=("Segoe UI", 14, "bold"),
                 bg=SIDEBAR, fg="white").pack(anchor="w")
        tk.Label(logo_txt, text="Sistema Escolar v2.0", font=FONT_TINY,
                 bg=SIDEBAR, fg=SB_SECTION).pack(anchor="w")

        _sep(self.sidebar, SIDEBAR_H)

        # Nav sections
        self._nav_btns = {}
        _sb_section(self.sidebar, "PRINCIPAL")
        for key, label, icon, badge in NAV_ITEMS:
            self._nav_btns[key] = _NavBtn(self.sidebar, icon + label, badge,
                                          lambda k=key: self._show_page(k))

        _sep(self.sidebar, SIDEBAR_H)
        _sb_section(self.sidebar, "DADOS")
        for key, label, icon in IO_ITEMS:
            self._nav_btns[key] = _NavBtn(self.sidebar, icon + label, None,
                                          lambda k=key: self._show_page(k))

        # Spacer
        tk.Frame(self.sidebar, bg=SIDEBAR).pack(fill="both", expand=True)

        # AI model status
        self._build_ai_badge()

        _sep(self.sidebar, SIDEBAR_H)

        # User profile row
        user_f = tk.Frame(self.sidebar, bg=SIDEBAR)
        user_f.pack(fill="x", padx=14, pady=(8, 14))
        avt = tk.Label(user_f, text="MR",
                       font=("Segoe UI", 10, "bold"),
                       bg="#8B5CF6", fg="white", width=3)
        avt.pack(side="left", padx=(0, 8), ipady=4)
        ux = tk.Frame(user_f, bg=SIDEBAR)
        ux.pack(side="left")
        tk.Label(ux, text="Coordenação", font=("Segoe UI", 10, "bold"),
                 bg=SIDEBAR, fg="white").pack(anchor="w")
        tk.Label(ux, text="Administrador", font=FONT_TINY,
                 bg=SIDEBAR, fg=SB_SECTION).pack(anchor="w")

        # ── Main area ────────────────────────────────────────────────────────
        self.main_outer = tk.Frame(self, bg=BG)
        self.main_outer.pack(side="left", fill="both", expand=True)

        # Topbar
        self.topbar = tk.Frame(self.main_outer, bg=BG)
        self.topbar.pack(fill="x", padx=28, pady=(18, 0))

        self._crumb_var = tk.StringVar()
        self._title_var = tk.StringVar()
        self._sub_var   = tk.StringVar()

        tk.Label(self.topbar, textvariable=self._crumb_var,
                 font=FONT_TINY, bg=BG, fg=MUTED).pack(anchor="w")
        title_row = tk.Frame(self.topbar, bg=BG)
        title_row.pack(fill="x", anchor="w", pady=(2, 0))
        tk.Label(title_row, textvariable=self._title_var,
                 font=FONT_TITLE, bg=BG, fg=TEXT).pack(side="left")
        self._kicker_lbl = tk.Label(title_row, text="",
                                    font=FONT_TINY, bg=BLUE_L, fg=ACCENT,
                                    padx=8, pady=2)
        self._kicker_lbl.pack(side="left", padx=(10, 0))
        self._kicker_lbl.pack_forget()  # hidden until set

        tk.Label(self.topbar, textvariable=self._sub_var,
                 font=FONT_BODY, bg=BG, fg=MUTED).pack(anchor="w", pady=(3, 0))

        _hsep(self.main_outer, BORDER)

        # Content container
        self.main = tk.Frame(self.main_outer, bg=BG)
        self.main.pack(fill="both", expand=True)

        # Pages
        self._pages = {}
        for cls, key in [
            (DashboardPage, "dashboard"),
            (AlunosPage,    "alunos"),
            (SalasPage,     "salas"),
            (MateriasPage,  "materias"),
            (NotasPage,     "notas"),
            (PredictionPage, "predicoes"),
            (RelatorioPage, "relatorio"),
            (MLPage,         "ml"),
            (ImportarPage,  "importar"),
            (ExportarPage,  "exportar"),
        ]:
            p = cls(self.main, self)
            p.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._pages[key] = p

    def _build_ai_badge(self):
        """AI model indicator in sidebar bottom."""
        import json
        from pathlib import Path as P
        models_dir = P(__file__).parent.parent / "02-ML" / "ml_models"
        meta = models_dir / "RF_M3_metadata.json"
        acc_str = "91.3%"
        try:
            if meta.exists():
                d = json.loads(meta.read_text(encoding="utf-8"))
                v = d.get("accuracy", 0)
                acc_str = f"{v:.1%}" if v else "—"
        except Exception:
            pass

        f = tk.Frame(self.sidebar, bg="#1E293B",
                     highlightbackground="#334155", highlightthickness=1)
        f.pack(fill="x", padx=12, pady=(0, 8))
        hdr = tk.Frame(f, bg="#1E293B")
        hdr.pack(fill="x", padx=12, pady=(8, 2))
        tk.Label(hdr, text="✦ Modelo IA Ativo", font=FONT_TINY,
                 bg="#1E293B", fg=ACCENT2).pack(side="left")
        tk.Label(f, text=f"RF_M3 — {acc_str}", font=("Segoe UI", 10, "bold"),
                 bg="#1E293B", fg="white").pack(anchor="w", padx=12, pady=(0, 2))
        tk.Label(f, text="Treinado e pronto", font=FONT_TINY,
                 bg="#1E293B", fg=SB_SECTION).pack(anchor="w", padx=12, pady=(0, 8))

    def _show_page(self, key):
        # Update nav buttons
        for k, btn in self._nav_btns.items():
            btn.set_active(k == key)

        # Update topbar
        meta = PAGE_META.get(key, (key.title(), ""))
        self._title_var.set(meta[0])
        self._sub_var.set(meta[1])
        crumbs = {
            "dashboard": "Visão geral",
            "alunos":    "Gestão / Alunos",
            "salas":     "Gestão / Salas e Turmas",
            "materias":  "Currículo / Matérias",
            "notas":     "Lançamento / Notas",
            "predicoes": "Inteligência Artificial / Predições",
            "relatorio": "Análise / Relatório",
            "ml":        "IA Avançada / Machine Learning",
            "importar":  "Dados / Importar",
            "exportar":  "Dados / Exportar",
        }
        self._crumb_var.set(crumbs.get(key, ""))

        for k, pg in self._pages.items():
            if k == key:
                pg.lift()
                if hasattr(pg, "refresh"):
                    try:
                        pg.refresh()
                    except Exception as e:
                        import traceback
                        print(f"[refresh error on '{key}']: {e}")
                        traceback.print_exc()


# ── Sidebar helpers ───────────────────────────────────────────────────────────

class _NavBtn:
    """Sidebar navigation item with active/inactive state."""
    def __init__(self, parent, label, badge, command):
        self.frame = tk.Frame(parent, bg=SIDEBAR, cursor="hand2")
        self.frame.pack(fill="x", padx=8, pady=1)

        self.lbl = tk.Label(self.frame, text=label, font=FONT_NAV,
                            bg=SIDEBAR, fg=SB_TEXT, anchor="w", padx=10, pady=7)
        self.lbl.pack(side="left", fill="x", expand=True)

        if badge:
            bg_c = ACCENT if badge == "IA" else "#1E293B"
            fg_c = "white" if badge == "IA" else MUTED2
            tk.Label(self.frame, text=badge, font=FONT_TINY,
                     bg=bg_c, fg=fg_c, padx=5, pady=1).pack(side="right", padx=8)

        self.frame.bind("<Button-1>", lambda e: command())
        self.lbl.bind("<Button-1>", lambda e: command())
        self.frame.bind("<Enter>", self._on_enter)
        self.frame.bind("<Leave>", self._on_leave)
        self.lbl.bind("<Enter>", self._on_enter)
        self.lbl.bind("<Leave>", self._on_leave)
        self._active = False


    def set_active(self, active):
        self._active = active
        bg = ACCENT if active else SIDEBAR
        fg = "white" if active else SB_TEXT
        self.frame.configure(bg=bg)
        self.lbl.configure(bg=bg, fg=fg)
        for w in self.frame.winfo_children():
            if isinstance(w, tk.Label) and w is not self.lbl:
                if active:
                    w.configure(bg=bg)
                else:
                    w.configure(bg=w.cget("bg"))  # keep badge color

    def _on_enter(self, _=None):
        if not self._active:
            self.frame.configure(bg=SIDEBAR_H)
            self.lbl.configure(bg=SIDEBAR_H, fg="#CBD5E1")

    def _on_leave(self, _=None):
        if not self._active:
            self.frame.configure(bg=SIDEBAR)
            self.lbl.configure(bg=SIDEBAR, fg=SB_TEXT)


def _sep(parent, color):
    tk.Frame(parent, bg=color, height=1).pack(fill="x", padx=0, pady=4)

def _hsep(parent, color):
    tk.Frame(parent, bg=color, height=1).pack(fill="x")

def _sb_section(parent, text):
    tk.Label(parent, text=text, font=FONT_CAP,
             bg=SIDEBAR, fg=SB_SECTION, anchor="w",
             padx=18).pack(fill="x", pady=(8, 2))


# ── Base Page ─────────────────────────────────────────────────────────────────

class BasePage(tk.Frame):
    def __init__(self, parent, app, title="", icon=""):
        super().__init__(parent, bg=BG)
        self.app = app

    def card(self, parent, **kwargs):
        kwargs.pop('relief', None)
        kwargs.pop('bd', None)
        f = tk.Frame(parent, bg=CARD, **kwargs)
        f.configure(highlightbackground=BORDER, highlightthickness=1)
        return f

    def btn(self, parent, text, cmd, color=ACCENT, fg="white", **kwargs):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color, fg=fg, font=FONT_BTN,
                      relief="flat", cursor="hand2", padx=12, pady=6,
                      activebackground=ACCENT2, activeforeground="white", **kwargs)
        return b

    def stat_card(self, parent, label, value, color=ACCENT, sub=None, delta=None, delta_color=None):
        f = self.card(parent)
        inner = tk.Frame(f, bg=CARD)
        inner.pack(fill="both", expand=True, padx=16, pady=14)

        top_row = tk.Frame(inner, bg=CARD)
        top_row.pack(fill="x")
        tk.Label(top_row, text=label, font=FONT_SMALL,
                 bg=CARD, fg=MUTED).pack(side="left")

        val_row = tk.Frame(inner, bg=CARD)
        val_row.pack(fill="x", pady=(6, 0))
        tk.Label(val_row, text=str(value), font=FONT_NUM,
                 bg=CARD, fg=color).pack(side="left")
        if delta:
            dc = delta_color or (SUCCESS if "+" in str(delta) else DANGER)
            tk.Label(val_row, text=str(delta), font=("Segoe UI", 10, "bold"),
                     bg=CARD, fg=dc).pack(side="left", padx=(8, 0), pady=(8, 0))

        if sub:
            tk.Label(inner, text=sub, font=FONT_TINY,
                     bg=CARD, fg=MUTED2).pack(anchor="w", pady=(3, 0))

        # colored left accent bar
        accent = tk.Frame(f, bg=color, width=4)
        accent.place(relx=0, rely=0, relheight=1, width=4)
        return f

    def section_title(self, parent, text, side="left"):
        lbl = tk.Label(parent, text=text.upper(),
                       font=FONT_CAP, bg=BG, fg=MUTED)
        lbl.pack(anchor="w", pady=(12, 4))
        return lbl

    def _table_head_style(self):
        style = ttk.Style()
        style.configure("Academy.Treeview",
                        font=("Segoe UI", 9),
                        rowheight=28,
                        background=CARD,
                        fieldbackground=CARD,
                        foreground=TEXT2,
                        borderwidth=0)
        style.configure("Academy.Treeview.Heading",
                        font=FONT_CAP,
                        background=HEADER_BG,
                        foreground=MUTED,
                        relief="flat",
                        borderwidth=0)
        style.map("Academy.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])
        return "Academy.Treeview"


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.stats_frame = tk.Frame(self, bg=BG)
        self.stats_frame.pack(fill="x", padx=28, pady=(18, 0))
        self.ml_strip    = tk.Frame(self, bg=BG)
        self.ml_strip.pack(fill="x", padx=28, pady=(8, 0))
        self.bottom      = tk.Frame(self, bg=BG)
        self.bottom.pack(fill="both", expand=True, padx=28, pady=(12, 16))

    def refresh(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()
        for w in self.ml_strip.winfo_children():
            w.destroy()
        for w in self.bottom.winfo_children():
            w.destroy()

        conn = cads.get_conn()
        na = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
        nm = conn.execute("SELECT COUNT(*) FROM materias").fetchone()[0]
        nn = conn.execute("SELECT COUNT(*) FROM notas WHERE n1 IS NOT NULL").fetchone()[0]
        n_risco = conn.execute(
            "SELECT COUNT(*) FROM ml_features WHERE status_encoded IN (0, 1)"
        ).fetchone()[0]
        conn.close()

        # KPI row
        kpis = [
            ("Alunos ativos",    na,      ACCENT,   "em todas as turmas", None),
            ("Matérias",         nm,      INFO,     "disciplinas cadastradas", None),
            ("Notas lançadas",   nn,      SUCCESS,  "registros de nota", None),
            ("Em risco (IA)",    n_risco, DANGER,   "previsto pelo modelo RF_M3", None),
        ]
        for label, val, col, sub, delta in kpis:
            c = self.stat_card(self.stats_frame, label, val, col, sub=sub, delta=delta)
            c.pack(side="left", padx=(0, 12), ipadx=4, fill="x", expand=True)

        # ML model status strip
        self._build_ml_strip()

        # Salas table
        left = tk.Frame(self.bottom, bg=BG)
        left.pack(fill="both", expand=True)

        tk.Label(left, text="ALUNOS POR TURMA", font=FONT_CAP,
                 bg=BG, fg=MUTED).pack(anchor="w", pady=(0, 6))

        c = self.card(left)
        c.pack(fill="both", expand=True)

        style_name = self._table_head_style()
        cols = ("Turma", "Código", "Alunos", "Em Risco")
        tv = ttk.Treeview(c, columns=cols, show="headings",
                          style=style_name, height=8)
        for col in cols:
            tv.heading(col, text=col)
            tv.column(col, anchor="center", width=160)
        tv.column("Turma", anchor="w", width=220)

        conn = cads.get_conn()
        salas = conn.execute("""
            SELECT s.nome, s.codigo, COUNT(DISTINCT a.id) as cnt,
                   SUM(CASE WHEN f.status_encoded IN (0,1) THEN 1 ELSE 0 END) as risco
            FROM salas s
            LEFT JOIN alunos a ON a.sala_id = s.id
            LEFT JOIN ml_features f ON f.aluno_id = a.id
            GROUP BY s.id ORDER BY s.id
        """).fetchall()
        conn.close()

        for i, r in enumerate(salas):
            risco_val = r[3] if r[3] else 0
            tag = "risk" if risco_val > 5 else ("alt" if i % 2 else "")
            tv.insert("", "end", values=(r[0], r[1], r[2], risco_val), tags=(tag,))

        tv.tag_configure("alt",  background=ROW_ALT)
        tv.tag_configure("risk", background=RED_L)

        sb = ttk.Scrollbar(c, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        tv.pack(fill="both", expand=True, padx=1, pady=1)

    def _build_ml_strip(self):
        import json
        from pathlib import Path as P
        models_dir = P(__file__).parent.parent / "ml_models"
        if not models_dir.exists():
            models_dir = P(__file__).parent.parent / "02-ML" / "ml_models"
        if not any(models_dir.glob("RF_M*.json")):
            # try root-level ml_models
            alt = P(__file__).parent.parent
            if (alt / "ml_models").exists():
                models_dir = alt / "ml_models"

        strip = tk.Frame(self.ml_strip, bg="#1E293B",
                         highlightbackground="#334155", highlightthickness=1)
        strip.pack(fill="x")

        inner = tk.Frame(strip, bg="#1E293B")
        inner.pack(fill="x", padx=16, pady=10)

        tk.Label(inner, text="✦  MODELOS IA", font=FONT_CAP,
                 bg="#1E293B", fg=ACCENT2).pack(side="left", padx=(0, 16))

        for name in ["RF_M1", "RF_M2", "RF_M3"]:
            meta_file = models_dir / f"{name}_metadata.json"
            ok = meta_file.exists()
            try:
                acc = json.loads(meta_file.read_text(encoding="utf-8")).get("accuracy", 0) if ok else 0
                acc_str = f"{acc:.1%}" if acc else "—"
            except Exception:
                acc_str = "—"

            badge = tk.Frame(inner, bg="#334155",
                             highlightbackground="#475569", highlightthickness=1)
            badge.pack(side="left", padx=4, ipady=4, ipadx=8)
            tk.Label(badge, text=name, font=("Segoe UI", 9, "bold"),
                     bg="#334155", fg="white").pack(side="left", padx=(4, 4))
            color = SUCCESS if ok else MUTED2
            dot = "●" if ok else "○"
            tk.Label(badge, text=f"{dot} {acc_str}", font=FONT_TINY,
                     bg="#334155", fg=color).pack(side="left", padx=(0, 4))

        tk.Label(inner, text="RF_M3 em produção  •  91.3% acurácia",
                 font=FONT_TINY, bg="#1E293B", fg=MUTED2).pack(side="right")


# ── Alunos ────────────────────────────────────────────────────────────────────

class AlunosPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        # Controls
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=28, pady=(14, 8))

        tk.Label(ctrl, text="Turma:", font=FONT_SMALL, bg=BG, fg=MUTED).pack(side="left")
        self.sala_var = tk.StringVar()
        self.sala_cb = ttk.Combobox(ctrl, textvariable=self.sala_var,
                                    state="readonly", width=22, font=FONT_BODY)
        self.sala_cb.pack(side="left", padx=(4, 12))
        self.sala_cb.bind("<<ComboboxSelected>>", lambda e: self._load_alunos())

        tk.Label(ctrl, text="Nome:", font=FONT_SMALL, bg=BG, fg=MUTED).pack(side="left")
        self.nome_var = tk.StringVar()
        nome_entry = tk.Entry(ctrl, textvariable=self.nome_var,
                              font=FONT_BODY, width=22,
                              relief="flat", bg=CARD,
                              highlightbackground=BORDER, highlightthickness=1)
        nome_entry.pack(side="left", padx=(4, 12), ipady=4)

        self.btn(ctrl, "+ Adicionar Aluno", self._add_aluno).pack(side="left", padx=4)
        self.btn(ctrl, "+200 Genéricos", self._add_200, color=WARN).pack(side="left", padx=4)
        self.btn(ctrl, "Remover", self._del_aluno, color=DANGER).pack(side="left", padx=4)
        self.btn(ctrl, "Atribuir Matérias", self._atribuir, color=SUCCESS).pack(side="left", padx=4)

        # Table
        c = self.card(self)
        c.pack(fill="both", expand=True, padx=28, pady=(0, 16))

        style_name = self._table_head_style()
        cols = ("Matrícula", "Nome", "Turma")
        self.tv = ttk.Treeview(c, columns=cols, show="headings",
                               style=style_name)
        self.tv.heading("Matrícula", text="MATRÍCULA")
        self.tv.heading("Nome",      text="NOME")
        self.tv.heading("Turma",     text="TURMA")
        self.tv.column("Matrícula", width=110, anchor="center")
        self.tv.column("Nome",      width=300, anchor="w")
        self.tv.column("Turma",     width=200, anchor="center")

        sb = ttk.Scrollbar(c, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True, padx=1, pady=1)
        self.tv.tag_configure("alt", background=ROW_ALT)

    def refresh(self):
        salas = cads.get_salas()
        self._sala_map = {s['nome']: s['id'] for s in salas}
        self.sala_cb['values'] = ["Todas"] + [s['nome'] for s in salas]
        if not self.sala_var.get():
            self.sala_var.set("Todas")
        self._load_alunos()

    def _load_alunos(self):
        sala_id = None
        if self.sala_var.get() != "Todas":
            sala_id = self._sala_map.get(self.sala_var.get())
        alunos = cads.get_alunos(sala_id)
        self.tv.delete(*self.tv.get_children())
        for i, a in enumerate(alunos):
            tag = "alt" if i % 2 else ""
            self.tv.insert("", "end", iid=str(a['id']),
                           values=(a['matricula'], a['nome'], a['sala_nome']),
                           tags=(tag,))

    def _get_sala_id(self):
        nome = self.sala_var.get()
        if nome == "Todas" or not nome:
            messagebox.showwarning("Atenção", "Selecione uma turma específica.")
            return None
        return self._sala_map.get(nome)

    def _add_aluno(self):
        sala_id = self._get_sala_id()
        if not sala_id:
            return
        nome = self.nome_var.get().strip().title()
        if not nome:
            messagebox.showwarning("Atenção", "Digite o nome do aluno.")
            return
        cads.adicionar_aluno(nome, sala_id)
        self.nome_var.set("")
        self._load_alunos()

    def _add_200(self):
        sala_id = self._get_sala_id()
        if not sala_id:
            return
        n = cads.gerar_alunos_genericos(200, sala_id)
        messagebox.showinfo("Sucesso", f"{n} alunos genéricos adicionados!")
        self._load_alunos()

    def _del_aluno(self):
        sel = self.tv.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um aluno para remover.")
            return
        if not messagebox.askyesno("Confirmar", f"Remover {len(sel)} aluno(s)?"):
            return
        conn = cads.get_conn()
        for iid in sel:
            conn.execute("DELETE FROM notas WHERE aluno_id=?", (iid,))
            conn.execute("DELETE FROM alunos WHERE id=?", (iid,))
        conn.commit()
        conn.close()
        self._load_alunos()

    def _atribuir(self):
        n = cads.atribuir_materias_todos()
        messagebox.showinfo("Sucesso", f"Matérias atribuídas! {n} registros criados.")
        self._load_alunos()


# ── Matérias ──────────────────────────────────────────────────────────────────

class MateriasPage(BasePage):
    DEFAULT = ["Português", "Matemática", "História", "Geografia", "Ciências",
               "Física", "Química", "Biologia", "Inglês", "Filosofia",
               "Sociologia", "Educação Física", "Arte"]

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=28, pady=(14, 8))

        tk.Label(ctrl, text="Nova Matéria:", font=FONT_SMALL, bg=BG, fg=MUTED).pack(side="left")
        self.nome_var = tk.StringVar()
        tk.Entry(ctrl, textvariable=self.nome_var, font=FONT_BODY, width=26,
                 relief="flat", bg=CARD,
                 highlightbackground=BORDER, highlightthickness=1).pack(
                     side="left", padx=(4, 12), ipady=4)
        self.btn(ctrl, "+ Adicionar", self._add).pack(side="left", padx=4)
        self.btn(ctrl, "Padrão (13)", self._add_default, color=MUTED).pack(side="left", padx=4)
        self.btn(ctrl, "Remover", self._del, color=DANGER).pack(side="left", padx=4)

        c = self.card(self)
        c.pack(fill="both", expand=True, padx=28, pady=(0, 16))

        style_name = self._table_head_style()
        self.tv = ttk.Treeview(c, columns=("ID", "Matéria"), show="headings",
                               style=style_name)
        self.tv.heading("ID",      text="#")
        self.tv.heading("Matéria", text="NOME DA MATÉRIA")
        self.tv.column("ID",      width=60,  anchor="center")
        self.tv.column("Matéria", width=400, anchor="w")

        sb = ttk.Scrollbar(c, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True, padx=1, pady=1)
        self.tv.tag_configure("alt", background=ROW_ALT)

    def refresh(self):
        self._load()

    def _load(self):
        mats = cads.get_materias()
        self.tv.delete(*self.tv.get_children())
        for i, m in enumerate(mats):
            tag = "alt" if i % 2 else ""
            self.tv.insert("", "end", iid=str(m['id']),
                           values=(m['id'], m['nome']), tags=(tag,))

    def _add(self):
        nome = self.nome_var.get().strip().title()
        if not nome:
            return
        cads.adicionar_materia(nome)
        self.nome_var.set("")
        self._load()

    def _add_default(self):
        for m in self.DEFAULT:
            cads.adicionar_materia(m)
        messagebox.showinfo("Sucesso", f"{len(self.DEFAULT)} matérias adicionadas!")
        self._load()

    def _del(self):
        sel = self.tv.selection()
        if not sel:
            return
        if not messagebox.askyesno("Confirmar", f"Remover {len(sel)} matéria(s)?"):
            return
        conn = cads.get_conn()
        for iid in sel:
            conn.execute("DELETE FROM notas WHERE materia_id=?", (iid,))
            conn.execute("DELETE FROM materias WHERE id=?", (iid,))
        conn.commit()
        conn.close()
        self._load()


# ── Notas ─────────────────────────────────────────────────────────────────────

class NotasPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()
        self._aluno_id = None

    def _build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=28, pady=(14, 8))

        tk.Label(top, text="Turma:", font=FONT_SMALL, bg=BG, fg=MUTED).pack(side="left")
        self.sala_var = tk.StringVar()
        self.sala_cb = ttk.Combobox(top, textvariable=self.sala_var,
                                    state="readonly", width=20, font=FONT_BODY)
        self.sala_cb.pack(side="left", padx=(4, 12))
        self.sala_cb.bind("<<ComboboxSelected>>", lambda e: self._load_alunos())

        tk.Label(top, text="Aluno:", font=FONT_SMALL, bg=BG, fg=MUTED).pack(side="left")
        self.aluno_var = tk.StringVar()
        self.aluno_cb = ttk.Combobox(top, textvariable=self.aluno_var,
                                     state="readonly", width=28, font=FONT_BODY)
        self.aluno_cb.pack(side="left", padx=(4, 12))
        self.aluno_cb.bind("<<ComboboxSelected>>", lambda e: self._load_notas())

        self.btn(top, "Aleatório (Aluno)",  self._rand_aluno,  color="#7B1FA2").pack(side="left", padx=3)
        self.btn(top, "Aleatório (Turma)",  self._rand_turma,  color="#4A148C").pack(side="left", padx=3)
        self.btn(top, "Gerar Tudo",         self._rand_all,    color=ACCENT).pack(side="left", padx=3)

        # Table
        pane = tk.Frame(self, bg=BG)
        pane.pack(fill="both", expand=True, padx=28, pady=0)

        c = self.card(pane)
        c.pack(fill="both", expand=True)

        style_name = self._table_head_style()
        cols = ("Matéria", "N1", "N2", "N3", "N4", "Média", "Status")
        self.tv = ttk.Treeview(c, columns=cols, show="headings", style=style_name)
        for col in cols:
            self.tv.heading(col, text=col.upper())
            self.tv.column(col, anchor="center", width=110)
        self.tv.column("Matéria", width=200, anchor="w")

        sb = ttk.Scrollbar(c, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True, padx=1, pady=1)
        self.tv.tag_configure("aprov", background=GRN_L)
        self.tv.tag_configure("recup", background=WARN_L)
        self.tv.tag_configure("reprov", background=RED_L)
        self.tv.tag_configure("alt", background=ROW_ALT)
        self.tv.bind("<Double-1>", self._edit_nota)

        # Edit row
        edit = tk.Frame(self, bg=HEADER_BG,
                        highlightbackground=BORDER, highlightthickness=1)
        edit.pack(fill="x", padx=28, pady=(0, 16))
        inner = tk.Frame(edit, bg=HEADER_BG)
        inner.pack(fill="x", padx=16, pady=8)
        tk.Label(inner, text="Editar nota selecionada →",
                 font=FONT_SMALL, bg=HEADER_BG, fg=MUTED).pack(side="left")
        self._nota_vars = {}
        for n in ["N1", "N2", "N3", "N4"]:
            tk.Label(inner, text=f"{n}:", font=FONT_SMALL,
                     bg=HEADER_BG, fg=MUTED2).pack(side="left", padx=(12, 3))
            v = tk.StringVar()
            tk.Entry(inner, textvariable=v, width=6, font=FONT_BODY,
                     relief="flat", bg=CARD,
                     highlightbackground=BORDER, highlightthickness=1).pack(
                         side="left", ipady=3)
            self._nota_vars[n] = v
        self.btn(inner, "Salvar", self._save_nota, color=SUCCESS).pack(side="left", padx=(14, 0))

    def refresh(self):
        salas = cads.get_salas()
        self._sala_map = {s['nome']: s['id'] for s in salas}
        self.sala_cb['values'] = [s['nome'] for s in salas]
        if salas and not self.sala_var.get():
            self.sala_var.set(salas[0]['nome'])
        self._load_alunos()

    def _load_alunos(self):
        sala_id = self._sala_map.get(self.sala_var.get())
        alunos = cads.get_alunos(sala_id) if sala_id else []
        self._aluno_map = {a['nome']: a['id'] for a in alunos}
        self.aluno_cb['values'] = [a['nome'] for a in alunos]
        if alunos:
            self.aluno_var.set(alunos[0]['nome'])
            self._load_notas()

    def _load_notas(self):
        nome = self.aluno_var.get()
        self._aluno_id = self._aluno_map.get(nome)
        if not self._aluno_id:
            return
        notas = cads.get_notas(self._aluno_id)
        self.tv.delete(*self.tv.get_children())
        for i, n in enumerate(notas):
            vals = [n.get('n1'), n.get('n2'), n.get('n3'), n.get('n4')]
            valid = [v for v in vals if v is not None]
            media = round(sum(valid) / len(valid), 1) if valid else "-"
            if isinstance(media, float):
                if media >= 6:
                    status, tag = "Aprovado", "aprov"
                elif media >= 5:
                    status, tag = "Recuperação", "recup"
                else:
                    status, tag = "Reprovado", "reprov"
            else:
                status, tag = "-", "alt" if i % 2 else ""
            self.tv.insert("", "end", iid=str(n['id']),
                           values=(n['materia_nome'],
                                   n['n1'] or "-", n['n2'] or "-",
                                   n['n3'] or "-", n['n4'] or "-",
                                   media, status),
                           tags=(tag,))

    def _edit_nota(self, event):
        sel = self.tv.selection()
        if not sel:
            return
        vals = self.tv.item(sel[0])['values']
        for i, key in enumerate(["N1", "N2", "N3", "N4"], 1):
            v = vals[i]
            self._nota_vars[key].set("" if v == "-" else str(v))

    def _save_nota(self):
        sel = self.tv.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma matéria na tabela.")
            return
        nota_id = int(sel[0])
        conn = cads.get_conn()
        row = conn.execute("SELECT aluno_id, materia_id FROM notas WHERE id=?", (nota_id,)).fetchone()
        conn.close()
        def parse(v):
            try:
                x = float(v.strip())
                return max(0.0, min(10.0, x))
            except:
                return None
        n1 = parse(self._nota_vars["N1"].get())
        n2 = parse(self._nota_vars["N2"].get())
        n3 = parse(self._nota_vars["N3"].get())
        n4 = parse(self._nota_vars["N4"].get())
        cads.salvar_nota(row['aluno_id'], row['materia_id'], n1, n2, n3, n4)
        self._load_notas()

    def _rand_aluno(self):
        if not self._aluno_id:
            return
        n = cads.gerar_notas_aleatorias(aluno_ids=[self._aluno_id])
        messagebox.showinfo("Sucesso", f"{n} notas geradas para o aluno!")
        self._load_notas()

    def _rand_turma(self):
        sala_id = self._sala_map.get(self.sala_var.get())
        if not sala_id:
            return
        alunos = cads.get_alunos(sala_id)
        ids = [a['id'] for a in alunos]
        n = cads.gerar_notas_aleatorias(aluno_ids=ids)
        messagebox.showinfo("Sucesso", f"{n} notas geradas para a turma!")
        self._load_notas()

    def _rand_all(self):
        if not messagebox.askyesno("Confirmar", "Gerar notas aleatórias para TODOS os alunos?"):
            return
        n = cads.gerar_notas_aleatorias()
        messagebox.showinfo("Sucesso", f"{n} notas geradas!")
        self._load_notas()


# ── Relatório ─────────────────────────────────────────────────────────────────

class RelatorioPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        # Stats bar
        self.stats_f = tk.Frame(self, bg=BG)
        self.stats_f.pack(fill="x", padx=28, pady=(14, 8))

        # Controls
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=28, pady=(0, 8))
        tk.Label(ctrl, text="Filtrar por Turma:", font=FONT_SMALL, bg=BG, fg=MUTED).pack(side="left")
        self.sala_var = tk.StringVar()
        self.sala_cb = ttk.Combobox(ctrl, textvariable=self.sala_var,
                                    state="readonly", width=22, font=FONT_BODY)
        self.sala_cb.pack(side="left", padx=(4, 8))
        self.btn(ctrl, "Atualizar", self._load, color=ACCENT).pack(side="left")

        c = self.card(self)
        c.pack(fill="both", expand=True, padx=28, pady=(0, 16))

        style_name = self._table_head_style()
        cols = ("Aluno", "Turma", "Matéria", "N1", "N2", "N3", "N4", "Média", "Status")
        self.tv = ttk.Treeview(c, columns=cols, show="headings", style=style_name)
        for col in cols:
            self.tv.heading(col, text=col.upper())
            self.tv.column(col, anchor="center", width=90)
        self.tv.column("Aluno",   width=180, anchor="w")
        self.tv.column("Turma",   width=130)
        self.tv.column("Matéria", width=130)

        sb = ttk.Scrollbar(c, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True, padx=1, pady=1)
        self.tv.tag_configure("aprov",  background=GRN_L)
        self.tv.tag_configure("recup",  background=WARN_L)
        self.tv.tag_configure("reprov", background=RED_L)
        self.tv.tag_configure("alt",    background=ROW_ALT)

    def refresh(self):
        salas = cads.get_salas()
        self._sala_map = {s['nome']: s['id'] for s in salas}
        self.sala_cb['values'] = ["Todas"] + [s['nome'] for s in salas]
        if not self.sala_var.get():
            self.sala_var.set("Todas")
        self._load()

    def _load(self):
        sala_id = None
        if self.sala_var.get() != "Todas":
            sala_id = self._sala_map.get(self.sala_var.get())
        dados = cads.get_relatorio(sala_id)

        self.tv.delete(*self.tv.get_children())
        aprov = recup = reprov = total = 0
        for i, d in enumerate(dados):
            vals = [d.get('n1'), d.get('n2'), d.get('n3'), d.get('n4')]
            valid = [v for v in vals if v is not None]
            media = round(sum(valid) / len(valid), 1) if valid else "-"
            if isinstance(media, float):
                total += 1
                if media >= 6:
                    status, tag = "Aprovado", "aprov"; aprov += 1
                elif media >= 5:
                    status, tag = "Recuperação", "recup"; recup += 1
                else:
                    status, tag = "Reprovado", "reprov"; reprov += 1
            else:
                status, tag = "-", "alt" if i % 2 else ""
            self.tv.insert("", "end", values=(
                d['aluno'], d['sala'], d['materia'],
                d.get('n1') or "-", d.get('n2') or "-",
                d.get('n3') or "-", d.get('n4') or "-",
                media, status
            ), tags=(tag,))

        # Update stats bar
        for w in self.stats_f.winfo_children():
            w.destroy()
        for label, val, col in [
            ("Total de notas",    total,                ACCENT),
            ("Aprovados",         aprov,                SUCCESS),
            ("Recuperação",       recup,                WARN),
            ("Reprovados",        reprov,               DANGER),
            ("Taxa aprovação",    f"{aprov/max(total,1)*100:.0f}%", INFO),
        ]:
            c2 = self.stat_card(self.stats_f, label, val, col)
            c2.pack(side="left", padx=(0, 10), ipadx=4, fill="x", expand=True)


# ── ML Features Page (preserved, styling updated) ─────────────────────────────

class MLPage(BasePage):
    FEATURE_DOCS = [
        ("n1 / n2 / n3 / n4",
         "Notas brutas",
         "As quatro notas bimestrais lançadas pelo professor, no intervalo original de 0 a 10.\n"
         "Entram na tabela sem normalização para facilitar leitura humana.\n"
         "No vetor de entrada do modelo elas aparecem normalizadas (n1_norm … n4_norm = nota ÷ 10)."),
        ("Média Pond.",
         "Média ponderada normalizada (feature: media_pond_norm)",
         "Combina as quatro notas com pesos configuráveis:\n"
         "  média = (w1·N1 + w2·N2 + w3·N3 + w4·N4) / (w1+w2+w3+w4)\n\n"
         "Padrão pedagógico: N1=20% N2=25% N3=25% N4=30%\n"
         "(N4 tem peso maior por ser a avaliação final do bimestre)\n\n"
         "O resultado é dividido por 10 para ficar em 0–1.\n"
         "É a feature mais importante para o modelo — resume o desempenho no bimestre."),
        ("Média Geral",
         "Média global do aluno (feature: media_geral_aluno)",
         "Média das médias ponderadas do aluno em TODAS as matérias, normalizada (÷10).\n\n"
         "Captura o perfil geral do aluno independente da matéria atual.\n"
         "Um aluno com média geral alta em recuperação em Física pode ser um caso isolado;\n"
         "um com média geral baixa em recuperação pode precisar de acompanhamento mais amplo."),
        ("Slope",
         "Tendência de progresso (feature: slope_notas)",
         "Inclinação da reta de regressão linear sobre [N1, N2, N3, N4].\n\n"
         "  Slope > 0 → aluno melhorando ao longo do bimestre ↗\n"
         "  Slope < 0 → aluno piorando ↘\n"
         "  Slope ≈ 0 → desempenho estável →\n\n"
         "Normalizado para -1 a +1.\n"
         "Permite detectar alunos em queda antes da reprovação final."),
        ("Variância",
         "Inconsistência das notas (feature: variancia_notas)",
         "Desvio padrão das quatro notas, normalizado por 5 (→ 0–1).\n\n"
         "  Alta variância → notas muito oscilantes (ex: 2, 9, 3, 10)\n"
         "  Baixa variância → desempenho consistente (ex: 6, 6, 7, 6)\n\n"
         "Oscilações extremas podem indicar problemas de assiduidade,\n"
         "cola em algumas avaliações ou dificuldades pontuais."),
        ("Série Norm",
         "Posição na escolaridade (feature: serie_num_norm)",
         "Converte a série do aluno em um número de 0 a 1:\n\n"
         "  6º Fundamental → 0.00\n"
         "  7º Fundamental → 0.17\n"
         "  8º Fundamental → 0.33\n"
         "  9º Fundamental → 0.50\n"
         "  1º Médio       → 0.67\n"
         "  2º Médio       → 0.83\n"
         "  3º Médio       → 1.00\n\n"
         "Permite ao modelo aprender padrões diferentes por nível escolar."),
        ("% Mat.OK",
         "Fração de matérias aprovadas (feature: pct_materias_ok)",
         "Proporção das matérias em que o aluno já tem média ≥ 6.0, de 0 a 1.\n\n"
         "  0%  → reprovado em tudo\n"
         "  50% → metade das matérias aprovadas\n"
         " 100% → aprovado em todas\n\n"
         "Contextualiza o registro atual: um aluno com 0% em tudo e nota 5.9\n"
         "tem perfil diferente de um com 90% e a mesma nota em uma única matéria."),
        ("Média Turma",
         "Média da turma na mesma matéria (feature: media_turma_norm)",
         "Média de todos os alunos da mesma turma (sala) na mesma matéria, normalizada.\n\n"
         "Permite relativizar o desempenho do aluno:\n"
         "  nota 5.0 numa turma com média 4.0 → acima da média\n"
         "  nota 5.0 numa turma com média 7.5 → abaixo da média\n\n"
         "Captura efeitos de turma (professor, horário, dificuldade da matéria)."),
        ("Label / Status",
         "Variável alvo — o que o modelo aprende a prever (status_encoded)",
         "É a saída (y) do modelo — o que queremos predizer:\n\n"
         "  0 = Reprovado    (média ponderada < 5.0)   → vermelho\n"
         "  1 = Recuperação  (média entre 5.0 e 5.9)   → amarelo\n"
         "  2 = Aprovado     (média ≥ 6.0)             → verde\n\n"
         "Problema de classificação multiclasse (3 classes).\n"
         "O modelo treinado com esses dados poderá prever o status de um aluno\n"
         "mesmo antes de todas as notas estarem lançadas."),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._sala_map  = {}
        self.sala_cb    = None
        self.sala_var   = tk.StringVar()
        self._stat_vars = {}
        self._peso_int  = {}
        self.prog_var   = tk.StringVar()
        self.tv         = None
        self._build()

    def _build(self):
        # 1. Stat cards
        info = tk.Frame(self, bg=BG)
        info.pack(fill="x", padx=28, pady=(14, 0))
        for key, label, col in [
            ("total",       "Features geradas", ACCENT),
            ("aprovado",    "Aprovado (2)",      SUCCESS),
            ("recuperacao", "Recuperação (1)",   WARN),
            ("reprovado",   "Reprovado (0)",      DANGER),
        ]:
            f = self.stat_card(info, label, "—", col)
            f.pack(side="left", padx=(0, 10), ipadx=4, fill="x", expand=True)
            v = tk.StringVar(value="—")
            self._stat_vars[key] = v
            # Bind the var to the card's value label (3rd child of inner frame)
            for child in f.winfo_children():
                if isinstance(child, tk.Frame):
                    for gc in child.winfo_children():
                        if isinstance(gc, tk.Frame):
                            sub = gc.winfo_children()
                            if sub and isinstance(sub[0], tk.Label):
                                sub[0].configure(textvariable=v)
                                break

        # 2. Pesos card
        pw = self.card(self)
        pw.pack(fill="x", padx=28, pady=10)
        ph = tk.Frame(pw, bg=CARD)
        ph.pack(fill="x", padx=18, pady=(12, 4))
        tk.Label(ph, text="Pesos da Média Ponderada", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")
        tk.Label(ph, text="(somam 1.0 automaticamente ao gerar)",
                 font=FONT_SMALL, bg=CARD, fg=MUTED).pack(side="left", padx=10)
        self.btn(ph, "? O que são pesos?", self._help_pesos,
                 color=ACCENT2).pack(side="right", padx=4)

        pb = tk.Frame(pw, bg=CARD)
        pb.pack(fill="x", padx=18, pady=(0, 14))

        pesos_def = {"N1": 0.20, "N2": 0.25, "N3": 0.25, "N4": 0.30}
        cores     = {"N1": ACCENT2, "N2": ACCENT, "N3": "#3730A3", "N4": "#1E1B4B"}
        self._peso_int = {n: int(round(v * 100)) for n, v in pesos_def.items()}

        for nota in ["N1", "N2", "N3", "N4"]:
            cor = cores[nota]
            box = tk.Frame(pb, bg=CARD,
                           highlightbackground=BORDER, highlightthickness=1)
            box.pack(side="left", padx=8, ipadx=12, ipady=8)
            tk.Label(box, text=nota, font=("Segoe UI", 13, "bold"),
                     bg=CARD, fg=cor).pack(pady=(4, 2))
            disp = tk.Label(box, text=f"{self._peso_int[nota]}%",
                            font=("Segoe UI", 16, "bold"), bg=CARD, fg=cor, width=5)
            disp.pack()
            sub_lbl = tk.Label(box, text=f"= {self._peso_int[nota]/100:.2f}",
                               font=FONT_TINY, bg=CARD, fg=MUTED2)
            sub_lbl.pack(pady=(0, 4))
            brow = tk.Frame(box, bg=CARD)
            brow.pack(pady=(0, 4))

            def make_dec(n=nota, d=disp, s=sub_lbl):
                def fn():
                    self._peso_int[n] = max(5, self._peso_int[n] - 5)
                    d.configure(text=f"{self._peso_int[n]}%")
                    s.configure(text=f"= {self._peso_int[n]/100:.2f}")
                return fn

            def make_inc(n=nota, d=disp, s=sub_lbl):
                def fn():
                    self._peso_int[n] = min(70, self._peso_int[n] + 5)
                    d.configure(text=f"{self._peso_int[n]}%")
                    s.configure(text=f"= {self._peso_int[n]/100:.2f}")
                return fn

            tk.Button(brow, text=" − ", font=("Segoe UI", 11, "bold"),
                      bg=HEADER_BG, fg=cor, relief="flat", cursor="hand2",
                      activebackground=BORDER, command=make_dec()).pack(side="left", padx=2)
            tk.Button(brow, text=" + ", font=("Segoe UI", 11, "bold"),
                      bg=HEADER_BG, fg=cor, relief="flat", cursor="hand2",
                      activebackground=BORDER, command=make_inc()).pack(side="left", padx=2)

        # 3. Action bar
        act = tk.Frame(self, bg=BG)
        act.pack(fill="x", padx=28, pady=4)
        self.sala_cb = ttk.Combobox(act, textvariable=self.sala_var,
                                    state="readonly", width=20, font=FONT_BODY)
        self.sala_cb.pack(side="left", padx=(0, 8))
        self.btn(act, "Gerar Features ML",    self._gerar,          color=ACCENT).pack(side="left", padx=3)
        self.btn(act, "Exportar CSV",         self._exportar_csv,   color=MUTED).pack(side="left", padx=3)
        self.btn(act, "Atualizar",            self._load_table,     color=ACCENT2).pack(side="left", padx=3)
        self.btn(act, "? Entender os dados",  self._help_dados,     color=INFO).pack(side="left", padx=3)
        tk.Label(act, textvariable=self.prog_var, font=FONT_SMALL,
                 bg=BG, fg=SUCCESS).pack(side="left", padx=10)

        # 4. Feature table
        tc = self.card(self)
        tc.pack(fill="both", expand=True, padx=28, pady=(0, 10))
        thead = tk.Frame(tc, bg=CARD)
        thead.pack(fill="x", padx=8, pady=(6, 0))
        tk.Label(thead, text="Duplo clique em uma linha para ver detalhes  |  "
                 "Clique nos cabeçalhos para ordenar",
                 font=FONT_TINY, bg=CARD, fg=MUTED2).pack(side="left")
        self.btn(thead, "Legenda de colunas", self._help_colunas,
                 color=MUTED).pack(side="right", padx=4, pady=2)

        style_name = self._table_head_style()
        cols = ("Aluno", "Turma", "Matéria",
                "N1", "N2", "N3", "N4",
                "Média Pond.", "Média Geral", "Slope", "Variância",
                "Série Norm", "% Mat.OK", "Média Turma",
                "Label", "Status")
        self.tv = ttk.Treeview(tc, columns=cols, show="headings",
                               selectmode="browse", style=style_name)
        widths = [160, 120, 120, 48, 48, 48, 48, 88, 88, 70, 75, 75, 68, 85, 52, 90]
        for col, w in zip(cols, widths):
            self.tv.heading(col, text=col.upper() if len(col) <= 8 else col,
                            command=lambda c=col: self._sort_col(c))
            self.tv.column(col, anchor="center", width=w, minwidth=w)
        for c in ("Aluno", "Turma", "Matéria"):
            self.tv.column(c, anchor="w")

        sb_x = ttk.Scrollbar(tc, orient="horizontal", command=self.tv.xview)
        sb_y = ttk.Scrollbar(tc, orient="vertical",   command=self.tv.yview)
        self.tv.configure(xscrollcommand=sb_x.set, yscrollcommand=sb_y.set)
        sb_x.pack(side="bottom", fill="x")
        sb_y.pack(side="right",  fill="y")
        self.tv.pack(fill="both", expand=True, padx=1, pady=1)
        self.tv.tag_configure("aprov",  background=GRN_L)
        self.tv.tag_configure("recup",  background=WARN_L)
        self.tv.tag_configure("reprov", background=RED_L)
        self.tv.tag_configure("alt",    background=ROW_ALT)
        self.tv.bind("<Double-1>", self._detail_row)
        self._sort_state = {}

    def refresh(self):
        salas = cads.get_salas()
        self._sala_map = {s["nome"]: s["id"] for s in salas}
        if self.sala_cb is None:
            return
        self.sala_cb["values"] = ["Todas"] + [s["nome"] for s in salas]
        if not self.sala_var.get():
            self.sala_var.set("Todas")
        if self._stat_vars:
            self._update_stats()
        if self.tv is not None:
            self._load_table()

    def _update_stats(self):
        total, dist = cads.get_ml_stats()
        self._stat_vars["total"].set(str(total))
        self._stat_vars["aprovado"].set(str(dist.get("Aprovado", 0)))
        self._stat_vars["recuperacao"].set(str(dist.get("Recuperação", 0)))
        self._stat_vars["reprovado"].set(str(dist.get("Reprovado", 0)))

    def _get_sala_id(self):
        nome = self.sala_var.get()
        return self._sala_map.get(nome) if nome != "Todas" else None

    def _gerar(self):
        try:
            raw = {k.lower(): self._peso_int[k] for k in ["N1","N2","N3","N4"]}
            total_p = sum(raw.values())
            if total_p <= 0:
                raise ValueError
            pesos = {k: round(v / total_p, 4) for k, v in raw.items()}
            cads.PESOS_NOTAS = pesos
        except Exception:
            messagebox.showwarning("Pesos inválidos", "Usando padrão 20/25/25/30%.")
            cads.PESOS_NOTAS = {"n1": 0.20, "n2": 0.25, "n3": 0.25, "n4": 0.30}
        sala_id = self._get_sala_id()
        self.prog_var.set("Gerando features...")
        self.update()
        n, stats = cads.gerar_features_ml(sala_id)
        self._update_stats()
        self._load_table()
        self.prog_var.set(
            f"✓ {n} geradas  Aprov:{stats.get('aprovado',0)}  "
            f"Recup:{stats.get('recuperacao',0)}  Reprov:{stats.get('reprovado',0)}"
        )

    def _load_table(self):
        conn = cads.get_conn()
        rows = conn.execute("""
            SELECT aluno_nome, sala_nome, materia_nome,
                   ROUND(COALESCE(n1,0),1) AS n1,
                   ROUND(COALESCE(n2,0),1) AS n2,
                   ROUND(COALESCE(n3,0),1) AS n3,
                   ROUND(COALESCE(n4,0),1) AS n4,
                   ROUND(COALESCE(media_pond_norm,0),3)   AS mp,
                   ROUND(COALESCE(media_geral_aluno,0),3) AS mg,
                   ROUND(COALESCE(slope_notas,0),3)       AS slope,
                   ROUND(COALESCE(variancia_notas,0),3)   AS var,
                   ROUND(COALESCE(serie_num_norm,0),2)    AS serie,
                   ROUND(COALESCE(pct_materias_ok,0),2)   AS pct,
                   ROUND(COALESCE(media_turma_norm,0),3)  AS mt,
                   COALESCE(status_encoded,-1)             AS enc,
                   COALESCE(status_label,"—")              AS lbl
            FROM ml_features
            ORDER BY sala_nome, aluno_nome, materia_nome
            LIMIT 3000
        """).fetchall()
        conn.close()
        self.tv.delete(*self.tv.get_children())
        for i, r in enumerate(rows):
            vals = (
                r["aluno_nome"] or "—", r["sala_nome"] or "—",
                r["materia_nome"] or "—",
                f"{r['n1']:.1f}", f"{r['n2']:.1f}", f"{r['n3']:.1f}", f"{r['n4']:.1f}",
                f"{r['mp']:.3f}", f"{r['mg']:.3f}", f"{r['slope']:+.3f}",
                f"{r['var']:.3f}", f"{r['serie']:.2f}", f"{r['pct']:.0%}",
                f"{r['mt']:.3f}",
                str(r["enc"]) if r["enc"] != -1 else "—",
                r["lbl"],
            )
            enc = r["enc"]
            tag = "aprov" if enc == 2 else "recup" if enc == 1 else "reprov" if enc == 0 else ("alt" if i%2 else "")
            self.tv.insert("", "end", values=vals, tags=(tag,))

    def _sort_col(self, col):
        asc = not self._sort_state.get(col, False)
        self._sort_state[col] = asc
        items = [(self.tv.set(k, col), k) for k in self.tv.get_children("")]
        try:
            items.sort(key=lambda t: float(t[0].replace("%","").replace("+","")), reverse=not asc)
        except ValueError:
            items.sort(key=lambda t: t[0], reverse=not asc)
        for idx, (_, k) in enumerate(items):
            self.tv.move(k, "", idx)

    def _exportar_csv(self):
        sala_id = self._get_sala_id()
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="ml_dataset.csv"
        )
        if not path:
            return
        out, msg = cads.exportar_ml_csv(sala_id, path)
        if out:
            self.prog_var.set(f"✓ {msg}")
            messagebox.showinfo("CSV exportado", f"{msg}\n\nSalvo em:\n{path}")
        else:
            messagebox.showwarning("Aviso", msg)

    def _make_help_win(self, title, w=620, h=500):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry(f"{w}x{h}")
        win.configure(bg=CARD)
        win.resizable(True, True)
        win.grab_set()
        return win

    def _help_pesos(self):
        win = self._make_help_win("Pesos da Média Ponderada", 580, 420)
        tk.Label(win, text="Pesos da Média Ponderada", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(pady=(16, 4))
        txt = tk.Text(win, font=("Consolas", 10), bg=HEADER_BG, fg=TEXT,
                      relief="flat", padx=16, pady=12, wrap="word", height=16)
        txt.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        txt.insert("end", """O que são os pesos?
───────────────────
Cada avaliação bimestral (N1, N2, N3, N4) contribui com um peso
diferente para a média final do aluno na matéria.

Fórmula usada:
   Média = (w1·N1 + w2·N2 + w3·N3 + w4·N4) ÷ (w1+w2+w3+w4)

Padrão pedagógico:
   N1 = 20%  (diagnóstica — começo do bimestre)
   N2 = 25%  (formativa)
   N3 = 25%  (formativa)
   N4 = 30%  (somativa final — maior peso)

Por que personalizar?
─────────────────────
Algumas escolas dão pesos iguais (25% cada).
Outras valorizam mais o progresso (peso crescente N1→N4).
Os pesos aqui configurados são os que o modelo de Machine
Learning vai usar para aprender — pesos diferentes geram
datasets diferentes e, potencialmente, modelos diferentes.
""")
        txt.configure(state="disabled")

    def _help_colunas(self):
        win = self._make_help_win("Legenda de Colunas", w=700, h=560)
        tk.Label(win, text="O que significa cada coluna?", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(pady=(16, 4))
        tk.Label(win, text="Clique em uma coluna para ver detalhes",
                 font=FONT_SMALL, bg=CARD, fg=MUTED).pack(pady=(0, 8))

        pane = tk.Frame(win, bg=CARD)
        pane.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        lb_frame = tk.Frame(pane, bg=CARD)
        lb_frame.pack(side="left", fill="y")
        lb = tk.Listbox(lb_frame, font=FONT_BODY, width=18, relief="flat",
                        bg=HEADER_BG, selectbackground=ACCENT, selectforeground="white",
                        activestyle="none", cursor="hand2")
        lb.pack(fill="y", expand=True)
        for nome, _, _ in self.FEATURE_DOCS:
            lb.insert("end", nome)

        right = tk.Frame(pane, bg=CARD)
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))
        title_lbl = tk.Label(right, text="", font=FONT_HEAD, bg=CARD, fg=ACCENT,
                             anchor="w", wraplength=440, justify="left")
        title_lbl.pack(fill="x")
        detail = tk.Text(right, font=FONT_BODY, bg=HEADER_BG, fg=TEXT,
                         relief="flat", padx=12, pady=10, wrap="word")
        detail.pack(fill="both", expand=True)
        detail.configure(state="disabled")

        def on_select(event):
            sel = lb.curselection()
            if not sel:
                return
            _, titulo, descricao = self.FEATURE_DOCS[sel[0]]
            title_lbl.configure(text=titulo)
            detail.configure(state="normal")
            detail.delete("1.0", "end")
            detail.insert("end", descricao)
            detail.configure(state="disabled")

        lb.bind("<<ListboxSelect>>", on_select)
        lb.selection_set(0)
        on_select(None)

    def _help_dados(self):
        win = self._make_help_win("Entendendo os dados de ML", w=680, h=600)
        nb = ttk.Notebook(win)
        nb.pack(fill="both", expand=True, padx=12, pady=12)
        tabs = [
            ("Objetivo", """O que este módulo faz?
═══════════════════════════════════════════════
Este módulo prepara os dados dos alunos para treinar
um modelo de Machine Learning capaz de PREVER o status
final (Aprovado / Recuperação / Reprovado) de um aluno.

Como funciona o fluxo:
  1. Você lança as notas (N1–N4) dos alunos
  2. Clica em "Gerar Features ML"
  3. O sistema calcula ~11 métricas (features) por aluno×matéria
  4. Cada registro recebe um label (0, 1 ou 2)
  5. Você exporta o CSV e usa num modelo sklearn/PyTorch

Por que isso é útil?
  → Identificar alunos em risco ANTES do final do bimestre
  → Analisar quais fatores mais influenciam a aprovação
  → Personalizar intervenções pedagógicas por perfil"""),
            ("Features (X)", """Features — o vetor de entrada do modelo
═══════════════════════════════════════════════
São os dados numéricos que o modelo recebe para aprender.
Todas estão normalizadas no intervalo 0–1 (exceto slope: -1 a +1).

NOTAS DIRETAS (4 features)
  n1_norm … n4_norm   →  nota ÷ 10

DESEMPENHO (3 features)
  media_pond_norm     →  média ponderada ÷ 10
  media_geral_aluno   →  média do aluno em TODAS as matérias ÷ 10
  media_turma_norm    →  média da turma na matéria ÷ 10

COMPORTAMENTO (2 features)
  slope_notas         →  tendência N1→N4 (-1=caindo, +1=subindo)
  variancia_notas     →  inconsistência (0=estável, 1=muito oscilante)

CONTEXTO (2 features)
  serie_num_norm      →  posição na escolaridade (6F=0 … 3M=1)
  pct_materias_ok     →  % de matérias com média ≥ 6

Total: 11 features numéricas por amostra"""),
            ("Label (y)", """Label — o que o modelo aprende a prever
═══════════════════════════════════════════════
Coluna: status_encoded  (variável alvo / target)

Valores possíveis:
  0 = Reprovado    →  média ponderada < 5.0
  1 = Recuperação  →  média ponderada entre 5.0 e 5.9
  2 = Aprovado     →  média ponderada ≥ 6.0

Tipo de problema: Classificação multiclasse (3 classes)

Modelos recomendados:
  • Random Forest       → sklearn.ensemble.RandomForestClassifier
  • Gradient Boosting   → sklearn.ensemble.GradientBoostingClassifier
  • Rede Neural (MLP)   → sklearn.neural_network.MLPClassifier
  • PyTorch / Keras     → modelo sequencial com softmax na saída"""),
            ("Dicas", """Dicas para obter bons resultados
═══════════════════════════════════════════════
VOLUME DE DADOS
  → Mínimo recomendado: 500 amostras (aluno × matéria)
  → Ideal: 2.000+ para redes neurais
  → Use "+200 Alunos Genéricos" + notas aleatórias para testar

BALANCEAMENTO DE CLASSES
  → Se 90% das amostras são "Aprovado", o modelo aprende
    a dizer "Aprovado" pra tudo e parece ter 90% de acurácia
  → Use class_weight="balanced" no sklearn para compensar

FEATURES MAIS IMPORTANTES
  → media_pond_norm e pct_materias_ok costumam ser as mais
    preditivas — verifique com model.feature_importances_

PRÓXIMOS PASSOS SUGERIDOS
  1. Exportar CSV → ml_dataset.csv
  2. Abrir no Jupyter Notebook / Google Colab
  3. Treinar com RandomForest para baseline
  4. Analisar feature importances
  5. Iterar com redes neurais"""),
        ]
        for tab_title, tab_text in tabs:
            frame = tk.Frame(nb, bg=CARD)
            nb.add(frame, text=tab_title)
            txt = tk.Text(frame, font=("Consolas", 10), bg=HEADER_BG, fg=TEXT,
                          relief="flat", padx=16, pady=14, wrap="word")
            sb = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
            txt.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y")
            txt.pack(fill="both", expand=True)
            txt.insert("end", tab_text.strip())
            txt.configure(state="disabled")

    def _detail_row(self, event):
        sel = self.tv.selection()
        if not sel:
            return
        vals = self.tv.item(sel[0])["values"]
        cols = ("Aluno","Turma","Matéria","N1","N2","N3","N4",
                "Média Pond.","Média Geral","Slope","Variância",
                "Série Norm","% Mat.OK","Média Turma","Label","Status")
        descs = {
            "N1":"Nota bimestral 1 (bruta)",
            "N2":"Nota bimestral 2 (bruta)",
            "N3":"Nota bimestral 3 (bruta)",
            "N4":"Nota bimestral 4 (bruta, maior peso)",
            "Média Pond.":"Média ponderada normalizada (0–1)",
            "Média Geral":"Média global do aluno em todas as matérias (0–1)",
            "Slope":"Tendência N1→N4: negativo=caindo, positivo=subindo (-1 a +1)",
            "Variância":"Inconsistência das notas (0=estável, 1=muito oscilante)",
            "Série Norm":"Posição na escolaridade: 6º Fund.=0.00, 3º Médio=1.00",
            "% Mat.OK":"Fração de matérias com média ≥ 6 (0–100%)",
            "Média Turma":"Média da turma na mesma matéria, normalizada (0–1)",
            "Label":"Código do status: 0=Reprovado | 1=Recuperação | 2=Aprovado",
            "Status":"Status final calculado pela média ponderada",
        }
        win = self._make_help_win(f"{vals[0]} — {vals[2]}", w=480, h=440)
        tk.Label(win, text=f"{vals[0]}", font=FONT_HEAD, bg=CARD, fg=TEXT).pack(pady=(14,2))
        tk.Label(win, text=f"{vals[1]}  ·  {vals[2]}", font=FONT_BODY, bg=CARD, fg=MUTED).pack(pady=(0,10))
        tbl = tk.Frame(win, bg=CARD)
        tbl.pack(fill="both", expand=True, padx=20, pady=(0,16))
        status_colors = {"Aprovado": SUCCESS, "Recuperação": WARN, "Reprovado": DANGER}
        for i, (col, val) in enumerate(zip(cols[3:], vals[3:])):
            bg = ROW_ALT if i % 2 == 0 else CARD
            row_f = tk.Frame(tbl, bg=bg)
            row_f.pack(fill="x")
            tk.Label(row_f, text=col, font=("Segoe UI", 9, "bold"),
                     bg=bg, fg=TEXT, width=14, anchor="w").pack(side="left", padx=(8,4), pady=3)
            fc = status_colors.get(str(val), ACCENT) if col == "Status" else TEXT
            tk.Label(row_f, text=str(val), font=FONT_SMALL,
                     bg=bg, fg=fc, anchor="w").pack(side="left", padx=4)
            desc = descs.get(col, "")
            if desc:
                tk.Label(row_f, text=f"← {desc}", font=FONT_TINY,
                         bg=bg, fg=MUTED2, anchor="w").pack(side="left", padx=(8,4))


# ── Importar ──────────────────────────────────────────────────────────────────

class ImportarPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=28, pady=(14, 16))

        # File picker card
        pick_card = self.card(outer)
        pick_card.pack(fill="x", pady=(0, 10))
        top = tk.Frame(pick_card, bg=CARD)
        top.pack(fill="x", padx=20, pady=14)
        tk.Label(top, text="Selecionar Arquivo", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")
        right = tk.Frame(top, bg=CARD)
        right.pack(side="right")
        self.btn(right, "Escolher .xlsx / .csv", self._escolher, color=ACCENT).pack(side="left", padx=5)
        self.btn(right, "Formatos suportados",   self._show_help, color=MUTED).pack(side="left", padx=5)
        self.file_var = tk.StringVar(value="Nenhum arquivo selecionado")
        self.file_lbl = tk.Label(pick_card, textvariable=self.file_var,
                                 font=FONT_SMALL, bg=CARD, fg=MUTED2, wraplength=800)
        self.file_lbl.pack(padx=20, pady=(0, 8))

        # Preview card
        prev_card = self.card(outer)
        prev_card.pack(fill="x", pady=(0, 10))
        prev_top = tk.Frame(prev_card, bg=CARD)
        prev_top.pack(fill="x", padx=20, pady=10)
        tk.Label(prev_top, text="Pré-visualização", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")
        self.btn(prev_top, "Pré-visualizar", self._preview, color=INFO).pack(side="right", padx=5)
        style_name = self._table_head_style()
        self.prev_tv = ttk.Treeview(prev_card, show="headings", height=5, style=style_name)
        prev_sb = ttk.Scrollbar(prev_card, orient="vertical", command=self.prev_tv.yview)
        self.prev_tv.configure(yscrollcommand=prev_sb.set)
        prev_sb.pack(side="right", fill="y", padx=(0, 5), pady=5)
        self.prev_tv.pack(fill="x", padx=5, pady=(0, 5))

        # Options card
        opt_card = self.card(outer)
        opt_card.pack(fill="x", pady=(0, 10))
        opt_top = tk.Frame(opt_card, bg=CARD)
        opt_top.pack(fill="x", padx=20, pady=12)
        tk.Label(opt_top, text="Opções de Importação", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")
        opts = tk.Frame(opt_card, bg=CARD)
        opts.pack(fill="x", padx=20, pady=(0, 12))
        self.opt_criar_alunos   = tk.BooleanVar(value=True)
        self.opt_criar_materias = tk.BooleanVar(value=True)
        self.opt_sobrescrever   = tk.BooleanVar(value=False)
        for var, text in [
            (self.opt_criar_alunos,   "Criar alunos novos automaticamente"),
            (self.opt_criar_materias, "Criar matérias novas automaticamente"),
            (self.opt_sobrescrever,   "Sobrescrever notas existentes"),
        ]:
            tk.Checkbutton(opts, text=text, variable=var,
                           bg=CARD, font=FONT_BODY,
                           activebackground=CARD).pack(side="left", padx=(0, 20))

        # Action bar
        action = tk.Frame(outer, bg=BG)
        action.pack(fill="x", pady=5)
        self.btn(action, "Importar Dados", self._importar, color=SUCCESS).pack(side="left", padx=5, ipadx=10)
        self.progress = ttk.Progressbar(action, mode="indeterminate", length=200)
        self.progress.pack(side="left", padx=15)

        # Log
        log_card = self.card(outer)
        log_card.pack(fill="both", expand=True, pady=(5, 0))
        log_top = tk.Frame(log_card, bg=CARD)
        log_top.pack(fill="x", padx=20, pady=8)
        tk.Label(log_top, text="Log de Importação", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")
        self.btn(log_top, "Limpar", self._clear_log, color=MUTED).pack(side="right")
        self.log = tk.Text(log_card, height=8, font=("Consolas", 9),
                           bg="#0F172A", fg="#CBD5E1", relief="flat",
                           state="disabled", wrap="word")
        log_sb = ttk.Scrollbar(log_card, orient="vertical", command=self.log.yview)
        self.log.configure(yscrollcommand=log_sb.set)
        log_sb.pack(side="right", fill="y", padx=(0, 5), pady=5)
        self.log.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.log.tag_configure("ok",   foreground="#A6E3A1")
        self.log.tag_configure("warn", foreground="#F9E2AF")
        self.log.tag_configure("err",  foreground="#F38BA8")
        self.log.tag_configure("info", foreground="#89B4FA")
        self.log.tag_configure("head", foreground="#CBA6F7", font=("Consolas", 9, "bold"))
        self._filepath = None

    def refresh(self):
        pass

    def _log(self, msg, tag="info"):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n", tag)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _escolher(self):
        path = filedialog.askopenfilename(
            title="Selecionar planilha",
            filetypes=[
                ("Planilhas", "*.xlsx *.xls *.csv"),
                ("Excel", "*.xlsx *.xls"),
                ("CSV", "*.csv"),
                ("Todos", "*.*"),
            ]
        )
        if path:
            self._filepath = path
            self.file_var.set(f"{Path(path).name}  ({Path(path).stat().st_size // 1024 + 1} KB)")
            self.file_lbl.configure(fg=ACCENT)
            self._preview()

    def _preview(self):
        if not self._filepath:
            messagebox.showwarning("Atenção", "Selecione um arquivo primeiro.")
            return
        try:
            import pandas as pd
            if self._filepath.endswith(".csv"):
                df = pd.read_csv(self._filepath, nrows=8)
            else:
                df = pd.read_excel(self._filepath, nrows=8)
            for col in self.prev_tv["columns"]:
                self.prev_tv.heading(col, text="")
            self.prev_tv.delete(*self.prev_tv.get_children())
            cols = list(df.columns)
            self.prev_tv["columns"] = cols
            self.prev_tv["show"] = "headings"
            for c in cols:
                self.prev_tv.heading(c, text=str(c))
                self.prev_tv.column(c, width=max(80, min(160, len(str(c)) * 12)), anchor="center")
            for i, (_, row) in enumerate(df.iterrows()):
                tag = "alt" if i % 2 else ""
                self.prev_tv.insert("", "end",
                                    values=[str(v) if str(v) != "nan" else "" for v in row],
                                    tags=(tag,))
            self.prev_tv.tag_configure("alt", background=ROW_ALT)
            self._log(f"[Pré-visualização] {len(df)} linhas de '{Path(self._filepath).name}'", "info")
            self._log(f"  Colunas: {', '.join(cols)}", "info")
        except Exception as e:
            self._log(f"[ERRO] Não foi possível pré-visualizar: {e}", "err")

    def _importar(self):
        if not self._filepath:
            messagebox.showwarning("Atenção", "Selecione um arquivo primeiro.")
            return
        self.progress.start(10)
        self._log(f"\n{'─'*60}", "head")
        self._log(f"[INÍCIO] Importando '{Path(self._filepath).name}'...", "head")
        def _run():
            try:
                total, erros, avisos = cads.importar_excel(self._filepath)
                self.after(0, lambda: self._on_done(total, erros, avisos))
            except Exception as e:
                self.after(0, lambda: self._on_error(str(e)))
        threading.Thread(target=_run, daemon=True).start()

    def _on_done(self, total, erros, avisos):
        self.progress.stop()
        self._log(f"[OK] {total} registros importados com sucesso.", "ok")
        for av in avisos:
            self._log(f"[AVISO] {av}", "warn")
        for er in erros:
            self._log(f"[ERRO]  {er}", "err")
        self._log(f"{'─'*60}", "head")
        if erros:
            messagebox.showwarning("Importação concluída com avisos",
                                   f"✓ {total} importados\n⚠ {len(erros)} erro(s)\n"
                                   f"  {len(avisos)} aviso(s)\n\nVeja o log para detalhes.")
        else:
            messagebox.showinfo("Importação concluída",
                                f"✓ {total} registros importados!\n  {len(avisos)} aviso(s)")

    def _on_error(self, msg):
        self.progress.stop()
        self._log(f"[ERRO CRÍTICO] {msg}", "err")
        messagebox.showerror("Erro de importação", msg)

    def _show_help(self):
        win = tk.Toplevel(self)
        win.title("Formatos de importação suportados")
        win.geometry("600x420")
        win.configure(bg=CARD)
        tk.Label(win, text="Formatos de Importação", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(pady=15)
        txt = tk.Text(win, font=("Consolas", 9), bg="#0F172A", fg="#CBD5E1",
                      relief="flat", padx=10, pady=10, wrap="word")
        txt.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        txt.insert("end", """FORMATO A — Padrão do sistema (com Turma)
─────────────────────────────────────────
Aluno        | Turma          | Disciplina  | N1  | N2  | N3  | N4
Ana Lima     | 6º Fundamental | Matemática  | 7.5 | 8.0 | 6.5 | 9.0

FORMATO B — Simples (sem Turma)
─────────────────────────────────────────
Aluno        | Disciplina  | N1  | N2  | N3  | N4
Ana Lima     | Matemática  | 7.5 | 8.0 | 6.5 | 9.0

FORMATO C — P1/P2/P3/P4
─────────────────────────────────────────
Aluno         | Disciplina  | P1  | P2  | P3  | P4

REGRAS GERAIS
─────────────────────────────────────────
• Cabeçalhos podem estar em qualquer ordem
• Alunos e matérias inexistentes são criados automaticamente
• Notas são mescladas (valores existentes mantidos se a célula estiver vazia)
• Notas devem estar entre 0 e 10 (vírgula ou ponto como decimal)
""")
        txt.configure(state="disabled")


# ── Exportar ──────────────────────────────────────────────────────────────────

class ExportarPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(expand=True)

        c = self.card(outer)
        c.pack(padx=0, pady=40, ipadx=40, ipady=10)

        inner = tk.Frame(c, bg=CARD)
        inner.pack(padx=40, pady=20)

        tk.Label(inner, text="Exportar Planilha de Notas",
                 font=FONT_TITLE, bg=CARD, fg=TEXT).pack(pady=(0, 6))
        tk.Label(inner, text="Gera um arquivo .xlsx com todas as notas, médias e status dos alunos.",
                 font=FONT_BODY, bg=CARD, fg=MUTED).pack()

        tk.Label(inner, text="Turma:", font=FONT_SMALL,
                 bg=CARD, fg=MUTED).pack(pady=(20, 4))
        self.sala_var = tk.StringVar()
        self.sala_cb = ttk.Combobox(inner, textvariable=self.sala_var,
                                    state="readonly", width=28, font=FONT_BODY)
        self.sala_cb.pack()

        self.btn(inner, "Exportar Excel", self._exportar,
                 color=SUCCESS).pack(pady=(20, 8), ipadx=20, ipady=2)

        self.status_var = tk.StringVar()
        tk.Label(inner, textvariable=self.status_var, font=FONT_BODY,
                 bg=CARD, fg=ACCENT).pack(pady=(0, 10))

    def refresh(self):
        salas = cads.get_salas()
        self._sala_map = {s['nome']: s['id'] for s in salas}
        self.sala_cb['values'] = ["Todas"] + [s['nome'] for s in salas]
        if not self.sala_var.get():
            self.sala_var.set("Todas")

    def _exportar(self):
        sala_id = None
        if self.sala_var.get() != "Todas":
            sala_id = self._sala_map.get(self.sala_var.get())
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile="notas_exportadas.xlsx"
        )
        if not path:
            return
        out, msg = cads.exportar_excel(sala_id, path)
        if out:
            self.status_var.set(f"✓ Exportado: {Path(path).name} — {msg}")
        else:
            self.status_var.set(f"⚠ {msg}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    app = App()
    style = ttk.Style(app)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    # Academy Treeview base style
    style.configure("Treeview",
                    font=("Segoe UI", 9),
                    rowheight=28,
                    background=CARD,
                    fieldbackground=CARD,
                    foreground=TEXT2,
                    borderwidth=0,
                    relief="flat")
    style.configure("Treeview.Heading",
                    font=FONT_CAP,
                    background=HEADER_BG,
                    foreground=MUTED,
                    relief="flat",
                    borderwidth=0)
    style.map("Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", "white")])

    # Named Academy style (same but allows override)
    style.configure("Academy.Treeview",
                    font=("Segoe UI", 9),
                    rowheight=28,
                    background=CARD,
                    fieldbackground=CARD,
                    foreground=TEXT2,
                    borderwidth=0)
    style.configure("Academy.Treeview.Heading",
                    font=FONT_CAP,
                    background=HEADER_BG,
                    foreground=MUTED,
                    relief="flat",
                    borderwidth=0)
    style.map("Academy.Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", "white")])

    style.configure("TCombobox", font=FONT_BODY)
    style.configure("Horizontal.TProgressbar", troughcolor=BORDER, background=ACCENT)

    try:
        app.mainloop()
    except KeyboardInterrupt:
        app.quit()
    except Exception as e:
        print(f"[ERRO] {e}")
        app.quit()


if __name__ == "__main__":
    main()
