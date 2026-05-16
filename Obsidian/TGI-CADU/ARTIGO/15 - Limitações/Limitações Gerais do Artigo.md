---
tags: [artigo, limitacoes, critica, metodologia]
created: 2026-05-16
---

# Limitações Gerais do Artigo — EduPredict

[[INDEX - ARTIGO|← Índice]] | [[Análise Crítica do TGI]] | [[Dataset — Estrutura e Geração Sintética]] | [[Débitos Técnicos Identificados]]

> [!NOTE] Esta nota cataloga limitações reconhecidas e não-reconhecidas pelo artigo

---

## 1. Limitações Reconhecidas pelo Artigo

### L1 — Ausência de Frequência/Assiduidade
O dataset não inclui dados de presença. Lima (2021) e Melo (2023) incluem frequência como feature — ela é frequentemente a variável mais preditiva de evasão precoce (um aluno para de comparecer antes de reprovar).

**Impacto:** o sistema não pode detectar o padrão "ausente mas com notas OK" — um sinal crítico de evasão iminente.

### L2 — Ausência de Variáveis Socioeconômicas e Emocionais
Fatores como renda familiar, distância de casa à escola, e bem-estar emocional são preditores de reprovação mas ausentes no dataset. O artigo menciona isso como limitação de privacidade/LGPD.

### L3 — Dataset Sintético
O artigo menciona que os dados são gerados sinteticamente como "limitação esperada de TGI", mas não discute o impacto quantitativo na validade dos resultados.

---

## 2. Limitações NÃO Reconhecidas pelo Artigo

### L4 — Validação Cruzada com Vazamento Intra-Aluno (crítica)
StratifiedKFold divide pares (aluno, matéria) aleatoriamente. O mesmo aluno pode aparecer em treino e teste. Como um aluno com N1=8,0 em Matemática provavelmente tem N1=7,5 em Português, o modelo vaza informação do aluno entre treino e teste.

**Solução:** GroupKFold por aluno_id.
**Impacto estimado:** acurácia real pode ser 2-5% menor.

### L5 — Leakage Indireto de `pct_materias_ok`
Se `pct_materias_ok` é calculada com status_encoded que inclui N4 (leakage), então `pct_materias_ok` carrega leakage indireto não detectado pela correlação de Pearson (r < 0,9).

### L6 — Threshold de Detecção de Leakage Arbitrário
O limiar r > 0,9 não foi validado empiricamente. Uma análise de sensibilidade (0,7; 0,8; 0,85; 0,9; 0,95) deveria ter sido realizada.

### L7 — Hiperparâmetros Não Otimizados
O artigo não documenta se foi feita busca de hiperparâmetros (grid search, random search, Bayesian optimization). Com parâmetros padrão, o RF pode estar sub-ótimo.

### L8 — Ausência de Métricas Adequadas para EWS
A acurácia global (94%) é a métrica principal reportada. Para um sistema de Early Warning, o recall da classe Recuperação (62,2%) e o recall de Reprovado (76,3%) são mais importantes. AUC-ROC e macro-F1 também deveriam ser reportados.

### L9 — Sem Análise de Erros Estrutural
O artigo não analisa qualitativamente os casos onde o modelo erra — que tipos de aluno causam erro? Alunos com trajetória não-linear? Alunos de determinadas séries? Determinadas matérias?

### L10 — Explicabilidade Apenas Global
Feature importance global não justifica predições individuais. Para uso pedagógico real (um professor precisa saber POR QUE aquele aluno específico está em risco), SHAP local é necessário.

---

## 3. Limitações de Escopo (Fora do Artigo mas Relevantes)

### L11 — Sem Protocolo Operacional Definido
O sistema gera predições mas não define:
- Quem recebe os alertas?
- Em qual formato?
- Qual ação é esperada do professor?
- Qual o prazo para resposta?

### L12 — LGPD Não Tratada
O sistema processa dados pessoais de menores de idade sem discutir:
- Base legal para processamento
- Consentimento dos responsáveis
- Direito de acesso e correção
- Retenção e exclusão de dados

### L13 — Sem Validação com Especialistas Pedagógicos
Os thresholds do EWS (avg_risk > 0,7 para Crítico) não foram validados com educadores ou gestores escolares. Podem ser inadequados para a realidade pedagógica.

---

## 4. Matriz de Severidade × Facilidade de Correção

| Limitação | Severidade | Facilidade de Correção |
|---|---|---|
| L4 — Validação intra-aluno | 🔴 Alta | ✅ Fácil (GroupKFold) |
| L5 — Leakage indireto | 🔴 Alta | 🟡 Moderada |
| L8 — Métricas inadequadas | 🟡 Média | ✅ Fácil (adicionar métricas) |
| L1 — Frequência ausente | 🟡 Média | 🔴 Difícil (precisa de novos dados) |
| L10 — Sem SHAP | 🟡 Média | 🟡 Moderada |
| L12 — LGPD | 🟡 Média | 🟡 Moderada |
| L3 — Dataset sintético | 🟡 Média | 🔴 Difícil (coleta de dados reais) |
| L7 — Hiperparâmetros | 🟢 Baixa | ✅ Fácil (grid search) |

---

## Links

- [[Análise Crítica do TGI]]
- [[Dataset — Estrutura e Geração Sintética]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
- [[Detecção Automática por Correlação de Pearson]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Débitos Técnicos Identificados]]
- [[Plano de Artigo ABNT]]
