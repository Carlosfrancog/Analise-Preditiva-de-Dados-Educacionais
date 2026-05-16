---
tags: [artigo, feature-engineering, notas, normalizacao, bimestral]
aliases: [n1 n3 norm — Notas Bimestrais, n1 n2 n3 — Notas Normalizadas, Notas Normalizadas]
created: 2026-05-16
---

# n1_norm, n2_norm, n3_norm — Notas Bimestrais Normalizadas

[← Índice](<../INDEX - ARTIGO.md>) | [[Visão Geral das 9 Features]] | [[n2 norm — Feature Dominante]] | [[media pond norm — Feature Removida]]

---

## 1. Definição e Fórmula

As três features representam as notas bimestrais divididas por 10 para normalização no intervalo [0,1]:

```python
# cads.py — gerar_features_ml()
n1_norm = nota_bimestre_1 / 10.0   # Nota do 1º bimestre
n2_norm = nota_bimestre_2 / 10.0   # Nota do 2º bimestre
n3_norm = nota_bimestre_3 / 10.0   # Nota do 3º bimestre (ausente → 0.0)
```

**Escala original:** 0 a 10 (sistema decimal brasileiro)
**Escala normalizada:** 0.0 a 1.0

---

## 2. Papel de Cada Nota no Pipeline

| Feature | Momento de Disponibilidade | Modelos que usam |
|---|---|---|
| `n1_norm` | Após 1º bimestre | M1, M2, M3 |
| `n2_norm` | Após 2º bimestre | M2, M3 |
| `n3_norm` | Após 3º bimestre | M3 |

> **M1 usa apenas n1_norm + serie_num_norm** (GUI) — as demais são 0.0 no treinamento M1 via `gui_ml_advanced.py`.
> Em `train_simple.py`, todos os 3 modelos são treinados com as **mesmas 9 features** (n3 pode ser 0.0 para alunos sem nota N3 ainda).

---

## 3. Comportamento Quando Nota Ausente

```python
# cads.py — gerar_features_ml()
n3 = row['n3'] or 0  # None/NULL → 0.0
n3_norm = n3 / 10.0  # resultado: 0.0 para notas ausentes
```

**Problema:** 0.0 é ambíguo — pode significar "nota ausente" ou "nota zero". O modelo não distingue esses casos. Um aluno com n3=0 (zero real) e um aluno sem n3 recebem a mesma representação.

---

## 4. Feature Importance por Modelo

```
M1: n1_norm → dominante (único dado disponível)
M2: n2_norm > n1_norm (n2 captura evolução)
M3: n2_norm (32.3%) > pct_materias_ok (21.5%) > slope (12.3%) > n3_norm (8.7%)
```

`n3_norm` tem importância de ~8.7% no M3 — menos que n2 porque:
- Alunos com status definido já mostravam tendência clara em n1/n2
- slope_notas resume a trajetória n1→n2→n3 de forma mais compacta

---

## 5. Por Que n4_norm Foi Removida

`n4_norm` (4º bimestre) foi removida por data leakage — correlação de Pearson r=0.91 com `status_encoded`. O 4º bimestre ocorre **após** a definição do status final, tornando-a um proxy direto do target.

`n3_norm` permanece porque o status final é definido pela **média dos 4 bimestres**, não disponível no 3º bimestre.

Ver: [[n4 norm — Feature Removida]] | [[Data Leakage — Conceito e Impacto]]

---

## 6. Normalização vs Escala Original

A escolha de dividir por 10 (em vez de min-max ou z-score) é deliberada:

| Abordagem | Vantagem | Desvantagem |
|---|---|---|
| `/10` (atual) | Interpretável, estável entre datasets | Pressupõe escala 0-10 fixa |
| Min-max | Usa todo o range [0,1] | Depende do dataset (treino ≠ produção) |
| Z-score | Compatível com dados fora do range | Perde interpretabilidade |

Para o contexto escolar brasileiro (notas 0-10), `/10` é a escolha correta.

---

## 7. Dado Real do Sistema

No `escola.db`, as notas ficam na tabela `notas`:

```sql
CREATE TABLE notas (
    id      INTEGER PRIMARY KEY,
    aluno_id INTEGER,
    materia_id INTEGER,
    n1 REAL, n2 REAL, n3 REAL, n4 REAL,
    media_pondP REAL,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
);
```

`gerar_features_ml()` faz JOIN de `alunos`, `notas` e `turmas` para calcular as features.

---

## Links

- [[Visão Geral das 9 Features]]
- [[n2 norm — Feature Dominante]]
- [[n4 norm — Feature Removida]]
- [[media pond norm — Feature Removida]]
- [[Data Leakage — Conceito e Impacto]]
- [[M1 — Modelo Precoce]]
- [[M3 — Modelo de Produção (Após N3)]]
