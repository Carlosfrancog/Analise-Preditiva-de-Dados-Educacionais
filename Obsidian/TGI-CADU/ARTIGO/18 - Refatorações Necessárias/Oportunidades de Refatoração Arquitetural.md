---
tags: [artigo, refatoracao, arquitetura, melhorias, codigo]
created: 2026-05-16
---

# Oportunidades de Refatoração Arquitetural

[← Índice](<../INDEX - ARTIGO.md>) | [[Débitos Técnicos Identificados]] | [[Compatibilidade Arquitetural]] | [[Gaps — TGI vs EduNotas Atual]]

---

## 1. Contexto

Além dos débitos técnicos específicos (DT-01 a DT-07), existem oportunidades de refatoração que melhorariam a manutenibilidade, testabilidade e extensibilidade do sistema como um todo.

---

## 2. Separação de Camadas (Mais Urgente)

**Problema:** `cads.py` mistura responsabilidades:
```
cads.py hoje:
├── Gerenciamento de conexão DB (get_conn, DB_PATH)
├── Schema e migração (init_db)
├── CRUD de alunos, turmas, notas
├── Geração de dados sintéticos (gerar_alunos_genericos, gerar_notas_aleatorias)
├── Feature engineering (gerar_features_ml, _slope, _std)
└── Constantes (SALAS, NOMES, SOBRENOMES, MATERIAS, PESOS_NOTAS)
```

**Refatoração proposta:**
```
cads/
├── db.py           ← conexão, schema, migração
├── crud.py         ← alunos, turmas, notas CRUD
├── features.py     ← gerar_features_ml, _slope, _std
├── synthetic.py    ← gerar_alunos_genericos, gerar_notas_aleatorias
└── constants.py    ← SALAS, NOMES, MATERIAS, PESOS_NOTAS
```

**Benefício:** Permite testar `features.py` independentemente do banco; permite substituir `synthetic.py` por dados reais sem tocar no CRUD.

---

## 3. Injeção de Dependência em MLModelLoader

**Problema atual:**
```python
class MLModelLoader:
    def __init__(self):
        self._load_models()  # hardcoded path "02-ML/ml_models/"
```

**Refatoração:**
```python
class MLModelLoader:
    def __init__(self, model_dir: Path = None):
        self.model_dir = model_dir or Path("02-ML/ml_models")
        self._load_models()
```

**Benefício:** Permite testes com diretório temporário sem modificar o código de produção.

---

## 4. Interface Explícita para Features

**Problema atual:**
```python
# feature_cols hardcoded em dois lugares diferentes:
# train_simple.py: feature_cols = ['n1_norm', 'n2_norm', ...]
# gui_ml_integration.py: recuperado do metadata.json
# Se um mudar sem o outro → FeatureNamesWarning ou ValueError
```

**Refatoração:**
```python
# cads/constants.py:
SAFE_TRAINING_FEATURES = [
    'n1_norm', 'n2_norm', 'n3_norm',
    'slope_notas', 'variancia_notas',
    'media_geral_aluno', 'pct_materias_ok',
    'media_turma_norm', 'serie_num_norm'
]
LEAKY_FEATURES = frozenset(['media_pond_norm', 'n4_norm'])

# train_simple.py:
from cads.constants import SAFE_TRAINING_FEATURES
X = df[SAFE_TRAINING_FEATURES]

# gui_ml_integration.py:
from cads.constants import SAFE_TRAINING_FEATURES
features_pred_df = pd.DataFrame([features_pred], columns=SAFE_TRAINING_FEATURES)
```

---

## 5. Configuração Centralizada

**Problema:** Parâmetros críticos espalhados por múltiplos arquivos:
```python
# Em cads.py:
PESOS_NOTAS = {"n1": 1, "n2": 2, "n3": 3, "n4": 4}

# Em train_simple.py:
test_size = 0.2
random_state = 42

# Em gui_ml_integration.py:
RISK_THRESHOLD_CRITICO = 0.70
RISK_THRESHOLD_RISCO   = 0.40
SLOPE_MELHORA   = 20  # slope_pct > 20% → will_improve
SLOPE_PIORA     = -20 # slope_pct < -20% → will_decline
```

**Refatoração:** Arquivo `config.py` ou `settings.py` com todos os hiperparâmetros e thresholds. Permite ajuste sem tocar na lógica.

---

## 6. Tratamento de Erros Consistente

**Problema:** Erros silenciosos em vários pontos:
```python
# gui_ml_integration.py — atual:
try:
    pred, proba = model_loader.predict(nome, features)
except Exception:
    pass  # falha silenciosa → UI mostra estado indefinido
```

**Refatoração:** Hierarquia de exceções explícita:
```python
class EduPredictError(Exception): pass
class ModelNotLoadedError(EduPredictError): pass
class FeatureMismatchError(EduPredictError): pass
class InsufficientDataError(EduPredictError): pass

# Capturar e exibir na UI:
try:
    pred, proba = model_loader.predict(...)
except ModelNotLoadedError:
    messagebox.showerror("Modelo não encontrado", "Execute train_simple.py primeiro")
except FeatureMismatchError as e:
    messagebox.showerror("Inconsistência", str(e))
```

---

## 7. Testes Unitários

**Estado atual:** Nenhum teste automatizado identificado no projeto.

**Prioridade de cobertura:**
```python
# tests/test_features.py
def test_slope_positivo():
    assert cads._slope([5, 6, 7]) > 0

def test_slope_notas_zeradas():
    # n3 ausente → não deve quebrar
    result = cads._slope([6, 7, 0])
    assert result is not None

def test_detect_leakage():
    assert 'media_pond_norm' in cads.detect_leakage(df)
    assert 'n4_norm' in cads.detect_leakage(df)

def test_predict_with_correct_features():
    loader = MLModelLoader(model_dir=Path("tests/fixtures/models"))
    pred, proba = loader.predict("RF_M3", SAFE_FEATURES_SAMPLE)
    assert pred in [0, 1, 2]
```

---

## Links

- [[Débitos Técnicos Identificados]]
- [[Compatibilidade Arquitetural]]
- [[cads.py — Análise Profunda]]
- [[gui ml integration py — Motor de Predição]]
- [[Serialização dos Modelos]]
