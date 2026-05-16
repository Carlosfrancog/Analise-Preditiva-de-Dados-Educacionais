---
tags: [artigo, edm, learning-analytics, teoria, mineracao-dados]
created: 2026-05-14
---

# Educational Data Mining e Learning Analytics

[[INDEX - ARTIGO|← Índice]] | [[Machine Learning em Educação]] | [[Romero e Ventura 2020 — EDM Survey]]

---

## 1. Definições e Distinção

**Educational Data Mining (EDM):**
Campo interdisciplinar que aplica técnicas de mineração de dados a dados gerados em contextos educacionais, com o objetivo de descobrir padrões que melhorem o processo de ensino-aprendizagem (Romero e Ventura, 2020).

**Learning Analytics (LA):**
Medição, coleta, análise e comunicação de dados sobre aprendizes e seus contextos, com o propósito de compreender e otimizar a aprendizagem e os ambientes em que ela ocorre (Society for Learning Analytics Research, 2011).

### Distinção Prática

| Dimensão | EDM | LA |
|---|---|---|
| **Foco** | Descoberta automática de padrões | Reflexão e ação humana sobre padrões |
| **Audiência primária** | Pesquisadores/engenheiros | Educadores e gestores |
| **Abordagem** | Bottom-up (dados → padrões) | Top-down (hipóteses → dados) |
| **Exemplo** | Treinar RF para detectar evasão | Dashboard de engajamento para professor |

O EduPredict se posiciona como **EDM** (descoberta automatizada via RF), com potencial de evoluir para **LA** ao adicionar o portal de visualização para educadores.

---

## 2. Geração de Abordagens na Literatura

| Geração | Período | Tecnologia | Limitação principal |
|---|---|---|---|
| 1ª | 2000-2010 | Regras estáticas, limiar de frequência | Baixa sensibilidade, critérios arbitrários |
| 2ª | 2010-2018 | ML supervisionado (RF, SVM, regressão) | Caixa-preta, sem explicabilidade, data leakage não tratado |
| 3ª | 2018-hoje | ML + SHAP + feedback loops + LGPD | Em desenvolvimento; foco do artigo de extensão |

O EduPredict está na **transição 2ª→3ª geração**: implementou detecção de data leakage (diferencial), mas ainda não incorporou SHAP nem mecanismos de feedback.

---

## 3. Taxonomia de Tarefas em EDM

Romero e Ventura (2020) classificam as tarefas de EDM em:

1. **Predição de desempenho** — classificar alunos em categorias de sucesso/risco ← *foco do EduPredict*
2. **Clustering** — agrupar alunos por perfil de aprendizagem
3. **Mineração de padrões de relacionamento** — descobrir associações entre disciplinas
4. **Detecção de comportamentos** — identificar comportamentos de evasão em LMS
5. **Descoberta de estrutura** — mapear dependências entre conceitos

O EduPredict faz exclusivamente **tarefa 1**, com dados estáticos de notas. A evolução natural seria incorporar tarefas 4 e 5 com dados de presença e engajamento.

---

## 4. Data Leakage em EDM — Por Que É Negligenciado?

Romero e Ventura (2020) explicitamente identificam data leakage como problema frequente na literatura de EDM. Os autores observam que:

> *"Muitos estudos reportam acurácias acima de 90% que não se sustentam em validação externa, frequentemente porque variáveis derivadas do target são incluídas como features."*

O EduPredict é um dos poucos artigos de EDM no contexto brasileiro que implementa **detecção automática** de data leakage. Ver [[Detecção Automática por Correlação de Pearson]].

---

## 5. Impacto no Projeto Atual

O sistema EduNotas implementa EDM de forma completa (geração de features SQL → treino RF → predição por aluno). A interface de predições ([[gui predicoes improved py — Interface Preditiva]]) é uma forma primitiva de Learning Analytics — mostra o resultado ao professor, mas sem contexto interpretativo suficiente (SHAP local ausente).

**Refatoração sugerida:** adicionar camada de LA sobre o EDM existente — traduzir feature importance local em linguagem natural para cada predição exibida no dashboard.

---

## 6. Análise Crítica

> [!WARNING] Limitação metodológica da geração 2 que o EduPredict herda
> O EduPredict usa feature importance global (média sobre todo o dataset) para interpretar o modelo. Isso é **insuficiente** para uso prático: a importância de `n2_norm` ser 32,3% em média não significa que ela é a mais importante para *aquele* aluno específico.
>
> Um aluno com N1=9,0 e N2=3,0 tem uma situação completamente diferente de um com N1=4,0 e N2=4,5, mesmo que ambos tenham a mesma média. SHAP local resolveria isso.

---

## Links

- [[Romero e Ventura 2020 — EDM Survey]]
- [[Machine Learning em Educação]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Feature Importance Detalhada — M3]]
- [[Análise Crítica do TGI]]
