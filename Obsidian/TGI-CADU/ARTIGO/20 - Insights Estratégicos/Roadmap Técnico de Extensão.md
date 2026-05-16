---
tags: [artigo, roadmap, extensao, futuro, planejamento]
created: 2026-05-16
---

# Roadmap Técnico de Extensão

[← Índice](<../INDEX - ARTIGO.md>) | [[Insights para o Artigo de Extensão]] | [[Gaps — TGI vs EduNotas Atual]] | [[Compatibilidade Arquitetural]]

---

## 1. Correções Prioritárias (Antes de Qualquer Extensão)

### Sprint 1 — Débitos Críticos (1-2 semanas)

```
[ ] DT-01: Corrigir features incorretas na predição em tempo real
    - gui_ml_integration.py linhas 283-295
    - Ler features do banco (ml_features) em vez de calcular na mão

[ ] DT-04: GroupKFold para evitar vazamento intra-aluno
    - train_simple.py: substituir StratifiedKFold por GroupKFold
    - Re-avaliar e reportar acurácia real (esperado -3 a -7pp)

[ ] DT-03: Adicionar guards de leakage em cads.py
    - LEAKY_FEATURES = frozenset(['media_pond_norm', 'n4_norm'])
    - Assertion em train_simple.py
```

---

## 2. Melhorias de Primeira Ordem (1-3 meses)

### SHAP Local por Aluno

```
[ ] pip install shap
[ ] Integrar TreeExplainer em MLModelLoader
[ ] Widget de gráfico de barras SHAP em gui_predicoes_improved.py
[ ] Texto de explicação gerado automaticamente a partir dos valores SHAP
```

Estimativa: 2-3 semanas de desenvolvimento.

### Alertas EWS Automatizados

```
[ ] Nova tabela alertas_ews em cads.py
[ ] Scheduler periódico (verificar novos dados → gerar alertas)
[ ] Notificação na UI (badge contador na aba de predições)
[ ] Dashboard de alertas pendentes
```

Estimativa: 3-4 semanas.

---

## 3. Melhorias de Segunda Ordem (3-6 meses)

### Frequência como Feature

```
[ ] Nova tabela presencas(aluno_id, materia_id, bimestre, aulas_dadas, faltas)
[ ] gerar_features_ml(): calcular pct_presenca_norm
[ ] Coletar dados reais de frequência (ou gerar sinteticamente correlacionado com notas)
[ ] Re-treinar modelos com feature adicional
[ ] Avaliar ganho: Recall(Recuperação) com vs sem frequência
```

Estimativa: 1-2 meses (coleta de dados é o gargalo).

### Módulo de Feedback Docente

```
[ ] Nova tabela feedback_docente em cads.py
[ ] Botões de feedback nos cards de disciplina
[ ] Dashboard de eficácia do sistema
[ ] Exportação de relatório de impacto
```

Estimativa: 3-4 semanas.

---

## 4. Extensões de Pesquisa (6-12 meses)

### Validação com Dados Reais

```
[ ] Contato com escola parceira
[ ] Protocolo de pesquisa (TCLE, LGPD, CEP se necessário)
[ ] Coleta de dados anonimizados: 3 turmas, 1 ano letivo
[ ] Comparação: acurácia em dados sintéticos vs reais
[ ] Análise de viés por série, gênero, turno
```

### Artigo de Extensão

```
[ ] Seção de metodologia: GroupKFold + dados reais
[ ] Seção de resultados: comparação M1-M3 + XGBoost + LR
[ ] Seção de SHAP: análise de viés algorítmico
[ ] Seção de estudo de usuário: adoção por professores
[ ] Submissão: SBIE 2027 ou RBIE
```

---

## 5. Dependências Entre Iniciativas

```
DT-01 (correção features)
    └→ SHAP local (precisa de predições corretas)
    └→ Alertas EWS (baseados em predições corretas)
    └→ Feedback docente (feedback sobre predições corretas)

DT-04 (GroupKFold)
    └→ Artigo de extensão (métricas honestas)

Frequência como Feature
    └→ Re-treino completo dos modelos
    └→ Atualização do metadata.json
    └→ Atualização da interface de entrada de dados
```

---

## 6. KPIs para Avaliar Sucesso

| Indicador | Baseline (atual) | Meta |
|---|---|---|
| Acurácia M3 (GroupKFold) | ~94% (StratifiedKFold) | ~88-91% real |
| Recall(Recuperação) | 62.2% | >75% |
| Taxa de adoção docente | 0% (não medido) | >50% professores em 6 meses |
| Tempo até ação pedagógica | N/A | <48h após alerta |

---

## Links

- [[Insights para o Artigo de Extensão]]
- [[Débitos Técnicos Identificados]]
- [[Compatibilidade Arquitetural]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Protocolo de Alertas EWS]]
- [[Módulo de Feedback Docente]]
- [[Incorporação de Frequência e Engajamento]]
