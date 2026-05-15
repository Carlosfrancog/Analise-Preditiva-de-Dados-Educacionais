[← Raiz](../README.md) · [Índice](INDICE_DOCUMENTACAO.md) · [Resumo Executivo](RESUMO_EXECUTIVO.md) · [Guia Completo](GUIA_COMPLETO.md) · [Arquitetura](ARQUITETURA_SISTEMA.md)

---

## 🚀 INÍCIO RÁPIDO - EXECUTE EM 5 MINUTOS

### Pré-requisito: Python 3.8+

```bash
python --version  # Deve ser 3.8 ou superior
```

---

## ⚡ 5 Passos

### 1️⃣ Instalar dependências (2 min)

```bash
cd C:\Users\carlos.eduardo\Desktop\CaduProjetos\TGI-CODES
pip install -r requirements.txt
```

**O que instala:**
- scikit-learn (Random Forest)
- pandas, numpy (dados)
- matplotlib (gráficos)
- openpyxl (Excel - já usa cads.py)
- shap (opcional, para explicabilidade avançada)

### 2️⃣ Preparar dados (1 min)

```python
# No Python console ou script
from cads import init_db, gerar_features_ml

init_db()
gerar_features_ml()
```

**O que faz:**
- Inicializa banco de dados SQLite
- Gera tabela `ml_features` com 20+ features calculadas
- Necessário fazer UMA VEZ

### 3️⃣ Executar ML Pipeline (2 min)

```bash
python run_ml_pipeline.py
```

**O que acontece:**
1. ✅ Debug completo de dados
2. ✅ Treina M1, M2, M3
3. ✅ Gera gráficos
4. ✅ Compara modelos
5. ✅ Salva resultados

**Outputs:**
- `01_debug_results.json` - Validação de dados
- `02_training_summary.json` - Métricas de treinamento
- `ml_models/RF_M3_...` - Modelo pronto para usar

### 4️⃣ Revisar Resultados

```bash
# Ver debug
python -c "import json; print(json.dumps(json.load(open('01_debug_results.json')), ensure_ascii=False, indent=2))" | head -50

# Ver resultados
python -c "import json; data = json.load(open('02_training_summary.json')); print(f\"M3 Accuracy: {data['M3']['results']['accuracy']:.4f}\")"
```

### 5️⃣ Usar o Modelo

```python
from ml_pipeline import predict_student_status
from pathlib import Path

# Encontrar modelo mais recente
import os
models = [d for d in os.listdir('ml_models') if d.startswith('RF_M3')]
model_dir = f"ml_models/{max(models)}"

# Predizer para um aluno
prediction, error = predict_student_status(model_dir, aluno_id=1, materia_id=1)

if not error:
    print(f"Status: {prediction['predicted_label']}")
    print(f"Confiança: {prediction['confidence']:.1%}")
    print(f"Probabilidades:")
    for label, prob in prediction['probabilidades'].items():
        print(f"  {label}: {prob:.1%}")
```

---

## 📊 Resultado Esperado

```
Após executar run_ml_pipeline.py você verá:

╔════════════════════════════════════════════════════════════════════════════╗
║ 🔍 SISTEMA COMPLETO DE DEBUG - PIPELINE DE DADOS ML                       ║
╚════════════════════════════════════════════════════════════════════════════╝

✅ STATUS DE QUALIDADE DOS DADOS:

  [✅] Data Leakage: Nenhuma variável suspeita
  [✅] Integridade: Todas as notas válidas  
  [✅] Média ponderada: Cálculos corretos
  [✅] Distribuição: Balanceada (1.5x)
  [✅] Outliers: Nenhum detectado

╔════════════════════════════════════════════════════════════════════════════╗
║ 🎯 RESULTADOS DO TREINAMENTO - M3                                        ║
╚════════════════════════════════════════════════════════════════════════════╝

📊 MÉTRICAS DE DESEMPENHO:
  Acurácia:          0.8234
  F1-Score (macro):  0.7891
  F1-Score (weighted): 0.8123

🔄 VALIDAÇÃO CRUZADA (5-fold):
  Scores:  [0.8012, 0.7856, 0.8145, 0.8234, 0.8056]
  Média:   0.8061 ± 0.0134

✅ Modelo M3 treinado e salvo em: ml_models/RF_M3_20240414_143022
```

---

## 🎓 Próximas Coisas Legais

### Ver gráficos gerados
```bash
# No File Explorer
ml_models/
  ├─ feature_importance_plot.png   # Quais features importam
  ├─ correlation_plot.png           # Correlação com target
  └─ shap_importance_plot.png      # Análise SHAP (avançado)
```

### Testar exemplos interativos
```bash
python example_usage.py
# Menu com 10 exemplos diferentes para explorar
```

### Integrar com GUI
```python
# Em gui_escola.py, adicionar:
from ml_gui_integration import MLModel

class MinhaGUI:
    def __init__(self):
        self.ml = MLModel("M3")  # Carrega automaticamente
    
    def prever_aluno(self, aluno_id, materia_id):
        pred = self.ml.predict(aluno_id, materia_id)
        return f"{pred['predicted_label']} ({pred['confidence']:.0%})"
```

---

## 🔧 Troubleshooting Rápido

### ❌ Erro: "ModuleNotFoundError: No module named 'sklearn'"
```bash
pip install scikit-learn pandas numpy matplotlib
```

### ❌ Erro: "Nenhuma feature gerada"
```python
from cads import gerar_features_ml
gerar_features_ml()  # Execute antes
```

### ❌ Erro: "Dados insuficientes"
Precisa de >= 30 amostras. Verifique:
```python
import sqlite3
conn = sqlite3.connect('escola.db')
count = conn.execute("SELECT COUNT(*) FROM ml_features WHERE status_encoded IS NOT NULL").fetchone()[0]
print(f"Amostras válidas: {count}")
```

Se < 30, adicione mais alunos/notas em `cads.py`

---

## 📚 Documentação Completa

Para detalhes, veja:
- **RESUMO_EXECUTIVO.md** - Visão geral do projeto
- **GUIA_COMPLETO.md** - Guia prático detalhado
- **ML_README.md** - Referência técnica
- Comentários nos arquivos `.py`

---

## ✅ Checklist

- [ ] Python 3.8+ instalado
- [ ] `pip install -r requirements.txt` executado
- [ ] `init_db()` e `gerar_features_ml()` rodados
- [ ] `python run_ml_pipeline.py` executado
- [ ] Resultados visualizados em `ml_models/`
- [ ] Exemplos testados com `python example_usage.py`
- [ ] Documentação lida

---

## 🎯 Pronto?

```bash
# Tudo em uma linha:
pip install -r requirements.txt && python -c "from cads import init_db, gerar_features_ml; init_db(); gerar_features_ml()" && python run_ml_pipeline.py
```

**Tempo total: ~5 minutos** ⏱️

---

## 💡 Se não tiver dados suficientes ainda

```python
# Gerar dados de teste
from cads import gerar_alunos_genericos, adicionar_materia, gerar_notas_aleatorias, atribuir_materias_todos, gerar_features_ml
import sqlite3

conn = sqlite3.connect('escola.db')

# Adicionar matérias (se necessário)
for materia in ['Português', 'Matemática', 'Ciências', 'História', 'Geografia']:
    adicionar_materia(materia)

# Adicionar alunos
for sala_id in [1, 2, 3]:
    gerar_alunos_genericos(10, sala_id)  # 10 alunos por sala

# Atribuir e gerar notas
atribuir_materias_todos()
gerar_notas_aleatorias()

# Gerar features
gerar_features_ml()

# Verificar
count = conn.execute("SELECT COUNT(*) FROM ml_features WHERE status_encoded IS NOT NULL").fetchone()[0]
print(f"✅ {count} amostras geradas")

conn.close()
```

Depois rodar: `python run_ml_pipeline.py`

---

**Bom começo! 🚀**

Qualquer dúvida, consulte `GUIA_COMPLETO.md`
