---
tags: [artigo, trabalhos-relacionados, lima2021, random-forest, svm]
created: 2026-05-14
---

# Lima (2021) — RF e SVM para Evasão em Graduação

[[INDEX - ARTIGO|← Índice]] | [[Análise Comparativa dos Trabalhos]] | [[Melo 2023 — MAPEA]]

---

## Referência

LIMA, A. C. **Mineração de dados educacionais e Machine Learning para análise e prevenção da evasão escolar em um curso de graduação.** Dissertação (Mestrado), Universidade Federal do Rio Grande do Norte, 2021.

---

## Contribuição Principal

Primeiro estudo robusto no Brasil aplicando RF e SVM simultaneamente para predição de evasão em contexto de graduação, com uso de variáveis de **frequência e engajamento** — ausentes no EduPredict.

**Resultado:** 78% de acurácia na identificação de alunos em risco.

---

## Features Utilizadas (Diferença Crítica vs EduPredict)

| Feature | Lima (2021) | EduPredict |
|---|---|---|
| Notas por período | ✅ | ✅ |
| Frequência/assiduidade | ✅ | ❌ |
| Engajamento em atividades | ✅ | ❌ |
| Perfil socioeconômico | ✅ | ❌ |
| Série/nível escolar | ✅ | ✅ |
| Slope (tendência) | ❌ | ✅ |
| Data leakage treatment | ❌ | ✅ |

---

## Limitação Principal

Desbalanceamento de classes: alunos evadidos são minoria no dataset. O modelo aprendia a dizer "não vai evadir" para tudo e ainda atingia 78% de acurácia aparente. Isso é o **paradoxo de acurácia em classes desbalanceadas**.

**Como EduPredict mitigou:** `class_weight='balanced'` — ver [[class weight balanced — Tratamento de Desbalanceamento]].

---

## Impacto no Projeto

A ausência de frequência no EduPredict é a **principal oportunidade de melhoria** identificada a partir de Lima (2021). A frequência é o preditor mais precoce de evasão — alunos param de comparecer antes de reprovar.

Ver [[Incorporação de Frequência e Engajamento]].
