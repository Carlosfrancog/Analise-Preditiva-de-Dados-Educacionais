---
tags: [artigo, modelos, comparação, trade-off, temporal]
created: 2026-05-16
---

# Comparação M1 × M2 × M3 — Trade-off Antecedência × Acurácia

[[INDEX - ARTIGO|← Índice]] | [[M1 — Modelo Precoce]] | [[M2 — Modelo Intermediário]] | [[M3 — Modelo de Produção (Após N3)]]

---

## 1. Tabela Comparativa Central

| Aspecto | M1 | M2 | M3 |
|---|---|---|---|
| **Ponto temporal** | Após N1 | Após N2 | Após N3 |
| **Antecedência** | ~9 meses | ~6 meses | ~3 meses |
| **Features** | 2 | 4-5 | 9 |
| **Acurácia** | 83,8% | 92,5% | 94,0% |
| **Ganho incremental** | — | +8,7 pp | +1,5 pp |
| **Modelo arquivo** | model_m1.pkl | model_m2.pkl | model_m3.pkl |

---

## 2. Curva de Aprendizado Temporal

```
Acurácia
94% |                               ●  M3
    |
92% |               ●  M2
    |
    |
    |
83% | ●  M1
    └──────────────────────────────────
       N1           N2           N3
       (1º bimestre) (2º bimestre) (3º bimestre)
```

O ganho diminuente entre modelos sugere **lei dos retornos decrescentes**: cada bimestre adicional de dados adiciona menos informação preditiva. N2 é o salto crítico; N3 adiciona apenas refinamento marginal.

---

## 3. Análise de Retorno de Investimento Pedagógico

| Modelo | Acurácia | Antecedência | Valor pedagógico |
|---|---|---|---|
| **M1** | 83,8% | Máxima | Alertas precoces porém imprecisos — muitos falsos alarmes |
| **M2** | 92,5% | Alta | **Melhor custo-benefício** — alta acurácia com tempo para agir |
| **M3** | 94,0% | Baixa | Precisão máxima mas janela de ação estreita |

**Recomendação:** para uma escola real, M2 deveria ser o modelo operacional principal. M3 seria usado como refinamento no conselho de classe.

---

## 4. Por Que o Sistema Usa M3 Como Padrão?

A interface de predições (`gui_predicoes_improved.py`) usa automaticamente o modelo mais avançado disponível:

```python
# gui_ml_integration.py
if n3 is not None:
    model = model_m3  # ← usado sempre que N3 existe
```

Isso significa que no momento de consulta do professor (que pode ser após N3), o sistema usa M3 automaticamente. Não há como pedir explicitamente M1 ou M2 pela interface.

**Problema:** um professor que consulta após N2 mas antes de N3 usaria M2 corretamente. Mas um professor que consulta após N3 usa M3 — e pode não saber que isso reduz a antecedência. A interface deveria exibir qual modelo está sendo usado e em qual ponto temporal estamos.

---

## 5. Diagrama de Seleção de Modelo

```
Notas disponíveis?
    ↓
N1 apenas → usa M1 (83,8%)
N1 + N2   → usa M2 (92,5%)
N1+N2+N3  → usa M3 (94,0%)
Nenhuma   → "dados insuficientes"
```

---

## 6. Implicações para o EWS de 3 Níveis

| Modelo | Falsos Negativos | Risco de EWS |
|---|---|---|
| M1 | ~16% | Muitos alertas perdidos |
| M2 | ~7,5% | Operacionalmente aceitável |
| M3 | ~6% | Melhor — mas intervenção tardia |

O EWS deveria calibrar os thresholds de alerta diferentemente para cada modelo. Um alerta M1 "EM RISCO" deveria ter peso diferente de um alerta M3 "EM RISCO".

---

## Links

- [[M1 — Modelo Precoce]]
- [[M2 — Modelo Intermediário]]
- [[M3 — Modelo de Produção (Após N3)]]
- [[Pipeline Completo de Treinamento]]
- [[Protocolo de Alertas EWS]]
- [[Análise Crítica do TGI]]
