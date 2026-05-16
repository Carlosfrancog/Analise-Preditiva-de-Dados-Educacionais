---
tags: [artigo, feature-engineering, turma, media, referencia]
aliases: [media turma norm — Efeito de Turma, media turma norm — Referência de Turma]
created: 2026-05-16
---

# media_turma_norm — Referência de Turma

[← Índice](<../INDEX - ARTIGO.md>) | [[Visão Geral das 9 Features]] | [[serie num norm — Contexto Série]] | [[media geral aluno — Contexto Transversal]]

---

## 1. Definição

`media_turma_norm` é a **média das notas de todos os alunos da mesma turma na matéria avaliada**, normalizada por 10:

```python
# cads.py — gerar_features_ml()
# Para cada (aluno, matéria):
SELECT AVG(n.media) FROM notas n
JOIN alunos a ON a.id = n.aluno_id
WHERE a.sala_id = [sala_do_aluno_atual]
AND n.materia_id = [materia_atual]
# resultado / 10 → media_turma_norm ∈ [0,1]
```

---

## 2. Por Que Inclui Esta Feature

A média da turma funciona como **contexto de dificuldade**:

```
Situação A: Aluno tem nota 5.0 em Matemática
  - media_turma = 4.2 → aluno está ACIMA da média da turma
  - Interpretação: matéria está difícil para todos, aluno relativamente ok

Situação B: Aluno tem nota 5.0 em Matemática  
  - media_turma = 7.8 → aluno está ABAIXO da média da turma
  - Interpretação: dificuldade específica do aluno, risco real
```

O modelo pode usar `media_turma_norm` para relativizar o desempenho individual.

---

## 3. Feature Importance e Limitações

**Importância no M3:** ~4-6% — a menor entre as features não-removidas.

**Razão da baixa importância:**
- O dataset sintético tem turmas equilibradas (notas geradas aleatoriamente com a mesma distribuição)
- Em dados reais, turmas têm perfis distintos (escola pública vs privada, turno, professor)
- No dataset artificial, `media_turma_norm` tende a convergir para ~0.6 para todas as turmas, oferecendo pouco poder discriminante

---

## 4. Risco de Leakage por Contaminação

**Problema potencial:** Se a média da turma for calculada usando todos os alunos (incluindo o aluno avaliado), há contaminação circular. Mas o impacto é mínimo para turmas grandes (1/N onde N≈30).

**Risco maior:** Se `media_pondP` (que inclui n4) for usada no cálculo da média da turma, a feature se torna leaky indiretamente.

---

## 5. Alternativas Mais Robustas

| Feature | Informação capturada |
|---|---|
| `media_turma_norm` (atual) | Nível médio da turma na matéria |
| Percentil do aluno na turma | Posição relativa (ex: top 20%) |
| Desvio padrão da turma | Homogeneidade da turma |
| Diferença aluno-turma | Desempenho relativo direto |

Uma feature `diff_aluno_turma = n_norm - media_turma_norm` seria mais informativa que cada uma isolada, mas aumenta correlações com n_norm.

---

## 6. Relação com serie_num_norm

`serie_num_norm` e `media_turma_norm` capturam informações diferentes mas relacionadas:

| Feature | O que captura |
|---|---|
| `serie_num_norm` | Nível do currículo (6º Fund. → 3º Médio) |
| `media_turma_norm` | Desempenho real da turma (pode ser alta série com turma fraca) |

Em turmas regulares, são moderadamente correlacionadas (séries mais avançadas tendem a ter médias menores), mas não o suficiente para criar multicolinearidade problemática.

---

## Links

- [[Visão Geral das 9 Features]]
- [[serie num norm — Contexto Série]]
- [[media geral aluno — Contexto Transversal]]
- [[Data Leakage — Conceito e Impacto]]
- [[Dataset — Estrutura e Geração Sintética]]
