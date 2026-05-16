---
tags: [artigo, random-forest, desbalanceamento, class_weight, metricas]
created: 2026-05-16
---

# `class_weight='balanced'` — Tratamento de Desbalanceamento de Classes

[[INDEX - ARTIGO|← Índice]] | [[Random Forest — Algoritmo e Justificativa]] | [[Matriz de Confusão M3 — Análise Detalhada]]

---

## 1. O Problema de Classes Desbalanceadas

No dataset do EduPredict, a distribuição estimada das classes é:

| Classe | Status | Estimativa |
|---|---|---|
| 2 — Aprovado | média ≥ 6,0 | ~60% dos registros |
| 0 — Reprovado | média < 5,0 | ~30% dos registros |
| 1 — Recuperação | 5,0 ≤ média < 6,0 | ~10% dos registros |

Sem tratamento, um classificador naive que sempre prediz "Aprovado" acertaria 60% — acurácia global razoável, mas recall de Recuperação = 0% e recall de Reprovado = 0%.

---

## 2. Como `class_weight='balanced'` Funciona

O sklearn computa automaticamente:

$$w_k = \frac{n\_total}{n\_classes \times n_k}$$

Para as classes estimadas:
- $w_{Aprovado} = \frac{15613}{3 \times 9368} \approx 0,56$
- $w_{Reprovado} = \frac{15613}{3 \times 4684} \approx 1,11$
- $w_{Recuperação} = \frac{15613}{3 \times 1561} \approx 3,33$

**Efeito:** cada amostra de Recuperação tem peso 6× maior que uma amostra de Aprovado no critério de split das árvores. O modelo "aprende" mais de cada exemplo de Recuperação.

---

## 3. Impacto Observado

Com `class_weight='balanced'`:
- Aprovado: recall 91,7% (ligeiramente reduzido vs sem balanceamento)
- Recuperação: recall 62,2% (muito melhorado vs ~10-20% sem balanceamento)
- Reprovado: recall 76,3% (melhorado vs ~60% sem balanceamento)

O recall de Recuperação (62,2%) ainda é baixo, mas seria muito pior sem o balanceamento.

---

## 4. Alternativas ao `class_weight='balanced'`

| Técnica | Como funciona | Prós | Contras |
|---|---|---|---|
| **class_weight** (usado) | Ajusta pesos no critério de split | Simples, sem geração de dados | Não cria novos exemplos da minoria |
| **SMOTE** | Gera exemplos sintéticos da minoria | Mais exemplos para aprender | Pode gerar exemplos não-realistas |
| **Undersampling** | Remove exemplos da maioria | Simples | Perde informação |
| **Threshold tuning** | Ajusta limiar de decisão | Sem mudança no treino | Requer calibração cuidadosa |
| **Ensemble especializado** | BalancedRandomForest, EasyEnsemble | Robusto | Mais complexo |

Para o artigo de extensão, comparar `class_weight='balanced'` com SMOTE + RF seria contribuição relevante, especialmente para a classe Recuperação.

---

## 5. Por Que Recuperação Ainda Tem 62,2%?

`class_weight='balanced'` aumenta o peso dos exemplos de Recuperação, mas não resolve o problema fundamental: Recuperação é uma zona de transição intrinsecamente difusa (notas 5,0-5,9) com fronteiras arbitrárias. Ver [[Matriz de Confusão M3 — Análise Detalhada#3 Por Que Recuperação É Tão Difícil de Classificar]].

---

## 6. Comparação com Lima (2021)

Lima (2021) identificou o desbalanceamento como limitação mas não implementou `class_weight`. O EduPredict avança nesse ponto — é uma diferença metodológica real. Ver [[Análise Comparativa dos Trabalhos]].

---

## Links

- [[Random Forest — Algoritmo e Justificativa]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
- [[Análise Comparativa dos Trabalhos]]
- [[Lima 2021 — Random Forest e SVM]]
- [[Acurácia F1 e Métricas Gerais]]
