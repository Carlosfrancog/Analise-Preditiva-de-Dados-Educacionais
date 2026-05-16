---
tags:
  - moc
  - artigo
  - tgi-codes
  - edupredict
created: 2026-05-14
---

# ARTIGO — Mapa do Conhecimento EduPredict

[← Vault Principal](<../MOC - TGI-CODES.md>) | [[Plano de Artigo ABNT]] | [[Roadmap]]

> [!NOTE] Fonte primária
> **GABRIEL, C. E. F.; ROCHA, M. F. P. S.** *EduPredict: Um Sistema Baseado em Machine Learning para Predição de Desempenho e Evasão Escolar.* UNICSUL, 2026. 12 p.
> — 200 alunos · 13 matérias · 7 séries · 15.613 registros · RF M3: **94,0% acurácia**

---

## 01 — Problema e Objetivos
- [[Problema Central e Justificativa]] — evasão 8%, custo socioeconômico, oportunidade de ML
- [[Questão de Pesquisa e Objetivos]] — hipótese, OG, OE1-OE5

## 02 — Fundamentação Teórica
- [[Evasão Escolar no Brasil]] — INEP 2023, multidimensionalidade, cadeia causal
- [[Educational Data Mining e Learning Analytics]] — EDM vs LA, geração de abordagens
- [[Machine Learning em Educação]] — taxonomia de aplicações, estado da arte

## 03 — Trabalhos Relacionados
- [[Lima 2021 — Random Forest e SVM]] — 78% acurácia, desbalanceamento
- [[Melo 2023 — MAPEA]] — 82% acurácia, falta de explicabilidade
- [[Velasco 2022 — Análise Crítica]] — qualidade de dados, viés algorítmico
- [[Romero e Ventura 2020 — EDM Survey]] — revisão sistemática, data leakage negligenciado
- [[Análise Comparativa dos Trabalhos]] — lacunas identificadas, diferencial do EduPredict

## 04 — Metodologia
- [[Classificação e Design da Pesquisa]] — aplicada, quantitativa, exploratória

## 05 — Base de Dados
- [[Dataset — Estrutura e Origem]] — 200 alunos, 13 matérias, 15.613 registros
- [[Pré-processamento dos Dados]] — normalização, dados ausentes, codificação
- [[Distribuição de Classes e Desbalanceamento]] — Aprovado 60,3% · Recuperação 25,8% · Reprovado 13,9%

## 06 — Feature Engineering
- [[Visão Geral das 9 Features]] — mapa completo, importância, normalização
- [[n1 n2 n3 — Notas Normalizadas]] — base bruta, divisão por 10
- [[slope notas — Tendência Temporal]] ⭐ — regressão linear, interpretação, riscos
- [[variancia notas — Consistência]] — desvio padrão normalizado, oscilação
- [[media geral aluno — Perfil Holístico]] — média global, efeito de contexto
- [[pct materias ok — Aprovação Global]] ⭐ — 21,5% importância, preditor crítico
- [[media turma norm — Efeito de Turma]] — relativização, professor/horário
- [[serie num norm — Nível Escolar]] — 6F=0 até 3M=1, padrões por série

## 07 — Pipeline de ML
- [[Pipeline Completo de Treinamento]] — 5 etapas, SQL → features → modelo → avaliação → serialização
- [[Divisão Treino-Teste e Validação Cruzada]] — 80/20 estratificado, CV 5-fold
- [[Serialização e Versionamento de Modelos]] — pickle + metadata.json, reprodutibilidade

## 08 — Data Leakage
- [[Data Leakage — Conceito e Impacto]] ⭐⭐ — definição, tipos, consequências catastróficas
- [[Detecção Automática por Correlação de Pearson]] — limiar 0,9, 10 validações
- [[media pond norm — Feature Removida]] — correlação 0,95, por que vaza
- [[n4 norm — Feature Removida]] — correlação 0,91, por que vaza

## 09 — Modelos Preditivos
- [[M1 — Alerta Precoce (Após N1)]] — 1 feature, 83,8%, intervenção máxima antecipada
- [[M2 — Predição Intermediária (Após N2)]] — 4 features, 92,5%, ponto ótimo custo-benefício
- [[M3 — Modelo de Produção (Após N3)]] ⭐ — 9 features, 94,0%, modelo principal
- [[Comparação Temporal dos Três Modelos]] — trade-off antecedência × acurácia

## 10 — Random Forest
- [[Algoritmo Random Forest — Base Teórica]] — Breiman 2001, ensemble, bagging
- [[Hiperparâmetros e Configuração]] — n_estimators, max_depth, class_weight, random_state
- [[Feature Importance — Interpretação]] — Gini impurity, global vs local, limitações
- [[class weight balanced — Tratamento de Desbalanceamento]] — efeito, alternativas

## 11 — Arquitetura do Sistema
- [[Arquitetura Modular do EduPredict]] — 3 módulos, separação de responsabilidades
- [[Módulo de Dados — cads.py]] — SQLite, CRUD, feature engineering
- [[Módulo de ML — train simple e gui ml integration]] — pipeline, predição, serialização
- [[Módulo de Interface — GUI tkinter]] — páginas, navegação, threading

## 12 — Implementação Python
- [[cads.py — Análise Profunda]] — funções críticas, acoplamento, débitos técnicos
- [[train simple py — Pipeline Autônomo]] — fluxo completo, pontos frágeis
- [[gui ml integration py — Motor de Predição]] — DisciplinePerformanceAnalyzer, MLModelLoader
- [[gui predicoes improved py — Interface Preditiva]] — cards, filtros, scroll

## 13 — Avaliação e Métricas
- [[Acurácia e F1-Score — Definição e Uso]] — macro vs weighted, quando usar cada
- [[Matriz de Confusão M3 — Análise Detalhada]] ⭐ — 62,2% Recuperação: implicação real
- [[Validação Cruzada 5-fold — Robustez]] — média ± desvio, overfitting check
- [[Desempenho por Nível de Ensino]] — Fundamental I 89,2% → Médio 95,1%

## 14 — Resultados
- [[Resultados Gerais — M1 M2 M3]] — tabela comparativa, benchmarks da literatura
- [[Feature Importance Detalhada — M3]] — n2_norm 32,3%, pct_materias_ok 21,5%
- [[Acurácia por Classe — Análise Crítica]] — Recuperação 62,2%: o problema real

## 15 — Limitações
- [[Limitações Gerais do Artigo]] — síntese crítica das 6 lacunas
- [[Ausência de Indicadores Socioemocionais]] — motivação, família, saúde mental
- [[Dataset Sintético — Risco de Não-generalização]] — 200 alunos, dados controlados
- [[Ausência de Frequência como Feature]] — preditor-chave ignorado

## 16 — Melhorias Futuras
- [[Roadmap Técnico de Extensão]] — 8 direções priorizadas
- [[SHAP — Explicabilidade Local por Aluno]] — Lundberg 2017, SHAP values, implementação
- [[Modelos Alternativos — XGBoost e Redes Neurais]] — quando usar, trade-offs
- [[Incorporação de Frequência e Engajamento]] — feature mais urgente, impacto esperado
- [[Módulo de Feedback Docente]] — retreino incremental, loop de aprendizado
- [[Portal de Transparência Familiar]] — LGPD, comunicação proativa

## 17 — Relação com Projeto Atual
- [[Mapeamento Teoria-Código]] ⭐ — TGI vs implementação real linha a linha
- [[Gaps — TGI vs EduNotas Atual]] — o que está implementado, o que falta
- [[Compatibilidade Arquitetural]] — onde o código atual diverge do artigo

## 18 — Refatorações Necessárias
- [[Débitos Técnicos Identificados]] — acoplamento, hardcoded paths, falta de testes
- [[Oportunidades de Refatoração Arquitetural]] — MVC, separação GUI/lógica, API

## 19 — Referências Técnicas
- [[Referências ABNT Completas]] — 6 referências do artigo + complementares

## 20 — Insights Estratégicos
- [[Análise Crítica do TGI]] ⭐⭐ — o que o artigo acerta, onde falha, o que omite
- [[Decisões Arquiteturais e Trade-offs]] — SQLite vs PostgreSQL, tkinter vs web, etc.
- [[Insights para o Artigo de Extensão]] — como aproveitar o EduPredict como base

---

## Referência Rápida

| Quero entender... | Nota |
|---|---|
| Por que o modelo tem 94%? | [[M3 — Modelo de Produção (Após N3)]] |
| O que é data leakage aqui? | [[Data Leakage — Conceito e Impacto]] |
| Qual feature é mais importante? | [[Feature Importance Detalhada — M3]] |
| Por que Recuperação tem 62%? | [[Matriz de Confusão M3 — Análise Detalhada]] |
| Como o slope é calculado? | [[slope notas — Tendência Temporal]] |
| O que o artigo deixou de fora? | [[Limitações Gerais do Artigo]] |
| Onde o código diverge do TGI? | [[Gaps — TGI vs EduNotas Atual]] |
| O que refatorar primeiro? | [[Débitos Técnicos Identificados]] |
