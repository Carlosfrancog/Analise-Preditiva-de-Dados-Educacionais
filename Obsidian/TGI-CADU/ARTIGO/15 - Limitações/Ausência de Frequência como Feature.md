---
tags: [artigo, limitacoes, frequencia, feature, ausencia]
created: 2026-05-16
---

# Ausência de Frequência como Feature

[← Índice](<../INDEX - ARTIGO.md>) | [[Limitações Gerais do Artigo]] | [[Incorporação de Frequência e Engajamento]] | [[Visão Geral das 9 Features]]

---

## 1. A Lacuna

O EduPredict usa apenas **notas** como proxy de desempenho. Frequência escolar — um preditor estabelecido na literatura de EDM — está completamente ausente do sistema.

---

## 2. Por Que Frequência Importa

Estudos de EDM (incluindo Romero e Ventura, 2020) consistentemente identificam frequência como um dos 3 principais preditores de evasão e reprovação:

```
Correlação típica na literatura:
  frequência > 90%  → 85% de probabilidade de aprovação
  frequência 75-90% → 65% de probabilidade de aprovação
  frequência < 75%  → 40% de probabilidade de aprovação (mínimo legal: 75%)
```

Um aluno com nota 7.0 e 60% de frequência tem perfil de risco muito diferente de um aluno com nota 7.0 e 95% de frequência — o modelo atual trata os dois identicamente.

---

## 3. Como Afeta as 9 Features Atuais

| Feature atual | O que frequência adicionaria |
|---|---|
| `n1_norm`, `n2_norm` | Faltas causam notas baixas — mas a causa (ausência) é invisível |
| `slope_notas` | Queda de notas por aumento de faltas vs queda por dificuldade acadêmica |
| `pct_materias_ok` | Faltas em matérias específicas (falta seletiva) vs geral |
| `media_geral_aluno` | Aluno com boas notas mas muitas faltas — risco invisível |

---

## 4. Por Que Foi Omitida

### Hipótese 1 — Dataset sintético não tem frequência
`gerar_notas_aleatorias()` em `cads.py` gera apenas notas, não frequência. Como o sistema foi desenvolvido e testado com dados sintéticos, a ausência de frequência nos dados tornou impossível incluí-la como feature.

### Hipótese 2 — Complexidade de coleta
Em escolas reais, frequência é registrada por aula/dia, não por bimestre. Integrar esses dados exige:
- Sistema de chamada eletrônica (ou manual digitalizado)
- Cálculo de `pct_frequencia = presencas / aulas_previstas`
- Padronização por matéria (matérias com mais aulas têm mais peso)

### Hipótese 3 — Escopo do TGI
O sistema foi projetado para prever desempenho com base em notas — frequência estava fora do escopo definido.

---

## 5. Impacto Estimado na Acurácia

Baseado em estudos similares na literatura:

```
Modelo sem frequência (atual):          M3 = 94.0% (dados sintéticos)
Modelo com frequência (estimado):       ~95-97% (dados reais com frequência)
```

Em dados sintéticos, o ganho seria mínimo (frequência não foi usada para gerar as notas). Em dados reais, o ganho seria mais significativo — especialmente para o Recall de Recuperação.

---

## 6. Proposta de Implementação

Ver [[Incorporação de Frequência e Engajamento]] para o plano técnico completo.

Resumo:
```python
# Nova feature em cads.py:
pct_frequencia_norm = presencas_bimestre / aulas_previstas_bimestre
# Normalização: já está em [0,1] naturalmente

# Adicionada ao feature_cols:
SAFE_TRAINING_FEATURES = [..., 'pct_frequencia_norm']
```

O maior desafio é a **coleta de dados de frequência**, não a implementação da feature em si.

---

## Links

- [[Limitações Gerais do Artigo]]
- [[Incorporação de Frequência e Engajamento]]
- [[Visão Geral das 9 Features]]
- [[Romero e Ventura 2020 — EDM Survey]]
- [[Dataset — Estrutura e Geração Sintética]]
