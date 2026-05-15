#!/usr/bin/env python3
"""Teste de análise com prognóstico"""
import cads
from gui_ml_integration import DisciplinePerformanceAnalyzer, load_ml_models

# Carrega modelos
ml = load_ml_models()

# Busca um aluno
alunos = cads.get_alunos()
if not alunos:
    print("❌ Sem alunos")
    exit(1)

aluno = alunos[0]
print(f"\n{'='*70}")
print(f"ANÁLISE COM PROGNÓSTICO: {aluno['nome']}")
print(f"{'='*70}\n")

# Analisa
analise = DisciplinePerformanceAnalyzer.analyze_student(
    "escola.db",
    aluno['id'], 
    model_loader=ml
)

if not analise:
    print("❌ Análise falhou")
    exit(1)

print(f"STATUS GERAL: {analise['profile']}\n")

# Mostra 5 disciplinas com detalhes
print(f"{'Disciplina':<20} {'Notas':<18} {'Média':<6} {'Status':<12} {'Prognóstico':<35}")
print("-" * 100)

for disc in analise['disciplinas'][:8]:
    nome = disc['nome'][:18]
    n1 = f"N1={disc['n1']:.0f}" if disc['n1'] else "—"
    n2 = f" N2={disc['n2']:.0f}" if disc['n2'] else ""
    notas_str = f"{n1}{n2}".ljust(18)
    
    media = f"{disc['media']:.1f}".ljust(5)
    status = disc['emoji']
    status_str = f"{status} {disc['status_name']}".ljust(12)
    
    trend = disc.get('trend', '→')
    prognosis_map = {
        "will_decline": "⚠️ Vai PIORAR",
        "will_improve": "✨ Vai MELHORAR",
        "stable": "→ Mantém nível",
        "worse_than_expected": "📉 Piorou",
        "better_than_expected": "📈 Melhorou",
        "as_expected": "→ Normal",
        "normal": "→ Normal"
    }
    prognosis = prognosis_map.get(disc.get('prognosis'), '?')
    prognosis_str = f"{trend} {prognosis}".ljust(35)
    
    print(f"{nome:<20} {notas_str:<18} {media:<6} {status_str:<12} {prognosis_str:<35}")

print(f"\n{'='*70}")
print("✅ ANÁLISE CONCLUÍDA")
print(f"{'='*70}")
