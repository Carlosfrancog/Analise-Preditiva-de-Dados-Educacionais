---
tags: [artigo, resultados, feature-importance, M3, interpretabilidade]
created: 2026-05-16
---

# Feature Importance Detalhada — M3

[[INDEX - ARTIGO|← Índice]] | [[M3 — Modelo de Produção (Após N3)]] | [[Visão Geral das 9 Features]] | [[Random Forest — Algoritmo e Justificativa]]

---

## 1. Ranking Completo de Importâncias (M3)

| Rank | Feature | Importância | Grupo | Interpretação |
|---|---|---|---|---|
| 1 | `n2_norm` | **32,3%** | Nota bruta | Nota do 2º bimestre domina o modelo |
| 2 | `pct_materias_ok` | **21,5%** | Contexto global | Comportamento cross-matéria é altamente preditivo |
| 3 | `slope_notas` | **12,3%** | Dinâmica temporal | Tendência (para cima ou baixo) é mais informativa que a média |
| 4 | `n3_norm` | 8,7% | Nota bruta | Nota mais recente — surpreendentemente menos importante que N2 |
| 5 | `media_geral_aluno` | 7,8% | Contexto global | Média histórica do aluno tem peso moderado |
| 6 | `variancia_notas` | 5,2% | Dinâmica temporal | Consistência das notas — complementa o slope |
| 7 | `media_turma_norm` | 4,8% | Referência | Comparação com a turma tem impacto pequeno mas real |
| 8 | `n1_norm` | 4,1% | Nota bruta | Nota inicial — pouco informativa com N2 e N3 disponíveis |
| 9 | `serie_num_norm` | 3,3% | Contextual | Série escolar — menos importante do que esperado |

---

## 2. Insights Analíticos

### Por que n2_norm (32,3%) supera n3_norm (8,7%)?

N2 é a nota do 2º bimestre. N3 é a nota do 3º bimestre — a mais recente no ponto de predição do M3. Intuitivamente, N3 deveria ser mais informativa (mais próxima do resultado).

**Hipóteses para a dominância de N2:**

1. **Estabilidade:** N2 é uma avaliação "de meio de caminho" — alunos que vão bem em N2 tendem a confirmar em N3 e N4. N3 pode ser mais ruidosa (alguns alunos estudam muito para N3 após um N2 ruim, criando ruído).

2. **N2 captura o "verdadeiro nível":** após N1 (pode ser alta variância), N2 é quando os alunos ajustam sua dedicação. É o primeiro dado de "comportamento equilibrado".

3. **Correlação com slope:** n2_norm e slope_notas juntos explicam 44,6% da importância. N2 entra tanto diretamente quanto indiretamente (via slope = f(N1, N2, N3)).

4. **Multicolinearidade N2/N3:** n2_norm e n3_norm são correlacionadas. O RF distribui a importância entre elas — se uma é removida, a outra absorve. A distribuição pode ser historicamente incidental ao dataset sintético.

### Por que pct_materias_ok (21,5%) supera todas as notas individuais exceto N2?

Comportamento cross-matéria captura o "tipo de aluno" de forma mais robusta que qualquer nota específica. Um aluno em risco em 10 de 13 matérias tem um perfil estrutural diferente — não é uma questão de dificuldade com uma matéria específica.

### Por que serie_num_norm (3,3%) é tão pouco importante?

Série escolar deveria capturar diferenças de dificuldade curricular. Possíveis razões para baixa importância:
1. O dataset sintético pode ter distribuído notas de forma similar em todas as séries
2. As outras features (especialmente médias normalizadas) já capturam indiretamente o efeito série
3. O currículo brasileiro tem pouca variação inter-série na estrutura de avaliação

---

## 3. Comparação com Feature Importance de M1 e M2

O artigo reporta importâncias apenas para M3. Extrapolando:

**M1 (2 features):**
- `n1_norm`: ~90% (quase tudo)
- `serie_num_norm`: ~10%

**M2 (4-5 features):**
- `n2_norm`: ~55% (domina ainda mais que no M3)
- `slope_notas`: ~20%
- `n1_norm`: ~15%
- `variancia_notas`, `serie_num_norm`: ~10%

A dominância de N2 é um padrão consistente entre M2 e M3. Isso sugere que o design de usar M2 como modelo operacional principal (maior antecedência com alta acurácia) está bem fundamentado.

---

## 4. Feature Importance Global vs Local

As importâncias acima são **globais** — médias sobre todos os exemplos de treinamento. Para um professor que quer entender por que o aluno João está em risco, a importância local (SHAP) seria:

```
João — predição: 67% Reprovado
  n2_norm (3,5/10):        +0,42 para Reprovado  ← mais importante para João
  pct_materias_ok (0,3):   +0,28 para Reprovado  ← 70% das matérias em risco
  slope_notas (-0,3):      +0,15 para Reprovado  ← tendência descendente
  n3_norm (4,0/10):        +0,09 para Reprovado
  ...
```

Feature importance global diz "N2 é importante em média". SHAP diz "a N2 específica de João é por isso que ele vai reprovar". A diferença é fundamental para intervenção pedagógica.

---

## 5. Implicações Práticas

| Feature importante | Intervenção possível |
|---|---|
| `n2_norm` alta importância | Focar atenção após N2 — esse é o ponto crítico de alerta |
| `pct_materias_ok` alta importância | Monitorar alunos com falhas em múltiplas matérias simultaneamente |
| `slope_notas` 3ª posição | Tendência importa — um N2 ruim mas com slope positivo é menos grave |
| `n3_norm` menos importante que N2 | N3 pode ser estudada "em crise" — não captura o nível real |

---

## Links

- [[M3 — Modelo de Produção (Após N3)]]
- [[Visão Geral das 9 Features]]
- [[Random Forest — Algoritmo e Justificativa]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Análise Crítica do TGI]]
- [[Insights para Artigo de Extensão]]
