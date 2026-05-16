---
tags: [artigo, modelos, M1, random-forest, early-warning]
created: 2026-05-16
---

# M1 — Modelo Precoce (Após N1)

[[INDEX - ARTIGO|← Índice]] | [[M2 — Modelo Intermediário]] | [[M3 — Modelo de Produção (Após N3)]] | [[Comparação M1 M2 M3]]

> [!INFO] 83,8% de acurácia — máxima antecedência, mínima precisão

---

## 1. Especificação Técnica

| Parâmetro | Valor |
|---|---|
| **Ponto temporal** | Após lançamento de N1 (1º bimestre) |
| **Features de entrada** | 2 |
| **Algoritmo** | RandomForestClassifier |
| **Acurácia (CV 5-fold)** | **83,8%** |
| **Arquivo de modelo** | `02-ML/models/model_m1.pkl` |

---

## 2. Features do M1

| Feature | Importância estimada | Disponível |
|---|---|---|
| `n1_norm` | ~85-90% | ✅ |
| `serie_num_norm` | ~10-15% | ✅ |

Com apenas 2 features, M1 é essencialmente um threshold em N1 com ajuste por série. A complexidade do Random Forest é desperdiçada aqui — uma regressão logística simples provavelmente atingiria performance similar.

---

## 3. Por Que 2 Features Apenas?

No ponto temporal do M1 (após N1), as seguintes features são indisponíveis ou instáveis:
- `n2_norm`, `n3_norm` — notas ainda não lançadas
- `slope_notas` — com 1 ponto, slope = 0 (definido assim em `_slope()` com n<2)
- `variancia_notas` — com 1 ponto, variância = 0
- `pct_materias_ok` — status calculado com N1 apenas, instável

Na prática, apenas `n1_norm` carrega informação real. `serie_num_norm` é constante por aluno e captura contexto estrutural (série 9º ano tem distribuição de notas diferente de 6º ano).

---

## 4. Valor Operacional do M1

O M1 com 83,8% de acurácia e **9 meses de antecedência** (N1 é lançada no 1º bimestre, resultado final no 4º) tem alto valor se:

1. A escola consegue agir com 9 meses de antecedência
2. A intervenção com base em N1 é possível e eficaz
3. O custo de falsos positivos (alarme desnecessário) é aceitável

**Limitação prática:** um professor que vê um aluno tirar 3,0 em N1 já sabe que há risco — o M1 não adiciona muito sobre o julgamento humano imediato. O valor do ML aqui seria para **consolidação de múltiplas matérias** — identificar automaticamente alunos em risco em TODAS as disciplinas, não apenas na disciplina do professor.

---

## 5. Degradação de Performance vs M3

| Modelo | Acurácia | Antecedência | Gap de acurácia vs M3 |
|---|---|---|---|
| M1 | 83,8% | 9 meses | -10,2 pp |
| M2 | 92,5% | 6 meses | -1,5 pp |
| M3 | 94,0% | 3 meses | 0 (referência) |

O salto M1→M2 (+8,7 pp) é muito maior que M2→M3 (+1,5 pp). Isso sugere que N2 carrega informação crítica — a nota do 2º bimestre é muito mais preditiva do resultado final que a nota do 1º.

---

## 6. Implementação e Uso

```python
# gui_ml_integration.py — seleção automática de modelo
class MLModelLoader:
    def load_model(self, n1, n2, n3):
        """Seleciona o modelo mais avançado disponível."""
        if n3 is not None:
            return self.model_m3, 'M3'
        elif n2 is not None:
            return self.model_m2, 'M2'
        elif n1 is not None:
            return self.model_m1, 'M1'
        else:
            return None, None
```

M1 é usado automaticamente quando apenas N1 está disponível. A interface não exibe qual modelo está sendo usado — seria uma melhoria de transparência.

---

## 7. Limitações Específicas do M1

1. **Alta incerteza:** com 1 nota e 1 feature contextual, a variância da predição é muito alta. O modelo pode estar muito confiante em predições que não se sustentam ao longo do ano.

2. **Efeito "prova fácil":** se N1 foi uma prova atípica (fácil ou difícil), distorce toda a predição. Com apenas 1 ponto temporal, não há mecanismo de correção.

3. **Sem contexto de comportamento:** um aluno que tira 4,0 em N1 mas vai frequentemente às aulas de reforço tem prognóstico diferente de um que tira 4,0 e não aparece. M1 não captura isso.

4. **Viés de série:** `serie_num_norm` pode capturar diferenças curriculares reais entre séries, mas também pode capturar diferenças na dificuldade das provas por série — confundidores não separados.

---

## Links

- [[M2 — Modelo Intermediário]]
- [[M3 — Modelo de Produção (Após N3)]]
- [[Comparação M1 M2 M3]]
- [[Visão Geral das 9 Features]]
- [[Pipeline Completo de Treinamento]]
- [[gui ml integration py — Motor de Predição]]
