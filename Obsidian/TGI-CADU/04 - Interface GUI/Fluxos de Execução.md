---
tags:
  - gui
  - fluxos
  - tgi-codes
created: 2026-05-13
---

# Fluxos de Execução

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## Fluxo 1 — Iniciar a Aplicação

```
python gui_escola.py
    ↓
App.__init__()
    ├── cads.init_db()               → cria schema se não existir
    ├── _build_ui()                  → monta sidebar e área principal
    ├── Instancia páginas
    └── Exibe DashboardPage
```

---

## Fluxo 2 — Gerar Features ML

```
Usuário clica "🔄 Gerar Features"
    ↓
MLAdvancedPage._generate_features()
    ├── Extrai pesos dos sliders (N1, N2, N3, N4)
    ├── Normaliza para somar 1.0
    ├── cads.PESOS_NOTAS = pesos_normalizados
    └── cads.gerar_features_ml()
            ├── SELECT notas, alunos, materias, salas
            ├── Para cada (aluno × matéria):
            │   ├── Calcular media_ponderada
            │   ├── n1_norm = n1/10, n2_norm = n2/10, ...
            │   ├── slope = _slope([n1, n2, n3])
            │   └── variancia = _std([n1, n2, n3]) / 10
            └── INSERT INTO ml_features
    ↓
Status: "✅ 15.613 features geradas"
```

---

## Fluxo 3 — Treinar Modelos

```
Usuário clica "🚀 Treinar Todos"
    ↓
MLAdvancedPage._train_models(["RF_M1", "RF_M2", "RF_M3"])
    ├── Status: "⏳ Carregando dados..."
    ├── pd.read_csv("ml_dataset.csv")
    ├── train_test_split(80% treino / 20% teste)
    └── Para cada modelo:
            ├── Status: "⏳ Treinando RF_M1..."
            ├── RandomForestClassifier().fit(X_train, y_train)
            ├── accuracy = accuracy_score(y_test, y_pred)
            ├── pickle.dump(model, "RF_M1.pkl")
            ├── json.dump(metadata, "RF_M1_metadata.json")
            └── Progresso: +33%
    ↓
_show_training_summary(results)
Status: "✅ Treinamento concluído!"
```

---

## Fluxo 4 — Analisar Decisão de Aluno

```
Usuário seleciona Aluno + Matéria + clica "Analisar"
    ↓
MLAdvancedPage._analyze_decision()
    ├── SELECT * FROM ml_features
    │   WHERE aluno_nome=? AND materia_nome=?
    └── Formata output:
            ├── INFORMAÇÕES: aluno, matéria, série
            ├── NOTAS: N1-N4 + normalizadas
            ├── FEATURES: slope + interpretação
            │               variância + interpretação
            ├── RESULTADO: status real
            └── INTERPRETAÇÃO: texto em linguagem natural
    ↓
Exibe no widget de texto
```

---

## Fluxo 5 — Ver Prognóstico de Aluno (Predições)

```
Usuário acessa página "Predições" e seleciona aluno
    ↓
PredictionPageImproved._load_student()
    ├── cads.get_notas(aluno_id)
    ├── Para cada matéria:
    │   └── DisciplinePerformanceAnalyzer.analyze_student()
    │           ├── Calcula features normalizadas
    │           ├── MLModelLoader.predict(features)
    │           │   └── rf_m3.predict([features])
    │           ├── Gera prognóstico: vai_melhorar / vai_piorar / estável
    │           └── Retorna status + cor + mensagem
    └── Exibe cards por matéria com cores
```

---

## Links Relacionados

- [[Componentes e Páginas]] — detalhes de cada classe GUI
- [[Arquitetura do Sistema]] — visão geral dos componentes
- [[cads.py — Core do Sistema]] — funções chamadas pelos fluxos
