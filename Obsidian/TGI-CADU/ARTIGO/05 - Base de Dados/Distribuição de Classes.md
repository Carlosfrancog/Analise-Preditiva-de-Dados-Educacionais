---
tags: [artigo, dataset, distribuicao, classes, desbalanceamento]
aliases: [Distribuição de Classes e Desbalanceamento, Distribuição de Classes]
created: 2026-05-16
---

# Distribuição de Classes — Desbalanceamento no Dataset

[← Índice](<../INDEX - ARTIGO.md>) | [[Dataset — Estrutura e Geração Sintética]] | [[class weight balanced — Tratamento de Desbalanceamento]] | [[Acurácia F1 e Métricas Gerais]]

---

## 1. Classes do Problema

O EduPredict classifica cada par (aluno, matéria) em três classes baseadas na média ponderada:

```python
# cads.py — gerar_features_ml()
if media >= 6.0:   status_encoded = 2  # Aprovado
elif media >= 5.0: status_encoded = 1  # Recuperação
else:              status_encoded = 0  # Reprovado
```

---

## 2. Distribuição Estimada no Dataset Sintético

Com 200 alunos × 13 matérias = 2600 observações totais:

```
Aprovado    (media ≥ 6.0): ~65%  → ~1690 amostras
Recuperação (5.0 ≤ m < 6.0): ~20% → ~520 amostras
Reprovado   (media < 5.0):  ~15% → ~390 amostras
```

> **Nota:** distribuição estimada baseada na geração aleatória com `media_geral ≈ N(6.5, 1.5)` em `cads.gerar_notas_aleatorias()`. Os valores reais dependem dos parâmetros exatos da geração sintética.

---

## 3. Por Que Este Desbalanceamento Existe

### No dataset sintético:
A função `gerar_notas_aleatorias()` gera notas com distribuição normal centrada em ~6.5 — ligeiramente acima do limiar de aprovação. Isso resulta em mais aprovados que reprovados, espelhando a realidade de escolas com bom desempenho médio.

### Na realidade:
- Escolas com alto IDEB: distribuição pode ser 80/12/8 (mais aprovados)
- Escolas em vulnerabilidade: pode ser 50/25/25 (mais reprovações)
- O dataset sintético não captura essas variações

---

## 4. Impacto do Desbalanceamento

### Na Acurácia:
Um modelo "burro" que prediz sempre "Aprovado" teria ~65% de acurácia — próximo de M1 (83.8%). A **diferença real de M1** é apenas +18.8 pontos percentuais acima do baseline trivial.

```
Baseline (sempre Aprovado): ~65%
M1:  83.8%  → +18.8pp acima do baseline
M2:  92.5%  → +27.5pp acima do baseline
M3:  94.0%  → +29.0pp acima do baseline
```

### Na Recall de Recuperação:
Com 20% das amostras em Recuperação, o modelo tem incentivo a classificar erroneamente como Aprovado ou Reprovado — resultando em Recall=62.2% para Recuperação no M3 (ver [[Matriz de Confusão M3 — Análise Detalhada]]).

---

## 5. Estratégias de Balanceamento

| Estratégia | Técnica | Status no EduPredict |
|---|---|---|
| **class_weight='balanced'** | Aumenta peso das classes minoritárias no loss | Documentado, implementação a verificar |
| **SMOTE** | Gera amostras sintéticas de classes minoritárias | ❌ Não implementado |
| **Oversampling manual** | Duplica amostras de Recuperação e Reprovado | ❌ Não implementado |
| **Threshold calibration** | Ajusta limiar de decisão para favorecer recalls | ❌ Não implementado |

### Threshold Calibration — Mais Relevante para EWS:

```python
# Para um sistema de alerta precoce, preferir False Positives a False Negatives:
# Melhor alertar um aluno "seguro" do que ignorar um aluno "em risco"

proba = model.predict_proba(X)[0]  # [P(Reprovado), P(Recuperação), P(Aprovado)]

# Threshold padrão (0.5):
pred = np.argmax(proba)

# Threshold EWS (favorece detectar risco):
THRESHOLD_REPROVADO    = 0.30  # alertar se P(Reprovado) > 30%
THRESHOLD_RECUPERACAO  = 0.25  # alertar se P(Recuperação) > 25%
```

---

## 6. Desbalanceamento por Série

Séries mais avançadas tendem a ter mais reprovações — `serie_num_norm` captura parcialmente essa relação, mas a distribuição de classes **varia por série**:

```
6F (Aprovado=70%, Recup=20%, Reprov=10%)  ← mais aprovados
3M (Aprovado=55%, Recup=22%, Reprov=23%)  ← mais reprovações
```

O `StratifiedKFold` mantém a distribuição geral, mas não por série. Um split que separe treino/teste por série seria mais realista para avaliar generalização.

---

## Links

- [[Dataset — Estrutura e Geração Sintética]]
- [[class weight balanced — Tratamento de Desbalanceamento]]
- [[Acurácia F1 e Métricas Gerais]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
- [[Análise Crítica do TGI]]
