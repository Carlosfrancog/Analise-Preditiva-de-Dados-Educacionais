---
tags:
  - codigo
  - ml
  - gui
  - tgi-codes
created: 2026-05-13
---

# `gui_ml_advanced.py` — Documentação de Código

[[INDEX - Código|← Índice de Código]] | [[MOC - TGI-CODES|← MOC]]

> [!NOTE] Localização
> `02-ML/gui_ml_advanced.py` | Importado por: [[gui_escola.py#_build_ui|gui_escola.py → _build_ui()]]

---

## Imports e Dependências

```python
import cads                              # → [[cads.py]]
from gui_predicoes_improved import BasePage  # → [[gui_predicoes_improved.py]]
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import pickle, json, pandas as pd, numpy as np
```

---

## Constantes de Tema (Dark Mode)

```python
DARK_BG = "#0F1419"    # fundo da página ML
CARD_BG = "#1E2329"    # cards internos
ACCENT  = "#5B9FDB"    # azul
SUCCESS = "#4CBD71"    # verde
WARN    = "#FFB946"    # laranja
ERROR   = "#F76A6A"    # vermelho

COLORS = {
    0: {"name": "Reprovado",   "hex": "#F76A6A"},
    1: {"name": "Recuperação", "hex": "#FFB946"},
    2: {"name": "Aprovado",    "hex": "#4CBD71"},
}
```

---

## `class MLAdvancedPage(BasePage)` {#MLAdvancedPage}

```python
class MLAdvancedPage(BasePage):
    """Dashboard de ML com treino, visualização e análise de decisões."""

    def __init__(self, parent, app):
        super().__init__(parent, app, "Machine Learning Avançado", "🤖")
        self.model_loader = None
        self.last_training = None
        self._build()
        self.after(100, self._load_weights_config)
```

**Responsabilidade:** Página completa de ML — exibe modelos treinados, permite treinar novos, analisa decisões por aluno e configura pesos da média ponderada.

**Herda de:** [[gui_predicoes_improved.py#BasePage|BasePage]] (via `gui_predicoes_improved.py`)

---

## `_build()` {#_build}

```python
def _build(self) -> None:
```

**O que faz:** Constrói as 4 seções da interface em sequência.

**Chama:**
- [[gui_ml_advanced.py#_create_model_card|_create_model_card()]] — 3 vezes (M1, M2, M3)

**Seções criadas:**
1. **📊 MODELOS TREINADOS** — cards RF_M1, RF_M2, RF_M3
2. **⚙️ TREINAR MODELOS** — botões + barra de progresso
3. **🔍 ANALISAR DECISÕES** — comboboxes + área de texto
4. **⚖️ CONFIGURAR PESOS** — 4 sliders N1-N4

---

## `_create_model_card(parent, model_name, config)` {#_create_model_card}

```python
def _create_model_card(
    self,
    parent: tk.Frame,
    model_name: str,       # "RF_M1", "RF_M2", "RF_M3"
    config: str            # descrição textual
) -> None:
```

**O que faz:** Cria card visual com nome, configuração, acurácia e data do treino.

**Chama:**
- [[gui_ml_advanced.py#_load_model_info|_load_model_info(model_name)]] — preenche acurácia e data a partir do JSON

**Armazena em:**
```python
self.model_cards["RF_M3"] = {
    "accuracy": tk.StringVar,   # "Acurácia: 94%"
    "date": tk.StringVar,       # "Data: 2026-04-14"
    "frame": tk.Frame
}
```

---

## `_load_model_info(model_name)` {#_load_model_info}

```python
def _load_model_info(self, model_name: str) -> None:
```

**O que faz:** Lê `ml_models/{model_name}_metadata.json` e atualiza as `StringVar` do card correspondente.

**Lê de:** `02-ML/ml_models/RF_M*_metadata.json`

**Chamado por:** [[gui_ml_advanced.py#_create_model_card|_create_model_card()]] e [[gui_ml_advanced.py#refresh|refresh()]]

---

## `_generate_features()` {#_generate_features}

```python
def _generate_features(self) -> None:
```

**O que faz:**
1. Lê valores dos sliders N1–N4
2. Normaliza pesos para somar 1.0
3. Define `cads.PESOS_NOTAS` com os novos pesos
4. Chama `cads.gerar_features_ml()`
5. Atualiza status label com total gerado

**Chama:**
- [[cads.py#gerar_features_ml|cads.gerar_features_ml()]]

**Modifica:**
- [[cads.py#PESOS_NOTAS|cads.PESOS_NOTAS]] — variável global

```python
# Lógica de normalização dos pesos
raw = {n: scale.get() for n, scale in self.weights.items()}
total = sum(raw.values())
normalized = {n: v / total for n, v in raw.items()}
cads.PESOS_NOTAS = {
    "n1": normalized["N1"],
    "n2": normalized["N2"],
    ...
}
```

---

## `_train_all_models()` {#_train_all_models}

```python
def _train_all_models(self) -> None:
```

**O que faz:** Atalho que chama `_train_models(["RF_M1", "RF_M2", "RF_M3"])`.

**Chama:** [[gui_ml_advanced.py#_train_models|_train_models()]]

---

## `_train_m3_only()` {#_train_m3_only}

```python
def _train_m3_only(self) -> None:
```

**O que faz:** Atalho que chama `_train_models(["RF_M3"])`.

**Chama:** [[gui_ml_advanced.py#_train_models|_train_models()]]

---

## `_train_models(model_names)` {#_train_models}

```python
def _train_models(self, model_names: list[str]) -> None:
```

**O que faz:** Pipeline completo de treino em thread separada (não trava GUI).

**Sequência:**

```python
# 1. Exportar features para CSV
cads.exportar_ml_csv()            # → [[cads.py#exportar_ml_csv]]

# 2. Carregar dataset
df = pd.read_csv("ml_dataset.csv")

# 3. Definir features por modelo
features_map = {
    "RF_M1": ["n1_norm"],
    "RF_M2": ["n1_norm", "n2_norm", "slope_notas", "variancia_notas"],
    "RF_M3": FEATURES_SEGURAS,    # 9 features sem leakage
}

# 4. Treinar cada modelo
for name in model_names:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    clf = RandomForestClassifier(
        n_estimators={"RF_M1": 100, "RF_M2": 150, "RF_M3": 200}[name]
    )
    clf.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, clf.predict(X_test))

# 5. Salvar
pickle.dump(clf, open(f"ml_models/{name}.pkl", "wb"))
json.dump(metadata, open(f"ml_models/{name}_metadata.json", "w"))
```

**Chama:**
- [[cads.py#exportar_ml_csv|cads.exportar_ml_csv()]]
- [[gui_ml_advanced.py#_show_training_summary|_show_training_summary()]]
- [[gui_ml_advanced.py#_load_model_info|_load_model_info()]] — atualiza cards após treino

**Ver também:** [[Pipeline de Treinamento]], [[Modelos RF (M1-M2-M3)]]

---

## `_analyze_decision()` {#_analyze_decision}

```python
def _analyze_decision(self) -> None:
```

**O que faz:** Busca features do aluno+matéria selecionados e exibe análise detalhada no widget de texto.

**Output formatado:**
```
═══ ANÁLISE: João Silva / Matemática ═══

INFORMAÇÕES:
  Aluno:   João Silva
  Matéria: Matemática
  Série:   2º Médio

NOTAS:
  N1: 7.0 (norm: 0.70)  N2: 6.5 (norm: 0.65)
  N3: 8.0 (norm: 0.80)  N4: —

FEATURES ML:
  slope_notas:    +0.43  → Tendência positiva (melhorando)
  variancia_notas: 0.12  → Aluno consistente

RESULTADO:
  Status real: Aprovado
```

**Chama:**
- [[cads.py#get_conn|cads.get_conn()]] — SELECT em `ml_features`
- [[gui_ml_advanced.py#_interpret_slope|_interpret_slope(valor)]]
- [[gui_ml_advanced.py#_interpret_variance|_interpret_variance(valor)]]

---

## `_interpret_slope(valor)` {#_interpret_slope}

```python
def _interpret_slope(self, valor: float) -> str:
```

| Valor | Retorna |
|---|---|
| > 0.20 | `"Tendência positiva (melhorando)"` |
| 0 a 0.20 | `"Estável ou levemente melhorando"` |
| -0.20 a 0 | `"Levemente piorando"` |
| < -0.20 | `"Tendência negativa (piorando)"` |

**Chamado por:** [[gui_ml_advanced.py#_analyze_decision|_analyze_decision()]]

---

## `_interpret_variance(valor)` {#_interpret_variance}

```python
def _interpret_variance(self, valor: float) -> str:
```

| Valor | Retorna |
|---|---|
| < 0.15 | `"Aluno consistente"` |
| 0.15–0.30 | `"Variação moderada"` |
| > 0.30 | `"Alta inconsistência"` |

**Chamado por:** [[gui_ml_advanced.py#_analyze_decision|_analyze_decision()]]

---

## `_show_training_summary(results)` {#_show_training_summary}

```python
def _show_training_summary(self, results: dict) -> None:
```

**O que faz:** Abre popup `messagebox` com acurácia de cada modelo treinado.

**Chamado por:** [[gui_ml_advanced.py#_train_models|_train_models()]] ao final do treino

---

## `refresh()` {#refresh}

```python
def refresh(self) -> None:
```

**O que faz:** Recarrega comboboxes de Aluno e Matéria com dados atuais do banco.

**Chamado por:** [[gui_escola.py#_show_page|App._show_page("ml")]] — sempre que a página é exibida
