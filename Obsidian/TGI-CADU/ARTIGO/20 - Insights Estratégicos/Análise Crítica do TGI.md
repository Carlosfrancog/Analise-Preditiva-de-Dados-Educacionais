---
tags: [artigo, critica, tgi, analise, limitacoes, insights]
created: 2026-05-16
---

# Análise Crítica do TGI — EduPredict

[[INDEX - ARTIGO|← Índice]] | [[Limitações Gerais do Artigo]] | [[Análise Comparativa dos Trabalhos]] | [[Decisões e Trade-offs]]

> [!WARNING] Esta nota é deliberadamente crítica — o objetivo é identificar o que o TGI não diz, onde a argumentação é fraca, e o que pode ser melhorado em um artigo de extensão.

---

## 1. Pontos Fortes Genuínos

### 1.1 Detecção Automática de Data Leakage
Este é o diferencial técnico mais sólido. A implementação com Pearson > 0,9 é simples mas eficaz para os casos identificados. É uma contribuição real — ver [[Detecção Automática por Correlação de Pearson]].

### 1.2 Três Modelos Temporais
A abordagem M1/M2/M3 com pontos de corte temporais é metodologicamente sofisticada. Permite análise explícita do trade-off antecedência × acurácia — algo que Lima (2021) e Melo (2023) não fazem.

### 1.3 Volume de Dados
15.613 registros supera todos os trabalhos nacionais consultados (Melo: 500 alunos). Mesmo sendo dados sintéticos, o volume é relevante para estabilidade estatística.

---

## 2. Pontos Fracos Críticos

### 2.1 Dataset Sintético — A Limitação Mais Grave

**O problema:** os dados são gerados artificialmente, não coletados de uma escola real. Isso levanta questões sérias:

1. **Distribuição de notas** — a geração sintética pode não capturar padrões reais (concentração bimodal de notas, efeito professor, sazonalidade)
2. **Correlação inter-matérias** — um aluno real que vai mal em Matemática tem probabilidade maior de ir mal em Física. Dados sintéticos podem não capturar essa correlação estrutural
3. **Ausência de drift temporal** — alunos reais mudam ao longo do ano de formas que dados sintéticos não reproduzem

**Consequência:** a acurácia de 94,0% pode ser inflada pela estrutura artificial dos dados. Um modelo treinado nesses dados pode ter performance significativamente inferior em dados reais.

**O artigo deveria:** discutir explicitamente a ausência de dados reais como limitação maior, não apenas como "dataset para desenvolvimento".

### 2.2 Benchmark Injusto

O artigo compara seus 94,0% com Lima (78%) e Melo (82%), mas:

- Lima: dados **reais** de universidade, com problemas de desbalanceamento não tratados
- Melo: 500 alunos, contexto diferente
- EduPredict: 200 alunos / 13 matérias / dados sintéticos

A comparação não é metodologicamente justa. Dados sintéticos tendem a ser mais "limpos" e estruturados do que dados reais. O ganho de 12-16 pontos percentuais pode ser parcialmente artificial.

### 2.3 Recuperação com Recall 62,2% — Não Discutido Adequadamente

O grupo mais crítico para um EWS (alunos em zona de risco marginal — Recuperação) é o que o modelo pior classifica. O artigo reporta o número mas não discute as implicações operacionais:

- Quantos alunos reais seriam "deixados passar" por semestre?
- Qual o custo pedagógico de um falso negativo vs falso positivo?
- Qual threshold seria mais adequado para uso real?

### 2.4 Hiperparâmetros Não Documentados

O artigo menciona `class_weight='balanced'` e `random_state=42`, mas não documenta:
- `n_estimators`
- `max_depth`
- `max_features`
- Processo de seleção de hiperparâmetros (grid search? manual?)

Isso viola o princípio de reprodutibilidade científica.

### 2.5 Validação Cruzada com Vazamento Intra-Aluno

O dataset tem 200 alunos × 13 matérias = 2.600 pares aluno-matéria. A validação cruzada com k=5 divide aleatoriamente esses pares, mas **o mesmo aluno pode aparecer no treino e no teste**. Isso viola a independência das observações:

- Se aluno X com notas altas aparece em treino, o modelo "aprende" seu padrão geral
- O mesmo aluno X no teste tem features parecidas → inflação de acurácia

**Solução correta:** validação cruzada agrupada por aluno (GroupKFold):
```python
from sklearn.model_selection import GroupKFold
gkf = GroupKFold(n_splits=5)
scores = cross_val_score(clf, X, y, groups=df['aluno_id'], cv=gkf)
```

Esta é provavelmente a limitação metodológica mais grave do TGI, e não é mencionada.

### 2.6 Ausência de LGPD/Ética

O sistema processa dados de alunos menores de idade. O artigo não discute:
- Consentimento informado
- Direito ao contraditório (aluno pode contestar predição)
- Retenção e exclusão de dados
- Transparência algorítmica para pais/responsáveis

Em contexto regulatório real, isso seria um bloqueador de implantação.

---

## 3. Argumentação Questionável

### 3.1 "O sistema implementa EWS de 3 níveis"

O EWS com 3 níveis (Informativo/Atenção/Crítico) é descrito como contribuição, mas:
- A lógica de classificação usa `avg_risk > 0.7` e `avg_risk > 0.4` — thresholds arbitrários sem validação com dados reais ou especialistas pedagógicos
- O "Early Warning" em M3 (após N3) não é tão "early" — restam apenas ~2 meses

### 3.2 "Dataset de 15.613 registros"

O número parece grande mas é enganoso: são 200 alunos × 13 matérias × 7 notas/aluno/matéria = 18.200 entradas brutas, mas os registros ML são por (aluno, matéria), não por nota individual. 200 alunos × 13 matérias = 2.600 pares únicos é o número real de observações independentes.

### 3.3 Feature Importance como Explicabilidade

O artigo usa feature importance global como se fosse explicabilidade do modelo. São coisas diferentes:
- **Feature importance global:** "N2 é importante para o modelo em média"
- **Explicabilidade local (SHAP):** "Para esse aluno específico, N2 aumentou/diminuiu a probabilidade de reprovação em X%"

Para uso pedagógico real, apenas a explicabilidade local é útil.

---

## 4. O Que o TGI É vs O Que Afirma Ser

| Afirmação | Realidade |
|---|---|
| "Sistema de predição precoce" | Sistema de predição tardia (usa até N3 de 4) |
| "Dataset de 15.613 registros" | ~2.600 pares (aluno, matéria) com 7 duplicatas cada |
| "Acurácia de 94%" | 94% com possível inflação por validação não agrupada por aluno |
| "Data leakage tratado" | Leakage direto tratado; leakage indireto (pct_materias_ok) não verificado |
| "Diferencial único na literatura" | Detecção automática de leakage é diferencial real; RF em EDM não é |

---

## 5. O Que Realmente Funciona (Perspectiva de Engenharia)

Apesar das críticas, o sistema **funciona como software**:
- Pipeline de ponta a ponta (dados → treino → predição → interface)
- Interface tkinter funcional com visualizações
- Integração ML → GUI bem estruturada
- Arquitetura modular (cads.py, train_simple.py, gui_ml_integration.py)

O problema não é de engenharia — é de rigor científico na avaliação e apresentação dos resultados.

---

## 6. Recomendações para o Artigo de Extensão

1. **Usar GroupKFold** por aluno para validação cruzada honesta
2. **Coletar dados reais** de pelo menos uma escola parceira (mesmo que pequenos)
3. **Reportar macro-recall** em vez de apenas acurácia global
4. **Discutir LGPD** como constraint de design, não como footnote
5. **Implementar SHAP** para justificar predições individuais
6. **Ajustar threshold** de Recuperação para priorizar recall sobre precisão
7. **Validar thresholds do EWS** com educadores — 0,7 e 0,4 são arbitrários

---

## Links

- [[Limitações Gerais do Artigo]]
- [[Análise Comparativa dos Trabalhos]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
- [[Data Leakage — Conceito e Impacto]]
- [[Detecção Automática por Correlação de Pearson]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[LGPD e Ética no EduPredict]]
- [[Decisões e Trade-offs]]
- [[Plano de Artigo ABNT]]
