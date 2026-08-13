---
tags:
  - guia
  - contribuicao
  - tgi-codes
created: 2026-05-13
---

# Como Contribuir — Adicionar Módulos e Documentação

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## Estrutura de Categorias

| Pasta | Para quê |
|---|---|
| `01-CORE/` | Lógica de banco de dados ou negócio fundamental |
| `02-ML/` | Algoritmos, treino, predição, pipeline de dados |
| `03-GUI/` | Telas e interação com o usuário |
| `04-DOCS/` | Documentação em markdown |
| `05-TESTS/` | Testes unitários e scripts de debug |
| `06-OUTPUT/` | Arquivos gerados — **não commitar** |

---

## Adicionando uma Nova Página GUI

### 1. Criar o arquivo

```
03-GUI/gui_minha_pagina.py
```

### 2. Herdar de `BasePage`

```python
from gui_predicoes import BasePage

class MinhaPagina(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build()

    def _build(self):
        # Monta a UI aqui
        pass

    def refresh(self):
        # Chamado quando a página é exibida
        pass
```

### 3. Registrar em `gui_escola.py`

```python
from gui_minha_pagina import MinhaPagina

# Na lista de páginas:
(MinhaPagina, "minha_pagina"),
```

---

## Adicionando um Novo Modelo ML

### 1. Criar script de treino em `02-ML/`

```python
# 02-ML/model_xgboost.py
from xgboost import XGBClassifier
import cads

def train_xgboost():
    df = pd.read_csv("02-ML/ml_dataset.csv")
    # ... treino
```

### 2. Salvar com padrão de nomenclatura

```
02-ML/ml_models/XGB_M3.pkl
02-ML/ml_models/XGB_M3_metadata.json
```

### 3. Atualizar `gui_ml_advanced.py`

Adicionar card e botão de treino para o novo modelo.

---

## Adicionando uma Nova Feature

### 1. Calcular em `cads.py`

```python
def gerar_features_ml():
    # ... código existente
    # Adicionar nova feature:
    nova_feature = calcular_nova_feature(aluno_id)
    INSERT INTO ml_features (nova_feature) VALUES (?)
```

### 2. Adicionar à lista de features seguras

Verificar se não há [[Data Leakage]] — correlação ≥ 0.85 com target.

### 3. Atualizar documentação

Adicionar na nota [[Features e Cálculos]] com fórmula e intervalo.

---

## Convenções de Código

- Funções privadas (internas à classe): prefixo `_` (ex: `_build`, `_train`)
- Páginas GUI: sufixo `Page` (ex: `MLAdvancedPage`)
- Arquivos de módulo: prefixo descritivo (ex: `gui_`, `ml_`)
- Testes: prefixo `test_` em `05-TESTS/`

---

## Checklist ao Adicionar Módulo

- [ ] Arquivo na pasta correta (`01` a `05`)
- [ ] Nomenclatura seguindo o padrão
- [ ] Função `refresh()` se for página GUI
- [ ] Sem data leakage nas novas features
- [ ] Teste em `05-TESTS/`
- [ ] Documentação atualizada (este vault ou `04-DOCS/`)

---

## Links Relacionados

- [[Arquitetura do Sistema]] — diagrama de dependências
- [[Visão Geral]] — estrutura de pastas completa
- [[Roadmap]] — funcionalidades planejadas para contribuir
