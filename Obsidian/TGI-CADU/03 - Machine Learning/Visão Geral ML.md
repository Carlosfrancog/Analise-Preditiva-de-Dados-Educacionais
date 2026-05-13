---
tags:
  - ml
  - tgi-codes
created: 2026-05-13
---

# Visão Geral — Machine Learning

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## O Problema

Prever se um aluno será **Aprovado**, ficará em **Recuperação** ou será **Reprovado** antes do fim do ano letivo, permitindo intervenção pedagógica antecipada.

---

## Pipeline Completo

```
Notas (N1–N4)
    ↓
Calcular Features Brutas (cads.gerar_features_ml)
    ↓
Normalizar Features para [0, 1]
    ↓
Remover Data Leakage automático
    ↓
Treinar Random Forest (train_simple.py ou gui_ml_advanced)
    ↓
Serializar modelo (.pkl + metadata.json)
    ↓
Predição em tempo real via DisciplinePerformanceAnalyzer
    ↓
Exibir resultado no dashboard
```

---

## Três Etapas de Validação

Antes de treinar, `ml_debug.py` executa **10 validações automáticas**:

| # | Validação | O que detecta |
|---|---|---|
| 1 | Data Leakage | Features com correlação ≥ 0.9 com target |
| 2 | Integridade | Notas fora do intervalo [0-10] ou duplicatas |
| 3 | Média Ponderada | Cálculo incorreto com pesos N1-N4 |
| 4 | Distribuição | Desbalanceamento de classes |
| 5 | Feature Slope | Normalização fora de [-1, +1] |
| 6 | Feature Variância | Normalização fora de [0, 1] |
| 7 | Contexto | Integridade de agregados por turma |
| 8 | Outliers | Anomalias nas notas |
| 9 | Drift | Diferença de distribuição entre turmas |
| 10 | Robustez | Dependência excessiva de uma só feature |

---

## Classes de Predição

O modelo classifica cada aluno em uma de três classes:

| Código | Label | Significado |
|---|---|---|
| 0 | Reprovado | Média final abaixo de 5 |
| 1 | Recuperação | Média entre 5 e 6 (zona de risco) |
| 2 | Aprovado | Média final ≥ 6 |

---

## Tecnologias

- **scikit-learn** — `RandomForestClassifier`
- **pandas** — manipulação do dataset
- **numpy** — cálculos de slope e variância
- **SHAP** (opcional) — explicabilidade por predição individual
- **pickle** — serialização dos modelos

---

## Links Relacionados

- [[Modelos RF (M1-M2-M3)]] — detalhes e comparação dos três modelos
- [[Features e Cálculos]] — como cada feature é calculada
- [[Data Leakage]] — problema identificado e solução
- [[Módulos ML]] — código-fonte dos módulos
- [[Pipeline de Treinamento]] — passo a passo do treino
