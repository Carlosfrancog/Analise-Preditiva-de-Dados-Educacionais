---
tags:
  - codigo
  - ml
  - tgi-codes
created: 2026-05-13
---

# `gui_ml_integration.py` — Documentação de Código

[[INDEX - Código|← Índice de Código]] | [[MOC - TGI-CODES|← MOC]]

> [!NOTE] Localização
> `02-ML/gui_ml_integration.py` | Importado por: [[gui_predicoes_improved.py]]

---

## Imports e Dependências

```python
import cads           # → [[cads.py]] (get_conn, _slope, _std)
import pickle, json
import numpy as np
import pandas as pd
from pathlib import Path
```

---

## `class MLModelLoader` {#MLModelLoader}

```python
class MLModelLoader:
    """Carrega e gerencia os modelos treinados (M1, M2, M3)."""

    def __init__(self):
        self.models = {}     # model_name → sklearn model
        self.metadata = {}   # model_name → dict do JSON
        self.models_dir = Path("ml_models")
        self._load_models()
```

**Responsabilidade:** Localiza e carrega todos os arquivos `.pkl` + `_metadata.json` na pasta `ml_models/`. Suporta dois formatos:
- **Novo:** `ml_models/RF_M3.pkl` + `ml_models/RF_M3_metadata.json`
- **Antigo:** `ml_models/RF_M3/model.pkl` + `ml_models/RF_M3/metadata.json`

**Chamado por:** [[gui_predicoes_improved.py#PredictionPageImproved|PredictionPageImproved.__init__()]]

---

### `_load_models()` {#_load_models}

```python
def _load_models(self) -> None:
```

**O que faz:** Varre `ml_models/` com `glob("RF_M*.pkl")` e carrega cada modelo com `pickle.load()`. Preenche `self.models` e `self.metadata`.

**Prioridade:** Formato novo (`.pkl` na raiz) tem prioridade sobre formato antigo (subdiretório).

```python
# Após carregar com sucesso:
print(f"[OK] RF_M3 carregado (acuracia: 94.0%, 9 features)")
```

---

### `is_available(model_name)` {#is_available}

```python
def is_available(self, model_name: str = "RF_M3") -> bool:
```

**Chamado por:** [[gui_ml_integration.py#analyze_student|DisciplinePerformanceAnalyzer.analyze_student()]] — verifica se há modelo antes de predizer

---

### `predict(model_name, features)` {#predict}

```python
def predict(
    self,
    model_name: str,          # "RF_M3"
    features: list[float]     # lista na ordem do metadata["features"]
) -> tuple[int | None, np.ndarray | None]:
    # Retorna: (classe_predita, array_de_probabilidades)
    # Ex: (2, [0.02, 0.11, 0.87])
```

**O que faz:**
1. Constrói DataFrame com `feature_names` do metadata (evita warnings do sklearn)
2. Chama `model.predict_proba(features_df)`
3. Retorna `(argmax(proba), proba)`

**Chamado por:** [[gui_ml_integration.py#analyze_student|DisciplinePerformanceAnalyzer.analyze_student()]]

> [!NOTE] Feature names
> Usa o campo `metadata["features"]` para criar o DataFrame com nomes corretos, eliminando `FeatureNamesWarning` do scikit-learn.

---

## `class DisciplinePerformanceAnalyzer` {#DisciplinePerformanceAnalyzer}

```python
class DisciplinePerformanceAnalyzer:
    """Analisa o desempenho do aluno em cada disciplina."""

    STATUS_COLOR = {
        0: {"name": "Reprovado",    "color": "#C62828", "emoji": "[X]"},
        1: {"name": "Recuperacao",  "color": "#FF9800", "emoji": "[!]"},
        2: {"name": "Aprovado",     "color": "#2E7D32", "emoji": "[ok]"},
    }
```

**Responsabilidade:** Orquestra a análise completa de um aluno — busca notas, calcula features em tempo real, prediz com RF_M3 e gera prognóstico.

---

### `analyze_student(db_path, aluno_id, model_loader)` {#analyze_student}

```python
@staticmethod
def analyze_student(
    db_path: str,
    aluno_id: int,
    model_loader: MLModelLoader
) -> dict | None:
```

**O que faz:** Análise completa do aluno em TODAS as disciplinas.

**Sequência interna:**

```python
# 1. Conectar ao banco
conn = cads.get_conn()              # → [[cads.py#get_conn]]

# 2. Buscar aluno e disciplinas
aluno = conn.execute("SELECT ... FROM alunos WHERE id = ?", ...)
disciplinas = conn.execute("SELECT ... FROM materias JOIN notas ...", ...)

# 3. Para cada disciplina:
for materia in disciplinas:
    notas = conn.execute("SELECT n1,n2,n3,n4 FROM notas WHERE ...", ...)

    # Normalizar notas para [0, 1]
    n1 = n1_raw / 10
    n2 = n2_raw / 10
    ...

    # Calcular features temporais
    slope = cads._slope([n1_raw, n2_raw, n3_raw, n4_raw])   # → [[cads.py#_slope]]
    var   = cads._std([n1_raw, n2_raw, n3_raw, n4_raw])     # → [[cads.py#_std]]

    # Predição com modelo
    features = [n1, n2, n3, slope, var, ...]
    pred, proba = model_loader.predict("RF_M3", features)   # → [[gui_ml_integration.py#predict]]

    # Gerar prognóstico
    if slope > 0.20: prognostico = "vai_melhorar"
    elif slope < -0.20: prognostico = "vai_piorar"
    else: prognostico = "estavel"
```

**Retorno:**

```python
{
    "aluno": {
        "id": 5,
        "nome": "João Silva",
        "matricula": "2M0001",
        "sala": "2º Médio"
    },
    "disciplinas": [
        {
            "nome": "Matemática",
            "n1": 7.0, "n2": 6.5, "n3": 8.0, "n4": None,
            "media_atual": 7.1,
            "status_pred": 2,          # 0=Reprovado, 1=Recup., 2=Aprovado
            "status_label": "Aprovado",
            "confianca": 0.87,
            "slope": 0.43,
            "prognostico": "vai_melhorar",
            "cor": "#2E7D32"
        },
        ...
    ],
    "strengths": ["Matemática", "Ciências"],   # status_pred == 2
    "weaknesses": ["História"],                # status_pred == 0
    "at_risk": ["Geografia"],                  # status_pred == 1
    "profile": "Equilibrado"
}
```

**Chamado por:** [[gui_predicoes_improved.py#_load_aluno|PredictionPageImproved._load_aluno()]]

**Chama:**
- [[cads.py#get_conn|cads.get_conn()]]
- [[cads.py#_slope|cads._slope()]]
- [[cads.py#_std|cads._std()]]
- [[gui_ml_integration.py#predict|MLModelLoader.predict()]]

**Ver também:** [[Modelos RF (M1-M2-M3)]], [[Features e Cálculos]]
