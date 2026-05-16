---
tags: [artigo, arquitetura, compatibilidade, integracao, codigo]
created: 2026-05-16
---

# Compatibilidade Arquitetural — TGI vs EduNotas

[← Índice](<../INDEX - ARTIGO.md>) | [[Gaps — TGI vs EduNotas Atual]] | [[Mapeamento Teoria-Código]] | [[Arquitetura Modular — Visão Geral]]

---

## 1. O Que É Compatibilidade Aqui

"Compatibilidade arquitetural" refere-se à capacidade de integrar as melhorias propostas no artigo ao código existente do EduNotas **sem reescrever a base**. A pergunta central: as sugestões teóricas do TGI são implementáveis na arquitetura atual?

---

## 2. Arquitetura Atual — Resumo

```
01-CORE/cads.py          ← banco SQLite + features ML + CRUD
02-ML/train_simple.py    ← pipeline de treino (standalone)
02-ML/gui_ml_integration.py ← motor de predição (MLModelLoader + Analyzer)
03-GUI/gui_escola.py     ← janela principal + roteamento de páginas
03-GUI/gui_predicoes_improved.py ← UI de predições
03-GUI/gui_ml_advanced.py    ← UI de treino e análise
```

---

## 3. Compatibilidade por Melhoria Proposta

### SHAP — Explicabilidade Local

**Compatibilidade:** Alta — pode ser adicionado sem modificar a arquitetura

```python
# Adicionar em gui_ml_integration.py:
import shap

explainer = shap.TreeExplainer(self.models["RF_M3"])
shap_values = explainer.shap_values(df_features)
# Integra diretamente com o MLModelLoader existente
```

**Ponto de integração:** `MLModelLoader.predict()` — retornar `shap_values` junto com `pred, proba`.

### GroupKFold — Validação sem Leakage

**Compatibilidade:** Alta — apenas modifica `train_simple.py`

```python
# Mudança cirúrgica em train_simple.py:
# Antes: StratifiedKFold(n_splits=5)
# Depois: GroupKFold(n_splits=5) com groups=df['aluno_id']
# Sem impacto na arquitetura GUI
```

### Frequência como Feature

**Compatibilidade:** Média — requer nova tabela + nova coluna em ml_features

```python
# Mudanças necessárias:
# 1. cads.py: nova tabela presencas(aluno_id, materia_id, aulas_total, faltas)
# 2. cads.py: gerar_features_ml() + pct_presenca_norm
# 3. train_simple.py: adicionar feature à lista
# 4. gui_ml_integration.py: calcular pct_presenca na predição em tempo real
# PROBLEMA: pct_presenca_norm = 0.5 hardcoded inevitável se dado ausente
```

### LGPD — Conformidade

**Compatibilidade:** Baixa — requer mudanças transversais

```python
# Mudanças necessárias:
# - gui_escola.py: banner de aviso de IA
# - cads.py: nova tabela consentimentos(aluno_id, responsavel, data, aceito)
# - gui_escola.py: nova página "Minha Privacidade" (alunos/responsáveis)
# - gui_ml_integration.py: log de acesso às predições
# Nenhuma dessas quebra a arquitetura, mas requerem muito trabalho
```

---

## 4. Pontos de Integração Arquitetural

```
cads.py (Core)
  ↓ nova tabela → facilita SHAP storage, presencas, consentimentos

MLModelLoader (gui_ml_integration.py)
  ↓ retornar shap_values → suporta SHAP na UI sem mudança de interface

train_simple.py
  ↓ GroupKFold + novas features → retrocompatível via metadata.json

gui_predicoes_improved.py
  ↓ renderizar SHAP chart por aluno → requer novo widget tkinter
```

---

## 5. O Débito Mais Bloqueante — DT-01

O débito DT-01 (features erradas na predição) é o mais urgente antes de qualquer melhoria:

```python
# Estado atual: features incorretas → predições inválidas
features_pred = [n1, n2, 0, 0, slope, variancia, media_norm, 0.5, 0.5]

# Correção necessária: ler ml_features do banco
features_pred = [features_row[f] for f in feature_names]
```

Qualquer melhoria construída sobre a arquitetura atual herda esse problema. Corrigir DT-01 é **pré-requisito arquitetural** para implementar SHAP, alertas EWS, e outras melhorias.

---

## 6. Compatibilidade com Extensão do Artigo

As melhorias propostas em [[Gaps — TGI vs EduNotas Atual]] foram avaliadas:

| Melhoria | Compatibilidade | Pré-requisito |
|---|---|---|
| SHAP local | ✅ Alta | DT-01 corrigido |
| GroupKFold | ✅ Alta | Nenhum |
| Frequência | 🟡 Média | Nova tabela em cads.py |
| Alertas EWS | ✅ Alta | DT-01 corrigido |
| LGPD | 🔴 Baixa | Redesign de GUI |
| Portal familiar | 🔴 Baixa | Nova aplicação web |

---

## Links

- [[Gaps — TGI vs EduNotas Atual]]
- [[Mapeamento Teoria-Código]]
- [[Débitos Técnicos Identificados]]
- [[Arquitetura Modular — Visão Geral]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Incorporação de Frequência e Engajamento]]
- [[Oportunidades de Refatoração Arquitetural]]
