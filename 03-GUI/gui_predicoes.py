#!/usr/bin/env python3
"""
Página de Predições - Integração ML com GUI Escolar
Análise de desempenho e alerta de déficits por aluno
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from gui_ml_integration import MLModelLoader, DisciplinePerformanceAnalyzer, DisciplineCard, StatusBadge
import numpy as np

# Constantes de cores (mesmas da GUI principal)
BG        = "#F0F4FF"
ACCENT    = "#3949AB"
ACCENT2   = "#5C6BC0"
SUCCESS   = "#2E7D32"
WARN      = "#E65100"
DANGER    = "#C62828"
CARD      = "#FFFFFF"
TEXT      = "#1A1A2E"
MUTED     = "#8892B0"
HEADER_BG = "#E8EAF6"
ROW_ALT   = "#F5F7FF"

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_HEAD   = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_BTN    = ("Segoe UI", 10, "bold")
FONT_BIG    = ("Segoe UI", 28, "bold")

# ──────────────────────────────────────────────────────────────────────────────
# BASE PAGE (Reuse from main GUI)
# ──────────────────────────────────────────────────────────────────────────────

class BasePage(tk.Frame):
    """Classe base para páginas da aplicação."""
    def __init__(self, parent, app, title="", icon=""):
        super().__init__(parent, bg=BG)
        self.app = app
        if title:
            hdr = tk.Frame(self, bg=BG)
            hdr.pack(fill="x", padx=30, pady=(20, 5))
            tk.Label(hdr, text=f"{icon}  {title}", font=FONT_TITLE,
                     bg=BG, fg=TEXT).pack(side="left")

    def card(self, parent, **kwargs):
        # Remove conflitos de parâmetros que vêm nos kwargs
        kwargs.pop('relief', None)
        kwargs.pop('bd', None)
        f = tk.Frame(parent, bg=CARD, relief="flat", bd=0, **kwargs)
        f.configure(highlightbackground="#D0D8F0", highlightthickness=1)
        return f

    def btn(self, parent, text, cmd, color=ACCENT, fg="white", **kwargs):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color, fg=fg, font=FONT_BTN,
                      relief="flat", cursor="hand2", padx=12, pady=6,
                      activebackground=ACCENT2, activeforeground="white", **kwargs)
        return b

# ──────────────────────────────────────────────────────────────────────────────
# PÁGINA DE PREDIÇÕES
# ──────────────────────────────────────────────────────────────────────────────

class PredictionPage(BasePage):
    """
    Integra o ML com a GUI escolar.
    Permite selecionar um aluno e ver predições de desempenho por disciplina.
    """
    
    def __init__(self, parent, app):
        super().__init__(parent, app, "Predições de Desempenho do Aluno", "🎯")
        self.ml_loader = MLModelLoader()
        self.aluno_var = tk.StringVar()
        self.aluno_data = {}
        self.aluno_cb = None
        self.sala_var = tk.StringVar()
        self.sala_cb = None
        self.sala_map = {}
        self.result_frame = None
        self._build_ui()
    
    def _build_ui(self):
        """Constrói a interface."""
        
        # Descrição
        desc = tk.Frame(self, bg=BG)
        desc.pack(fill="x", padx=30, pady=(0, 10))
        tk.Label(
            desc,
            text="Identifique déficits logo no começo do ano — análise por disciplina",
            font=FONT_SMALL,
            bg=BG,
            fg=MUTED
        ).pack(anchor="w")
        
        # Controles
        self._build_controls()
        
        # Área de resultado
        self.result_frame = tk.Frame(self, bg=BG)
        self.result_frame.pack(fill="both", expand=True, padx=30, pady=(10, 30))
    
    def _build_controls(self):
        """Constrói painel de controles e filtros."""
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=30, pady=(10, 5))
        
        # Linha 1: Seleção de turma e aluno
        row1 = tk.Frame(ctrl, bg=BG)
        row1.pack(fill="x", pady=(0, 8))
        
        tk.Label(row1, text="Turma:", font=FONT_BODY, bg=BG).pack(side="left", padx=(0, 5))
        self.sala_var = tk.StringVar()
        self.sala_cb = ttk.Combobox(
            row1,
            textvariable=self.sala_var,
            state="readonly",
            width=20,
            font=FONT_BODY
        )
        self.sala_cb.pack(side="left", padx=(0, 15))
        self.sala_cb.bind("<<ComboboxSelected>>", lambda e: self._load_students())
        
        tk.Label(row1, text="Aluno:", font=FONT_BODY, bg=BG).pack(side="left", padx=(0, 5))
        self.aluno_var = tk.StringVar()
        self.aluno_cb = ttk.Combobox(
            row1,
            textvariable=self.aluno_var,
            state="readonly",
            width=30,
            font=FONT_BODY
        )
        self.aluno_cb.pack(side="left", padx=(0, 15), expand=True, fill="x")
        
        btn_analisar = self.btn(
            row1,
            "🔍 Analisar",
            self._load_student_analysis
        )
        btn_analisar.pack(side="left", padx=5)
    
    def refresh(self):
        """Atualiza lista de turmas."""
        import cads
        salas = cads.get_salas()
        self.sala_map = {s['nome']: s['id'] for s in salas}
        self.sala_cb['values'] = list(self.sala_map.keys())
        if not self.sala_var.get() and self.sala_map:
            self.sala_var.set(list(self.sala_map.keys())[0])
            self._load_students()
    
    def _load_students(self):
        """Carrega alunos da turma selecionada."""
        import cads
        sala_id = self.sala_map.get(self.sala_var.get())
        if not sala_id:
            return
        
        alunos = cads.get_alunos(sala_id)
        aluno_list = [f"{a['nome']} ({a['matricula']})" for a in alunos]
        self.aluno_cb['values'] = aluno_list
        self.aluno_data = {f"{a['nome']} ({a['matricula']})": a['id'] for a in alunos}
    
    def _load_student_analysis(self):
        """Carrega análise do aluno selecionado."""
        if not self.aluno_var.get():
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        
        aluno_id = self.aluno_data.get(self.aluno_var.get())
        if not aluno_id:
            return
        
        # Analisar
        analise = DisciplinePerformanceAnalyzer.analyze_student(
            "escola.db",
            aluno_id,
            self.ml_loader
        )
        
        if not analise:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return
        
        # Limpar resultado anterior
        for w in self.result_frame.winfo_children():
            w.destroy()
        
        # Exibir resultados
        self._display_analysis(analise)
    
    def _display_analysis(self, analise):
        """Exibe análise visual do aluno."""
        
        # Card de resumo do aluno
        aluno_card = self.card(self.result_frame, relief="solid", bd=1)
        aluno_card.pack(fill="x", pady=(0, 15))
        
        header = tk.Frame(aluno_card, bg=HEADER_BG)
        header.pack(fill="x")
        
        info_text = f"{analise['aluno']['nome']} • Matrícula: {analise['aluno']['matricula']} • {analise['aluno']['sala']}"
        tk.Label(
            header,
            text=info_text,
            font=FONT_HEAD,
            bg=HEADER_BG,
            fg=TEXT,
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(10, 8))
        
        # Perfil e recomendações
        body = tk.Frame(aluno_card, bg=CARD)
        body.pack(fill="x", padx=15, pady=(8, 15))
        
        # Status geral
        tk.Label(
            body,
            text="Status Geral:",
            font=FONT_BODY,
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 4))
        
        tk.Label(
            body,
            text=analise['profile'],
            font=("Segoe UI", 13, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w", pady=(0, 12))
        
        # Estatísticas
        stats_frame = tk.Frame(body, bg=CARD)
        stats_frame.pack(fill="x")
        
        for label, items, color in [
            ("✅ Bem nas disciplinas", analise['strengths'], SUCCESS),
            ("⚠️ Precisa de atenção", analise['at_risk'], WARN),
            ("❌ Com déficit", analise['weaknesses'], DANGER),
        ]:
            col = tk.Frame(stats_frame, bg=CARD)
            col.pack(side="left", fill="both", expand=True, padx=(0, 15))
            
            tk.Label(col, text=label, font=("Segoe UI", 9, "bold"), bg=CARD, fg=color).pack(anchor="w")
            
            if items:
                txt = ", ".join(items)
                tk.Label(col, text=txt, font=FONT_SMALL, bg=CARD, fg=TEXT, wraplength=200, justify="left").pack(anchor="w")
            else:
                tk.Label(col, text="—", font=FONT_SMALL, bg=CARD, fg=MUTED).pack(anchor="w")
        
        # Cards de disciplinas
        disc_label = tk.Label(
            self.result_frame,
            text="Análise por Disciplina",
            font=FONT_HEAD,
            bg=BG,
            fg=TEXT
        )
        disc_label.pack(anchor="w", pady=(15, 8))
        
        # Scroll frame para disciplinas
        scroll_frame = tk.Frame(self.result_frame, bg=BG)
        scroll_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(scroll_frame, bg=BG, relief="flat", bd=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Adicionar cards de disciplinas
        for disc in analise['disciplinas']:
            card = DisciplineCard(scrollable_frame, disc)
            card.pack(fill="x", pady=6)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Rodapé com info dos modelos
        footer = self.card(self.result_frame)
        footer.pack(fill="x", pady=(15, 0), side="bottom")
        
        model_info = f"Modelo de predição: M3 (9 features, 84.6% acurácia)"
        tk.Label(
            footer,
            text=f"ℹ️  {model_info}",
            font=FONT_SMALL,
            bg=HEADER_BG,
            fg=MUTED
        ).pack(anchor="w", padx=12, pady=6)


# ──────────────────────────────────────────────────────────────────────────────
# PÁGINA DE GERENCIAMENTO DE SALAS
# ──────────────────────────────────────────────────────────────────────────────

class SalasPage(BasePage):
    """Gerencia criação e edição de salas (turmas)."""
    
    def __init__(self, parent, app):
        super().__init__(parent, app, "Gerenciar Salas/Turmas", "🏫")
        self._build_ui()
    
    def _build_ui(self):
        """Constrói a interface."""
        
        # Controles
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=30, pady=5)
        
        tk.Label(ctrl, text="Nome da Sala:", font=FONT_BODY, bg=BG).pack(side="left", padx=(0, 5))
        self.nome_var = tk.StringVar()
        tk.Entry(ctrl, textvariable=self.nome_var, font=FONT_BODY, width=20).pack(side="left", padx=(0, 10))
        
        tk.Label(ctrl, text="Código (ex: 6a):", font=FONT_BODY, bg=BG).pack(side="left", padx=(0, 5))
        self.codigo_var = tk.StringVar()
        tk.Entry(ctrl, textvariable=self.codigo_var, font=FONT_BODY, width=12).pack(side="left", padx=(0, 15))
        
        btn_criar = self.btn(ctrl, "➕ Criar Sala", self._criar_sala, color=SUCCESS)
        btn_criar.pack(side="left", padx=5)
        
        btn_remover = self.btn(ctrl, "🗑 Remover", self._remover_sala, color="#C62828")
        btn_remover.pack(side="left", padx=5)
        
        # Tabela de salas
        card = self.card(self)
        card.pack(fill="both", expand=True, padx=30, pady=(10, 30))
        
        cols = ("Sala", "Código", "Alunos")
        self.tv = ttk.Treeview(card, columns=cols, show="headings", height=12)
        
        for col in cols:
            self.tv.heading(col, text=col)
        
        self.tv.column("Sala", width=250, anchor="w")
        self.tv.column("Código", width=100, anchor="center")
        self.tv.column("Alunos", width=100, anchor="center")
        
        sb = ttk.Scrollbar(card, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        
        sb.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True, padx=5, pady=5)
        self.tv.tag_configure("alt", background=ROW_ALT)
    
    def refresh(self):
        """Atualiza lista de salas."""
        import cads
        
        self.tv.delete(*self.tv.get_children())
        salas = cads.get_salas()
        
        conn = sqlite3.connect("escola.db")
        
        for i, sala in enumerate(salas):
            cnt = conn.execute(
                "SELECT COUNT(*) FROM alunos WHERE sala_id = ?",
                (sala['id'],)
            ).fetchone()[0]
            
            tag = "alt" if i % 2 else ""
            self.tv.insert("", "end", iid=str(sala['id']),
                          values=(sala['nome'], sala['codigo'], cnt),
                          tags=(tag,))
        
        conn.close()
    
    def _criar_sala(self):
        """Cria uma nova sala."""
        import cads
        
        nome = self.nome_var.get().strip()
        codigo = self.codigo_var.get().strip().upper()
        
        if not nome or not codigo:
            messagebox.showwarning("Atenção", "Preencha nome e código.")
            return
        
        try:
            cads.adicionar_sala(nome, codigo)
            messagebox.showinfo("Sucesso", f"Sala '{nome}' ({codigo}) criada!")
            self.nome_var.set("")
            self.codigo_var.set("")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar sala: {e}")
    
    def _remover_sala(self):
        """Remove sala selecionada."""
        import cads
        
        sel = self.tv.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma sala.")
            return
        
        if messagebox.askyesno("Confirmação", "Remover esta sala?"):
            sala_id = int(sel[0])
            try:
                cads.remover_sala(sala_id)
                messagebox.showinfo("Sucesso", "Sala removida!")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover: {e}")
