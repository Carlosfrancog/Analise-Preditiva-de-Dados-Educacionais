#!/usr/bin/env python3
"""
Integracao ML com GUI Escolar
Dashboard de Predicoes e Analise de Desempenho por Aluno
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from pathlib import Path
import pickle
import json
from typing import Optional, Dict, List
import sys
import numpy as np
import pandas as pd

# Adicionar pastas ao path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "01-CORE"))
sys.path.insert(0, str(project_root / "02-ML"))
sys.path.insert(0, str(project_root / "03-GUI"))

import cads  # ← Importar para usar cads.get_conn()

# ──────────────────────────────────────────────────────────────────────────────
# 📊 CARREGADOR DE MODELOS TREINADOS
# ──────────────────────────────────────────────────────────────────────────────

class MLModelLoader:
    """Carrega e gerencia os modelos treinados (M1, M2, M3)."""
    
    def __init__(self):
        self.models = {}
        self.metadata = {}
        # Procurar ml_models em locais possíveis
        if Path("ml_models").exists():
            self.models_dir = Path("ml_models")
        elif Path("../02-ML/ml_models").exists():
            self.models_dir = Path("../02-ML/ml_models")
        elif (Path(__file__).parent / "ml_models").exists():
            self.models_dir = Path(__file__).parent / "ml_models"
        else:
            self.models_dir = Path("ml_models")
        
        self._load_models()
    
    def _load_models(self):
        """Carrega todos os modelos disponíveis."""
        if not self.models_dir.exists():
            print(f"[!] Diretorio ml_models nao encontrado em {self.models_dir.resolve()}")
            return
        
        # Procura por arquivos .pkl (novo formato) ou subdiretórios (antigo formato)
        model_files = list(self.models_dir.glob("RF_M*.pkl"))
        model_dirs = [d for d in self.models_dir.glob("RF_M*") if d.is_dir()]
        
        # Carregar modelos do novo formato (arquivos .pkl)
        for model_file in model_files:
            model_name = model_file.stem  # ex: RF_M1, RF_M2, RF_M3
            
            try:
                # Carregar modelo
                with open(model_file, "rb") as f:
                    self.models[model_name] = pickle.load(f)
                
                # Carregar metadata
                metadata_file = self.models_dir / f"{model_name}_metadata.json"
                with open(metadata_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    self.metadata[model_name] = metadata
                
                accuracy = metadata.get('accuracy', 0)
                n_features = metadata.get('n_features', '?')
                print(f"[OK] {model_name} carregado (acuracia: {accuracy:.1%}, {n_features} features)")
            
            except Exception as e:
                print(f"[ERRO] Erro ao carregar {model_name}: {e}")
        
        # Carregar modelos do antigo formato (subdiretórios)
        for model_dir in model_dirs:
            model_name = model_dir.name  # ex: RF_M1, RF_M2, RF_M3
            
            # Pular se já foi carregado do novo formato
            if model_name in self.models:
                continue
            
            try:
                # Carregar modelo
                with open(model_dir / "model.pkl", "rb") as f:
                    self.models[model_name] = pickle.load(f)
                
                # Carregar metadata
                with open(model_dir / "metadata.json", "r", encoding="utf-8") as f:
                    content = f.read()
                    # Trata se metadata foi salvo como string
                    if content.startswith('"') and content.endswith('"'):
                        import ast
                        metadata = ast.literal_eval(content)
                    else:
                        metadata = json.loads(content)
                    self.metadata[model_name] = metadata
                
                accuracy = metadata.get('accuracy', 0)
                n_features = metadata.get('n_features', '?')
                print(f"[OK] {model_name} carregado (acuracia: {accuracy:.1%}, {n_features} features)")
            
            except Exception as e:
                print(f"[ERRO] Erro ao carregar {model_name}: {e}")
    
    def is_available(self, model_name="RF_M3"):
        """Verifica se um modelo está disponível."""
        return model_name in self.models
    
    def predict(self, model_name, features):
        """Faz predicao com um modelo."""
        if model_name not in self.models:
            return None, None
        
        try:
            model = self.models[model_name]
            
            # Obter feature names do metadata
            feature_names = self.metadata.get(model_name, {}).get('features', None)
            
            if feature_names:
                # Usar DataFrame com nomes de features (elimina aviso)
                features_df = pd.DataFrame([features], columns=feature_names)
                proba = model.predict_proba(features_df)[0]
            else:
                # Fallback para array numpy
                features_array = np.array([features])
                proba = model.predict_proba(features_array)[0]
            
            pred = np.argmax(proba)
            
            return pred, proba
        except Exception as e:
            print(f"[ERRO] Erro na predicao: {e}")
            return None, None


# ──────────────────────────────────────────────────────────────────────────────
# 🎯 ANALISADOR DE DESEMPENHO POR DISCIPLINA
# ──────────────────────────────────────────────────────────────────────────────

class DisciplinePerformanceAnalyzer:
    """Analisa o desempenho do aluno em cada disciplina."""
    
    STATUS_COLOR = {
        0: {"name": "Reprovado", "color": "#C62828", "emoji": "[X]", "weight": 0},
        1: {"name": "Recuperacao", "color": "#FF9800", "emoji": "[!]", "weight": 0.5},
        2: {"name": "Aprovado", "color": "#2E7D32", "emoji": "[ok]", "weight": 1},
    }
    
    @staticmethod
    def analyze_student(db_path, aluno_id, model_loader):
        """
        Analisa o desempenho do aluno em TODAS as disciplinas.
        
        Retorna dict com:
        - aluno: info do aluno
        - disciplinas: lista com análise de cada disciplina
        - risk_level: nível geral de risco
        - strengths: disciplinas em que está bem
        - weaknesses: disciplinas que precisam atenção
        """
        
        conn = cads.get_conn()  # ← Usar cads.get_conn() para path correto
        
        # Buscar aluno
        aluno = conn.execute(
            "SELECT a.id, a.nome, a.matricula, s.nome as sala_nome FROM alunos a LEFT JOIN salas s ON a.sala_id=s.id WHERE a.id = ?", 
            (aluno_id,)
        ).fetchone()
        
        if not aluno:
            conn.close()
            return None
        
        # Buscar todas as disciplinas do aluno
        disciplinas = conn.execute("""
            SELECT DISTINCT d.id, d.nome
            FROM materias d
            JOIN notas n ON n.materia_id = d.id
            WHERE n.aluno_id = ?
            ORDER BY d.nome
        """, (aluno_id,)).fetchall()
        
        analise = {
            "aluno": {
                "id": aluno["id"],
                "nome": aluno["nome"],
                "matricula": aluno["matricula"],
                "sala": aluno["sala_nome"],
            },
            "disciplinas": [],
            "strengths": [],
            "weaknesses": [],
            "at_risk": [],
            "profile": "Equilibrado",
        }
        
        risk_scores = []
        
        for materia in disciplinas:
            # Buscar notas dessa disciplina
            notas = conn.execute("""
                SELECT n1, n2, n3, n4 FROM notas
                WHERE aluno_id = ? AND materia_id = ?
            """, (aluno_id, materia["id"])).fetchone()
            
            if not notas:
                continue
            
            # Notas em escala 0-10 (SEM normalizar)
            n1_raw = notas[0] if notas[0] is not None else 0
            n2_raw = notas[1] if notas[1] is not None else 0
            n3_raw = notas[2] if notas[2] is not None else 0
            n4_raw = notas[3] if notas[3] is not None else 0
            
            # Preparar features NORMALIZADAS (0-1) para modelo ML
            n1 = n1_raw / 10 if n1_raw > 0 else 0
            n2 = n2_raw / 10 if n2_raw > 0 else 0
            n3 = n3_raw / 10 if n3_raw > 0 else 0
            n4 = n4_raw / 10 if n4_raw > 0 else 0
            
            # Calcular média ponderada (escala 0-10) levando em conta apenas notas preenchidas
            notas_preenchidas = []
            pesos_prop = []
            
            if n1_raw > 0:
                notas_preenchidas.append(n1_raw)
                pesos_prop.append(0.2)
            if n2_raw > 0:
                notas_preenchidas.append(n2_raw)
                pesos_prop.append(0.25)
            if n3_raw > 0:
                notas_preenchidas.append(n3_raw)
                pesos_prop.append(0.25)
            if n4_raw > 0:
                notas_preenchidas.append(n4_raw)
                pesos_prop.append(0.30)
            
            # Normalizar pesos para somar 1.0
            if pesos_prop:
                soma_pesos = sum(pesos_prop)
                pesos_prop = [p / soma_pesos for p in pesos_prop]
                media = sum(n * p for n, p in zip(notas_preenchidas, pesos_prop))
            else:
                media = 0
            
            # Determinar status (escala 0-10)
            if media < 5:
                status = 0  # Reprovado
            elif media < 6:
                status = 1  # Recuperação
            else:
                status = 2  # Aprovado
            
            disc_info = {
                "id": materia["id"],
                "nome": materia["nome"],
                "n1": n1_raw,
                "n2": n2_raw,
                "n3": n3_raw,
                "n4": n4_raw,
                "media": media,
                "status": status,
                "status_name": DisciplinePerformanceAnalyzer.STATUS_COLOR[status]["name"],
                "status_color": DisciplinePerformanceAnalyzer.STATUS_COLOR[status]["color"],
                "emoji": DisciplinePerformanceAnalyzer.STATUS_COLOR[status]["emoji"],
                "risk_score": max(0, min(1, 1 - (media / 10))),  # 0 = seguro, 1 = em risco
                "trend": "->",  # Padrão: mantém
                "prognosis": "normal",
                "predicted_status": None,
            }
            
            # ============================================================================
            # PREDIÇÃO REAL: Usar modelo para prever desempenho futuro
            # ============================================================================
            
            if n1_raw > 0 or n2_raw > 0:
                # Calcular features para o modelo
                slope = (n2 - n1) if (n1_raw > 0 and n2_raw > 0) else 0
                variancia = abs(n1 - n2) if (n1_raw > 0 and n2_raw > 0) else 0
                media_atual = (n1_raw + n2_raw) / 2
                media_norm = media_atual / 10
                
                # ================================================================
                # IMPORTANTE: Para predição com N1+N2 apenas:
                # Zeramento N3 e N4 (ainda não aconteceram)
                # ================================================================
                
                features_pred = [n1, n2, 0, 0, slope, variancia, media_norm, 0.5, 0.5]
                
                # Faz predição com modelo ML (usando apenas N1+N2)
                if model_loader.is_available("RF_M3"):
                    try:
                        pred, proba = model_loader.predict("RF_M3", features_pred)
                        
                        if pred is not None:
                            predicted_status = int(pred)
                            disc_info["predicted_status"] = predicted_status
                            disc_info["predicted_proba"] = list(proba) if proba is not None else None
                            
                            # ================================================================
                            # ANÁLISE DE TENDÊNCIA: Compara previsão com realidade
                            # ================================================================
                            
                            # Se tem N3 e N4: análise de como realmente foi
                            if n3_raw > 0 or n4_raw > 0:
                                # Calcula status REAL de N3+N4
                                notas_n34 = []
                                pesos_n34 = []
                                if n3_raw > 0:
                                    notas_n34.append(n3_raw)
                                    pesos_n34.append(0.5)
                                if n4_raw > 0:
                                    notas_n34.append(n4_raw)
                                    pesos_n34.append(0.5)
                                
                                if pesos_n34:
                                    soma_pesos = sum(pesos_n34)
                                    pesos_norm = [p / soma_pesos for p in pesos_n34]
                                    media_n34 = sum(n * p for n, p in zip(notas_n34, pesos_norm))
                                else:
                                    media_n34 = 0
                                
                                # Status real de N3+N4
                                if media_n34 < 5:
                                    status_real_n34 = 0
                                elif media_n34 < 6:
                                    status_real_n34 = 1
                                else:
                                    status_real_n34 = 2
                                
                                # Comparar previsão (baseada em N1+N2) com realidade (N3+N4)
                                if predicted_status < status_real_n34:
                                    disc_info["trend"] = "[+]"  # Melhorou do que era esperado
                                    disc_info["prognosis"] = "better_than_expected"
                                elif predicted_status > status_real_n34:
                                    disc_info["trend"] = "[-]"  # Piorou do que era esperado
                                    disc_info["prognosis"] = "worse_than_expected"
                                else:
                                    disc_info["trend"] = "->"   # Manteve o previsto
                                    disc_info["prognosis"] = "as_expected"
                            
                            # Se só tem N1 e N2: mostrar prognóstico baseado em tendência + modelo
                            else:
                                # Calcula status atual apenas com N1+N2
                                media_n12 = (n1_raw + n2_raw) / 2 if (n1_raw > 0 and n2_raw > 0) else n1_raw if n1_raw > 0 else n2_raw
                                
                                if media_n12 < 5:
                                    status_n12 = 0
                                elif media_n12 < 6:
                                    status_n12 = 1
                                else:
                                    status_n12 = 2
                                
                                # ============================================================
                                # IMPORTANTE: Considerar o SINAL do slope
                                # ============================================================
                                # slope > 0: N2 > N1 = MELHORA (mesmo com variância alta!)
                                # slope < 0: N2 < N1 = PIORA (e variância alta piora mais)
                                # slope ≈ 0: N2 ≈ N1 = ESTÁVEL
                                # ============================================================
                                
                                if n1_raw > 0 and n2_raw > 0:
                                    # Temos esplope real
                                    slope_pct = ((n2_raw - n1_raw) / n1_raw) * 100
                                    
                                    if slope_pct > 20:
                                        # Melhora significativa (> 20%)
                                        disc_info["trend"] = "[*]"
                                        disc_info["prognosis"] = "will_improve"
                                    elif slope_pct < -20:
                                        # Queda significativa (< -20%)
                                        disc_info["trend"] = "[!]"
                                        disc_info["prognosis"] = "will_decline"
                                    else:
                                        # Estavel (-20% a +20%)
                                        # Usar modelo como desempate
                                        if predicted_status > status_n12:
                                            disc_info["trend"] = "[*]"
                                            disc_info["prognosis"] = "will_improve"
                                        elif predicted_status < status_n12:
                                            disc_info["trend"] = "[!]"
                                            disc_info["prognosis"] = "will_decline"
                                        else:
                                            disc_info["trend"] = "->"
                                            disc_info["prognosis"] = "stable"
                                else:
                                    # Só N1 ou só N2: usar modelo
                                    if predicted_status > status_n12:
                                        disc_info["trend"] = "[*]"
                                        disc_info["prognosis"] = "will_improve"
                                    elif predicted_status < status_n12:
                                        disc_info["trend"] = "[!]"
                                        disc_info["prognosis"] = "will_decline"
                                    else:
                                        disc_info["trend"] = "->"
                                        disc_info["prognosis"] = "stable"
                            
                    except Exception as e:
                        # Se falhar predição, apenas ignora
                        pass
            
            # Gerar explicação baseada no prognosis
            disc_info["explicacao"] = DisciplineCard._gerar_explicacao_pred(
                n1_raw, n2_raw, n3_raw, n4_raw, disc_info["prognosis"]
            )
            
            analise["disciplinas"].append(disc_info)
            risk_scores.append(disc_info["risk_score"])
            
            # Classificação por status atual
            if status == 2:
                analise["strengths"].append(materia["nome"])
            elif status == 0:
                analise["weaknesses"].append(materia["nome"])
            elif status == 1:
                analise["at_risk"].append(materia["nome"])
        
        # Perfil geral
        if risk_scores:
            avg_risk = np.mean(risk_scores)
            if avg_risk > 0.7:
                analise["profile"] = "🔴 CRÍTICO - Atenção imediata"
            elif avg_risk > 0.4:
                analise["profile"] = "🟡 EM RISCO - Acompanhamento"
            else:
                analise["profile"] = "🟢 SEGURO - Desempenho normal"
        
        conn.close()
        return analise


# ──────────────────────────────────────────────────────────────────────────────
# 🎨 WIDGETS CUSTOMIZADOS
# ──────────────────────────────────────────────────────────────────────────────

class StatusBadge(tk.Frame):
    """Widget que mostra o status com indicador e cor."""
    
    def __init__(self, parent, status_code, status_name, **kwargs):
        super().__init__(parent, bg="white", relief="flat", **kwargs)
        
        colors = {
            0: "#FFEBEE",  # Vermelho claro - Reprovado
            1: "#FFF3E0",  # Laranja claro - Recuperação
            2: "#E8F5E9",  # Verde claro - Aprovado
        }
        
        emojis = {
            0: "❌",
            1: "⚠️ ",
            2: "✅",
        }
        
        fg_colors = {
            0: "#C62828",
            1: "#E65100",
            2: "#2E7D32",
        }
        
        self.configure(bg=colors.get(status_code, "white"))
        
        tk.Label(
            self,
            text=f"{emojis.get(status_code, '•')} {status_name}",
            font=("Segoe UI", 10, "bold"),
            bg=colors.get(status_code),
            fg=fg_colors.get(status_code)
        ).pack(padx=8, pady=4)


class DisciplineCard(tk.Frame):
    """Card individual de uma disciplina."""
    
    def __init__(self, parent, disc_info, **kwargs):
        super().__init__(parent, bg="white", relief="solid", bd=1, **kwargs)
        
        # Header
        head = tk.Frame(self, bg="#F5F5F5")
        head.pack(fill="x")
        
        tk.Label(
            head,
            text=disc_info["nome"],
            font=("Segoe UI", 11, "bold"),
            bg="#F5F5F5",
            fg="#1A1A2E"
        ).pack(anchor="w", padx=12, pady=8, side="left", expand=True)
        
        StatusBadge(head, disc_info["status"], disc_info["status_name"]).pack(
            side="right", padx=8, pady=4
        )
        
        # Body
        body = tk.Frame(self, bg="white")
        body.pack(fill="both", expand=True, padx=12, pady=8)
        
        # Notas
        notas_frame = tk.Frame(body, bg="white")
        notas_frame.pack(fill="x", pady=(0, 8))
        
        for i, (label, value) in enumerate([
            ("N1", disc_info["n1"]),
            ("N2", disc_info["n2"]),
            ("N3", disc_info["n3"]),
            ("N4", disc_info["n4"]),
        ]):
            col = tk.Frame(notas_frame, bg="white")
            col.pack(side="left", expand=True)
            
            if value is None:
                tk.Label(col, text=label, font=("Segoe UI", 8), fg="#999").pack()
                tk.Label(col, text="—", font=("Segoe UI", 11, "bold"), fg="#CCC").pack()
            else:
                tk.Label(col, text=label, font=("Segoe UI", 8), fg="#666").pack()
                tk.Label(
                    col,
                    text=f"{value:.1f}",
                    font=("Segoe UI", 12, "bold"),
                    fg="#1A1A2E"
                ).pack()
        
        # Média
        media_frame = tk.Frame(body, bg="#E8EAF6", relief="flat")
        media_frame.pack(fill="x", pady=(8, 0), ipadx=12, ipady=6)
        
        tk.Label(
            media_frame,
            text="Média Ponderada:",
            font=("Segoe UI", 9),
            bg="#E8EAF6",
            fg="#5C6BC0"
        ).pack(anchor="w")
        
        tk.Label(
            media_frame,
            text=f"{disc_info['media']:.2f}",
            font=("Segoe UI", 14, "bold"),
            bg="#E8EAF6",
            fg="#3949AB"
        ).pack(anchor="w")
        
        # Tendência e Prognóstico (adicionado)
        if disc_info.get("trend") or disc_info.get("prognosis"):
            trend_frame = tk.Frame(body, bg="white")
            trend_frame.pack(fill="x", pady=(8, 0))
            
            trend = disc_info.get("trend", "→")
            prognosis = disc_info.get("prognosis", "normal")
            
            # Mapa de prognósticos para descrição amigável
            prognosis_map = {
                "will_decline": "⚠️ Vai PIORAR se não estudar más",
                "will_improve": "✨ Vai MELHORAR naturalmente",
                "stable": "→ Vai manter o mesmo nível",
                "worse_than_expected": "📉 Piorou do que era previsto",
                "better_than_expected": "📈 Melhorou mais que o previsto",
                "as_expected": "→ Mantendo a previsão normal",
                "normal": "→ Status normal"
            }
            
            desc = prognosis_map.get(prognosis, "Status desconhecido")
            
            tk.Label(
                trend_frame,
                text=f"{trend} {desc}",
                font=("Segoe UI", 9, "italic"),
                bg="white",
                fg="#E65100" if "PIORAR" in desc or "📉" in trend else "#2E7D32"
            ).pack(anchor="w")
            
            # Explicação matemática (tooltip style)
            explain_frame = tk.Frame(body, bg="#FFF9C4", relief="flat", bd=1)
            explain_frame.pack(fill="x", pady=(8, 0), padx=0)
            
            # Gera explicação
            n1 = disc_info.get("n1", 0)
            n2 = disc_info.get("n2", 0)
            n3 = disc_info.get("n3", 0)
            n4 = disc_info.get("n4", 0)
            
            explicacao = DisciplineCard._gerar_explicacao_pred(n1, n2, n3, n4, prognosis)
            
            tk.Label(
                explain_frame,
                text=explicacao,
                font=("Segoe UI", 8),
                bg="#FFF9C4",
                fg="#E65100",
                justify="left",
                wraplength=300
            ).pack(anchor="w", padx=8, pady=4)
        
        # Tendência e Prognóstico (removido duplicado abaixo)
        elif disc_info.get("trend"):
            trend_frame = tk.Frame(body, bg="white")
            trend_frame.pack(fill="x", pady=(8, 0))
            
            trend = disc_info.get("trend", "→")
    
    @staticmethod
    def _gerar_explicacao_pred(n1, n2, n3, n4, prognosis):
        """Gera explicacao matematica da predicao."""
        
        if not n1 and not n2:
            return "Sem dados para prognostico"
        
        # Calcula slope
        if n1 and n2:
            slope_pct = ((n2 - n1) / n1) * 100
            variancia = abs(n1 - n2)
            media = (n1 + n2) / 2
        else:
            slope_pct = 0
            variancia = 0
            media = n1 or n2 or 0
        
        # Gera mensagem
        if prognosis == "will_decline":
            if slope_pct < -30:
                return f"Queda BRUSCA de {abs(slope_pct):.0f}% (N1->N2). Tendencia negativa forte!"
            else:
                return f"Desempenho em risco. Variacao detectada ({variancia:.1f} pts)."
        
        elif prognosis == "will_improve":
            if slope_pct > 50:
                return f"MELHORA EXCEPCIONAL de {slope_pct:.0f}% (N1->N2)!"
            elif slope_pct > 20:
                return f"Melhora significativa de {slope_pct:.0f}% (N1->N2). Otimo progresso!"
            else:
                return f"Base solida ({media:.1f}). Modelo preve continuidade."
        
        elif prognosis == "stable":
            if abs(slope_pct) < 5:
                return f"Desempenho consistente ({media:.1f}). Sem fluctuacoes significativas."
            else:
                return f"Desempenho moderado ({media:.1f}). Estabilidade esperada."
        
        elif prognosis == "better_than_expected":
            return f"Superou a previsao! Melhoria maior que esperado."
        
        elif prognosis == "worse_than_expected":
            return f"Desempenho abaixo. Queda maior que a prevista."
        
        elif prognosis == "as_expected":
            return f"Confirmou a previsao. Desempenho dentro do esperado."
        
        else:
            return "Status: analise em andamento"


# ──────────────────────────────────────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ──────────────────────────────────────────────────────────────────────────────

def load_ml_models():
    """Carrega os modelos treinados."""
    return MLModelLoader()


def get_disciplinas_by_turma(db_path, sala_id):
    """Busca disciplinas de uma turma."""
    conn = cads.get_conn()  # ← Usar cads.get_conn()
    cursor = conn.execute("""
        SELECT DISTINCT d.id, d.nome
        FROM materias d
        WHERE d.sala_id = ?
        ORDER BY d.nome
    """, (sala_id,))
    result = cursor.fetchall()
    conn.close()
    return result


if __name__ == "__main__":
    # Test
    loader = load_ml_models()
    print(f"Modelos disponíveis: {list(loader.models.keys())}")
