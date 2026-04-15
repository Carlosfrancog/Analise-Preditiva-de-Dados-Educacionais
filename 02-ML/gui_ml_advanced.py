#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dashboard Avançado de Machine Learning - Treino, Análise e Visualizações
Modernizado com interface limpa e funcionalidades completas
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from pathlib import Path
import pickle
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
import subprocess
import sys

# Adicionar pastas ao path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "01-CORE"))
sys.path.insert(0, str(project_root / "02-ML"))
sys.path.insert(0, str(project_root / "03-GUI"))

import cads
from gui_predicoes_improved import BasePage

# ──────────────────────────────────────────────────────────────────────────────
# CORES E ESTILOS MODERNOS
# ──────────────────────────────────────────────────────────────────────────────

DARK_BG = "#0F1419"
CARD_BG = "#1E2329"
ACCENT = "#5B9FDB"
SUCCESS = "#4CBD71"
WARN = "#FFB946"
ERROR = "#F76A6A"
TEXT = "#FFFFFF"
MUTED = "#8D99AC"

COLORS = {
    0: {"name": "Reprovado", "hex": "#F76A6A", "light": "#FFE1E1"},
    1: {"name": "Recuperação", "hex": "#FFB946", "light": "#FFF8E1"},
    2: {"name": "Aprovado", "hex": "#4CBD71", "light": "#E1F5E1"},
}

# ──────────────────────────────────────────────────────────────────────────────
# PÁGINA ML AVANÇADA
# ──────────────────────────────────────────────────────────────────────────────

class MLAdvancedPage(BasePage):
    """Dashboard de ML com treino, visualização e análise de decisões."""

    def __init__(self, parent, app):
        super().__init__(parent, app, "Machine Learning Avançado", "🤖")
        self.model_loader = None
        self.last_training = None
        self._build()
        # Carregar pesos salvos após construir interface
        self.after(100, self._load_weights_config)

    def _build(self):
        """Constrói toda a interface modernizada."""
        
        # ────────────────────────────────────────────────────────
        # SEÇÃO 1: Resumo de Modelos
        # ────────────────────────────────────────────────────────
        
        summary_frame = tk.Frame(self, bg=DARK_BG)
        summary_frame.pack(fill="x", padx=20, pady=(15, 0))
        
        tk.Label(
            summary_frame, text="📊 MODELOS TREINADOS",
            font=("Segoe UI", 14, "bold"),
            bg=DARK_BG, fg=TEXT
        ).pack(anchor="w", pady=(0, 10))
        
        # Cards dos modelos
        models_container = tk.Frame(summary_frame, bg=DARK_BG)
        models_container.pack(fill="x")
        
        self.model_cards = {}  # model_name → frames dict
        
        for model_name, config in [
            ("RF_M1", "100 árvores, profund. 5"),
            ("RF_M2", "150 árvores, profund. 10"),
            ("RF_M3", "200 árvores (PRODUÇÃO)"),
        ]:
            self._create_model_card(models_container, model_name, config)
        
        # ────────────────────────────────────────────────────────
        # SEÇÃO 2: Controles de Treino
        # ────────────────────────────────────────────────────────
        
        train_frame = tk.Frame(self, bg=DARK_BG)
        train_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(
            train_frame, text="⚙️  TREINAR MODELOS",
            font=("Segoe UI", 14, "bold"),
            bg=DARK_BG, fg=TEXT
        ).pack(anchor="w", pady=(0, 10))
        
        action_frame = tk.Frame(train_frame, bg=CARD_BG, relief="flat")
        action_frame.pack(fill="x", padx=15, pady=10, ipady=15)
        
        # Botões principais
        btn_frame = tk.Frame(action_frame, bg=CARD_BG)
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        tk.Button(
            btn_frame, text="🔄 Gerar Features",
            bg=ACCENT, fg=TEXT, font=("Segoe UI", 11, "bold"),
            relief="flat", cursor="hand2", padx=15, pady=8,
            command=self._generate_features
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame, text="🚀 Treinar Todos os Modelos",
            bg=SUCCESS, fg=TEXT, font=("Segoe UI", 11, "bold"),
            relief="flat", cursor="hand2", padx=15, pady=8,
            command=self._train_all_models
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame, text="📈 Treinar RF_M3 (Produção)",
            bg="#7986CB", fg=TEXT, font=("Segoe UI", 11, "bold"),
            relief="flat", cursor="hand2", padx=15, pady=8,
            command=self._train_m3_only
        ).pack(side="left", padx=5)
        
        # Status área
        self.status_var = tk.StringVar(value="Aguardando ação...")
        self.progress_var = tk.IntVar(value=0)
        
        status_frame = tk.Frame(action_frame, bg=CARD_BG)
        status_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(
            status_frame, textvariable=self.status_var,
            font=("Segoe UI", 10), bg=CARD_BG, fg=MUTED
        ).pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(
            status_frame, variable=self.progress_var,
            mode='determinate', length=400
        )
        self.progress_bar.pack(fill="x", pady=(8, 0), ipady=2)
        
        # ────────────────────────────────────────────────────────
        # SEÇÃO 3: Análise de Decisões
        # ────────────────────────────────────────────────────────
        
        analysis_frame = tk.Frame(self, bg=DARK_BG)
        analysis_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(
            analysis_frame, text="🔍 ANALISAR DECISÕES DO MODELO",
            font=("Segoe UI", 14, "bold"),
            bg=DARK_BG, fg=TEXT
        ).pack(anchor="w", pady=(0, 10))
        
        decision_frame = tk.Frame(analysis_frame, bg=CARD_BG, relief="flat")
        decision_frame.pack(fill="x", padx=15, pady=10, ipady=15)
        
        # Seleção de aluno e matéria
        selector_frame = tk.Frame(decision_frame, bg=CARD_BG)
        selector_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Coluna 1: Aluno
        tk.Label(selector_frame, text="Aluno:", font=("Segoe UI", 10, "bold"),
                bg=CARD_BG, fg=TEXT).pack(side="left", padx=(0, 5))
        
        self.aluno_var = tk.StringVar()
        self.aluno_cb = ttk.Combobox(selector_frame, textvariable=self.aluno_var,
                                      state="readonly", width=25, font=("Segoe UI", 10))
        self.aluno_cb.pack(side="left", padx=(0, 20))
        
        # Coluna 2: Matéria
        tk.Label(selector_frame, text="Matéria:", font=("Segoe UI", 10, "bold"),
                bg=CARD_BG, fg=TEXT).pack(side="left", padx=(0, 5))
        
        self.materia_var = tk.StringVar()
        self.materia_cb = ttk.Combobox(selector_frame, textvariable=self.materia_var,
                                        state="readonly", width=25, font=("Segoe UI", 10))
        self.materia_cb.pack(side="left", padx=(0, 20))
        
        # Botão analisar
        tk.Button(
            selector_frame, text="🔍 Analisar",
            bg=ACCENT, fg=TEXT, font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2", padx=12, pady=5,
            command=self._analyze_decision
        ).pack(side="left")
        
        # Área de resultado
        self.result_text = tk.Text(
            decision_frame, height=12, width=80,
            bg="#252D36", fg=TEXT, font=("Courier New", 9),
            relief="flat", borderwidth=0, padx=15, pady=15
        )
        self.result_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # ────────────────────────────────────────────────────────
        # SEÇÃO 4: Configuração de Pesos
        # ────────────────────────────────────────────────────────
        
        weights_frame = tk.Frame(self, bg=DARK_BG)
        weights_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(
            weights_frame, text="⚖️  CONFIGURAR PESOS DA MÉDIA PONDERADA",
            font=("Segoe UI", 14, "bold"),
            bg=DARK_BG, fg=TEXT
        ).pack(anchor="w", pady=(0, 10))
        
        weight_config = tk.Frame(weights_frame, bg=CARD_BG, relief="flat")
        weight_config.pack(fill="x", padx=15, pady=10, ipady=15)
        
        self.weights = {}
        self.weight_displays = {}
        
        weight_grid = tk.Frame(weight_config, bg=CARD_BG)
        weight_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        for i, (nota, default) in enumerate([("N1", 0.20), ("N2", 0.25), ("N3", 0.25), ("N4", 0.30)]):
            col_frame = tk.Frame(weight_grid, bg=CARD_BG)
            col_frame.pack(side="left", padx=15)
            
            tk.Label(col_frame, text=nota, font=("Segoe UI", 12, "bold"),
                    bg=CARD_BG, fg=COLORS[i if i < 3 else 2]["hex"]).pack()
            
            self.weight_displays[nota] = tk.Label(
                col_frame, text=f"{default:.0%}",
                font=("Segoe UI", 16, "bold"), bg=CARD_BG,
                fg=COLORS[i if i < 3 else 2]["hex"]
            )
            self.weight_displays[nota].pack()
            
            # Scale para ajustar
            scale = tk.Scale(
                col_frame, from_=5, to=50, orient="horizontal",
                bg=CARD_BG, fg=ACCENT, highlightthickness=0,
                troughcolor="#1E2329", length=100,
                command=lambda val, n=nota: self._update_weight(n, val)
            )
            scale.set(int(default * 100))
            scale.pack(pady=(5, 0))
            
            self.weights[nota] = scale
        
        # Label informativo
        tk.Label(
            weight_config, text="Ajuste os pesos e clique em 'Gerar Features' para aplicar",
            font=("Segoe UI", 9), bg=CARD_BG, fg=MUTED
        ).pack(padx=15, pady=(0, 10))
        
        # ────────────────────────────────────────────────────────
        # RODAPÉ
        # ────────────────────────────────────────────────────────
        
        footer = tk.Frame(self, bg=DARK_BG)
        footer.pack(fill="x", padx=20, pady=(0, 15))
        
        tk.Label(
            footer, text="💡 Dica: Treino leva ~30-60s. Não feche a janela durante.",
            font=("Segoe UI", 9), bg=DARK_BG, fg=MUTED
        ).pack(anchor="w")

    def _create_model_card(self, parent, model_name, config):
        """Cria card visual para cada modelo."""
        card = tk.Frame(parent, bg=CARD_BG, relief="flat")
        card.pack(side="left", padx=10, pady=5, ipadx=15, ipady=12, fill="both", expand=True)
        
        # Título
        tk.Label(
            card, text=model_name, font=("Segoe UI", 12, "bold"),
            bg=CARD_BG, fg=ACCENT
        ).pack(anchor="w", pady=(0, 5))
        
        # Descrição
        tk.Label(
            card, text=config, font=("Segoe UI", 9),
            bg=CARD_BG, fg=MUTED, justify="left"
        ).pack(anchor="w", pady=(0, 8))
        
        # Labels para acurácia, data, etc
        info_frame = tk.Frame(card, bg=CARD_BG)
        info_frame.pack(fill="x")
        
        accuracy_var = tk.StringVar(value="Acurácia: —")
        date_var = tk.StringVar(value="Data: —")
        
        tk.Label(info_frame, textvariable=accuracy_var, font=("Segoe UI", 9),
                bg=CARD_BG, fg=SUCCESS).pack(anchor="w")
        tk.Label(info_frame, textvariable=date_var, font=("Segoe UI", 8),
                bg=CARD_BG, fg=MUTED).pack(anchor="w")
        
        self.model_cards[model_name] = {
            "accuracy": accuracy_var,
            "date": date_var,
            "frame": card
        }
        
        self._load_model_info(model_name)

    def _load_model_info(self, model_name):
        """Carrega informações do modelo salvo."""
        try:
            metadata_path = Path(f"ml_models/{model_name}_metadata.json")
            if metadata_path.exists():
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    accuracy = metadata.get("accuracy", 0)
                    date = metadata.get("date", "?")
                    
                    self.model_cards[model_name]["accuracy"].set(
                        f"Acurácia: {accuracy:.1%}"
                    )
                    self.model_cards[model_name]["date"].set(
                        f"Data: {date}"
                    )
        except Exception as e:
            print(f"Erro ao carregar info de {model_name}: {e}")

    def _update_weight(self, nota, value):
        """Atualiza display do peso quando slider muda e salva em config."""
        val = int(value) / 100.0
        self.weight_displays[nota].pack()
        self.weight_displays[nota].config(text=f"{val:.0%}")
        
        # Salvar pesos em arquivo de config
        self._save_weights_config()

    def _save_weights_config(self):
        """Salva pesos atuais em arquivo JSON."""
        try:
            pesos = {}
            for nota, scale in self.weights.items():
                pesos[nota.lower()] = int(scale.get()) / 100.0
            
            # Normalizar para somar 1.0
            total = sum(pesos.values())
            if total > 0:
                pesos = {k: v / total for k, v in pesos.items()}
            
            config = {"pesos": pesos, "atualizado_em": str(pd.Timestamp.now())}
            
            config_path = Path("config_pesos.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar pesos: {e}")

    def _load_weights_config(self):
        """Carrega pesos do arquivo JSON se existir."""
        try:
            config_path = Path("config_pesos.json")
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    pesos = config.get("pesos", {})
                    
                    # Atualizar sliders com valores salvos
                    for nota in ["n1", "n2", "n3", "n4"]:
                        if nota in pesos and nota.upper() in self.weights:
                            val = max(5, min(50, int(pesos[nota] * 100)))
                            self.weights[nota.upper()].set(val)
                            # Atualizar display também
                            self.weight_displays[nota.upper()].config(text=f"{pesos[nota]:.0%}")
        except Exception as e:
            print(f"Erro ao carregar pesos: {e}")

    def _generate_features(self):
        """Gera features com os pesos atuais e exporta para CSV."""
        try:
            # Aplicar pesos
            pesos = {}
            for nota, scale in self.weights.items():
                pesos[nota.lower()] = int(scale.get()) / 100.0
            
            total = sum(pesos.values())
            if total <= 0:
                raise ValueError("Soma dos pesos deve ser > 0")
            
            # Normalizar
            pesos = {k: v / total for k, v in pesos.items()}
            cads.PESOS_NOTAS = pesos
            
            self.status_var.set("⏳ Gerando features...")
            self.progress_var.set(0)
            self.update()
            
            # Gerar features na tabela ml_features
            n, stats = cads.gerar_features_ml()
            
            if n == 0:
                raise ValueError("Nenhuma feature foi gerada. Verifique se há notas cadastradas.")
            
            self.progress_var.set(50)
            self.update()
            
            # Exportar para CSV (necessário para treinar)
            self.status_var.set("⏳ Exportando CSV...")
            csv_path, csv_msg = cads.exportar_ml_csv()
            
            if csv_path is None:
                raise ValueError(f"Erro ao exportar: {csv_msg}")
            
            self.status_var.set(
                f"✅ {n} features geradas e exportadas | "
                f"Aprovado: {stats.get('aprovado', 0)} | "
                f"Recuperação: {stats.get('recuperacao', 0)} | "
                f"Reprovado: {stats.get('reprovado', 0)}"
            )
            self.progress_var.set(100)
            
            messagebox.showinfo("Sucesso", 
                f"Features geradas e exportadas!\n\n"
                f"Total: {n} registros\n"
                f"Aprovado: {stats.get('aprovado', 0)}\n"
                f"Recuperação: {stats.get('recuperacao', 0)}\n"
                f"Reprovado: {stats.get('reprovado', 0)}\n\n"
                f"Agora pode clicar em 'Treinar Modelos'")
            
        except Exception as e:
            self.status_var.set(f"❌ Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao gerar features:\n{e}")

    def _train_all_models(self):
        """Treina todos os 3 modelos."""
        self._train_models(["RF_M1", "RF_M2", "RF_M3"])

    def _train_m3_only(self):
        """Treina apenas RF_M3 (produção)."""
        self._train_models(["RF_M3"])

    def _train_models(self, model_names):
        """Executa treinamento dos modelos especificados."""
        try:
            # Procurar ml_dataset.csv em vários locais possíveis
            possible_paths = [
                Path("ml_dataset.csv"),
                Path("../02-ML/ml_dataset.csv"),
                Path(__file__).parent / "ml_dataset.csv",
            ]
            
            dataset_path = None
            for p in possible_paths:
                if p.exists():
                    dataset_path = p
                    break
            
            if dataset_path is None:
                messagebox.showwarning(
                    "Dados não encontrados",
                    "Clique em 'Gerar Features' primeiro!"
                )
                return
            
            self.status_var.set("⏳ Carregando dados...")
            self.progress_var.set(10)
            self.update()
            
            # Carregar dataset
            df = pd.read_csv(str(dataset_path))
            
            feature_cols = [
                'n1_norm', 'n2_norm', 'n3_norm', 'n4_norm',
                'slope_notas', 'variancia_notas', 'media_geral_aluno',
                'serie_num_norm', 'media_turma_norm'
            ]
            
            X = df[feature_cols]
            y = df['status_encoded']
            
            # Separar treino/teste
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            self.status_var.set("⏳ Treinando modelos...")
            self.progress_var.set(30)
            self.update()
            
            # Treinar modelos
            configs = {
                'RF_M1': {'n_estimators': 100, 'max_depth': 5, 'random_state': 42},
                'RF_M2': {'n_estimators': 150, 'max_depth': 10, 'random_state': 42},
                'RF_M3': {'n_estimators': 200, 'random_state': 42},
            }
            
            Path("ml_models").mkdir(exist_ok=True)
            
            results = {}
            
            for i, model_name in enumerate(model_names):
                if model_name not in configs:
                    continue
                
                self.status_var.set(f"⏳ Treinando {model_name}...")
                progress = 30 + (i + 1) * (60 // len(model_names))
                self.progress_var.set(progress)
                self.update()
                
                # Treinar
                model = RandomForestClassifier(**configs[model_name])
                model.fit(X_train, y_train)
                
                # Avaliar
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred, average='weighted')
                
                # Salvar
                with open(f"ml_models/{model_name}.pkl", "wb") as f:
                    pickle.dump(model, f)
                
                metadata = {
                    "accuracy": float(accuracy),
                    "f1": float(f1),
                    "n_features": len(feature_cols),
                    "features": feature_cols,
                    "n_samples_train": len(X_train),
                    "n_samples_test": len(X_test),
                    "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
                }
                
                with open(f"ml_models/{model_name}_metadata.json", "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                
                results[model_name] = metadata
                
                # Atualizar card
                self._load_model_info(model_name)
            
            # Salvar resumo de treinamento
            self.last_training = {
                "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "models": results,
                "total_samples": len(df),
                "train_size": len(X_train),
                "test_size": len(X_test),
            }
            
            with open("training_summary.json", "w", encoding="utf-8") as f:
                json.dump(self.last_training, f, indent=2, ensure_ascii=False)
            
            self.status_var.set("✅ Treinamento concluído!")
            self.progress_var.set(100)
            
            # Mostrar resumo
            self._show_training_summary(results)
            
        except Exception as e:
            self.status_var.set(f"❌ Erro: {str(e)}")
            messagebox.showerror("Erro no Treinamento", f"{e}")

    def _show_training_summary(self, results):
        """Exibe resumo do treinamento em dialog."""
        summary_text = "📊 RESUMO DE TREINAMENTO\n" + "="*50 + "\n\n"
        
        for model_name, meta in results.items():
            summary_text += f"{model_name}\n"
            summary_text += f"  Acurácia: {meta['accuracy']:.1%}\n"
            summary_text += f"  F1-Score: {meta['f1']:.3f}\n"
            summary_text += f"  Treino: {meta['n_samples_train']} amostras\n"
            summary_text += f"  Teste: {meta['n_samples_test']} amostras\n"
            summary_text += f"  Data: {meta['date']}\n\n"
        
        messagebox.showinfo("Treinamento Concluído", summary_text)

    def _analyze_decision(self):
        """Analisa as decisões do modelo para um aluno/matéria."""
        aluno_nome = self.aluno_var.get()
        materia_nome = self.materia_var.get()
        
        if not aluno_nome or not materia_nome:
            messagebox.showwarning("Campos Vazios", "Selecione aluno e matéria")
            return
        
        try:
            conn = cads.get_conn()
            
            # Buscar dados do registro
            row = conn.execute("""
                SELECT mf.*
                FROM ml_features mf
                WHERE mf.aluno_nome = ? AND mf.materia_nome = ?
                LIMIT 1
            """, (aluno_nome, materia_nome)).fetchone()
            
            conn.close()
            
            if not row:
                messagebox.showwarning("Não Encontrado",
                    f"Nenhum registro para {aluno_nome} em {materia_nome}")
                return
            
            # Montar resultado visual
            output = f"""
╔════════════════════════════════════════════════════════════════╗
║ ANÁLISE DE DECISÃO DO MODELO - MACHINE LEARNING              ║
╚════════════════════════════════════════════════════════════════╝

📋 INFORMAÇÕES:
  Aluno:        {row['aluno_nome']}
  Matéria:      {row['materia_nome']}
  Série:        {row['sala_nome']}
  Data Análise: {row['gerado_em']}

📊 NOTAS:
  N1 (1º Bim):  {row['n1']:.1f}  →  Normalizado: {row['n1_norm']:.3f}
  N2 (2º Bim):  {row['n2']:.1f}  →  Normalizado: {row['n2_norm']:.3f}
  N3 (3º Bim):  {row['n3']:.1f}  →  Normalizado: {row['n3_norm']:.3f}
  N4 (4º Bim):  {row['n4']:.1f}  →  Normalizado: {row['n4_norm']:.3f}

📈 FEATURES CALCULADAS (Entrada do Modelo):
  Média Ponderada:     {row['media_ponderada']:.2f} (normalizado: {row['media_pond_norm']:.3f})
  Slope (Tendência):   {row['slope_notas']:+.3f}  ({self._interpret_slope(row['slope_notas'])})
  Variância (Oscilação): {row['variancia_notas']:.3f}  ({self._interpret_variance(row['variancia_notas'])})
  Média Geral Aluno:   {row['media_geral_aluno']:.2f}
  Série Normalizada:   {row['serie_num_norm']:.3f}
  % Matérias OK:       {row['pct_materias_ok']:.1%}
  Média da Turma:      {row['media_turma_norm']:.3f}

🎯 RESULTADO DO MODELO:
  Status Real:    {row['status_label']} ({row['status_encoded']})
  Confiança:      Verificar arquivo de predições

💡 INTERPRETAÇÃO:
  • N1→N2: Tendência {self._trend_description(row)}
  • Variância: {self._variance_description(row)}
  • Contexto: Aluno está {self._context_description(row)} em {row['materia_nome']}
"""
            
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", output)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao analisar: {e}")

    def _interpret_slope(self, slope):
        """Interpreta valor do slope em linguagem natural."""
        if slope > 0.5:
            return "Forte melhora"
        elif slope > 0:
            return "Melhora leve"
        elif slope < -0.5:
            return "Forte queda"
        elif slope < 0:
            return "Queda leve"
        else:
            return "Estável"

    def _interpret_variance(self, variance):
        """Interpreta variância em linguagem natural."""
        if variance > 0.7:
            return "Muito oscilante"
        elif variance > 0.4:
            return "Oscilante"
        else:
            return "Consistente"

    def _trend_description(self, row):
        """Descreve tendência entre N1 e N2."""
        n1, n2 = row['n1'], row['n2']
        if n1 == 0:
            return "sem dados"
        slope_pct = ((n2 - n1) / n1) * 100
        return f"de {slope_pct:.0f}%"

    def _variance_description(self, row):
        """Descreve padrão de notas."""
        if row['variancia_notas'] < 0.2:
            return "Notas muito consistentes"
        elif row['variancia_notas'] < 0.5:
            return "Notas razoavelmente consistentes"
        else:
            return "Notas muito variáveis - possível problema de assiduidade ou fatores externos"

    def _context_description(self, row):
        """Descreve contexto do aluno."""
        mg = row['media_geral_aluno']
        if mg >= 0.7:
            return "entre os melhores"
        elif mg >= 0.5:
            return "na média"
        else:
            return "com dificuldades"

    def refresh(self):
        """Atualiza dados quando aba é ativada."""
        # Carregar lista de alunos e matérias
        try:
            conn = cads.get_conn()
            
            alunos = [row[0] for row in conn.execute(
                "SELECT DISTINCT aluno_nome FROM ml_features ORDER BY aluno_nome"
            ).fetchall()]
            
            materias = [row[0] for row in conn.execute(
                "SELECT DISTINCT materia_nome FROM ml_features ORDER BY materia_nome"
            ).fetchall()]
            
            conn.close()
            
            self.aluno_cb['values'] = alunos
            self.materia_cb['values'] = materias
            
            # Carregar info dos modelos
            for model_name in ["RF_M1", "RF_M2", "RF_M3"]:
                self._load_model_info(model_name)
            
        except Exception as e:
            print(f"Erro ao atualizar: {e}")
