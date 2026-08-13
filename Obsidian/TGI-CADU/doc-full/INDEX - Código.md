---
tags:
  - codigo
  - indice
  - tgi-codes
created: 2026-05-13
---

# Índice de Código

[[MOC - TGI-CODES|← Voltar ao índice]]

> [!NOTE] Como usar este índice
> Cada nota documenta um arquivo `.py` com suas funções, assinaturas, o que chamam e quem as chama. Use as setas `→` (chama) e `←` (é chamado por) para navegar entre dependências.

---

## Mapa de Dependências

```
gui_escola.py                     (entry point)
    ├── → cads.py                 (init_db, get_*)
    ├── → gui_predicoes_improved.py
    │       └── → gui_ml_integration.py
    │               ├── → cads.py (get_conn)
    │               └── → ml_models/RF_M*.pkl
    ├── → gui_ml_advanced.py
    │       ├── → cads.py (gerar_features_ml, PESOS_NOTAS)
    │       └── → ml_models/RF_M*.pkl
    └── → gui_predicoes.py (BasePage, SalasPage)
```

---

## Arquivos Principais

| Arquivo | Nota | Responsabilidade |
|---|---|---|
| `01-CORE/cads.py` | [[cads.py]] | BD, CRUD, features ML |
| `03-GUI/gui_escola.py` | [[gui_escola.py]] | App principal, navegação |
| `02-ML/gui_ml_advanced.py` | [[gui_ml_advanced.py]] | Dashboard ML, treino |
| `02-ML/gui_ml_integration.py` | [[gui_ml_integration.py]] | Análise de desempenho |
| `03-GUI/gui_predicoes_improved.py` | [[gui_predicoes_improved.py]] | Dashboard de predições |
| `02-ML/train_simple.py` | [[train_simple.py]] | Treino autônomo dos modelos |

---

## Índice por Classe/Função

### `cads.py`
- [[cads.py#get_conn|get_conn()]]
- [[cads.py#init_db|init_db()]]
- [[cads.py#_migrate_db|_migrate_db()]]
- [[cads.py#_slope|_slope(vals)]]
- [[cads.py#_std|_std(vals)]]
- [[cads.py#gerar_features_ml|gerar_features_ml(sala_id)]]
- [[cads.py#get_alunos|get_alunos(sala_id)]]
- [[cads.py#get_notas|get_notas(aluno_id)]]
- [[cads.py#salvar_nota|salvar_nota(...)]]

### `gui_escola.py`
- [[gui_escola.py#App|class App]]
- [[gui_escola.py#BasePage|class BasePage]]
- [[gui_escola.py#DashboardPage|class DashboardPage]]

### `gui_ml_advanced.py`
- [[gui_ml_advanced.py#MLAdvancedPage|class MLAdvancedPage]]
- [[gui_ml_advanced.py#_build|_build()]]
- [[gui_ml_advanced.py#_generate_features|_generate_features()]]
- [[gui_ml_advanced.py#_train_models|_train_models(model_names)]]
- [[gui_ml_advanced.py#_analyze_decision|_analyze_decision()]]

### `gui_ml_integration.py`
- [[gui_ml_integration.py#MLModelLoader|class MLModelLoader]]
- [[gui_ml_integration.py#DisciplinePerformanceAnalyzer|class DisciplinePerformanceAnalyzer]]
- [[gui_ml_integration.py#analyze_student|analyze_student(db_path, aluno_id, model_loader)]]

### `gui_predicoes_improved.py`
- [[gui_predicoes_improved.py#PredictionPageImproved|class PredictionPageImproved]]

---

## Fluxo de Chamadas — Treino de Modelos

```
MLAdvancedPage._train_all_models()         [[gui_ml_advanced.py#_train_all_models]]
    └── MLAdvancedPage._train_models()     [[gui_ml_advanced.py#_train_models]]
            ├── cads.exportar_ml_csv()     [[cads.py#exportar_ml_csv]]
            ├── pd.read_csv()
            ├── train_test_split()
            ├── RandomForestClassifier.fit()
            ├── pickle.dump()
            └── json.dump()
```

## Fluxo de Chamadas — Predição de Aluno

```
PredictionPageImproved._load_aluno()        [[gui_predicoes_improved.py#_load_aluno]]
    └── DisciplinePerformanceAnalyzer
            .analyze_student()              [[gui_ml_integration.py#analyze_student]]
                ├── cads.get_conn()         [[cads.py#get_conn]]
                ├── cads._slope()           [[cads.py#_slope]]
                ├── cads._std()             [[cads.py#_std]]
                └── MLModelLoader.predict() [[gui_ml_integration.py#MLModelLoader]]
```
