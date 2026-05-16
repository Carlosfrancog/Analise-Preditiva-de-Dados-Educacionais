---
tags: [artigo, modelos, M3, random-forest, producao]
created: 2026-05-16
---

# M3 — Modelo de Produção (Após N3)

[[INDEX - ARTIGO|← Índice]] | [[M1 — Modelo Precoce]] | [[M2 — Modelo Intermediário]] | [[Comparação M1 M2 M3]]

> [!SUCCESS] 94,0% de acurácia — modelo com maior precisão, menor antecedência

---

## 1. Especificação Técnica

| Parâmetro | Valor |
|---|---|
| **Ponto temporal** | Após lançamento de N3 (3º bimestre) |
| **Features de entrada** | 9 (todas disponíveis) |
| **Algoritmo** | RandomForestClassifier |
| **Acurácia (CV 5-fold)** | **94,0%** |
| **Macro-F1** | A calcular (não explicitado no artigo) |
| **Arquivo de modelo** | `02-ML/models/model_m3.pkl` |
| **Arquivo de features** | `02-ML/models/features_m3.pkl` |

---

## 2. Features e Importâncias

| Feature | Importância | Rank |
|---|---|---|
| `n2_norm` | 32,3% | 1º |
| `pct_materias_ok` | 21,5% | 2º |
| `slope_notas` | 12,3% | 3º |
| `n3_norm` | 8,7% | 4º |
| `media_geral_aluno` | 7,8% | 5º |
| `variancia_notas` | 5,2% | 6º |
| `media_turma_norm` | 4,8% | 7º |
| `n1_norm` | 4,1% | 8º |
| `serie_num_norm` | 3,3% | 9º |

**Achado surpreendente:** `n3_norm` (nota do 3º bimestre — a mais recente no momento de predição M3) tem apenas 8,7% de importância, enquanto `n2_norm` domina com 32,3%. Hipótese: N2 é mais estável e consistente; N3 pode ter alta variância (alunos que "estudam para N3" após resultado ruim em N2).

---

## 3. Desempenho por Classe

| Classe | Precisão | Recall | F1 | Suporte |
|---|---|---|---|---|
| **Aprovado** (2) | Alta | **91,7%** | Alto | Maioria |
| **Recuperação** (1) | Moderada | **62,2%** | Moderado | Minoria |
| **Reprovado** (0) | Moderada | **76,3%** | Moderado | Minoria |

**Ponto crítico:** o modelo identifica corretamente apenas 62,2% dos alunos em Recuperação. Isso é o recall — de 100 alunos em Recuperação real, 38 são classificados como Aprovados ou Reprovados. Para um sistema de Early Warning, esse é o erro mais custoso. Ver [[Matriz de Confusão M3 — Análise Detalhada]].

---

## 4. Código de Treinamento

```python
# 02-ML/train_simple.py — treinamento M3 (reconstruído do artigo)
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
import pickle

FEATURES_M3 = [
    'n1_norm', 'n2_norm', 'n3_norm',
    'slope_notas', 'variancia_notas',
    'media_geral_aluno', 'pct_materias_ok',
    'media_turma_norm', 'serie_num_norm'
]

# Carregar dados (sem features leaky)
df = load_ml_features()
df_m3 = df[df['n3_norm'].notna()]  # Somente registros com N3

X = df_m3[FEATURES_M3]
y = df_m3['status_encoded']

# Modelo com balanceamento de classes
clf_m3 = RandomForestClassifier(
    class_weight='balanced',
    random_state=42,
    # Hiperparâmetros não documentados no artigo
)

# Validação cruzada estratificada
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(clf_m3, X, y, cv=cv, scoring='accuracy')
print(f"M3: {scores.mean():.3f} ± {scores.std():.3f}")  # → 0.940 ± ?

# Treinar no conjunto completo e serializar
clf_m3.fit(X, y)
pickle.dump(clf_m3, open('models/model_m3.pkl', 'wb'))
pickle.dump(FEATURES_M3, open('models/features_m3.pkl', 'wb'))
```

Ver [[Pipeline Completo de Treinamento]] e [[Serialização dos Modelos]].

---

## 5. Como M3 É Usado na Interface

```python
# 02-ML/gui_ml_integration.py — predição com M3
def predict_m3(aluno_id, materia_id, conn):
    features = extract_features_m3(aluno_id, materia_id, conn)
    model = pickle.load(open('models/model_m3.pkl', 'rb'))
    
    X = pd.DataFrame([features])
    prediction = model.predict(X)[0]       # 0=Reprovado, 1=Recup, 2=Aprovado
    probas = model.predict_proba(X)[0]     # [p_reprov, p_recup, p_aprov]
    
    return prediction, probas
```

A seleção automática do modelo correto (M1/M2/M3) baseada na disponibilidade de notas está em `MLModelLoader.load_model()`. Ver [[gui ml integration py — Motor de Predição]].

---

## 6. Posição no Trade-off Antecedência × Acurácia

```
M1 (após N1) ← maior antecedência, menor acurácia (83,8%)
M2 (após N2) ← equilíbrio (+8,7pp vs M1, -1,5pp vs M3)
M3 (após N3) ← menor antecedência, maior acurácia (94,0%)
```

Para intervenção pedagógica, o trade-off ideal depende da janela de ação:
- Se a escola pode intervir com 6 meses de antecedência → M1 é suficiente
- Se intervir com 3 meses basta → M2 oferece melhor custo-benefício
- Se o semestre acabou e só falta N4 → M3 é o mais preciso para conselho de classe

**O sistema EduPredict usa M3 por padrão** para a interface de predições, sem justificativa explícita no artigo.

---

## 7. Limitações Específicas do M3

1. **Timing de intervenção:** com N3 já lançada, restam apenas ~2 meses antes do resultado final. A janela de intervenção é curta.

2. **Recuperação não identificada:** 38% dos alunos em Recuperação são misclassificados. Em uma turma de 30 alunos, isso é ~5-6 alunos que o sistema "deixa passar".

3. **Dados de N4 ausentes:** o modelo não usa N4 (leakage), mas N4 existe na realidade — um professor poderia informalmente saber que o aluno está mal em N4, mas o modelo não captura isso.

4. **Dependência de N2 dominante:** se N2 fosse uma prova atípica (muito fácil, muito difícil), o modelo M3 seria comprometido por uma nota que já tem 2 bimestres de atraso.

---

## 8. Hiperparâmetros Não Documentados

O artigo menciona `class_weight='balanced'` mas não especifica:
- `n_estimators` (número de árvores)
- `max_depth` (profundidade máxima)
- `min_samples_split`
- `min_samples_leaf`
- `max_features`

Isso impede reprodutibilidade completa. Ver [[Débitos Técnicos Identificados]].

---

## Links

- [[M1 — Modelo Precoce]]
- [[M2 — Modelo Intermediário]]
- [[Comparação M1 M2 M3]]
- [[Visão Geral das 9 Features]]
- [[Feature Importance Detalhada — M3]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
- [[class weight balanced — Tratamento de Desbalanceamento]]
- [[Pipeline Completo de Treinamento]]
- [[gui ml integration py — Motor de Predição]]
- [[Serialização dos Modelos]]
