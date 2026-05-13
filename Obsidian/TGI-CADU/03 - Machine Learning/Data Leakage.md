---
tags:
  - ml
  - data-leakage
  - tgi-codes
created: 2026-05-13
---

# Data Leakage

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## O Problema

Duas features do dataset têm correlação altíssima com o target (`status_encoded`), indicando que elas **derivam diretamente do resultado** — usar no treino tornaria o modelo inútil em produção.

| Feature | Correlação com target | Motivo |
|---|---|---|
| `media_pond_norm` | 0.95 | É calculada com N1+N2+N3+N4 — já "sabe" o resultado |
| `n4_norm` | 0.91 | N4 é a nota final / recuperação — define o status diretamente |

> [!WARNING] Efeito
> Um modelo treinado com essas features atingiria ~98% de acurácia no treino, mas **falharia completamente em produção**, pois N4 ainda não existe quando a predição precisa ser feita.

---

## A Solução Implementada

O módulo `ml_debug.py` detecta automaticamente features suspeitas e o `ml_pipeline.py` as remove antes do treino:

```python
# ml_debug.py — detecção automática
LEAKAGE_THRESHOLD = 0.85

for feature in features:
    corr = df[feature].corr(df['status_encoded'])
    if abs(corr) >= LEAKAGE_THRESHOLD:
        suspicious.append({
            "feature": feature,
            "correlacao": corr,
            "risco": "CRÍTICO"
        })
```

---

## Features Removidas vs Mantidas

```
REMOVIDAS (Data Leakage):
  ❌ media_pond_norm   → derivada do target
  ❌ n4_norm           → nota final não disponível em tempo real

MANTIDAS (Seguras para produção):
  ✅ n1_norm, n2_norm, n3_norm   → notas parciais
  ✅ slope_notas                  → tendência
  ✅ variancia_notas              → consistência
  ✅ pct_materias_ok              → contexto
  ✅ media_geral_aluno            → contexto
  ✅ serie_num_norm               → contexto
  ✅ media_turma_norm             → contexto
```

---

## Output do Debug

Os resultados são salvos em `06-OUTPUT/01_debug_results.json`:

```json
{
  "leakage": {
    "suspicious_count": 2,
    "suspicious": [
      {
        "tipo": "ALTA CORRELAÇÃO",
        "feature": "media_pond_norm",
        "correlacao": 0.9543,
        "risco": "CRÍTICO"
      },
      {
        "tipo": "ALTA CORRELAÇÃO",
        "feature": "n4_norm",
        "correlacao": 0.9134,
        "risco": "CRÍTICO"
      }
    ]
  }
}
```

---

## Links Relacionados

- [[Features e Cálculos]] — lista completa das 9 features seguras
- [[Modelos RF (M1-M2-M3)]] — como os modelos usam essas features
- [[Visão Geral ML]] — pipeline completo com etapa de validação
- [[Módulos ML]] — código de `ml_debug.py`
