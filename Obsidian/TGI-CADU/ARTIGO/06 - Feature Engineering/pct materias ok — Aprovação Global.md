---
tags: [artigo, feature-engineering, pct_materias_ok, features, aprovação]
created: 2026-05-16
---

# pct_materias_ok — Aprovação Global do Aluno

[[INDEX - ARTIGO|← Índice]] | [[Visão Geral das 9 Features]] | [[slope notas — Tendência Temporal]] | [[variancia notas — Consistência]]

> [!NOTE] Importância no M3: 21,5% — 2ª feature mais importante

---

## 1. Definição

`pct_materias_ok` é a fração de matérias em que o aluno possui status diferente de Reprovado no momento da extração de features:

$$pct\_materias\_ok = \frac{\text{matérias com status} \geq \text{Recuperação}}{\text{total de matérias}}$$

Onde "status ≥ Recuperação" significa média ponderada ≥ 5,0 (equivalente a status_encoded ∈ {1, 2}).

---

## 2. Por Que É a 2ª Feature Mais Importante?

A intuição é clara: um aluno reprovando em 8 de 13 matérias tem um perfil radicalmente diferente de um reprovando em apenas 1. A nota de uma matéria específica não captura essa dimensão sistêmica.

**O modelo aprende:** uma matéria em risco numa configuração de "maioria em risco" é muito mais grave que a mesma matéria isolada. `pct_materias_ok` codifica o **contexto de risco sistêmico**.

Isso explica por que supera `n3_norm` (8,7%) em importância — a nota da matéria específica é menos informativa que o padrão geral do aluno.

---

## 3. Implementação Esperada no Código

```python
# cads.py — cálculo de pct_materias_ok (lógica inferida)
def _pct_materias_ok(aluno_id, conn):
    """Fração de matérias com média >= 5 (não Reprovado)."""
    rows = conn.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN media_pond >= 5 THEN 1 ELSE 0 END) as ok
        FROM ml_features
        WHERE aluno_id = ?
    """, (aluno_id,)).fetchone()
    
    if rows['total'] == 0:
        return 0.0
    return rows['ok'] / rows['total']
```

**Ponto de atenção:** a query usa `media_pond >= 5`, mas o status_encoded usa a mesma lógica. Se `media_pond` inclui N4 (que é leakage), então `pct_materias_ok` pode indiretamente incorporar leakage. Ver [[Data Leakage — Conceito e Impacto]].

---

## 4. Risco de Leakage Indireto

Este é o risco mais sutil do pipeline:

```
N4 → media_pond_norm → status_encoded → pct_materias_ok → FEATURE DE ENTRADA
         (leakage direto, detectado)           (leakage indireto, NÃO detectado)
```

Se `pct_materias_ok` é calculado usando o status_encoded que por sua vez foi calculado com N4, então `pct_materias_ok` carrega informação do futuro de forma indireta.

**O Pearson entre pct_materias_ok e target provavelmente está abaixo de 0,9** — por isso não foi detectado. Mas isso não significa que não há leakage.

**Mitigação recomendada:** calcular `pct_materias_ok` usando apenas as notas disponíveis no momento temporal do modelo (M1: só N1; M2: N1+N2; M3: N1+N2+N3).

---

## 5. Interpretação Pedagógica

| Valor | Interpretação | Prevalência esperada |
|---|---|---|
| 1,0 (100%) | Aluno aprovado em todas as matérias | Maioria dos Aprovados |
| 0,7-0,9 | 1-4 matérias em risco | Zona cinza |
| 0,5-0,7 | 4-7 matérias em risco | Sinal de alerta |
| < 0,5 | Maioria das matérias em risco | Alto risco de reprovação por conselho |
| 0,0 | Reprovado em todas as matérias | Extremo — evasão ou abandono |

---

## 6. Feature Dinâmica vs Estática

`pct_materias_ok` é **dinâmica** — muda à medida que novas notas são lançadas. Isso é diferente de `serie_num_norm` (estática) ou `media_turma_norm` (muda apenas entre bimestres).

A versão correta da feature para cada modelo:
- **M1:** usa apenas status baseado em N1 (1 ponto)
- **M2:** usa status baseado em N1+N2 (2 pontos)
- **M3:** usa status baseado em N1+N2+N3 (3 pontos)

O artigo não especifica se essa distinção temporal foi implementada corretamente.

---

## 7. Alternativas Melhores

| Alternativa | Vantagem | Desvantagem |
|---|---|---|
| `pct_materias_ok` (atual) | Simples, interpretável | Risco de leakage indireto |
| `count_materias_reprovado` (contagem bruta) | Mais direto | Não normalizado por nº total |
| `weighted_pct_ok` (ponderado por carga horária) | Mais fiel ao currículo | Complexo, dados nem sempre disponíveis |
| `pct_materias_ok_early` (somente com N1/N2) | Sem risco de leakage | Menos informativo |

---

## 8. Relação com a Métrica de Aprovação Real

No sistema escolar brasileiro, a reprovação por conselho considera o desempenho global. Um aluno com muitas reprovações pode ser retido mesmo que a matéria específica tenha nota marginal. `pct_materias_ok` aproxima esse critério holístico que o modelo precisa capturar.

---

## Links

- [[Visão Geral das 9 Features]]
- [[Data Leakage — Conceito e Impacto]]
- [[Detecção Automática por Correlação de Pearson]]
- [[slope notas — Tendência Temporal]]
- [[variancia notas — Consistência]]
- [[Feature Importance Detalhada — M3]]
- [[Débitos Técnicos Identificados]]
