---
tags: [artigo, implementacao, mapeamento, teoria-codigo, relacao]
created: 2026-05-16
---

# Mapeamento Teoria → Código — EduPredict

[[INDEX - ARTIGO|← Índice]] | [[Arquitetura Modular — Visão Geral]] | [[Gaps — TGI vs EduNotas Atual]] | [[Débitos Técnicos Identificados]]

> [!INFO] Conecta cada conceito do artigo com sua implementação exata no código

---

## 1. Conceitos do Artigo → Implementação

| Conceito (Artigo) | Arquivo | Função/Classe | Linha aprox. |
|---|---|---|---|
| Geração de features ML | `01-CORE/cads.py` | `gerar_features_ml()` | ~150-250 |
| slope_notas | `01-CORE/cads.py` | `_slope(vals)` | ~80-95 |
| variancia_notas | `01-CORE/cads.py` | `_variancia(vals)` | ~97-108 |
| Detecção de leakage | `02-ML/train_simple.py` | `detect_leakage()` | ~45-60 |
| Treinamento M1/M2/M3 | `02-ML/train_simple.py` | função principal | ~70-150 |
| Seleção automática de modelo | `02-ML/gui_ml_integration.py` | `MLModelLoader.load_model()` | ~80-110 |
| Análise por aluno | `02-ML/gui_ml_integration.py` | `DisciplinePerformanceAnalyzer.analyze_student()` | ~130-200 |
| Interface de predições | `03-GUI/gui_predicoes_improved.py` | `PredictionsPageImproved` | classe completa |
| Dashboard com métricas | `03-GUI/gui_escola.py` | `DashboardPage` | ~300-500 |
| Tabela de features | `01-CORE/cads.py` | SQL schema `ml_features` | ~20-40 |

---

## 2. Features Teóricas → Código Real

### n1_norm, n2_norm, n3_norm, n4_norm

```python
# cads.py — normalização simples
n1_norm = n1 / 10.0 if n1 is not None else None
n2_norm = n2 / 10.0 if n2 is not None else None
n3_norm = n3 / 10.0 if n3 is not None else None
n4_norm = n4 / 10.0 if n4 is not None else None  # leaky — não usada no treino
```

### slope_notas

```python
# cads.py
def _slope(vals):
    n = len(vals)
    if n < 2:
        return 0.0
    xs = list(range(n))
    xm = sum(xs) / n
    ym = sum(vals) / n
    num = sum((x - xm) * (y - ym) for x, y in zip(xs, vals))
    den = sum((x - xm) ** 2 for x in xs)
    return num / den if den != 0 else 0.0
```

### media_pond_norm (leaky — visualização apenas)

```python
# cads.py — calculada mas excluída do treino
media_pond = (0.2*n1 + 0.25*n2 + 0.25*n3 + 0.30*n4) / 10.0
```

### status_encoded (target)

```python
# cads.py
if media_pond >= 0.6:  # >= 6,0 em escala original
    status_encoded = 2  # Aprovado
elif media_pond >= 0.5:  # >= 5,0
    status_encoded = 1  # Recuperação
else:
    status_encoded = 0  # Reprovado
```

---

## 3. Modelos → Arquivos

```
02-ML/models/
  model_m1.pkl    ← RandomForestClassifier com 2 features
  model_m2.pkl    ← RandomForestClassifier com 4-5 features
  model_m3.pkl    ← RandomForestClassifier com 9 features
  features_m1.pkl ← ['n1_norm', 'serie_num_norm']
  features_m2.pkl ← ['n1_norm', 'n2_norm', 'slope_notas', 'variancia_notas', 'serie_num_norm']
  features_m3.pkl ← [todas as 9 features]
```

---

## 4. EWS → Código

```python
# gui_ml_integration.py — DisciplinePerformanceAnalyzer
def _classify_profile(self, avg_risk):
    if avg_risk > 0.7:
        return "🔴 CRÍTICO - Atenção imediata"
    elif avg_risk > 0.4:
        return "🟡 EM RISCO - Acompanhamento"
    else:
        return "🟢 SEGURO - Desempenho normal"
```

**Thresholds 0,7 e 0,4** são arbitrários — não foram validados com especialistas pedagógicos. Ver [[Débitos Técnicos Identificados]].

---

## 5. Interface → Componentes

```
gui_escola.py:
  DashboardPage    ← Visão geral com métricas ML (alunos em risco por sala)
  NotasPage        ← Tabela de notas com status Aprovado/Recuperação/Reprovado
  RelatorioPage    ← Relatório consolidado com status
  MLPage           ← Tabela raw de ml_features para diagnóstico

gui_predicoes_improved.py:
  PredictionsPageImproved  ← Seleção de aluno + análise por modelo
  DisciplineCardImproved   ← Card por matéria com prognóstico e recomendações

gui_ml_advanced.py (02-ML/):
  MLAdvancedPage   ← Análise avançada (feature importance, distribuições)
```

---

## 6. Gaps Entre Artigo e Implementação Atual

| Descrito no artigo | Implementado? | Observação |
|---|---|---|
| 3 modelos temporais M1/M2/M3 | ✅ | Correto |
| Detecção de leakage com Pearson | ✅ | Correto |
| 9 features em M3 | ✅ | Correto |
| `class_weight='balanced'` | ✅ | Correto |
| EWS com 3 níveis | ⚠️ Parcial | Implementado, mas thresholds arbitrários |
| slope_notas consistente | ❌ | Inconsistência cads.py vs gui_ml_integration.py |
| Explicabilidade por aluno | ❌ | Apenas feature importance global |
| Loop de feedback docente | ❌ | Não implementado |
| LGPD compliance | ❌ | Não tratado |

---

## Links

- [[Arquitetura Modular — Visão Geral]]
- [[Gaps — TGI vs EduNotas Atual]]
- [[Débitos Técnicos Identificados]]
- [[cads.py — Análise Profunda]]
- [[gui ml integration py — Motor de Predição]]
- [[slope notas — Tendência Temporal]]
