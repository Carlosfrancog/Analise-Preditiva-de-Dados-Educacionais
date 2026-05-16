---
tags: [artigo, limitacoes, lgpd, etica, privacidade, dados]
created: 2026-05-16
---

# LGPD e Ética no EduPredict

[← Índice](<../INDEX - ARTIGO.md>) | [[Limitações Gerais do Artigo]] | [[Velasco 2022 — Análise Crítica de Sistemas EDM]] | [[Análise Crítica do TGI]]

---

## 1. Lacuna Principal

O artigo do EduPredict **não aborda** conformidade com a Lei Geral de Proteção de Dados (Lei 13.709/2018 — LGPD) nem princípios éticos de IA em educação. Esta é uma das lacunas mais críticas identificadas por [[Velasco 2022 — Análise Crítica de Sistemas EDM]].

---

## 2. Dados Processados — Análise LGPD

O EduPredict processa os seguintes dados pessoais de menores:

| Dado | Categoria LGPD | Base legal necessária |
|---|---|---|
| Nome do aluno | Pessoal simples | Contrato/legítimo interesse |
| Notas bimestrais | Pessoal simples | Contrato educacional |
| Série/turma | Pessoal simples | Contrato educacional |
| Predição de reprovação | **Decisão automatizada** | **Exige Art. 20 LGPD** |
| Perfil de risco | **Dado derivado sensível** | Consentimento ou legítimo interesse específico |

### Art. 20 LGPD — Decisões Automatizadas

> "O titular dos dados tem direito a solicitar revisão de decisões tomadas unicamente com base em tratamento automatizado de dados pessoais que afetem seus interesses."

Uma predição de reprovação é uma **decisão automatizada** que afeta diretamente o titular (menor de idade). O sistema **não implementa** nenhum mecanismo de revisão ou contestação.

---

## 3. Princípios Éticos Violados ou Não Endereçados

### 3.1 Transparência (Art. 6º, VI)

O aluno e responsável **não são informados** de que um modelo de ML prediz seu desempenho. Não há:
- Aviso de uso de IA
- Explicação da lógica de predição
- Acesso à predição pelo próprio titular

### 3.2 Direito de Acesso (Art. 18)

O titular pode solicitar:
- Quais dados são processados
- Por quanto tempo são retidos
- Para qual finalidade

O EduPredict não tem mecanismo para atender essas solicitações.

### 3.3 Direito ao Contraditório (Art. 20, §1º)

> "A critério do titular, em caso de decisão automatizada... deverá ser informada a lógica, os critérios e os procedimentos utilizados para a decisão."

Feature importance global (o que o sistema fornece) **não é suficiente** para atender este artigo — é necessária explicabilidade por indivíduo (SHAP por aluno).

---

## 4. Viés Algorítmico — Risco Ético

O modelo é treinado com dados históricos que **reproduzem desigualdades históricas**:

```
Hipótese de viés:
  - Alunos de série 6F têm historicamente mais reprovações no dataset
  - O modelo aprende: serie_num_norm=0.0 → risk_score alto
  - Novo aluno do 6º ano recebe risco elevado automaticamente
  - Professor (inadvertidamente) presta menos atenção a alunos "já condenados"
  → Profecia autorrealizável
```

`serie_num_norm` como feature cria exatamente este risco — comentado em [[serie num norm — Contexto Série]].

---

## 5. Dados de Menores — Atenção Especial

A LGPD (Art. 14) exige **consentimento explícito do responsável legal** para tratamento de dados de crianças e adolescentes:

> "O tratamento de dados pessoais de crianças e adolescentes deverá ser realizado em seu melhor interesse."

O EduPredict usa dados de alunos de 6º Fundamental (11-12 anos) a 3º Médio (17-18 anos) — todos menores. O artigo não menciona coleta de consentimento.

---

## 6. Retenção e Exclusão de Dados

O banco `escola.db` não tem:
- Política de retenção de dados (por quanto tempo os dados ficam?)
- Mecanismo de exclusão por solicitação
- Anonimização após certo período
- Pseudonimização dos identificadores

---

## 7. O Que Seria Necessário para Conformidade Mínima

```
1. Aviso de uso de IA na interface (banner visível)
2. Política de privacidade simplificada (lei exige linguagem acessível)
3. Mecanismo de exportação de dados por aluno
4. SHAP por aluno para justificar predições (Art. 20)
5. Log de acesso às predições (quem viu, quando)
6. Prazo de retenção definido + rotina de exclusão
7. Consentimento dos responsáveis (menores)
```

---

## 8. Ética Além da Lei — Princípios UNESCO/OECD

| Princípio | Status EduPredict |
|---|---|
| Transparência | ❌ Ausente |
| Explicabilidade | ❌ Apenas global |
| Não-discriminação | ⚠️ Risco via serie_num_norm |
| Privacidade | ❌ Não abordado |
| Responsabilidade | ❌ Sem auditoria |
| Contestabilidade | ❌ Sem mecanismo |

---

## Links

- [[Limitações Gerais do Artigo]]
- [[Velasco 2022 — Análise Crítica de Sistemas EDM]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[serie num norm — Contexto Série]]
- [[Análise Crítica do TGI]]
- [[Módulo de Feedback Docente]]
