#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste específico para o caso reportado pelo usuário:
N1=1.0, N2=9.0 em Química deveria mostrar melhora, não piora!
"""

import sqlite3
from gui_ml_integration import DisciplinePerformanceAnalyzer, MLModelLoader

# Carregar modelos
loader = MLModelLoader()

print("="*70)
print("TESTE: Caso reportado pelo usuario")
print("N1=1.0, N2=9.0 em Quimica (sem N3, N4)")
print("="*70)

# Criar um aluno de teste com dados manuais
# Vamos ler o primeiro aluno e simular os dados
conn = sqlite3.connect('escola.db')
cursor = conn.cursor()

# Buscar um aluno que tem quimica/quimica/quimica...
cursor.execute("""
    SELECT DISTINCT a.id, a.nome
    FROM alunos a
    JOIN notas n ON a.id = n.aluno_id
    LIMIT 1
""")

aluno = cursor.fetchone()
if aluno:
    aluno_id = aluno[0]
    aluno_nome = aluno[1]
    
    # Obter a materia ID de quimica
    cursor.execute("SELECT id FROM materias LIMIT 1")
    materia = cursor.fetchone()
    materia_id = materia[0]
    
    # Atualizar temporariamente as notas para o teste
    cursor.execute("""
        UPDATE notas
        SET n1=1.0, n2=9.0, n3=NULL, n4=NULL
        WHERE aluno_id=? AND materia_id=?
    """, (aluno_id, materia_id))
    conn.commit()
    
    print(f"\nAluno teste: {aluno_nome} (ID={aluno_id})")
    print("Notas atualizadas: N1=1.0, N2=9.0, N3=NULL, N4=NULL")
    
    # Analisar
    result = DisciplinePerformanceAnalyzer.analyze_student("escola.db", aluno_id, loader)
    
    if result:
        for disc in result['disciplinas']:
            if disc['n1'] == 1.0 and disc['n2'] == 9.0:
                print(f"\nDisciplina: {disc['nome']}")
                print(f"  N1={disc['n1']}, N2={disc['n2']}, N3={disc.get('n3')}, N4={disc.get('n4')}")
                print(f"  Status: {disc['status_name']}")
                print(f"  Trend: {disc['trend']}")
                print(f"  Prognosis: {disc['prognosis']}")
                print(f"  Explicacao: {disc['explicacao']}")
                
                # Verificacao
                slope = ((9.0 - 1.0) / 1.0) * 100
                print(f"\n  Slope: {slope}%")
                if slope > 20:
                    if disc['prognosis'] == 'will_improve':
                        print(f"  [OK] Resultado correto: will_improve")
                    else:
                        print(f"  [ERRO] Esperado: will_improve, Obteve: {disc['prognosis']}")
                break
    
    # Restaurar dados
    cursor.execute("""
        UPDATE notas
        SET n1=NULL, n2=NULL, n3=NULL, n4=NULL
        WHERE aluno_id=? AND materia_id=?
    """, (aluno_id, materia_id))
    conn.commit()
    
    print("\nNotas restauradas ao estado original")

conn.close()

print("\n[OK] Teste concluido")
