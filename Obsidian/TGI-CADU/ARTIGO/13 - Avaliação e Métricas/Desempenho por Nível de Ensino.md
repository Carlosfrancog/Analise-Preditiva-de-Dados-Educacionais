---
tags: [artigo, metricas, desempenho, nivel-escolar, serie, resultados]
aliases: [Desempenho por Nível Escolar, Desempenho por Nível de Ensino]
created: 2026-05-16
---

# Desempenho por Nível de Ensino — M3

[← Índice](<../INDEX - ARTIGO.md>) | [[Acurácia F1 e Métricas Gerais]] | [[Matriz de Confusão M3 — Análise Detalhada]] | [[serie num norm — Contexto Série]]

---

## 1. Por Que Analisar por Nível

Uma acurácia global de 94% pode esconder variações sistemáticas por série. Se o modelo performa muito melhor no Ensino Médio do que no Fundamental, isso sugere que:
- O modelo é mais útil para professores do EM
- Os professores do Ensino Fundamental têm predições menos confiáveis
- A coleta de dados ou distribuição de classes varia por nível

---

## 2. Acurácia Estimada por Nível (Baseado no Dataset Sintético)

> **Nota:** Os valores abaixo são estimativas baseadas na análise das features e distribuição do dataset sintético. Não foram calculados explicitamente no artigo — seriam resultado de subgrupo análise pós-hoc.

| Nível | Séries | Acurácia M3 (estimada) |
|---|---|---|
| **Fundamental** | 6F, 7F, 8F, 9F | ~89-92% |
| **Médio** | 1M, 2M, 3M | ~94-96% |

**Por que o Médio seria ligeiramente melhor:**
- Alunos do Ensino Médio têm trajetória de notas mais estável (padrão estabelecido de 4+ anos)
- `pct_materias_ok` é mais discriminante no EM (alunos com dificuldades têm padrão claro)
- O limiar de 6.0 para aprovação é mais consistentemente aplicado no EM

---

## 3. Análise por Série — Insight de serie_num_norm

```python
# Análise de subgrupo (não implementada no sistema atual):
for serie in df['serie_num_norm'].unique():
    mask = df['serie_num_norm'] == serie
    acc_serie = accuracy_score(y_test[mask], y_pred[mask])
    print(f"série {serie:.2f}: {acc_serie:.1%}")
```

**Resultado esperado:**
```
6F (0.00): ~88%  ← menor  — notas mais variáveis, padrão menos estabelecido
7F (0.17): ~90%
8F (0.33): ~91%
9F (0.50): ~92%
1M (0.67): ~93%
2M (0.83): ~94%
3M (1.00): ~95%  ← maior  — padrão mais estável, pressão ENEM clareia tendências
```

---

## 4. Implicação para Uso em Produção

Se a acurácia varia por série, professores do Ensino Fundamental deveriam receber a informação de confiança junto com a predição:

```
Card de Disciplina (6º Fundamental):
  Predição: Em Risco (72% de probabilidade)
  ⚠️ Confiança: Moderada — modelo tem 89% de acurácia para o 6º ano
  
Card de Disciplina (3º Médio):
  Predição: Em Risco (72% de probabilidade)
  ✓ Confiança: Alta — modelo tem 95% de acurácia para o 3º ano
```

Isso exigiria calibração de confiança por subgrupo — funcionalidade não implementada.

---

## 5. Viés por Nível — Risco Ético

O fato de o modelo ter acurácia mais baixa no Fundamental **não significa que é menos útil**. Mas significa que alunos do 6º ano têm probabilidade maior de receber predições incorretas — tanto falsas alarmes quanto falsos seguros.

Como o Ensino Fundamental atende crianças mais jovens (11-14 anos), erros de predição têm impacto pedagógico maior (expectativas de professores, comunicação com família).

Ver: [[LGPD e Ética no EduPredict]] | [[serie num norm — Contexto Série]]

---

## 6. Análise por Matéria — Outra Dimensão

Além de nível de ensino, o desempenho do modelo pode variar por matéria:
- Matemática: notas mais bimodais (ou vai bem ou vai mal) → maior separabilidade → maior acurácia
- Artes: notas mais uniformemente altas → menos variação → modelo menos informativo
- Educação Física: quase todos aprovados → acurácia trivialmente alta

O dataset sintético usa as mesmas 13 matérias para todos os alunos, o que suaviza essas diferenças reais.

---

## Links

- [[Acurácia F1 e Métricas Gerais]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
- [[serie num norm — Contexto Série]]
- [[LGPD e Ética no EduPredict]]
- [[Análise Crítica do TGI]]
- [[Dataset — Estrutura e Geração Sintética]]
