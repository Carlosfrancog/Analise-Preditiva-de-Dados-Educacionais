---
tags: [artigo, data-leakage, ml, metodologia, critico]
created: 2026-05-14
---

# Data Leakage — Conceito e Impacto

[[INDEX - ARTIGO|← Índice]] | [[Detecção Automática por Correlação de Pearson]] | [[media pond norm — Feature Removida]] | [[n4 norm — Feature Removida]]

> [!CRITICAL] Diferencial metodológico principal do EduPredict
> A detecção automática de data leakage é a contribuição técnica mais relevante do artigo e a menos comum na literatura nacional de EDM (Romero e Ventura, 2020).

---

## 1. Definição Precisa

**Data leakage** (vazamento de dados) ocorre quando **informações do futuro** — que não estariam disponíveis no momento da predição real — são inadvertidamente incluídas no conjunto de treinamento, inflando artificialmente a acurácia do modelo.

### Tipos de Leakage

| Tipo | Descrição | Exemplo no contexto escolar |
|---|---|---|
| **Target leakage** | Feature derivada diretamente do target | `media_pond_norm` calculada com N1-N4 para prever status calculado com N1-N4 |
| **Temporal leakage** | Uso de informação futura em predição passada | Usar N4 para prever o status antes de N4 ser lançada |
| **Train-test contamination** | Informação do conjunto de teste vaza para o treino | Normalização calculada sobre o dataset completo antes do split |

O EduPredict identificou e eliminou os dois primeiros tipos. O terceiro não é discutido.

---

## 2. Por Que É Tão Devastador?

Considere o cenário sem detecção de leakage:

```python
# CENÁRIO COM LEAKAGE (como muitos artigos fazem)
features = ['n1_norm', 'n2_norm', 'n3_norm', 'n4_norm', 'media_pond_norm']
target = 'status_encoded'  # calculado com as 4 notas

# media_pond_norm é calculada assim:
media_pond_norm = (0.2*N1 + 0.25*N2 + 0.25*N3 + 0.30*N4) / 10

# status_encoded é calculado assim:
# status = 2 (Aprovado) se media_pond >= 6
# status = 1 (Recuperação) se 5 <= media_pond < 6
# status = 0 (Reprovado) se media_pond < 5

# Resultado: media_pond_norm DETERMINA status_encoded com r=0.95
# O modelo aprende: "se media_pond_norm >= 0.6, prediz Aprovado"
# Acurácia: ~99% — completamente artificial
```

**Sem leakage, o modelo estaria "trapaceando":** usaria informações que só existem DEPOIS do evento que tenta predizer.

---

## 3. Impacto Quantitativo no EduPredict

Com `media_pond_norm` (r=0,95) e `n4_norm` (r=0,91) **incluídas**, a acurácia estimada seria próxima de 99%. Após remoção:

- **M3 real: 94,0%** — ainda excelente, mas sem artificialismo

A diferença de ~5 pontos percentuais representa a "acurácia fantasma" que enganou estudos anteriores.

---

## 4. Implementação da Detecção no EduPredict

O mecanismo implementado verifica **10 tipos de validação**, incluindo:

```python
# Pseudocódigo do mecanismo de detecção
for feature in all_features:
    correlation = pearson_correlation(feature, target)
    if abs(correlation) > 0.9:
        mark_as_leakage(feature)
        remove_from_training_set(feature)
        log_warning(f"{feature}: correlação {correlation:.2f} — removida")
```

**Limiar 0,9:** arbitrário, mas conservador. Features com correlação 0,7-0,9 podem ser genuínas (ex: `n3_norm` tem correlação natural com status final, mas não é leakage — N3 está disponível antes do resultado).

Ver [[Detecção Automática por Correlação de Pearson]] para análise completa.

---

## 5. Onde Está no Código

```python
# 02-ML/train_simple.py — função de detecção
def detect_leakage(df, target_col, threshold=0.9):
    correlations = df.corr()[target_col].abs()
    leaky_features = correlations[correlations > threshold].index.tolist()
    leaky_features.remove(target_col)  # não remover o próprio target
    return leaky_features
```

A chamada ocorre antes do treinamento de cada modelo M1/M2/M3 em `train_simple.py`.

---

## 6. Riscos Residuais — O Que a Detecção Atual NÃO Captura

| Risco | Descrição | Impacto |
|---|---|---|
| **Leakage indireto** | Feature A correlaciona com Feature B que loga com target | Não detectado por correlação univariada de Pearson |
| **Train-test contamination** | Normalização pré-split usa stats do conjunto completo | Não verificado no artigo |
| **Temporal leakage sutil** | `pct_materias_ok` usa status atual de TODAS as matérias — se calculada no momento certo, pode estar usando informação de matérias ainda não concluídas | Risco baixo se feature engineering é feita corretamente |

---

## 7. Alternativas Melhores ao Pearson

| Método | Vantagem | Desvantagem |
|---|---|---|
| **Correlação de Pearson** (usado) | Simples, rápido | Só detecta relações lineares |
| **Informação Mútua** | Detecta relações não-lineares | Mais custoso computacionalmente |
| **Permutation importance** | Baseado no impacto real no modelo | Requer modelo já treinado |
| **SHAP-based leakage detection** | Mais preciso, detecta leakage indireta | Complexo de implementar |

**Recomendação para o artigo de extensão:** adicionar informação mútua como segundo critério de detecção.

---

## 8. Impacto no Projeto Atual

O `cads.py` calcula `media_pond_norm` mas ela é **corretamente excluída** do treinamento pelo `train_simple.py`. Porém, a tabela `ml_features` ainda armazena `media_pond_norm` para fins de visualização na interface (`MLPage` no `gui_escola.py`).

**Risco:** um desenvolvedor futuro poderia inadvertidamente incluir `media_pond_norm` em um modelo sem conhecer o problema de leakage. O código carece de comentários ou assertions que enforcem essa exclusão.

**Refatoração sugerida:**
```python
# Em cads.py — marcar features proibidas no schema
LEAKY_FEATURES = ['media_pond_norm', 'n4_norm']  # excluir do treinamento
TRAINING_FEATURES = [f for f in ALL_FEATURES if f not in LEAKY_FEATURES]
```

---

## Links

- [[Detecção Automática por Correlação de Pearson]]
- [[media pond norm — Feature Removida]]
- [[n4 norm — Feature Removida]]
- [[Pipeline Completo de Treinamento]]
- [[Análise Comparativa dos Trabalhos]] — por que outros trabalhos não detectaram
- [[Débitos Técnicos Identificados]] — risco de reintrodução acidental
