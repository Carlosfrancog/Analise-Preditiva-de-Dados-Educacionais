---
tags:
  - ml
  - features
  - calculos
  - tgi-codes
created: 2026-05-13
---

# Features e Cálculos

[[MOC - TGI-CODES|← Voltar ao índice]]

> [!NOTE] Onde está o código?
> - Geração: `cads.py` → função `gerar_features_ml()` (~linha 400)
> - Uso em tempo real: `gui_ml_integration.py` → função `analyze_student()` (~linha 200)

---

## Grupo 1: Notas Normalizadas

### `n1_norm`, `n2_norm`, `n3_norm`, `n4_norm`

**Fórmula:** `nX_norm = NX / 10`

**Intervalo:** `[0, 1]`

> [!WARNING] n4_norm removida do treino
> `n4_norm` tem correlação 0.91 com o target — ela **prevê diretamente** o resultado final, causando [[Data Leakage]]. É usada apenas para análise pós-hoc.

---

## Grupo 2: Tendência e Consistência

### `slope_notas` — Tendência Linear

Mede se as notas do aluno estão **melhorando** (+) ou **piorando** (-) ao longo dos bimestres.

**Fórmula:** Regressão linear simples sobre os valores de N1…N3 (ou N4 se disponível).

```python
# Implementação em cads.py → _slope(vals)
# Regressão linear: y = a*x + b
# slope = a (coeficiente angular)
```

**Intervalo:** `[-1, +1]`

| Valor | Interpretação |
|---|---|
| > +0.20 | Tendência positiva forte (melhorando) |
| 0 a +0.20 | Estável ou levemente melhorando |
| -0.20 a 0 | Levemente piorando |
| < -0.20 | Tendência negativa (piorando) |

---

### `variancia_notas` — Consistência

Mede o **desvio padrão** das notas — quão inconsistente é o desempenho do aluno.

**Fórmula:** `variancia_notas = std(N1, N2, N3) / 10`

**Intervalo:** `[0, 1]`

| Valor | Interpretação |
|---|---|
| Próximo de 0 | Aluno consistente |
| Próximo de 1 | Aluno muito inconsistente |

---

## Grupo 3: Contexto

### `media_geral_aluno` — Desempenho Geral

Média ponderada do aluno em **todas as matérias**, não só a matéria em análise.

**Fórmula:** `Σ(media_pond_materia) / nº_materias`

---

### `serie_num_norm` — Série Escolar

Série do aluno normalizada para o intervalo `[0, 1]`.

**Fórmula:** `(serie_num - serie_min) / (serie_max - serie_min)`

Onde séries vão de 6º Fundamental (6F) ao 3º Médio (3M).

---

### `pct_materias_ok` — Aprovação nas Matérias

Percentual de matérias em que o aluno já está aprovado (status ≥ 6).

**Fórmula:** `qtd_aprovadas / qtd_total_materias`

**Intervalo:** `[0, 1]`

---

### `media_turma_norm` — Nível da Turma

Média normalizada da turma na matéria em análise — fornece contexto sobre o nível da classe.

---

## Média Ponderada (usada no target)

**Pesos padrão:**

| Nota | Peso |
|---|---|
| N1 | 20% |
| N2 | 25% |
| N3 | 25% |
| N4 | 30% |

**Fórmula:** `media_pond = 0.20*N1 + 0.25*N2 + 0.25*N3 + 0.30*N4`

> [!INFO] Pesos configuráveis
> Os pesos podem ser alterados via sliders na página ML da GUI. O sistema normaliza automaticamente para somar 1.0.

---

## Resumo das 9 Features Seguras

| Feature | Intervalo | Descrição |
|---|---|---|
| `n1_norm` | [0, 1] | Nota 1 normalizada |
| `n2_norm` | [0, 1] | Nota 2 normalizada |
| `n3_norm` | [0, 1] | Nota 3 normalizada |
| `slope_notas` | [-1, +1] | Tendência das notas |
| `variancia_notas` | [0, 1] | Inconsistência |
| `media_geral_aluno` | [0, 10] | Desempenho geral |
| `serie_num_norm` | [0, 1] | Série escolar |
| `pct_materias_ok` | [0, 1] | % matérias aprovadas |
| `media_turma_norm` | [0, 1] | Nível da turma |

---

## Links Relacionados

- [[Modelos RF (M1-M2-M3)]] — quais features cada modelo usa
- [[Data Leakage]] — features que foram removidas do treino
- [[Modelo de Dados]] — schema da tabela ml_features
