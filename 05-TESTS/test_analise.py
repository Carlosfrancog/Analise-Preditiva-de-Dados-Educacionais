#!/usr/bin/env python3
"""Teste específico da análise de desempenho"""
import cads
from gui_ml_integration import DisciplinePerformanceAnalyzer, load_ml_models

# Carrega os modelos
model_loader = load_ml_models()

# Busca um aluno com muitas notas
alunos = cads.get_alunos()
if not alunos:
    print("❌ Nenhum aluno encontrado")
    exit(1)

# Pega o primeiro aluno
aluno = alunos[0]
aluno_id = aluno['id']

print(f"\n{'='*80}")
print(f"🧪 TESTE DE ANÁLISE PREDITIVA")
print(f"{'='*80}\n")

print(f"Aluno: {aluno['nome']} (ID: {aluno_id})")
print(f"Matrícula: {aluno['matricula']}\n")

# Analisa o aluno
try:
    analise = DisciplinePerformanceAnalyzer.analyze_student(
        aluno_id, 
        model_loader=model_loader
    )
    
    if not analise:
        print("❌ Análise retornou None")
        exit(1)
    
    print(f"STATUS GERAL: {analise['profile']}\n")
    
    print(f"Disciplinas analisadas: {len(analise['disciplinas'])}")
    print(f"  ✅ Bem: {len(analise['strengths'])} ({', '.join(analise['strengths'][:3])}...)")
    print(f"  ⚠️  Atenção: {len(analise['at_risk'])} ({', '.join(analise['at_risk'])})")
    print(f"  ❌ Crítico: {len(analise['weaknesses'])} ({', '.join(analise['weaknesses'][:3])}...)\n")
    
    # Mostra detalhes de cada disciplina
    print("DETALHES POR DISCIPLINA:")
    print("-" * 80)
    for disc in analise['disciplinas'][:5]:  # primeiras 5
        print(f"  {disc['emoji']} {disc['nome']:<20} | ", end="")
        print(f"N1={disc['n1']:.1f if disc['n1'] else 0:<4} ", end="")
        print(f"N2={disc['n2']:.1f if disc['n2'] else 0:<4} ", end="")
        print(f"Média={disc['media']:.1f if disc['media'] else 0:<5} ", end="")
        print(f"Risk={disc['risk_score']:.2f}")
    
    print(f"\n{'='*80}")
    print("✅ ANÁLISE COMPLETA COM SUCESSO!")
    print(f"{'='*80}")
    
except Exception as e:
    print(f"❌ Erro na análise: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
