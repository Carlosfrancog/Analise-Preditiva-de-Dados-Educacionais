---
tags: [artigo, metricas, matriz-confusao, M3, avaliacao, recall]
created: 2026-05-16
---

# Matriz de Confusão M3 — Análise Detalhada

[[INDEX - ARTIGO|← Índice]] | [[M3 — Modelo de Produção (Após N3)]] | [[Acurácia F1 e Métricas Gerais]] | [[Desempenho por Nível Escolar]]

> [!WARNING] Recuperação com 62,2% de recall — o maior problema operacional do sistema

---

## 1. Recalls por Classe

| Classe | Recall | Interpretação |
|---|---|---|
| **Aprovado** | 91,7% | De 100 aprovados reais, 92 são identificados corretamente |
| **Reprovado** | 76,3% | De 100 reprovados reais, 76 são identificados corretamente |
| **Recuperação** | **62,2%** | De 100 alunos em Recuperação real, apenas 62 são identificados |

---

## 2. Reconstrução Estimada da Matriz de Confusão

O artigo fornece apenas os recalls por classe. A matriz completa pode ser estimada considerando a distribuição de classes do dataset:

**Distribuição estimada do dataset:**
- Aprovado: ~60% dos registros (dominante)
- Reprovado: ~30%
- Recuperação: ~10% (classe mais rara — zona marginal 5,0-5,9)

```
                    Predito
                 Aprov  Recup  Reprov
Real  Aprovado  [91,7%   ?      ?  ]
      Recup     [  ?    62,2%   ?  ]
      Reprovado [  ?     ?    76,3%]
```

**Onde vão os 37,8% não identificados em Recuperação?**
Provavelmente classificados como:
- Aprovado (~25%): borderline Recuperação→Aprovado
- Reprovado (~13%): borderline Recuperação→Reprovado

---

## 3. Por Que Recuperação É Tão Difícil de Classificar?

### Razão 1 — Classe Minoritária
Recuperação corresponde a médias entre 5,0 e 5,9 — uma banda estreita de apenas 1 ponto. Em termos de distribuição, é naturalmente a classe menos frequente. Com `class_weight='balanced'`, o modelo tenta compensar, mas a classe ainda é difícil de separar.

### Razão 2 — Fronteira Difusa
A fronteira Aprovado/Recuperação (média = 6,0) e Recuperação/Reprovado (média = 5,0) são arbitrárias. Um aluno com média 5,95 vs 6,05 pode ter notas praticamente idênticas mas classes diferentes. O modelo não consegue distinguir por princípio.

### Razão 3 — Ruído nas Features
Features como `slope_notas` com apenas 2 pontos têm alta variância. Um aluno com N1=5,0 e N2=6,0 pode ter slope positivo mas estar em Recuperação — confunde o modelo.

### Razão 4 — Natureza Transicional
Recuperação é intrinsecamente um estado de transição — alguns alunos melhoram (→ Aprovado), outros pioram (→ Reprovado). Prever o estado intermediário é fundamentalmente mais difícil.

---

## 4. Implicações Operacionais para o EWS

O recall de 62,2% significa que o sistema de Early Warning **falha em 38% dos alunos em Recuperação**. Para o contexto pedagógico:

| Tipo de Erro | Taxa | Consequência |
|---|---|---|
| **Falso Negativo (Recuperação → Aprovado)** | ~25% | Aluno em risco não recebe intervenção — **o mais perigoso** |
| **Falso Negativo (Recuperação → Reprovado)** | ~13% | Intervenção errada (muito severa) |
| **Falso Positivo (Aprovado → Recuperação)** | Baixo | Professor se preocupa desnecessariamente |
| **Falso Positivo (Reprovado → Recuperação)** | Moderado | Subestimação da gravidade |

**Implicação:** para uso clínico/pedagógico, um threshold mais conservador (prever Recuperação quando a probabilidade for > 35%, em vez de 50%) aumentaria o recall à custa de mais falsos positivos. Melhor errar para o lado da cautela.

---

## 5. Estratégias para Melhorar o Recall de Recuperação

### Estratégia 1 — Threshold Ajustado

```python
# Em vez de usar predict() direto, usar predict_proba() com threshold menor
probas = model.predict_proba(X)[0]  # [p_reprov, p_recup, p_aprov]

THRESHOLD_RECUP = 0.35  # em vez de 0.50 padrão

if probas[1] >= THRESHOLD_RECUP:  # p_recup >= 35%
    prediction = 1  # Recuperação
elif probas[0] > probas[2]:
    prediction = 0  # Reprovado
else:
    prediction = 2  # Aprovado
```

### Estratégia 2 — Abordagem Hierárquica

Primeiro classificar "Em risco (Recup + Reprov)" vs "Aprovado", depois dentro de "Em risco" classificar Recup vs Reprov. Dois classificadores binários em cascata.

### Estratégia 3 — One-vs-Rest com Calibração de Probabilidade

```python
from sklearn.calibration import CalibratedClassifierCV
calibrated_rf = CalibratedClassifierCV(rf, method='isotonic', cv=3)
```

Calibração melhora a confiabilidade das probabilidades, o que beneficia threshold tuning.

### Estratégia 4 — SMOTE para Oversampling

```python
from imblearn.over_sampling import SMOTE
X_res, y_res = SMOTE(random_state=42).fit_resample(X, y)
```

Gera amostras sintéticas da classe Recuperação para balancear o treinamento. Porém, o artigo já usa `class_weight='balanced'`, que é a alternativa mais simples.

---

## 6. Acurácia Global vs Acurácia por Classe

A acurácia global de 94,0% mascara o desempenho heterogêneo por classe. Uma análise honesta apresenta:

```
Acurácia global: 94,0%   ← número do artigo
Recall Aprovado: 91,7%   ← OK para a maioria dos alunos
Recall Reprovado: 76,3%  ← aceitável para intervenção
Recall Recuperação: 62,2% ← PROBLEMÁTICO — o grupo que mais precisa de ajuda
```

Para um sistema de EWS, o recall de Recuperação e Reprovado é mais importante que a acurácia global. O artigo deveria ter enfatizado isso mais.

---

## 7. Métricas Mais Apropriadas para EWS

| Métrica | Valor M3 | Por que relevante |
|---|---|---|
| **Acurácia global** | 94,0% | Visão geral |
| **Macro-recall** | ~76,7% | Média não ponderada dos recalls — mais honesta |
| **Recall Recuperação** | 62,2% | Detecta a classe que mais precisa de atenção |
| **Recall combinado (Recup+Reprov)** | ~70% | Recall de "em risco" como binário |
| **AUC-ROC (One-vs-Rest)** | ? (não reportado) | Mais robusto que acurácia |

O artigo deveria reportar AUC-ROC e macro-F1 em vez de focar apenas na acurácia.

---

## Links

- [[M3 — Modelo de Produção (Após N3)]]
- [[class weight balanced — Tratamento de Desbalanceamento]]
- [[Acurácia F1 e Métricas Gerais]]
- [[Limitações Gerais do Artigo]]
- [[Análise Crítica do TGI]]
- [[Protocolo de Alertas EWS]]
