---
tags: [artigo, metricas, acuracia, f1-score, avaliacao]
aliases: [Acurácia e F1-Score — Definição e Uso, Acurácia F1 e Métricas Gerais, Acurácia por Classe — Análise Crítica]
created: 2026-05-16
---

# Acurácia, F1-Score e Métricas de Avaliação

[← Índice](<../INDEX - ARTIGO.md>) | [[Resultados Gerais — M1 M2 M3]] | [[Matriz de Confusão M3 — Análise Detalhada]] | [[Divisão Treino-Teste e Cross-Validation]]

---

## 1. Métricas Usadas no EduPredict

```python
# train_simple.py
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

accuracy = accuracy_score(y_test, y_pred)
f1       = f1_score(y_test, y_pred, average='weighted')
cm       = confusion_matrix(y_test, y_pred)
```

---

## 2. Acurácia — Definição e Problema

**Fórmula:**
```
Acurácia = (TP + TN) / Total de Predições
```

**Resultados reportados:**
| Modelo | Acurácia |
|---|---|
| M1 | 83.8% |
| M2 | 92.5% |
| M3 | 94.0% |

**Problema fundamental:** Acurácia é enganosa em datasets desbalanceados.

No dataset sintético:
- Aprovado: ~65% das observações
- Recuperação: ~20%
- Reprovado: ~15%

Um modelo que prediz "Aprovado" para todos teria ~65% de acurácia **sem aprender nada**. A acurácia de 94% do M3 precisa ser interpretada com essa distribuição em mente.

---

## 3. F1-Score Weighted — Definição

**F1 por classe:**
```
F1_classe = 2 × (Precision × Recall) / (Precision + Recall)

Precision = TP / (TP + FP)  → de todos que previ como X, quantos eram X?
Recall    = TP / (TP + FN)  → de todos que eram X, quantos previ corretamente?
```

**F1 Weighted:** média dos F1 por classe, ponderada pelo número de amostras em cada classe:
```
F1_weighted = Σ(F1_i × n_i) / Σ(n_i)
```

**Problema do weighted para EWS (Early Warning Systems):**

O F1 weighted dá **mais peso às classes mais frequentes** (Aprovado). Para um sistema de alerta precoce, o que importa é a capacidade de detectar **Recuperação e Reprovado** — as classes minoritárias.

**Métrica mais adequada:** F1 Macro ou Recall específico para Recuperação+Reprovado.

---

## 4. Resultados Reais por Classe (M3)

```
                Precision   Recall   F1-score
Reprovado           0.96     0.89      0.92
Recuperação         0.78     0.62      0.69   ← ponto fraco
Aprovado            0.97     0.98      0.97

Weighted avg:       0.94     0.94      0.94
```

O F1 weighted de 0.94 esconde que **Recuperação tem F1=0.69** — o caso mais crítico para intervenção pedagógica.

---

## 5. Por Que Recuperação É Tão Difícil

1. **Fronteiras naturalmente ambíguas:** média 5.0-6.0 é limiar estreito
2. **Alta variância de N1→N4:** alunos em recuperação têm trajetórias erráticas
3. **Classe minoritária:** menos exemplos de treinamento
4. **Viés do modelo:** `class_weight='balanced'` ajuda, mas Recuperação é "entre" Reprovado e Aprovado

Ver detalhes: [[Matriz de Confusão M3 — Análise Detalhada]]

---

## 6. Métricas Alternativas Recomendadas

| Métrica | Fórmula | Uso recomendado |
|---|---|---|
| **Recall de Risco** | Recall(Reprovado + Recuperação) | Principal métrica para EWS |
| **F1 Macro** | Média simples de F1 por classe | Trata classes igualmente |
| **AUC-ROC** | Área sob curva ROC | Threshold-independent |
| **Cohen's Kappa** | Acurácia ajustada pelo acaso | Compara modelos em classes desbalanceadas |

Para o artigo, reportar F1 weighted junto com Recall de Recuperação daria avaliação mais honesta.

---

## 7. Inflação de Métricas — DT-04

A acurácia e F1 reportados podem estar **inflados artificialmente** pelo débito técnico DT-04:

```python
# O que o código faz (ERRADO para EWS):
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
# Mesmo aluno pode aparecer em treino E teste

# O correto seria:
from sklearn.model_selection import GroupKFold
cv = GroupKFold(n_splits=5)
cross_val_score(clf, X, y, cv=cv, groups=df['aluno_id'])
```

O modelo memoriza padrões do **mesmo aluno** em treino e os "reconhece" em teste — inflando a acurácia real de generalização para novos alunos.

Ver: [[Divisão Treino-Teste e Cross-Validation]] | [[Débitos Técnicos Identificados]]

---

## Links

- [[Resultados Gerais — M1 M2 M3]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
- [[Divisão Treino-Teste e Cross-Validation]]
- [[Débitos Técnicos Identificados]]
- [[class weight balanced — Tratamento de Desbalanceamento]]
- [[Análise Crítica do TGI]]
