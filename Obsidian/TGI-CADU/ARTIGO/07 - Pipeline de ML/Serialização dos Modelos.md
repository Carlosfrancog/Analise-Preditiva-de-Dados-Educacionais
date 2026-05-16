---
tags: [artigo, pipeline, serializacao, pickle, modelos]
aliases: [Serialização e Versionamento de Modelos, Serialização dos Modelos]
created: 2026-05-16
---

# Serialização dos Modelos — Pickle e Metadata JSON

[← Índice](<../INDEX - ARTIGO.md>) | [[Pipeline Completo de Treinamento]] | [[train simple py — Pipeline Autônomo]] | [[gui ml integration py — Motor de Predição]]

---

## 1. Mecanismo de Serialização

O EduPredict usa `pickle` (via `joblib`) para serializar os modelos treinados:

```python
# train_simple.py — Passo 4
import pickle, json

for nome, modelo in modelos.items():
    # Serializar o classificador treinado
    pkl_path = f"02-ML/ml_models/{nome}.pkl"
    with open(pkl_path, 'wb') as f:
        pickle.dump(modelo, f)

    # Salvar metadados em JSON legível
    meta = {
        "accuracy":      float(accuracy),
        "f1":            float(f1),
        "n_features":    len(feature_cols),
        "features":      feature_cols,
        "n_samples_train": len(X_train),
        "n_samples_test":  len(X_test),
        "date":          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "confusion_matrix": cm.tolist(),
        "n_estimators":  modelo.n_estimators,
        "max_depth":     modelo.max_depth   # None para RF_M3
    }
    with open(f"02-ML/ml_models/{nome}_metadata.json", 'w') as f:
        json.dump(meta, f, indent=4)
```

---

## 2. Estrutura de Arquivos Gerados

```
02-ML/ml_models/
├── RF_M1.pkl
├── RF_M1_metadata.json
├── RF_M2.pkl
├── RF_M2_metadata.json
├── RF_M3.pkl              ← modelo principal de produção
└── RF_M3_metadata.json    ← lido por MLModelLoader na inicialização
```

---

## 3. Por Que o Metadata JSON É Crítico

O campo `features` no metadata é usado pelo `MLModelLoader.predict()` para criar o DataFrame com os **nomes corretos das features**:

```python
# gui_ml_integration.py — MLModelLoader.predict()
feature_names = self.metadata.get("RF_M3", {}).get("features", [])
# ["n1_norm", "n2_norm", "n3_norm", "slope_notas", ...]

df_pred = pd.DataFrame([features_pred], columns=feature_names)
# Evita FeatureNamesWarning do sklearn 1.x:
# "X has feature names, but RandomForestClassifier was fitted without feature names"
pred = model.predict(df_pred)
```

Se o metadata estiver desatualizado (features adicionadas/removidas após último treino), o predict falha com `ValueError: X has N features but model was fitted with M features`.

---

## 4. Carregamento na Inicialização

```python
# gui_ml_integration.py — MLModelLoader.__init__()
class MLModelLoader:
    def __init__(self):
        self.models = {}
        self.metadata = {}
        self._load_models()

    def _load_models(self):
        model_dir = Path("02-ML/ml_models")
        for nome in ["RF_M1", "RF_M2", "RF_M3"]:
            pkl = model_dir / f"{nome}.pkl"
            meta = model_dir / f"{nome}_metadata.json"

            if pkl.exists():
                with open(pkl, 'rb') as f:
                    self.models[nome] = pickle.load(f)
            if meta.exists():
                with open(meta, 'r') as f:
                    self.metadata[nome] = json.load(f)
```

Os modelos são carregados **uma vez** na inicialização da GUI. Se o arquivo `.pkl` não existir (antes de rodar `train_simple.py`), `MLModelLoader.models` fica vazio e as predições retornam `None`.

---

## 5. Riscos de Segurança — Pickle

`pickle` não é seguro contra arquivos maliciosos — um `.pkl` modificado pode executar código arbitrário no load. Isso é aceitável para uso local (arquivo gerado pelo próprio sistema), mas **não** para distribuição em produção.

Alternativas mais seguras para deployment:
- `joblib` (padrão para sklearn, mesmos riscos que pickle)
- ONNX (formato aberto, seguro, portável)
- MLflow Model Registry (versionamento + tracking)

---

## 6. Ausência de Versionamento — Risco

O sistema sobrescreve o `.pkl` e `.json` a cada execução de `train_simple.py` sem:
- Numeração de versão
- Hash do dataset usado no treinamento
- Comparação com modelo anterior antes de substituir
- Rollback se novo modelo for pior

**Cenário de falha:** Alguém roda `train_simple.py` com dados corrompidos ou com feature diferente → modelo sobrescrito → interface quebra ou prediz com garbage.

**Solução mínima:**
```python
# Antes de salvar o novo modelo:
import hashlib
data_hash = hashlib.md5(df.to_csv().encode()).hexdigest()
meta["dataset_hash"] = data_hash
meta["previous_accuracy"] = old_meta.get("accuracy", 0)
# Só substituir se novo modelo for melhor
```

---

## Links

- [[Pipeline Completo de Treinamento]]
- [[train simple py — Pipeline Autônomo]]
- [[gui ml integration py — Motor de Predição]]
- [[Débitos Técnicos Identificados]]
- [[Oportunidades de Refatoração Arquitetural]]
