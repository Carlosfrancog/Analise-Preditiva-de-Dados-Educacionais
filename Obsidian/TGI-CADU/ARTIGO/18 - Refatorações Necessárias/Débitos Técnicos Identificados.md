---
tags: [artigo, refatoracao, debitos-tecnicos, codigo, melhorias]
created: 2026-05-16
---

# Débitos Técnicos Identificados — EduPredict

[[INDEX - ARTIGO|← Índice]] | [[slope notas — Tendência Temporal]] | [[Data Leakage — Conceito e Impacto]] | [[Análise Crítica do TGI]]

> [!WARNING] Débitos que afetam correção, manutenibilidade ou reprodutibilidade

---

## 1. DT-01 — Inconsistência de slope entre cads.py e gui_ml_integration.py

**Arquivo:** `02-ML/gui_ml_integration.py` vs `01-CORE/cads.py`

**Problema:**
```python
# cads.py — usa regressão linear sobre todas as notas disponíveis
slope_notas = _slope([n/10 for n in notas_disponíveis])

# gui_ml_integration.py — usa variação percentual N2→N1
slope_pct = ((n2_raw - n1_raw) / n1_raw) * 100
```

São medidas fundamentalmente diferentes. O modelo ML usa a versão de `cads.py` para treinamento, mas a interface usa a versão percentual para exibir prognósticos. Um aluno pode receber o prognóstico "vai melhorar" na interface mas ter slope negativo nos dados usados para treinamento.

**Correção proposta:**
```python
# gui_ml_integration.py — substituir slope_pct por _slope
from cads import _slope
notas_disponiveis = [n for n in [n1_raw, n2_raw, n3_raw, n4_raw] if n > 0]
slope_real = _slope([n/10 for n in notas_disponiveis])

if slope_real > 0.15:
    disc_info["prognosis"] = "will_improve"
elif slope_real < -0.15:
    disc_info["prognosis"] = "will_decline"
else:
    disc_info["prognosis"] = "stable"
```

**Severidade:** Alta — afeta a consistência entre o que o modelo vê e o que o usuário vê.

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
