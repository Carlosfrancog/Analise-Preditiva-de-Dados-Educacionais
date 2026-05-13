---
tags:
  - python
  - ml
  - modulos
  - tgi-codes
created: 2026-05-13
---

# Módulos ML — Referência

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## `ml_debug.py` (~800 linhas)

Responsável pelas **10 validações automáticas** do dataset antes do treino.

**Função principal:**
```python
from ml_debug import run_full_debug_report

results = run_full_debug_report(verbose=True)
# Retorna dict com resultado de cada validação
# Salva em 06-OUTPUT/01_debug_results.json
```

**Validações executadas:** [[Visão Geral ML#Três Etapas de Validação]]

---

## `ml_pipeline.py` (~600 linhas)

Pipeline de treinamento com remoção automática de data leakage.

**Funções principais:**
```python
from ml_pipeline import train_random_forest, predict_student_status

# Treinar
result = train_random_forest(model_type="M3")

# Predição em produção
prediction, error = predict_student_status(
    model_dir="ml_models/RF_M3_...",
    aluno_id=1,
    materia_id=2
)

print(prediction['predicted_label'])  # "Aprovado"
print(prediction['confidence'])       # 0.87
print(prediction['probabilities'])    # {0: 0.02, 1: 0.11, 2: 0.87}
```

---

## `ml_models.py` (~500 linhas)

Análise de explicabilidade dos modelos treinados.

**Funções principais:**
```python
from ml_models import analyze_feature_importance

# Feature importance com gráfico
analyze_feature_importance("ml_models/RF_M3_...", plot=True)
# Salva: feature_importance_plot.png

# Correlação feature-target
analyze_feature_target_correlation(df)
# Salva: correlation_plot.png

# SHAP (se instalado)
run_shap_analysis("ml_models/RF_M3_...", X_sample)
# Salva: shap_importance_plot.png
```

---

## `run_ml_pipeline.py` (~400 linhas)

**Orquestrador completo** — executa debug + treino + análise + comparação em sequência.

```bash
python run_ml_pipeline.py
```

**Sequência executada:**
1. `run_full_debug_report()` → valida dados
2. `train_all_models()` → treina M1, M2, M3
3. `analyze_feature_importance()` → gráficos
4. Comparação M1 vs M2 vs M3
5. Recomendação do melhor modelo

**Outputs:**
```
06-OUTPUT/
├── 01_debug_results.json
└── 02_training_summary.json

02-ML/ml_models/
├── feature_importance_plot.png
├── correlation_plot.png
└── shap_importance_plot.png  (se SHAP instalado)
```

---

## `ml_gui_integration.py` (~300 linhas)

Classes para integrar os modelos com tkinter.

```python
from ml_gui_integration import MLModel, MLPredictionEngine

# Carregar modelo
model = MLModel("M3")  # carrega RF_M3.pkl automaticamente

# Predição simples
pred = model.predict(aluno_id=5, materia_id=3)

# Predição em batch (não trava a GUI — usa threading)
engine = MLPredictionEngine()
engine.predict_batch(alunos_ids, callback=atualizar_gui)
```

---

## `example_usage.py` (~400 linhas)

Menu interativo com 10 exemplos práticos:

```bash
python example_usage.py
# Exibe menu:
# 1. Debug rápido
# 2. Treinar M3
# 3. Predição única
# 4. Predição em batch
# 5. Feature importance
# ... etc
```

---

## Links Relacionados

- [[Pipeline de Treinamento]] — sequência completa do treino
- [[Data Leakage]] — o que ml_debug detecta
- [[Modelos RF (M1-M2-M3)]] — modelos gerados por ml_pipeline
- [[Início Rápido]] — como executar tudo do zero
