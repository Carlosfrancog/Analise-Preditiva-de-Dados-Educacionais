---
tags: [artigo, random-forest, hiperparametros, configuracao, sklearn]
aliases: [Hiperparâmetros e Configuração, Hiperparâmetros do Random Forest]
created: 2026-05-16
---

# Hiperparâmetros do Random Forest — EduPredict

[← Índice](<../INDEX - ARTIGO.md>) | [[Random Forest — Algoritmo e Justificativa]] | [[Comparação M1 M2 M3]] | [[train simple py — Pipeline Autônomo]]

---

## 1. Configuração Real dos Três Modelos

```python
# train_simple.py — código real
from sklearn.ensemble import RandomForestClassifier

modelos = {
    'RF_M1': RandomForestClassifier(
        n_estimators=100,
        max_depth=5,         # árvores rasas — regularização forte
        random_state=42
        # class_weight não especificado → usa 'None' (uniforme)
    ),
    'RF_M2': RandomForestClassifier(
        n_estimators=150,
        max_depth=10,        # profundidade intermediária
        random_state=42
    ),
    'RF_M3': RandomForestClassifier(
        n_estimators=200,
        # max_depth=None     # sem limite — árvores crescem até pureza
        random_state=42
    ),
}
```

> **Nota:** `class_weight='balanced'` aparece na documentação do artigo mas **não está explicitamente no código lido**. O comportamento padrão (`class_weight=None`) trata todas as classes igualmente. Verificar arquivo real.

---

## 2. Parâmetros Padrão do sklearn (Não Especificados)

Os parâmetros abaixo usam os defaults do sklearn — não foram otimizados:

| Parâmetro | Default sklearn | Impacto |
|---|---|---|
| `min_samples_split` | 2 | Mínimo de amostras para dividir um nó |
| `min_samples_leaf` | 1 | Mínimo de amostras em uma folha |
| `max_features` | `'sqrt'` | Features consideradas por split |
| `bootstrap` | `True` | Usa amostras com reposição |
| `criterion` | `'gini'` | Critério de impureza |
| `class_weight` | `None` | Sem pesos (ou verificar se balanced) |

---

## 3. Efeito de n_estimators

```
M1: 100 árvores  → mais rápido, menor variância que 1 árvore, mas menos estável que M3
M2: 150 árvores  → intermediário
M3: 200 árvores  → convergência melhor, ganho marginal vs M2 é pequeno

Regra geral: ganhos diminuem após ~100-200 árvores para datasets pequenos
```

Para 2600 amostras e 9 features, a diferença entre 100 e 200 árvores é mínima em acurácia — o ganho de M1 para M3 vem principalmente das **features adicionais** (n2, n3, pct_materias_ok), não do número de árvores.

---

## 4. Efeito de max_depth

| max_depth | Efeito | Trade-off |
|---|---|---|
| 5 (M1) | Regularização forte, árvores rasas | Underfitting possível, boa generalização |
| 10 (M2) | Profundidade moderada | Equilíbrio bias-variance |
| None (M3) | Árvores crescem até pureza | Risco de overfitting (mitigado pelo ensemble) |

**Para datasets sintéticos:** `max_depth=None` pode levar a memorização de ruído. Em dados reais com padrões menos previsíveis, a regularização via `max_depth` seria mais importante.

---

## 5. Ausência de Grid Search — Débito Técnico DT-06

Os hiperparâmetros foram escolhidos manualmente, sem busca sistemática:

```python
# O que deveria ser feito (não implementado):
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [3, 5, 10, None],
    'min_samples_leaf': [1, 2, 5],
    'class_weight': ['balanced', None]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=GroupKFold(n_splits=5),
    scoring='f1_macro',        # métrica mais adequada para EWS
    n_jobs=-1
)
grid_search.fit(X_train, y_train, groups=groups_train)
```

A escolha manual de `n_estimators ∈ {100, 150, 200}` e `max_depth ∈ {5, 10, None}` é intuitiva mas não justificada scientificamente.

---

## 6. random_state=42 — Reprodutibilidade

```python
random_state=42  # semente aleatória fixa para reprodutibilidade
```

Garante que os resultados são idênticos a cada execução. Importante para:
- Reprodutibilidade científica
- Debugging (mesmos resultados errados permitem comparação)

**Risco:** A escolha de `random_state=42` pode ter sido usada para selecionar o melhor resultado entre várias sementes (data snooping). O artigo não menciona se outras sementes foram testadas.

---

## 7. Comparação de Hiperparâmetros vs Acurácia

```
RF_M1: n=100, max_depth=5,    2 features → 83.8%
RF_M2: n=150, max_depth=10,   9 features → 92.5%
RF_M3: n=200, max_depth=None, 9 features → 94.0%

Diferença M2→M3: +1.5% com +50 árvores e profundidade irrestrita
→ ganho marginal: mais árvores contribuem pouco
→ principal diferença: features disponíveis (M1 tem apenas 2)
```

---

## Links

- [[Random Forest — Algoritmo e Justificativa]]
- [[Comparação M1 M2 M3]]
- [[train simple py — Pipeline Autônomo]]
- [[Débitos Técnicos Identificados]]
- [[class weight balanced — Tratamento de Desbalanceamento]]
- [[Acurácia F1 e Métricas Gerais]]
