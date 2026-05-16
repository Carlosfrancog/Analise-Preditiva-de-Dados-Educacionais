---
tags: [artigo, pipeline, treino-teste, cross-validation, validacao]
aliases: [Divisão Treino-Teste e Validação Cruzada, Validação Cruzada 5-fold — Robustez, Divisão Treino-Teste e Cross-Validation]
created: 2026-05-16
---

# Divisão Treino-Teste e Cross-Validation

[← Índice](<../INDEX - ARTIGO.md>) | [[Pipeline Completo de Treinamento]] | [[Acurácia F1 e Métricas Gerais]] | [[Débitos Técnicos Identificados]]

---

## 1. Implementação Atual

```python
# train_simple.py — Passo 3
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 80% treino, 20% teste
    random_state=42,     # reprodutibilidade
    stratify=y           # mantém proporção de classes
)

# Tamanhos com 2600 observações totais (200 alunos × 13 matérias):
# X_train: 2080 amostras
# X_test:  520 amostras
```

---

## 2. Por Que 80/20

| Split | Treino | Teste | Adequado para |
|---|---|---|---|
| 70/30 | 1820 | 780 | Datasets grandes |
| **80/20** (atual) | 2080 | 520 | Datasets médios |
| 90/10 | 2340 | 260 | Datasets pequenos |

Com 2600 observações, 80/20 é uma escolha razoável mas o conjunto de teste (520 amostras) pode ter variância alta nas métricas.

---

## 3. Stratify=y — Estratificação por Classe

```python
stratify=y  # garante que as proporções de classes sejam mantidas no split
```

Sem estratificação, em um split aleatório com apenas 15% de amostras Reprovado, seria possível ter o conjunto de teste sem exemplos suficientes dessa classe. `stratify=y` garante:

```
Treino: 65% Aprovado, 20% Recuperação, 15% Reprovado
Teste:  65% Aprovado, 20% Recuperação, 15% Reprovado
```

---

## 4. Cross-Validation 5-fold

O código usa validação cruzada para estimativa mais robusta das métricas:

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(clf, X, y, cv=cv, scoring='accuracy')
# mean ± std reportados no artigo
```

**5-fold:** divide os dados em 5 partes iguais (520 amostras cada), treina em 4 e testa em 1, rotacionando. Resultado final é a média dos 5 folds.

---

## 5. O Problema Crítico — DT-04: Vazamento Intra-Aluno

```python
# PROBLEMA: mesmo aluno em treino E teste
# Com 200 alunos × 13 matérias = 2600 observações:
# Aluno X tem 13 linhas no dataset
# split aleatório → 10 linhas no treino, 3 linhas no teste
# → modelo "conhece" o aluno pelo treino → inflação artificial de acurácia
```

**Exemplo concreto:**
```
Treino:  Aluno X - Matemática (n1=7, n2=6.5, n3=8 → Aprovado)
         Aluno X - Português  (n1=6, n2=7,   n3=7 → Aprovado)
         ...10 matérias do mesmo aluno...

Teste:   Aluno X - História   (n1=7, n2=6.5, n3=8 → ?)
         → modelo já "conhece" o padrão de notas do Aluno X
         → prediz com alta confiança sem generalizar para NOVOS alunos
```

---

## 6. Correção com GroupKFold

```python
# CORRETO para evitar vazamento intra-aluno:
from sklearn.model_selection import GroupKFold

groups = df['aluno_id'].values  # identifica o grupo de cada amostra

cv = GroupKFold(n_splits=5)
scores = cross_val_score(clf, X, y, cv=cv, groups=groups)
# Garante: nenhum aluno aparece em treino E teste no mesmo fold
```

**Nota:** `GroupKFold` não suporta `stratify` — pode resultar em distribuições de classes desequilibradas por fold. Solução: `StratifiedGroupKFold` (sklearn ≥ 0.24).

---

## 7. Impacto Estimado do DT-04

| Cenário | Acurácia estimada |
|---|---|
| Split atual (com leakage intra-aluno) | 94.0% (M3) |
| GroupKFold correto | Estimado 87-91% |

A diferença pode ser de 3-7 pontos percentuais — significativa para um artigo científico. A acurácia real de generalização para novos alunos (não vistos em treino) é provavelmente ~88-90%.

---

## 8. Train/Test Split vs Cross-Validation — Diferença

| Abordagem | Uso no EduPredict | Resultado |
|---|---|---|
| `train_test_split` | Avaliação final dos modelos | 1 par treino/teste |
| `StratifiedKFold` | Estimativa de variância das métricas | 5 pares, média reportada |

O artigo reporta os resultados do `train_test_split` (split único), não a média da CV. A CV foi usada para verificar estabilidade, mas os números 83.8%, 92.5%, 94.0% vêm do split único.

---

## Links

- [[Pipeline Completo de Treinamento]]
- [[Acurácia F1 e Métricas Gerais]]
- [[Débitos Técnicos Identificados]]
- [[Análise Crítica do TGI]]
- [[class weight balanced — Tratamento de Desbalanceamento]]
- [[Dataset — Estrutura e Geração Sintética]]
