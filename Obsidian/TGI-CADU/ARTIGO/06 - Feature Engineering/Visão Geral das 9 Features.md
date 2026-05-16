---
tags: [artigo, feature-engineering, features, overview, ml]
created: 2026-05-16
---

# Visão Geral das 9 Features de Entrada

[[INDEX - ARTIGO|← Índice]] | [[slope notas — Tendência Temporal]] | [[pct materias ok — Aprovação Global]] | [[Pipeline Completo de Treinamento]]

> [!INFO] 9 features compõem o vetor de entrada do M3 — nenhuma derivada diretamente do target

---

## 1. Tabela Mestre das Features

| Feature | Descrição | Disponível em | Importância M3 | Tipo |
|---|---|---|---|---|
| `n1_norm` | N1 / 10 | M1, M2, M3 | 4,1% | Contínua [0,1] |
| `n2_norm` | N2 / 10 | M2, M3 | **32,3%** | Contínua [0,1] |
| `n3_norm` | N3 / 10 | M3 | 8,7% | Contínua [0,1] |
| `slope_notas` | Regressão linear sobre notas | M2, M3 | 12,3% | Contínua (~-0,5 a +0,5) |
| `variancia_notas` | Var. populacional das notas | M2, M3 | 5,2% | Contínua ≥ 0 |
| `media_geral_aluno` | Média global do aluno (todas as matérias) | M3 | 7,8% | Contínua [0,1] |
| `pct_materias_ok` | % matérias com status ≥ Recuperação | M3 | **21,5%** | Contínua [0,1] |
| `media_turma_norm` | Média normalizada da turma | M3 | 4,8% | Contínua [0,1] |
| `serie_num_norm` | Série escolar normalizada | M1, M2, M3 | 3,3% | Contínua [0,1] |

---

## 2. Agrupamento por Natureza

### Grupo A — Desempenho Individual (notas brutas)
`n1_norm`, `n2_norm`, `n3_norm` — captura o estado atual. `n2_norm` domina com 32,3% de importância, provavelmente porque N2 é a nota mais recente disponível com N3 ainda sendo o ponto de corte temporal do M3.

### Grupo B — Dinâmica Temporal
`slope_notas`, `variancia_notas` — captura **como** as notas evoluem. Slope = tendência direcional; variância = consistência. São complementares: um aluno pode ter slope positivo mas alta variância (melhora errática).

### Grupo C — Contexto Global
`media_geral_aluno`, `pct_materias_ok`, `media_turma_norm`, `serie_num_norm` — captura a posição relativa do aluno no ecossistema escolar. `pct_materias_ok` (21,5%) é a segunda feature mais importante, indicando que o comportamento cross-matéria é altamente preditivo.

---

## 3. Por Que Essas 9 e Não Outras?

### Features Removidas por Leakage
- `media_pond_norm` — r=0,95 com target (ver [[Data Leakage — Conceito e Impacto]])
- `n4_norm` — r=0,91 com target (N4 só existe após o resultado)

### Features Ausentes (Oportunidade Futura)
- **Frequência/assiduidade** — Lima (2021) e Melo (2023) incluem. Mais preditiva que notas para evasão precoce.
- **Engajamento em atividades** — não disponível no dataset
- **Variáveis socioeconômicas** — ausentes por design (LGPD / privacidade)
- **Tempo entre avaliações** — não capturado pelo sistema

---

## 4. Como São Calculadas no Código

Todas as 9 features são calculadas em `cads.py` — função `gerar_features_ml()`:

```python
# cads.py — trecho de gerar_features_ml() (pseudocódigo simplificado)
for aluno in alunos:
    for materia in materias:
        notas = get_notas(aluno, materia)  # N1, N2, N3, N4
        
        # Grupo A — Notas brutas normalizadas
        n1_norm = notas[0] / 10 if notas[0] else None
        n2_norm = notas[1] / 10 if notas[1] else None
        n3_norm = notas[2] / 10 if notas[2] else None
        
        # Grupo B — Dinâmica temporal
        disponíveis = [n for n in notas if n is not None]
        slope_notas = _slope([n/10 for n in disponíveis])
        variancia_notas = _variancia([n/10 for n in disponíveis])
        
        # Grupo C — Contexto global
        media_geral_aluno = avg_todas_notas(aluno) / 10
        pct_materias_ok = count_materias_aprovadas(aluno) / total_materias
        media_turma_norm = avg_turma(aluno.sala) / 10
        serie_num_norm = aluno.serie / max_serie
        
        insert_ml_features(aluno_id, materia_id, ...)
```

Ver [[cads.py — Análise Profunda]] para implementação completa.

---

## 5. Análise de Correlações Entre Features

Features altamente correlacionadas podem causar redundância (multicolinearidade). No EduPredict:

| Par | Correlação esperada | Impacto |
|---|---|---|
| `n2_norm` ↔ `n3_norm` | Alta positiva | RF é robusto a multicolinearidade |
| `n3_norm` ↔ `media_geral_aluno` | Moderada | Aceitável |
| `slope_notas` ↔ `variancia_notas` | Baixa | Capturam aspectos distintos |
| `pct_materias_ok` ↔ `media_geral_aluno` | Alta | Possível redundância |

O Random Forest trata multicolinearidade melhor que regressão logística — não é um problema crítico, mas pode subestimar a importância individual de features correlacionadas.

---

## 6. Features por Modelo (Disponibilidade Temporal)

```
Ponto no tempo:     [N1 lançada]    [N2 lançada]    [N3 lançada]
                         ↓               ↓               ↓
M1 usa:              n1_norm          n2_norm          n3_norm
                    serie_num_norm   slope_notas      slope_notas
                                    variancia        variancia
                                    serie_num_norm   media_geral
                                                     pct_materias_ok
                                                     media_turma_norm
                                                     serie_num_norm
```

M1 — apenas 1 feature real (n1_norm) + 1 contextual (serie_num_norm)
M2 — 4 features: n1, n2, slope, variancia
M3 — todas as 9 features

---

## 7. Limitações do Conjunto de Features

1. **Dependência de N2:** 32,3% da importância concentrada em uma única feature é arriscado. Se N2 for um outlier (prova fácil, cola), o modelo erra sistematicamente.

2. **Ausência de features temporais entre avaliações:** slope_notas captura tendência, mas não captura aceleração — um aluno caindo de 8→6→4 tem a mesma aceleração que um caindo de 5→4→3, mas em situações muito diferentes.

3. **pct_materias_ok usa status atual:** se calculada com N3, inclui informação de matérias já concluídas mas também matérias com apenas N1/N2 disponíveis — pode haver inconsistência temporal.

4. **Sem features de sequência temporal entre bimestres:** LSTM ou RNN poderiam capturar padrões sequenciais que o RF perde por tratar as notas como independentes.

---

## Links

- [[slope notas — Tendência Temporal]]
- [[variancia notas — Consistência]]
- [[pct materias ok — Aprovação Global]]
- [[n2 norm — Feature Dominante]]
- [[media geral aluno — Contexto Transversal]]
- [[serie num norm — Contexto Série]]
- [[media turma norm — Referência de Turma]]
- [[Data Leakage — Conceito e Impacto]]
- [[Pipeline Completo de Treinamento]]
- [[Feature Importance Detalhada — M3]]
- [[cads.py — Análise Profunda]]
