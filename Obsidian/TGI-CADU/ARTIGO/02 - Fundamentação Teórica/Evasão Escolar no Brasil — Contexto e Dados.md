---
tags: [artigo, evasao, brasil, educacao, contexto]
aliases: [Evasão Escolar no Brasil]
created: 2026-05-16
---

# Evasão Escolar no Brasil — Contexto e Dados

[[INDEX - ARTIGO|← Índice]] | [[Problema Central e Justificativa]] | [[Educational Data Mining e Learning Analytics]]

---

## 1. Dados Quantitativos do Artigo

O artigo cita uma taxa de evasão de **8%** no ensino fundamental brasileiro como motivação central. Esse dado ancora a justificativa do EduPredict como necessário.

**Fontes prováveis:** INEP (Instituto Nacional de Estudos e Pesquisas Educacionais), PNAD Educação, Censo Escolar.

---

## 2. Distinção Crítica — Evasão vs Reprovação

> [!WARNING] Confusão conceitual no artigo
> O EduPredict prediz **reprovação** (status final: Aprovado/Recuperação/Reprovado) mas a justificativa usa dados de **evasão escolar** (abandono). São fenômenos diferentes com causas e intervenções distintas.

| Fenômeno | Definição | Prevalência | Intervalo de Detecção |
|---|---|---|---|
| **Evasão** | Aluno abandona a escola | 8% (artigo) | Precoce — ausências crescentes |
| **Reprovação** | Aluno falha nas avaliações | ~15-25% (estimativa) | Tardia — resultado bimestral |

Um aluno pode reprovar sem evadir (repete o ano). Um aluno pode evadir sem reprovar (abandona com boas notas — raro mas possível). O EduPredict detecta risco de reprovação, não de evasão.

**Para detecção de evasão**, o preditor mais poderoso é frequência — dados ausentes no EduPredict. Ver [[Lima 2021 — Random Forest e SVM#Contribuição Principal]].

---

## 3. Fatores de Evasão na Literatura

| Fator | Tipo | Capturado pelo EduPredict? |
|---|---|---|
| Desempenho acadêmico baixo | Acadêmico | ✅ Parcialmente (via notas) |
| Frequência baixa | Comportamental | ❌ Ausente |
| Situação socioeconômica | Socioeconômico | ❌ Ausente |
| Distância escola-residência | Logístico | ❌ Ausente |
| Violência escolar | Social | ❌ Ausente |
| Necessidade de trabalhar | Econômico | ❌ Ausente |
| Gravidez na adolescência | Pessoal | ❌ Ausente |
| Desengajamento com o currículo | Pedagógico | ❌ Ausente |

O EduPredict captura apenas 1 dos 8 fatores principais. Isso é uma limitação séria para usar "prevenção de evasão" como justificativa.

---

## 4. O Que o EduPredict Realmente Resolve

Ser honesto sobre o escopo:
- ✅ **Detecção de risco de reprovação** — sim, com 94% de acurácia
- ✅ **Priorização de atenção pedagógica** — identifica quais alunos precisam de suporte
- ✅ **Análise de tendência temporal** — slope informa direção, não apenas estado
- ❌ **Prevenção de evasão** — não diretamente; indiretamente se reprovação leva a evasão

O sistema é valioso mesmo com esse escopo mais restrito — a justificativa deveria ser mais precisa.

---

## 5. Pipeline Causal Evasão ← Reprovação

A lógica implícita do artigo é:

```
Reprovação → Desmotivação → Evasão
```

Isso é parcialmente correto: alunos que reprovam têm maior probabilidade de evadir nos anos seguintes. Mas não é a causa única nem a mais frequente de evasão imediata.

**Se o objetivo é realmente reduzir evasão**, o sistema deveria:
1. Prever reprovação (o que faz)
2. Trigger intervenção precoce (o que propõe no EWS)
3. Medir se a intervenção reduziu reprovação (loop de feedback — não implementado)
4. Medir se a redução de reprovação reduziu evasão (validação externa — ausente)

---

## 6. Dados do Censo Escolar Relevantes

O Censo Escolar INEP fornece dados anuais sobre:
- Taxa de abandono por série e rede (pública/privada)
- Taxa de reprovação por série
- Taxa de distorção idade-série

Para contextualizar o EduPredict, seria útil comparar a taxa de reprovação do dataset sintético com os dados reais do Censo Escolar da região/série correspondente.

---

## Links

- [[Problema Central e Justificativa]]
- [[Questão de Pesquisa e Objetivos]]
- [[Educational Data Mining e Learning Analytics]]
- [[Lima 2021 — Random Forest e SVM]]
- [[Incorporação de Frequência e Engajamento]]
- [[Limitações Gerais do Artigo]]
