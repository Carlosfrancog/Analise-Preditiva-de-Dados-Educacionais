---
tags: [artigo, feature-engineering, serie, nivel-escolar, normalizacao]
aliases: [serie num norm — Nível Escolar, serie num norm — Contexto Série]
created: 2026-05-16
---

# serie_num_norm — Nível Escolar Normalizado

[← Índice](<../INDEX - ARTIGO.md>) | [[Visão Geral das 9 Features]] | [[media turma norm — Referência de Turma]] | [[Análise Crítica do TGI]]

---

## 1. Definição e Mapeamento

`serie_num_norm` é a série/ano escolar codificada ordinalmente e normalizada para [0,1]:

```python
# cads.py — constante SALAS
SALAS = {
    "6º Fundamental": "6F",   # → serie_num = 0 → serie_num_norm = 0.00
    "7º Fundamental": "7F",   # → serie_num = 1 → serie_num_norm = 0.17
    "8º Fundamental": "8F",   # → serie_num = 2 → serie_num_norm = 0.33
    "9º Fundamental": "9F",   # → serie_num = 3 → serie_num_norm = 0.50
    "1º Médio":       "1M",   # → serie_num = 4 → serie_num_norm = 0.67
    "2º Médio":       "2M",   # → serie_num = 5 → serie_num_norm = 0.83
    "3º Médio":       "3M",   # → serie_num = 6 → serie_num_norm = 1.00
}

# Normalização: serie_num / 6 (7 séries, índices 0-6)
serie_num_norm = serie_index / 6.0
```

---

## 2. Papel no Modelo

A feature serve como **proxy de complexidade curricular**:

- Alunos do 6º Fundamental têm currículo menos exigente → menor risco esperado
- Alunos do 3º Médio têm currículo mais exigente + pressão do ENEM → maior risco
- O modelo aprende que a mesma nota 5.0 tem significados diferentes dependendo da série

---

## 3. Feature Importance

No M3, `serie_num_norm` aparece com ~5-7% de importância. É uma feature complementar — não domina mas refina a predição.

**No M1 (via GUI):** `serie_num_norm` é a **segunda feature** (ao lado de `n1_norm`), pois no início do ano é pouco se sabe sobre o aluno além da nota e da série.

---

## 4. O Problema do Hardcoding na GUI — DT-01

O débito técnico DT-01 inclui `serie_num_norm = 0.5` **hardcoded** na predição em tempo real:

```python
# gui_ml_integration.py — linhas 285-295 (código real)
features_pred = [n1, n2, 0, 0, slope, variancia, media_norm, 0.5, 0.5]
#                                                             ^^^
#                                               serie_num_norm=0.5 (fixo!)
```

`0.5` corresponde a `9º Fundamental` — todos os alunos são tratados como se fossem do 9º ano na predição em tempo real, independente da série real.

**Impacto:** Alunos do 6º Fundamental têm risco subestimado; alunos do 3º Médio têm risco subestimado também (9º ≠ 3M).

Ver: [[Débitos Técnicos Identificados]]

---

## 5. Viés Histórico — Análise Crítica

`serie_num_norm` é um proxy de nível escolar que **carrega viés histórico**:

Se historicamente alunos do 6º Fundamental têm mais reprovações (por qualquer razão — transição do fundamental I para II, adaptação), o modelo aprende a aumentar o risco para `serie_num_norm=0.0`. Isso pode criar um viés discriminatório circular.

Ver: [[Análise Crítica do TGI]] | [[Velasco 2022 — Análise Crítica de Sistemas EDM]]

---

## 6. Codificação Ordinal vs One-Hot

| Abordagem | Pressuposto | Adequada? |
|---|---|---|
| Ordinal /6 (atual) | 3M é "mais que" 6F de forma linear | Razoável — série tem ordem real |
| One-hot (7 variáveis) | Séries são categorias independentes | Mais precisa mas aumenta dimensão |
| Embedding | Séries têm relações não-lineares | Superdimensionamento para este problema |

A codificação ordinal é razoável porque a série tem ordem pedagógica real, mas pressupõe que a diferença 6F→7F é equivalente a 2M→3M, o que pode não ser verdade.

---

## Links

- [[Visão Geral das 9 Features]]
- [[media turma norm — Referência de Turma]]
- [[Débitos Técnicos Identificados]]
- [[Análise Crítica do TGI]]
- [[Velasco 2022 — Análise Crítica de Sistemas EDM]]
- [[M1 — Modelo Precoce]]
