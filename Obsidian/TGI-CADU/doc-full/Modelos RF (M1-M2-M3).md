---
tags:
  - ml
  - modelos
  - tgi-codes
created: 2026-05-13
---

# Modelos Random Forest — M1, M2 e M3

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## Comparação dos Modelos

| Atributo | RF_M1 | RF_M2 | RF_M3 ⭐ |
|---|---|---|---|
| **Quando usar** | Após N1 | Após N2 | Após N3 |
| **Nº de features** | 1 | 4 | 9 |
| **Acurácia** | ~55–60% | ~65–75% | ~80–94% |
| **Árvores** | 100 | 150 | 200 |
| **Max depth** | 5 | 10 | sem limite |
| **Uso recomendado** | Alerta inicial | Intervenção | Referência final |

> [!TIP] Qual modelo usar?
> Use **RF_M3** para produção — maior acurácia. Use **RF_M2** se precisar prever antes de N3.

---

## RF_M1 — Predição Muito Antecipada

**Features:** `n1_norm` (apenas a primeira nota)

Útil para identificar alunos que já começaram mal logo no primeiro bimestre. Acurácia baixa pois há poucos dados disponíveis.

```python
# Localização do modelo
ml_models/RF_M1.pkl
ml_models/RF_M1_metadata.json
```

---

## RF_M2 — Predição Intermediária

**Features:** `n1_norm`, `n2_norm`, `slope_notas`, `variancia_notas`

O ponto ideal para **intervenção pedagógica**: já temos duas notas e a tendência de evolução do aluno.

```python
# Localização do modelo
ml_models/RF_M2.pkl
ml_models/RF_M2_metadata.json
```

---

## RF_M3 — Predição Robusta (Recomendado)

**Features (9):**
1. `n1_norm` — Primeira nota normalizada
2. `n2_norm` — Segunda nota normalizada
3. `n3_norm` — Terceira nota normalizada
4. `slope_notas` — Tendência de evolução
5. `variancia_notas` — Consistência das notas
6. `media_geral_aluno` — Contexto: desempenho geral do aluno
7. `serie_num_norm` — Série/ano escolar normalizado
8. `pct_materias_ok` — % de matérias que o aluno está aprovado
9. `media_turma_norm` — Contexto: nível da turma

```python
# Usar em produção
from ml_pipeline import predict_student_status

prediction, error = predict_student_status(
    model_dir="ml_models/RF_M3...",
    aluno_id=1,
    materia_id=2
)
print(prediction['predicted_label'])   # "Aprovado"
print(f"{prediction['confidence']:.1%}")  # "87.0%"
```

---

## Feature Importance (RF_M3)

Contribuição aproximada de cada feature para as decisões do modelo:

```
n2_norm              ████████░  32.3%
pct_materias_ok      █████░░    21.4%
media_geral_aluno    ████░░     18.7%
slope_notas          ███░       12.3%
n3_norm              ██░         8.1%
n1_norm              █░          4.6%
variancia_notas      █░          2.6%
```

---

## Arquivos no Disco

```
02-ML/ml_models/
├── RF_M1.pkl
├── RF_M1_metadata.json
├── RF_M2.pkl
├── RF_M2_metadata.json
├── RF_M3.pkl           ← usar este em produção
├── RF_M3_metadata.json
└── training_summary.json
```

---

## Links Relacionados

- [[Features e Cálculos]] — o que cada feature significa
- [[Data Leakage]] — por que n4_norm foi excluída do treino
- [[Pipeline de Treinamento]] — como o treino é executado
- [[Visão Geral ML]] — contexto geral do sistema de ML
