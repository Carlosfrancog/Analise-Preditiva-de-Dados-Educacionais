---
tags: [artigo, data-leakage, pearson, deteccao, metodologia]
created: 2026-05-16
---

# Detecção Automática de Data Leakage por Correlação de Pearson

[[INDEX - ARTIGO|← Índice]] | [[Data Leakage — Conceito e Impacto]] | [[media pond norm — Feature Removida]] | [[n4 norm — Feature Removida]]

> [!SUCCESS] Diferencial técnico central do EduPredict — único na literatura EDM nacional consultada

---

## 1. O Mecanismo

O EduPredict implementa detecção automática de data leakage via correlação de Pearson entre cada feature e o target (`status_encoded`) antes de qualquer treinamento:

```python
# 02-ML/train_simple.py — detecção de leakage
def detect_leakage(df, target_col, threshold=0.9):
    """Remove features com correlação > 0.9 com o target."""
    correlations = df.corr()[target_col].abs()
    leaky_features = correlations[correlations > threshold].index.tolist()
    leaky_features.remove(target_col)  # não remover o próprio target
    return leaky_features

# Execução antes de cada modelo M1/M2/M3
leaky = detect_leakage(df_train, 'status_encoded', threshold=0.9)
df_clean = df_train.drop(columns=leaky)
```

---

## 2. Resultados da Detecção

| Feature | Correlação com target | Status | Razão |
|---|---|---|---|
| `media_pond_norm` | 0,95 | 🚫 Removida | Derivada diretamente do resultado |
| `n4_norm` | 0,91 | 🚫 Removida | N4 só existe após o resultado |
| `n3_norm` | ~0,75 | ✅ Mantida | N3 está disponível antes do resultado final |
| `n2_norm` | ~0,65 | ✅ Mantida | Feature legítima |
| `pct_materias_ok` | ~0,60 | ✅ Mantida | Limiar < 0,9 (risco residual — ver abaixo) |

---

## 3. Justificativa do Limiar 0,9

O artigo não discute formalmente a escolha de 0,9, mas a lógica é:

**Por que não 0,7?** Features como `n3_norm` têm correlação ~0,75 com o target — isso é correlação genuína, não leakage. N3 existe antes do resultado e é informativa. Usar 0,7 removeria features legítimas.

**Por que não 0,95?** `n4_norm` tem r=0,91 — seria mantida com limiar 0,95, o que seria errado.

**0,9 captura o limiar:** acima de 0,9, a feature essencialmente determina o target (é circular). Abaixo, a correlação é informação útil.

**Limitação:** a escolha de 0,9 é arbitrária e não foi validada com análise de sensibilidade. Ver [[Limitações Gerais do Artigo]].

---

## 4. Por Que Pearson Especificamente?

| Método | Detecta | Usado no EduPredict |
|---|---|---|
| **Pearson** | Relações lineares | ✅ Sim |
| **Spearman** | Relações monotônicas | ❌ Não |
| **Informação Mútua** | Relações não-lineares, dependências complexas | ❌ Não |
| **SHAP-based** | Impacto causal no modelo | ❌ Não |

Pearson é adequado aqui porque:
1. `media_pond_norm` → `status_encoded` é quase perfeitamente linear (step function com 3 degraus)
2. `n4_norm` → `status_encoded` também é altamente linear

Para relações não-lineares ou leakage indireto, Pearson falharia. Ver [[Data Leakage — Conceito e Impacto#6 Riscos Residuais]].

---

## 5. Fluxo Completo no Pipeline

```
Dados brutos (15.613 registros)
          ↓
gerar_features_ml() [cads.py]
          ↓
df com todas as features + target
          ↓
detect_leakage(threshold=0.9) [train_simple.py]
    → remove media_pond_norm (r=0.95)
    → remove n4_norm (r=0.91)
          ↓
df_clean com 9 features legítimas
          ↓
Divisão treino/teste (80/20 estratificado)
          ↓
Treinamento M1/M2/M3 [RandomForestClassifier]
```

---

## 6. Onde o Mecanismo Vive no Código

```
02-ML/
  train_simple.py          ← detect_leakage() implementado aqui
  gui_ml_integration.py    ← NÃO reaplica detecção (risco!)
  
01-CORE/
  cads.py                  ← gerar_features_ml() — calcula e salva todas as features
                              (incluindo as leaky, para visualização)
  
03-GUI/
  gui_escola.py            ← MLPage exibe media_pond_norm, mas não usa para predição
```

**Risco identificado:** `media_pond_norm` é armazenada na tabela `ml_features` para visualização. Um desenvolvedor futuro poderia inadvertidamente passá-la ao modelo. O código não tem guards/assertions protegendo isso.

---

## 7. O Que Tornaria a Detecção Mais Robusta

### Melhoria 1 — Adicionar Informação Mútua como segundo critério

```python
from sklearn.feature_selection import mutual_info_classif

def detect_leakage_v2(df, target_col, pearson_threshold=0.9, mi_threshold=0.8):
    # Critério 1: Pearson (relações lineares)
    pearson = df.corr()[target_col].abs()
    leaky_pearson = set(pearson[pearson > pearson_threshold].index)
    
    # Critério 2: Informação Mútua (relações não-lineares)
    X = df.drop(columns=[target_col])
    mi = mutual_info_classif(X, df[target_col])
    mi_series = pd.Series(mi, index=X.columns)
    leaky_mi = set(mi_series[mi_series > mi_threshold].index)
    
    # União dos dois critérios
    return leaky_pearson.union(leaky_mi) - {target_col}
```

### Melhoria 2 — Adicionar assertions no schema

```python
# cads.py — constantes protegidas
LEAKY_FEATURES = frozenset(['media_pond_norm', 'n4_norm'])
TRAINING_FEATURES = [f for f in ALL_FEATURES if f not in LEAKY_FEATURES]

def get_training_df():
    """Retorna DataFrame apenas com features de treinamento."""
    df = get_all_features_df()
    assert not any(f in df.columns for f in LEAKY_FEATURES), \
        f"LEAKY FEATURES DETECTED: {LEAKY_FEATURES & set(df.columns)}"
    return df[TRAINING_FEATURES + ['status_encoded']]
```

---

## 8. Impacto Quantificado

Sem detecção de leakage, a acurácia estimada seria ~99% (media_pond_norm determina o target). Com detecção:
- M3: **94,0%** — real, sem artificialismo
- A diferença de ~5 pontos percentuais é a "acurácia fantasma"

Ver [[Análise Comparativa dos Trabalhos]] — Lima (78%) e Melo (82%) não trataram leakage.

---

## Links

- [[Data Leakage — Conceito e Impacto]]
- [[media pond norm — Feature Removida]]
- [[n4 norm — Feature Removida]]
- [[Pipeline Completo de Treinamento]]
- [[Débitos Técnicos Identificados]]
- [[Limitações Gerais do Artigo]]
- [[Análise Crítica do TGI]]
