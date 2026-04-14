#!/usr/bin/env python3
"""
🔗 INTEGRAÇÃO COM GUI
Módulo para integrar o sistema de ML com a interface gráfica (gui_escola.py)
"""

import threading
import queue
from pathlib import Path
from datetime import datetime
import json

try:
    from tkinter import messagebox
except ImportError:
    messagebox = None

from ml_pipeline import load_model, predict_student_status, MODELS_DIR
from ml_debug import analyze_class_distribution
import sqlite3


class MLModel:
    """
    Wrapper para carregar e usar modelos de ML.
    Gerencia cache e predições.
    """
    
    def __init__(self, model_type="M3"):
        """
        Inicializa e carrega o modelo mais recente.
        
        Parametros:
        - model_type: "M1", "M2", ou "M3"
        """
        self.model_type = model_type
        self.model = None
        self.results = None
        self.mapping = None
        self.model_dir = None
        self.loaded = False
        
        self._load_model()
    
    def _load_model(self):
        """Carrega o modelo mais recente do tipo especificado."""
        try:
            model_dirs = list(MODELS_DIR.glob(f"RF_{self.model_type}_*"))
            
            if not model_dirs:
                print(f"⚠️  Nenhum modelo {self.model_type} encontrado em {MODELS_DIR}")
                return False
            
            # Usar o mais recente
            self.model_dir = max(model_dirs, key=lambda p: p.stat().st_mtime)
            self.model, self.results, self.mapping = load_model(self.model_dir)
            self.loaded = True
            
            print(f"✅ Modelo {self.model_type} carregado de: {self.model_dir.name}")
            print(f"   Acurácia: {self.results['accuracy']:.4f}")
            print(f"   Features: {', '.join(self.mapping['feature_names'])}")
            
            return True
        
        except Exception as e:
            print(f"❌ Erro ao carregar modelo {self.model_type}: {e}")
            return False
    
    def predict(self, aluno_id, materia_id):
        """
        Faz predição para um aluno em uma matéria.
        
        Retorna:
        - dict com predição e probabilidades
        - ou None se houver erro
        """
        if not self.loaded:
            return None
        
        try:
            prediction, error = predict_student_status(
                self.model_dir,
                aluno_id=aluno_id,
                materia_id=materia_id
            )
            return prediction if error is None else None
        
        except Exception as e:
            print(f"❌ Erro na predição: {e}")
            return None
    
    def get_info(self):
        """Retorna informações do modelo."""
        if not self.loaded:
            return None
        
        return {
            "modelo": self.model_type,
            "caminho": str(self.model_dir),
            "acuracia": self.results['accuracy'],
            "f1_macro": self.results['f1_macro'],
            "f1_weighted": self.results['f1_weighted'],
            "cv_mean": self.results['cv_mean'],
            "cv_std": self.results['cv_std'],
            "features": self.mapping['feature_names'],
            "n_features": self.mapping['n_features'],
            "n_samples_treino": self.mapping['n_samples'],
            "data_treino": self.results.get('timestamp', 'N/A')
        }


class MLPredictionEngine:
    """
    Motor de predição separado que pode rodar em thread.
    Útil para não travar a GUI durante predições.
    """
    
    def __init__(self, model_type="M3"):
        self.model = MLModel(model_type)
        self.cache = {}  # Cache simples para evitar recálculos
    
    def predict_batch(self, predictions_list):
        """
        Faz predições em batch (para múltiplos alunos).
        
        Parametros:
        - predictions_list: list de dicts {"aluno_id": ..., "materia_id": ...}
        
        Retorna:
        - list de resultados
        """
        results = []
        
        for item in predictions_list:
            aluno_id = item["aluno_id"]
            materia_id = item["materia_id"]
            
            # Verificar cache
            cache_key = f"{aluno_id}_{materia_id}"
            if cache_key in self.cache:
                results.append(self.cache[cache_key])
                continue
            
            # Predição
            prediction = self.model.predict(aluno_id, materia_id)
            
            if prediction:
                self.cache[cache_key] = prediction
                results.append(prediction)
        
        return results
    
    def predict_with_callback(self, aluno_id, materia_id, callback):
        """
        Faz predição de forma assíncrona e chama callback quando pronto.
        Útil para não travar GUI.
        
        Parametros:
        - aluno_id: id do aluno
        - materia_id: id da matéria
        - callback: função callable(prediction)
        """
        def _predict():
            prediction = self.model.predict(aluno_id, materia_id)
            if callback:
                callback(prediction)
        
        # Rodar em thread separada
        thread = threading.Thread(target=_predict, daemon=True)
        thread.start()


# ═════════════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES PARA GUI
# ═════════════════════════════════════════════════════════════════════════════════

def format_prediction_for_display(prediction):
    """Formata predição para exibição na GUI."""
    if not prediction:
        return None
    
    return {
        "aluno": prediction.get('aluno_nome', 'N/A'),
        "materia": prediction.get('materia_nome', 'N/A'),
        "status": prediction.get('predicted_label', 'N/A'),
        "confianca": f"{prediction.get('confidence', 0):.1%}",
        "probabilidades": {
            label: f"{prob:.1%}"
            for label, prob in prediction.get('probabilities', {}).items()
        },
        "classe": prediction.get('predicted_class', -1)
    }


def get_class_distribution_summary():
    """Retorna resumo da distribuição de classes para exibição."""
    try:
        dist = analyze_class_distribution(verbose=False)
        
        return {
            "total": dist.get('total', 0),
            "aprovado": dist.get('distribuicao', {}).get('Aprovado', 0),
            "recuperacao": dist.get('distribuicao', {}).get('Recuperação', 0),
            "reprovado": dist.get('distribuicao', {}).get('Reprovado', 0),
            "desbalanceamento": f"{dist.get('imbalance_ratio', 1):.2f}x"
        }
    except:
        return None


def get_available_models():
    """Retorna lista de modelos disponíveis."""
    models = {}
    
    for model_type in ["M1", "M2", "M3"]:
        model_dirs = list(MODELS_DIR.glob(f"RF_{model_type}_*"))
        
        if model_dirs:
            latest = max(model_dirs, key=lambda p: p.stat().st_mtime)
            
            try:
                _, results, mapping = load_model(latest)
                models[model_type] = {
                    "disponivel": True,
                    "caminho": str(latest),
                    "acuracia": results['accuracy'],
                    "f1": results['f1_macro'],
                    "features": len(mapping['feature_names']),
                    "data": latest.name.split('_')[-1]
                }
            except:
                models[model_type] = {
                    "disponivel": False,
                    "motivo": "Erro ao carregar"
                }
        else:
            models[model_type] = {
                "disponivel": False,
                "motivo": "Modelo não encontrado"
            }
    
    return models


# ═════════════════════════════════════════════════════════════════════════════════
# EXEMPLO DE INTEGRAÇÃO NA GUI
# ═════════════════════════════════════════════════════════════════════════════════

def exemplo_integracao_gui():
    """
    Exemplo de como integrar com tkinter (gui_escola.py).
    
    Adicionar à classe principal:
    
        from ml_gui_integration import MLModel, format_prediction_for_display
        
        def __init__(self):
            # ...
            self.ml_engine = MLModel("M3")
            self.setup_ml_tab()
        
        def setup_ml_tab(self):
            # Criar aba para ML
            ml_frame = Frame(self.notebook)
            self.notebook.add(ml_frame, text="ML Predictions")
            
            # Label de status
            status_label = Label(ml_frame, text="Carregando modelo...")
            status_label.pack()
            
            if self.ml_engine.loaded:
                info = self.ml_engine.get_info()
                text = f"Modelo {info['modelo']} - Acurácia: {info['acuracia']:.2%}"
                status_label.config(text=text)
            
            # Entrada de dados
            # ...
            
            # Botão de predição
            def fazer_predicao():
                aluno_id = int(entry_aluno.get())
                materia_id = int(entry_materia.get())
                
                prediction = self.ml_engine.predict(aluno_id, materia_id)
                formatted = format_prediction_for_display(prediction)
                
                if formatted:
                    resultado_label.config(
                        text=f"Status: {formatted['status']} "
                             f"({formatted['confianca']})"
                    )
                else:
                    resultado_label.config(text="Erro na predição")
            
            btn_predict = Button(ml_frame, text="Prever Status", command=fazer_predicao)
            btn_predict.pack()
    """
    pass


if __name__ == "__main__":
    # Teste
    print("\n" + "="*80)
    print("🔗 TESTE DE INTEGRAÇÃO")
    print("="*80 + "\n")
    
    # Listar modelos disponíveis
    print("📊 Modelos disponíveis:\n")
    models = get_available_models()
    for model_type, info in models.items():
        if info.get('disponivel'):
            print(f"✅ {model_type}")
            print(f"   Acurácia: {info['acuracia']:.4f}")
            print(f"   F1: {info['f1']:.4f}")
            print(f"   Data: {info['data']}\n")
        else:
            print(f"❌ {model_type}: {info.get('motivo')}\n")
    
    # Criar engine
    print("─"*80)
    print("Carregando motor de predição (M3)...\n")
    engine = MLPredictionEngine("M3")
    
    if engine.model.loaded:
        print("✅ Motor pronto para predições\n")
        
        # Info do modelo
        info = engine.model.get_info()
        print("Informações do modelo:")
        for key, value in info.items():
            if key != 'features':
                print(f"  {key}: {value}")
        
        # Exemplo de predição
        print("\n" + "─"*80)
        print("Exemplo de predição:\n")
        prediction = engine.model.predict(1, 1)
        
        if prediction:
            formatted = format_prediction_for_display(prediction)
            print(f"Aluno: {formatted['aluno']}")
            print(f"Matéria: {formatted['materia']}")
            print(f"Status predito: {formatted['status']}")
            print(f"Confiança: {formatted['confianca']}")
            print(f"Probabilidades:")
            for label, prob in formatted['probabilidades'].items():
                print(f"  {label}: {prob}")
        else:
            print("Sem dados disponíveis para este par aluno-materia")
    else:
        print("❌ Falha ao carregar modelo")
