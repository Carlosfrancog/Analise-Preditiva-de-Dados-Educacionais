---
tags: [artigo, random-forest, algoritmo, ml, ensemble]
created: 2026-05-16
---

# Random Forest — Algoritmo e Justificativa de Escolha

[[INDEX - ARTIGO|← Índice]] | [[class weight balanced — Tratamento de Desbalanceamento]] | [[Feature Importance Detalhada — M3]] | [[Hiperparâmetros do Random Forest]]

---

## 1. O Algoritmo em Resumo

Random Forest é um método ensemble que combina múltiplas árvores de decisão treinadas em subamostras aleatórias dos dados (bootstrap) com subconjuntos aleatórios de features em cada divisão (feature bagging):

```
Para cada estimador t = 1 ... n_estimators:
    1. Amostragem bootstrap: D_t = bootstrap(D_treino)
    2. Treinar árvore T_t em D_t com feature bagging
    
Predição por voto majoritário:
    ŷ = mode({T_1(x), T_2(x), ..., T_n(x)})
    
Probabilidade:
    P(ŷ=k) = (1/n) * Σ [T_t(x) == k]
```

---

## 2. Por Que Random Forest para EDM?

### Vantagens no contexto escolar

| Propriedade | Por que importa no EduPredict |
|---|---|
| **Não requer normalização** | Features em escalas diferentes (notas 0-1, pct 0-1, série 0-1) não precisam de z-score |
| **Robusto a multicolinearidade** | n2_norm e n3_norm são correlacionadas — RF lida melhor que regressão logística |
| **Feature importance nativa** | Gera ranking de importância diretamente (Gini importance) |
| **Não paramétrico** | Não assume distribuição gaussiana — notas podem ter distribuição bimodal |
| **Tolerante a outliers** | Uma nota atípica não destrói o modelo (distribuída por muitas árvores) |
| **Multiclasse nativo** | Suporta 3 classes (Aprovado/Recuperação/Reprovado) diretamente |

### Comparação com alternativas

| Algoritmo | Acurácia esperada | Interpretabilidade | Limitação principal |
|---|---|---|---|
| **Random Forest** (escolhido) | 94% | Média (global) | Caixa-preta individual |
| **Regressão Logística** | ~85% | Alta | Linear — perde padrões não-lineares |
| **SVM** | ~89% | Baixa | Lento em grandes datasets |
| **Gradient Boosting** | ~95% | Baixa | Mais hiperparâmetros, overfitting |
| **Rede Neural** | ~93-96% | Muito baixa | Precisa mais dados, difícil de explicar |
| **KNN** | ~78% | Intuitiva | Lento em predição, sensível a escala |

RF é uma escolha sólida e bem justificada para o contexto. Gradient Boosting (XGBoost/LightGBM) provavelmente superaria, mas com mais complexidade.

---

## 3. Feature Importance — Como é Calculada

O RF calcula importância pela redução de impureza de Gini que cada feature causa, média sobre todas as árvores:

$$Importance(f) = \frac{1}{n_{trees}} \sum_{t=1}^{n_{trees}} \sum_{v \in T_t, split\_feature(v)=f} \Delta Gini(v)$$

**Limitações da Gini Importance:**
1. Favorece features com muitos valores únicos — features contínuas (notas) vs categóricas (série)
2. É a importância **global** — não diz nada sobre alunos individuais
3. Não é uma medida causal — importância ≠ causalidade

**Alternativa mais robusta:** SHAP (SHapley Additive exPlanations) — ver [[SHAP — Explicabilidade Local por Aluno]].

---

## 4. `class_weight='balanced'` — Por Que É Essencial

O dataset tem distribuição desbalanceada:
- Aprovado: ~60% (dominante)
- Reprovado: ~30%
- Recuperação: ~10% (minoria)

Sem balanceamento, o modelo aprende a dizer "Aprovado" para tudo e acerta 60% — acurácia aparente alta, mas recall de Recuperação ≈ 0%.

`class_weight='balanced'` ajusta os pesos de forma inversamente proporcional à frequência:
```
weight_k = n_samples / (n_classes * count_k)
```

Ver [[class weight balanced — Tratamento de Desbalanceamento]].

---

## 5. Interpretabilidade Global vs Local

**O que o EduPredict fornece (feature importance global):**
```
n2_norm: 32,3%  ← importante em média sobre todos os alunos
pct_materias_ok: 21,5%
slope_notas: 12,3%
...
```

**O que falta (SHAP local):**
```
Para o aluno João Silva, matéria Matemática:
  n2_norm contribuiu com +0,35 para P(Reprovado)  ← específico para este aluno
  pct_materias_ok contribuiu com -0,12 para P(Reprovado)
  slope_notas contribuiu com +0,08 para P(Reprovado)
```

A diferença é fundamental para uso pedagógico real. Feature importance global não justifica uma decisão individual.

---

## 6. Hiperparâmetros Não Documentados

O artigo especifica apenas:
- `class_weight='balanced'`
- `random_state=42`

Parâmetros padrão do sklearn são provavelmente usados:
- `n_estimators=100` (100 árvores)
- `max_depth=None` (árvores crescem até pureza completa)
- `min_samples_split=2`
- `min_samples_leaf=1`
- `max_features='sqrt'` (raiz quadrada das features em cada split)

Com `max_depth=None`, as árvores podem fazer overfitting. Em um dataset de 15.613 registros, árvores sem limite de profundidade podem memorizar o treinamento. A validação cruzada captura isso, mas o modelo final (treinado no dataset completo) pode ser menos generalizável.

---

## 7. Por Que Não Gradient Boosting?

Gradient Boosting (XGBoost, LightGBM) tipicamente supera RF em benchmarks de classificação tabular. O artigo não justifica a escolha de RF sobre GB.

Possíveis razões:
1. RF é mais simples e menos propenso a overfitting com configuração padrão
2. RF é paralelizável (árvores independentes) — mais rápido de treinar
3. RF é mais robusto sem tuning de hiperparâmetros
4. Contexto acadêmico — RF é mais familiar e bem-documentado

Para o artigo de extensão, comparar RF vs XGBoost vs LightGBM seria contribuição válida.

---

## Links

- [[class weight balanced — Tratamento de Desbalanceamento]]
- [[Feature Importance Detalhada — M3]]
- [[Hiperparâmetros do Random Forest]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[M3 — Modelo de Produção (Após N3)]]
- [[Pipeline Completo de Treinamento]]
- [[Análise Crítica do TGI]]
