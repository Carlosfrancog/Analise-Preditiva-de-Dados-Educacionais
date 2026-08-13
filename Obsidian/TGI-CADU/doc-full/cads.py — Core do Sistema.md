---
tags:
  - python
  - core
  - banco-de-dados
  - tgi-codes
created: 2026-05-13
---

# `cads.py` — Core do Sistema

[[MOC - TGI-CODES|← Voltar ao índice]]

> [!NOTE] Localização
> `01-CORE/cads.py` — Módulo central, importado por todos os outros.

---

## Responsabilidades

1. **Schema do banco de dados** SQLite (`escola.db`)
2. **CRUD** de alunos, matérias, salas e notas
3. **Cálculo das features de ML** (slope, variância, normalização)
4. **Exportação** do dataset para CSV

---

## Funções Principais

### Banco de Dados

| Função | Descrição |
|---|---|
| `init_db()` | Cria todas as tabelas se não existirem |
| `get_salas()` | Retorna lista de salas |
| `get_alunos(sala_id?)` | Lista alunos, opcionalmente filtrado por sala |
| `get_materias()` | Lista matérias |
| `get_notas(aluno_id, materia_id?)` | Retorna notas de um aluno |
| `save_nota(...)` | Insere ou atualiza nota |

---

### Features de ML

| Função | Descrição |
|---|---|
| `_slope(vals)` | Regressão linear → tendência das notas |
| `_std(vals)` | Desvio padrão → inconsistência |
| `gerar_features_ml()` | Calcula e insere as 9 features em `ml_features` |
| `exportar_ml_csv(path?)` | Salva `ml_features` em CSV |
| `get_ml_stats()` | Retorna estatísticas do dataset |

---

### Variável Global de Pesos

```python
# Pesos padrão (podem ser alterados pela GUI)
PESOS_NOTAS = {
    "n1": 0.20,
    "n2": 0.25,
    "n3": 0.25,
    "n4": 0.30
}
```

A GUI de ML avança altera `PESOS_NOTAS` antes de chamar `gerar_features_ml()`.

---

## Tabelas do Banco

```sql
alunos     (id, nome, sala_id, serie)
materias   (id, nome)
salas      (id, nome, serie_num)
notas      (id, aluno_id, materia_id, n1, n2, n3, n4)
ml_features (... 9 features + target + metadata)
```

---

## Como Chamar as Funções

```python
import cads

# Inicializar banco
cads.init_db()

# Listar dados
alunos = cads.get_alunos()
notas = cads.get_notas(aluno_id=5)

# Gerar features para ML
total, stats = cads.gerar_features_ml()
print(f"{total} features geradas")

# Exportar para CSV
cads.exportar_ml_csv("02-ML/ml_dataset.csv")
```

---

## Links Relacionados

- [[Modelo de Dados]] — schema completo da tabela `ml_features`
- [[Features e Cálculos]] — detalhes de slope, variância e normalização
- [[Arquitetura do Sistema]] — como cads.py se encaixa no sistema
