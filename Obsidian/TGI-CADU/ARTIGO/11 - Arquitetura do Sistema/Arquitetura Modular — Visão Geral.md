---
tags: [artigo, arquitetura, modulos, sistema, design]
created: 2026-05-16
---

# Arquitetura Modular — Visão Geral do Sistema EduNotas

[[INDEX - ARTIGO|← Índice]] | [[cads.py — Análise Profunda]] | [[gui ml integration py — Motor de Predição]] | [[gui predicoes improved py — Interface Preditiva]]

---

## 1. Diagrama de Módulos

```
┌─────────────────────────────────────────────────────────────────┐
│                        03-GUI/                                  │
│  gui_escola.py ← gui_predicoes_improved.py ← gui_ml_advanced.py│
│  (Main App)      (Predições)                  (de 02-ML/ ⚠)    │
└──────────────────────────┬──────────────────────────────────────┘
                           │ import
┌──────────────────────────▼──────────────────────────────────────┐
│                        02-ML/                                   │
│  gui_ml_integration.py  ←  train_simple.py                     │
│  (Motor ML em tempo real)    (Treinamento offline)              │
│           │                        │                            │
│           │ modelos pkl             │ serializa                  │
│           ▼                        ▼                            │
│       models/                  models/                          │
│  model_m1/m2/m3.pkl        features_m1/m2/m3.pkl               │
└──────────────────────────┬──────────────────────────────────────┘
                           │ import cads
┌──────────────────────────▼──────────────────────────────────────┐
│                        01-CORE/                                 │
│  cads.py (DB_PATH, get_conn, CRUD, gerar_features_ml)          │
│           │                                                     │
│           ▼                                                     │
│       escola.db (SQLite)                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Responsabilidades por Módulo

### `01-CORE/cads.py` — Foundation Layer
- Fonte de verdade do banco de dados (`DB_PATH`)
- Todas as operações CRUD (alunos, salas, notas, matérias)
- Geração das features ML (`gerar_features_ml()`)
- Cálculos matemáticos auxiliares (`_slope()`, `_variancia()`)
- Schema e migrações do banco

### `02-ML/train_simple.py` — Training Layer (offline)
- Execução única ou periódica, não em tempo real
- Detecção de leakage, preparação de dados
- Treinamento e serialização de M1/M2/M3
- **Não é importado pela GUI** — é um script independente

### `02-ML/gui_ml_integration.py` — Integration Layer
- Carregamento dos modelos PKL em tempo real
- `MLModelLoader` — seleção automática de M1/M2/M3
- `DisciplinePerformanceAnalyzer` — análise por aluno/matéria
- Interface entre GUI e ML
- **Ponto crítico:** usa `cads.get_conn()` diretamente, ignorando o parâmetro db_path

### `03-GUI/gui_escola.py` — Presentation Layer
- Classe principal `App` com navegação entre páginas
- Constantes de cor, fontes, dimensões
- `DashboardPage`, `AlunosPage`, `NotasPage`, `RelatorioPage`, `MLPage`
- Import de `gui_predicoes_improved.py` e `gui_ml_advanced` (de lugar errado)

### `03-GUI/gui_predicoes_improved.py` — Prediction UI
- Interface preditiva principal
- `DisciplineCardImproved` — card por matéria com prognóstico
- Usa `gui_ml_integration.DisciplinePerformanceAnalyzer`

---

## 3. Fluxo de Dados em Tempo Real (Predição)

```
Usuário seleciona aluno na interface
          ↓
gui_predicoes_improved.PredictionsPageImproved._load_student_analysis()
          ↓
gui_ml_integration.DisciplinePerformanceAnalyzer.analyze_student(aluno_id)
          ↓
cads.get_conn() → SELECT notas FROM escola.db WHERE aluno_id=?
          ↓
MLModelLoader.load_model() → model_m1/m2/m3.pkl (baseado em notas disponíveis)
          ↓
RandomForestClassifier.predict_proba(features)
          ↓
Resultado: {status_pred, risk_score, profile, prognosis por matéria}
          ↓
gui_predicoes_improved: renderiza DisciplineCardImproved para cada matéria
```

---

## 4. Fluxo de Dados Offline (Treinamento)

```
cads.gerar_features_ml() → INSERT INTO ml_features (escola.db)
          ↓
train_simple.py: load ml_features
          ↓
detect_leakage() → remove media_pond_norm, n4_norm
          ↓
Treinar M1/M2/M3 com StratifiedKFold
          ↓
pickle.dump(model, features) → 02-ML/models/
```

Os dois fluxos são desacoplados — treino é offline, predição é online. Isso é correto arquiteturalmente.

---

## 5. Problemas de Arquitetura Identificados

### Problema 1 — gui_ml_advanced.py no Lugar Errado
```
02-ML/gui_ml_advanced.py  ← arquivo de GUI no diretório ML
03-GUI/gui_escola.py: from gui_ml_advanced import MLAdvancedPage  ← import frágil
```

### Problema 2 — Acoplamento Rígido ao DB_PATH
`cads.py` hardcoda `DB_PATH` no módulo. Não há injeção de dependência — impossível usar um banco de dados diferente sem modificar o código.

### Problema 3 — Estado de Sessão na GUI
A GUI não gerencia estado entre navegações de forma explícita. Cada página recarrega dados do banco ao ser exibida — correto, mas ineficiente para navegações rápidas.

### Problema 4 — Sem Tratamento de Modelos Não Treinados
Se os arquivos `.pkl` não existem (treinamento não executado), a GUI falha com FileNotFoundError. Não há verificação graceful de existência dos modelos.

---

## 6. Qualidade Arquitetural Geral

**Positivo:**
- Separação clara de responsabilidades (dados / ML / GUI)
- Pipeline de treinamento desacoplado da GUI
- Schema de banco bem estruturado

**Negativo:**
- gui_ml_advanced.py em diretório errado
- Acoplamento rígido via DB_PATH global
- Sem interfaces/abstrações formais entre camadas
- Sem testes unitários por módulo

---

## Links

- [[cads.py — Análise Profunda]]
- [[gui ml integration py — Motor de Predição]]
- [[gui predicoes improved py — Interface Preditiva]]
- [[Pipeline Completo de Treinamento]]
- [[Débitos Técnicos Identificados]]
- [[Gaps — TGI vs EduNotas Atual]]
