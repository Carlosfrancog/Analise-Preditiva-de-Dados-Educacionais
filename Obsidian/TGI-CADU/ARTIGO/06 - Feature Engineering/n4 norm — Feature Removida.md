---
tags: [artigo, feature-engineering, leakage, n4_norm, removida]
created: 2026-05-16
---

# n4_norm — Feature Removida por Leakage Temporal

[[INDEX - ARTIGO|← Índice]] | [[Data Leakage — Conceito e Impacto]] | [[media pond norm — Feature Removida]] | [[Visão Geral das 9 Features]]

> [!CRITICAL] Correlação r=0,91 com o target — temporal leakage claro

---

## 1. Definição

$$n4\_norm = \frac{N4}{10}$$

Nota do 4º bimestre normalizada. N4 tem peso 30% na média ponderada — o maior peso entre as 4 notas.

---

## 2. Por Que É Leakage Temporal

N4 é a última nota antes do resultado final. No calendário escolar:
- Status final é calculado no final do 4º bimestre
- N4 é lançada no mesmo período do status final

Um modelo que usa N4 para "prever" o status não está fazendo previsão — está aplicando uma regra determinística sobre dados que só existem simultaneamente ao resultado:

```
Se o aluno tem N4 → o status já foi determinado
Logo, N4 não é uma feature preditiva — é contemporânea ao target
```

---

## 3. Correlação Alta — r=0,91

N4 tem peso 30% na média ponderada. A correlação de 0,91 é alta mas não tão alta quanto media_pond_norm (0,95) porque N4 sozinha não determina completamente o status — os outros 70% do peso vêm de N1-N3.

Mas 0,91 ainda está acima do threshold de 0,9 e foi corretamente removida.

---

## 4. Cenário de Uso Indevido

```python
# CENÁRIO INDEVIDO — usar N4 para "prever" status
# Na realidade: N4 só existe quando o status já foi calculado
# Isso só seria útil se houvesse delay entre o lançamento de N4 e o conselho de classe

features_com_n4 = ['n1_norm', 'n2_norm', 'n3_norm', 'n4_norm', ...]
# modelo aprenderia: if n4 > 0.5 and n1+n2+n3 suficientes → Aprovado
# Acurácia artificial: ~96%
```

---

## 5. Diferença de n3_norm (Legítima) vs n4_norm (Leaky)

| Feature | Disponível quando? | Status |
|---|---|---|
| `n3_norm` | Após 3º bimestre — 3 meses antes do resultado | ✅ Legítima |
| `n4_norm` | Após 4º bimestre — mesmo momento que o resultado | 🚫 Leakage |

A diferença é o timing. n3_norm existe antes do resultado — é previsão legítima. n4_norm existe ao mesmo tempo que o resultado — não é previsão.

---

## 6. Por Que Foi Armazenada em ml_features?

Similar a `media_pond_norm` — armazenada para visualização, não para treinamento. Um professor consultando as notas de um aluno pelo sistema pode ver N4 na tabela de features ML, mas essa nota nunca entra em nenhum modelo.

---

## Links

- [[Data Leakage — Conceito e Impacto]]
- [[Detecção Automática por Correlação de Pearson]]
- [[media pond norm — Feature Removida]]
- [[Visão Geral das 9 Features]]
- [[Débitos Técnicos Identificados]]
