#!/usr/bin/env python3
"""Debug com múltiplas disciplinas"""
import cads
from gui_ml_integration import load_ml_models

ml = load_ml_models()

# Busca aluno
alunos = cads.get_alunos()
aluno = alunos[0]
aluno_id = aluno['id']

print(f"Aluno: {aluno['nome']}\n")
print(f"{'Matéria':<20} {'N1':<5} {'N2':<5} {'N3':<5} {'N4':<5} {'Pred':<6} {'Atual':<6} {'Resultado':<20}")
print("-" * 90)

# Busca TODAS as disciplinas
import sqlite3
conn = sqlite3.connect("escola.db")
conn.row_factory = sqlite3.Row

notas_list = conn.execute("""
    SELECT m.nome, n.n1, n.n2, n.n3, n.n4
    FROM notas n
    JOIN materias m ON m.id = n.materia_id
    WHERE n.aluno_id = ?
    ORDER BY m.nome
    LIMIT 10
""", (aluno_id,)).fetchall()

for nota in notas_list:
    # Normaliza
    n1 = nota['n1'] / 10 if nota['n1'] else 0
    n2 = nota['n2'] / 10 if nota['n2'] else 0
    n3 = nota['n3'] / 10 if nota['n3'] else 0
    n4 = nota['n4'] / 10 if nota['n4'] else 0
    
    # Features
    slope = (n2 - n1) if (nota['n1'] and nota['n2']) else 0
    media_n12 = (nota['n1'] + nota['n2']) / 2 if (nota['n1'] and nota['n2']) else (nota['n1'] or nota['n2'] or 0)
    variancia = abs(n1 - n2) if (nota['n1'] and nota['n2']) else 0
    media_norm = media_n12 / 10
    
    features = [n1, n2, 0, 0, slope, variancia, media_norm, 0.5, 0.5]
    
    # Predição
    pred, proba = ml.predict("RF_M3", features)
    pred = int(pred) if pred is not None else -1
    
    # Status atual N1+N2
    if media_n12 < 5:
        status_atual = 0
    elif media_n12 < 6:
        status_atual = 1
    else:
        status_atual = 2
    
    # Resultado
    if pred > status_atual:
        resultado = "✨ Vai MELHORAR"
    elif pred < status_atual:
        resultado = "⚠️ Vai PIORAR"
    else:
        resultado = "→ Mantém"
    
    status_names = {0: "❌", 1: "⚠️", 2: "✅"}
    
    print(f"{nota['nome']:<20} {nota['n1']:<5.0f} {nota['n2']:<5.0f} {nota['n3'] if nota['n3'] else '-':<5} {nota['n4'] if nota['n4'] else '-':<5} {status_names.get(pred, '?'):<6} {status_names.get(status_atual, '?'):<6} {resultado:<20}")

conn.close()
