---
tags:
  - codigo
  - gui
  - tgi-codes
created: 2026-05-13
---

# `gui_escola.py` — Documentação de Código

[[INDEX - Código|← Índice de Código]] | [[MOC - TGI-CODES|← MOC]]

> [!NOTE] Localização
> `03-GUI/gui_escola.py` | **Entry point da aplicação** — `python gui_escola.py`

---

## Imports e Dependências

```python
import cads                                           # → [[cads.py]]
from gui_predicoes_improved import PredictionPageImproved  # → [[gui_predicoes_improved.py]]
from gui_predicoes import SalasPage, BasePage         # → gui_predicoes.py
from gui_ml_advanced import MLAdvancedPage            # → [[gui_ml_advanced.py]]
```

---

## Constantes de Tema

```python
# Paleta de cores (Light Mode)
BG        = "#F0F4FF"   # fundo geral
SIDEBAR   = "#1A237E"   # sidebar escura
ACCENT    = "#3949AB"   # cor principal
SUCCESS   = "#2E7D32"   # verde
WARN      = "#E65100"   # laranja

# Fontes
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEAD  = ("Segoe UI", 12, "bold")
FONT_BODY  = ("Segoe UI", 10)
```

---

## `class App(tk.Tk)` {#App}

```python
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        cads.init_db()        # → [[cads.py#init_db]]
        self._build_ui()
        self._show_page("dashboard")
```

**Responsabilidade:** Janela principal da aplicação. Gerencia sidebar, navegação entre páginas e ciclo de vida.

**Chama:**
- [[cads.py#init_db|cads.init_db()]] — inicializa banco ao subir
- [[gui_escola.py#_build_ui|_build_ui()]] — monta layout
- [[gui_escola.py#_show_page|_show_page()]] — exibe página inicial

### `_build_ui()` {#_build_ui}

```python
def _build_ui(self) -> None:
```

**O que faz:** Cria sidebar com botões de navegação e instancia todas as páginas sobrepostas com `.place()`.

**Páginas instanciadas:**

| Chave | Classe | Arquivo |
|---|---|---|
| `"dashboard"` | `DashboardPage` | [[gui_escola.py#DashboardPage]] |
| `"alunos"` | `AlunosPage` | [[gui_escola.py]] |
| `"salas"` | `SalasPage` | `gui_predicoes.py` |
| `"materias"` | `MateriasPage` | [[gui_escola.py]] |
| `"notas"` | `NotasPage` | [[gui_escola.py]] |
| `"predicoes"` | `PredictionPageImproved` | [[gui_predicoes_improved.py]] |
| `"relatorio"` | `RelatorioPage` | [[gui_escola.py]] |
| `"ml"` | `MLAdvancedPage` | [[gui_ml_advanced.py]] |
| `"importar"` | `ImportarPage` | [[gui_escola.py]] |
| `"exportar"` | `ExportarPage` | [[gui_escola.py]] |

### `_show_page(key)` {#_show_page}

```python
def _show_page(self, key: str) -> None:
```

**O que faz:** Levanta a página solicitada com `.lift()` e chama `page.refresh()` se o método existir.

> [!TIP] refresh()
> Toda página deve implementar `refresh()` — é chamado sempre que a página é exibida, garantindo dados atualizados.

---

## `class BasePage(tk.Frame)` {#BasePage}

```python
class BasePage(tk.Frame):
    def __init__(self, parent, app, title="", icon=""):
```

**Responsabilidade:** Classe base com helpers de UI reutilizáveis. Todas as páginas herdam dela.

**Métodos utilitários:**

### `card(parent, **kwargs)` → `tk.Frame`
Retorna um Frame com borda sutil (highlightbackground). Usado para criar cards visuais.

```python
# Exemplo de uso em subclasse
c = self.card(self.some_frame)
c.pack(fill="x", padx=10)
```

### `btn(parent, text, cmd, color?, fg?)` → `tk.Button`
Cria botão padronizado com estilo flat, cursor hand2 e fonte `FONT_BTN`.

```python
b = self.btn(frame, "Salvar", self._salvar, color=SUCCESS)
b.pack(side="right")
```

### `stat_card(parent, label, value, color?)` → `tk.Frame`
Card de estatística com número grande + label pequeno. Usado no [[gui_escola.py#DashboardPage]].

---

## `class DashboardPage(BasePage)` {#DashboardPage}

```python
class DashboardPage(BasePage):
    def refresh(self) -> None:
```

**O que faz:** Exibe contadores (alunos, matérias, notas lançadas) e tabela de alunos por turma.

**Chama:**
- [[cads.py#get_conn|cads.get_conn()]] — consultas `COUNT(*)` diretas
- [[gui_escola.py#BasePage|BasePage.stat_card()]] — renderiza cada contador

```python
# Queries executadas em refresh()
SELECT COUNT(*) FROM alunos
SELECT COUNT(*) FROM materias
SELECT COUNT(*) FROM notas WHERE n1 IS NOT NULL

SELECT s.nome, s.codigo, COUNT(a.id) as cnt
FROM salas s LEFT JOIN alunos a ON a.sala_id=s.id
GROUP BY s.id ORDER BY s.id
```

---

## `class AlunosPage(BasePage)` {#AlunosPage}

**O que faz:** CRUD de alunos. Filtro por sala, adicionar individualmente ou gerar alunos genéricos em lote.

**Chama:**
- [[cads.py#get_alunos|cads.get_alunos(sala_id)]]
- [[cads.py#adicionar_aluno|cads.adicionar_aluno(nome, sala_id)]]
- [[cads.py#gerar_alunos_genericos|cads.gerar_alunos_genericos(qtd, sala_id)]]

---

## `class NotasPage(BasePage)` {#NotasPage}

**O que faz:** Grade de notas por aluno/sala. Permite editar N1–N4 inline e salvar.

**Chama:**
- [[cads.py#get_notas|cads.get_notas(aluno_id)]]
- [[cads.py#salvar_nota|cads.salvar_nota(...)]]
- [[cads.py#gerar_notas_aleatorias|cads.gerar_notas_aleatorias(...)]] — botão de teste

---

## `class ImportarPage` / `class ExportarPage`

**ImportarPage:** Lê arquivo Excel e importa notas para o banco via `openpyxl`.

**ExportarPage:** Chama [[cads.py|cads]] para gerar Excel com todas as notas e médias calculadas.
