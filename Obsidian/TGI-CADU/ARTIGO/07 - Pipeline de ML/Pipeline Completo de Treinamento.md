---
tags: [artigo, pipeline, treinamento, ml, train_simple]
created: 2026-05-16
---

# Pipeline Completo de Treinamento

[[INDEX - ARTIGO|← Índice]] | [[M1 — Modelo Precoce]] | [[M2 — Modelo Intermediário]] | [[M3 — Modelo de Produção (Após N3)]] | [[Serialização dos Modelos]]

---

## 1. Visão Geral do Fluxo

```
[escola.db]
    ↓  cads.gerar_features_ml()
[tabela ml_features — 15.613 registros com todas as features]
    ↓  train_simple.py
[detect_leakage() → remove media_pond_norm, n4_norm]
    ↓
[df_clean — 9 features legítimas + status_encoded]
    ↓  split por disponibilidade de notas
    ┌─────────────────────────────────────────────────┐
    │  M1: df[n1 notna]   M2: df[n2 notna]   M3: df[n3 notna]  │
    └─────────────────────────────────────────────────┘
    ↓  para cada modelo:
[StratifiedKFold(n=5) cross_val_score]
    ↓  fit no conjunto completo
[RandomForestClassifier.fit(X, y)]
    ↓  pickle.dump
[model_m1.pkl / model_m2.pkl / model_m3.pkl]
[features_m1.pkl / features_m2.pkl / features_m3.pkl]
```

---

## 2. Etapa 1 — Geração de Features (cads.py)

`gerar_features_ml()` executa uma query SQL complexa que:
1. Busca todos os alunos e matérias
2. Agrega notas N1-N4 por (aluno, matéria)
3. Calcula features derivadas em Python (slope, variância)
4. Calcula features contextuais com subqueries (media_geral_aluno, pct_materias_ok, media_turma_norm)
5. Insere/atualiza na tabela `ml_features`

A tabela `ml_features` serve duplo propósito: fonte para o treino **e** cache para a interface de predições.

---

## 3. Etapa 2 — Detecção de Leakage (train_simple.py)

```python
# Antes de qualquer modelo
leaky = detect_leakage(df, 'status_encoded', threshold=0.9)
# Resultado: ['media_pond_norm', 'n4_norm']
df_clean = df.drop(columns=leaky)
```

Ver [[Detecção Automática por Correlação de Pearson]].

---

## 4. Etapa 3 — Divisão por Ponto Temporal

Cada modelo usa subconjuntos diferentes do dataframe:

```python
# M1 — todos os registros com N1 disponível
df_m1 = df_clean[df_clean['n1_norm'].notna()]
X_m1 = df_m1[['n1_norm', 'serie_num_norm']]

# M2 — todos os registros com N2 disponível
df_m2 = df_clean[df_clean['n2_norm'].notna()]
X_m2 = df_m2[['n1_norm', 'n2_norm', 'slope_notas', 'variancia_notas', 'serie_num_norm']]

# M3 — todos os registros com N3 disponível
df_m3 = df_clean[df_clean['n3_norm'].notna()]
X_m3 = df_m3[FEATURES_M3_ALL_9]
```

**Risco:** os conjuntos M1 ⊆ M2 ⊆ M3 (M3 é subconjunto de M2 que é subconjunto de M1). Registros com N1 mas sem N2 são usados apenas em M1. Isso cria heterogeneidade nos conjuntos de treinamento.

---

## 5. Etapa 4 — Validação Cruzada

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
clf = RandomForestClassifier(class_weight='balanced', random_state=42)

# Para cada modelo
scores = cross_val_score(clf, X, y, cv=cv, scoring='accuracy')
print(f"Acurácia: {scores.mean():.3f} ± {scores.std():.3f}")
```

**Limitação crítica:** StratifiedKFold não agrupa por aluno. O mesmo aluno pode aparecer em múltiplos folds, violando a independência das observações. Ver [[Análise Crítica do TGI#2.5 Validação Cruzada com Vazamento Intra-Aluno]].

**Solução mais correta:**
```python
from sklearn.model_selection import GroupKFold
gkf = GroupKFold(n_splits=5)
scores = cross_val_score(clf, X, y, cv=gkf, groups=df['aluno_id'])
```

---

## 6. Etapa 5 — Treinamento Final e Serialização

```python
# Treinar no conjunto completo após validação
clf.fit(X, y)

# Serializar modelo e lista de features
import pickle
pickle.dump(clf, open(f'models/model_{version}.pkl', 'wb'))
pickle.dump(list(X.columns), open(f'models/features_{version}.pkl', 'wb'))
```

A lista de features é serializada junto com o modelo para garantir que a interface use exatamente as mesmas features na mesma ordem durante a predição. Isso evita erros silenciosos de feature mismatch.

---

## 7. Estrutura de Arquivos Pós-Treinamento

```
02-ML/
  models/
    model_m1.pkl         ← RandomForestClassifier treinado com 2 features
    model_m2.pkl         ← RandomForestClassifier treinado com 4-5 features
    model_m3.pkl         ← RandomForestClassifier treinado com 9 features
    features_m1.pkl      ← ['n1_norm', 'serie_num_norm']
    features_m2.pkl      ← ['n1_norm', 'n2_norm', 'slope_notas', 'variancia_notas', ...]
    features_m3.pkl      ← [todas as 9 features]
  train_simple.py        ← Script de treinamento
  gui_ml_integration.py  ← Carrega modelos para predição em tempo real
```

---

## 8. Reprodutibilidade

O pipeline usa `random_state=42` para reproducibility:
- `StratifiedKFold(shuffle=True, random_state=42)`
- `RandomForestClassifier(random_state=42)`

**O que falta para reprodutibilidade completa:**
- Versões das dependências (sklearn, numpy, pandas) não documentadas
- Hiperparâmetros além de `class_weight` e `random_state`
- Seed do gerador de dados sintéticos
- Timestamp da geração dos dados

---

## 9. Tempo de Treinamento Estimado

Com 15.613 registros e RF com parâmetros padrão (~100 estimadores):
- M1: < 5 segundos
- M2: < 10 segundos
- M3: < 30 segundos

O pipeline pode ser re-executado facilmente — não é um bottleneck. Isso é importante porque os modelos deveriam ser re-treinados quando novos dados são adicionados.

---

## 10. Problema — Re-treinamento Não Automatizado

O pipeline atual exige execução manual de `train_simple.py`. O sistema não possui:
- Gatilho automático de re-treinamento ao adicionar alunos/notas
- Versionamento de modelos (qual modelo foi usado para qual predição)
- Monitoramento de drift de performance

Para uso em produção real, isso seria crítico.

---

## Links

- [[M1 — Modelo Precoce]]
- [[M2 — Modelo Intermediário]]
- [[M3 — Modelo de Produção (Após N3)]]
- [[Detecção Automática por Correlação de Pearson]]
- [[Serialização dos Modelos]]
- [[Divisão Treino-Teste e Cross-Validation]]
- [[class weight balanced — Tratamento de Desbalanceamento]]
- [[cads.py — Análise Profunda]]
- [[Análise Crítica do TGI]]
