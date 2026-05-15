#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de treinamento automático dos modelos com análise completa
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
import cads

print("\n" + "="*80)
print("TREINAMENTO AUTOMATICO DE MODELOS ML")
print("="*80)

# ============================================================================
# PASSO 1: Gerar features
# ============================================================================
print("\n[1/4] Gerando features para todas as notas...")
try:
    cads.gerar_features_ml()
    print("     [OK] Features geradas")
except Exception as e:
    print(f"     [ERRO] {e}")
    sys.exit(1)

# ============================================================================
# PASSO 2: Exportar como CSV
# ============================================================================
print("\n[1.5/4] Exportando features como CSV...")
try:
    df_info, msg = cads.exportar_ml_csv()
    if df_info is None:
        print(f"     [ERRO] {msg}")
        sys.exit(1)
    print("     [OK] Features exportadas para ml_dataset.csv")
except Exception as e:
    print(f"     [ERRO] {e}")
    sys.exit(1)

# ============================================================================
# PASSO 3: Carregar dados
# ============================================================================
print("\n[2/4] Carregando dados...")
try:
    df = pd.read_csv("ml_dataset.csv")
    print(f"     [OK] {len(df)} registros carregados")
    print(f"     Distribuicao de classes:")
    for status in [0, 1, 2]:
        count = (df['status_encoded'] == status).sum()
        pct = (count / len(df)) * 100
        nomes = ["Reprovado", "Recuperacao", "Aprovado"]
        print(f"       - {nomes[status]}: {count} ({pct:.1f}%)")
except Exception as e:
    print(f"     [ERRO] {e}")
    sys.exit(1)

# ============================================================================
# PASSO 3: Preparação dos dados
# ============================================================================
print("\n[3/4] Preparando dados para treinamento...")

feature_cols = [
    'n1_norm', 'n2_norm', 'n3_norm', 'n4_norm',
    'slope_notas', 'variancia_notas', 'media_geral_aluno',
    'serie_num_norm', 'media_turma_norm'
]

X = df[feature_cols]
y = df['status_encoded']

# Split 80/20
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"     Features: {len(feature_cols)}")
print(f"     Treino: {len(X_train)} amostras ({(len(X_train)/len(X))*100:.1f}%)")
print(f"     Teste:  {len(X_test)} amostras ({(len(X_test)/len(X))*100:.1f}%)")

# ============================================================================
# PASSO 4: Treinamento dos 3 modelos
# ============================================================================
print("\n[4/4] Treinando modelos...")

modelos = {
    'RF_M1': {
        'config': {'n_estimators': 100, 'max_depth': 5, 'random_state': 42},
        'descricao': 'RF (100 arvores, profund. max 5)'
    },
    'RF_M2': {
        'config': {'n_estimators': 150, 'max_depth': 10, 'random_state': 42},
        'descricao': 'RF (150 arvores, profund. max 10)'
    },
    'RF_M3': {
        'config': {'n_estimators': 200, 'random_state': 42},
        'descricao': 'RF (200 arvores, sem limite de profundidade)'
    }
}

resultados = {}

for nome, info in modelos.items():
    print(f"\n  {nome}: {info['descricao']}")
    
    # Treinar
    modelo = RandomForestClassifier(**info['config'])
    modelo.fit(X_train, y_train)
    
    # Prever
    y_pred = modelo.predict(X_test)
    y_proba = modelo.predict_proba(X_test)
    
    # Metricas
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    resultados[nome] = {
        'modelo': modelo,
        'accuracy': acc,
        'f1': f1,
        'y_pred': y_pred,
        'y_proba': y_proba
    }
    
    print(f"    Acuracia: {acc*100:.1f}%")
    print(f"    F1-Score: {f1:.3f}")
    
    # Matriz de confusao
    cm = confusion_matrix(y_test, y_pred)
    print(f"    Matriz de confusao:")
    for i, row in enumerate(cm):
        print(f"      {row}")

# ============================================================================
# ANALISE COMPARATIVA
# ============================================================================
print("\n" + "="*80)
print("ANALISE COMPARATIVA DOS MODELOS")
print("="*80)

print("\nRanking por Acuracia:")
sorted_by_acc = sorted(resultados.items(), key=lambda x: x[1]['accuracy'], reverse=True)
for i, (nome, res) in enumerate(sorted_by_acc, 1):
    print(f"  {i}. {nome}: {res['accuracy']*100:.1f}%")

print("\nRanking por F1-Score:")
sorted_by_f1 = sorted(resultados.items(), key=lambda x: x[1]['f1'], reverse=True)
for i, (nome, res) in enumerate(sorted_by_f1, 1):
    print(f"  {i}. {nome}: {res['f1']:.3f}")

# ============================================================================
# FEATURE IMPORTANCE DO MELHOR MODELO
# ============================================================================
print("\n" + "="*80)
print("IMPORTANCIA DAS FEATURES (Melhor Modelo)")
print("="*80)

melhor_nome = sorted_by_acc[0][0]
melhor_modelo = resultados[melhor_nome]['modelo']

importances = melhor_modelo.feature_importances_
sorted_idx = np.argsort(importances)[::-1]

print(f"\nModelo: {melhor_nome}\n")
for i, idx in enumerate(sorted_idx):
    feature = feature_cols[idx]
    importance = importances[idx]
    bar = "#" * int(importance * 50)
    print(f"{feature:20s}: {importance:.3f} {bar}")

# ============================================================================
# SALVANDO OS MODELOS
# ============================================================================
print("\n" + "="*80)
print("SALVANDO MODELOS RETREINADOS")
print("="*80)

if not os.path.exists('ml_models'):
    os.makedirs('ml_models')

for nome, res in resultados.items():
    modelo = res['modelo']
    acc = res['accuracy']
    f1 = res['f1']
    
    # Salvar modelo
    filepath = f'ml_models/{nome}.pkl'
    with open(filepath, 'wb') as f:
        pickle.dump(modelo, f)
    
    # Salvar metadata
    metadata = {
        'accuracy': acc,
        'f1_score': f1,
        'n_features': len(feature_cols),
        'features': feature_cols,
        'classes': [0, 1, 2],
        'class_names': ['Reprovado', 'Recuperacao', 'Aprovado']
    }
    
    metadata_path = f'ml_models/{nome}_metadata.json'
    import json
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{nome}:")
    print(f"  - Modelo: {filepath}")
    print(f"  - Metadata: {metadata_path}")
    print(f"  - Acuracia: {acc*100:.1f}%")
    print(f"  - F1-Score: {f1:.3f}")

print("\n" + "="*80)
print("TREINAMENTO CONCLUIDO COM SUCESSO!")
print("="*80 + "\n")

# Dicas
print("DICAS PARA MELHORAR AINDA MAIS:")
print("1. Adicionar mais dados de alunos")
print("2. Tentar outras features (ex: evolucao no tempo)")
print("3. Usar cross-validation para avaliar melhor")
print("4. Testar outros algoritmos (XGBoost, SVM)")
print("5. Fazer tuning de hyperparametros")
print()
