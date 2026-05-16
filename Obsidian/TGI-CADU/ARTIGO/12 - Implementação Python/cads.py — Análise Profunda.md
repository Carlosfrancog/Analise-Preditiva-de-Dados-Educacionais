---
tags: [artigo, implementacao, cads, python, core, banco]
created: 2026-05-16
---

# cads.py — Análise Profunda do Módulo Core

[[INDEX - ARTIGO|← Índice]] | [[Arquitetura Modular — Visão Geral]] | [[gui ml integration py — Motor de Predição]] | [[Mapeamento Teoria-Código]]

---

## 1. Papel no Sistema

`cads.py` é a **camada de fundação** do EduPredict:
- Define o caminho do banco de dados (`DB_PATH`)
- Fornece `get_conn()` para todas as queries
- Implementa todo o CRUD (Create, Read, Update, Delete)
- Implementa a geração de features ML (`gerar_features_ml()`)
- Implementa as funções matemáticas auxiliares (`_slope`, `_variancia`)

Todos os outros módulos importam `cads`. É o único módulo que conhece o schema do banco.

---

## 2. DB_PATH — Decisão de Design

```python
# cads.py
from pathlib import Path
DB_PATH = str(Path(__file__).parent / "escola.db")
```

O banco fica no **mesmo diretório que cads.py** (`01-CORE/escola.db`). Isso é conveniente para deployment simples mas cria acoplamento — qualquer módulo que importa `cads` usa automaticamente esse banco.

**Consequência:** não é possível usar um banco diferente sem modificar `cads.py`. Isso dificulta:
- Testes com bancos separados (banco de teste vs produção)
- Multi-tenancy (múltiplas escolas em instalações separadas)
- Ver [[Débitos Técnicos Identificados#DT-02]]

---

## 3. `_slope(vals)` — Implementação

```python
def _slope(vals):
    """Regressão linear simples sobre lista de notas."""
    n = len(vals)
    if n < 2:
        return 0.0
    xs = list(range(n))
    xm = sum(xs) / n
    ym = sum(vals) / n
    num = sum((x - xm) * (y - ym) for x, y in zip(xs, vals))
    den = sum((x - xm) ** 2 for x in xs)
    return num / den if den != 0 else 0.0
```

**Análise:**
- Correto matematicamente — implementa o estimador OLS de mínimos quadrados
- `xs = list(range(n))` → índices 0, 1, 2, 3 (não 1, 2, 3, 4 — indiferente para o slope)
- Retorna 0,0 para n < 2 e den == 0 (caso constante) — defensivo
- Entradas esperadas: valores já normalizados em [0, 1]

**Inconsistência crítica:** `gui_ml_integration.py` usa `slope_pct = ((n2-n1)/n1)*100` em vez desta função. Ver [[Débitos Técnicos Identificados#DT-01]].

---

## 4. `_variancia(vals)` — Implementação Inferida

```python
def _variancia(vals):
    """Variância populacional das notas normalizadas."""
    n = len(vals)
    if n < 2:
        return 0.0
    ym = sum(vals) / n
    return sum((y - ym) ** 2 for y in vals) / n
```

Variância **populacional** (divisão por n, não por n-1). Para o contexto (todas as notas disponíveis de um aluno em uma matéria), população é o correto — não é uma amostra de um universo maior.

---

## 5. `gerar_features_ml()` — Estrutura Esperada

Esta é a função mais complexa do sistema. Executa:

```python
def gerar_features_ml():
    conn = get_conn()
    
    # Query principal — busca todas as notas por (aluno, matéria)
    rows = conn.execute("""
        SELECT 
            a.id as aluno_id,
            a.sala_id,
            s.serie,
            n.materia_id,
            n.n1, n.n2, n.n3, n.n4
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN salas s ON a.sala_id = s.id
        ORDER BY a.id, n.materia_id
    """).fetchall()
    
    for row in rows:
        # Normalizar notas
        n1_norm = row['n1'] / 10.0 if row['n1'] else None
        ...
        
        # Features derivadas
        notas_disponíveis = [n/10 for n in [row['n1'], row['n2'], row['n3']] if n]
        slope_notas = _slope(notas_disponíveis)
        variancia_notas = _variancia(notas_disponíveis)
        
        # Features contextuais (subqueries)
        media_geral_aluno = _get_media_geral(row['aluno_id'], conn)
        pct_materias_ok = _get_pct_ok(row['aluno_id'], conn)
        media_turma_norm = _get_media_turma(row['sala_id'], conn)
        serie_num_norm = _normalize_serie(row['serie'])
        
        # Features leaky (calculadas mas não usadas no treino)
        media_pond_norm = _calc_media_pond(row['n1'], row['n2'], row['n3'], row['n4'])
        
        # Target
        status_encoded = _encode_status(media_pond_norm)
        
        # INSERT/UPDATE em ml_features
        conn.execute("INSERT OR REPLACE INTO ml_features ...", (...))
    
    conn.commit()
```

A função executa O(n_alunos × n_materias) subqueries para features contextuais — potencial gargalo de performance para datasets grandes.

---

## 6. Schema da Tabela `ml_features`

```sql
CREATE TABLE IF NOT EXISTS ml_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    materia_id INTEGER NOT NULL,
    n1_norm REAL, n2_norm REAL, n3_norm REAL,
    n4_norm REAL,           -- leakage — não entra no treino
    slope_notas REAL,
    variancia_notas REAL,
    media_geral_aluno REAL,
    pct_materias_ok REAL,
    media_turma_norm REAL,
    serie_num_norm REAL,
    media_pond_norm REAL,   -- leakage — não entra no treino
    status_encoded INTEGER, -- target: 0=Reprovado, 1=Recuperação, 2=Aprovado
    UNIQUE(aluno_id, materia_id),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
);
```

---

## 7. Outras Funções do cads.py

| Função | Propósito |
|---|---|
| `get_conn()` | Retorna conexão SQLite com row_factory=sqlite3.Row |
| `add_aluno(nome, sala_id)` | Insere aluno no banco |
| `get_alunos(sala_id)` | Lista alunos de uma sala |
| `save_notas(aluno_id, materia_id, n1, n2, n3, n4)` | Salva/atualiza notas |
| `get_notas(aluno_id)` | Retorna todas as notas de um aluno |
| `get_salas()` | Lista todas as salas/turmas |
| `gerar_features_ml()` | Calcula e persiste todas as features ML |

---

## 8. Qualidade do Código

**Positivo:**
- Funções auxiliares pequenas e focadas (`_slope`, `_variancia`)
- Uso de `sqlite3.Row` para acesso por nome de coluna
- Lógica matemática correta

**Negativo:**
- DB_PATH hardcoded (sem injeção de dependência)
- Sem testes unitários documentados
- `gerar_features_ml()` provavelmente muito longa (monolítica)
- Mistura lógica de negócio (cálculo de status) com acesso a dados

---

## Links

- [[Arquitetura Modular — Visão Geral]]
- [[slope notas — Tendência Temporal]]
- [[variancia notas — Consistência]]
- [[Pipeline Completo de Treinamento]]
- [[Débitos Técnicos Identificados]]
- [[Mapeamento Teoria-Código]]
