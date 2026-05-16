---
tags: [artigo, insights, extensao, futuro, pesquisa]
aliases: [Insights para Artigo de Extensão, Insights para o Artigo de Extensão]
created: 2026-05-16
---

# Insights para o Artigo de Extensão

[← Índice](<../INDEX - ARTIGO.md>) | [[Análise Crítica do TGI]] | [[Decisões e Trade-offs]] | [[Limitações Gerais do Artigo]]

---

## 1. Por Que um Artigo de Extensão

O TGI documenta uma **prova de conceito funcional** mas com limitações metodológicas significativas. Um artigo de extensão (para conferência ou periódico) poderia:

1. Corrigir as limitações identificadas (GroupKFold, dados reais)
2. Comparar com baselines publicados
3. Conduzir estudo de usuário com professores reais
4. Abordar LGPD e ética

---

## 2. Principais Achados do TGI — O Que Vale Preservar

### 2.1 Detecção Automática de Data Leakage
O mecanismo de Pearson (threshold=0.9) para detectar features leaky é a contribuição técnica mais original e diretamente publicável.

```python
# O pipeline de detecção — contribuição core:
correlations = df[feature_cols].corrwith(df['status_encoded']).abs()
leaky = correlations[correlations > threshold].index.tolist()
```

Contribuição: **sistemática, automática, replicável** — vs abordagem manual de outros trabalhos.

### 2.2 Arquitetura Temporal de Três Modelos
M1→M2→M3 com contextos crescentes de informação é um framework natural para EWS escolar. O design é sólido mesmo que a execução tenha débitos.

### 2.3 Interface Integrada com o Professor
A GUI com cards por disciplina e perfil de risco é um differentiator vs artigos que só relatam métricas — aborda o problema de adoção.

---

## 3. Agenda de Pesquisa — Contribuições para Extensão

### 3.1 Validação com Dados Reais
**Por que importa:** Dataset sintético limita generalizabilidade. Com dados reais:
- Distribuição de classes diferente
- Correlações entre features diferentes
- Leakage patterns diferentes

**O que fazer:**
```
- Parceria com escola municipal/estadual
- Anonimização dos dados (LGPD)
- Mínimo: 3 turmas, 1 ano letivo completo
- Comparar: acurácia sintético vs real
```

### 3.2 Estudo de Usuário com Professores
**Métricas de adoção:**
- Tempo até primeira ação pedagógica após alerta
- Taxa de concordância professor/modelo
- Impacto nos resultados finais dos alunos alertados

**Design:** protocolo A/B — turmas com sistema vs controle.

### 3.3 SHAP para Justiça Algorítmica
**Pergunta de pesquisa:** "O modelo discrimina alunos por série de forma injustificada?"

```python
# Análise de SHAP por subgrupo:
for serie in df['serie_num_norm'].unique():
    mask = df['serie_num_norm'] == serie
    shap_subset = shap_values[mask]
    # Comparar: qual feature mais influencia por série?
```

### 3.4 Comparação com Baselines da Literatura
O artigo atual não compara com trabalhos como Lima (2021) nos mesmos dados. Um artigo de extensão deveria:
- Reimplementar Lima (2021) no mesmo dataset
- Comparar com XGBoost, SVM, Logistic Regression
- Reportar F1 Macro (não apenas Weighted) para comparação justa

---

## 4. Hipóteses para Testar

1. **H1:** GroupKFold reduz a acurácia reportada em ≥5 pontos percentuais
2. **H2:** Dados reais têm distribuição de leaky features diferente do sintético
3. **H3:** SHAP local aumenta a taxa de ação pedagógica dos professores em >20%
4. **H4:** A incorporação de frequência aumenta o Recall de Recuperação em >10pp

---

## 5. Framing Narrativo para Publicação

**Ângulo recomendado:** "Early Warning Systems para educação básica brasileira: uma abordagem modular com detecção automática de data leakage e feedback incremental"

**Pontos fortes a enfatizar:**
- Contexto brasileiro (LGPD, ENEM, sistema bimestral)
- Detecção automática de leakage (contribuição técnica)
- Interface pedagógica (não só ML puro)
- Abordagem temporal M1-M2-M3

**Pontos a abordar honestamente:**
- Dataset sintético (limitação explícita)
- Sem comparação com baselines externos
- Sem estudo de impacto real

---

## 6. Roadmap para Extensão (12 meses)

```
Mês 1-2:   Corrigir DT-01, DT-04 no código atual
Mês 2-3:   Coletar dados reais (parceria com escola)
Mês 3-4:   Implementar SHAP + Alertas EWS
Mês 4-6:   Estudo piloto com 1-2 professores
Mês 6-8:   Análise de resultados e comparação com literatura
Mês 8-10:  Redigir artigo de extensão
Mês 10-12: Submissão para SBIE/CBIE/RBIE ou periódico Qualis A2+
```

---

## Links

- [[Análise Crítica do TGI]]
- [[Limitações Gerais do Artigo]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Protocolo de Alertas EWS]]
- [[Incorporação de Frequência e Engajamento]]
- [[LGPD e Ética no EduPredict]]
- [[Débitos Técnicos Identificados]]
