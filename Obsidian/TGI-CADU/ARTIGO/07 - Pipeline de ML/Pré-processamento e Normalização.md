---
tags: [artigo, pipeline, preprocessamento, normalizacao, dados]
aliases: [Pré-processamento dos Dados, Pré-processamento e Normalização]
created: 2026-05-16
---

# Pré-processamento e Normalização dos Dados

[← Índice](<../INDEX - ARTIGO.md>) | [[Pipeline Completo de Treinamento]] | [[Visão Geral das 9 Features]] | [[Data Leakage — Conceito e Impacto]]

---

## 1. Pipeline de Pré-processamento

O EduPredict usa normalização manual (sem `sklearn.preprocessing`) aplicada dentro de `cads.gerar_features_ml()`:

```
Dados brutos (tabela notas)
    ↓
Cálculo de features por (aluno, matéria)
    ↓
Normalização por domínio:
  - notas: /10       → [0,1]
  - série: /6        → [0,1]
  - slope: min-max   → calculado via _slope()
  - std: range-based → calculado via _std()
    ↓
Armazenamento em tabela ml_features
    ↓
Exportação para ml_dataset.csv
    ↓
Remoção de features leaky (detect_leakage)
    ↓
Treinamento do modelo
```

---

## 2. Normalização por Feature

| Feature | Pré-processamento | Fórmula |
|---|---|---|
| `n1_norm`, `n2_norm`, `n3_norm` | Escala fixo | `nota / 10.0` |
| `n4_norm` *(removida)* | Escala fixo | `nota / 10.0` |
| `media_pond_norm` *(removida)* | Escala fixo | `media / 10.0` |
| `slope_notas` | Regressão linear normalizada | `cads._slope([n1, n2, n3])` |
| `variancia_notas` | Desvio padrão normalizado | `cads._std([n1, n2, n3])` |
| `media_geral_aluno` | Escala fixo | `media_cross_matérias / 10.0` |
| `pct_materias_ok` | Proporção natural | `n_aprovadas / n_total` |
| `media_turma_norm` | Escala fixo | `media_turma / 10.0` |
| `serie_num_norm` | Ordinal | `indice_serie / 6.0` |

---

## 3. Tratamento de Valores Ausentes

```python
# cads.py — gerar_features_ml()
n1 = row['n1'] or 0   # NULL → 0
n2 = row['n2'] or 0   # NULL → 0
n3 = row['n3'] or 0   # NULL → 0
# n4 ignorado (feature removida)

n1_norm = n1 / 10.0
n2_norm = n2 / 10.0
n3_norm = n3 / 10.0
```

**Problema:** `0` para nota ausente vs `0` para nota zero são indistinguíveis. Uma flag binária `n3_disponivel` seria mais informativa:

```python
# Alternativa mais informativa:
n3_disponivel = 1 if row['n3'] is not None else 0
n3_norm = (row['n3'] or 0) / 10.0
```

---

## 4. slope_notas — Implementação Real

```python
# cads.py — _slope()
def _slope(vals):
    """Regressão linear nos valores não-zero."""
    vals = [v for v in vals if v > 0]
    if len(vals) < 2:
        return 0.0
    x = list(range(len(vals)))
    n = len(vals)
    sx = sum(x); sy = sum(vals)
    sxy = sum(xi * yi for xi, yi in zip(x, vals))
    sx2 = sum(xi**2 for xi in x)
    denom = n * sx2 - sx**2
    if denom == 0:
        return 0.0
    slope = (n * sxy - sx * sy) / denom
    # Normalização: dividir por 10 (range máximo de nota)
    return slope / 10.0
```

`_slope()` retorna o coeficiente angular da regressão linear sobre as notas não-zero, normalizado. Valores positivos indicam tendência de melhora; negativos, queda.

---

## 5. variancia_notas — Implementação Real

```python
# cads.py — _std()
def _std(vals):
    """Desvio padrão normalizado dos valores não-zero."""
    vals = [v for v in vals if v > 0]
    if len(vals) < 2:
        return 0.0
    media = sum(vals) / len(vals)
    variancia = sum((v - media)**2 for v in vals) / len(vals)
    std = variancia ** 0.5
    return std / 10.0  # normalizar pelo range
```

O nome da feature é `variancia_notas` mas o cálculo é o **desvio padrão** (raiz da variância), normalizado por 10.

---

## 6. Ausência de StandardScaler/MinMaxScaler

O EduPredict não usa `sklearn.preprocessing` — toda normalização é feita manualmente. Isso é compatível com o Random Forest (RF não é sensível à escala), mas criaria problema com SVM ou redes neurais.

**Vantagem:** As features têm semântica clara ([0,1]) sem precisar de estatísticas de treino.
**Desvantagem:** Se uma nota vier fora do range [0,10], a normalização /10 pode produzir valores >1 ou <0.

---

## Links

- [[Pipeline Completo de Treinamento]]
- [[Visão Geral das 9 Features]]
- [[slope notas — Tendência Temporal]]
- [[variancia notas — Consistência]]
- [[Data Leakage — Conceito e Impacto]]
- [[cads.py — Análise Profunda]]
