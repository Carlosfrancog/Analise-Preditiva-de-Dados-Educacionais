---
tags: [artigo, feature-engineering, slope, tendencia, regressao-linear]
created: 2026-05-14
---

# slope_notas — Tendência Temporal das Notas

[[INDEX - ARTIGO|← Índice]] | [[Visão Geral das 9 Features]] | [[variancia notas — Consistência]] | [[pct materias ok — Aprovação Global]]

> [!NOTE] Importância no M3: 12,3% — 3ª feature mais importante

---

## 1. Definição Matemática

O `slope_notas` é calculado pela **regressão linear simples** sobre as notas disponíveis (N1, N2, N3, N4):

$$slope = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

Onde:
- $x_i$ = índice da avaliação (1, 2, 3 ou 4)
- $y_i$ = nota normalizada ($N_i / 10$)
- $\bar{x}$, $\bar{y}$ = médias dos índices e notas

**Implementação em `cads.py`:**
```python
def _slope(vals):
    """Regressão linear simples sobre lista de notas."""
    n = len(vals)
    if n < 2:
        return 0.0
    xs = list(range(n))
    xm = sum(xs) / n
    ym = sum(vals) / n
    num = sum((x - xm) * (y - ym) for x, y in zip(xs, vals))
    den = sum((x - xm) ** 2 for x in xs)
    return num / den if den != 0 else 0.0
```

---

## 2. Interpretação Pedagógica

| Valor do slope | Interpretação | Ação pedagógica |
|---|---|---|
| `slope > 0,15` | Aluno em clara melhora — cada bimestre vai melhor | Manutenção — motivar |
| `0,05 < slope ≤ 0,15` | Leve tendência de melhora | Acompanhamento leve |
| `-0,05 ≤ slope ≤ 0,05` | Estável — notas consistentes | Monitoramento padrão |
| `-0,15 ≤ slope < -0,05` | Leve declínio | Alerta informativo |
| `slope < -0,15` | Declínio acentuado — cada bimestre vai pior | 🔴 Intervenção urgente |

**Exemplo concreto:**
- Aluno A: N1=3,0, N2=5,0, N3=7,0 → slope ≈ +0,40 (forte melhora)
- Aluno B: N1=7,0, N2=6,0, N3=5,0 → slope ≈ -0,40 (forte queda)
- Ambos têm a mesma média (5,0), mas prognósticos opostos

---

## 3. Por Que Slope É Mais Informativo Que a Média

A média pontual captura onde o aluno está. O slope captura **para onde está indo**. Um aluno com média 5,0 e slope -0,40 tem perfil completamente diferente de um com média 5,0 e slope +0,40 — o modelo precisa distinguir esses casos.

Isso é corroborado pelo artigo: a importância do slope (12,3%) indica que a trajetória é informativa mesmo **após** controlar pela nota atual.

---

## 4. Limitações Técnicas

### Limitação 1 — Instabilidade com Poucos Pontos
Com apenas N1 e N2 (2 pontos), a regressão linear é determinística — qualquer par de pontos define exatamente uma reta. Isso significa que o slope com 2 pontos tem variância muito alta: um único outlier define a tendência inteira.

**Implicação:** o modelo M1 e M2 usam slope calculado com 1 e 2 pontos, respectivamente. A incerteza do slope nesses modelos é subestimada.

**Alternativa mais robusta:** EWMA (Exponential Weighted Moving Average) — dá mais peso às notas recentes e é menos sensível a outliers.

### Limitação 2 — Normalização do Slope

O slope calculado está em escala de notas normalizadas (0-1). Porém, o range teórico de slope é (-∞, +∞). Na prática, com notas entre 0-1 e índices 1-4, o slope está entre aproximadamente -0,5 e +0,5. Não é normalizado explicitamente para [-1, +1].

Isso pode criar problemas se notas em outras escalas forem usadas (ex: notas 0-100 sem normalização prévia).

---

## 5. Uso no `gui_ml_integration.py`

O slope é recalculado em tempo real na análise de predição para cada disciplina:

```python
# gui_ml_integration.py — DisciplinePerformanceAnalyzer
slope = (n2 - n1) if (n1_raw > 0 and n2_raw > 0) else 0
slope_pct = ((n2_raw - n1_raw) / n1_raw) * 100 if n1_raw > 0 else 0

if slope_pct > 20:
    disc_info["prognosis"] = "will_improve"
elif slope_pct < -20:
    disc_info["prognosis"] = "will_decline"
```

**Inconsistência crítica:** o código usa `slope_pct` (variação percentual N2→N1) em vez do slope de regressão linear do `cads.py`. São medidas diferentes! O slope percentual N2→N1 é menos robusto que a regressão linear sobre todos os pontos disponíveis.

Essa inconsistência significa que o **prognóstico exibido na interface pode divergir do que o modelo ML usa internamente.**

---

## 6. Refatoração Necessária

```python
# ATUAL (gui_ml_integration.py) — inconsistente
slope_pct = ((n2_raw - n1_raw) / n1_raw) * 100

# PROPOSTO — usar a mesma função de cads.py
from cads import _slope
notas_disponiveis = [n for n in [n1_raw, n2_raw, n3_raw, n4_raw] if n > 0]
slope_real = _slope([n/10 for n in notas_disponiveis])
# Usar slope_real para prognóstico e para features do modelo
```

Ver [[Débitos Técnicos Identificados]].

---

## 7. Alternativas ao Slope Linear

| Método | Pros | Cons |
|---|---|---|
| **Regressão linear** (atual) | Simples, interpretável | Instável com poucos pontos |
| **EWMA** | Robusto, dá peso a recentes | Menos interpretável |
| **Diferença simples N2-N1** | Trivial | Só captura variação de 1 período |
| **Mann-Kendall trend test** | Robusto a não-normalidade | Complexo para séries curtas |

---

## Links

- [[Visão Geral das 9 Features]]
- [[variancia notas — Consistência]]
- [[Pipeline Completo de Treinamento]]
- [[gui ml integration py — Motor de Predição]]
- [[Débitos Técnicos Identificados]] — inconsistência slope_pct vs slope regressão
- [[Feature Importance Detalhada — M3]]
