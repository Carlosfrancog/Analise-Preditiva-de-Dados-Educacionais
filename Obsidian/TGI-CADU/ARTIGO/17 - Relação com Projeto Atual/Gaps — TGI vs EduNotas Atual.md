---
tags: [artigo, gaps, tgi, edunotas, relacao, compatibilidade]
created: 2026-05-16
---

# Gaps — TGI vs EduNotas Atual

[[INDEX - ARTIGO|← Índice]] | [[Mapeamento Teoria-Código]] | [[Débitos Técnicos Identificados]] | [[Análise Crítica do TGI]]

> [!INFO] O que o artigo descreve vs o que está no código — onde existem divergências

---

## 1. O Que o Artigo Descreve Corretamente

| Aspecto | Código Correspondente | Status |
|---|---|---|
| 3 modelos M1/M2/M3 | `02-ML/train_simple.py` + modelos pkl | ✅ Correto |
| Detecção de leakage com Pearson | `train_simple.py: detect_leakage()` | ✅ Correto |
| 9 features em M3 | `ml_features` schema + `gerar_features_ml()` | ✅ Correto |
| Random Forest com `class_weight` | `RandomForestClassifier(class_weight='balanced')` | ✅ Correto |
| StratifiedKFold 5-fold | `cross_val_score(cv=StratifiedKFold(5))` | ✅ Correto |
| Feature importance global | `clf.feature_importances_` | ✅ Correto |

---

## 2. O Que o Artigo Descreve mas Diverge no Código

| Aspecto | O que o artigo diz | O que o código faz | Impacto |
|---|---|---|---|
| **slope_notas** | Regressão linear `_slope()` | GUI usa `slope_pct = (n2-n1)/n1 * 100` | Prognósticos inconsistentes |
| **db_path** | `analyze_student(db_path, ...)` aceita caminho | `cads.get_conn()` ignora o parâmetro | Interface enganosa |
| **gui_ml_advanced.py** | Módulo de análise avançada | Arquivo em `02-ML/` não em `03-GUI/` | Import frágil |

---

## 3. O Que o Artigo Não Descreve mas Existe no Código

| Feature no código | Descrita no artigo? | Observação |
|---|---|---|
| **Dashboard ML** com "Em Risco" no DashboardPage | ❌ | Adição feita na sessão de melhorias 2026-05-14 |
| **Tag `recup`** (fundo amarelo) no Treeview de notas | ❌ | Melhoria de UI 2026-05-14 |
| **Correção do status** (media<6 não é necessariamente Recuperação) | ❌ | Bug corrigido 2026-05-14 |
| **gui_predicoes_improved.py** (página de predições melhorada) | Parcialmente | Extensão da interface básica |

---

## 4. O Que o Artigo Descreve mas NÃO Existe no Código

| Aspecto descrito | Implementado? | Prioridade |
|---|---|---|
| **LGPD compliance** | ❌ | Alta para produção |
| **Loop de feedback docente** | ❌ | Alta para extensão |
| **Protocolo formal de alertas EWS** | ❌ | Alta para produção |
| **Agrupamento por aluno no CV** | ❌ | Alta para rigor científico |
| **SHAP local** | ❌ | Média para extensão |
| **Calibração de thresholds EWS** | ❌ | Média |
| **Re-treinamento automático** | ❌ | Baixa para MVP |

---

## 5. Estado Atual vs Estado Descrito no Artigo

O artigo descreve o sistema em seu estado de TGI, que foi desenvolvido em ambiente acadêmico. O código atual (após as melhorias de 2026-05-14) está **mais avançado** que o artigo descreve em alguns aspectos:

**Melhorias pós-TGI aplicadas:**
- Correção do status tricolor (Aprovado/Recuperação/Reprovado)
- Dashboard com métricas de risco ML
- Interface de predições melhorada com tratamento de erros
- Documentação no vault Obsidian

**Débitos ainda presentes:**
- Inconsistência de slope (DT-01)
- db_path ignorado (DT-02)
- Guards de leakage ausentes (DT-03)
- GroupKFold não aplicado (DT-04)

---

## 6. Roadmap de Alinhamento

Para que o código corresponda completamente ao que um artigo de extensão descreveria:

```
Prioridade 1 (curto prazo — 1-2 semanas):
  □ Corrigir DT-01 (slope consistente)
  □ Corrigir DT-03 (guards de leakage)
  □ Corrigir DT-04 (GroupKFold)
  □ Documentar hiperparâmetros

Prioridade 2 (médio prazo — 1-3 meses):
  □ Implementar SHAP
  □ Implementar registro de alertas EWS
  □ Definir protocolo operacional
  □ Coletar dados reais de escola parceira

Prioridade 3 (longo prazo — 3-6 meses):
  □ Implementar feedback docente
  □ LGPD compliance
  □ Portal web para pais
  □ Incorporar frequência
```

---

## Links

- [[Mapeamento Teoria-Código]]
- [[Débitos Técnicos Identificados]]
- [[Análise Crítica do TGI]]
- [[Protocolo de Alertas EWS]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Incorporação de Frequência e Engajamento]]
- [[Plano de Artigo ABNT]]
