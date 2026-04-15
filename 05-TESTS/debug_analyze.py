#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Debug script para entender por que o prognosis nao esta sendo setado."""

from gui_ml_integration import DisciplinePerformanceAnalyzer, MLModelLoader
import sqlite3

# Carregar modelos
loader = MLModelLoader()

# Analisar aluno 1
aluno_id = 1
result = DisciplinePerformanceAnalyzer.analyze_student("escola.db", aluno_id, loader)

if result:
    # Procurar pela disciplina Arte
    for disc in result['disciplinas']:
        if disc['nome'] == 'Arte':
            print("=== DEBUG: Analise de Arte ===")
            print(f"  N1={disc['n1']}, N2={disc['n2']}, N3={disc['n3']}, N4={disc['n4']}")
            print(f"  Media: {disc['media']}")
            print(f"  Status: {disc['status']} ({disc['status_name']})")
            print(f"  Predicted Status: {disc.get('predicted_status', 'N/A')}")
            print(f"  Trend: {disc['trend']}")
            print(f"  Prognosis: {disc['prognosis']}")
            print(f"  Explicacao: {disc['explicacao']}")
            print()
            
            # Verificar manualmente
            n1 = disc['n1']
            n2 = disc['n2']
            n3 = disc['n3']
            n4 = disc['n4']
            
            if n1 and n2:
                slope_pct = ((n2 - n1) / n1) * 100
                print(f"  Slope calculado: {slope_pct}%")
                print(f"  N3 e N4 preenchidos? N3={n3 is not None and n3 > 0}, N4={n4 is not None and n4 > 0}")
                
                if n3 or n4:
                    print("  -> Tem N3 ou N4, so deveria usar logica de comparacao com realidade")
                else:
                    print("  -> Nao tem N3 ou N4, deveria usar logica de slope")
                    if slope_pct > 20:
                        print(f"     Esperado: will_improve (slope {slope_pct} > 20)")
                    elif slope_pct < -20:
                        print(f"     Esperado: will_decline (slope {slope_pct} < -20)")
                    else:
                        print(f"     Esperado: stable ou prognosis do modelo")

print("\n[OK] Debug concluido")
