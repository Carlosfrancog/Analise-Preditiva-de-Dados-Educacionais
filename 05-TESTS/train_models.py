#!/usr/bin/env python3
"""
FERRAMENTA DE TREINAMENTO E ANÁLISE DE MODELOS

Permite:
1. Retreinar modelos com dados atualizados
2. Ver importância de cada feature
3. Testar diferentes configurações
4. Comparar performance
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import cads

print(f"\n{'='*80}")
print(f"🤖 FERRAMENTA DE TREINAMENTO DE MODELOS ML")
print(f"{'='*80}\n")

# Opções de menu
print("O que você deseja fazer?\n")
print("1. Retreinar modelos (M1, M2, M3)")
print("2. Analisar importância de features")
print("3. Testar diferentes configurações")
print("4. Comparar modelos")
print("5. Ver estatísticas dos dados\n")

opcao = input("Escolha: ").strip()

# ============================================================================
# OPÇÃO 1: Retreinar modelos
# ============================================================================
if opcao == "1":
    print(f"\n{'='*80}")
    print(f"🔄 RETREINANDO MODELOS...")
    print(f"{'='*80}\n")
    
    # Gera features
    print("1️⃣  Gerando features para todas as notas...")
    try:
        cads.gerar_features_ml()
        print("✅ Features geradas com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao gerar features: {e}")
        sys.exit(1)
    
    # Lê dados
    print("2️⃣  Lendo dados do banco...")
    try:
        df = pd.read_csv("ml_dataset.csv")
        print(f"✅ {len(df)} registros carregados\n")
    except Exception as e:
        print(f"❌ Erro ao ler dados: {e}")
        sys.exit(1)
    
    # Prepara features
    feature_cols = [
        'n1_norm', 'n2_norm', 'n3_norm', 'n4_norm',
        'slope_notas', 'variancia_notas', 'media_geral_aluno',
        'serie_num_norm', 'media_turma_norm'
    ]
    
    X = df[feature_cols]
    y = df['status_encoded']
    
    print(f"3️⃣  Preparando dados...")
    print(f"   - Features: {len(feature_cols)} ({', '.join(feature_cols)})")
    print(f"   - Amostras: {len(X)}")
    print(f"   - Classes: {len(np.unique(y))} (0=Reprovado, 1=Recuperação, 2=Aprovado)\n")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Treina modelos
    modelos = {
        'M1': RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
        'M2': RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42),
        'M3': RandomForestClassifier(n_estimators=200, random_state=42),
    }
    
    print(f"4️⃣  Treinando modelos...\n")
    
    resultados = {}
    
    for nome, modelo in modelos.items():
        print(f"   {nome}...", end=" ", flush=True)
        
        modelo.fit(X_train, y_train)
        
        y_pred = modelo.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        resultados[nome] = {
            'modelo': modelo,
            'acuracia': acc,
            'f1': f1,
            'features': modelo.feature_importances_
        }
        
        print(f"✅ (Acurácia: {acc:.1%}, F1: {f1:.1%})")
    
    # Salva modelos
    print(f"\n5️⃣  Salvando modelos...\n")
    
    os.makedirs('ml_models', exist_ok=True)
    
    for nome, dados in resultados.items():
        modelo = dados['modelo']
        acc = dados['acuracia']
        
        # Cria diretório
        dir_modelo = f'ml_models/RF_{nome}'
        os.makedirs(dir_modelo, exist_ok=True)
        
        # Salva pickle
        with open(f'{dir_modelo}/model.pkl', 'wb') as f:
            pickle.dump(modelo, f)
        
        # Salva metadata json
        import json
        metadata = {
            'acuracia': float(acc),
            'f1_score': float(dados['f1']),
            'features': len(model.feature_importances_),
            'tipo': 'RandomForestClassifier',
            'data_treino': "14/04/2026"
        }
        
        with open(f'{dir_modelo}/metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ RF_{nome} salvo em ml_models/RF_{nome}/")
    
    print(f"\n{'='*80}")
    print(f"✅ TREINAMENTO CONCLUÍDO!")
    print(f"{'='*80}\n")
    
    print(f"📊 RESULTADOS:\n")
    for nome, dados in sorted(resultados.items(), key=lambda x: x[1]['acuracia'], reverse=True):
        print(f"   {nome}: {dados['acuracia']:.1%} acurácia (F1: {dados['f1']:.1%})")
    
    print(f"\nPróximos passos:")
    print(f"  1. Teste: python gui_escola.py")
    print(f"  2. Vá em 'Predições'")
    print(f"  3. Analise um aluno com os novos modelos")

# ============================================================================
# OPÇÃO 2: Analisar importância de features
# ============================================================================
elif opcao == "2":
    print(f"\n{'='*80}")
    print(f"📊 IMPORTÂNCIA DE FEATURES")
    print(f"{'='*80}\n")
    
    try:
        from gui_ml_integration import load_ml_models
        ml = load_ml_models()
        
        feature_names = [
            'N1 Normalizado', 'N2 Normalizado', 'N3 Normalizado', 'N4 Normalizado',
            'Slope (Tendência)', 'Variância', 'Média Geral',
            'Série Normalizada', 'Turma Normalizada'
        ]
        
        for nome in ['RF_M1', 'RF_M2', 'RF_M3']:
            if ml.is_available(nome):
                modelo = ml.models[nome]
                importances = modelo.feature_importances_
                
                print(f"\n{nome}:")
                print(f"{'─'*70}")
                
                for feat_name, imp in sorted(
                    zip(feature_names, importances),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    bar = "█" * int(imp * 50)
                    print(f"  {feat_name:<25} | {bar:<50} | {imp:>6.1%}")
                
    except Exception as e:
        print(f"❌ Erro: {e}")

# ============================================================================
# OPÇÃO 3: Testar diferentes configurações
# ============================================================================
elif opcao == "3":
    print(f"\n{'='*80}")
    print(f"⚙️  TESTANDO CONFIGURAÇÕES")
    print(f"{'='*80}\n")
    
    print("Lendo dados...")
    try:
        cads.gerar_features_ml()
        df = pd.read_csv("ml_dataset.csv")
        
        feature_cols = [
            'n1_norm', 'n2_norm', 'n3_norm', 'n4_norm',
            'slope_notas', 'variancia_notas', 'media_geral_aluno',
            'serie_num_norm', 'media_turma_norm'
        ]
        
        X = df[feature_cols]
        y = df['status_encoded']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print("✅ Dados carregados\n")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)
    
    # Testa diferentes n_estimators
    print("Testando número de árvores:\n")
    
    for n_trees in [50, 100, 150, 200, 250]:
        modelo = RandomForestClassifier(n_estimators=n_trees, random_state=42)
        modelo.fit(X_train, y_train)
        
        y_pred = modelo.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        bar = "█" * int(acc * 50)
        print(f"  {n_trees} árvores | {bar:<50} | {acc:.1%}")
    
    # Testa diferentes max_depth
    print("\n\nTestando profundidade máxima:\n")
    
    for depth in [5, 10, 15, 20, None]:
        modelo = RandomForestClassifier(n_estimators=200, max_depth=depth, random_state=42)
        modelo.fit(X_train, y_train)
        
        y_pred = modelo.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        depth_str = f"{depth}" if depth else "Ilimitado"
        bar = "█" * int(acc * 50)
        print(f"  Profundidade {depth_str:<12} | {bar:<50} | {acc:.1%}")

# ============================================================================
# OPÇÃO 4: Comparar modelos
# ============================================================================
elif opcao == "4":
    print(f"\n{'='*80}")
    print(f"⚖️  COMPARANDO MODELOS")
    print(f"{'='*80}\n")
    
    try:
        cads.gerar_features_ml()
        df = pd.read_csv("ml_dataset.csv")
        
        feature_cols = [
            'n1_norm', 'n2_norm', 'n3_norm', 'n4_norm',
            'slope_notas', 'variancia_notas', 'media_geral_aluno',
            'serie_num_norm', 'media_turma_norm'
        ]
        
        X = df[feature_cols]
        y = df['status_encoded']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print("Testando diferentes algoritmos:\n")
        
        modelos = {
            'Random Forest': RandomForestClassifier(n_estimators=200, random_state=42),
            'Gradient Boost': GradientBoostingClassifier(n_estimators=100, random_state=42),
        }
        
        for nome, modelo in modelos.items():
            print(f"  {nome}...", end=" ", flush=True)
            
            modelo.fit(X_train, y_train)
            y_pred = modelo.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            print(f"✅ (Acurácia: {acc:.1%}, F1: {f1:.1%})")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

# ============================================================================
# OPÇÃO 5: Estatísticas dos dados
# ============================================================================
elif opcao == "5":
    print(f"\n{'='*80}")
    print(f"📈 ESTATÍSTICAS DOS DADOS")
    print(f"{'='*80}\n")
    
    try:
        cads.gerar_features_ml()
        df = pd.read_csv("ml_dataset.csv")
        
        print(f"Total de amostras: {len(df)}")
        print(f"\nDistribuição de classes:")
        
        for status in sorted(df['status_encoded'].unique()):
            count = len(df[df['status_encoded'] == status])
            pct = 100 * count / len(df)
            status_names = {0: "Reprovado", 1: "Recuperação", 2: "Aprovado"}
            print(f"  {status_names[status]:<15}: {count:>4} ({pct:>5.1f}%)")
        
        print(f"\nEstatísticas de cada feature:")
        
        feature_cols = [
            'n1_norm', 'n2_norm', 'n3_norm', 'n4_norm',
            'slope_notas', 'variancia_notas', 'media_geral_aluno',
            'serie_num_norm', 'media_turma_norm'
        ]
        
        for col in feature_cols:
            mean = df[col].mean()
            std = df[col].std()
            print(f"  {col:<25}: μ={mean:.3f}, σ={std:.3f}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

else:
    print("❌ Opção inválida")
