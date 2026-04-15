#!/usr/bin/env python3
"""
🤖 PIPELINE DE MACHINE LEARNING - RANDOM FOREST
Treina modelos de classificação multiclasse (0, 1, 2) do status do aluno
Modelos temporais: M1 (N1), M2 (N1+N2), M3 (N1+N2+N3)
"""

import sqlite3
import pickle
import json
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    f1_score, precision_score, recall_score
)
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

DB_PATH = "escola.db"
MODELS_DIR = Path("ml_models")
MODELS_DIR.mkdir(exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ═══════════════════════════════════════════════════════════════════════════════
# 🔴 REMOÇÃO DE DATA LEAKAGE
# ═══════════════════════════════════════════════════════════════════════════════

def remove_data_leakage():
    """
    Define features SEGURAS (sem vazamento de informação do target).
    
    REMOVIDAS:
    - media_pond_norm: calculada diretamente do target
    - n4_norm: avaliação final (alta predictibilidade do status)
    - qualquer feature derivada do target
    
    MANTIDAS:
    - n1_norm, n2_norm, n3_norm: notas parciais
    - slope_notas: tendência
    - variancia_notas: consistência
    - pct_materias_ok, media_geral_aluno: contexto
    - serie_num_norm, media_turma_norm: contexto
    """
    safe_features = {
        "M1": [  # Apenas N1 (previsão muito antecipada)
            "n1_norm"
        ],
        "M2": [  # N1 + N2 + comportamento (previsão intermediária)
            "n1_norm", "n2_norm",
            "slope_notas", "variancia_notas"
        ],
        "M3": [  # N1 + N2 + N3 + contexto (previsão robusta)
            "n1_norm", "n2_norm", "n3_norm",
            "slope_notas", "variancia_notas",
            "pct_materias_ok", "media_geral_aluno",
            "serie_num_norm", "media_turma_norm"
        ]
    }
    
    return safe_features


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ═══════════════════════════════════════════════════════════════════════════════

def load_data_for_training(model_type="M3", verbose=True):
    """
    Carrega dados do banco de dados, remove leakage e retorna X, y preparados.
    
    Parametros:
    - model_type: "M1", "M2", ou "M3"
    - verbose: prints detalhados
    
    Retorna:
    - X: features (np.array)
    - y: target (np.array)
    - feature_names: lista de nomes das features
    - mapping: dicionário metadata
    """
    conn = get_conn()
    
    # Todas as features disponíveis
    all_features = [
        "n1_norm", "n2_norm", "n3_norm",
        "slope_notas", "variancia_notas",
        "pct_materias_ok", "media_geral_aluno",
        "serie_num_norm", "media_turma_norm"
    ]
    
    # Carregar dados
    df = pd.read_sql_query(f"""
        SELECT 
            aluno_id, materia_id, aluno_nome, materia_nome, sala_nome,
            {', '.join(all_features)},
            status_encoded, status_label
        FROM ml_features
        WHERE status_encoded IS NOT NULL
    """, conn)
    
    conn.close()
    
    if df.empty:
        raise ValueError("Nenhuma feature ML gerada. Execute cads.gerar_features_ml() primeiro.")
    
    # Selecionar features pelo model type
    safe_features = remove_data_leakage()
    selected_features = safe_features.get(model_type, safe_features["M3"])
    
    # Remover linhas com valores nulos nas features selecionadas
    df_clean = df.dropna(subset=selected_features + ["status_encoded"])
    
    if len(df_clean) < 30:
        raise ValueError(f"Dados insuficientes após limpeza: {len(df_clean)} amostras")
    
    X = df_clean[selected_features].values
    y = df_clean["status_encoded"].values
    
    mapping = {
        "model_type": model_type,
        "n_samples": len(df_clean),
        "n_features": len(selected_features),
        "feature_names": selected_features,
        "class_distribution": dict(pd.Series(y).value_counts().sort_index()),
        "class_labels": {0: "Reprovado", 1: "Recuperação", 2: "Aprovado"},
        "removed_null_samples": len(df) - len(df_clean)
    }
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"📊 CARREGAMENTO DE DADOS - {model_type}")
        print(f"{'='*80}")
        print(f"\nFeatures selecionadas: {len(selected_features)}")
        print(f"  {', '.join(selected_features)}")
        print(f"\nAmostras totais: {len(df)}")
        print(f"Amostras válidas: {len(df_clean)}")
        print(f"Amostras removidas (nulos): {mapping['removed_null_samples']}")
        print(f"\nDistribuição de classes:")
        for class_id, label in mapping["class_labels"].items():
            count = mapping["class_distribution"].get(class_id, 0)
            pct = 100 * count / len(df_clean)
            print(f"  {label:15s}: {count:4d} ({pct:5.1f}%)")
    
    return X, y, selected_features, mapping


# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 TREINAMENTO DO RANDOM FOREST
# ═══════════════════════════════════════════════════════════════════════════════

def train_random_forest(model_type="M3", test_size=0.2, random_state=42, verbose=True):
    """
    Treina modelo Random Forest com validação cruzada.
    
    Retorna:
    - model: modelo treinado
    - results: dict com métricas
    - mapping: metadata
    """
    # Carregar e preparar dados
    X, y, feature_names, mapping = load_data_for_training(model_type, verbose=False)
    
    # Train-test split com estratificação
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state,
        stratify=y
    )
    
    # Treinar modelo
    # Usar class_weight='balanced' se houver desbalanceamento
    unique, counts = np.unique(y_train, return_counts=True)
    imbalance_ratio = max(counts) / min(counts)
    
    class_weight = 'balanced' if imbalance_ratio > 1.5 else None
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=random_state,
        n_jobs=-1,
        class_weight=class_weight,
        verbose=0
    )
    
    model.fit(X_train, y_train)
    
    # Predições
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Métricas
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    
    # Classification report
    class_report = classification_report(
        y_test, y_pred,
        target_names=["Reprovado", "Recuperação", "Aprovado"],
        output_dict=True
    )
    
    # Confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Cross-validation scores
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1_macro')
    
    results = {
        "model_type": model_type,
        "accuracy": float(accuracy),
        "f1_macro": float(f1_macro),
        "f1_weighted": float(f1_weighted),
        "cv_scores": [float(s) for s in cv_scores],
        "cv_mean": float(cv_scores.mean()),
        "cv_std": float(cv_scores.std()),
        "imbalance_ratio": float(imbalance_ratio),
        "class_weight_used": class_weight is not None,
        "classification_report": class_report,
        "confusion_matrix": conf_matrix.tolist(),
        "feature_importance": {
            feature_names[i]: float(importance)
            for i, importance in enumerate(model.feature_importances_)
        },
        "training_set_size": len(X_train),
        "test_set_size": len(X_test),
        "timestamp": datetime.now().isoformat()
    }
    
    if verbose:
        print_training_results(results, mapping)
    
    return model, results, mapping


def print_training_results(results, mapping):
    """Imprime resultados do treinamento de forma formatada."""
    print(f"\n{'='*80}")
    print(f"🎯 RESULTADOS DO TREINAMENTO - {results['model_type']}")
    print(f"{'='*80}")
    
    print(f"\n📊 MÉTRICAS DE DESEMPENHO:")
    print(f"  Acurácia:          {results['accuracy']:.4f}")
    print(f"  F1-Score (macro):  {results['f1_macro']:.4f}")
    print(f"  F1-Score (weighted): {results['f1_weighted']:.4f}")
    
    print(f"\n🔄 VALIDAÇÃO CRUZADA (5-fold):")
    print(f"  Scores:  {[f'{s:.4f}' for s in results['cv_scores']]}")
    print(f"  Média:   {results['cv_mean']:.4f} ± {results['cv_std']:.4f}")
    
    print(f"\n📈 CONFIGURAÇÃO:")
    print(f"  Features: {mapping['n_features']}")
    print(f"  Train set: {results['training_set_size']}")
    print(f"  Test set:  {results['test_set_size']}")
    print(f"  Class weight: {'SIM' if results['class_weight_used'] else 'NÃO'}")
    
    print(f"\n🎓 PERFORMANCE POR CLASSE:")
    for class_name in ["Reprovado", "Recuperação", "Aprovado"]:
        if class_name in results['classification_report']:
            cr = results['classification_report'][class_name]
            print(f"  {class_name:15s}: precision={cr['precision']:.3f}  recall={cr['recall']:.3f}  f1={cr['f1-score']:.3f}")
    
    print(f"\n🔍 IMPORTÂNCIA DAS FEATURES (top 5):")
    importances = sorted(
        results['feature_importance'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    for feat, importance in importances[:5]:
        bar = "█" * int(importance * 50)
        print(f"  {feat:25s}: {importance:6.4f} {bar}")
    
    # Confusion matrix formatado
    print(f"\n📊 MATRIZ DE CONFUSÃO:")
    cm = results['confusion_matrix']
    labels = ["Repr.", "Recup.", "Aprov."]
    print(f"            Predito")
    print(f"            {labels[0]:>6s} {labels[1]:>6s} {labels[2]:>6s}")
    for i, label in enumerate(labels):
        print(f"  Real {label}: {cm[i][0]:6d} {cm[i][1]:6d} {cm[i][2]:6d}")


# ═══════════════════════════════════════════════════════════════════════════════
# 💾 PERSISTÊNCIA E CARREGAMENTO DE MODELOS
# ═══════════════════════════════════════════════════════════════════════════════

def save_model(model, results, mapping, model_name=None):
    """Salva modelo em disco."""
    if model_name is None:
        model_name = f"{results['model_type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    model_dir = MODELS_DIR / model_name
    model_dir.mkdir(exist_ok=True)
    
    # Função auxiliar de serialização
    def serialize(obj, depth=0):
        if depth > 50:
            return str(obj)
        try:
            if obj is None:
                return None
            if isinstance(obj, bool):
                return bool(obj)
            if isinstance(obj, int) and not isinstance(obj, np.integer):
                return obj
            if isinstance(obj, float) and not isinstance(obj, np.floating):
                return obj
            if isinstance(obj, str):
                return obj
            if isinstance(obj, np.bool_):
                return bool(obj)
            if isinstance(obj, (np.integer, np.int_, np.int64, np.int32)):
                return int(obj)
            if isinstance(obj, (np.floating, np.float_, np.float64, np.float32)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return serialize(obj.tolist(), depth=depth+1)
            if isinstance(obj, dict):
                return {k: serialize(v, depth=depth+1) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [serialize(item, depth=depth+1) for item in obj]
            if isinstance(obj, bytes):
                return str(obj)
            return str(obj)
        except Exception:
            return str(obj)
    
    # Salvar modelo
    with open(model_dir / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    # Salvar resultados
    with open(model_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(serialize(results), f, indent=2, ensure_ascii=False)
    
    # Salvar mapping
    with open(model_dir / "mapping.json", "w", encoding="utf-8") as f:
        json.dump(serialize(mapping), f, indent=2, ensure_ascii=False)
    
    # Metadados
    metadata = {
        "model_name": model_name,
        "timestamp": datetime.now().isoformat(),
        "model_type": results["model_type"],
        "accuracy": float(results["accuracy"]),
        "f1_macro": float(results["f1_macro"]),
        "n_features": int(mapping["n_features"]),
        "n_samples": int(mapping["n_samples"])
    }
    
    with open(model_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(serialize(metadata), f, indent=2, ensure_ascii=False)
    
    return str(model_dir)


def load_model(model_dir):
    """Carrega modelo do disco."""
    model_dir = Path(model_dir)
    
    with open(model_dir / "model.pkl", "rb") as f:
        model = pickle.load(f)
    
    with open(model_dir / "results.json") as f:
        results = json.load(f)
    
    with open(model_dir / "mapping.json") as f:
        mapping = json.load(f)
    
    return model, results, mapping


# ═══════════════════════════════════════════════════════════════════════════════
# 🔮 PREDIÇÃO EM TEMPO REAL
# ═══════════════════════════════════════════════════════════════════════════════

def predict_student_status(model_dir, aluno_id, materia_id):
    """
    Faz predição para um aluno específico (aquele com dados em ml_features).
    
    Retorna:
    - probabilities: dict com {status_label: probabilidade}
    - predicted_class: classe predita (0, 1, 2)
    """
    model, results, mapping = load_model(model_dir)
    
    # Buscar dados do aluno na ml_features
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT *
        FROM ml_features
        WHERE aluno_id = ? AND materia_id = ?
    """, conn, params=(aluno_id, materia_id))
    conn.close()
    
    if df.empty:
        return None, f"Nenhum registro para aluno {aluno_id} e matéria {materia_id}"
    
    # Extrair features
    feature_names = mapping["feature_names"]
    X = df[feature_names].values
    
    # Predição
    y_proba = model.predict_proba(X)[0]
    y_pred = model.predict(X)[0]
    
    class_labels = {0: "Reprovado", 1: "Recuperação", 2: "Aprovado"}
    
    return {
        "aluno_id": aluno_id,
        "materia_id": materia_id,
        "aluno_nome": df.iloc[0]['aluno_nome'],
        "materia_nome": df.iloc[0]['materia_nome'],
        "predicted_class": int(y_pred),
        "predicted_label": class_labels[y_pred],
        "probabilities": {
            class_labels[i]: float(y_proba[i])
            for i in range(3)
        },
        "confidence": float(max(y_proba))
    }, None


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 TREINAR TODOS OS MODELOS
# ═══════════════════════════════════════════════════════════════════════════════

def train_all_models(verbose=True):
    """
    Treina os 3 modelos temporais: M1, M2, M3.
    
    Retorna:
    - dict com todos os modelos e resultados
    """
    all_results = {}
    
    for model_type in ["M1", "M2", "M3"]:
        print(f"\n{'█'*80}")
        print(f"█ Treinando modelo {model_type}".ljust(79) + "█")
        print(f"{'█'*80}")
        
        try:
            model, results, mapping = train_random_forest(
                model_type=model_type,
                verbose=True
            )
            
            # Salvar modelo
            model_path = save_model(model, results, mapping, model_name=f"RF_{model_type}")
            results["model_path"] = model_path
            
            all_results[model_type] = {
                "status": "sucesso",
                "results": results,
                "mapping": mapping,
                "model_path": model_path
            }
            
            print(f"\n✅ Modelo {model_type} treinado e salvo em: {model_path}")
        
        except Exception as e:
            all_results[model_type] = {
                "status": "erro",
                "mensagem": str(e)
            }
            print(f"\n❌ Erro ao treinar modelo {model_type}: {e}")
    
    # Resumo comparativo
    print(f"\n{'█'*80}")
    print("📊 RESUMO COMPARATIVO DE MODELOS".center(80))
    print(f"{'█'*80}\n")
    
    for model_type in ["M1", "M2", "M3"]:
        if all_results[model_type]["status"] == "sucesso":
            res = all_results[model_type]["results"]
            print(f"{model_type}: Acurácia={res['accuracy']:.4f}, F1={res['f1_macro']:.4f}, CV={res['cv_mean']:.4f}")
    
    return all_results


if __name__ == "__main__":
    # Treinar todos os modelos
    all_results = train_all_models(verbose=True)
    
    # Salvar resumo
    with open("training_summary.json", "w", encoding="utf-8") as f:
        # Serializar para JSON
        def serialize(obj):
            if obj is None:
                return None
            if isinstance(obj, bool):
                return obj
            if isinstance(obj, (int, float)):
                return obj
            if isinstance(obj, np.bool_):
                return bool(obj)
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return serialize(obj.tolist())
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [serialize(i) for i in obj]
            if isinstance(obj, (str, bytes)):
                return obj
            return str(obj)
        
        json.dump(serialize(all_results), f, indent=2, ensure_ascii=False)
    
    print("\n✅ Resumo salvo em training_summary.json")
