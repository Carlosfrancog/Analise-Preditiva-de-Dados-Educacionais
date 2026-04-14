#!/usr/bin/env python3
"""
Interface Gráfica - Sistema de Cadastro Escolar
Gerencia alunos, matérias e notas por turma
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import random
import sys
from pathlib import Path

# Import backend
import cads

# ── Color Palette ─────────────────────────────────────────────────────────────
BG        = "#F0F4FF"
SIDEBAR   = "#1A237E"
SIDEBAR_H = "#283593"
ACCENT    = "#3949AB"
ACCENT2   = "#5C6BC0"
SUCCESS   = "#2E7D32"
WARN      = "#E65100"
CARD      = "#FFFFFF"
TEXT      = "#1A1A2E"
MUTED     = "#8892B0"
HEADER_BG = "#E8EAF6"
ROW_ALT   = "#F5F7FF"
RED_L     = "#FFEBEE"
GRN_L     = "#E8F5E9"

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_HEAD   = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_BTN    = ("Segoe UI", 10, "bold")
FONT_BIG    = ("Segoe UI", 28, "bold")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        cads.init_db()
        self.title("📚 Sistema Escolar — Notas & Alunos")
        self.geometry("1280x780")
        self.minsize(1100, 680)
        self.configure(bg=BG)
        self._build_ui()
        self._show_page("dashboard")

    # ── Layout ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="📚", font=("Segoe UI", 30),
                 bg=SIDEBAR, fg="white").pack(pady=(20, 0))
        tk.Label(self.sidebar, text="EduNotas", font=("Segoe UI", 14, "bold"),
                 bg=SIDEBAR, fg="white").pack()
        tk.Label(self.sidebar, text="Sistema Escolar", font=("Segoe UI", 8),
                 bg=SIDEBAR, fg=ACCENT2).pack(pady=(0, 20))

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=15, pady=5)

        self._nav_btns = {}
        nav_items = [
            ("dashboard", "🏠  Dashboard"),
            ("alunos",    "👤  Alunos"),
            ("materias",  "📖  Matérias"),
            ("notas",     "✏️  Notas"),
            ("relatorio", "📊  Relatório"),
            ("ml",        "🤖  Machine Learning"),
            ("importar",  "📤  Importar Excel"),
            ("exportar",  "📥  Exportar Excel"),
        ]
        for key, label in nav_items:
            btn = tk.Button(self.sidebar, text=label, font=FONT_BODY,
                            bg=SIDEBAR, fg="white", relief="flat",
                            anchor="w", padx=20, cursor="hand2",
                            activebackground=SIDEBAR_H, activeforeground="white",
                            command=lambda k=key: self._show_page(k))
            btn.pack(fill="x", pady=1)
            self._nav_btns[key] = btn

        # Main area
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        # Pages
        self._pages = {}
        for cls, key in [
            (DashboardPage, "dashboard"),
            (AlunosPage,    "alunos"),
            (MateriasPage,  "materias"),
            (NotasPage,     "notas"),
            (RelatorioPage, "relatorio"),
            (MLPage,        "ml"),
            (ImportarPage,  "importar"),
            (ExportarPage,  "exportar"),
        ]:
            p = cls(self.main, self)
            p.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._pages[key] = p

    def _show_page(self, key):
        for k, btn in self._nav_btns.items():
            btn.configure(bg=SIDEBAR_H if k == key else SIDEBAR)
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


# ── Base Page ─────────────────────────────────────────────────────────────────

class BasePage(tk.Frame):
    def __init__(self, parent, app, title="", icon=""):
        super().__init__(parent, bg=BG)
        self.app = app
        if title:
            hdr = tk.Frame(self, bg=BG)
            hdr.pack(fill="x", padx=30, pady=(20, 5))
            tk.Label(hdr, text=f"{icon}  {title}", font=FONT_TITLE,
                     bg=BG, fg=TEXT).pack(side="left")

    def card(self, parent, **kwargs):
        f = tk.Frame(parent, bg=CARD, relief="flat", bd=0, **kwargs)
        f.configure(highlightbackground="#D0D8F0", highlightthickness=1)
        return f

    def btn(self, parent, text, cmd, color=ACCENT, fg="white", **kwargs):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color, fg=fg, font=FONT_BTN,
                      relief="flat", cursor="hand2", padx=12, pady=6,
                      activebackground=ACCENT2, activeforeground="white", **kwargs)
        return b

    def stat_card(self, parent, label, value, color=ACCENT):
        f = self.card(parent)
        tk.Label(f, text=str(value), font=FONT_BIG, bg=CARD, fg=color).pack(pady=(15, 0))
        tk.Label(f, text=label, font=FONT_SMALL, bg=CARD, fg=MUTED).pack(pady=(0, 15))
        return f


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Dashboard", "🏠")
        self.stats_frame = tk.Frame(self, bg=BG)
        self.stats_frame.pack(fill="x", padx=30, pady=10)
        self.sala_frame = tk.Frame(self, bg=BG)
        self.sala_frame.pack(fill="both", expand=True, padx=30, pady=5)

    def refresh(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()
        for w in self.sala_frame.winfo_children():
            w.destroy()
        conn = cads.get_conn()
        na = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
        nm = conn.execute("SELECT COUNT(*) FROM materias").fetchone()[0]
        nn = conn.execute("SELECT COUNT(*) FROM notas WHERE n1 IS NOT NULL").fetchone()[0]
        conn.close()

        for label, val, col in [
            ("Alunos", na, ACCENT),
            ("Matérias", nm, SUCCESS),
            ("Notas Lançadas", nn, WARN),
        ]:
            c = self.stat_card(self.stats_frame, label, val, col)
            c.pack(side="left", padx=8, ipadx=20)

        # Salas table
        tk.Label(self.sala_frame, text="Alunos por Turma",
                 font=FONT_HEAD, bg=BG, fg=TEXT).pack(anchor="w", pady=(10, 5))
        c = self.card(self.sala_frame)
        c.pack(fill="both", expand=True)
        cols = ("Turma", "Código", "Qtd. Alunos")
        tv = ttk.Treeview(c, columns=cols, show="headings", height=7)
        for col in cols:
            tv.heading(col, text=col)
            tv.column(col, anchor="center", width=180)
        conn = cads.get_conn()
        salas = conn.execute("""
            SELECT s.nome, s.codigo, COUNT(a.id) as cnt
            FROM salas s LEFT JOIN alunos a ON a.sala_id=s.id
            GROUP BY s.id ORDER BY s.id
        """).fetchall()
        conn.close()
        for i, r in enumerate(salas):
            tag = "alt" if i % 2 else ""
            tv.insert("", "end", values=(r[0], r[1], r[2]), tags=(tag,))
        tv.tag_configure("alt", background=ROW_ALT)
        tv.pack(fill="both", expand=True, padx=5, pady=5)


# ── Alunos ────────────────────────────────────────────────────────────────────

class AlunosPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Alunos", "👤")
        self._build()

    def _build(self):
        # Controls
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=30, pady=5)

        tk.Label(ctrl, text="Turma:", font=FONT_BODY, bg=BG).pack(side="left")
        self.sala_var = tk.StringVar()
        self.sala_cb = ttk.Combobox(ctrl, textvariable=self.sala_var,
                                    state="readonly", width=22, font=FONT_BODY)
        self.sala_cb.pack(side="left", padx=5)
        self.sala_cb.bind("<<ComboboxSelected>>", lambda e: self._load_alunos())

        tk.Label(ctrl, text="Nome:", font=FONT_BODY, bg=BG).pack(side="left", padx=(15, 0))
        self.nome_var = tk.StringVar()
        tk.Entry(ctrl, textvariable=self.nome_var, font=FONT_BODY, width=22).pack(side="left", padx=5)

        self.btn(ctrl, "➕ Adicionar Aluno", self._add_aluno).pack(side="left", padx=5)
        self.btn(ctrl, "+200 Alunos Genéricos", self._add_200,
                 color="#FF6F00").pack(side="left", padx=5)
        self.btn(ctrl, "🗑 Remover", self._del_aluno,
                 color="#C62828").pack(side="left", padx=5)
        self.btn(ctrl, "👥 Atribuir Todas as Matérias", self._atribuir,
                 color=SUCCESS).pack(side="left", padx=5)

        # Table
        c = self.card(self, padx=5, pady=5)
        c.pack(fill="both", expand=True, padx=30, pady=10)
        cols = ("Matrícula", "Nome", "Turma")
        self.tv = ttk.Treeview(c, columns=cols, show="headings")
        for col in cols:
            self.tv.heading(col, text=col)
        self.tv.column("Matrícula", width=100, anchor="center")
        self.tv.column("Nome", width=280)
        self.tv.column("Turma", width=180, anchor="center")
        sb = ttk.Scrollbar(c, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True)
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
        messagebox.showinfo("Sucesso", f"Matérias atribuídas! {n} registros de notas criados.")
        self._load_alunos()


# ── Matérias ──────────────────────────────────────────────────────────────────

class MateriasPage(BasePage):
    DEFAULT = ["Português", "Matemática", "História", "Geografia", "Ciências",
               "Física", "Química", "Biologia", "Inglês", "Filosofia",
               "Sociologia", "Educação Física", "Arte"]

    def __init__(self, parent, app):
        super().__init__(parent, app, "Matérias", "📖")
        self._build()

    def _build(self):
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=30, pady=5)
        tk.Label(ctrl, text="Nova Matéria:", font=FONT_BODY, bg=BG).pack(side="left")
        self.nome_var = tk.StringVar()
        tk.Entry(ctrl, textvariable=self.nome_var, font=FONT_BODY, width=25).pack(side="left", padx=5)
        self.btn(ctrl, "➕ Adicionar", self._add).pack(side="left", padx=5)
        self.btn(ctrl, "📋 Adicionar Padrão", self._add_default, color="#546E7A").pack(side="left", padx=5)
        self.btn(ctrl, "🗑 Remover", self._del, color="#C62828").pack(side="left", padx=5)

        c = self.card(self)
        c.pack(fill="both", expand=True, padx=30, pady=10)
        self.tv = ttk.Treeview(c, columns=("ID", "Matéria"), show="headings")
        self.tv.heading("ID", text="#")
        self.tv.heading("Matéria", text="Nome da Matéria")
        self.tv.column("ID", width=60, anchor="center")
        self.tv.column("Matéria", width=400)
        sb = ttk.Scrollbar(c, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True)
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
        messagebox.showinfo("Sucesso", f"{len(self.DEFAULT)} matérias padrão adicionadas!")
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
        super().__init__(parent, app, "Notas", "✏️")
        self._build()
        self._aluno_id = None

    def _build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=30, pady=5)

        # Filters
        tk.Label(top, text="Turma:", font=FONT_BODY, bg=BG).pack(side="left")
        self.sala_var = tk.StringVar()
        self.sala_cb = ttk.Combobox(top, textvariable=self.sala_var,
                                    state="readonly", width=20, font=FONT_BODY)
        self.sala_cb.pack(side="left", padx=5)
        self.sala_cb.bind("<<ComboboxSelected>>", lambda e: self._load_alunos())

        tk.Label(top, text="Aluno:", font=FONT_BODY, bg=BG).pack(side="left", padx=(10, 0))
        self.aluno_var = tk.StringVar()
        self.aluno_cb = ttk.Combobox(top, textvariable=self.aluno_var,
                                     state="readonly", width=28, font=FONT_BODY)
        self.aluno_cb.pack(side="left", padx=5)
        self.aluno_cb.bind("<<ComboboxSelected>>", lambda e: self._load_notas())

        self.btn(top, "🎲 Notas Aleatórias (Aluno)", self._rand_aluno,
                 color="#7B1FA2").pack(side="left", padx=5)
        self.btn(top, "🎲 Notas Aleatórias (Turma)", self._rand_turma,
                 color="#4A148C").pack(side="left", padx=5)
        self.btn(top, "🎲 Gerar Tudo", self._rand_all,
                 color="#1A237E").pack(side="left", padx=5)

        # Notes table
        pane = tk.Frame(self, bg=BG)
        pane.pack(fill="both", expand=True, padx=30, pady=5)

        c = self.card(pane)
        c.pack(fill="both", expand=True)
        cols = ("Matéria", "N1", "N2", "N3", "N4", "Média", "Status")
        self.tv = ttk.Treeview(c, columns=cols, show="headings")
        for col in cols:
            self.tv.heading(col, text=col)
            self.tv.column(col, anchor="center", width=110)
        self.tv.column("Matéria", width=180, anchor="w")
        sb = ttk.Scrollbar(c, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True)
        self.tv.tag_configure("aprov", background=GRN_L)
        self.tv.tag_configure("reprov", background=RED_L)
        self.tv.tag_configure("alt", background=ROW_ALT)
        self.tv.bind("<Double-1>", self._edit_nota)

        # Edit row
        edit = tk.Frame(self, bg=BG)
        edit.pack(fill="x", padx=30, pady=5)
        tk.Label(edit, text="Editar Nota Selecionada →", font=FONT_BODY, bg=BG).pack(side="left")
        self._nota_vars = {}
        for n in ["N1", "N2", "N3", "N4"]:
            tk.Label(edit, text=f"{n}:", font=FONT_BODY, bg=BG).pack(side="left", padx=(10, 2))
            v = tk.StringVar()
            tk.Entry(edit, textvariable=v, width=6, font=FONT_BODY).pack(side="left")
            self._nota_vars[n] = v
        self.btn(edit, "💾 Salvar", self._save_nota, color=SUCCESS).pack(side="left", padx=10)

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
            status = "Aprovado" if isinstance(media, float) and media >= 6 else \
                     "Recuperação" if isinstance(media, float) else "-"
            tag = "aprov" if status == "Aprovado" else "reprov" if status == "Recuperação" else "alt"
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
        super().__init__(parent, app, "Relatório", "📊")
        self._build()

    def _build(self):
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=30, pady=5)
        tk.Label(ctrl, text="Filtrar por Turma:", font=FONT_BODY, bg=BG).pack(side="left")
        self.sala_var = tk.StringVar()
        self.sala_cb = ttk.Combobox(ctrl, textvariable=self.sala_var,
                                    state="readonly", width=22, font=FONT_BODY)
        self.sala_cb.pack(side="left", padx=5)
        self.btn(ctrl, "🔄 Atualizar", self._load, color=ACCENT).pack(side="left", padx=5)

        c = self.card(self)
        c.pack(fill="both", expand=True, padx=30, pady=10)
        cols = ("Aluno", "Turma", "Matéria", "N1", "N2", "N3", "N4", "Média", "Status")
        self.tv = ttk.Treeview(c, columns=cols, show="headings")
        for col in cols:
            self.tv.heading(col, text=col)
            self.tv.column(col, anchor="center", width=90)
        self.tv.column("Aluno", width=180, anchor="w")
        self.tv.column("Turma", width=130)
        self.tv.column("Matéria", width=120)
        sb = ttk.Scrollbar(c, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True)
        self.tv.tag_configure("aprov", background=GRN_L)
        self.tv.tag_configure("reprov", background=RED_L)
        self.tv.tag_configure("alt", background=ROW_ALT)

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
        for i, d in enumerate(dados):
            vals = [d.get('n1'), d.get('n2'), d.get('n3'), d.get('n4')]
            valid = [v for v in vals if v is not None]
            media = round(sum(valid) / len(valid), 1) if valid else "-"
            status = "Aprovado" if isinstance(media, float) and media >= 6 else \
                     "Recuperação" if isinstance(media, float) else "-"
            tag = "aprov" if status == "Aprovado" else "reprov" if status == "Recuperação" else "alt"
            self.tv.insert("", "end", values=(
                d['aluno'], d['sala'], d['materia'],
                d.get('n1') or "-", d.get('n2') or "-",
                d.get('n3') or "-", d.get('n4') or "-",
                media, status
            ), tags=(tag,))



# ── ML Features ───────────────────────────────────────────────────────────────


class MLPage(BasePage):
    # ── Documentação das features (usada nas subjanelas de ajuda) ──────────
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
        super().__init__(parent, app, "Machine Learning", "🤖")
        self._sala_map  = {}
        self.sala_cb    = None
        self.sala_var   = tk.StringVar()
        self._stat_vars = {}
        self._peso_vars = {}   # nota → tk.DoubleVar
        self.prog_var   = tk.StringVar()
        self.tv         = None
        self._build()

    # ── UI ────────────────────────────────────────────────────────────────

    def _build(self):
        # 1. Stat cards
        info = tk.Frame(self, bg=BG)
        info.pack(fill="x", padx=30, pady=(5, 0))
        for key, label, col in [
            ("total",       "Features geradas", ACCENT),
            ("aprovado",    "Aprovado (2)",      SUCCESS),
            ("recuperacao", "Recuperação (1)",   WARN),
            ("reprovado",   "Reprovado (0)",     "#C62828"),
        ]:
            f = self.card(info)
            f.pack(side="left", padx=6, ipadx=16)
            v = tk.StringVar(value="—")
            self._stat_vars[key] = v
            tk.Label(f, textvariable=v, font=FONT_BIG,   bg=CARD, fg=col).pack(pady=(12, 0))
            tk.Label(f, text=label,     font=FONT_SMALL, bg=CARD, fg=MUTED).pack(pady=(0, 12))

        # 2. Pesos card
        pw = self.card(self)
        pw.pack(fill="x", padx=30, pady=6)

        ph = tk.Frame(pw, bg=CARD)
        ph.pack(fill="x", padx=18, pady=(10, 4))
        tk.Label(ph, text="⚖️  Pesos da Média Ponderada", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")
        tk.Label(ph, text="(somam 1.0 automaticamente ao gerar)",
                 font=FONT_SMALL, bg=CARD, fg=MUTED).pack(side="left", padx=10)
        self.btn(ph, "❓ O que são pesos?", self._help_pesos,
                 color="#7986CB").pack(side="right", padx=4)

        pb = tk.Frame(pw, bg=CARD)
        pb.pack(fill="x", padx=18, pady=(0, 12))

        pesos_def = {"N1": 0.20, "N2": 0.25, "N3": 0.25, "N4": 0.30}
        cores     = {"N1": "#5C6BC0", "N2": "#3949AB", "N3": "#1A237E", "N4": "#283593"}
        # _peso_int[nota] = valor em centésimos (int), ex: 20 = 0.20
        self._peso_int = {n: int(round(v * 100)) for n, v in pesos_def.items()}

        for nota in ["N1", "N2", "N3", "N4"]:
            cor = cores[nota]
            box = tk.Frame(pb, bg=CARD, relief="flat",
                           highlightbackground="#D0D8F0", highlightthickness=1)
            box.pack(side="left", padx=8, ipadx=10, ipady=8)

            tk.Label(box, text=nota, font=("Segoe UI", 13, "bold"),
                     bg=CARD, fg=cor).pack(pady=(4, 2))

            # Display label (mostra o valor atual em %)
            disp = tk.Label(box, text=f"{self._peso_int[nota]}%",
                            font=("Segoe UI", 16, "bold"), bg=CARD, fg=cor, width=5)
            disp.pack()

            sub_lbl = tk.Label(box, text=f"= {self._peso_int[nota]/100:.2f}",
                               font=("Segoe UI", 9), bg=CARD, fg=MUTED)
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

            tk.Button(brow, text="  −  ", font=("Segoe UI", 11, "bold"),
                      bg=HEADER_BG, fg=cor, relief="flat", cursor="hand2",
                      activebackground="#D0D8F0",
                      command=make_dec()).pack(side="left", padx=2)
            tk.Button(brow, text="  +  ", font=("Segoe UI", 11, "bold"),
                      bg=HEADER_BG, fg=cor, relief="flat", cursor="hand2",
                      activebackground="#D0D8F0",
                      command=make_inc()).pack(side="left", padx=2)

        # 3. Action bar
        act = tk.Frame(self, bg=BG)
        act.pack(fill="x", padx=30, pady=4)

        self.sala_cb = ttk.Combobox(act, textvariable=self.sala_var,
                                    state="readonly", width=20, font=FONT_BODY)
        self.sala_cb.pack(side="left", padx=(0, 8))

        self.btn(act, "⚙️ Gerar Features ML", self._gerar,
                 color=ACCENT).pack(side="left", padx=3)
        self.btn(act, "📄 Exportar CSV",       self._exportar_csv,
                 color="#546E7A").pack(side="left", padx=3)
        self.btn(act, "🔄 Atualizar",          self._load_table,
                 color=ACCENT2).pack(side="left", padx=3)
        self.btn(act, "❓ Entender os dados",  self._help_dados,
                 color="#7986CB").pack(side="left", padx=3)

        tk.Label(act, textvariable=self.prog_var, font=FONT_SMALL,
                 bg=BG, fg=SUCCESS).pack(side="left", padx=10)

        # 4. Feature table
        tc = self.card(self)
        tc.pack(fill="both", expand=True, padx=30, pady=(0, 8))

        # Header row with help buttons per column
        thead = tk.Frame(tc, bg=CARD)
        thead.pack(fill="x", padx=4, pady=(4, 0))
        tk.Label(thead, text="Clique em qualquer linha para ver detalhes do aluno  |  "
                 "Clique nos cabeçalhos da tabela abaixo para ordenar",
                 font=FONT_SMALL, bg=CARD, fg=MUTED).pack(side="left")
        self.btn(thead, "📖 Legenda de colunas", self._help_colunas,
                 color="#546E7A").pack(side="right", padx=4, pady=2)

        cols = ("Aluno", "Turma", "Matéria",
                "N1", "N2", "N3", "N4",
                "Média Pond.", "Média Geral", "Slope", "Variância",
                "Série Norm", "% Mat.OK", "Média Turma",
                "Label", "Status")
        self.tv = ttk.Treeview(tc, columns=cols, show="headings", selectmode="browse")
        widths  = [160, 120, 120, 48, 48, 48, 48, 88, 88, 70, 75, 75, 68, 85, 52, 90]
        for col, w in zip(cols, widths):
            self.tv.heading(col, text=col,
                            command=lambda c=col: self._sort_col(c))
            self.tv.column(col, anchor="center", width=w, minwidth=w)
        for c in ("Aluno", "Turma", "Matéria"):
            self.tv.column(c, anchor="w")

        sb_x = ttk.Scrollbar(tc, orient="horizontal", command=self.tv.xview)
        sb_y = ttk.Scrollbar(tc, orient="vertical",   command=self.tv.yview)
        self.tv.configure(xscrollcommand=sb_x.set, yscrollcommand=sb_y.set)
        sb_x.pack(side="bottom", fill="x")
        sb_y.pack(side="right",  fill="y")
        self.tv.pack(fill="both", expand=True)
        self.tv.tag_configure("aprov",  background=GRN_L)
        self.tv.tag_configure("recup",  background="#FFF8E1")
        self.tv.tag_configure("reprov", background=RED_L)
        self.tv.tag_configure("alt",    background=ROW_ALT)
        self.tv.bind("<Double-1>", self._detail_row)

        self._sort_state = {}   # col → bool (ascending)

    # ── Logic ─────────────────────────────────────────────────────────────

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
        self.prog_var.set("⏳ Gerando features...")
        self.update()
        n, stats = cads.gerar_features_ml(sala_id)
        self._update_stats()
        self._load_table()
        self.prog_var.set(
            f"✅ {n} geradas  Aprov:{stats.get('aprovado',0)}  "
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
                r["aluno_nome"] or "—",
                r["sala_nome"]  or "—",
                r["materia_nome"] or "—",
                f"{r['n1']:.1f}",
                f"{r['n2']:.1f}",
                f"{r['n3']:.1f}",
                f"{r['n4']:.1f}",
                f"{r['mp']:.3f}",
                f"{r['mg']:.3f}",
                f"{r['slope']:+.3f}",
                f"{r['var']:.3f}",
                f"{r['serie']:.2f}",
                f"{r['pct']:.0%}",
                f"{r['mt']:.3f}",
                str(r["enc"]) if r["enc"] != -1 else "—",
                r["lbl"],
            )
            enc = r["enc"]
            tag = "aprov" if enc == 2 else "recup" if enc == 1 else "reprov" if enc == 0 else ("alt" if i%2 else "")
            self.tv.insert("", "end", values=vals, tags=(tag,))

    def _sort_col(self, col):
        """Ordena a tabela pelo cabeçalho clicado."""
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
            self.prog_var.set(f"✅ {msg}")
            messagebox.showinfo("CSV exportado", f"{msg}\n\nSalvo em:\n{path}")
        else:
            messagebox.showwarning("Aviso", msg)

    # ── Subjanelas de ajuda ───────────────────────────────────────────────

    def _make_help_win(self, title, w=620, h=500):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry(f"{w}x{h}")
        win.configure(bg=CARD)
        win.resizable(True, True)
        win.grab_set()
        return win

    def _help_pesos(self):
        win = self._make_help_win("⚖️  Como funcionam os pesos?", 580, 420)
        tk.Label(win, text="⚖️  Pesos da Média Ponderada", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(pady=(16, 4))
        txt = tk.Text(win, font=("Consolas", 10), bg="#F8F9FF", fg=TEXT,
                      relief="flat", padx=16, pady=12, wrap="word",
                      height=16)
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

Como mudar?
───────────
Use as setas (▲▼) nos campos N1–N4.
Os valores não precisam somar exatamente 1.0 —
o sistema normaliza automaticamente antes de calcular.
""")
        txt.configure(state="disabled")

    def _help_colunas(self):
        win = self._make_help_win("📖  Legenda de Colunas", w=700, h=560)
        tk.Label(win, text="📖  O que significa cada coluna?", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(pady=(16, 4))
        tk.Label(win, text="Clique em uma coluna para ver detalhes",
                 font=FONT_SMALL, bg=CARD, fg=MUTED).pack(pady=(0, 8))

        pane = tk.Frame(win, bg=CARD)
        pane.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Left list
        lb_frame = tk.Frame(pane, bg=CARD)
        lb_frame.pack(side="left", fill="y")
        lb = tk.Listbox(lb_frame, font=FONT_BODY, width=18, relief="flat",
                        bg="#EEF1FA", selectbackground=ACCENT, selectforeground="white",
                        activestyle="none", cursor="hand2")
        lb.pack(fill="y", expand=True)
        for nome, _, _ in self.FEATURE_DOCS:
            lb.insert("end", nome)

        # Right detail
        right = tk.Frame(pane, bg=CARD)
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        title_lbl = tk.Label(right, text="", font=FONT_HEAD, bg=CARD, fg=ACCENT,
                             anchor="w", wraplength=440, justify="left")
        title_lbl.pack(fill="x")

        detail = tk.Text(right, font=("Segoe UI", 10), bg="#F8F9FF", fg=TEXT,
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
        win = self._make_help_win("❓  Entendendo os dados de ML", w=680, h=600)
        nb = ttk.Notebook(win)
        nb.pack(fill="both", expand=True, padx=12, pady=12)

        tabs = [
            ("🎯 Objetivo", """O que este módulo faz?
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

            ("📊 Features (X)", """Features — o vetor de entrada do modelo
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

            ("🏷️ Label (y)", """Label — o que o modelo aprende a prever
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
  • PyTorch / Keras     → modelo sequencial com softmax na saída

Exemplo rápido (sklearn):
─────────────────────────
  import pandas as pd
  from sklearn.ensemble import RandomForestClassifier
  from sklearn.model_selection import train_test_split

  df = pd.read_csv("ml_dataset.csv")
  X  = df.iloc[:, 4:15]   # 11 features
  y  = df["status_encoded"]

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
  model = RandomForestClassifier(n_estimators=100)
  model.fit(X_train, y_train)
  print(model.score(X_test, y_test))"""),

            ("💡 Dicas", """Dicas para obter bons resultados
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

OVERFITTING
  → Use train_test_split (80/20) ou cross_val_score (cv=5)
  → Evite treinar e avaliar no mesmo conjunto

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
            txt = tk.Text(frame, font=("Consolas", 10), bg="#F8F9FF", fg=TEXT,
                          relief="flat", padx=16, pady=14, wrap="word")
            sb  = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
            txt.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y")
            txt.pack(fill="both", expand=True)
            txt.insert("end", tab_text.strip())
            txt.configure(state="disabled")

    def _detail_row(self, event):
        """Duplo clique numa linha → subjanela com todos os dados do registro."""
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
        win = self._make_help_win(f"📋  {vals[0]} — {vals[2]}", w=480, h=440)
        tk.Label(win, text=f"📋  {vals[0]}", font=FONT_HEAD, bg=CARD, fg=TEXT).pack(pady=(14,2))
        tk.Label(win, text=f"{vals[1]}  ·  {vals[2]}", font=FONT_BODY, bg=CARD, fg=MUTED).pack(pady=(0,10))

        tbl = tk.Frame(win, bg=CARD)
        tbl.pack(fill="both", expand=True, padx=20, pady=(0,16))
        status_colors = {"Aprovado": SUCCESS, "Recuperação": WARN, "Reprovado": "#C62828"}

        for i, (col, val) in enumerate(zip(cols[3:], vals[3:])):  # skip Aluno/Turma/Matéria
            bg = "#F5F7FF" if i % 2 == 0 else CARD
            row_f = tk.Frame(tbl, bg=bg)
            row_f.pack(fill="x")
            col_name = tk.Label(row_f, text=col, font=("Segoe UI", 9, "bold"),
                                bg=bg, fg=TEXT, width=14, anchor="w")
            col_name.pack(side="left", padx=(8,4), pady=3)
            fc = status_colors.get(str(val), ACCENT) if col == "Status" else TEXT
            col_val = tk.Label(row_f, text=str(val), font=("Segoe UI", 9),
                               bg=bg, fg=fc, anchor="w")
            col_val.pack(side="left", padx=4)
            desc = descs.get(col, "")
            if desc:
                col_desc = tk.Label(row_f, text=f"← {desc}", font=("Segoe UI", 8),
                                    bg=bg, fg=MUTED, anchor="w")
                col_desc.pack(side="left", padx=(8,4))

# ── Importar ──────────────────────────────────────────────────────────────────

class ImportarPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Importar Excel", "📤")
        self._build()

    def _build(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=40, pady=10)

        # ── Drop zone / file picker card
        pick_card = self.card(outer)
        pick_card.pack(fill="x", pady=(0, 10))

        top = tk.Frame(pick_card, bg=CARD)
        top.pack(fill="x", padx=20, pady=15)

        tk.Label(top, text="📂  Selecionar Arquivo", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")

        right = tk.Frame(top, bg=CARD)
        right.pack(side="right")
        self.btn(right, "Escolher arquivo .xlsx / .csv", self._escolher,
                 color=ACCENT).pack(side="left", padx=5)
        self.btn(right, "ℹ️ Formatos suportados", self._show_help,
                 color="#546E7A").pack(side="left", padx=5)

        self.file_var = tk.StringVar(value="Nenhum arquivo selecionado")
        self.file_lbl = tk.Label(pick_card, textvariable=self.file_var,
                                 font=FONT_SMALL, bg=CARD, fg=MUTED, wraplength=800)
        self.file_lbl.pack(padx=20, pady=(0, 5))

        # ── Preview card
        prev_card = self.card(outer)
        prev_card.pack(fill="x", pady=(0, 10))

        prev_top = tk.Frame(prev_card, bg=CARD)
        prev_top.pack(fill="x", padx=20, pady=10)
        tk.Label(prev_top, text="👁  Pré-visualização", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")
        self.btn(prev_top, "🔍 Pré-visualizar", self._preview,
                 color=ACCENT2).pack(side="right", padx=5)

        self.prev_tv = ttk.Treeview(prev_card, show="headings", height=5)
        prev_sb = ttk.Scrollbar(prev_card, orient="vertical", command=self.prev_tv.yview)
        self.prev_tv.configure(yscrollcommand=prev_sb.set)
        prev_sb.pack(side="right", fill="y", padx=(0, 5), pady=5)
        self.prev_tv.pack(fill="x", padx=5, pady=(0, 5))

        # ── Options card
        opt_card = self.card(outer)
        opt_card.pack(fill="x", pady=(0, 10))

        opt_top = tk.Frame(opt_card, bg=CARD)
        opt_top.pack(fill="x", padx=20, pady=12)

        tk.Label(opt_top, text="⚙️  Opções de Importação", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")

        opts = tk.Frame(opt_card, bg=CARD)
        opts.pack(fill="x", padx=20, pady=(0, 12))

        self.opt_criar_alunos = tk.BooleanVar(value=True)
        tk.Checkbutton(opts, text="Criar alunos novos automaticamente",
                       variable=self.opt_criar_alunos,
                       bg=CARD, font=FONT_BODY).pack(side="left", padx=(0, 20))

        self.opt_criar_materias = tk.BooleanVar(value=True)
        tk.Checkbutton(opts, text="Criar matérias novas automaticamente",
                       variable=self.opt_criar_materias,
                       bg=CARD, font=FONT_BODY).pack(side="left", padx=(0, 20))

        self.opt_sobrescrever = tk.BooleanVar(value=False)
        tk.Checkbutton(opts, text="Sobrescrever notas existentes (ao invés de mesclar)",
                       variable=self.opt_sobrescrever,
                       bg=CARD, font=FONT_BODY).pack(side="left")

        # ── Import button + progress
        action = tk.Frame(outer, bg=BG)
        action.pack(fill="x", pady=5)

        self.btn(action, "📥  Importar Dados", self._importar,
                 color=SUCCESS).pack(side="left", padx=5, ipadx=15)

        self.progress = ttk.Progressbar(action, mode="indeterminate", length=200)
        self.progress.pack(side="left", padx=15)

        # ── Log area
        log_card = self.card(outer)
        log_card.pack(fill="both", expand=True, pady=(5, 0))

        log_top = tk.Frame(log_card, bg=CARD)
        log_top.pack(fill="x", padx=20, pady=8)
        tk.Label(log_top, text="📋  Log de Importação", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(side="left")
        self.btn(log_top, "🗑 Limpar", self._clear_log, color="#78909C").pack(side="right")

        self.log = tk.Text(log_card, height=8, font=("Consolas", 9),
                           bg="#1E1E2E", fg="#CDD6F4", relief="flat",
                           state="disabled", wrap="word")
        log_sb = ttk.Scrollbar(log_card, orient="vertical", command=self.log.yview)
        self.log.configure(yscrollcommand=log_sb.set)
        log_sb.pack(side="right", fill="y", padx=(0, 5), pady=5)
        self.log.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # Color tags for log
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
            self.file_var.set(f"📄  {Path(path).name}  ({Path(path).stat().st_size // 1024 + 1} KB)")
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

            # Clear treeview
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

            self._log(f"[Pré-visualização] {len(df)} linhas mostradas de '{Path(self._filepath).name}'", "info")
            self._log(f"  Colunas detectadas: {', '.join(cols)}", "info")

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
                                   f"✅ {total} importados\n⚠️ {len(erros)} erro(s)\n"
                                   f"ℹ️ {len(avisos)} aviso(s)\n\nVeja o log para detalhes.")
        else:
            messagebox.showinfo("Importação concluída",
                                f"✅ {total} registros importados!\n"
                                f"ℹ️ {len(avisos)} aviso(s)")

    def _on_error(self, msg):
        self.progress.stop()
        self._log(f"[ERRO CRÍTICO] {msg}", "err")
        messagebox.showerror("Erro de importação", msg)

    def _show_help(self):
        win = tk.Toplevel(self)
        win.title("Formatos de importação suportados")
        win.geometry("600x420")
        win.configure(bg=CARD)
        tk.Label(win, text="📋  Formatos de Importação", font=FONT_HEAD,
                 bg=CARD, fg=TEXT).pack(pady=15)
        txt = tk.Text(win, font=("Consolas", 9), bg="#1E1E2E", fg="#CDD6F4",
                      relief="flat", padx=10, pady=10, wrap="word")
        txt.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        txt.insert("end", """FORMATO A — Padrão do sistema (com Turma)
─────────────────────────────────────────
Aluno        | Turma          | Disciplina  | N1  | N2  | N3  | N4
Ana Lima     | 6º Fundamental | Matemática  | 7.5 | 8.0 | 6.5 | 9.0
Bruno Silva  | 7º Fundamental | Português   | 5.0 | 6.5 | 7.0 | 8.5

FORMATO B — Simples (sem Turma)
─────────────────────────────────────────
Aluno        | Disciplina  | N1  | N2  | N3  | N4
Ana Lima     | Matemática  | 7.5 | 8.0 | 6.5 | 9.0
Bruno Silva  | Português   | 5.0 | 6.5 | 7.0 | 8.5

FORMATO C — Igual ao arquivo de exemplo (P1/P2/P3/P4)
─────────────────────────────────────────
Aluno         | Disciplina  | P1  | P2  | P3  | P4
Ana Lima      | Geografia   | 5.5 | 2.8 | 4.7 | 6.0

REGRAS GERAIS
─────────────────────────────────────────
• Cabeçalhos podem estar em qualquer ordem
• Nomes das colunas são flexíveis (N1/P1/Nota1, Aluno/Nome, etc.)
• Alunos e matérias inexistentes são criados automaticamente
• Notas são mescladas (valores existentes mantidos se a célula estiver vazia)
• Notas devem estar entre 0 e 10 (vírgula ou ponto como decimal)
• Linhas completamente vazias são ignoradas
""")
        txt.configure(state="disabled")


# ── Exportar ──────────────────────────────────────────────────────────────────

class ExportarPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Exportar Excel", "📥")
        self._build()

    def _build(self):
        c = self.card(self)
        c.pack(padx=80, pady=40, fill="x")
        tk.Label(c, text="Exportar Planilha de Notas",
                 font=FONT_HEAD, bg=CARD, fg=TEXT).pack(pady=(20, 5))
        tk.Label(c, text="Gera um arquivo .xlsx com todas as notas, médias e status dos alunos.",
                 font=FONT_BODY, bg=CARD, fg=MUTED).pack()

        tk.Label(c, text="Turma:", font=FONT_BODY, bg=CARD).pack(pady=(15, 2))
        self.sala_var = tk.StringVar()
        self.sala_cb = ttk.Combobox(c, textvariable=self.sala_var,
                                    state="readonly", width=25, font=FONT_BODY)
        self.sala_cb.pack()

        self.btn(c, "📥  Exportar Excel", self._exportar,
                 color=SUCCESS).pack(pady=15, ipadx=20)

        self.status_var = tk.StringVar()
        tk.Label(c, textvariable=self.status_var, font=FONT_BODY,
                 bg=CARD, fg=ACCENT).pack(pady=(0, 20))

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
            self.status_var.set(f"✅ Exportado: {Path(path).name} — {msg}")
        else:
            self.status_var.set(f"⚠️ {msg}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Apply a clean ttk theme
    root_check = tk.Tk()
    root_check.withdraw()
    style = ttk.Style(root_check)
    available = style.theme_names()
    root_check.destroy()

    app = App()
    style = ttk.Style(app)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    style.configure("Treeview", font=("Segoe UI", 9), rowheight=26, background="white")
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                    background=HEADER_BG, foreground=TEXT)
    style.map("Treeview", background=[("selected", ACCENT2)])
    style.configure("TCombobox", font=FONT_BODY)
    app.mainloop()

if __name__ == "__main__":
    main()