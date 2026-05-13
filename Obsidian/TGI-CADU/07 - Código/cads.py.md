---
tags:
  - codigo
  - core
  - banco-de-dados
  - tgi-codes
created: 2026-05-13
---

# `cads.py` — Documentação de Código

[[INDEX - Código|← Índice de Código]] | [[MOC - TGI-CODES|← MOC]]

> [!NOTE] Localização
> `01-CORE/cads.py` | Importado por: [[gui_escola.py]], [[gui_ml_advanced.py]], [[gui_ml_integration.py]], [[train_simple.py]]

---

## Constantes Globais

```python
DB_PATH = str(Path(__file__).parent / "escola.db")

PESOS_NOTAS = {"n1": 0.20, "n2": 0.25, "n3": 0.25, "n4": 0.30}
# ↑ Modificado por [[gui_ml_advanced.py#_generate_features]] via sliders

SERIE_MAP = {"6F": 6, "7F": 7, "8F": 8, "9F": 9, "1M": 10, "2M": 11, "3M": 12}
SERIE_MIN, SERIE_MAX = 6, 12
```

---

## `get_conn()` {#get_conn}

```python
def get_conn() -> sqlite3.Connection:
```

**O que faz:** Abre e retorna uma conexão SQLite com `row_factory = sqlite3.Row` (acesso por nome de coluna).

**Chamado por:**
- [[gui_ml_integration.py#analyze_student|DisciplinePerformanceAnalyzer.analyze_student()]] — `conn = cads.get_conn()`
- [[gui_escola.py#DashboardPage|DashboardPage.refresh()]] — consultas de estatísticas
- Internamente por quase todas as funções de `cads.py`

> [!WARNING] Sempre fechar
> Toda função que chama `get_conn()` deve chamar `conn.close()` no final. Nunca deixar conexão aberta.

---

## `init_db()` {#init_db}

```python
def init_db() -> None:
```

**O que faz:** Cria todas as tabelas se não existirem e insere as salas padrão. Chama `_migrate_db()` ao final para compatibilidade com bancos antigos.

**Tabelas criadas:** `salas`, `alunos`, `materias`, `notas`, `ml_features`

**Chamado por:**
- [[gui_escola.py#App|App.__init__()]] — primeira linha após `super().__init__()`

**Chama:**
- [[cads.py#get_conn|get_conn()]]
- [[cads.py#_migrate_db|_migrate_db()]]

```python
# Uso típico
import cads
cads.init_db()
```

---

## `_migrate_db()` {#_migrate_db}

```python
def _migrate_db() -> None:
```

**O que faz:** Adiciona colunas novas à tabela `ml_features` em bancos criados antes de versões anteriores. Seguro rodar múltiplas vezes — ignora erros de coluna já existente.

**Colunas verificadas:** `gerado_em`, `media_ponderada`, `media_geral_aluno`, `slope_notas`, `variancia_notas`, `serie_num_norm`, `pct_materias_ok`, `media_turma_norm`

**Chamado por:**
- [[cads.py#init_db|init_db()]] — automaticamente ao inicializar

---

## `_slope(vals)` {#_slope}

```python
def _slope(vals: list[float | None]) -> float:
    # Retorna valor em [-1.0, +1.0]
```

**O que faz:** Regressão linear simples sobre uma lista de valores. Ignora `None`. Normaliza o coeficiente angular pelo slope máximo possível (notas 0→10 em N passos).

**Fórmula:**
```
slope_raw = Σ((x - x̄)(y - ȳ)) / Σ((x - x̄)²)
slope_norm = clamp(slope_raw / (10 / (n-1)), -1.0, +1.0)
```

**Chamado por:**
- [[cads.py#gerar_features_ml|gerar_features_ml()]] — calcula `slope_notas` para cada (aluno, matéria)
- [[gui_ml_integration.py#analyze_student|DisciplinePerformanceAnalyzer.analyze_student()]] — recalcula em tempo real

**Ver também:** [[Features e Cálculos#slope_notas|Documentação da feature slope_notas]]

---

## `_std(vals)` {#_std}

```python
def _std(vals: list[float | None]) -> float:
    # Retorna valor em [0.0, 1.0]
```

**O que faz:** Desvio padrão das notas não-nulas, normalizado para `[0, 1]` dividindo pelo desvio máximo possível (5.0).

**Fórmula:**
```
std = sqrt(Σ(v - mean)² / n)
variancia_norm = min(1.0, std / 5.0)
```

**Chamado por:**
- [[cads.py#gerar_features_ml|gerar_features_ml()]] — calcula `variancia_notas`
- [[gui_ml_integration.py#analyze_student|DisciplinePerformanceAnalyzer.analyze_student()]]

**Ver também:** [[Features e Cálculos#variancia_notas|Documentação da feature variancia_notas]]

---

## `gerar_features_ml(sala_id?)` {#gerar_features_ml}

```python
def gerar_features_ml(sala_id: int | None = None) -> tuple[int, dict]:
    # Retorna: (total_gerado, dict_estatísticas)
```

**O que faz:** Para cada par `(aluno × matéria)` com pelo menos uma nota, calcula as 9 features de ML e faz upsert em `ml_features`.

**Features geradas:**

| Feature | Cálculo |
|---|---|
| `n1_norm` … `n4_norm` | `nX / 10` |
| `media_ponderada` | soma ponderada com [[cads.py#PESOS_NOTAS\|PESOS_NOTAS]] |
| `slope_notas` | [[cads.py#_slope|_slope([n1, n2, n3, n4])]] |
| `variancia_notas` | [[cads.py#_std|_std([n1, n2, n3, n4])]] |
| `media_geral_aluno` | média de todas as matérias do aluno |
| `serie_num_norm` | `(serie - 6) / (12 - 6)` |
| `pct_materias_ok` | aprovadas / total |
| `media_turma_norm` | média da turma normalizada |

**Target calculado:**
```python
status = 0  # Reprovado   (media < 5)
status = 1  # Recuperação (5 ≤ media < 6)
status = 2  # Aprovado    (media ≥ 6)
```

**Chamado por:**
- [[gui_ml_advanced.py#_generate_features|MLAdvancedPage._generate_features()]] — via botão na GUI
- [[train_simple.py|train_simple.py]] — antes de exportar CSV

**Chama:**
- [[cads.py#get_conn|get_conn()]]
- [[cads.py#_slope|_slope()]]
- [[cads.py#_std|_std()]]

```python
# Uso
total, stats = cads.gerar_features_ml()
print(f"{total} features geradas")
# stats: {"aprovados": 250, "reprovados": 50, "recuperacao": 100}
```

---

## `exportar_ml_csv(path?)` {#exportar_ml_csv}

```python
def exportar_ml_csv(path: str = "ml_dataset.csv") -> str:
```

**O que faz:** Exporta a tabela `ml_features` para CSV. Inclui apenas colunas de features + target (sem IDs ou metadados).

**Chamado por:**
- [[gui_ml_advanced.py#_train_models|MLAdvancedPage._train_models()]] — gera CSV antes de treinar
- [[train_simple.py|train_simple.py]] — passo 2 do pipeline

---

## `get_alunos(sala_id?)` {#get_alunos}

```python
def get_alunos(sala_id: int | None = None) -> list[dict]:
```

**O que faz:** Retorna lista de alunos com JOIN em salas. Filtra por sala se `sala_id` fornecido.

**Campos retornados:** `id`, `nome`, `sala_id`, `matricula`, `sala_nome`, `sala_codigo`

**Chamado por:**
- [[gui_escola.py|AlunosPage.refresh()]]
- [[gui_ml_advanced.py#refresh|MLAdvancedPage.refresh()]]

---

## `get_notas(aluno_id)` {#get_notas}

```python
def get_notas(aluno_id: int) -> list[dict]:
```

**O que faz:** Retorna todas as notas de um aluno com JOIN em matérias.

**Campos retornados:** `id`, `aluno_id`, `materia_id`, `n1`, `n2`, `n3`, `n4`, `materia_nome`

**Chamado por:**
- [[gui_escola.py|NotasPage.refresh()]]

---

## `salvar_nota(aluno_id, materia_id, n1, n2, n3, n4)` {#salvar_nota}

```python
def salvar_nota(
    aluno_id: int, materia_id: int,
    n1: float, n2: float, n3: float, n4: float
) -> None:
```

**O que faz:** INSERT OR UPDATE (upsert) na tabela `notas`. Usa `ON CONFLICT DO UPDATE SET`.

**Chamado por:**
- [[gui_escola.py|NotasPage]] — ao salvar formulário de notas

---

## `adicionar_aluno(nome, sala_id)` {#adicionar_aluno}

```python
def adicionar_aluno(nome: str, sala_id: int) -> None:
```

**Chama:** [[cads.py#gerar_matricula|gerar_matricula(sala_id)]] para gerar matrícula automática.

---

## `adicionar_sala(nome, codigo)` {#adicionar_sala}

```python
def adicionar_sala(nome: str, codigo: str) -> None:
    # raises ValueError se nome ou código já existir
```

---

## `remover_sala(sala_id)` {#remover_sala}

```python
def remover_sala(sala_id: int) -> None:
    # raises ValueError se sala tiver alunos
```

**Proteção:** Verifica `COUNT(alunos)` antes de deletar. Lança `ValueError` com mensagem descritiva.
