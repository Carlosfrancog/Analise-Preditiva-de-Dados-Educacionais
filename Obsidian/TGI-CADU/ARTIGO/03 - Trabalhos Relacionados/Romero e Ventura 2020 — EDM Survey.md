---
tags: [artigo, trabalhos-relacionados, romero, ventura, edm, survey]
created: 2026-05-16
---

# Romero e Ventura (2020) — Survey de Educational Data Mining

[[INDEX - ARTIGO|← Índice]] | [[Análise Comparativa dos Trabalhos]] | [[Educational Data Mining e Learning Analytics]]

---

## Referência

ROMERO, C.; VENTURA, S. **Educational data mining and learning analytics: An updated survey.** WIREs Data Mining and Knowledge Discovery, v. 10, n. 3, e1355, 2020.

---

## 1. Contribuição Principal

Survey mais abrangente de EDM publicado na última década. Cobre 20 anos de literatura com análise de tendências, lacunas e direções futuras. É a referência canônica em EDM — qualquer artigo na área precisa citá-lo.

**Para o EduPredict:** fornece o enquadramento teórico que legitima as escolhas metodológicas (RF, validação cruzada, feature engineering) e identifica as lacunas que o sistema tenta preencher.

---

## 2. Principais Contribuições do Survey

### 2.1 Taxonomia de Tarefas em EDM

Romero e Ventura classificam EDM em:
1. Predição de desempenho (foco do EduPredict)
2. Clustering de alunos
3. Mineração de padrões de relacionamento
4. Detecção de comportamentos (evasão em LMS)
5. Descoberta de estrutura (dependências entre conceitos)

### 2.2 Data Leakage como Problema Recorrente

> *"Muitos estudos reportam acurácias acima de 90% que não se sustentam em validação externa, frequentemente porque variáveis derivadas do target são incluídas como features."*

Este é o fundamento para o mecanismo de detecção de leakage do EduPredict. Ver [[Data Leakage — Conceito e Impacto]].

### 2.3 Explicabilidade como Lacuna Crítica

O survey identifica que a grande maioria dos sistemas EDM usa modelos caixa-preta (RF, SVM, redes neurais) sem fornecer explicações individuais para educadores. SHAP e LIME são identificados como soluções emergentes.

### 2.4 Ausência de Mecanismos de Feedback

Sistemas EDM são tipicamente estáticos — treinados uma vez, usados sem atualização. O survey recomenda loops de feedback onde o julgamento do educador retroalimenta o modelo.

---

## 3. Onde o EduPredict se Posiciona

| Aspecto do Survey | EduPredict |
|---|---|
| Taxonomia de tarefas | Predição de desempenho (tarefa 1) |
| Detecção de leakage | ✅ Implementado (diferencial) |
| Explicabilidade | ❌ Apenas global (lacuna) |
| Loop de feedback | ❌ Não implementado (lacuna) |
| Dados reais | ❌ Dataset sintético (limitação) |
| Validação LGPD/Ética | ❌ Não abordado (lacuna) |

---

## 4. Insights para o Artigo de Extensão

O survey de Romero e Ventura (2020) é citado pelo próprio EduPredict, mas o artigo poderia usar os achados do survey de forma mais cirúrgica para posicionar sua contribuição:

1. **Citar a frase sobre leakage** para validar a importância da detecção automática
2. **Citar a lacuna de explicabilidade** para justificar SHAP como próximo passo
3. **Usar a taxonomia** para clarificar que o EduPredict faz predição de desempenho, não detecção de evasão direta

---

## 5. Limitações do Survey

- Survey de 2020 — não cobre aplicações recentes de LLMs em EDM
- Foco maior em contexto de ensino superior e LMS — ensino básico brasileiro é pouco representado
- Autores europeus — contexto regulatório (GDPR) pode não se traduzir diretamente para LGPD

---

## Links

- [[Educational Data Mining e Learning Analytics]]
- [[Data Leakage — Conceito e Impacto]]
- [[Análise Comparativa dos Trabalhos]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Limitações Gerais do Artigo]]
