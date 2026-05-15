---
tags:
  - moc
  - tgi-codes
aliases:
  - Índice
  - Home
created: 2026-05-13
---

# TGI-CODES — Mapa do Conhecimento

> [!TIP] Navegação
> Este é o ponto de entrada do vault. Clique nos links para navegar pelas notas.

---

## Projeto

- [[Visão Geral]] — O que é o sistema, objetivos e status atual
- [[Roadmap]] — Próximos passos e metas futuras
- [[Melhorias 2026-05-14]] — Bugfixes e melhorias de UI (status de notas, dashboard ML, predições)
- [[Plano de Artigo ABNT]] — Plano de anotação científica: comportamento operacional, feedback e transparência familiar

---

## Arquitetura

- [[Arquitetura do Sistema]] — Como os módulos se conectam e o fluxo de dados
- [[Modelo de Dados]] — Schema da tabela `ml_features` e estrutura de arquivos

---

## Machine Learning

- [[Visão Geral ML]] — Pipeline completo de ML: debug → treino → análise
- [[Modelos RF (M1-M2-M3)]] — Detalhes dos três Random Forest e quando usar cada um
- [[Features e Cálculos]] — As 9 features, fórmulas de normalização e slope/variância
- [[Data Leakage]] — Problema detectado, features removidas e solução implementada

---

## Interface GUI

- [[Componentes e Páginas]] — Todas as páginas tkinter e seus métodos
- [[Fluxos de Execução]] — Sequência de chamadas para cada ação do usuário

---

## Módulos Python

- [[cads.py — Core do Sistema]] — Banco de dados, CRUD e geração de features
- [[Módulos ML]] — `ml_debug`, `ml_pipeline`, `ml_models`, `run_ml_pipeline`

---

## Guias

- [[Início Rápido]] — 7 passos para rodar o sistema do zero
- [[Como Contribuir]] — Padrões para adicionar novos módulos e documentação

---

## Referência de Código

- [[INDEX - Código]] — Índice de todos os arquivos `.py` com funções e referências cruzadas
  - [[cads.py]] — `get_conn`, `init_db`, `_slope`, `_std`, `gerar_features_ml`, ...
  - [[gui_escola.py]] — `App`, `BasePage`, `DashboardPage`, ...
  - [[gui_ml_advanced.py]] — `MLAdvancedPage`, `_train_models`, `_analyze_decision`, ...
  - [[gui_ml_integration.py]] — `MLModelLoader`, `DisciplinePerformanceAnalyzer`, ...
  - [[gui_predicoes_improved.py]] — `PredictionPageImproved`, `_load_aluno`, ...
  - [[train_simple.py]] — Pipeline autônomo de treino dos 3 modelos

---

## Referência Rápida

| Preciso... | Nota |
|---|---|
| Rodar o sistema agora | [[Início Rápido]] |
| Entender as features de ML | [[Features e Cálculos]] |
| Ver o fluxo de treino | [[Fluxos de Execução]] |
| Saber qual modelo usar | [[Modelos RF (M1-M2-M3)]] |
| Entender o banco de dados | [[Modelo de Dados]] |
| Adicionar novo módulo | [[Como Contribuir]] |
| Ver código de uma função | [[INDEX - Código]] |
