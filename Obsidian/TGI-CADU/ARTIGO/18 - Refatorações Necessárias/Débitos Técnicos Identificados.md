---
tags: [artigo, refatoracao, debitos-tecnicos, codigo, melhorias]
created: 2026-05-16
---

# Débitos Técnicos Identificados — EduPredict

[[INDEX - ARTIGO|← Índice]] | [[slope notas — Tendência Temporal]] | [[Data Leakage — Conceito e Impacto]] | [[Análise Crítica do TGI]]

> [!WARNING] Débitos que afetam correção, manutenibilidade ou reprodutibilidade

---

## 1. DT-01 — Features Incorretas Enviadas ao Modelo na Predição em Tempo Real

**Arquivo:** `02-ML/gui_ml_integration.py`, linhas 283-295

**Problema crítico — 4 sub-problemas:**

```python
# O que o código faz na predição GUI (linhas 283-295):
slope     = (n2 - n1)                    # ← diferença simples entre norm. [0-1]
variancia = abs(n1 - n2)                 # ← absoluto, NÃO desvio padrão
media_norm = (n1_raw + n2_raw) / 2 / 10 # ← só 2 notas, não media_geral_aluno

features_pred = [n1, n2, 0, 0, slope, variancia, media_norm, 0.5, 0.5]
#                        ^^^^  ← N3 e N4 zerados MESMO quando disponíveis
#                                                              ^^^  ^^^
#                                               serie_num_norm=0.5  ← hardcoded!
#                                               pct_materias_ok=0.5 ← hardcoded!
```

**O que o modelo foi treinado a esperar (train_simple.py):**
```python
# 9 features reais calculadas por cads.gerar_features_ml():
[n1_norm, n2_norm, n3_norm,         # notas reais
 slope_notas,                        # cads._slope() = regressão linear
 variancia_notas,                    # cads._std() = desvio padrão normalizado
 media_geral_aluno,                  # média cross-matéria do aluno
 serie_num_norm,                     # série real (6F=0 a 3M=1)
 pct_materias_ok,                    # % matérias não-reprovadas
 media_turma_norm]                   # média da turma
```

**Impacto:** O RF_M3 recebe features completamente diferentes do que aprendeu. A predição exibida na interface pode estar sistematicamente errada para alunos de séries extremas (6F ou 3M) ou com muitas/poucas matérias em risco.

**Também existe `slope_pct`** (linha 371) usado separadamente para prognóstico (will_improve/will_decline):
```python
slope_pct = ((n2_raw - n1_raw) / n1_raw) * 100  # variação percentual N1→N2
```

**Correção proposta:**
```python
# gui_ml_integration.py — usar features corretas do banco
features_row = conn.execute(
    "SELECT * FROM ml_features WHERE aluno_id=? AND materia_id=?",
    (aluno_id, materia_id)
).fetchone()

if features_row:
    feature_names = model_loader.metadata.get("RF_M3", {}).get("features", [])
    features_pred = [features_row[f] or 0 for f in feature_names]
    pred, proba = model_loader.predict("RF_M3", features_pred)
```

**Severidade:** Alta — o modelo prediz com features que não correspondem ao treinamento.

---

## 2. DT-02 — `db_path` Ignorado em `analyze_student()`

**Arquivo:** `02-ML/gui_ml_integration.py`, linha ~169

**Problema:**
```python
def analyze_student(db_path, aluno_id, model_loader):
    conn = cads.get_conn()  # ← ignora db_path completamente!
```

O parâmetro `db_path` é aceito mas nunca usado. `cads.get_conn()` usa o caminho hardcoded em `cads.DB_PATH`. Isso impede testes com bancos alternativos.

**Correção:**
```python
def analyze_student(db_path, aluno_id, model_loader):
    conn = cads.get_conn(db_path) if db_path else cads.get_conn()
    # OU: sempre usar cads.get_conn() e documentar que db_path é ignorado
```

**Severidade:** Média — não causa erro, mas é uma interface enganosa.

---

## 3. DT-03 — Features Leaky Armazenadas sem Guards

**Arquivo:** `01-CORE/cads.py`, tabela `ml_features`

**Problema:** `media_pond_norm` e `n4_norm` são armazenadas na tabela `ml_features` para fins de visualização, mas um desenvolvedor futuro poderia inadvertidamente incluí-las no treinamento.

**Correção:**
```python
# cads.py — constantes de proteção
LEAKY_FEATURES = frozenset(['media_pond_norm', 'n4_norm'])
SAFE_TRAINING_FEATURES = [
    'n1_norm', 'n2_norm', 'n3_norm',
    'slope_notas', 'variancia_notas',
    'media_geral_aluno', 'pct_materias_ok',
    'media_turma_norm', 'serie_num_norm'
]

# train_simple.py — assertion explícita
X = df[SAFE_TRAINING_FEATURES]
assert not any(f in X.columns for f in LEAKY_FEATURES), "LEAKAGE DETECTED"
```

**Severidade:** Alta — risco de reintrodução de leakage em manutenção futura.

---

## 4. DT-04 — Validação Cruzada sem Agrupamento por Aluno

**Arquivo:** `02-ML/train_simple.py`

**Problema:**
```python
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(clf, X, y, cv=cv)
# Sem groups= → mesmo aluno pode aparecer em treino E teste
```

**Correção:**
```python
from sklearn.model_selection import GroupKFold
groups = df['aluno_id'].values
cv = GroupKFold(n_splits=5)
scores = cross_val_score(clf, X, y, cv=cv, groups=groups)
```

**Severidade:** Alta — infla artificialmente a acurácia reportada.

---

## 5. DT-05 — gui_ml_advanced.py em Diretório Errado

**Arquivos:** `02-ML/gui_ml_advanced.py`, `03-GUI/gui_escola.py`

**Problema:**
```python
# gui_escola.py
from gui_ml_advanced import MLAdvancedPage  # ← espera no mesmo diretório
# Mas gui_ml_advanced.py está em 02-ML/
```

Funciona apenas porque o `sys.path` inclui ambos os diretórios. Em deployment padrão ou ao refatorar, causará ImportError.

**Correção:** mover `gui_ml_advanced.py` para `03-GUI/` ou criar estrutura de pacotes Python com imports relativos.

**Severidade:** Baixa — não causa erro no ambiente atual, mas é um risco de manutenção.

---

## 6. DT-06 — Ausência de Hiperparâmetros Documentados

**Arquivo:** `02-ML/train_simple.py`

**Problema:** o código usa parâmetros padrão do RandomForestClassifier sem documentação ou justificativa. Impossível reproduzir exatamente os resultados do artigo.

**Correção:** documentar explicitamente:
```python
clf = RandomForestClassifier(
    n_estimators=100,          # padrão sklearn
    max_depth=None,            # sem limite de profundidade
    min_samples_split=2,       # padrão
    min_samples_leaf=1,        # padrão
    max_features='sqrt',       # padrão para classificação
    class_weight='balanced',   # DOCUMENTADO
    random_state=42,           # DOCUMENTADO
    # Nota: hiperparâmetros não foram otimizados via grid search
)
```

**Severidade:** Média — afeta reprodutibilidade científica.

---

## 7. DT-07 — Status de Notas Corrigido em GUI (jan 2026)

**Arquivo:** `03-GUI/gui_escola.py`

**Problema (resolvido):** `NotasPage._load_notas()` e `RelatorioPage._load()` classificavam médias como Recuperação quando eram Reprovado (if media < 6 → Recuperação, ignorando o limiar de 5,0).

**Correção aplicada:**
```python
if media >= 6:
    status, tag = "Aprovado", "aprov"
elif media >= 5:
    status, tag = "Recuperação", "recup"
else:
    status, tag = "Reprovado", "reprov"
```

**Status:** ✅ Corrigido em commit `aba29ab`.

---

## 8. Prioridade de Correção

| ID | Débito | Prioridade | Complexidade |
|---|---|---|---|
| DT-01 | Inconsistência slope | 🔴 Alta | 🟡 Média |
| DT-03 | Guards de leakage | 🔴 Alta | ✅ Baixa |
| DT-04 | GroupKFold | 🔴 Alta | ✅ Baixa |
| DT-02 | db_path ignorado | 🟡 Média | ✅ Baixa |
| DT-06 | Hiperparâmetros | 🟡 Média | ✅ Baixa |
| DT-05 | Diretório errado | 🟢 Baixa | 🟡 Média |
| DT-07 | Status GUI | ✅ Resolvido | — |

---

## Links

- [[slope notas — Tendência Temporal]]
- [[Data Leakage — Conceito e Impacto]]
- [[Detecção Automática por Correlação de Pearson]]
- [[Análise Crítica do TGI]]
- [[Pipeline Completo de Treinamento]]
- [[gui ml integration py — Motor de Predição]]
