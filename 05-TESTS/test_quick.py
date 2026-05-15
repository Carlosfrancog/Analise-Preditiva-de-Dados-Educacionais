#!/usr/bin/env python3
"""
🧪 TESTE RÁPIDO - Verificar se tudo funciona
"""

import sys
from datetime import datetime

print("\n" + "="*80)
print("🧪 TESTE RÁPIDO DO SISTEMA DE ML")
print("="*80 + "\n")

# Teste 1: Imports
print("1️⃣  Testando imports...")
try:
    from cads import init_db, gerar_features_ml
    from ml_debug import analyze_class_distribution
    from ml_pipeline import train_random_forest
    from ml_models import compare_models
    print("   ✅ Todos os imports OK\n")
except Exception as e:
    print(f"   ❌ Erro: {e}\n")
    sys.exit(1)

# Teste 2: Dados
print("2️⃣  Verificando dados...")
import sqlite3
conn = sqlite3.connect("escola.db")
count = conn.execute("SELECT COUNT(*) FROM ml_features WHERE status_encoded IS NOT NULL").fetchone()[0]
conn.close()

print(f"   Total de amostras: {count}\n")

if count < 30:
    print("   ⚠️  Dados insuficientes (< 30 amostras)")
    print("   Gerando dados de teste...\n")
    init_db()
    gerar_features_ml()
    conn = sqlite3.connect("escola.db")
    count = conn.execute("SELECT COUNT(*) FROM ml_features WHERE status_encoded IS NOT NULL").fetchone()[0]
    conn.close()
    print(f"   ✅ Dados gerados: {count} amostras\n")

# Teste 3: Análise de distribuição
print("3️⃣  Analisando distribuição de classes...")
dist = analyze_class_distribution(verbose=False)
print(f"   ✅ Distribuição OK (razão desbalanceamento: {dist['imbalance_ratio']:.2f}x)\n")

# Teste 4: Treinar um modelo simples (M1)
print("4️⃣  Treinando modelo M1 (simples, rápido)...")
try:
    model_m1, results_m1, mapping_m1 = train_random_forest("M1", verbose=False)
    print(f"   ✅ M1 treinado!")
    print(f"      Acurácia: {results_m1['accuracy']:.4f}")
    print(f"      F1-Score: {results_m1['f1_macro']:.4f}\n")
except Exception as e:
    print(f"   ❌ Erro ao treinar M1: {e}\n")
    sys.exit(1)

# Teste 5: Resumo
print("="*80)
print("✅ TODOS OS TESTES PASSARAM!")
print("="*80)

print("""
🎉 Sistema de ML está funcionando corretamente!

Próximos passos:
  1. Executar pipeline completa: python run_ml_pipeline.py
  2. Ver exemplos: python example_usage.py
  3. Integrar com GUI: consultar ML_README.md

Para começar:
  python run_ml_pipeline.py
""")
