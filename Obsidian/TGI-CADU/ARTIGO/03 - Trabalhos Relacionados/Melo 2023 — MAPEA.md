---
tags: [artigo, trabalhos-relacionados, melo2023, mapea, ensemble]
created: 2026-05-16
---

# Melo (2023) — MAPEA: Sistema de Predição para Ed. Básica

[[INDEX - ARTIGO|← Índice]] | [[Análise Comparativa dos Trabalhos]] | [[Lima 2021 — Random Forest e SVM]]

---

## Referência

MELO, R. S. **MAPEA: Modelo de Avaliação e Predição do Êxito Acadêmico no Ensino Fundamental.** [Dissertação/Artigo], 2023.

*(Referência completa não disponível no artigo consultado — reconstruída do contexto)*

---

## 1. Contribuição Principal

Primeiro sistema de predição acadêmica brasileiro focado especificamente no **Ensino Fundamental** (não universitário). Usa ensemble (MAPEA — nome próprio) com 82% de acurácia.

---

## 2. Características Técnicas

| Característica | Melo (2023) | EduPredict |
|---|---|---|
| **Algoritmo** | MAPEA (ensemble proprietário) | Random Forest |
| **Dataset** | 500 alunos (real) | 200 alunos (sintético) |
| **Contexto** | Ensino Fundamental (real) | Ed. Básica (todas as séries, sintético) |
| **Acurácia** | 82% | 94,0% |
| **Frequência** | ✅ Incluída | ❌ Ausente |
| **Data leakage** | Não tratado | ✅ Tratado |
| **Explicabilidade** | Não | Apenas global |

---

## 3. Por Que Melo Usa Dados Reais e EduPredict Não?

Melo (2023) com 500 alunos reais tem maior validade ecológica. A limitação é o volume — 500 alunos podem não ser suficientes para treinar um RF estável com muitas features.

O EduPredict contornou a limitação de dados reais usando síntese — mas ao custo de validade externa.

---

## 4. MAPEA — O Que É?

O artigo consultado não detalha o algoritmo MAPEA. Provavelmente é um ensemble customizado (combinação de múltiplos classificadores) com lógica específica para o contexto escolar brasileiro.

**Limitação para citação:** sem acesso ao artigo completo de Melo (2023), detalhes técnicos são incompletos. O artigo de extensão deve buscar a referência completa.

---

## 5. Comparação de Acurácia — Justa?

| Aspecto | Impacto na comparação |
|---|---|
| Melo: dados reais | Mais difícil de modelar → acurácia esperada menor |
| EduPredict: dados sintéticos | Dados mais "limpos" → acurácia artificialmente maior |
| Melo: sem tratamento de leakage | Acurácia pode estar subestimada (leakage inflaria) |
| EduPredict: com leakage tratado | Acurácia real, não inflada por leakage |

A comparação "94% vs 82%" é enganosa sem ajuste pelo contexto de dados. Com dados reais, o EduPredict provavelmente mostraria acurácia menor.

---

## 6. Contribuição do Melo Relevante para o EduPredict

A inclusão de **frequência** é o diferencial técnico mais importante de Melo vs EduPredict. Ver [[Incorporação de Frequência e Engajamento]] para proposta de adição ao EduPredict.

---

## Links

- [[Análise Comparativa dos Trabalhos]]
- [[Lima 2021 — Random Forest e SVM]]
- [[Dataset — Estrutura e Geração Sintética]]
- [[Incorporação de Frequência e Engajamento]]
- [[Análise Crítica do TGI]]
