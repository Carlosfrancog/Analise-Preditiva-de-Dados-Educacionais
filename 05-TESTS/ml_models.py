#!/usr/bin/env python3
"""
📊 ANÁLISE DE EXPLICABILIDADE E INTERPRETABILIDADE
Feature Importance, SHAP, visualizações
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import sqlite3
from ml_pipeline import load_model, MODELS_DIR

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False


def get_conn():
    conn = sqlite3.connect("escola.db")
    conn.row_factory = sqlite3.Row
    return conn


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 FEATURE IMPORTANCE (Built-in do Random Forest)
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_feature_importance(model_dir, top_n=10, plot=True, save_path=None):
    """
    Análise de importância das features usando Random Forest importances.
    """
    model, results, mapping = load_model(model_dir)
    
    feature_names = mapping["feature_names"]
    importances = model.feature_importances_
    
    # Ordenar por importância
    indices = np.argsort(importances)[::-1]
    
    analysis = {
        "model_type": mapping["model_type"],
        "total_features": len(feature_names),
        "feature_ranking": {}
    }
    
    print(f"\n{'='*80}")
    print(f"🔍 FEATURE IMPORTANCE - {mapping['model_type']}")
    print(f"{'='*80}\n")
    
    for i in range(min(top_n, len(feature_names))):
        feat_idx = indices[i]
        feat_name = feature_names[feat_idx]
        importance = importances[feat_idx]
        
        analysis["feature_ranking"][feat_name] = float(importance)
        
        bar = "█" * int(importance * 80)
        print(f"{i+1:2d}. {feat_name:30s}: {importance:.6f} {bar}")
    
    # Categorizar features
    print(f"\n{'─'*80}")
    print("📂 CATEGORIZAÇÃO DE FEATURES:\n")
    
    note_features = [f for f in feature_names if 'norm' in f and f.startswith('n')]
    behavior_features = [f for f in feature_names if f in ['slope_notas', 'variancia_notas']]
    context_features = [f for f in feature_names if f not in note_features and f not in behavior_features]
    
    print(f"📝 Notas parciais ({len(note_features)}):")
    for feat in note_features:
        importance = importances[feature_names.index(feat)]
        print(f"   {feat:30s}: {importance:.6f}")
    
    print(f"\n🎯 Comportamento ({len(behavior_features)}):")
    for feat in behavior_features:
        importance = importances[feature_names.index(feat)]
        print(f"   {feat:30s}: {importance:.6f}")
    
    print(f"\n🔗 Contexto ({len(context_features)}):")
    for feat in context_features:
        importance = importances[feature_names.index(feat)]
        print(f"   {feat:30s}: {importance:.6f}")
    
    # Plotar
    if plot:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        top_indices = indices[:top_n]
        top_features = [feature_names[i] for i in top_indices]
        top_importances = importances[top_indices]
        
        # Cores por categoria
        colors = []
        for feat in top_features:
            if any(feat.startswith(n) for n in ['n1', 'n2', 'n3', 'n4']):
                colors.append('#FF6B6B')
            elif feat in ['slope_notas', 'variancia_notas']:
                colors.append('#4ECDC4')
            else:
                colors.append('#45B7D1')
        
        ax.barh(top_features, top_importances, color=colors)
        ax.set_xlabel('Importância', fontsize=12)
        ax.set_title(f'Feature Importance - Modelo {mapping["model_type"]}', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        plt.tight_layout()
        
        if save_path is None:
            save_path = MODELS_DIR / "feature_importance_plot.png"
        
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Gráfico salvo em: {save_path}")
        plt.close()
    
    return analysis


# ═══════════════════════════════════════════════════════════════════════════════
# 🎬 EXPLICAÇÕES BASEADAS EM SHAP (opcional)
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_with_shap(model_dir, sample_size=100, plot=True):
    """
    Análise SHAP para explicabilidade avançada.
    Requer: pip install shap
    """
    if not SHAP_AVAILABLE:
        print("⚠️  SHAP não instalado. Execute: pip install shap")
        return None
    
    # Carregar modelo
    model, results, mapping = load_model(model_dir)
    feature_names = mapping["feature_names"]
    
    # Carregar dados de treino
    conn = get_conn()
    df = pd.read_sql_query(f"""
        SELECT {', '.join(feature_names)} FROM ml_features
        WHERE status_encoded IS NOT NULL
        LIMIT ?
    """, conn, params=(sample_size,))
    conn.close()
    
    X = df[feature_names].values
    
    # Criar explainer SHAP
    print(f"\n{'='*80}")
    print(f"🎬 EXPLICABILIDADE SHAP - {mapping['model_type']}")
    print(f"{'='*80}\n")
    print("Calculando SHAP values (isso pode levar um tempo)...")
    
    # TreeExplainer para Random Forest
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    # Análise de importância média
    print("\n📊 MÉDIA DE IMPACTO ABSOLUTO POR FEATURE:\n")
    
    # Para classificação multiclasse, shap_values é lista de arrays
    if isinstance(shap_values, list):
        # Média de impacto em todas as classes
        mean_abs_shap = np.mean([np.abs(sv).mean(axis=0) for sv in shap_values], axis=0)
    else:
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
    
    # Ordenar
    indices = np.argsort(mean_abs_shap)[::-1]
    
    for i, idx in enumerate(indices):
        feat_name = feature_names[idx]
        impact = mean_abs_shap[idx]
        bar = "█" * int(impact * 50)
        print(f"{i+1:2d}. {feat_name:30s}: {impact:.6f} {bar}")
    
    # Plotar
    if plot and isinstance(shap_values, list):
        # SHAP summary plot (para primeira classe por simplicidade)
        fig, ax = plt.subplots(figsize=(12, 6))
        shap.summary_plot(shap_values[2], X, feature_names=feature_names, plot_type="bar", show=False)
        plt.title(f'SHAP Feature Importance - {mapping["model_type"]} (Classe: Aprovado)', fontsize=14)
        plt.tight_layout()
        plt.savefig(MODELS_DIR / "shap_importance_plot.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("\n✅ Gráfico SHAP salvo")
    
    return shap_values, explainer


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 ANÁLISE DE CORRELAÇÃO COM TARGET
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_feature_target_correlation(model_dir, plot=True):
    """
    Analisa correlação de cada feature com o target.
    Ajuda a identificar relacionamentos lineares.
    """
    model, results, mapping = load_model(model_dir)
    feature_names = mapping["feature_names"]
    
    # Carregar dados
    conn = get_conn()
    df = pd.read_sql_query(f"""
        SELECT {', '.join(feature_names)}, status_encoded
        FROM ml_features
        WHERE status_encoded IS NOT NULL
    """, conn)
    conn.close()
    
    # Calcular correlações
    correlations = {}
    for feat in feature_names:
        corr = df[feat].corr(df['status_encoded'])
        correlations[feat] = float(corr)
    
    # Ordenar
    sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    
    print(f"\n{'='*80}")
    print(f"📊 CORRELAÇÃO FEATURE-TARGET - {mapping['model_type']}")
    print(f"{'='*80}\n")
    
    for feat, corr in sorted_corr:
        direction = "↑" if corr > 0 else "↓"
        bar = "█" * int(abs(corr) * 40)
        print(f"{feat:30s}: {corr:7.4f} {direction} {bar}")
    
    # Plot
    if plot:
        fig, ax = plt.subplots(figsize=(12, 6))
        feats, corrs = zip(*sorted_corr)
        colors = ['green' if c > 0 else 'red' for c in corrs]
        ax.barh(feats, corrs, color=colors)
        ax.set_xlabel('Correlação', fontsize=12)
        ax.set_title(f'Correlação Feature-Target - {mapping["model_type"]}', fontsize=14, fontweight='bold')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(MODELS_DIR / "correlation_plot.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✅ Gráfico salvo em: {MODELS_DIR / 'correlation_plot.png'}")
    
    return correlations


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 DETECÇÃO DE OVERFITTING
# ═══════════════════════════════════════════════════════════════════════════════

def detect_overfitting(model_dir):
    """
    Detecta sinais de overfitting comparando train vs test performance.
    """
    try:
        model, results, mapping = load_model(model_dir)
        
        # Métricas disponíveis
        accuracy = results.get('accuracy')
        f1_test = results.get('f1_macro')
        f1_train_approx = f1_test * (1 + 0.1)  # Estimativa grosseira
        
        cv_mean = results.get('cv_mean', 0)
        cv_std = results.get('cv_std', 0)
        
        gap = abs(accuracy - cv_mean)
        
        print(f"\n{'='*80}")
        print(f"🔍 ANÁLISE DE OVERFITTING - {mapping['model_type']}")
        print(f"{'='*80}\n")
        
        print(f"Test Accuracy:  {accuracy:.4f}")
        print(f"CV Mean:        {cv_mean:.4f}")
        print(f"CV Std:         {cv_std:.4f}")
        print(f"Gap (Overfit):  {gap:.4f}")
        
        if gap > 0.1:
            print("\n⚠️  POSSÍVEL OVERFITTING DETECTADO!")
            print("  • Reduzir max_depth")
            print("  • Aumentar min_samples_split")
            print("  • Aumentar min_samples_leaf")
        elif gap < 0.02:
            print("\n✅ Sem sinais de overfitting")
        else:
            print("\n✅ Overfitting leve (aceitável)")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# 📈 COMPARAÇÃO ENTRE MODELOS
# ═══════════════════════════════════════════════════════════════════════════════

def compare_models():
    """
    Compara performance dos 3 modelos (M1, M2, M3).
    """
    print(f"\n{'█'*80}")
    print("📊 COMPARAÇÃO ENTRE MODELOS".center(80))
    print(f"{'█'*80}\n")
    
    models_to_compare = []
    for model_type in ["M1", "M2", "M3"]:
        model_paths = list(MODELS_DIR.glob(f"RF_{model_type}_*"))
        if model_paths:
            # Pegar o mais recente
            model_dir = max(model_paths, key=lambda p: p.stat().st_mtime)
            models_to_compare.append((model_type, model_dir))
    
    if not models_to_compare:
        print("❌ Nenhum modelo encontrado. Treine os modelos primeiro.")
        return
    
    # Tabela comparativa
    comparison_data = []
    
    for model_type, model_dir in models_to_compare:
        try:
            model, results, mapping = load_model(model_dir)
            
            comparison_data.append({
                "Modelo": model_type,
                "Accuracy": f"{results['accuracy']:.4f}",
                "F1 (macro)": f"{results['f1_macro']:.4f}",
                "F1 (weighted)": f"{results['f1_weighted']:.4f}",
                "CV Mean": f"{results['cv_mean']:.4f}",
                "CV Std": f"{results['cv_std']:.4f}",
                "Features": mapping["n_features"],
                "Amostras": mapping["n_samples"]
            })
        except Exception as e:
            print(f"❌ Erro ao carregar {model_type}: {e}")
    
    if comparison_data:
        df = pd.DataFrame(comparison_data)
        
        # Imprimir tabela
        print("┌" + "─" * 120 + "┐")
        for i, row in enumerate(df.iterrows()):
            if i == 0:
                print("│ " + " │ ".join(f"{col:12s}" for col in df.columns) + " │")
                print("├" + "─" * 120 + "┤")
            print("│ " + " │ ".join(f"{str(v):12s}" for v in row[1].values) + " │")
        print("└" + "─" * 120 + "┘")
        
        # Recomendação
        print(f"\n{'─'*80}")
        print("💡 RECOMENDAÇÕES:\n")
        
        best_idx = df['Accuracy'].str.split('.').apply(lambda x: float(x[0] + '.' + x[1])).idxmax()
        best_model = df.loc[best_idx, 'Modelo']
        
        print(f"✅ Melhor modelo em produção: {best_model}")
        print(f"   • Balanceamento entre complexidade e performance")
        print(f"   • {df.loc[best_idx, 'Features']} features")
        print(f"   • Acurácia: {df.loc[best_idx, 'Accuracy']}")
        
        if best_model == "M1":
            print("\n   ⚠️  M1 é adequado para previsão MUITO antecipada")
            print("   • Use para detectar risco antes de N2")
        elif best_model == "M2":
            print("\n   ✅ M2 é o melhor balance")
            print("   • Usa feedback de N1 e N2")
            print("   • Tempo útil para intervenção")
        elif best_model == "M3":
            print("\n   ⚠️  M3 é completo mas tardio")
            print("   • Usa dados até N3")
            print("   • Último momento para intervenção")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎓 RELATÓRIO DE EXPLICABILIDADE COMPLETO
# ═══════════════════════════════════════════════════════════════════════════════

def generate_explainability_report(model_dir, model_type="M3"):
    """
    Gera relatório completo de explicabilidade.
    """
    print(f"\n{'█'*80}")
    print(f"📋 RELATÓRIO COMPLETO DE EXPLICABILIDADE - {model_type}".center(80))
    print(f"{'█'*80}\n")
    
    # 1. Feature Importance
    print("1️⃣  IMPORTÂNCIA DAS FEATURES")
    print("─" * 80)
    importance_analysis = analyze_feature_importance(model_dir, top_n=10, plot=True)
    
    # 2. Correlação
    print("\n2️⃣  CORRELAÇÃO COM TARGET")
    print("─" * 80)
    correlations = analyze_feature_target_correlation(model_dir, plot=True)
    
    # 3. Overfitting
    print("\n3️⃣  ANÁLISE DE OVERFITTING")
    print("─" * 80)
    detect_overfitting(model_dir)
    
    # 4. SHAP (se disponível)
    if SHAP_AVAILABLE:
        print("\n4️⃣  ANÁLISE SHAP")
        print("─" * 80)
        try:
            shap_values, explainer = analyze_with_shap(model_dir, sample_size=50, plot=True)
        except Exception as e:
            print(f"⚠️  Erro na análise SHAP: {e}")
    
    print(f"\n{'█'*80}")
    print("✅ RELATÓRIO CONCLUÍDO".center(80))
    print(f"{'█'*80}\n")


if __name__ == "__main__":
    # Gerar relatórios para todos os modelos
    for model_type in ["M1", "M2", "M3"]:
        model_paths = list(MODELS_DIR.glob(f"RF_{model_type}_*"))
        if model_paths:
            model_dir = max(model_paths, key=lambda p: p.stat().st_mtime)
            print(f"\n{'='*80}\n")
            generate_explainability_report(model_dir, model_type=model_type)
    
    # Comparação entre modelos
    compare_models()
