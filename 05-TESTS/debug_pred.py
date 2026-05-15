#!/usr/bin/env python3
"""Debug de predicción"""
import cads
from gui_ml_integration import load_ml_models

ml = load_ml_models()

# Busca aluno
alunos = cads.get_alunos()
aluno = alunos[0]
aluno_id = aluno['id']

print(f"Aluno: {aluno['nome']}\n")

# Busca uma disciplina com N1 e N2
import sqlite3
conn = sqlite3.connect("escola.db")
conn.row_factory = sqlite3.Row

nota = conn.execute("""
    SELECT m.nome, n.n1, n.n2, n.n3, n.n4
    FROM notas n
    JOIN materias m ON m.id = n.materia_id
    WHERE n.aluno_id = ? AND n.n1 IS NOT NULL AND n.n2 IS NOT NULL
    LIMIT 1
""", (aluno_id,)).fetchone()

if nota:
    print(f"Matéria: {nota['nome']}")
    print(f"N1={nota['n1']}, N2={nota['n2']}, N3={nota['n3']}, N4={nota['n4']}\n")
    
    # Normaliza para model
    n1 = nota['n1'] / 10
    n2 = nota['n2'] / 10
    n3 = (nota['n3'] / 10) if nota['n3'] else 0
    n4 = (nota['n4'] / 10) if nota['n4'] else 0
    
    # Calcular features
    slope = (n2 - n1) if nota['n2'] > 0 else 0
    media_atual = (nota['n1'] + nota['n2']) / 2
    variancia = abs(n1 - n2)
    media_norm = media_atual / 10
    
    # Features APENAS com N1+N2 (N3 e N4 zerados)
    features = [n1, n2, 0, 0, slope, variancia, media_norm, 0.5, 0.5]
    
    print(f"Features para modelo (com N3=0, N4=0): {features}")
    print(f"Soma dos features: {sum([abs(f) for f in features])}")
    
    # Prediz
    pred, proba = ml.predict("RF_M3", features)
    
    print(f"\nPREDIÇÃO DO MODELO:")
    print(f"  Status predito: {pred}")
    print(f"  Probabilidades: {proba}")
    
    # Comparação
    status_map = {0: "Reprovado", 1: "Recuperação", 2: "Aprovado"}
    print(f"\n  Interpretação: {status_map.get(int(pred), '?')}")
    
    # Status atual apenas com N1+N2
    media_n12 = (nota['n1'] + nota['n2']) / 2
    if media_n12 < 5:
        status_atual = 0
    elif media_n12 < 6:
        status_atual = 1
    else:
        status_atual = 2
    
    print(f"\nSTATUS ATUAL (N1+N2):")
    print(f"  Média: {media_n12:.1f}")
    print(f"  Status: {status_map.get(status_atual, '?')}")
    
    print(f"\nCOMPARAÇÃO:")
    print(f"  Predito ({int(pred)}) vs Atual ({status_atual})")
    
    if int(pred) < status_atual:
        print(f"  → Vai PIORAR (⚠️)")
    elif int(pred) > status_atual:
        print(f"  → Vai MELHORAR (✨)")
    else:
        print(f"  → Mantém (→)")
else:
    print("Sem notas encontradas")

conn.close()
