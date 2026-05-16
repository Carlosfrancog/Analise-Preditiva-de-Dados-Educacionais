---
tags: [artigo, trabalhos-relacionados, comparativo, benchmarks]
created: 2026-05-14
---

# Análise Comparativa dos Trabalhos Relacionados

[[INDEX - ARTIGO|← Índice]] | [[Lima 2021 — Random Forest e SVM]] | [[Melo 2023 — MAPEA]] | [[Romero e Ventura 2020 — EDM Survey]]

---

## 1. Tabela Comparativa

| Aspecto | Lima (2021) | Melo (2023) | Velasco (2022) | Romero & Ventura (2020) | **EduPredict** |
|---|---|---|---|---|---|
| **Algoritmo** | RF + SVM | MAPEA (ensemble) | Análise crítica | Revisão | Random Forest |
| **Contexto** | Graduação | Ed. Básica (Fundamental) | Geral | Internacional | Ed. Básica (todas as séries) |
| **Acurácia** | 78% | 82% | N/A | Revisão | **94,0%** |
| **Dataset** | Real (universitário) | 500 alunos | N/A | Múltiplos | **15.613 registros** (sintético) |
| **Data leakage** | Não tratado | Não tratado | Menciona risco | Identifica problema | **Detecção automática** |
| **Explicabilidade** | Não | Não | Recomenda | Identifica necessidade | Apenas global |
| **LGPD/Ética** | Não aborda | Não aborda | Menciona | Menciona | Não aborda |
| **Frequência** | Sim (feature) | Sim (feature) | N/A | Varia | **Não incluída** |
| **Modelos temporais** | Não | Não | N/A | Varia | **Sim (M1, M2, M3)** |
| **Desbalanceamento** | Identificado como limitação | N/A | N/A | Varia | `class_weight='balanced'` |

---

## 2. Lacunas Transversais (Presentes em Todos os Trabalhos)

### Lacuna 1 — Ausência de SHAP/Explicabilidade Local
Nenhum dos trabalhos brasileiros implementa SHAP ou LIME para explicar predições individuais. Isso é crítico para adoção real: um professor precisa saber POR QUE o modelo diz que aquele aluno vai reprovar, não apenas que vai.

### Lacuna 2 — Sem Loop de Feedback
Todos os sistemas são estáticos — treinados uma vez e usados sem mecanismo de atualização baseado no julgamento do especialista (professor). O modelo aprende padrões históricos, mas não aprende com os casos em que errou.

### Lacuna 3 — Comportamento Pós-Predição Indefinido
Nenhum trabalho especifica o protocolo operacional: quem recebe o alerta, quando, em qual formato, e qual ação é esperada. O sistema existe para gerar predições, mas não para operacionalizá-las.

### Lacuna 4 — Frequência Ausente no EduPredict
Lima (2021) e Melo (2023) incluem frequência/assiduidade — uma das features mais importantes na literatura. O EduPredict a omite por limitação do dataset, não por decisão metodológica. É a adição de maior impacto potencial.

---

## 3. Diferenciais Reais do EduPredict

**O que o EduPredict genuinamente inova:**

1. **Detecção automática de data leakage** — único na literatura nacional consultada; metodologicamente rigoroso
2. **Três modelos temporais** — M1/M2/M3 com diferentes pontos de corte temporal permitem análise de trade-off antecedência × acurácia
3. **Volume de dados maior que os nacionais** — 15.613 vs 500 (Melo) e universo não especificado (Lima)

**O que o EduPredict afirma inovar mas não é único:**
- Uso de Random Forest — Lima (2021) também usou
- Validação cruzada — é prática padrão
- Tratamento de desbalanceamento com `class_weight` — técnica conhecida

---

## 4. Implicações para o Artigo de Extensão

O artigo de extensão ([[Plano de Artigo ABNT]]) deve posicionar-se como **Geração 3** de sistemas EDM, resolvendo as 4 lacunas transversais identificadas:

1. Implementar SHAP local → [[SHAP — Explicabilidade Local por Aluno]]
2. Implementar feedback docente → [[Módulo de Feedback Docente]]
3. Definir protocolo operacional → [[Plano de Artigo ABNT#3.3 Módulo de Comportamento Operacional]]
4. Incorporar frequência → [[Incorporação de Frequência e Engajamento]]

---

## 5. Análise Crítica do Benchmark

> [!WARNING] O benchmark de 94% é real?
> O EduPredict supera Lima (78%) e Melo (82%) com 94,0%. Porém, a comparação não é totalmente justa:
> - Lima usou dados **reais** de universidade — generalização difícil
> - Melo usou dados reais com 500 alunos — menor volume
> - EduPredict usou 15.613 registros, mas de apenas **200 alunos** (muitos registros por aluno) — risco de correlação intra-aluno aumentar artificialmente a acurácia de cross-validation
>
> A validação cruzada estratificada mitiga isso parcialmente, mas não elimina completamente o risco de vazamento de informação do mesmo aluno entre treino e teste.

---

## Links

- [[Lima 2021 — Random Forest e SVM]]
- [[Melo 2023 — MAPEA]]
- [[Velasco 2022 — Análise Crítica]]
- [[Romero e Ventura 2020 — EDM Survey]]
- [[Data Leakage — Conceito e Impacto]]
- [[Limitações Gerais do Artigo]]
- [[Gaps — TGI vs EduNotas Atual]]
