---
tags:
  - arquitetura
  - banco-de-dados
  - tgi-codes
created: 2026-05-13
---

# Modelo de Dados

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## Tabela Principal: `ml_features`

É a tabela central gerada por `cads.gerar_features_ml()`. Cada linha representa um par (aluno × matéria).

```sql
CREATE TABLE ml_features (
    -- Identificação
    aluno_id       INTEGER,
    materia_id     INTEGER,
    aluno_nome     TEXT,
    materia_nome   TEXT,
    sala_nome      TEXT,
    serie_num      INTEGER,

    -- Notas brutas (escala 0–10)
    n1   REAL,
    n2   REAL,
    n3   REAL,
    n4   REAL,

    -- Notas normalizadas (escala 0–1)
    n1_norm   REAL,
    n2_norm   REAL,
    n3_norm   REAL,
    n4_norm   REAL,

    -- Features para ML
    media_ponderada     REAL,   -- média N1-N4 com pesos configuráveis
    media_pond_norm     REAL,   -- ⚠️ DATA LEAKAGE — removida do treino
    media_geral_aluno   REAL,   -- média do aluno em todas as matérias
    slope_notas         REAL,   -- tendência linear (-1 a +1)
    variancia_notas     REAL,   -- inconsistência (0 a 1)
    serie_num_norm      REAL,   -- série normalizada
    pct_materias_ok     REAL,   -- % de matérias aprovadas
    media_turma_norm    REAL,   -- média da turma normalizada

    -- Target
    status_encoded  INTEGER,   -- 0=Reprovado, 1=Recuperação, 2=Aprovado
    status_label    TEXT,

    -- Metadata
    gerado_em   TIMESTAMP
);
```

> [!WARNING] Data Leakage
> `media_pond_norm` e `n4_norm` **não devem** ser usadas no treinamento — têm correlação ≥ 0.91 com o target. Ver [[Data Leakage]].

---

## Arquivo de Metadata do Modelo

Cada modelo treinado gera um `RF_M*_metadata.json`:

```json
{
    "accuracy": 0.94,
    "f1": 0.940,
    "n_features": 9,
    "features": [
        "n1_norm", "n2_norm", "n3_norm",
        "slope_notas", "variancia_notas",
        "media_geral_aluno", "serie_num_norm",
        "pct_materias_ok", "media_turma_norm"
    ],
    "n_samples_train": 12490,
    "n_samples_test": 3123,
    "date": "2026-04-14 15:32:00",
    "confusion_matrix": [[...], [...], [...]]
}
```

---

## Arquivos Gerados pelo Sistema

| Arquivo | Gerado por | Conteúdo |
|---|---|---|
| `escola.db` | `cads.init_db()` | Banco SQLite com alunos, notas, matérias |
| `ml_dataset.csv` | `cads.exportar_ml_csv()` | Dataset flat com as 9 features |
| `RF_M*.pkl` | `train_simple.py` | Modelo Random Forest serializado |
| `RF_M*_metadata.json` | `train_simple.py` | Métricas e lista de features |
| `training_summary.json` | `train_simple.py` | Resumo do último treinamento |
| `01_debug_results.json` | `run_ml_pipeline.py` | Resultados das 10 validações |

---

## Links Relacionados

- [[Features e Cálculos]] — como cada feature é calculada
- [[Data Leakage]] — por que media_pond_norm foi removida
- [[Arquitetura do Sistema]] — visão geral dos componentes
