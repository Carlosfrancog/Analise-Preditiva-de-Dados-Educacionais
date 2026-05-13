---
tags:
  - codigo
  - ml
  - treino
  - tgi-codes
created: 2026-05-13
---

# `train_simple.py` — Documentação de Código

[[INDEX - Código|← Índice de Código]] | [[MOC - TGI-CODES|← MOC]]

> [!NOTE] Localização
> `02-ML/train_simple.py` | Script autônomo — `python train_simple.py`
> Alternativa ao treino via GUI ([[gui_ml_advanced.py#_train_models]])

---

## Imports e Dependências

```python
import cads                                          # → [[cads.py]]
import pickle, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
```

---

## Pipeline de 4 Passos

O script executa sequencialmente, saindo com erro se qualquer passo falhar.

---

### Passo 1 — Gerar Features

```python
cads.gerar_features_ml()
# → [[cads.py#gerar_features_ml]]
# Calcula 9 features para cada (aluno × matéria) e persiste em ml_features
```

---

### Passo 2 — Exportar CSV

```python
df_info, msg = cads.exportar_ml_csv()
# → [[cads.py#exportar_ml_csv]]
# Gera: 02-ML/ml_dataset.csv
```

---

### Passo 3 — Carregar e Preparar Dados

```python
df = pd.read_csv("ml_dataset.csv")

# Features seguras (sem data leakage)
# Ver: [[Data Leakage]] para entender por que n4_norm e media_pond_norm são excluídas
feature_cols = [
    'n1_norm', 'n2_norm', 'n3_norm', 'n4_norm',
    'slope_notas', 'variancia_notas', 'media_geral_aluno',
    'serie_num_norm', 'media_turma_norm'
]

X = df[feature_cols]
y = df['status_encoded']    # 0=Reprovado, 1=Recuperação, 2=Aprovado

# Split estratificado 80/20 (mantém proporção de classes)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y          # ← garante mesma proporção no treino e teste
)
```

---

### Passo 4 — Treinar 3 Modelos

```python
modelos = {
    'RF_M1': RandomForestClassifier(n_estimators=100, max_depth=5,  random_state=42),
    'RF_M2': RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42),
    'RF_M3': RandomForestClassifier(n_estimators=200,               random_state=42),
    # RF_M3: sem max_depth = árvores crescem até pureza total (mais acurado)
}
```

Para cada modelo:

```python
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1       = f1_score(y_test, y_pred, average='weighted')
cm       = confusion_matrix(y_test, y_pred)

# Salvar modelo
with open(f"ml_models/{name}.pkl", "wb") as f:
    pickle.dump(clf, f)

# Salvar metadata
metadata = {
    "accuracy": float(accuracy),
    "f1": float(f1),
    "n_features": len(feature_cols),
    "features": feature_cols,
    "n_samples_train": len(X_train),
    "n_samples_test": len(X_test),
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "confusion_matrix": cm.tolist(),
    "n_estimators": clf.n_estimators,
    "max_depth": clf.max_depth
}
with open(f"ml_models/{name}_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
```

---

## Outputs Gerados

```
02-ML/ml_models/
├── RF_M1.pkl
├── RF_M1_metadata.json
├── RF_M2.pkl
├── RF_M2_metadata.json
├── RF_M3.pkl              ← carregar em produção
└── RF_M3_metadata.json    ← lido por [[gui_ml_advanced.py#_load_model_info]]
                           ← lido por [[gui_ml_integration.py#MLModelLoader]]
```

---

## Comparação com Treino via GUI

| Aspecto | `train_simple.py` | [[gui_ml_advanced.py#_train_models|MLAdvancedPage._train_models()]] |
|---|---|---|
| Como executar | `python train_simple.py` | Botão na interface |
| Thread | Síncrono (bloqueia terminal) | Thread separada (não trava GUI) |
| Features de M1 | todas as 9 | subset por modelo |
| Output | `.pkl` + `_metadata.json` | `.pkl` + `_metadata.json` |
| Pesos usados | `PESOS_NOTAS` padrão | pesos configurados nos sliders |

---

## Diferença de Features por Modelo

> [!NOTE] Atenção
> `train_simple.py` treina os 3 modelos com as **mesmas 9 features** — a diferença é apenas o número de árvores e profundidade. O [[gui_ml_advanced.py]] usa features diferentes por modelo (M1 só usa n1_norm, M2 usa 4 features, M3 usa 9).

**Ver:** [[Modelos RF (M1-M2-M3)]] para os detalhes de features por modelo
