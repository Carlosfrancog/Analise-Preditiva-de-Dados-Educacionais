---
tags: [artigo, metodologia, design, pesquisa, classificacao]
created: 2026-05-16
---

# Classificação e Design da Pesquisa — EduPredict

[[INDEX - ARTIGO|← Índice]] | [[Questão de Pesquisa e Objetivos]] | [[Pipeline Completo de Treinamento]] | [[Dataset — Estrutura e Geração Sintética]]

---

## 1. Classificação da Pesquisa

### Quanto à Natureza
**Pesquisa Aplicada** — não visa descoberta de novos conhecimentos teóricos, mas a aplicação de técnicas conhecidas (Random Forest, feature engineering) para resolver um problema real (predição de desempenho escolar).

### Quanto à Abordagem
**Quantitativa** — dados numéricos (notas, proporções), métricas numéricas de avaliação (acurácia, recall), análise estatística (correlação de Pearson, validação cruzada).

### Quanto aos Objetivos
**Descritiva e Explicativa:**
- **Descritiva:** descreve o desempenho dos modelos M1/M2/M3
- **Explicativa:** explica quais features determinam o risco (feature importance)

### Quanto aos Procedimentos Técnicos
**Experimental computacional** — experimentos controlados com datasets, métricas e baselines definidos.

---

## 2. Design Experimental

```
[Problema] → [Coleta/Geração de Dados] → [Feature Engineering] → 
[Treinamento ML] → [Avaliação] → [Análise] → [Interface]
```

### Variáveis Independentes
- Conjunto de features (9 features para M3)
- Ponto temporal (M1/M2/M3)
- Algoritmo (Random Forest)

### Variável Dependente
- Acurácia do modelo (% de predições corretas)
- Recall por classe (% de alunos em cada categoria identificados corretamente)

### Variáveis Controladas
- Dataset fixo (200 alunos, geração determinística com seed)
- Random seed (42) para reprodutibilidade
- Mesma divisão treino/teste (StratifiedKFold 5-fold)

---

## 3. Framework de Avaliação

O artigo usa **validação cruzada estratificada com k=5** como método principal de avaliação:
- 5 folds: 4 para treino, 1 para teste
- Estratificado: proporção de classes igual em cada fold
- Resultado: acurácia média e desvio padrão sobre os 5 folds

**Métricas reportadas:**
- Acurácia global: M1=83,8%, M2=92,5%, M3=94,0%
- Recall por classe (M3): Aprovado 91,7%, Recuperação 62,2%, Reprovado 76,3%

**Métricas não reportadas (lacuna):**
- AUC-ROC
- Macro-F1
- Precision por classe
- Confusion matrix completa

---

## 4. Justificativa do Random Forest como Algoritmo

O artigo deveria apresentar uma justificativa formal para a escolha de RF. Baseando-se nas melhores práticas da literatura EDM:

1. **Adequado para dados tabulares:** notas, percentuais, índices
2. **Nativo para multiclasse:** suporta 3 classes sem one-vs-rest
3. **Feature importance nativa:** insight sobre quais variáveis são mais preditivas
4. **Robusto a multicolinearidade:** features correlacionadas (n2, n3) não causam instabilidade
5. **`class_weight='balanced'`:** trata desbalanceamento nativamente
6. **Amplamente usado em EDM:** comparável com Lima (2021) e outros

Ver [[Random Forest — Algoritmo e Justificativa]] para análise completa.

---

## 5. Limitações Metodológicas Declaradas vs Reais

| Limitação | Declarada no artigo? | Gravidade real |
|---|---|---|
| Dataset sintético | Parcialmente | Alta |
| Validação intra-aluno | ❌ Não | Alta |
| Leakage indireto (pct_materias_ok) | ❌ Não | Média |
| Threshold de Pearson arbitrário | ❌ Não | Média |
| Hiperparâmetros não otimizados | ❌ Não | Baixa |
| Ausência de frequência | ✅ Sim | Média |
| Sem explicabilidade local | Parcialmente | Média |

Ver [[Limitações Gerais do Artigo]] para análise completa.

---

## 6. Comparação com Baselines

O artigo compara com Lima (2021) e Melo (2023) como baselines. A comparação tem limitações:
- Datasets diferentes (real vs sintético)
- Contextos diferentes (graduação, fundamental, todos)
- Métricas reportadas de formas diferentes

Para um artigo científico rigoroso, o baseline ideal seria re-implementar Lima e Melo no mesmo dataset — o que não foi feito.

---

## Links

- [[Questão de Pesquisa e Objetivos]]
- [[Dataset — Estrutura e Geração Sintética]]
- [[Random Forest — Algoritmo e Justificativa]]
- [[Pipeline Completo de Treinamento]]
- [[Limitações Gerais do Artigo]]
- [[Análise Comparativa dos Trabalhos]]
