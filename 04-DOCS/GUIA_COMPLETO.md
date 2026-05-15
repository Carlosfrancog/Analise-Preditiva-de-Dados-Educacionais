[← Raiz](../README.md) · [Índice](INDICE_DOCUMENTACAO.md) · [Início Rápido](INICIO_RAPIDO.md) · [Resumo Executivo](RESUMO_EXECUTIVO.md) · [Arquitetura](ARQUITETURA_SISTEMA.md) · [Cálculos ML](DOCUMENTACAO_CALCULOS.md)

---

# 🚀 GUIA COMPLETO - SISTEMA DE MACHINE LEARNING PARA PREVISÃO ACADÊMICA

## 📋 Sumário

1. [Início Rápido](#início-rápido)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Etapas da Pipeline](#etapas-da-pipeline)
4. [Detecção de Data Leakage](#detecção-de-data-leakage)
5. [Modelos Temporais](#modelos-temporais)
6. [Explicabilidade](#explicabilidade)
7. [Integração com GUI](#integração-com-gui)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Preparar Dados (primeira vez)

```python
from cads import init_db, gerar_features_ml

init_db()
gerar_features_ml()  # Gera tabela ml_features com todas as features necessárias
```

### 3. Executar Pipeline Completo

```bash
python run_ml_pipeline.py
```

É isso! Isso vai:
- ✅ Executar debug completo (validação de dados)
- ✅ Treinar M1, M2, M3
- ✅ Gerar gráficos e análises
- ✅ Comparar modelos e recomendar

### 4. Usar o Modelo em Produção

```python
from ml_pipeline import load_model, predict_student_status

# Carregar modelo
model_dir = "ml_models/RF_M3_..."  # Copiar path do output anterior
model, results, mapping = load_model(model_dir)

# Predição
prediction, error = predict_student_status(model_dir, aluno_id=1, materia_id=2)

if not error:
    print(f"Status: {prediction['predicted_label']}")
    print(f"Confiança: {prediction['confidence']:.2%}")
```

---

## 📁 Estrutura do Projeto

```
TGI-CODES/
│
├── 🗄️ DATABASE
│   └── escola.db                    # SQLite com dados
│
├── 🐍 CÓDIGO PRINCIPAL
│   ├── cads.py                      # Sistema de cadastro (já existente)
│   ├── gui_escola.py                # GUI principal (já existente)
│   │
│   ├── 🤖 MÓDULOS DE ML
│   ├── ml_debug.py                  # Debug e validação de dados
│   ├── ml_pipeline.py               # Treinamento de modelos
│   ├── ml_models.py                 # Explicabilidade (Feature Importance, SHAP)
│   ├── ml_gui_integration.py        # Integração com GUI
│   │
│   ├── 🚀 EXECUÇÃO
│   ├── run_ml_pipeline.py           # Script principal (orquestrador)
│   ├── example_usage.py              # Exemplos de uso
│   │
│   └── 📚 DOCUMENTAÇÃO
│       ├── ML_README.md              # Documentação técnica
│       ├── GUIA_COMPLETO.md          # Este arquivo
│       └── requirements.txt          # Dependências Python
│
└── 📊 OUTPUTS (gerados automaticamente)
    ├── 01_debug_results.json         # Resultados do debug
    ├── 02_training_summary.json      # Resumo de treinamento
    ├── debug_results.json            # Debug detalhado
    ├── training_summary.json         # Summary de training
    │
    └── ml_models/                    # Modelos treinados
        ├── RF_M1_20240101_120000/    # Modelo M1
        │   ├── model.pkl
        │   ├── results.json
        │   └── mapping.json
        ├── RF_M2_20240101_120000/    # Modelo M2
        ├── RF_M3_20240101_120000/    # Modelo M3 (recomendado)
        ├── feature_importance_plot.png
        ├── correlation_plot.png
        └── shap_importance_plot.png
```

---

## 🔄 Etapas da Pipeline

### ETAPA 1: Debug de Dados (ml_debug.py)

Executa 10 validações automáticas:

```python
from ml_debug import run_full_debug_report

results = run_full_debug_report(verbose=True)
```

**O que valida:**

| # | Validação | Descrição |
|---|-----------|-----------|
| 1 | **Data Leakage** | Encontra features com correlação > 0.9 com target |
| 2 | **Integridade** | Verifica intervalo [0-10], duplicatas, nulos |
| 3 | **Média Ponderada** | Valida cálculo com pesos 20%, 25%, 25%, 30% |
| 4 | **Distribuição** | Detecta desbalanceamento de classes |
| 5 | **Slope Features** | Valida normalização [-1, +1] |
| 6 | **Variância** | Valida normalização [0, 1] |
| 7 | **Contexto** | Verifica media_turma_norm, pct_materias_ok |
| 8 | **Outliers** | Detecta anomalias (notas fora intervalo, etc) |
| 9 | **Drift** | Analisa mudanças entre turmas |
| 10 | **Robustez** | Testa dependência de features |

**Saída:**
- Relatório detalhado no console
- `debug_results.json` com resultados estruturados

---

### ETAPA 2: Treinamento (ml_pipeline.py)

Treina 3 modelos com diferentes níveis de informação:

```python
from ml_pipeline import train_all_models

all_results = train_all_models(verbose=True)
```

**Modelos treinados:**

```
M1: Apenas N1
   └─ Preditivo muito antecipado (até primeira prova)
   └─ 1 feature

M2: N1 + N2 + Comportamento
   └─ Preditivo intermediário (até segunda prova)
   └─ 4 features

M3: N1 + N2 + N3 + Contexto ⭐ (RECOMENDADO)
   └─ Preditivo robusto (até terceira prova)
   └─ 10 features
```

**Features por modelo:**

```
M1: [n1_norm]

M2: [n1_norm, n2_norm, 
     slope_notas, variancia_notas]

M3: [n1_norm, n2_norm, n3_norm,
     slope_notas, variancia_notas,
     pct_materias_ok, media_geral_aluno,
     serie_num_norm, media_turma_norm]

❌ REMOVIDAS (data leakage):
   media_pond_norm  (derivada do target)
   n4_norm          (predição do target)
```

**Métricas retornadas:**
- Accuracy
- F1-score (macro e weighted)
- Cross-validation scores
- Confusion matrix
- Classification report
- Feature importance

---

### ETAPA 3: Explicabilidade (ml_models.py)

Entender COMO e POR QUE o modelo faz cada predição:

```python
from ml_models import (
    analyze_feature_importance,
    analyze_feature_target_correlation,
    detect_overfitting,
    generate_explainability_report
)

# Feature importance (qual feature importa mais)
importance = analyze_feature_importance(model_dir, top_n=10, plot=True)

# Correlação linear com target
correlations = analyze_feature_target_correlation(model_dir, plot=True)

# Sinais de overfitting
detect_overfitting(model_dir)

# Relatório completo (gera múltiplos gráficos)
generate_explainability_report(model_dir, model_type="M3")
```

**SHAP Analysis (explicabilidade avançada):**

```bash
pip install shap
python ml_models.py  # Gera gráficos SHAP
```

---

### ETAPA 4: Comparação (ml_models.py)

Comparar os 3 modelos e escolher qual usar em produção:

```python
from ml_models import compare_models

compare_models()
```

Retorna tabela com:
- M1 vs M2 vs M3
- Accuracy, F1, CV scores
- Número de features
- Recomendação

---

## ⚠️ Detecção de Data Leakage

### O Problema

Features que "vazam" informação do target causam:
- ❌ Overfitting extremo
- ❌ Acurácia artificialmente alta (80%+)
- ❌ Modelo inútil em produção
- ❌ Impossível de usar para predição antecipada

### Features Suspeitas Identificadas

| Feature | Razão | Ação |
|---------|-------|------|
| `media_pond_norm` | **Calculada diretamente do target** | **REMOVER** |
| `n4_norm` | Nota final (prediz status direto) | **REMOVER** |

### Como é Feita a Detecção

```python
from ml_debug import detect_data_leakage

results = detect_data_leakage(verbose=True)

# Verifica:
# - Correlação > 0.9 com target
# - Features derivadas do target
# - Variáveis indisponíveis em tempo de predição
```

### Features SEGURAS (Sem Leakage)

```
✅ n1_norm, n2_norm, n3_norm    # Notas parciais
✅ slope_notas                   # Tendência (calculada de n1, n2, n3)
✅ variancia_notas               # Consistência (idem)
✅ pct_materias_ok               # % materias OK
✅ media_geral_aluno             # Média histórica
✅ serie_num_norm                # Série (contexto estático)
✅ media_turma_norm              # Média turma (sem incluir próprio aluno)
```

**Garantia:** Estas features estão disponíveis ANTES de saber a nota final, permitindo predição antecipada.

---

## 🕐 Modelos Temporais

### M1: Predição Muito Antecipada

**Quando usar:**
- Na primeira reunião com aluno (logo após N1)
- Para alerta MUITO cedo

**Características:**
```
Features: 1 (apenas n1_norm)
Acurácia esperada: 50-60%
Performance: Rápida
Utilidade: Alerta muito inicial
```

**Exemplo:**
```
Aluno got 7.5 em português na N1
M1 prediz: 70% aprovado, 20% recuperação, 10% reprovado
```

---

### M2: Predição Intermediária ⭐

**Quando usar:**
- Após N2 (metade do bimestre)
- Melhor ponto para intervenção

**Características:**
```
Features: 4 (n1, n2 + comportamento)
Acurácia esperada: 65-75%
Performance: Rápida
Utilidade: Balance perfeito
```

**Exemplo:**
```
Aluno: N1=7, N2=6
Tendência: Estável
M2 prediz: 65% aprovado, 25% recuperação, 10% reprovado
→ Estudante está no caminho certo
```

---

### M3: Predição Robusta ⭐⭐ (RECOMENDADO)

**Quando usar:**
- Após N3 (2/3 do bimestre)
- Melhor acurácia possível
- Dados para tomar decisçõsão finais

**Características:**
```
Features: 10 (n1, n2, n3 + comportamento + contexto)
Acurácia esperada: 75-85%
Performance: Muito rápida
Utilidade: Referência final
```

**Exemplo:**
```
Aluno: N1=7.5, N2=6.0, N3=5.5
Tendência: Decrescente ↓
% OK: 60%
M3 prediz: 50% recuperação, 30% reprovado, 20% aprovado
→ Aluno deve fazer reforço urgentemente
```

---

## 📊 Explicabilidade

### Feature Importance (Built-in Random Forest)

Mostra quais features mais importam para as predições:

```python
from ml_models import analyze_feature_importance

analysis = analyze_feature_importance(model_dir, top_n=10, plot=True)

# Output típico:
# n2_norm             0.3234  ████████████████████░░░░░░░░
# pct_materias_ok     0.2145  ███████████░░░░░░░░░░░░░░░
# media_geral_aluno   0.1876  ██████████░░░░░░░░░░░░░░░░
# slope_notas         0.1234  ███████░░░░░░░░░░░░░░░░░░░
# ...
```

**Interpretação:**
- Alta importância = feature influencia muito as predições
- Baixa importância = feature pouco usada
- Deve corresponder ao senso comum educacional

---

### Correlação Feature-Target

Mostra relação LINEAR entre cada feature e status final:

```python
from ml_models import analyze_feature_target_correlation

correlations = analyze_feature_target_correlation(model_dir, plot=True)

# Output típico:
# n3_norm              0.7234  ↑ Forte positiva
# slope_notas          0.4512  ↑ Moderada
# variancia_notas     -0.3456  ↓ Moderada negativa
# media_turma_norm     0.1234  ↑ Fraca
```

**Interpretação:**
- Positiva: Aumentar feature → Melhor status
- Negativa: Aumentar feature → Pior status

---

### SHAP Analysis

Explicabilidade avançada - por que o modelo faz cada predição:

```bash
pip install shap
python ml_models.py
```

Gera gráficos mostrando:
- Impacto de cada feature em cada predição
- Direção do impacto (aumento/diminuição)
- Magnitude comparativa

---

## 🔗 Integração com GUI

### Arquivo: ml_gui_integration.py

Fornece classes prontas para integrar com `gui_escola.py`:

```python
from ml_gui_integration import MLModel, MLPredictionEngine

# Opção 1: Carregamento simples
ml = MLModel("M3")  # Carrega automaticamente modelo mais recente

if ml.loaded:
    # Fazer predição
    prediction = ml.predict(aluno_id=1, materia_id=2)
    
    # Exibir na GUI
    status = prediction['predicted_label']
    confianca = prediction['confidence']
    print(f"Status: {status} ({confianca:.0%})")

# Opção 2: Predições em batch (múltiplos alunos)
engine = MLPredictionEngine("M3")

alunos = [
    {"aluno_id": 1, "materia_id": 1},
    {"aluno_id": 1, "materia_id": 2},
    {"aluno_id": 2, "materia_id": 1},
]

results = engine.predict_batch(alunos)
```

### Exemplo de Integração Completa

```python
import tkinter as tk
from tkinter import ttk
from ml_gui_integration import MLModel, format_prediction_for_display

class MLTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Carregar modelo
        self.ml = MLModel("M3")
        
        # UI
        ttk.Label(self, text="Preditar Status").pack()
        
        ttk.Label(self, text="Aluno ID:").pack()
        self.aluno_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.aluno_var).pack()
        
        ttk.Label(self, text="Matéria ID:").pack()
        self.materia_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.materia_var).pack()
        
        ttk.Button(self, text="Prever", command=self.predict).pack()
        
        # Resultado
        self.result_var = tk.StringVar(value="...")
        ttk.Label(self, textvariable=self.result_var).pack()
    
    def predict(self):
        try:
            aluno_id = int(self.aluno_var.get())
            materia_id = int(self.materia_var.get())
            
            prediction = self.ml.predict(aluno_id, materia_id)
            formatted = format_prediction_for_display(prediction)
            
            if formatted:
                text = f"{formatted['status']} ({formatted['confianca']})"
                self.result_var.set(text)
            else:
                self.result_var.set("Sem dados")
        except:
            self.result_var.set("Erro")
```

---

## 🔧 Troubleshooting

### ❌ "Nenhuma feature gerada"

```python
from cads import gerar_features_ml
gerar_features_ml()  # Execute antes de treinar
```

### ❌ "Dados insuficientes"

Precisa de >= 30 amostras com `status_encoded != NULL`

```sql
SELECT COUNT(*) FROM ml_features WHERE status_encoded IS NOT NULL;
```

Se < 30:
1. Adicionar mais alunos/materias/notas em `cads.py`
2. Executar `gerar_features_ml()` novamente

### ❌ "SHAP não instalado"

```bash
pip install shap
```

### ❌ "Modelo não encontrado"

```python
from pathlib import Path
from ml_pipeline import MODELS_DIR

# Ver modelos disponíveis
for model in MODELS_DIR.glob("RF_*"):
    print(model.name)
```

### ❌ "Baixa performance (accuracy < 0.6)"

1. **Verificar data leakage:**
   ```python
   from ml_debug import detect_data_leakage
   detect_data_leakage()
   ```

2. **Aumentar dados:**
   - Adicionar mais alunos
   - Adicionar mais matérias
   - Mais períodos

3. **Verificar qualidade:**
   ```python
   from ml_debug import validate_notes_consistency
   validate_notes_consistency()
   ```

4. **Usar técnicas avançadas:**
   - SMOTE para desbalanceamento
   - GridSearch para hiperparâmetros
   - Stacking com múltiplos modelos

---

## 📚 Comando Rápido

### Executar tudo de uma vez

```bash
# Preparar dados
python -c "from cads import init_db, gerar_features_ml; init_db(); gerar_features_ml()"

# Executar pipeline completo
python run_ml_pipeline.py

# Ver exemplos
python example_usage.py
```

### Usar modelo específico

```python
from ml_pipeline import load_model, predict_student_status

model_dir = "ml_models/RF_M3_20240101_120000"
prediction, error = predict_student_status(model_dir, aluno_id=1, materia_id=1)
print(prediction)
```

---

## 📞 Suporte

Para dúvidas:
1. Verifique `ML_README.md`
2. Veja exemplos em `example_usage.py`
3. Execute `run_ml_pipeline.py -h` para ajuda
4. Consulte docstrings: `python -c "from ml_pipeline import train_random_forest; help(train_random_forest)"`

---

## ✅ Checklist para Produção

- [ ] Data leakage detectado e removido
- [ ] Debug completo executado (0 erros críticos)
- [ ] M3 treinado com accuracy > 0.70
- [ ] Cross-validation scores estáveis
- [ ] Feature importance faz sentido
- [ ] Modelo testado com dados reais
- [ ] GUI integrada e testada
- [ ] Documentação atualizada
- [ ] Backup de modelos feito
- [ ] Monitoramento configurado

---

**Última atualização:** 2024-01-01
**Status:** ✅ Pronto para Produção
