---
tags: [artigo, objetivos, hipotese, edupredict]
created: 2026-05-14
---

# Questão de Pesquisa e Objetivos

[[INDEX - ARTIGO|← Índice]] | [[Problema Central e Justificativa]] | [[Classificação e Design da Pesquisa]]

---

## 1. Questão de Pesquisa

> *"É tecnicamente viável utilizar modelos de Machine Learning para predizer desempenho acadêmico e risco de evasão na educação básica, garantindo níveis aceitáveis de acurácia e confiabilidade?"*

### Análise Crítica da Questão

A questão é **bem delimitada** — foca em viabilidade técnica, não em eficácia pedagógica ou impacto real. Isso é apropriado para um TGI, mas limita o escopo das conclusões: o artigo **não responde** se o sistema, uma vez implantado, realmente reduz a evasão.

**O que a questão implicitamente exige:**
- Definir "aceitável": o artigo usa benchmarks da literatura (Lima 2021: 78%, Melo 2023: 82%) como baseline
- Definir "confiabilidade": operacionalizado via validação cruzada 5-fold e F1-Score

**O que a questão não pergunta (oportunidade para extensão):**
- O sistema é usável por professores com pouca experiência em TI?
- A comunicação das predições às famílias é compreensível?
- As intervenções geradas pelos alertas são eficazes?

---

## 2. Objetivo Geral

> *Investigar a viabilidade técnica da utilização de Machine Learning para predição de desempenho acadêmico e identificação de alunos suscetíveis à evasão escolar.*

**Nota:** "investigar a viabilidade técnica" é um objetivo bem calibrado para o nível de graduação. Não propõe implantação em produção, apenas prova de conceito.

---

## 3. Objetivos Específicos (Inferidos do Texto)

O artigo não lista objetivos específicos de forma explícita, mas os seguintes são deduzíveis da estrutura metodológica:

| OE | Descrição | Seção do artigo |
|---|---|---|
| OE1 | Construir base de dados com registros de notas de alunos da educação básica | Seção 3.1 |
| OE2 | Extrair e validar features preditivas a partir dos dados disponíveis | Seção 3.2 |
| OE3 | Implementar pipeline de detecção automática de data leakage | Seção 3.4 |
| OE4 | Treinar três modelos temporais (M1, M2, M3) com diferentes níveis de antecedência | Seção 3.3 |
| OE5 | Avaliar o desempenho dos modelos com métricas robustas (acurácia, F1, CV 5-fold) | Seção 3.6 |

**Gap:** nenhum OE aborda explicabilidade, comunicação de resultados ou conformidade com LGPD.

---

## 4. Hipótese

Implicitamente:

> *Modelos Random Forest treinados com features derivadas de notas bimestrais e contexto acadêmico atingem acurácia superior a 80% na predição de desempenho, superando os benchmarks anteriores da literatura.*

**Resultado:** Hipótese confirmada — M3 atingiu 94,0%, superando Lima 2021 (78%) e Melo 2023 (82%).

---

## 5. Relevância para o Artigo de Extensão

O artigo de extensão ([[Plano de Artigo ABNT]]) **não questiona a viabilidade técnica** — ela já está provada. A questão de pesquisa do artigo de extensão é:

> *"Como deve se comportar operacionalmente um sistema preditivo escolar para gerar valor real, com transparência às famílias e conformidade à LGPD?"*

Isso representa uma evolução natural: de "funciona tecnicamente?" para "como funciona na prática?".

---

## Links

- [[Problema Central e Justificativa]]
- [[Classificação e Design da Pesquisa]]
- [[M3 — Modelo de Produção (Após N3)]] — onde o objetivo é atingido
- [[Análise Crítica do TGI]] — limitações do escopo
