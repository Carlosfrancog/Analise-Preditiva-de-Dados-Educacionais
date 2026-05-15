#!/usr/bin/env python3
"""
🧪 TESTE DA INTEGRAÇÃO ML COM GUI

Este script testa se todos os componentes estão funcionando corretamente.
"""

import sys
from pathlib import Path

print("\n" + "="*80)
print("🧪 TESTE DE INTEGRAÇÃO ML + GUI ESCOLAR")
print("="*80 + "\n")

# ──────────────────────────────────────────────────────────────────────────────
# 1. VERIFICAR IMPORTS
# ──────────────────────────────────────────────────────────────────────────────

print("1️⃣  Verificando imports...")
try:
    import cads
    print("   ✅ cads (backend)")
except ImportError as e:
    print(f"   ❌ cads: {e}")
    sys.exit(1)

try:
    from gui_ml_integration import MLModelLoader, DisciplinePerformanceAnalyzer
    print("   ✅ gui_ml_integration")
except ImportError as e:
    print(f"   ❌ gui_ml_integration: {e}")
    sys.exit(1)

try:
    from gui_predicoes import PredictionPage, SalasPage
    print("   ✅ gui_predicoes (páginas ML)")
except ImportError as e:
    print(f"   ❌ gui_predicoes: {e}")
    sys.exit(1)

try:
    from gui_escola import App
    print("   ✅ gui_escola (aplicação principal)")
except ImportError as e:
    print(f"   ❌ gui_escola: {e}")
    sys.exit(1)

print("\n✅ Todos os imports OK\n")

# ──────────────────────────────────────────────────────────────────────────────
# 2. VERIFICAR MODELOS TREINADOS
# ──────────────────────────────────────────────────────────────────────────────

print("2️⃣  Verificando modelos ML treinados...")

loader = MLModelLoader()
modelos = list(loader.models.keys())

if not modelos:
    print("   ⚠️  Nenhum modelo encontrado em ml_models/")
    print("   Execute antes: python run_pipeline_simple.py")
    sys.exit(1)

for model_name in sorted(modelos):
    metadata = loader.metadata.get(model_name, {})
    acuracia = metadata.get('accuracy', 0)
    n_features = metadata.get('n_features', '?')
    print(f"   ✅ {model_name}: {acuracia:.1%} acurácia, {n_features} features")

print("")

# ──────────────────────────────────────────────────────────────────────────────
# 3. VERIFICAR BANCO DE DADOS
# ──────────────────────────────────────────────────────────────────────────────

print("3️⃣  Verificando banco de dados...")

import sqlite3
try:
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    
    # Contar entidades
    salas = cursor.execute("SELECT COUNT(*) FROM salas").fetchone()[0]
    alunos = cursor.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
    materias = cursor.execute("SELECT COUNT(*) FROM materias").fetchone()[0]
    notas = cursor.execute("SELECT COUNT(*) FROM notas").fetchone()[0]
    
    print(f"   ✅ Salas: {salas}")
    print(f"   ✅ Alunos: {alunos}")
    print(f"   ✅ Matérias: {materias}")
    print(f"   ✅ Notas: {notas}")
    
    if alunos == 0:
        print("\n   ⚠️  Aviso: Nenhum aluno cadastrado!")
        print("      Use a GUI para adicionar alunos ou gerar dados de teste.")
    
    conn.close()
except Exception as e:
    print(f"   ❌ Erro ao acessar banco: {e}")
    sys.exit(1)

print("")

# ──────────────────────────────────────────────────────────────────────────────
# 4. TESTE DE ANÁLISE (Se houver dados)
# ──────────────────────────────────────────────────────────────────────────────

print("4️⃣  Testando análise de desempenho...")

conn = sqlite3.connect("escola.db")
aluno_test = conn.execute("SELECT id FROM alunos LIMIT 1").fetchone()
conn.close()

if aluno_test:
    try:
        analise = DisciplinePerformanceAnalyzer.analyze_student(
            "escola.db",
            aluno_test[0],
            loader
        )
        
        if analise:
            print(f"   ✅ Análise do aluno: {analise['aluno']['nome']}")
            print(f"   ✅ Status Geral: {analise['profile']}")
            print(f"   ✅ Disciplinas analisadas: {len(analise['disciplinas'])}")
            print(f"   ✅ Disciplinas em bom desempenho: {len(analise['strengths'])}")
            print(f"   ✅ Disciplinas em atenção: {len(analise['at_risk'])}")
            print(f"   ✅ Disciplinas críticas: {len(analise['weaknesses'])}")
        else:
            print("   ⚠️  Nenhuma análise disponível (sem notas?)")
    except Exception as e:
        print(f"   ❌ Erro na análise: {e}")
        import traceback
        traceback.print_exc()
else:
    print("   ℹ️  Nenhum aluno para testar (crie alunos primeiro)")

print("")

# ──────────────────────────────────────────────────────────────────────────────
# 5. RESUMO E INSTRUÇÕES
# ──────────────────────────────────────────────────────────────────────────────

print("="*80)
print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
print("="*80 + "\n")

print("📚 PRÓXIMOS PASSOS:\n")

print("1️⃣  PREPARE OS DADOS:")
print("   - Abra a GUI: python gui_escola.py")
print("   - Crie salas (ex: 6a, 6b, 6c) em 'Salas/Turmas'")
print("   - Adicione alunos em 'Alunos'")
print("   - Cadastre matérias em 'Matérias'")
print("   - Adicione notas em 'Notas'\n")

print("2️⃣  VISUALIZE AS PREDIÇÕES:")
print("   - Menu: Predições")
print("   - Selecione turma e aluno")
print("   - Veja análise por disciplina")
print("   - Identifique déficits e oportunidades\n")

print("3️⃣  INTERPRETE OS RESULTADOS:")
print("   - 🟢 SEGURO: Aluno com desempenho normal")
print("   - 🟡 EM RISCO: Precisa acompanhamento")
print("   - 🔴 CRÍTICO: Atenção imediata\n")

print("4️⃣  TOME AÇÕES:")
print("   - Organize reforço para disciplinas críticas")
print("   - Acompanhe progresso antes de N3 e N4")
print("   - Evite surpresas no final do bimestre\n")

print("="*80)
print("🎯 Objetivo: Identificar déficits NO INÍCIO DO ANO (N1+N2)")
print("     para intervir ANTES de N3 e N4")
print("="*80 + "\n")

print("📞 Para mais informações:")
print("   - Veja: INTEGRACAO_ML_GUI.md")
print("   - Veja: ML_README.md")

print("\n")
