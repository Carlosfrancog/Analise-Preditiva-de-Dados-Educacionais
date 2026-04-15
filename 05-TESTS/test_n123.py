#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste para entender como os dados N1=1, N2=9, N3=7.5 sao analisados
"""

import sqlite3
from gui_ml_integration import DisciplinePerformanceAnalyzer, MLModelLoader

# Carregar modelos
loader = MLModelLoader()

print("="*70)
print("TESTE: N1=1, N2=9, N3=7.5 (sem N4)")
print("="*70)

conn = sqlite3.connect('escola.db')
cursor = conn.cursor()

# Buscar um aluno
cursor.execute("SELECT DISTINCT a.id, a.nome FROM alunos a LIMIT 1")
aluno = cursor.fetchone()

if aluno:
    aluno_id = aluno[0]
    aluno_nome = aluno[1]
    
    # Obter a materia ID
    cursor.execute("SELECT id FROM materias LIMIT 1")
    materia_id = cursor.fetchone()[0]
    
    # Atualizar com N1=1, N2=9, N3=7.5, N4=NULL
    cursor.execute("""
        UPDATE notas
        SET n1=1.0, n2=9.0, n3=7.5, n4=NULL
        WHERE aluno_id=? AND materia_id=?
    """, (aluno_id, materia_id))
    conn.commit()
    
    print(f"\nAluno: {aluno_nome}")
    print("Notas: N1=1.0, N2=9.0, N3=7.5, N4=NULL")
    
    # Analisar
    result = DisciplinePerformanceAnalyzer.analyze_student("escola.db", aluno_id, loader)
    
    if result:
        for disc in result['disciplinas']:
            if disc['n1'] == 1.0 and disc['n2'] == 9.0 and disc['n3'] == 7.5:
                print(f"\nDisciplina: {disc['nome']}")
                print(f"  N1={disc['n1']}, N2={disc['n2']}, N3={disc['n3']}, N4={disc.get('n4')}")
                print(f"\n  ANALISE DO MODELO:")
                print(f"  - Status calc (media de N1+N2/N3+N4): {disc['status_name']}")
                print(f"  - Predicted Status (baseado em N1+N2): {disc.get('predicted_status', 'N/A')}")
                print(f"  - Proba: {disc.get('predicted_proba', 'N/A')}")
                print(f"\n  INTERPRETACAO:")
                print(f"  - Trend: {disc['trend']}")
                print(f"  - Prognosis: {disc['prognosis']}")
                print(f"  - Explicacao: {disc['explicacao']}")
                
                # Calculos manuais
                print(f"\n  CALCULOS MANUAIS:")
                
                # Media N1+N2
                media_n12 = (1.0 + 9.0) / 2
                print(f"  - Media N1+N2: {media_n12}")
                
                # Media N3
                media_n3 = 7.5
                print(f"  - Media N3: {media_n3}")
                
                # Slope N1->N2
                slope_n12 = ((9.0 - 1.0) / 1.0) * 100
                print(f"  - Slope N1->N2: {slope_n12}%")
                
                # Variancia N1 vs N2
                var_n12 = abs(1.0 - 9.0)
                print(f"  - Variancia |N1-N2|: {var_n12}")
                
                # Comparacao: N1+N2 (5.0) vs N3 (7.5)
                status_n12 = 0 if media_n12 < 5 else (1 if media_n12 < 6 else 2)
                status_n3 = 0 if media_n3 < 5 else (1 if media_n3 < 6 else 2)
                
                print(f"\n  STATUS:")
                print(f"  - Status N1+N2 (media={media_n12}): {status_n12}")
                print(f"  - Status N3 (media={media_n3}): {status_n3}")
                
                if status_n12 < status_n3:
                    print(f"  - Resultado: MELHORA real (predicao {status_n12} < realidade {status_n3})")
                elif status_n12 > status_n3:
                    print(f"  - Resultado: PIORA real (predicao {status_n12} > realidade {status_n3})")
                else:
                    print(f"  - Resultado: CONFIRMOU predicao (predicao {status_n12} = realidade {status_n3})")
                
                break
    
    # Restaurar
    cursor.execute("""
        UPDATE notas
        SET n1=NULL, n2=NULL, n3=NULL, n4=NULL
        WHERE aluno_id=? AND materia_id=?
    """, (aluno_id, materia_id))
    conn.commit()

conn.close()

print("\n[OK] Teste concluido")
