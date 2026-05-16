---
tags: [artigo, feature-engineering, leakage, media_pond_norm, removida]
created: 2026-05-16
---

# media_pond_norm — Feature Removida por Leakage

[[INDEX - ARTIGO|← Índice]] | [[Data Leakage — Conceito e Impacto]] | [[Detecção Automática por Correlação de Pearson]] | [[n4 norm — Feature Removida]]

> [!CRITICAL] Correlação r=0,95 com o target — a feature que mais infla a acurácia artificialmente

---

## 1. Definição

$$media\_pond\_norm = \frac{0,2 \times N1 + 0,25 \times N2 + 0,25 \times N3 + 0,30 \times N4}{10}$$

Média ponderada de todas as 4 notas, normalizada para [0, 1].

---

## 2. Por Que É Leakage

O target `status_encoded` é definido exatamente pela média ponderada:
- status = 2 (Aprovado) se `media_pond` ≥ 6,0
- status = 1 (Recuperação) se 5,0 ≤ `media_pond` < 6,0
- status = 0 (Reprovado) se `media_pond` < 5,0

Portanto, `media_pond_norm` **determina diretamente** `status_encoded`. Incluí-la como feature seria equivalente a incluir o target como feature — um caso extremo de target leakage.

A correlação de Pearson r=0,95 (quase perfeita) é a consequência matemática direta dessa relação.

---

## 3. O Problema Adicional — N4 Inclusa

`media_pond_norm` usa N4, que só está disponível ao final do ano letivo — exatamente o mesmo momento em que o resultado (status) é determinado. Um modelo que usa `media_pond_norm` para prever o status não está fazendo "previsão" — está calculando o resultado a partir dos mesmos dados que o definem.

---

## 4. O Que Aconteceria com media_pond_norm no Treino

```python
# CENÁRIO HIPOTÉTICO — com leakage
features_leaky = ['n1_norm', 'n2_norm', 'n3_norm', 'n4_norm', 'media_pond_norm', ...]
target = 'status_encoded'

# O modelo aprenderia:
# if media_pond_norm >= 0.6: status = 2
# elif media_pond_norm >= 0.5: status = 1
# else: status = 0

# Acurácia estimada: ~99% — completamente artificial
# Feature importance de media_pond_norm: ~90%
# Restante das features: ~10% no total
```

O modelo seria inútil para predição real (onde media_pond_norm não está disponível antes do resultado), mas mostraria métricas aparentemente excelentes.

---

## 5. Por Que É Mantida na Tabela ml_features?

`media_pond_norm` é calculada e armazenada em `ml_features` para **visualização** na interface `MLPage` do `gui_escola.py`. Professores podem consultar a média ponderada de um aluno pelo sistema.

Mas é excluída explicitamente antes do treinamento em `train_simple.py`.

**Risco:** um desenvolvedor futuro poderia inadvertidamente incluí-la em um modelo. Ver [[Débitos Técnicos Identificados#DT-03]].

---

## 6. Comparação com media_geral_aluno (Feature Legítima)

| Feature | Cálculo | Status | Razão |
|---|---|---|---|
| `media_pond_norm` | média de N1-N4 (ponderada) para ESTA matéria | 🚫 Removida (r=0,95) | Usa N4 — futuro |
| `media_geral_aluno` | média de TODAS as matérias do aluno (notas disponíveis) | ✅ Mantida (r≈0,60) | Usa apenas notas do passado |

A distinção é sutil mas crítica: `media_pond_norm` é a média desta matéria específica (com N4), enquanto `media_geral_aluno` é uma média cross-matéria das notas historicamente disponíveis.

---

## Links

- [[Data Leakage — Conceito e Impacto]]
- [[Detecção Automática por Correlação de Pearson]]
- [[n4 norm — Feature Removida]]
- [[Débitos Técnicos Identificados]]
- [[Visão Geral das 9 Features]]
