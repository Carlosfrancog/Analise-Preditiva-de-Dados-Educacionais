[← Raiz](../README.md) · [Índice](INDICE_DOCUMENTACAO.md) · [Resumo Executivo](RESUMO_EXECUTIVO.md) · [Cálculos ML](DOCUMENTACAO_CALCULOS.md) · [Estrutura do Projeto](ESTRUTURA_PROJETO.md) · [Guia Predições](GUIA_PREDICOES.md)

---

# 🏗️ ARQUITETURA DO SISTEMA COMPLETO

**Visão geral de como tudo se conecta**

---

## 🔗 FLUXO DE DADOS COMPLETO

```
┌──────────────────────────────────────────────────────────────────┐
│                    🎯 APLICAÇÃO PRINCIPAL                        │
│                      gui_escola.py                                │
│  (Gerencia navegação, tema, layout geral)                        │
└─────────────┬──────────────────────────────┬─────────────────────┘
              │                              │
              ↓ cads.import               ↓ gui_*.import
    ┌─────────────────────┐      ┌──────────────────────────┐
    │  BANCO DE DADOS     │      │   CAMADA DE UI           │
    │  ───────────────    │      │   ────────────           │
    │  cads.py            │      │                          │
    │  schema.db          │      │  • gui_predicoes.py      │
    │                     │      │  • gui_predicoes_improv  │
    │ ├─ alunos           │      │  • gui_ml_advanced.py ⭐ │
    │ ├─ materias         │      └──────────────────────────┘
    │ ├─ notas            │
    │ ├─ salas            │
    │ └─ ml_features      │
    └──────────┬──────────┘
               │
        ┌──────┴────────────┐
        ↓                   ↓
    ┌──────────────┐   ┌─────────────────┐
    │ GERAÇÃO DE   │   │   INTEGRAÇÃO    │
    │ FEATURES     │   │   ML + GUI      │
    │ ────────────│   │ ─────────────────│
    │ cads.py      │   │ gui_ml_integra  │
    │ _slope()     │   │ tion.py         │
    │ _std()       │   │                 │
    │ gerar_feat   │   │ DisciplinePerf  │
    │   _ml()      │   │ AnalyzerClass   │
    └──────────────┘   └─────────────────┘
        │                       ↑
        └───────────┬───────────┘
                    ↓
    ┌──────────────────────────────┐
    │  MACHINE LEARNING            │
    │  ──────────────────────────  │
    │                              │
    │ 📊 train_simple.py           │
    │    ├─ Load data              │
    │    ├─ Split train/test       │
    │    ├─ RF_M1 (100 árv)        │
    │    ├─ RF_M2 (150 árv) ← Mensagnar da Produção
    │    ├─ RF_M3 (200 árv) ← Usar em Produção
    │    └─ Save .pkl + metadata   │
    │                              │
    │ 🤖 gui_ml_advanced.py (NEW)  │
    │    ├─ _train_all_models()    │
    │    ├─ _train_m3_only()       │
    │    ├─ _analyze_decision()    │
    │    └─ _show_training_summary │
    │                              │
    │ 📁 ml_models/                │
    │    ├─ RF_M1.pkl              │
    │    ├─ RF_M1_metadata.json    │
    │    ├─ RF_M2.pkl              │
    │    ├─ RF_M2_metadata.json    │
    │    ├─ RF_M3.pkl ⭐           │
    │    ├─ RF_M3_metadata.json    │
    │    └─ training_summary.json  │
    │                              │
    │ 📊 ml_dataset.csv            │
    │    (features normalizadas)   │
    │                              │
    └──────────────────────────────┘
```

---

## 🎯 COMPONENTES PRINCIPAIS

### 1. **Core: cads.py**
```
Responsabilidade: Banco de dados + Operações CRUD

Funções Principais:
├─ init_db()              → Cria schema do banco
├─ get_salas()            → Lista salas
├─ get_alunos()           → Lista alunos
├─ get_materias()         → Lista matérias
├─ get_notas()            → Retorna notas de um aluno
├─ _slope(vals)           → Calcula tendência linear
├─ _std(vals)             → Calcula desvio padrão
├─ gerar_features_ml()    → Gera 9 features para ML
├─ exportar_ml_csv()      → Salva dataset em CSV
└─ get_ml_stats()         → Estatísticas do dataset

Dados Persistidos:
├─ ml_features (9 colunas)
├─ status_encoded (0, 1, 2)
└─ metadata (aluno, matéria, sala, etc)
```

### 2. **UI: gui_predicoes_improved.py**
```
Responsabilidade: Dashboard de Predições (Analytics)

PredictionPageImproved
├─ Carrega dados do aluno
├─ Calculate status for each discipline
├─ Filter by: Aprovadas, Recuperação, Reprovadas, etc
├─ Show recommendation engine
├─ Display N4 preview if not filled
└─ Canvas + Scrollbar for many disciplines

Usa:
├─ cads.py → Buscar dados
├─ gui_ml_integration.py → Analisar desempenho
└─ gui_predicoes_improved.py::_prever_n4() → Forecast
```

### 3. **ML Integration: gui_ml_integration.py**
```
Responsabilidade: Análise de Desempenho + Prognósticos

MLModelLoader
├─ Carrega modelos (.pkl + metadata.json)
├─ predict() → Faz predição com features

DisciplinePerformanceAnalyzer
├─ analyze_student() → Análise completa de 1 aluno
├─ Calcula features normalizadas
├─ Passa por modelo RF_M3
├─ Compara previsão vs realidade
├─ Gera prognósticos (vai melhorar, vai piorar, etc)
└─ Coloca cores (verde, laranja, vermelho)

Usa:
├─ cads.py → Buscar notas e contexto
├─ sklearn → Para predições
└─ numpy → Para cálculos
```

### 4. **ML Dashboard: gui_ml_advanced.py** (NEW)
```
Responsabilidade: Treinar, visualizar, configurar ML

MLAdvancedPage (classe nova)
├─ _create_model_card() → Visualiza modelos com acurácia
├─ _generate_features() → Chama cads.gerar_features_ml()
├─ _train_all_models() → Treina 3 modelos
├─ _train_m3_only() → Treina apenas produção
├─ _train_models() → Executa treino
├─ _show_training_summary() → Mostra resumo
├─ _analyze_decision() → Analisa 1 aluno+matéria
└─ refresh() → Atualiza comboboxes

Interface:
├─ Cards de modelos
├─ Botões de treino
├─ Barra de progresso
├─ Análise de decisões
├─ Sliders para pesos
└─ Resumo automático

Usa:
├─ cads.py → Buscar dados
├─ pandas → Para manipular dataset
├─ sklearn → Para treinar modelos
├─ pickle → Para salvar modelos
└─ sqlite3 → Acesso ao banco
```

### 5. **Training: train_simple.py**
```
Responsabilidade: Treino automático dos modelos

Pipeline:
1. gerar_features_ml() → Gera features em ml_features
2. exportar_ml_csv() → Salva em ml_dataset.csv
3. pd.read_csv() → Carrega em pandas
4. train_test_split() → 80/20
5. RandomForestClassifier() → Treina cada modelo
6. pickle.dump() → Salva .pkl
7. json.dump() → Salva metadata

Modelos Treinados:
├─ RF_M1: 100 árvores, max_depth=5
├─ RF_M2: 150 árvores, max_depth=10
└─ RF_M3: 200 árvores, sem limite de profundidade

Output:
├─ ml_models/RF_M*.pkl
├─ ml_models/RF_M*_metadata.json
└─ training_summary.json
```

---

## 🔄 FLUXOS DE EXECUÇÃO

### **Fluxo 1: Iniciar Aplicação**
```
python gui_escola.py
     ↓
gui_escola.py::App.__init__()
     ├─ cads.init_db()
     ├─ _build_ui()
     ├─ Cria páginas (cads, alunos, ml, etc)
     └─ Exibe sidebar + main area
     ↓
Usuário clica em "🤖 Machine Learning"
     ↓
gui_ml_advanced.py::MLAdvancedPage._build()
     ├─ _create_model_card() para cada modelo
     ├─ _load_model_info() busca metadata
     ├─ Cria interface com 4 seções
     └─ refresh() carrega alunos e matérias
```

### **Fluxo 2: Gerar Features**
```
Usuário clica "🔄 Gerar Features"
     ↓
MLAdvancedPage._generate_features()
     ├─ Extrai pesos dos sliders
     ├─ Normaliza para somar 1.0
     ├─ cads.PESOS_NOTAS = pesos
     ├─ cads.gerar_features_ml()
     │  ├─ SELECT notas, aluno, materia, sala
     │  ├─ Para cada (aluno, materia):
     │  │  ├─ Calcular media_ponderada
     │  │  ├─ Normalizar: n1_norm = n1/10, etc
     │  │  ├─ Calcular slope com regressão
     │  │  ├─ Calcular variancia com desvio padrão
     │  │  └─ INSERT INTO ml_features
     │  └─ RETURN total, stats
     ├─ _update_stats()
     └─ Exibe: "✅ 15613 features geradas"
```

### **Fluxo 3: Treinar Modelos**
```
Usuário clica "🚀 Treinar Todos"
     ↓
MLAdvancedPage._train_models(["RF_M1", "RF_M2", "RF_M3"])
     ├─ status: "⏳ Carregando dados..."
     ├─ pd.read_csv("ml_dataset.csv")
     ├─ train_test_split(80/20)
     ├─ Para cada modelo:
     │  ├─ status: "⏳ Treinando RF_M1..."
     │  ├─ RandomForestClassifier().fit(X_train, y_train)
     │  ├─ y_pred = model.predict(X_test)
     │  ├─ accuracy = accuracy_score(y_test, y_pred)
     │  ├─ pickle.dump(model, f"RF_M1.pkl")
     │  ├─ json.dump(metadata, f"RF_M1_metadata.json")
     │  └─ progress += 20%
     ├─ _show_training_summary(results)
     └─ status: "✅ Treinamento concluído!"
```

### **Fluxo 4: Analisar Decisão**
```
Usuário seleciona Aluno + Matéria + clica "Analisar"
     ↓
MLAdvancedPage._analyze_decision()
     ├─ SELECT * FROM ml_features WHERE aluno_nome=?, materia_nome=?
     ├─ Formata análise:
     │  ├─ INFORMAÇÕES: aluno, matéria, série
     │  ├─ NOTAS: N1, N2, N3, N4 + normalizados
     │  ├─ FEATURES: slope, variância, etc
     │  ├─ RESULTADO: status real
     │  └─ INTERPRETAÇÃO: em linguagem natural
     ├─ text.insert(output)
     └─ Exibe análise formatada no widget
```

---

## 📊 MODELO DE DADOS

### **Tabela: ml_features**
```sql
CREATE TABLE ml_features (
    -- IDs
    aluno_id INTEGER,
    materia_id INTEGER,
    
    -- Informações de contexto
    aluno_nome TEXT,
    materia_nome TEXT,
    sala_nome TEXT,
    serie_num INTEGER,
    
    -- Notas brutas (0-10)
    n1 REAL,
    n2 REAL,
    n3 REAL,
    n4 REAL,
    
    -- Notas normalizadas (0-1)
    n1_norm REAL,
    n2_norm REAL,
    n3_norm REAL,
    n4_norm REAL,
    
    -- Features para ML
    media_ponderada REAL,
    media_pond_norm REAL,
    media_geral_aluno REAL,
    slope_notas REAL,
    variancia_notas REAL,
    serie_num_norm REAL,
    pct_materias_ok REAL,
    media_turma_norm REAL,
    
    -- Target
    status_encoded INTEGER (0, 1, 2),
    status_label TEXT ("Reprovado", "Recuperação", "Aprovado"),
    
    -- Metadata
    gerado_em TIMESTAMP
);
```

### **Arquivo: RF_M3_metadata.json**
```json
{
    "accuracy": 0.94,
    "f1": 0.940,
    "n_features": 9,
    "features": [
        "n1_norm", "n2_norm", "n3_norm", "n4_norm",
        "slope_notas", "variancia_notas", "media_geral_aluno",
        "serie_num_norm", "media_turma_norm"
    ],
    "n_samples_train": 12490,
    "n_samples_test": 3123,
    "date": "2026-04-14 15:32:00",
    "confusion_matrix": [[...], [...], [...]]
}
```

---

## 🎨 ESTRUTURA DE UI

```
gui_escola.py
└─ Frame: self.main
    └─ Pages (sobrepostas com place)
        ├─ DashboardPage
        ├─ AlunosPage
        ├─ SalasPage
        ├─ MateriasPage
        ├─ NotasPage
        ├─ PredictionPageImproved
        │   └─ Usa gui_ml_integration.py
        ├─ RelatorioPage
        └─ MLAdvancedPage (NEW)
            ├─ Summary Frame
            │   ├─ Model Cards (RF_M1, M2, M3)
            │   └─ Accuracy + Date per model
            ├─ Training Frame
            │   ├─ Feature Generation Button
            │   ├─ Train All Button
            │   ├─ Train M3 Button
            │   ├─ Progress Bar
            │   └─ Status Label
            ├─ Analysis Frame
            │   ├─ Aluno Combobox
            │   ├─ Materia Combobox
            │   ├─ Analyze Button
            │   └─ Text Widget (análise)
            └─ Weights Frame
                ├─ N1 Slider (0-50%)
                ├─ N2 Slider (0-50%)
                ├─ N3 Slider (0-50%)
                └─ N4 Slider (0-50%)
```

---

## 🔄 CICLO DE VIDA DO SISTEMA

```
1. INICIALIZAÇÃO
   └─ cads.init_db() cria schema

2. OPERAÇÃO NORMAL
   ├─ Usuário adiciona alunos, matérias, notas
   ├─ Dados armazenados em escola.db
   └─ gui_predicoes_improved mostra análise

3. TREINAMENTO (NOVO)
   ├─ MLAdvancedPage._generate_features()
   ├─ cads.gerar_features_ml() calcula 9 features
   ├─ ML_Dataset.csv é criado
   └─ MLAdvancedPage._train_models() treina RF_M*

4. PREDIÇÃO CONTÍNUA
   ├─ Cada aluno tem prognóstico
   ├─ gui_ml_integration analisa desempenho
   └─ PredictionPageImproved exibe no dashboard

5. INTERVENÇÃO PEDAGÓGICA (Potencial Futuro)
   ├─ Identificar alunos em risco
   ├─ Sugerir ações educacionais
   └─ Rastrear evolução
```

---

## 📈 PRÓXIMAS INTEGRAÇÕES POSSÍVEIS

```
┌─────────────────────────────────────────┐
│  Futuros Módulos Potenciais             │
├─────────────────────────────────────────┤
│                                         │
│  API REST (Flask/FastAPI)              │
│  └─ Integração mobile                  │
│                                         │
│  Dashboard Web (Streamlit/Dash)        │
│  └─ Visualizações interativas          │
│                                         │
│  GPU Support (CuPy/RAPIDS)             │
│  └─ Treino mais rápido                │
│                                         │
│  Database (PostgreSQL/MongoDB)         │
│  └─ Escalabilidade                    │
│                                         │
│  CI/CD (GitHub Actions)                │
│  └─ Testes automáticos                │
│                                         │
└─────────────────────────────────────────┘
```

---

**Versão:** 2.1  
**Data:** Abril 2026  
**Status:** ✅ Completo
