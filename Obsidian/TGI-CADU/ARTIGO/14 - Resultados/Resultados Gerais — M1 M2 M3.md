---
tags: [artigo, resultados, acuracia, M1, M2, M3, comparativo]
created: 2026-05-16
---

# Resultados Gerais — Performance dos Três Modelos

[[INDEX - ARTIGO|← Índice]] | [[Comparação M1 M2 M3]] | [[Feature Importance Detalhada — M3]] | [[Matriz de Confusão M3 — Análise Detalhada]]

---

## 1. Tabela de Resultados Principal

| Modelo | Features | Acurácia | Recall Aprovado | Recall Recuperação | Recall Reprovado |
|---|---|---|---|---|---|
| **M1** | 2 | 83,8% | ~90% (est.) | ~35% (est.) | ~70% (est.) |
| **M2** | 4-5 | 92,5% | ~91% (est.) | ~55% (est.) | ~75% (est.) |
| **M3** | 9 | **94,0%** | 91,7% | 62,2% | 76,3% |

*Recalls de M1 e M2 são estimativas — artigo reporta apenas M3.*

---

## 2. Interpretação dos Resultados

### 83,8% (M1) — O Que Isso Significa

De 100 alunos, o M1 erra ~16. Com 200 alunos × 13 matérias = 2.600 pares, M1 erra ~430 predições. Para um EWS, erros em Recuperação e Reprovado são os mais custosos.

### 92,5% (M2) — Sweet Spot

O ganho de 8,7 pp de M1 para M2 é o maior salto. Indica que a adição de N2 (e derivados) é muito informativa. M2 erra ~195 predições de 2.600 — aceitável para uso operacional com 6 meses de antecedência.

### 94,0% (M3) — Produção mas Janela Curta

Apenas 35 predições a mais corretas vs M2 (em 2.600). O custo de esperar N3 para usar M3 (em vez de M2) é reduzir a janela de intervenção de 6 para 3 meses — por apenas 1,5 pp de ganho.

---

## 3. O Achado Principal — Retornos Decrescentes

```
Ganho M1→M2: +8,7 pp  (adição de N2 — muito informativa)
Ganho M2→M3: +1,5 pp  (adição de N3 e features contextuais — marginal)
```

Este é o resultado mais importante do artigo para a tomada de decisão operacional. A implicação: **usar M2 como modelo padrão**, não M3.

O artigo não discute isso explicitamente — uma oportunidade perdida de contribuição prática.

---

## 4. Limitações da Interpretação dos Resultados

### L1 — Acurácia Global Mascara Disparidade

94,0% global esconde:
- Aprovado: 91,7% → OK
- Reprovado: 76,3% → Aceitável
- **Recuperação: 62,2%** → Problemático

Se os pesos pedagógicos forem iguais, a acurácia relevante seria a média não-ponderada: (91,7 + 62,2 + 76,3) / 3 ≈ **76,7% macro-recall** — bem mais honesta que 94%.

### L2 — Validação Intra-Aluno Infla Resultados

Com StratifiedKFold (sem GroupKFold), o mesmo aluno pode aparecer em treino e teste. A acurácia real com GroupKFold provavelmente seria 2-5 pp menor. Ver [[Análise Crítica do TGI#2.5]].

### L3 — Dataset Sintético Favorece o Modelo

Dados sintéticos tendem a ter menos ruído e padrões mais regulares que dados reais. A acurácia em escola real provavelmente seria menor.

---

## 5. Comparação com Literatura

| Sistema | Acurácia | Contexto |
|---|---|---|
| Lima (2021) | 78% | Real, universitário, sem balanceamento |
| Melo (2023) | 82% | Real, fundamental, com frequência |
| **EduPredict M3** | **94%** | Sintético, fundamental, sem frequência |

O EduPredict supera ambos, mas a comparação não é justa pelas razões já discutidas em [[Análise Comparativa dos Trabalhos]].

---

## 6. O Que os Resultados Permitem Concluir (com Honestidade)

**Conclusões sólidas:**
1. O pipeline M1/M2/M3 demonstra que mais dados temporais → mais acurácia
2. N2 é a feature mais informativa disponível antes de N4
3. Detecção de leakage é necessária — sem ela, acurácia seria artificialmente ~99%

**Conclusões que requerem cautela:**
1. "94% de acurácia" é provavelmente superestimado por 2-5 pp (validação intra-aluno)
2. Superioridade sobre Lima e Melo é parcialmente explicada por dados sintéticos
3. A performance em escola real é desconhecida

---

## Links

- [[Comparação M1 M2 M3]]
- [[Feature Importance Detalhada — M3]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
- [[Análise Crítica do TGI]]
- [[Análise Comparativa dos Trabalhos]]
- [[Limitações Gerais do Artigo]]
