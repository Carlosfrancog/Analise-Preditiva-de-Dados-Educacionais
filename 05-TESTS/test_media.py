#!/usr/bin/env python3
"""Teste simples de análise"""
import cads
import sqlite3

conn = sqlite3.connect("escola.db")
conn.row_factory = sqlite3.Row

# Busca primeiro aluno
aluno = conn.execute("SELECT id, nome FROM alunos LIMIT 1").fetchone()
print(f"Aluno: {aluno['nome']}")

# Busca uma disciplina com notas
nota = conn.execute("""
    SELECT a.nome, m.nome as materia, n.n1, n.n2, n.n3, n.n4
    FROM notas n
    JOIN alunos a ON a.id = n.aluno_id
    JOIN materias m ON m.id = n.materia_id
    WHERE a.id = ? AND (n.n1 IS NOT NULL OR n.n2 IS NOT NULL)
    LIMIT 1
""", (aluno['id'],)).fetchone()

if nota:
    print(f"Matéria: {nota['materia']}")
    print(f"N1={nota['n1']}, N2={nota['n2']}, N3={nota['n3']}, N4={nota['n4']}")
    
    # Simula cálculo de média
    notas_list = []
    pesos = []
    
    if nota['n1']:
        notas_list.append(nota['n1'])
        pesos.append(0.2)
    if nota['n2']:
        notas_list.append(nota['n2'])
        pesos.append(0.25)
    if nota['n3']:
        notas_list.append(nota['n3'])
        pesos.append(0.25)
    if nota['n4']:
        notas_list.append(nota['n4'])
        pesos.append(0.30)
    
    soma_pesos = sum(pesos)
    pesos_norm = [p / soma_pesos for p in pesos]
    
    media = sum(n * p for n, p in zip(notas_list, pesos_norm))
    print(f"Média calculada: {media:.2f}")
    
    # Status
    if media < 5:
        status = "❌ REPROVADO"
    elif media < 6:
        status = "⚠️ RECUPERAÇÃO"
    else:
        status = "✅ APROVADO"
    
    print(f"Status: {status}")
else:
    print("Sem notas encontradas")

conn.close()
