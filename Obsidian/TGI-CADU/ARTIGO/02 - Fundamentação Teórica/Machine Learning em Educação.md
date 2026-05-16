---
tags: [artigo, machine-learning, educacao, algoritmos, classificacao]
created: 2026-05-16
---

# Machine Learning em Educação — Fundamentos e Aplicações

[[INDEX - ARTIGO|← Índice]] | [[Educational Data Mining e Learning Analytics]] | [[Random Forest — Algoritmo e Justificativa]]

---

## 1. Tipos de ML Aplicados em Educação

| Paradigma | Técnica | Aplicação típica em EDM |
|---|---|---|
| **Supervisionado** | Random Forest, SVM, Redes Neurais | Predição de desempenho, classificação de risco |
| **Não-supervisionado** | K-Means, DBSCAN | Agrupamento de perfis de aprendizagem |
| **Semi-supervisionado** | Label propagation | Datasets com poucos rótulos |
| **Por reforço** | Q-Learning | Sistemas de tutoria inteligente adaptativa |

O EduPredict usa exclusivamente **aprendizado supervisionado** (Random Forest) para **classificação multiclasse** (Aprovado/Recuperação/Reprovado).

---

## 2. Por Que Classificação (Não Regressão)?

O alvo do EduPredict é `status_encoded` — uma variável categórica ordinal com 3 valores. Alternativas:

| Abordagem | Target | Vantagem | Desvantagem |
|---|---|---|---|
| **Classificação** (escolhido) | 0/1/2 (Reprovado/Recup/Aprovado) | Diretamente acionável | Perde informação de "margem" |
| **Regressão** | Média ponderada (contínua) | Captura margem de aprovação | Requer threshold manual |
| **Regressão + threshold** | Média → classificação | Mais informativo | Mais complexo, threshold arbitrário |

A escolha de classificação direta é pragmática — professores precisam de categorias, não de números contínuos.

---

## 3. O Problema de Classificação Multiclasse Ordinal

Aprovado/Recuperação/Reprovado têm **ordem natural** (Reprovado < Recuperação < Aprovado). O Random Forest trata as classes como nominais (sem ordem), ignorando essa estrutura.

**Alternativas que exploram a ordem:**
- **Ordinal Regression** (CORAL, OrdinalClassifier): modela a ordem diretamente
- **Threshold-based regression**: prediz a média e aplica thresholds

Para o contexto do EduPredict, a perda de informação de ordem é aceitável — a fronteira Recuperação/Aprovado (limiar 6,0) é a mais crítica, e o RF aprende essa fronteira empiricamente mesmo sem a estrutura ordinal explícita.

---

## 4. Validação em ML Educacional

Princípios de validação específicos para EDM:

| Princípio | Descrição | Aplicado no EduPredict? |
|---|---|---|
| **Validação cruzada estratificada** | Mantém proporção de classes em cada fold | ✅ StratifiedKFold(5) |
| **Agrupamento por aluno** | Evita vazamento de informação do mesmo aluno | ❌ Não aplicado |
| **Holdout temporal** | Treinar em dados anteriores, testar em posteriores | ❌ Não aplicado |
| **Validação externa** | Testar em dados de escola diferente | ❌ Impossível com dados sintéticos |

A ausência de agrupamento por aluno é a limitação mais crítica. Ver [[Análise Crítica do TGI#2.5]].

---

## 5. Features Típicas em EDM vs EduPredict

| Categoria | Típico na literatura | EduPredict |
|---|---|---|
| **Notas/avaliações** | ✅ | ✅ (n1-n3 norm) |
| **Frequência** | ✅ | ❌ |
| **Engajamento** | ✅ (LMS) | ❌ |
| **Perfil socioeconômico** | Às vezes | ❌ |
| **Série/curso** | ✅ | ✅ (serie_num_norm) |
| **Tendência temporal** | Raramente | ✅ (slope, variância) |
| **Contexto de turma** | Raramente | ✅ (media_turma_norm) |

O EduPredict inova em features de tendência temporal (slope, variância) mas perde em frequência e engajamento.

---

## 6. Early Warning Systems em Educação

Um EWS de ML tem estrutura típica:

```
[Dados] → [Feature Engineering] → [Modelo ML] → [Score de Risco] → [Alerta] → [Intervenção]
```

O EduPredict implementa todos os passos exceto o protocolo formal de intervenção. Ver [[Protocolo de Alertas EWS]].

**Sistemas EWS de referência na literatura:**
- EDRM (Early Drop-out Risk Model) — Moodle plugin
- Student Success System (S3) — universidades americanas
- Purdue's Course Signals — baseado em RF com dados de LMS

---

## Links

- [[Educational Data Mining e Learning Analytics]]
- [[Random Forest — Algoritmo e Justificativa]]
- [[Pipeline Completo de Treinamento]]
- [[Análise Crítica do TGI]]
- [[Protocolo de Alertas EWS]]
