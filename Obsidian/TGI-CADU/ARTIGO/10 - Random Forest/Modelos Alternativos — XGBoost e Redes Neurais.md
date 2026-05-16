---
tags: [artigo, random-forest, xgboost, redes-neurais, alternativas, comparacao]
created: 2026-05-16
---

# Modelos Alternativos — XGBoost, SVM e Redes Neurais

[← Índice](<../INDEX - ARTIGO.md>) | [[Random Forest — Algoritmo e Justificativa]] | [[Comparação M1 M2 M3]] | [[Análise Crítica do TGI]]

---

## 1. Por Que Random Forest Foi Escolhido

O artigo justifica Random Forest por:
- Robustez a outliers e ruído nos dados
- Menor necessidade de tuning comparado a SVM/redes neurais
- Feature importance integrada (interpretabilidade)
- Bom desempenho em datasets tabulares de tamanho médio

Mas **não apresenta comparação empírica** com alternativas — uma limitação metodológica.

---

## 2. XGBoost — Alternativa Mais Provável de Superar RF

### Por Que XGBoost é Competitivo

```python
from xgboost import XGBClassifier

xgb = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='mlogloss',
    random_state=42
)
```

**Vantagens sobre RF:**
- Gradient boosting: cada árvore corrige os erros da anterior (vs RF: árvores independentes)
- Regularização L1/L2 integrada (reduz overfitting)
- Lida melhor com features desbalanceadas e missing values

**Desvantagem:**
- Mais lento para treinar
- Mais hiperparâmetros para tunar
- Menos interpretável que RF (sem feature importance direta; requer SHAP)

### Estimativa de Desempenho

Para datasets tabulares de tamanho médio (~2600 amostras):
- XGBoost tipicamente supera RF em 1-3 pontos percentuais
- Com dados sintéticos balanceados, a diferença seria mínima
- Com dados reais e mais ruído, XGBoost seria mais robusto

---

## 3. SVM — Referência da Literatura Brasileira

Lima (2021) usa SVM junto com RF — tornando SVM o baseline natural para comparação.

```python
from sklearn.svm import SVC

svm = SVC(
    kernel='rbf',          # Radial Basis Function — mais comum
    C=1.0,                 # regularização
    gamma='scale',         # default sklearn
    class_weight='balanced',
    probability=True,      # para ter proba e risk_score
    random_state=42
)
```

**Vantagens:** Funciona bem em alta dimensão, margem máxima.
**Desvantagens:** Lento para datasets grandes, sem feature importance nativa, sensível a escala (requer normalização — que o EduPredict já faz).

**Resultado esperado:** SVM deve ter desempenho similar ao RF em features já normalizadas [0,1]. A diferença é de interpretabilidade — RF tem feature importance, SVM não.

---

## 4. Redes Neurais — Overkill para Este Problema

```python
from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(
    hidden_layer_sizes=(64, 32),
    max_iter=300,
    random_state=42
)
```

**Por Que Redes Neurais Provavelmente Não Superam RF Aqui:**

1. **Poucos dados:** 2600 amostras é insuficiente para explorar a capacidade de redes neurais
2. **Pouças features:** 9 features — espaço muito pequeno para redes aprenderem representações complexas
3. **Sem imagem/texto:** redes neurais brilham em dados não-estruturados; tabelas favoreceram árvores
4. **Interpretabilidade:** NN são caixas-pretas — incompatível com requisitos de explicabilidade

---

## 5. Regressão Logística — Baseline Mais Simples

```python
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(
    multi_class='multinomial',
    class_weight='balanced',
    max_iter=500,
    random_state=42
)
```

**Por Que Incluir no Artigo:**
- Muito interpretável (coeficientes = importâncias diretas)
- Alta velocidade de treino e predição
- Se LR atingir 90%+ de acurácia, questiona se RF com 94% justifica a complexidade adicional
- Serve como baseline inferior — se RF não superar LR, há problema no pipeline

---

## 6. Tabela Comparativa Estimada

| Modelo | Acurácia estimada | F1 Macro | Interpretabilidade | Tempo de treino |
|---|---|---|---|---|
| Regressão Logística | ~82-86% | ~0.75 | Alta | < 1s |
| **Random Forest M3** | **94.0%** | **~0.88** | **Média** | **~5s** |
| XGBoost | ~94-96% | ~0.89 | Baixa (requer SHAP) | ~10s |
| SVM (RBF) | ~88-92% | ~0.83 | Baixa | ~15s |
| MLP (64,32) | ~88-92% | ~0.82 | Muito baixa | ~30s |

*Estimativas para dataset sintético; valores reais precisariam de experimentos.*

---

## 7. Recomendação para Artigo de Extensão

Incluir um benchmark com pelo menos:
1. Regressão Logística (baseline)
2. Random Forest M3 (modelo atual)
3. XGBoost (candidato superior)

Reportar F1 Macro e Recall de Recuperação — não apenas acurácia.

---

## Links

- [[Random Forest — Algoritmo e Justificativa]]
- [[Hiperparâmetros do Random Forest]]
- [[Comparação M1 M2 M3]]
- [[Acurácia F1 e Métricas Gerais]]
- [[Análise Crítica do TGI]]
- [[Lima 2021 — Random Forest e SVM]]
- [[Insights para o Artigo de Extensão]]
