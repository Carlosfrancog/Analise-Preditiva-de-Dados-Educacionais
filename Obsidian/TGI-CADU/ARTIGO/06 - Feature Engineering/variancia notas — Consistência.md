---
tags: [artigo, feature-engineering, variancia, consistencia, features]
created: 2026-05-16
---

# variancia_notas — Consistência das Notas

[[INDEX - ARTIGO|← Índice]] | [[Visão Geral das 9 Features]] | [[slope notas — Tendência Temporal]] | [[pct materias ok — Aprovação Global]]

> [!NOTE] Importância no M3: 5,2% — 6ª feature mais importante

---

## 1. Definição Matemática

`variancia_notas` é a variância populacional das notas normalizadas disponíveis:

$$variancia = \frac{1}{n}\sum_{i=1}^{n}(y_i - \bar{y})^2$$

Onde:
- $y_i$ = nota normalizada ($N_i / 10$)
- $\bar{y}$ = média das notas disponíveis
- $n$ = quantidade de notas disponíveis

**Implementação esperada em `cads.py`:**
```python
def _variancia(vals):
    """Variância populacional das notas normalizadas."""
    n = len(vals)
    if n < 2:
        return 0.0
    ym = sum(vals) / n
    return sum((y - ym) ** 2 for y in vals) / n
```

---

## 2. Interpretação Pedagógica

| Valor | Interpretação | Perfil do aluno |
|---|---|---|
| `var < 0,01` | Notas muito estáveis (ex: 5,0-5,0-5,0) | Consistente — para bem ou mal |
| `0,01-0,05` | Variação normal entre bimestres | Padrão típico |
| `0,05-0,10` | Alta variação — notas oscilatórias | Irregular — pode melhorar muito ou cair |
| `var > 0,10` | Extremamente irregular | 3,0→9,0→2,0 — instabilidade comportamental |

**Complementaridade com slope_notas:**
- slope > 0 + variância baixa → melhora consistente (melhor caso)
- slope > 0 + variância alta → melhora errática
- slope ≈ 0 + variância alta → aluno inconsistente — às vezes bem, às vezes mal
- slope < 0 + variância baixa → queda consistente (pior caso para EWS)

---

## 3. Por Que 5,2% de Importância?

Importância moderada-baixa porque:
1. Com 9 features ricas (n2_norm com 32,3%), a variância captura informação residual
2. Em M3, a variância é calculada sobre 3 pontos — mais estável que M2 (2 pontos)
3. Alta variância pode ser tanto positiva (aluno em melhora irregular) quanto negativa — ambiguidade que reduz importância

---

## 4. Problema de Escala com 2 Pontos (M2)

No M2, variância é calculada com N1 e N2 apenas. Com 2 pontos, a variância é:

$$var(N1, N2) = \frac{(N1/10 - \bar{y})^2 + (N2/10 - \bar{y})^2}{2} = \frac{(N1/10 - N2/10)^2}{4}$$

Ou seja, variância com 2 pontos é simplesmente o quadrado da metade da diferença. A complexidade da função `_variancia()` não agrega nada para 2 pontos — seria equivalente a `((n1 - n2) / 20) ** 2`.

---

## 5. Relação com slope_notas

Variância e slope são ortogonais matematicamente mas correlacionadas empiricamente:
- Alta variância implica que os pontos estão espalhados ao redor da reta de regressão
- slope é a inclinação da reta — não captura dispersão em torno da reta

Um aluno com N1=3, N2=9, N3=3 tem:
- slope ≈ 0 (média estável ao redor de 5,0)
- variância = 0,08 (muito alta)

O modelo captura ambos — slope diz "estável", variância diz "imprevisível".

---

## 6. Limitações

1. **Não diferencia direção:** alta variância pode ser subida ou descida. Precisa ser combinada com slope para ter sentido completo.

2. **Sensível a outliers:** uma única nota atípica (ex: doença, evento pessoal) inflaciona a variância e distorce a feature.

3. **Sem normalização formal:** o range teórico de variância com notas 0-1 é [0, 0,25]. Não é normalizado explicitamente.

---

## Links

- [[Visão Geral das 9 Features]]
- [[slope notas — Tendência Temporal]]
- [[Feature Importance Detalhada — M3]]
- [[M2 — Modelo Intermediário]]
