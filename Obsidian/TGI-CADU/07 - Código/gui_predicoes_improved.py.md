---
tags:
  - codigo
  - gui
  - predicoes
  - tgi-codes
created: 2026-05-13
---

# `gui_predicoes_improved.py` — Documentação de Código

[[INDEX - Código|← Índice de Código]] | [[MOC - TGI-CODES|← MOC]]

> [!NOTE] Localização
> `03-GUI/gui_predicoes_improved.py` | Importado por: [[gui_escola.py#_build_ui|gui_escola.py]] como `PredictionPage`

---

## Imports e Dependências

```python
from gui_ml_integration import DisciplinePerformanceAnalyzer, MLModelLoader
# → [[gui_ml_integration.py#DisciplinePerformanceAnalyzer]]
# → [[gui_ml_integration.py#MLModelLoader]]

from gui_predicoes import BasePage   # classe base
```

---

## `class PredictionPageImproved(BasePage)` {#PredictionPageImproved}

```python
class PredictionPageImproved(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Predicoes de Desempenho", "[Pred]")
        self.ml_loader = MLModelLoader()    # → [[gui_ml_integration.py#MLModelLoader]]
        self.aluno_var = tk.StringVar()
        self.aluno_data = {}    # nome → aluno_id
        self.sala_map   = {}    # nome → sala_id
        self.analise_atual = None
        self.filter_var = tk.StringVar(value="all")
        self._build_ui()
```

**Responsabilidade:** Dashboard de predições por aluno. Exibe cards por disciplina com notas, status ML e prognóstico de evolução.

**Instancia no `__init__`:**
- [[gui_ml_integration.py#MLModelLoader|MLModelLoader()]] — carrega modelos RF_M* ao abrir a página

---

## `_build_ui()` {#_build_ui}

```python
def _build_ui(self) -> None:
```

**O que constrói:**
- Combobox de **Sala** → filtra alunos
- Combobox de **Aluno** → seleciona quem analisar
- Botões de **Filtro:** Todos / Aprovados / Recuperação / Reprovados
- `result_frame` — área de scroll com cards de disciplinas

---

## `refresh()` {#refresh}

```python
def refresh(self) -> None:
```

**O que faz:** Recarrega lista de salas e alunos do banco.

**Chamado por:** [[gui_escola.py#_show_page|App._show_page("predicoes")]] — sempre que a página é exibida

**Chama:**
- [[cads.py#get_salas|cads.get_salas()]]
- [[cads.py#get_alunos|cads.get_alunos(sala_id)]]

---

## `_load_aluno()` {#_load_aluno}

```python
def _load_aluno(self, event=None) -> None:
```

**O que faz:** Disparado quando o usuário seleciona um aluno no combobox. Executa a análise completa e renderiza os cards.

**Sequência:**

```python
# 1. Obter aluno_id do combobox
aluno_id = self.aluno_data[self.aluno_var.get()]

# 2. Analisar com ML
self.analise_atual = DisciplinePerformanceAnalyzer.analyze_student(
    db_path=cads.DB_PATH,
    aluno_id=aluno_id,
    model_loader=self.ml_loader
)
# → [[gui_ml_integration.py#analyze_student]]

# 3. Renderizar cards
self._render_cards(self.analise_atual)
```

**Chama:**
- [[gui_ml_integration.py#analyze_student|DisciplinePerformanceAnalyzer.analyze_student()]]
- [[gui_predicoes_improved.py#_render_cards|_render_cards()]]

---

## `_render_cards(analise)` {#_render_cards}

```python
def _render_cards(self, analise: dict) -> None:
```

**O que faz:** Itera sobre `analise["disciplinas"]` e cria um card por matéria com:
- Nome da matéria e status colorido (verde/laranja/vermelho)
- Notas N1-N4
- Média atual
- Prognóstico (vai melhorar / vai piorar / estável)
- Confiança da predição em `%`

**Filtra por:** `self.filter_var` — "all", "aprovados", "recuperacao", "reprovados"

**Chama:** [[gui_predicoes_improved.py#_create_discipline_card|_create_discipline_card()]]

---

## `_create_discipline_card(parent, disc_data)` {#_create_discipline_card}

```python
def _create_discipline_card(self, parent: tk.Frame, disc_data: dict) -> None:
```

**Input esperado** (formato de `disc_data`):
```python
{
    "nome": "Matemática",
    "n1": 7.0, "n2": 6.5, "n3": 8.0, "n4": None,
    "media_atual": 7.1,
    "status_pred": 2,
    "status_label": "Aprovado",
    "confianca": 0.87,
    "slope": 0.43,
    "prognostico": "vai_melhorar",
    "cor": "#2E7D32"
}
```

**Chamado por:** [[gui_predicoes_improved.py#_render_cards|_render_cards()]]

---

## `_apply_filter(filtro)` {#_apply_filter}

```python
def _apply_filter(self, filtro: str) -> None:
    # filtro: "all" | "aprovados" | "recuperacao" | "reprovados"
```

**O que faz:** Redefine `self.filter_var` e chama `_render_cards()` com os dados atuais.

**Chamado por:** Botões de filtro no topo da página

---

## `BasePage` (re-exportada)

> [!INFO] Nota de importação
> `gui_predicoes_improved.py` exporta `BasePage` importada de `gui_predicoes.py`. Por isso `gui_ml_advanced.py` faz:
> ```python
> from gui_predicoes_improved import BasePage
> ```
> Em vez de importar diretamente de `gui_predicoes.py`.
