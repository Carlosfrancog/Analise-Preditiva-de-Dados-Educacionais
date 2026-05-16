---
tags: [artigo, modelos, M2, random-forest, intermediario]
aliases: [M2 — Predição Intermediária (Após N2), M2 — Modelo Intermediário]
created: 2026-05-16
---

# M2 — Modelo Intermediário (Após N2)

[[INDEX - ARTIGO|← Índice]] | [[M1 — Modelo Precoce]] | [[M3 — Modelo de Produção (Após N3)]] | [[Comparação M1 M2 M3]]

> [!NOTE] 92,5% de acurácia — melhor equilíbrio antecedência × precisão

---

## 1. Especificação Técnica

| Parâmetro | Valor |
|---|---|
| **Ponto temporal** | Após lançamento de N2 (2º bimestre) |
| **Features de entrada** | 4-5 |
| **Algoritmo** | RandomForestClassifier |
| **Acurácia (CV 5-fold)** | **92,5%** |
| **Arquivo de modelo** | `02-ML/models/model_m2.pkl` |

---

## 2. Features do M2

| Feature | Importância estimada | Observação |
|---|---|---|
| `n1_norm` | ~15% | Contexto inicial |
| `n2_norm` | ~55% | Dominante — a mais preditiva disponível |
| `slope_notas` | ~20% | Calculado com N1+N2 (2 pontos — alta variância) |
| `variancia_notas` | ~5% | Calculada com N1+N2 (mínima — 2 pontos) |
| `serie_num_norm` | ~5% | Contextual |

**Nota:** o artigo não reporta feature importances para M1 e M2, apenas para M3. Os valores acima são estimativas baseadas nos padrões observados no M3.

---

## 3. O Salto Crítico M1 → M2

O ganho de **+8,7 pontos percentuais** (83,8% → 92,5%) ao adicionar N2 é o maior salto no pipeline temporal. Isso ocorre porque:

1. **N2 é altamente correlacionada com o resultado final** — dois pontos temporais de dados permitem ao modelo aprender trajetórias, não apenas estados
2. **slope_notas com 2 pontos** — embora instável, adiciona informação direcional crítica
3. **N2 confirma ou contradiz N1** — um aluno que tirou 4,0 em N1 e 7,0 em N2 tem prognóstico radicalmente diferente do que tirou 7,0→4,0

O ganho de M2→M3 é apenas +1,5 pp — marginal em comparação.

---

## 4. Fragilidade do slope_notas no M2

Com apenas 2 pontos (N1 e N2), a regressão linear em `_slope(vals)` é determinística:
- slope = N2/10 - N1/10 = (N2 - N1) / 10

Para 2 pontos, slope_notas é exatamente a diferença simples normalizada — não há benefício da regressão linear sobre uma diferença simples. A complexidade matemática do `_slope()` não agrega nada para M2.

**Consequência:** slope_notas no M2 é altamente sensível a ruído (1 ponto define a "tendência" inteira).

---

## 5. Valor Operacional do M2

M2 é o modelo mais útil para intervenção pedagógica real:
- **92,5% de acurácia** — muito próximo de M3
- **6 meses de antecedência** (N2 lançada no 2º bimestre)
- **Tempo suficiente** para intervenções: reforço, tutoria, reunião com pais

O M2 é o "sweet spot" do sistema. Estranhamente, o EduPredict usa M3 como modelo padrão para a interface principal — uma escolha que prioriza precisão sobre antecedência.

---

## 6. Diagnóstico de Erros do M2

Os 7,5% de erro do M2 são provavelmente concentrados em:
1. Alunos com trajetória não-monotônica (sobem em N3 após queda em N2)
2. Alunos com N1 e N2 muito próximos ao limiar (5,0 e 6,0)
3. Efeito "prova difícil de N2" — nota atípica distorce slope e media

---

## Links

- [[M1 — Modelo Precoce]]
- [[M3 — Modelo de Produção (Após N3)]]
- [[Comparação M1 M2 M3]]
- [[slope notas — Tendência Temporal]]
- [[Visão Geral das 9 Features]]
- [[Pipeline Completo de Treinamento]]
