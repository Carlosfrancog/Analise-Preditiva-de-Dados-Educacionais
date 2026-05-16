---
tags: [artigo, implementacao, train_simple, treinamento, pipeline]
created: 2026-05-16
---

# train_simple.py — Pipeline Autônomo de Treinamento

[[INDEX - ARTIGO|← Índice]] | [← Código](../../07%20-%20Código/train_simple.py.md) | [[Pipeline Completo de Treinamento]] | [[cads.py — Análise Profunda]]

> Arquivo: `02-ML/train_simple.py` | Executado como: `python train_simple.py`

---

## 1. Papel no Sistema

Script standalone — não importado por nenhuma GUI. Executa o pipeline completo de treinamento offline e gera os arquivos `.pkl` que a interface usa.

**Quando executar:** sempre que os dados mudarem (novos alunos/notas) ou quando as features forem atualizadas em `cads.gerar_features_ml()`.

---

## 2. Pipeline de 4 Passos

```
Passo 1: cads.gerar_features_ml()
         → Calcula 9 features para cada (aluno × matéria)
         → Persiste em tabela ml_features no banco

Passo 2: cads.exportar_ml_csv()
         → Exporta ml_features para 02-ML/ml_dataset.csv

Passo 3: Carregar e preparar dados
         → pd.read_csv("ml_dataset.csv")
         → X = df[feature_cols], y = df['status_encoded']
         → train_test_split(stratify=y, test_size=0.2, random_state=42)

Passo 4: Treinar 3 modelos e serializar
         → RF_M1, RF_M2, RF_M3 com hiperparâmetros diferentes
         → Salvar .pkl + _metadata.json
```

---

## 3. Hiperparâmetros Reais dos Modelos

```python
modelos = {
    'RF_M1': RandomForestClassifier(
        n_estimators=100,
        max_depth=5,        # ← limitado, mais simples
        random_state=42
    ),
    'RF_M2': RandomForestClassifier(
        n_estimators=150,
        max_depth=10,       # ← intermediário
        random_state=42
    ),
    'RF_M3': RandomForestClassifier(
        n_estimators=200,
        # max_depth não definido = None (sem limite, árvores crescem até pureza)
        random_state=42
    ),
}
```

> Nota: `class_weight='balanced'` está nos docs do artigo mas NÃO aparece explicitamente no código lido. Verificar no arquivo real.

---

## 4. Features de Treinamento

```python
feature_cols = [
    'n1_norm', 'n2_norm', 'n3_norm', 'n4_norm',
    'slope_notas', 'variancia_notas', 'media_geral_aluno',
    'serie_num_norm', 'media_turma_norm'
]
# Nota: n4_norm e media_pond_norm excluídas pelo detect_leakage()
# Ver: Data Leakage — Conceito e Impacto
```

**Diferença importante vs análise no artigo:** `train_simple.py` treina os 3 modelos com as **mesmas 9 features**. A diferença de acurácia (M1=83,8%, M2=92,5%, M3=94,0%) vem dos hiperparâmetros e do subset de dados disponíveis, não de features diferentes por modelo.

O `gui_ml_advanced.py` (via GUI) usa features diferentes por modelo (M1 só n1_norm, M2 usa 4 features). `train_simple.py` usa as mesmas 9 para todos.

---

## 5. Output Gerado

```
02-ML/ml_models/
├── RF_M1.pkl              ← RandomForestClassifier serializado
├── RF_M1_metadata.json    ← acurácia, features, n_samples, date, confusion_matrix
├── RF_M2.pkl
├── RF_M2_metadata.json
├── RF_M3.pkl              ← modelo principal usado na interface
└── RF_M3_metadata.json    ← lido por MLModelLoader e MLAdvancedPage
```

### Estrutura do metadata.json

```json
{
    "accuracy": 0.94,
    "f1": 0.91,
    "n_features": 9,
    "features": ["n1_norm", "n2_norm", ...],
    "n_samples_train": 2080,
    "n_samples_test": 520,
    "date": "2026-05-14 10:30:00",
    "confusion_matrix": [[...], [...], [...]],
    "n_estimators": 200,
    "max_depth": null
}
```

O campo `features` no metadata é crítico — `MLModelLoader.predict()` usa essa lista para criar o DataFrame com nomes corretos, evitando `FeatureNamesWarning` do sklearn.

---

## 6. Divisão Treino/Teste

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 80% treino, 20% teste
    random_state=42,
    stratify=y           # mantém proporção de classes
)
```

**Sem `GroupKFold`:** o split divide pares (aluno, matéria) aleatoriamente. O mesmo aluno pode aparecer em treino E teste — ver [Débitos Técnicos DT-04](<../18 - Refatorações Necessárias/Débitos Técnicos Identificados.md>).

---

## 7. Métricas Calculadas

```python
accuracy = accuracy_score(y_test, y_pred)
f1       = f1_score(y_test, y_pred, average='weighted')
cm       = confusion_matrix(y_test, y_pred)
```

O f1 weighted dá mais peso às classes maiores. Para análise de EWS, macro-f1 seria mais honesto.

---

## 8. Diferença vs Treino via GUI

| Aspecto | `train_simple.py` | `gui_ml_advanced.py` |
|---|---|---|
| Ativação | Terminal: `python train_simple.py` | Botão "Treinar Modelos" na interface |
| Execução | Síncrona (bloqueia terminal) | Thread separada |
| Features M1 | Mesmas 9 features | Subset (n1_norm, serie_num_norm) |
| Features M2 | Mesmas 9 features | 4-5 features |
| Pesos | `PESOS_NOTAS` padrão | Ajustáveis via sliders na GUI |

---

## Links

- [[Pipeline Completo de Treinamento]]
- [[cads.py — Análise Profunda]]
- [[Débitos Técnicos Identificados]]
- [[Serialização dos Modelos]]
- [[Random Forest — Algoritmo e Justificativa]]
- [[Data Leakage — Conceito e Impacto]]
