[← Raiz](../README.md) · [Índice](INDICE_DOCUMENTACAO.md) · [Resumo Executivo](RESUMO_EXECUTIVO.md) · [Cálculos ML](DOCUMENTACAO_CALCULOS.md) · [Guia Completo](GUIA_COMPLETO.md) · [Guia Predições](GUIA_PREDICOES.md)

---

# 🤖 Sistema de Machine Learning para Previsão de Status Acadêmico

Sistema completo de ML com Random Forest para classificação multiclasse do status do aluno (Reprovado, Recuperação, Aprovado).

## 🎯 Características Principais

- **3 Modelos Temporais**: M1 (N1), M2 (N1+N2), M3 (N1+N2+N3)
- **Detecção automática de data leakage**: Remove features que vazam informação do target
- **Debug completo de dados**: 10 validações diferentes
- **Explicabilidade**: Feature importance + SHAP analysis
- **Validação cruzada**: Estratificação e múltiplos folds
- **Pronto para produção**: Serialização e API de predição

## 📋 Estrutura dos Arquivos

```
├── ml_debug.py              # 🔍 Debug e validação de dados
├── ml_pipeline.py           # 🤖 Treinamento de modelos
├── ml_models.py             # 📊 Explicabilidade e análise
├── run_ml_pipeline.py       # 🚀 Script principal (orquestrador)
├── requirements.txt         # 📦 Dependências
└── ml_models/               # 📁 Modelos treinados
    ├── RF_M1_20240101_120000/
    ├── RF_M2_20240101_120000/
    └── RF_M3_20240101_120000/
```

## 🚀 Quick Start

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Preparar dados

```python
from cads import init_db, gerar_features_ml

# Inicializar banco de dados e criar features
init_db()
gerar_features_ml()
```

### 3. Executar pipeline completo

```bash
python run_ml_pipeline.py
```

Isso vai:
1. ✅ Executar debug completo
2. ✅ Treinar M1, M2, M3
3. ✅ Gerar gráficos de explicabilidade
4. ✅ Comparar e recomendar melhor modelo

## 🔍 Debug de Dados (ml_debug.py)

Executa 10 validações automáticas:

```python
from ml_debug import run_full_debug_report

# Executar todas as validações
results = run_full_debug_report(verbose=True)
```

### Validações incluídas:

1. **🚨 Detecção de Data Leakage** - Encontra features com correlação >0.9 com target
2. **✅ Consistência das Notas** - Valida intervalo [0-10], duplicatas, nulos
3. **📊 Média Ponderada** - Verifica cálculo correto (20%, 25%, 25%, 30%)
4. **📈 Distribuição de Classes** - Detecta desbalanceamento
5. **📊 Validação de Slope** - Verifica normalização e correlação
6. **📊 Validação de Variância** - Verifica normalização [0-1]
7. **🔗 Integridade de Contexto** - Valida media_turma_norm, pct_materias_ok
8. **⚠️ Detecção de Outliers** - Encontra anomalias nos dados
9. **📊 Análise de Drift** - Detecta mudanças entre turmas
10. **🔧 Teste de Robustez** - Verifica dependência excessiva de features

## 🤖 Treinamento de Modelos (ml_pipeline.py)

### Treinar modelo específico

```python
from ml_pipeline import train_random_forest, save_model

# M1: Apenas N1 (previsão muito antecipada)
model_m1, results_m1, mapping_m1 = train_random_forest("M1", verbose=True)

# M2: N1 + N2 (previsão intermediária)
model_m2, results_m2, mapping_m2 = train_random_forest("M2", verbose=True)

# M3: N1 + N2 + N3 (previsão robusta)
model_m3, results_m3, mapping_m3 = train_random_forest("M3", verbose=True)

# Salvar modelos
save_model(model_m3, results_m3, mapping_m3, "melhor_modelo")
```

### Usar modelo em produção

```python
from ml_pipeline import load_model, predict_student_status

# Carregar modelo
model_dir = "ml_models/RF_M3_20240101_120000"
model, results, mapping = load_model(model_dir)

# Predição para um aluno
prediction, error = predict_student_status(
    model_dir, 
    aluno_id=1, 
    materia_id=2
)

if error is None:
    print(f"Status: {prediction['predicted_label']}")
    print(f"Confiança: {prediction['confidence']:.2%}")
    print(f"Probabilities:")
    for label, prob in prediction['probabilities'].items():
        print(f"  {label}: {prob:.2%}")
```

### Métricas de treinamento

Para cada modelo você obtém:
- **Accuracy**: Acerto total
- **F1-Score (macro)**: Média de F1 por classe
- **F1-Score (weighted)**: F1 ponderado pelo suporte
- **Cross-Validation**: Scores e desvio padrão
- **Classification Report**: Precision, recall, F1 por classe
- **Confusion Matrix**: Matriz de confusão
- **Feature Importance**: Importância de cada feature

## 📊 Explicabilidade (ml_models.py)

### Feature Importance

```python
from ml_models import analyze_feature_importance

analysis = analyze_feature_importance(
    model_dir="ml_models/RF_M3_...",
    top_n=10,
    plot=True
)
```

Gera gráfico e ranking das 10 features mais importantes.

### Análise com SHAP

```python
from ml_models import analyze_with_shap

# Requer: pip install shap
shap_values, explainer = analyze_with_shap(
    model_dir="ml_models/RF_M3_...",
    sample_size=100,
    plot=True
)
```

Gera gráficos SHAP para explicabilidade avançada.

### Correlação Feature-Target

```python
from ml_models import analyze_feature_target_correlation

correlations = analyze_feature_target_correlation(
    model_dir="ml_models/RF_M3_...",
    plot=True
)
```

### Detecção de Overfitting

```python
from ml_models import detect_overfitting

detect_overfitting(model_dir="ml_models/RF_M3_...")
```

### Comparação entre modelos

```python
from ml_models import compare_models

compare_models()
```

Tabela comparativa de M1, M2, M3 com recomendação de qual usar.

## ⚙️ Hiperparâmetros

RandomForestClassifier configurado com:

```python
RandomForestClassifier(
    n_estimators=200,              # Número de árvores
    max_depth=None,                # Profundidade máxima (ilimitada)
    min_samples_split=2,           # Min. amostras para split
    min_samples_leaf=1,            # Min. amostras por folha
    class_weight='balanced',       # Peso equilibrado se desbalanceamento > 1.5x
    random_state=42,               # Reprodutibilidade
    n_jobs=-1,                     # Usar todos os cores
    verbose=0
)
```

Para ajustar conforme necessário:

```python
from ml_pipeline import train_random_forest

# Reduzir overfitting
model, results, mapping = train_random_forest(
    "M3",
    # Adicionar parâmetros customizados...
)
```

## 🎯 Features Utilizadas

### Modelo M1 (Previsão Muito Antecipada)
- `n1_norm`: Primeira avaliação normalizada

### Modelo M2 (Previsão Intermediária)
- `n1_norm`, `n2_norm`: Primeira e segunda avaliações
- `slope_notas`: Tendência de crescimento
- `variancia_notas`: Consistência das notas

### Modelo M3 (Previsão Robusta) ⭐
- `n1_norm`, `n2_norm`, `n3_norm`: Primeiras 3 avaliações
- `slope_notas`, `variancia_notas`: Comportamento
- `pct_materias_ok`: % materias com média >= 6
- `media_geral_aluno`: Média geral do aluno
- `serie_num_norm`: Série/ano normalizado
- `media_turma_norm`: Média da turma normalizada

**Removidas (data leakage):**
- ~~`media_pond_norm`~~ - Derivada do target
- ~~`n4_norm`~~ - Avaliação final

## 📈 Classes de Predição

| Classe | Label | Descrição |
|--------|-------|-----------|
| 0 | Reprovado | Média < 5.0 |
| 1 | Recuperação | 5.0 ≤ Média < 6.0 |
| 2 | Aprovado | Média ≥ 6.0 |

## 🔗 Integração com GUI

Para adicionar aba de ML na GUI:

```python
# Em gui_escola.py
from ml_pipeline import load_model, predict_student_status

class MLPredictionTab(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.model_dir = "ml_models/RF_M3_..."
        self.model, _, _ = load_model(self.model_dir)
    
    def predict_for_student(self, aluno_id, materia_id):
        prediction, error = predict_student_status(
            self.model_dir, aluno_id, materia_id
        )
        if error is None:
            return prediction
        return None
```

## 📊 Arquivos de Output

### 01_debug_results.json
```json
{
  "leakage": {
    "suspicious_count": 0,
    "suspicious": []
  },
  "consistency": { ... },
  "class_dist": { ... }
}
```

### 02_training_summary.json
```json
{
  "M1": {
    "status": "sucesso",
    "results": {
      "accuracy": 0.7234,
      "f1_macro": 0.6891,
      ...
    }
  },
  ...
}
```

### ml_models/RF_M3_20240101_120000/
```
├── model.pkl          # Modelo serializado
├── results.json       # Métricas de treinamento
├── mapping.json       # Metadados (feature names, etc)
└── metadata.json      # Info geral do modelo
```

## 🔧 Troubleshooting

### Erro: "Nenhuma feature gerada"
```python
from cads import gerar_features_ml
gerar_features_ml()  # Execute antes de treinar
```

### Erro: "Dados insuficientes"
```
Precisa de pelo menos 30 amostras com status_encoded != NULL
Verifique: SELECT COUNT(*) FROM ml_features WHERE status_encoded IS NOT NULL
```

### Erro: "SHAP não instalado"
```bash
pip install shap
```

### Baixa performance (accuracy < 0.6)
1. Aumentar número de amostras
2. Verificar qualidade dos dados (debug)
3. Adicionar mais features contextuais
4. Usar SMOTE para classes minoritárias

## 📚 Referências

- [Scikit-learn RandomForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [SHAP](https://shap.readthedocs.io/)
- [Best Practices em ML](https://developers.google.com/machine-learning/crash-course)

## 📝 Changelog

### v1.0 (Initial Release)
- ✅ Pipeline completo de ML
- ✅ Debug automático de dados
- ✅ Modelos temporais M1, M2, M3
- ✅ Explicabilidade com Feature Importance
- ✅ Validação cruzada
- ✅ Pronto para produção

## 📄 Licença

Projeto educacional - Livre para uso e modificação

## 👨‍💻 Autor

Sistema desenvolvido para TGI - Iniciativa de Tecnologia em Educação
