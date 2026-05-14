#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Página de Predições com Layout Melhorado
- Cards lado a lado
- Previsão de N4
- Filtros de status
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sys

# Adicionar pastas ao path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "01-CORE"))
sys.path.insert(0, str(project_root / "02-ML"))
sys.path.insert(0, str(project_root / "03-GUI"))

from gui_ml_integration import DisciplinePerformanceAnalyzer, MLModelLoader

# Constantes de cores
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

# Importar BasePage
from gui_predicoes import BasePage

class PredictionPageImproved(BasePage):
    """
    Versão melhorada com:
    - Cards lado a lado
    - Previsão de N4
    - Filtros de status
    """
    
    def __init__(self, parent, app):
        super().__init__(parent, app, "Predições de Desempenho", "🎯")
        self.ml_loader = MLModelLoader()
        self.aluno_var = tk.StringVar()
        self.aluno_data = {}
        self.aluno_cb = None
        self.sala_var = tk.StringVar()
        self.sala_cb = None
        self.sala_map = {}
        self.result_frame = None
        self.filter_var = tk.StringVar(value="all")
        self.analise_atual = None
        self._build_ui()
    
    def _build_ui(self):
        """Constroi a interface."""
        
        # Descricao
        desc = tk.Frame(self, bg=BG)
        desc.pack(fill="x", padx=30, pady=(0, 10))
        tk.Label(
            desc,
            text="Identifique déficits logo no início do ano — análise por disciplina com previsões do modelo IA",
            font=FONT_SMALL,
            bg=BG,
            fg=MUTED
        ).pack(anchor="w")
        
        # Controles
        self._build_controls()
        
        # Area de resultado
        self.result_frame = tk.Frame(self, bg=BG)
        self.result_frame.pack(fill="both", expand=True, padx=30, pady=(10, 30))
    
    def _build_controls(self):
        """Constroi painel de controles e filtros."""
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=30, pady=(10, 5))
        
        # Linha 1: Selecao de turma e aluno
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
            "Analisar",
            self._load_student_analysis
        )
        btn_analisar.pack(side="left", padx=5)
        
        # Linha 2: Filtros
        row2 = tk.Frame(ctrl, bg=BG)
        row2.pack(fill="x", pady=(0, 8))
        
        tk.Label(row2, text="Filtro:", font=FONT_BODY, bg=BG).pack(side="left", padx=(0, 5))
        
        filtros = [
            ("Todas", "all"),
            ("Aprovadas", "aprovado"),
            ("Recuperação", "recuperacao"),
            ("Reprovadas", "reprovado"),
            ("Vai Melhorar", "melhorar"),
            ("Vai Piorar", "piorar"),
        ]
        
        for label, value in filtros:
            tk.Radiobutton(
                row2,
                text=label,
                variable=self.filter_var,
                value=value,
                font=FONT_SMALL,
                bg=BG,
                command=self._apply_filters
            ).pack(side="left", padx=5)
    
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

        # Aviso amigável se nenhum modelo foi treinado
        if not self.ml_loader.is_available("RF_M3") and \
           not self.ml_loader.is_available("RF_M2") and \
           not self.ml_loader.is_available("RF_M1"):
            resp = messagebox.askyesno(
                "Modelos não treinados",
                "Nenhum modelo de IA foi treinado ainda.\n\n"
                "A análise será feita apenas com as notas atuais, sem previsões.\n\n"
                "Deseja continuar mesmo assim?\n"
                "(Para treinar, acesse 🤖 Machine Learning)"
            )
            if not resp:
                return

        try:
            analise = DisciplinePerformanceAnalyzer.analyze_student(
                None,
                aluno_id,
                self.ml_loader
            )
        except Exception as e:
            messagebox.showerror("Erro na análise", f"Não foi possível analisar o aluno:\n{e}")
            return

        if not analise:
            messagebox.showerror("Erro", "Aluno não encontrado ou sem notas lançadas.")
            return

        self.analise_atual = analise
        self._display_analysis(analise)
    
    def _apply_filters(self):
        """Aplica filtros aos cards visíveis."""
        if not self.analise_atual:
            return
        
        self._display_analysis(self.analise_atual)
    
    def _display_analysis(self, analise):
        """Exibe analise visual do aluno com layout melhorado."""
        
        # Limpar resultado anterior
        for w in self.result_frame.winfo_children():
            w.destroy()
        
        # Card de resumo do aluno
        aluno_card = self.card(self.result_frame, relief="solid", bd=1)
        aluno_card.pack(fill="x", pady=(0, 15))
        
        header = tk.Frame(aluno_card, bg=HEADER_BG)
        header.pack(fill="x")
        
        info_text = f"{analise['aluno']['nome']}  ·  Matrícula: {analise['aluno']['matricula']}  ·  {analise['aluno']['sala']}"
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

        tk.Label(
            body,
            text="Perfil:",
            font=FONT_BODY,
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 4))

        # Cor baseada nos valores reais retornados pelo analisador
        profile = analise['profile']
        if "CRÍTICO" in profile:
            profile_color = DANGER
        elif "EM RISCO" in profile:
            profile_color = WARN
        else:
            profile_color = SUCCESS

        tk.Label(
            body,
            text=profile,
            font=("Segoe UI", 13, "bold"),
            bg=CARD,
            fg=profile_color
        ).pack(anchor="w", pady=(0, 12))
        
        # Recomendacoes por prioridade
        self._display_recommendations(body, analise)
        
        # Titulo das disciplinas
        disc_label = tk.Label(
            self.result_frame,
            text="Análise por Disciplina",
            font=FONT_HEAD,
            bg=BG,
            fg=TEXT
        )
        disc_label.pack(anchor="w", pady=(15, 8))
        
        # Container para cards em grid com scroll
        scroll_frame = tk.Frame(self.result_frame, bg=BG)
        scroll_frame.pack(fill="both", expand=True)
        
        # Canvas com Scrollbar
        canvas = tk.Canvas(scroll_frame, bg=BG, relief="flat", bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        cards_container = tk.Frame(canvas, bg=BG)
        
        # Atualizar scrollregion quando o tamanho da frame mudar
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        cards_container.bind("<Configure>", on_frame_configure)
        canvas.create_window((0, 0), window=cards_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Suporte para scroll com mouse wheel (apenas no canvas)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Vincular scroll apenas ao canvas, não a todos os widgets
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down
        
        # Empacotar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Aplicar filtro
        filter_type = self.filter_var.get()
        disciplinas_filtradas = self._filter_disciplines(analise['disciplinas'], filter_type)
        
        if not disciplinas_filtradas:
            tk.Label(
                cards_container,
                text="Nenhuma disciplina corresponde ao filtro selecionado.",
                font=FONT_SMALL,
                bg=BG,
                fg=MUTED
            ).pack(pady=20)
        else:
            # Grid de cards (3 colunas)
            for idx, disc in enumerate(disciplinas_filtradas):
                row = idx // 3
                col = idx % 3
                
                card = DisciplineCardImproved(cards_container, disc)
                card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Configurar peso das colunas
            for i in range(3):
                cards_container.grid_columnconfigure(i, weight=1)
    
    def _filter_disciplines(self, disciplinas, filter_type):
        """Filtra disciplinas conforme o tipo selecionado."""
        if filter_type == "all":
            return disciplinas
        elif filter_type == "aprovado":
            return [d for d in disciplinas if d['status'] == 2]
        elif filter_type == "recuperacao":
            return [d for d in disciplinas if d['status'] == 1]
        elif filter_type == "reprovado":
            return [d for d in disciplinas if d['status'] == 0]
        elif filter_type == "melhorar":
            return [d for d in disciplinas if d.get('prognosis') == 'will_improve']
        elif filter_type == "piorar":
            return [d for d in disciplinas if d.get('prognosis') == 'will_decline']
        return disciplinas
    
    def _display_recommendations(self, body, analise):
        """Exibe recomendacoes de foco baseadas no pior caso."""
        
        # Ordenar por prioridade: reprovados primeiro, depois recuperacao, depois problemas
        prioridade = []
        
        # Disciplinas reprovadas
        for disc in analise['disciplinas']:
            if disc['status'] == 0:
                prioridade.append((disc['nome'], "SUSPENSÃO", disc, 3))

        # Disciplinas em queda
        for disc in analise['disciplinas']:
            if disc.get('prognosis') == 'will_decline':
                prioridade.append((disc['nome'], "PREVENÇÃO", disc, 2))

        # Vai melhorar (informativo)
        melhora = [d['nome'] for d in analise['disciplinas'] if d.get('prognosis') == 'will_improve']

        if prioridade:
            tk.Label(
                body,
                text="RECOMENDAÇÕES (Prioridade de Foco):",
                font=("Segoe UI", 10, "bold"),
                bg=CARD,
                fg=DANGER
            ).pack(anchor="w", pady=(8, 6))

            for nome, tipo, disc, _ in sorted(prioridade, key=lambda x: x[3], reverse=True):
                tk.Label(
                    body,
                    text=f"  • {nome}: reforço imediato [{tipo}]",
                    font=FONT_SMALL,
                    bg=CARD,
                    fg=DANGER
                ).pack(anchor="w")

        if melhora:
            tk.Label(
                body,
                text=f"Manutenção positiva: {', '.join(melhora)}",
                font=FONT_SMALL,
                bg=CARD,
                fg=SUCCESS
            ).pack(anchor="w", pady=(6, 0))


class DisciplineCardImproved(tk.Frame):
    """Card aprimorado com previsao de N4 e layout horizontal otimizado."""
    
    def __init__(self, parent, disc_info, **kwargs):
        super().__init__(parent, bg="white", relief="solid", bd=1, **kwargs)
        
        # Header
        head = tk.Frame(self, bg="#F5F5F5")
        head.pack(fill="x")
        
        tk.Label(
            head,
            text=disc_info["nome"],
            font=("Segoe UI", 10, "bold"),
            bg="#F5F5F5",
            fg="#1A1A2E"
        ).pack(anchor="w", padx=10, pady=6, side="left", expand=True)
        
        # Status badge
        status_colors = {0: "#C62828", 1: "#E65100", 2: "#2E7D32"}
        status_names = {0: "Reprovado", 1: "Recuperação", 2: "Aprovado"}
        
        status_color = status_colors.get(disc_info["status"], "#666")
        status_name = status_names.get(disc_info["status"], "Desconhecido")
        
        tk.Label(
            head,
            text=status_name,
            font=("Segoe UI", 8, "bold"),
            bg=status_color,
            fg="white",
            padx=6,
            pady=2
        ).pack(side="right", padx=8, pady=4)
        
        # Body
        body = tk.Frame(self, bg="white")
        body.pack(fill="both", expand=True, padx=10, pady=8)
        
        # Notas em grid compacto
        notas_frame = tk.Frame(body, bg="white")
        notas_frame.pack(fill="x", pady=(0, 6))
        
        for i, (label, value) in enumerate([
            ("N1", disc_info["n1"]),
            ("N2", disc_info["n2"]),
            ("N3", disc_info["n3"]),
            ("N4", disc_info["n4"]),
        ]):
            col = tk.Frame(notas_frame, bg="white")
            col.pack(side="left", fill="x", expand=True, padx=2)
            
            if value is None or value == 0:
                tk.Label(col, text=label, font=("Segoe UI", 7), fg="#999").pack()
                tk.Label(col, text="—", font=("Segoe UI", 9, "bold"), fg="#CCC").pack()
            else:
                tk.Label(col, text=label, font=("Segoe UI", 7), fg="#666").pack()
                tk.Label(
                    col,
                    text=f"{value:.1f}",
                    font=("Segoe UI", 10, "bold"),
                    fg="#1A1A2E"
                ).pack()
        
        # Previsao de N4 se nao estiver preenchida
        if (disc_info.get("n4") is None or disc_info.get("n4") == 0) and disc_info.get("n1") and disc_info.get("n2"):
            prev_frame = tk.Frame(body, bg="#E3F2FD", relief="flat")
            prev_frame.pack(fill="x", pady=(6, 0), ipadx=8, ipady=4)
            
            tk.Label(
                prev_frame,
                text="Previsão N4:",
                font=("Segoe UI", 8),
                bg="#E3F2FD",
                fg="#1565C0"
            ).pack(anchor="w")

            # Calcula previsão baseada em slope (tendência)
            media_prevista = self._prever_n4(disc_info)
            
            tk.Label(
                prev_frame,
                text=f"~{media_prevista:.1f}",
                font=("Segoe UI", 11, "bold"),
                bg="#E3F2FD",
                fg="#0D47A1"
            ).pack(anchor="w")
        
        # Media ponderada
        media_frame = tk.Frame(body, bg="#E8EAF6", relief="flat")
        media_frame.pack(fill="x", pady=(6, 0), ipadx=10, ipady=4)
        
        tk.Label(
            media_frame,
            text="Media:",
            font=("Segoe UI", 8),
            bg="#E8EAF6",
            fg="#5C6BC0"
        ).pack(anchor="w")
        
        tk.Label(
            media_frame,
            text=f"{disc_info['media']:.2f}",
            font=("Segoe UI", 12, "bold"),
            bg="#E8EAF6",
            fg="#3949AB"
        ).pack(anchor="w")
        
        # Prognosis
        if disc_info.get("prognosis"):
            prognosis_colors = {
                "will_improve":         ("#C8E6C9", "#2E7D32", "↗ Vai Melhorar"),
                "will_decline":         ("#FFCCBC", "#C62828", "↘ Vai Piorar"),
                "stable":               ("#FFF9C4", "#F57F17", "→ Estável"),
                "better_than_expected": ("#C8E6C9", "#2E7D32", "↑ Superou Previsão"),
                "worse_than_expected":  ("#FFCCBC", "#C62828", "↓ Abaixo do Previsto"),
                "as_expected":          ("#FFF9C4", "#F57F17", "= Como Previsto"),
            }
            
            bg_color, fg_color, text = prognosis_colors.get(
                disc_info.get("prognosis"),
                ("#F5F5F5", "#666", "?")
            )
            
            prog_frame = tk.Frame(body, bg=bg_color, relief="flat")
            prog_frame.pack(fill="x", pady=(6, 0), ipadx=8, ipady=4)
            
            tk.Label(
                prog_frame,
                text=text,
                font=("Segoe UI", 8, "bold"),
                bg=bg_color,
                fg=fg_color
            ).pack(anchor="w")
    
    @staticmethod
    def _prever_n4(disc_info):
        """Preve N4 usando slope (tendencia) como base, nao media simples.
        Requisitos minimos: N1 e N2 para calcular slope.
        """
        n1 = disc_info.get("n1")
        n2 = disc_info.get("n2")
        n3 = disc_info.get("n3")
        
        # Requisito: minimo N1 e N2 para calcular slope
        if not n1 or not n2:
            return 5.0
        
        # Calcular slope percentual
        slope_pct = ((n2 - n1) / n1) * 100 if n1 > 0 else 0
        
        # Estrategia de previsao baseada em slope
        if slope_pct > 20:
            # Melhora significativa (> 20%): prever nota mais alta
            # Prever entre N2 e 10, tendendo mais para cima
            gap = 10 - n2
            return n2 + (gap * 0.65)
        elif slope_pct < -20:
            # Piora significativa (< -20%): prever nota mais baixa
            # Prever entre N2 e N2*0.7 (reduzindo conforme piora)
            reduction = n2 * 0.3
            return max(0, n2 - reduction)
        else:
            # Estavel (entre -20% e +20%): prever mantencao (usa N3 se disponivel)
            if n3:
                # Media entre N2 e N3 (ponderada)
                return (n2 * 0.6 + n3 * 0.4)
            else:
                # Sem N3, apenas contem N2 (com pequena margem de variacao)
                return n2
