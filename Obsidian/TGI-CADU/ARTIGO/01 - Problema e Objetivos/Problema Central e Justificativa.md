---
tags: [artigo, problema, justificativa, evasao, edupredict]
created: 2026-05-14
---

# Problema Central e Justificativa

[[INDEX - ARTIGO|← Índice ARTIGO]] | [[Questão de Pesquisa e Objetivos]] | [[Evasão Escolar no Brasil]]

---

## 1. O Problema Real

A evasão escolar na educação básica brasileira é um fenômeno estrutural que impede o progresso socioeconômico de milhões de indivíduos. Segundo o **INEP (2023)**, aproximadamente **8% dos alunos do Ensino Médio abandonam os estudos antes da conclusão** — índice que se agrava em regiões economicamente desfavorecidas.

O custo desse fenômeno é duplo:
1. **Individual:** perda de capital humano, menor renda ao longo da vida, vulnerabilidade social
2. **Social:** menor produtividade econômica, maior demanda por programas assistenciais, ciclo de pobreza intergeracional

> [!WARNING] Por que esse número é subestimado
> Os 8% referem-se apenas ao Ensino Médio. Incluindo o Ensino Fundamental II, a taxa de abandono acumulada ao longo da vida escolar é significativamente maior. A distorção idade-série (alunos que repetem anos) amplifica ainda mais o problema, pois alunos em distorção têm probabilidade 3,4× maior de evadir (ARROYO, 2000).

---

## 2. A Oportunidade de ML

**O momento crítico de intervenção é anterior ao abandono.** Estudos indicam que a trajetória de evasão começa a se manifestar **1 a 2 bimestres antes** do abandono efetivo, através de:
- Queda progressiva de notas (slope negativo)
- Infrequência crescente
- Reprovação em disciplinas-chave

Se um sistema detecta esses sinais cedo o suficiente, intervenções personalizadas são possíveis — reforço escolar, suporte familiar, encaminhamentos sociais.

**O problema técnico:** até 2020, a identificação de alunos em risco dependia da experiência subjetiva do professor. Não havia um sistema automatizado capaz de processar os dados já disponíveis no sistema escolar (notas bimestrais, histórico de turma, série) e gerar alertas precoces com fundamentação quantitativa.

---

## 3. Por Que Não Foi Resolvido Antes?

| Barreira | Descrição |
|---|---|
| **Dados fragmentados** | Notas em papel, Excel ou sistemas isolados sem API |
| **Falta de volume** | Modelos de ML requerem mínimo de centenas de amostras por classe |
| **Ausência de padronização** | Critérios de aprovação variam entre escolas, municípios e redes |
| **Data leakage não detectado** | Estudos anteriores usavam features derivadas do target → acurácia inflada artificialmente |
| **Falta de explicabilidade** | Modelos de caixa-preta não eram aceitos por gestores educacionais |

---

## 4. Contribuição do EduPredict

O EduPredict endereça especificamente as barreiras de **dados fragmentados** (centralizando em SQLite), **data leakage** (detecção automática por correlação de Pearson) e **volume** (15.613 registros gerados a partir de 200 alunos × 13 matérias).

O artigo **não endereça** explicabilidade (SHAP não implementado) nem padronização de critérios entre instituições.

---

## 5. Impacto no Projeto Atual

O `cads.py` já implementa a centralização de dados em SQLite (`escola.db`). A estrutura de tabelas (`alunos`, `materias`, `notas`, `ml_features`) resolve diretamente o problema de fragmentação identificado como barreira histórica.

**O que ainda falta:** o sistema atual não tem protocolo de intervenção após a predição — ele prediz, mas não define o que acontece depois. Ver [[Plano de Artigo ABNT]] para o protocolo de escalonamento proposto.

---

## 6. Análise Crítica

> [!CRITICAL] Limitação conceitual não discutida no artigo
> O artigo trata evasão e reprovação como sinônimos operacionais (ambos resultam em classificação negativa), mas são fenômenos distintos:
> - **Reprovação:** aluno permanece na escola, mas não progride de série
> - **Evasão:** aluno abandona o sistema escolar completamente
>
> O dataset usou notas para definir labels (Aprovado/Recuperação/Reprovado), o que detecta **risco de reprovação**, não diretamente **risco de evasão**. A correlação entre os dois existe, mas não é discutida metodologicamente. Esse é um gap conceitual que o artigo de extensão deve abordar.

---

## Links Relacionados

- [[Questão de Pesquisa e Objetivos]] — hipótese e OE
- [[Evasão Escolar no Brasil]] — dados e causas
- [[Limitações Gerais do Artigo]] — o que ficou de fora
- [[Análise Crítica do TGI]] — avaliação completa
- [[Dataset — Estrutura e Origem]] — como os dados foram coletados
