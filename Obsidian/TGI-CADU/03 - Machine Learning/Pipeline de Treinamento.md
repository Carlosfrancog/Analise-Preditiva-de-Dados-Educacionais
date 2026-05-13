---
tags:
  - ml
  - pipeline
  - tgi-codes
created: 2026-05-13
---

# Pipeline de Treinamento

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## Duas Formas de Treinar

### Via GUI (recomendado)

```
python gui_escola.py
→ Clique: 🤖 Machine Learning
→ Clique: 🔄 Gerar Features
→ Clique: 🚀 Treinar Todos
→ Ver resumo automático com acurácias
```

### Via Terminal

```bash
python train_simple.py
# ou para o pipeline completo com debug:
python run_ml_pipeline.py
```

---

## Sequência de Etapas

### Etapa 1 — Gerar Features

```python
# cads.py → gerar_features_ml()
import cads
cads.gerar_features_ml()
# Gera ~15.000 linhas na tabela ml_features
```

### Etapa 2 — Exportar para CSV

```python
cads.exportar_ml_csv()
# Salva: 02-ML/ml_dataset.csv
```

### Etapa 3 — Carregar e Dividir Dados

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("ml_dataset.csv")
X = df[FEATURES_SEGURAS]    # 9 features sem leakage
y = df['status_encoded']    # 0, 1 ou 2

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
```

### Etapa 4 — Treinar Modelos

```python
from sklearn.ensemble import RandomForestClassifier

modelos = {
    "RF_M1": RandomForestClassifier(n_estimators=100, max_depth=5),
    "RF_M2": RandomForestClassifier(n_estimators=150, max_depth=10),
    "RF_M3": RandomForestClassifier(n_estimators=200),  # sem limite
}

for nome, clf in modelos.items():
    clf.fit(X_train[features_do_modelo], y_train)
```

### Etapa 5 — Avaliar e Salvar

```python
import pickle, json
from sklearn.metrics import accuracy_score

y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)

# Salvar modelo
with open(f"ml_models/{nome}.pkl", "wb") as f:
    pickle.dump(clf, f)

# Salvar metadata
metadata = {"accuracy": acc, "features": lista_features, ...}
with open(f"ml_models/{nome}_metadata.json", "w") as f:
    json.dump(metadata, f)
```

---

## Outputs Gerados

```
02-ML/ml_models/
├── RF_M1.pkl
├── RF_M1_metadata.json
├── RF_M2.pkl
├── RF_M2_metadata.json
├── RF_M3.pkl              ← modelo de produção
└── RF_M3_metadata.json

06-OUTPUT/
├── 01_debug_results.json  ← resultados das 10 validações
└── 02_training_summary.json ← métricas M1, M2, M3
```

---

## Links Relacionados

- [[Módulos ML]] — código-fonte de `ml_pipeline.py` e `run_ml_pipeline.py`
- [[Modelos RF (M1-M2-M3)]] — detalhes de cada modelo
- [[Data Leakage]] — por que algumas features foram excluídas
- [[Início Rápido]] — guia passo a passo para rodar tudo
