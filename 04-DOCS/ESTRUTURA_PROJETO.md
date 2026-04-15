# 📁 ESTRUTURA DE ORGANIZAÇÃO DO PROJETO EDUCACIONAL

**Versão:** 2.1  
**Última Atualização:** Abril 2026  
**Objetivo:** Organizar módulos por categorias funcionais

---

## 📋 ESTRUTURA PROPOSTA

```
TGI-CODES/
│
├─ 📁 01-CORE/                          [Core do Sistema]
│  ├── cads.py                          - Banco de dados, CRUD de entidades
│  ├── requirements.txt                 - Dependências do projeto
│  └── escola.db                        - Banco de dados SQLite
│
├─ 📁 02-ML/                            [Machine Learning]
│  ├── gui_ml_advanced.py               - Dashboard de ML modernizado
│  ├── gui_ml_integration.py            - Integração ML com análise de desempenho
│  ├── train_simple.py                  - Treinamento de modelos
│  ├── train_models.py                  - Treinamento alternativo
│  ├── ml_models/                       - Modelos treinados
│  │  ├── RF_M1.pkl                     - Random Forest 100 árvores
│  │  ├── RF_M1_metadata.json          
│  │  ├── RF_M2.pkl                     - Random Forest 150 árvores
│  │  ├── RF_M2_metadata.json
│  │  ├── RF_M3.pkl                     - Random Forest 200 árvores (PRODUÇÃO)
│  │  └── RF_M3_metadata.json
│  ├── ml_dataset.csv                   - Dataset para treinamento
│  ├── ml_pipeline.py                   - Pipeline de dados
│  ├── ml_models.py                     - Funções de modelo
│  └── ml_gui_integration.py            - Integração GUI-ML
│
├─ 📁 03-GUI/                           [Interface Gráfica]
│  ├── gui_escola.py                    - MAIN - App principal, navegação
│  ├── gui_predicoes_improved.py        - Dashboard de Predições (melhorado)
│  ├── gui_predicoes.py                 - PredictionPage, SalasPage (legacy)
│  └── gui_ml_advanced.py               - Dashboard ML avançado (treino)
│
├─ 📁 04-DOCS/                          [Documentação]
│  ├── DOCUMENTACAO_CALCULOS.md         - Explicação de TODOS os cálculos
│  ├── ESTRUTURA_PROJETO.md             - Este arquivo
│  ├── GUIA_COMPLETO.md                 - Guia de uso completo
│  ├── GUIA_PREDICOES.md                - Guia de predições
│  ├── INICIO_RAPIDO.md                 - Quick start
│  ├── README.md                        - Visão geral do projeto
│  ├── RESUMO_EXECUTIVO.md              - Resumo executivo
│  ├── SISTEMA_COMPLETO.md              - Documentação completa
│  └── ML_README.md                     - Documentação de ML
│
├─ 📁 05-TESTS/                         [Testes e Debug]
│  ├── test_*.py                        - Testes diversos
│  ├── debug_*.py                       - Scripts de debug
│  ├── test_analise.py
│  ├── test_fix.py
│  ├── test_media.py
│  ├── test_ml_gui.py
│  ├── test_n*.py
│  ├── test_prognosis.py
│  ├── test_quick.py
│  ├── test_sala.py
│  ├── test_user_case.py
│  └── run_*.py                         - Scripts de execução
│
├─ 📁 06-OUTPUT/                        [Arquivos Gerados]
│  ├── ml_dataset.csv                   - Dataset exportado
│  ├── notas_exportadas.xlsx            - Notas em Excel
│  ├── ml_dataset.csv                   - Features
│  ├── 01_debug_results.json            - Resultados debug
│  └── 02_training_summary.json         - Resumo treinamento
│
├─ 📁 07-BUILD/                         [Para Build/Deploy]
│  ├── build/                           - Compilação local
│  ├── dist/                            - Distribuição
│  ├── EduNotas.spec                    - Spec do PyInstaller
│  ├── first_init.bat                   - Inicialização Windows
│  └── __pycache__/                     - Cache Python
│
├─ 📁 08-GIT/                           [Controle de Versão]
│  ├── .git/                            - Repositório Git
│  └── .gitignore                       - Arquivos ignorados
│
└─ 📄 ARQUIVOS RAIZ
   ├── gui_escola.py                    - Janela principal
   ├── cads.py                          - Backend
   └── train_simple.py                  - Treinar modelos
```

---

## 🎯 CATEGORIAS DE MÓDULOS

### **01 - CORE (Sistema Base)**

Responsabilidade: Banco de dados, CRUD, operações básicas

| Arquivo | Função Principal | Responsável por |
|---------|-----------------|-----------------|
| `cads.py` | BD + Operações | Alunos, matérias, notas, salas, features ML |
| `requirements.txt` | Dependências | pandas, sklearn, numpy, tkinter |

---

### **02 - ML (Machine Learning)**

Responsabilidade: Treinamento, predição, análise de modelos

| Arquivo | Função Principal | Responsável por |
|---------|-----------------|-----------------|
| `gui_ml_advanced.py` | Dashboard ML | Interface de treino, visualização de decisões |
| `gui_ml_integration.py` | Integração ML-GUI | Análise de desempenho, prognósticos |
| `train_simple.py` | Treinamento automático | Treina RF_M1, RF_M2, RF_M3 |
| `train_models.py` | Treinamento alternativo | Versão alternativa de treino |
| `ml_pipeline.py` | Pipeline de dados | Preparação e transformação de dados |
| `ml_models.py` | Utilitários de modelo | Funções auxiliares |
| `ml_gui_integration.py` | Integração baseada em GUI | Análise de decisões visuais |

---

### **03 - GUI (Interface Gráfica)**

Responsabilidade: Telas, layouts, interação com usuário

| Arquivo | Função Principal | Responsável por |
|---------|-----------------|-----------------|
| `gui_escola.py` | APP PRINCIPAL | Navegação, sidebar, layout geral |
| `gui_predicoes_improved.py` | Dashboard de Predições | Análise por aluno, cards, filtros |
| `gui_predicoes.py` | Componentes antigos | SalasPage, PredictionPage base |
| `gui_ml_advanced.py` | Dashboard ML Avançado | Treino, análise de decisões |

**Padrão de Páginas:** Todas herdam de `BasePage` definida em `gui_predicoes.py`

---

### **04 - DOCS (Documentação)**

Responsabilidade: Guias, explicações, referências

| Arquivo | Conteúdo |
|---------|----------|
| `DOCUMENTACAO_CALCULOS.md` | **👈 LEIA PRIMEIRO** - Explica todos os 9 features, fórmulas, pesos |
| `GUIA_COMPLETO.md` | Como usar cada parte do sistema |
| `GUIA_PREDICOES.md` | Detalhes das predições |
| `README.md` | Visão geral inicial |
| `INICIO_RAPIDO.md` | Primeiros passos |
| `ESTRUTURA_PROJETO.md` | Este arquivo |

---

### **05 - TESTS (Testes e Debug)**

Responsabilidade: Validação, troubleshooting, prototipagem

| Arquivo | Propósito |
|---------|----------|
| `test_*.py` | Testes unitários de funcionalidades |
| `debug_*.py` | Scripts para debug de específicos problemas |
| `run_*.py` | Scripts para executar tipicamente |

---

### **06 - OUTPUT (Gerados)**

Responsabilidade: Arquivos gerados pela aplicação (não commitar)

| Arquivo | Gerado por | Propósito |
|---------|-----------|----------|
| `ml_dataset.csv` | `cads.exportar_ml_csv()` | Dataset para treino |
| `notas_exportadas.xlsx` | Exportar Excel | Backup de notas |
| `training_summary.json` | `train_simple.py` | Resumo de último treino |

---

### **07 - BUILD (Compilação)**

Responsabilidade: Distribuição executável, build

| Arquivo | Uso |
|---------|-----|
| `EduNotas.spec` | Compilar com PyInstaller |
| `first_init.bat` | Iniciar no Windows |

---

## 🔄 FLUXO DE DADOS

```
┌──────────────────────┐
│   gui_escola.py      │ ← APP PRINCIPAL
│ (Navegação + Layout) │
└───────────┬──────────┘
            │
    ┌───────┴───────┬─────────────┬──────────────┐
    ↓               ↓             ↓              ↓
┌────────┐   ┌──────────┐  ┌────────────┐  ┌─────────────┐
│gui_    │   │gui_      │  │gui_        │  │gui_ml_     │
│predi   │   │predi     │  │predicoes   │  │advanced.py │
│coes_   │   │coes.py   │  │(legacy)    │  │(NEW)       │
│improv  │   │          │  │            │  │            │
│ed.py   │   │          │  │            │  │            │
└────────┘   └──────────┘  └────────────┘  └─────────────┘
    │            │              │               │
    └────────────┴──────────────┴───────────────┘
            │
    ┌───────┴──────────────────┐
    ↓                          ↓
┌─────────────────┐  ┌──────────────────────┐
│ gui_ml_         │  │cads.py               │
│integration.py   │  │(BD + Operações)      │
│(Análise ML)     │  └──────────────────────┘
└─────────────────┘           │
    │                         ↓
    └────────────┬────────┬────────────────┐
                 ↓        ↓                ↓
            ┌────────┐ ┌──────┐  ┌────────────────┐
            │train_  │ │ml_   │  │gui_ml_
            │simple  │ │models│  │integration.py  │
            └────────┘ └──────┘  └────────────────┘
                 │
                 ↓
            ┌──────────────┐
            │ ml_models/   │
            │ RF_M*.pkl    │
            └──────────────┘
```

---

## 📊 DEPENDÊNCIAS ENTRE MÓDULOS

```
gui_escola.py (MAIN)
  ├── cads.py
  ├── gui_predicoes_improved.py
  ├── gui_ml_advanced.py ← NEW
  │   ├── cads.py
  │   ├── pandas
  │   ├── sklearn
  │   └── sqlite3
  └── gui_predicoes.py (legacy)
      ├── gui_ml_integration.py
      │   ├── cads.py
      │   ├── sqlite3
      │   ├── numpy
      │   └── pickle
      └── cads.py

train_simple.py
  ├── cads.py
  ├── pandas
  ├── sklearn
  └── pickle
```

---

## 🛠️ COMO ADICIONAR NOVOS MÓDULOS

### Passo 1: Escolher Categoria
- **01-CORE**: Operações de BD ou lógica fundamental
- **02-ML**: Algoritmos, treino, predição
- **03-GUI**: Telas e interação
- **04-DOCS**: Documentação adicional
- **05-TESTS**: Testes

### Passo 2: Nomear Arquivo
```
01-CORE/analise_financeira.py  ← para operações de custo
02-ML/model_xgboost.py         ← para novo modelo
03-GUI/gui_relatorio.py        ← para nova página
```

### Passo 3: Importar em GUI
Se criar nova página, adicionar em `gui_escola.py`:

```python
from seu_modulo import SuaPage

# Na lista de pages:
for cls, key in [
    # ...
    (SuaPage, "sua_chave"),
    # ...
]:
```

### Passo 4: Documentar
Criar seção em `DOCUMENTACAO_CALCULOS.md` ou `GUIA_COMPLETO.md`

---

## ✅ CHECKLIST DE ORGANIZAÇÃO

- [x] **Core Organizado**: cads.py centralizado, BD limpo
- [x] **ML Centralizado**: Todos os modelos em ml_models/, treino em train_simple.py
- [x] **GUI Modular**: Cada página em seu arquivo, BasePage como padrão
- [x] **Docs Completa**: DOCUMENTACAO_CALCULOS.md explica tudo
- [x] **Build Pronto**: .spec e .bat para execução
- [ ] **(Futuro) Tests Extensos**: Adicionar mais testes unitários
- [ ] **(Futuro) CI/CD**: GitHub Actions para testes automáticos
- [ ] **(Futuro) API REST**: Se integração externa for necessária

---

## 📌 COMANDOS ÚTEIS

### Treinar Modelos
```bash
python train_simple.py
```

### Iniciar Aplicação
```bash
python gui_escola.py
```

### Gerar Dataset
```bash
python -c "import cads; cads.gerar_features_ml()"
```

### Exportar para CSV
```bash
python -c "import cads; cads.exportar_ml_csv()"
```

### Rodar Testes
```bash
python test_analise.py
python test_media.py
python test_prognosis.py
```

---

## 🎯 OBJETIVOS FUTUROS

1. **Modularização Ainda Maior**
   - Separar lógica de UI de lógica de negócio
   - Padrão MVC ou MVT

2. **Testes Unitários**
   - Coverage de pelo menos 80%
   - Testes de integração BD

3. **API REST**
   - Flask ou FastAPI
   - Integração com aplicativo mobile

4. **Banco de Dados Maior**
   - Migração para PostgreSQL se necessário
   - Indices otimizados

5. **Dashboard Web**
   - Streamlit ou Dash
   - Visualizações interativas em tempo real

---

## 📋 MANUTENÇÃO

**A revisar a cada atualização:**

1. Adicione linha na tabela de módulos
2. Atualize diagrama de fluxo se necessário
3. Documente em GUIA_COMPLETO.md
4. Comente o código
5. Add imports ao `__init__.py` (se criar)

---

**Elaborado por:** Sistema de IA  
**Para:** Gerenciamento de Projeto Educacional  
**Versão:** 2.1 - Incluindo GUI_ML_ADVANCED.py
