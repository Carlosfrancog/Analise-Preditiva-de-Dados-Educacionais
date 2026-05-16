---
tags: [artigo, feature-engineering, media, aluno, holístico]
aliases: [media geral aluno — Perfil Holístico, media geral aluno — Contexto Transversal]
created: 2026-05-16
---

# media_geral_aluno — Contexto Transversal do Aluno

[← Índice](<../INDEX - ARTIGO.md>) | [[Visão Geral das 9 Features]] | [[pct materias ok — Aprovação Global]] | [[media turma norm — Referência de Turma]]

---

## 1. Definição

`media_geral_aluno` representa a **média de notas do aluno através de todas as matérias** no momento do cálculo, normalizada para [0,1]:

```python
# cads.py — gerar_features_ml(), para cada (aluno, matéria)
# Calcula a média das notas disponíveis do aluno em TODAS as matérias
# (não apenas a matéria atual)

SELECT AVG(media) FROM notas WHERE aluno_id = ?
# Resultado dividido por 10: media_geral_aluno ∈ [0,1]
```

---

## 2. Por Que É uma Feature "Transversal"

Enquanto `n1_norm`, `n2_norm`, `n3_norm` descrevem o aluno **dentro de uma matéria específica**, `media_geral_aluno` descreve o aluno **como um todo**:

```
Aluno X na matéria Matemática:
  - n1_norm = 0.4  (nota 4 em Matemática)
  - media_geral_aluno = 0.72  (nota média 7.2 em TODAS as matérias)
  
→ O modelo recebe ambas as informações:
  "aluno tem nota baixa em Matemática MAS bom desempenho geral"
  → predição: provavelmente vai recuperar
```

Essa combinação permite ao modelo distinguir:
- Aluno com dificuldade específica na matéria (media_geral alta, nota baixa na matéria)
- Aluno com dificuldade sistêmica (media_geral baixa, nota baixa na matéria)

---

## 3. Feature Importance

Na importância do RF_M3, `media_geral_aluno` aparece com ~7-9% de importância — menor que `pct_materias_ok` (21.5%) porque:

- `pct_materias_ok` (percentual de matérias aprovadas) é uma **versão binária** mais direta do mesmo conceito
- A média contínua adiciona informação marginal, mas o threshold de aprovação (6.0) já captura a maior parte do sinal

---

## 4. Relação com pct_materias_ok

| Feature | O que mede | Tipo |
|---|---|---|
| `media_geral_aluno` | Desempenho médio contínuo cross-matéria | Contínua |
| `pct_materias_ok` | % de matérias com status não-reprovado | Proporção binária |

Exemplo:
- Aluno com 10 matérias: 6 aprovadas (≥6), 2 recuperação (5-6), 2 reprovadas (<5)
- `media_geral_aluno` ≈ 5.8 → normalizado 0.58
- `pct_materias_ok` = 8/10 = 0.80 (aprovadas + recuperação = não-reprovadas)

---

## 5. Risco de Leakage Indireto

`media_geral_aluno` pode incluir `n4` de outras matérias se o cálculo não filtrar por bimestre. Se a feature usa a `media_pondP` final da tabela `notas` para outras matérias, incorpora informação do 4º bimestre indiretamente.

**Status:** A implementação atual em `cads.py` usa a média disponível no momento da execução de `gerar_features_ml()`. Se chamada com dados completos (todos os 4 bimestres), a feature incorpora n4 indiretamente. Isso é um risco de leakage não detectado pelo threshold de Pearson.

---

## 6. Comparação com Benchmarks Alternativos

| Alternativa | Vantagem | Por que não foi usada |
|---|---|---|
| Rank percentual do aluno na turma | Remove viés de turma fácil/difícil | Maior complexidade |
| Média ponderada (n1×0.25 + n2×0.25...) | Mais fiel ao cálculo de aprovação | Redunda com media_pond |
| Média dos últimos 2 bimestres | Captura tendência recente | Diminui cobertura para M1 |

---

## Links

- [[Visão Geral das 9 Features]]
- [[pct materias ok — Aprovação Global]]
- [[media turma norm — Referência de Turma]]
- [[Data Leakage — Conceito e Impacto]]
- [[Feature Importance Detalhada — M3]]
