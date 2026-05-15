---
tags:
  - artigo
  - abnt
  - tgi-codes
  - planejamento
  - pesquisa
created: 2026-05-14
---

# Plano de Anotação Detalhado — Artigo Científico (ABNT)

[[MOC - TGI-CODES|← Índice]] | [[Melhorias 2026-05-14]] | [[Roadmap]]

> [!NOTE] Base do documento
> Fundamentado na leitura analítica de: **GABRIEL, C. E. F.; ROCHA, M. F. P. S.** *EduPredict: Um Sistema Baseado em Machine Learning para Predição de Desempenho e Evasão Escolar.* UNICSUL, 2026. (12 p.)

---

## 1. FICHAMENTO ANALÍTICO DO ARTIGO-BASE

### 1.1 Identificação

| Campo | Conteúdo |
|---|---|
| **Título** | EduPredict: Um Sistema Baseado em Machine Learning para Predição de Desempenho e Evasão Escolar |
| **Autores** | Carlos Eduardo Franco Gabriel (RGM 33060576); Miguel Ferreira Palmieri Souza Rocha (RGM 32818793) |
| **Orientador** | Mestre João Roberto Ursino da Cruz |
| **Instituição** | Universidade Cruzeiro do Sul — UNICSUL |
| **Tipo** | Artigo de graduação (TGI) |
| **Páginas** | 12 |
| **Problema central** | Viabilidade técnica de ML para predição de desempenho e evasão na educação básica |

---

### 1.2 Tese e Questão de Pesquisa

> *"É tecnicamente viável utilizar modelos de Machine Learning para predizer desempenho acadêmico e risco de evasão na educação básica, garantindo níveis aceitáveis de acurácia e confiabilidade?"*

**Resposta do artigo:** Sim — o modelo M3 (Random Forest, 200 árvores, 9 features) atingiu 94,0% de acurácia, superando benchmarks da literatura (Lima 2021: 78%; Melo 2023: 82%).

---

### 1.3 Metodologia — Pontos Críticos

| Aspecto | Dado | Observação crítica |
|---|---|---|
| **Base** | 200 alunos × 13 matérias × 7 séries = 15.613 registros | Dataset sintético/controlado — risco de não generalização |
| **Split** | 80% treino / 20% teste (estratificado) | Correto, mas população pequena |
| **Validação** | CV 5-fold | Adequado |
| **Data leakage** | Detecção automática por correlação de Pearson (limiar 0,9) | Diferencial metodológico relevante |
| **Features removidas** | `media_pond_norm` (r=0,95); `n4_norm` (r=0,91) | Essencial para predição antecipada |
| **Desbalanceamento** | `class_weight='balanced'` no RF | Tratado, mas acurácia de Recuperação ainda baixa (62,2%) |

---

### 1.4 Resultados — Análise Numérica

**Desempenho dos modelos:**

| Modelo | Momento | Features | Acurácia | F1-macro | CV (μ ± σ) |
|---|---|---|---|---|---|
| M1 | Após N1 | 1 | 83,8% | 0,834 | 0,801 ± 0,034 |
| M2 | Após N2 | 4 | 92,5% | 0,925 | 0,886 ± 0,028 |
| M3 | Após N3 | 9 | 94,0% | 0,940 | 0,912 ± 0,018 |

**Acurácia por classe — M3:**

| Classe | Acertos/Total | Acurácia | Análise |
|---|---|---|---|
| Aprovado | 1.284/1.400 | 91,7% | Classe majoritária, melhor desempenho |
| Recuperação | 342/550 | **62,2%** | ⚠ Zona de transição — maior confusão |
| Reprovado | 267/350 | 76,3% | Aceitável, mas intervenção mais urgente |

> [!WARNING] Ponto crítico para o artigo
> A classe **Recuperação** tem 62,2% de acurácia — 37,8% dos casos são classificados erroneamente. Em um sistema real com impacto sobre famílias e alunos, essa taxa de erro na zona de maior intervenção pedagógica é **clinicamente significativa**. O artigo não discute as consequências práticas desse erro.

**Importância das features — M3:**

| Feature | Importância | Interpretação pedagógica |
|---|---|---|
| `n2_norm` | 32,3% | N2 é o principal preditor — 2º bimestre define trajetória |
| `pct_materias_ok` | 21,5% | Desempenho holístico > desempenho isolado por disciplina |
| `slope_notas` | 12,3% | Tendência (trajetória) > nota pontual |
| demais features | ~34% | Contexto complementar |

---

### 1.5 Lacunas Identificadas no Artigo-Base

#### Lacuna 1 — Ausência de indicadores socioemocionais
O artigo reconhece (seção 5.5 e 6) que motivação, ansiedade, suporte familiar e saúde mental não foram incorporados. Isso é particularmente relevante porque a evasão é multidimensional — alunos com notas estáveis podem evadir por fatores externos.

#### Lacuna 2 — Comportamento operacional não definido
O artigo prova viabilidade técnica, mas não responde: **o que acontece quando o modelo emite um alerta?** Qual é o protocolo de intervenção? Quem recebe a notificação? Em quanto tempo? Qual é o fluxo de escalonamento?

#### Lacuna 3 — Ausência de mecanismos de feedback
O sistema é estático: modelos treinados uma vez, sem loop de retorno. Quando um professor discorda da predição, não há forma de corrigir ou retroalimentar o modelo.

#### Lacuna 4 — Transparência com famílias ausente
Nenhuma seção do artigo trata de como as informações preditivas são comunicadas aos responsáveis. Em um sistema com impacto real sobre crianças e adolescentes, a transparência familiar é tanto uma obrigação ética quanto um requisito legal (LGPD — Lei 13.709/2018).

#### Lacuna 5 — Sem dados de frequência
O artigo não incorpora frequência/assiduidade, que é um dos principais preditores de evasão na literatura (Lima, 2021; INEP, 2023). A evasão começa frequentemente pela infrequência antes da reprovação.

#### Lacuna 6 — Explicabilidade limitada
Feature importance (Figura 2) é apresentada apenas a nível global. Não há explicação por aluno/por predição (SHAP local), o que inviabiliza a justificativa individual para educadores e famílias.

---

## 2. TÍTULO E ENQUADRAMENTO DO ARTIGO PROPOSTO

### 2.1 Título

**EduPredict: Comportamento Operacional, Transparência Familiar e Gestão de Informações Estudantis em Sistemas Preditivos de Desempenho Acadêmico**

### 2.2 Subtítulo (opcional)

*Uma extensão arquitetural com módulo de feedback docente e portal de comunicação com responsáveis*

### 2.3 Classificação ABNT NBR 6022

- **Tipo:** Artigo científico original (relato de desenvolvimento e avaliação de sistema)
- **Área:** Ciência da Computação / Informática na Educação
- **Subárea:** Mineração de Dados Educacionais (MDE); Educational Data Mining (EDM)

---

## 3. ESTRUTURA DO ARTIGO (ABNT NBR 6022:2018)

```
1. INTRODUÇÃO
   1.1 Contextualização e justificativa
   1.2 Problema de pesquisa
   1.3 Objetivos (geral e específicos)
   1.4 Organização do artigo

2. REFERENCIAL TEÓRICO
   2.1 Evasão escolar no Brasil: panorama e causas
   2.2 Sistemas preditivos em educação: estado da arte
   2.3 Comportamento operacional de sistemas de alerta
   2.4 Transparência algorítmica e LGPD na educação
   2.5 Comunicação escola-família mediada por tecnologia

3. METODOLOGIA
   3.1 Classificação da pesquisa
   3.2 Arquitetura do sistema proposto (extensão do EduPredict)
   3.3 Módulo de comportamento operacional
   3.4 Módulo de feedback docente
   3.5 Módulo de comunicação familiar
   3.6 Critérios de avaliação

4. DESENVOLVIMENTO
   4.1 Fluxos de decisão do sistema
   4.2 Protocolo de escalonamento de alertas
   4.3 Mecanismo de feedback e retreino
   4.4 Portal de transparência familiar
   4.5 Gestão de consentimento e LGPD

5. ANÁLISE E DISCUSSÃO
   5.1 Impacto do feedback no desempenho dos modelos
   5.2 Usabilidade: perspectiva docente
   5.3 Aceitação: perspectiva familiar
   5.4 Implicações éticas e legais
   5.5 Limitações

6. CONSIDERAÇÕES FINAIS
   6.1 Conclusões
   6.2 Contribuições
   6.3 Trabalhos futuros

REFERÊNCIAS
APÊNDICES
```

---

## 4. DESENVOLVIMENTO TEÓRICO POR SEÇÃO

### SEÇÃO 1 — INTRODUÇÃO

#### 1.1 Contextualização e Justificativa

**Argumento central a desenvolver:**

O artigo-base (GABRIEL; ROCHA, 2026) demonstrou a viabilidade técnica do EduPredict com acurácia de 94,0% no modelo M3. Entretanto, um sistema preditivo só gera valor real quando seu comportamento operacional é definido — ou seja, quando se especifica **o que o sistema faz com cada predição**, **quem recebe cada informação** e **como o resultado do modelo se traduz em ação pedagógica**.

Além disso, sistemas que operam sobre dados de crianças e adolescentes em contexto escolar estão sujeitos à **Lei Geral de Proteção de Dados — LGPD (Lei 13.709/2018)**, ao **Estatuto da Criança e do Adolescente — ECA (Lei 8.069/1990)** e às diretrizes do **Conselho Nacional de Educação (CNE)**. A ausência de um protocolo claro de governança de dados e comunicação familiar em sistemas preditivos escolares constitui uma lacuna técnica e ética relevante.

**Dado de abertura sugerido:**
> "Segundo o INEP (2023), aproximadamente 8% dos alunos do Ensino Médio abandonam os estudos antes da conclusão. Modelos preditivos com 94,0% de acurácia existem (GABRIEL; ROCHA, 2026), mas um sistema tecnicamente funcional é eticamente incompleto sem definir quem recebe cada alerta, quando, como e com qual base de justificativa."

#### 1.2 Problema de Pesquisa

> *"Como deve se comportar operacionalmente um sistema preditivo escolar, garantindo transparência às famílias, mecanismos de feedback docente e conformidade com a LGPD, sem comprometer a acurácia e a confiança dos modelos?"*

#### 1.3 Objetivos

**Objetivo Geral:**
Propor e especificar a arquitetura operacional de extensão do EduPredict, contemplando fluxos de decisão, módulo de feedback docente e portal de comunicação familiar com conformidade à LGPD.

**Objetivos Específicos:**
1. Definir protocolo de escalonamento de alertas por nível de risco (informativo, atenção, crítico)
2. Especificar mecanismo de feedback docente para correção e retreino incremental dos modelos
3. Projetar módulo de comunicação familiar com granularidade de informação controlada por perfil
4. Avaliar implicações éticas e legais da exposição de predições ML a responsáveis legais
5. Validar a proposta com simulação de cenários de uso real

---

### SEÇÃO 2 — REFERENCIAL TEÓRICO

#### 2.1 Evasão Escolar no Brasil — Panorama e Causas

**Conteúdo a desenvolver:**

- Dados do INEP (2023): 8% de evasão no Ensino Médio
- Multidimensionalidade da evasão: não é apenas acadêmica — fatores socioeconômicos, familiares, territoriais
- Relação entre infrequência → baixo desempenho → evasão (cadeia causal)
- Diferença entre evasão, abandono, transferência e distorção idade-série

**Referências-chave:**
- INEP (2023) — Censo Escolar
- UNESCO (2022) — Global Education Monitoring Report
- ARROYO, M. G. (2000) — Fracasso-Sucesso: o peso da cultura escolar

#### 2.2 Sistemas Preditivos em Educação — Estado da Arte

**Conteúdo a desenvolver:**

Síntese evolutiva das abordagens:

| Geração | Período | Abordagem | Limitação |
|---|---|---|---|
| 1ª | 2010-2015 | Regras estáticas de limiar (ex: frequência < 75%) | Baixa sensibilidade, muitos falsos negativos |
| 2ª | 2015-2020 | ML supervisionado (RF, SVM, regressão logística) | Caixa-preta, sem explicabilidade |
| 3ª | 2020-hoje | ML + explicabilidade (SHAP, LIME) + feedback | Em desenvolvimento — foco deste artigo |

**Diferencial do EduPredict frente à literatura:**
- Detecção automática de data leakage (único na literatura consultada)
- Três modelos temporais com diferentes níveis de antecedência
- Lacuna: ausência de operacionalização pós-predição

#### 2.3 Comportamento Operacional de Sistemas de Alerta

> [!IMPORTANT] Núcleo da contribuição do artigo
> Esta subseção fundamenta a principal contribuição — definir como o sistema SE COMPORTA após emitir uma predição.

**Conteúdo a desenvolver:**

**Conceito de Early Warning System (EWS):**
Sistemas de alerta precoce (EWS) são estruturas que não apenas identificam risco, mas definem **níveis de resposta** proporcionais ao nível de risco identificado. Na literatura de saúde pública (NEWS score) e aviação (TCAS), EWS são padronizados com protocolos rígidos. Na educação, essa padronização ainda é incipiente.

**Tipologia de alertas proposta:**

| Nível | Trigger | Receptor | Ação | Prazo |
|---|---|---|---|---|
| **🟢 Informativo** | M1: risco baixo | Professor da disciplina | Monitoramento passivo — nenhuma ação obrigatória | — |
| **🟡 Atenção** | M2: Recuperação prevista | Professor + coordenação pedagógica | Reunião de acompanhamento, reforço direcionado | 5 dias úteis |
| **🔴 Crítico** | M3: Reprovação ou slope negativo acelerado | Professor + coordenação + família | Reunião presencial com responsável, plano de ação individual | 48 horas |

**Protocolo de escalonamento (Escalation Protocol):**

```
Evento: aluno classificado como Reprovado (M3, confiança ≥ 70%)
    ↓
PASSO 1: Sistema registra alerta no histórico do aluno
    ↓
PASSO 2: Notificação automática ao professor responsável pela disciplina
    ↓
PASSO 3: Professor confirma ou contesta (janela: 48h)
    ├── Contesta → feedback registrado, modelo marcado para retreino
    └── Confirma ou não responde → escala para coordenação
    ↓
PASSO 4: Coordenação valida e define intervenção
    ↓
PASSO 5: Comunicação à família (módulo transparência)
    ↓
PASSO 6: Registro da ação tomada no histórico (auditoria)
    ↓
PASSO 7: Reavaliação após N2/N3 seguinte — fechar o loop
```

**Nota metodológica:** O sistema NÃO deve agir autonomamente sobre alunos — toda decisão pedagógica é humana. O ML é ferramenta de apoio à decisão (Decision Support System), não de substituição do julgamento docente.

#### 2.4 Transparência Algorítmica e LGPD na Educação

**Conteúdo a desenvolver:**

**LGPD (Lei 13.709/2018) — Bases legais relevantes:**

| Artigo | Conteúdo | Implicação para o EduPredict |
|---|---|---|
| Art. 7º, inciso IX | Legítimo interesse do controlador | A escola pode processar dados para fins pedagógicos |
| Art. 14 | Dados de crianças e adolescentes exigem consentimento dos pais | Todo aluno menor precisa de consentimento parental explícito |
| Art. 20 | Direito à revisão de decisões automatizadas | Pais/alunos podem contestar classificações do modelo |
| Art. 46-49 | Segurança dos dados | Criptografia, controle de acesso, log de auditoria |

**Princípio da transparência algorítmica:**
Sistemas que produzem classificações com impacto sobre pessoas devem ser capazes de explicar — em linguagem acessível ao público-alvo — **por que** aquela classificação foi atribuída. Para o EduPredict, isso significa:
- Para professores: feature importance local (SHAP) por aluno/disciplina
- Para famílias: tradução em linguagem natural ("Seu filho teve queda nas notas de Matemática no 2º bimestre e a tendência é de piora")

**Referências:**
- BRASIL (2018) — Lei 13.709/2018 (LGPD)
- BRASIL (1990) — Lei 8.069/1990 (ECA), Art. 53, 54, 55
- FLORIDI, L. et al. (2018) — AI4People: An Ethical Framework for a Good AI Society
- DOSHI-VELEZ, F.; KIM, B. (2017) — Towards a rigorous science of interpretable machine learning

#### 2.5 Comunicação Escola-Família Mediada por Tecnologia

**Conteúdo a desenvolver:**

A literatura em pedagogia e psicologia educacional indica que o **envolvimento familiar** é um dos mais fortes preditores de sucesso escolar (EPSTEIN, 2001; CASTRO; REGATTIERI, 2009). Entretanto, a comunicação escola-família frequentemente é reativa (após o problema) e assimétrica (informação flui só da escola para a família).

**Proposta: comunicação proativa, gradual e bidirecional**

| Dimensão | Comunicação reativa (atual) | Comunicação proativa (proposta) |
|---|---|---|
| **Timing** | Após reprovação/reunião de conselho | Antes — durante o bimestre, quando ainda é possível intervir |
| **Conteúdo** | Nota final, frequência | Tendência, prognóstico, ação recomendada |
| **Canal** | Reunião presencial, bilhete | Portal digital + SMS/WhatsApp + reunião presencial (para casos críticos) |
| **Direção** | Escola → família | Escola → família E família → escola (canal de retorno) |
| **Linguagem** | Técnica/pedagógica | Acessível, sem jargão — tradução do ML para PT-BR simples |

---

### SEÇÃO 3 — METODOLOGIA

#### 3.1 Classificação da Pesquisa

- **Natureza:** Aplicada
- **Abordagem:** Quali-quantitativa
- **Objetivos:** Exploratória e descritiva (especificação de sistema) + avaliativa (simulação)
- **Procedimentos:** Pesquisa bibliográfica + prototipagem de software + avaliação por cenários

#### 3.2 Arquitetura do Sistema Proposto

**Extensão da arquitetura original (GABRIEL; ROCHA, 2026):**

```
CAMADA DE DADOS
├── escola.db (SQLite)                ← existente
├── ml_features (tabela)             ← existente
├── alertas (tabela nova)            ← NOVO
├── feedback_docente (tabela nova)   ← NOVO
├── consentimentos (tabela nova)     ← NOVO
└── comunicacoes_familia (tabela)    ← NOVO

CAMADA ML
├── RF_M1, RF_M2, RF_M3             ← existente
├── motor_retreino.py                ← NOVO
└── explicabilidade.py (SHAP)       ← NOVO

CAMADA DE SERVIÇOS
├── alerta_service.py                ← NOVO — disparo e escalonamento
├── feedback_service.py              ← NOVO — coleta e processamento
└── notificacao_service.py           ← NOVO — comunicação multicanal

CAMADA DE INTERFACE
├── 03-GUI/ (existente)              ← existente + melhorias
├── portal_familia/ (web)            ← NOVO — módulo web
└── api_rest/ (Flask)               ← NOVO — backend do portal
```

#### 3.3 Módulo de Comportamento Operacional — Especificação

**Tabela `alertas` (novo schema):**

```sql
CREATE TABLE alertas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id        INTEGER NOT NULL,
    materia_id      INTEGER,           -- NULL = alerta global
    modelo_usado    TEXT NOT NULL,     -- 'RF_M1', 'RF_M2', 'RF_M3'
    status_predito  INTEGER NOT NULL,  -- 0=Reprovado, 1=Recuperação, 2=Aprovado
    confianca       REAL NOT NULL,     -- probabilidade da classe predita (0-1)
    nivel_alerta    TEXT NOT NULL,     -- 'informativo', 'atencao', 'critico'
    criado_em       TEXT NOT NULL,     -- ISO 8601
    confirmado_por  INTEGER,           -- professor_id que confirmou
    contestado_por  INTEGER,           -- professor_id que contestou
    status_alerta   TEXT DEFAULT 'aberto', -- 'aberto', 'confirmado', 'contestado', 'fechado'
    acao_tomada     TEXT,              -- registro da intervenção pedagógica
    fechado_em      TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
);
```

**Regras de negócio para disparo de alertas:**

```python
def definir_nivel_alerta(status_predito, confianca, slope_notas):
    """
    Classificação de nível de alerta com base em:
    - status predito pelo modelo
    - confiança da predição
    - tendência (slope) das notas
    """
    if status_predito == 0:  # Reprovado
        if confianca >= 0.80 or slope_notas < -0.3:
            return 'critico'
        return 'atencao'

    if status_predito == 1:  # Recuperação
        if slope_notas < -0.2:  # Em queda mesmo em recuperação
            return 'atencao'
        return 'informativo'

    if status_predito == 2:  # Aprovado
        if slope_notas < -0.3:  # Tendência de queda preocupante
            return 'informativo'
        return None  # Sem alerta — aluno está bem
```

#### 3.4 Módulo de Feedback Docente — Especificação

**Objetivo:** Criar um loop de aprendizado contínuo onde o julgamento docente retroalimenta o modelo.

**Tabela `feedback_docente`:**

```sql
CREATE TABLE feedback_docente (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    alerta_id       INTEGER NOT NULL,
    professor_id    INTEGER NOT NULL,
    status_real     INTEGER,     -- 0/1/2 — classificação do professor
    justificativa   TEXT,        -- texto livre
    fator_externo   TEXT,        -- 'familiar', 'saude', 'bullying', 'financeiro', 'outro'
    criado_em       TEXT NOT NULL,
    usado_treino    INTEGER DEFAULT 0,  -- 0=não, 1=já incluído no retreino
    FOREIGN KEY (alerta_id) REFERENCES alertas(id)
);
```

**Protocolo de retreino incremental:**

```
1. Acumular feedbacks até atingir N=50 novos registros contestados
2. Validar inconsistências (professor A diz aprovado, modelo diz reprovado + nota 4.0 → descartar feedback)
3. Adicionar registros validados ao dataset de treino
4. Retreinar RF_M3 com dataset expandido
5. Avaliar: acurácia do novo modelo ≥ acurácia do modelo anterior - 1%
6. Se OK → substituir modelo em produção; se não → manter modelo anterior e registrar
7. Notificar coordenação: "Modelo atualizado — precisão melhorou de X% para Y%"
```

**Nota importante:** O feedback de fatores externos (`fator_externo`) captura o que o modelo não consegue ver (problema familiar, bullying, saúde) e cria um **vetor explicativo alternativo** para casos onde ML errou por razão legítima.

#### 3.5 Módulo de Comunicação Familiar — Especificação

**Princípios de design:**

1. **Progressividade:** a família recebe informação proporcional ao nível de risco — sem alarmar desnecessariamente
2. **Acionabilidade:** toda comunicação inclui o que a família pode FAZER, não apenas o diagnóstico
3. **Bidireionalidade:** a família pode reportar fatores externos (doença, mudança de cidade, problema em casa)
4. **Acessibilidade:** linguagem simples, sem jargão técnico, disponível em PT-BR
5. **Consentimento:** toda coleta de dados e comunicação é baseada em consentimento documentado

**Fluxo de comunicação por nível de alerta:**

```
ALERTA INFORMATIVO → Nenhuma comunicação à família (professor monitora)

ALERTA ATENÇÃO →
  • E-mail/SMS automático ao responsável:
    "Olá, [nome do responsável]. Identificamos que [nome do aluno]
     está com desempenho abaixo do esperado em [disciplina].
     Recomendamos acompanhar as atividades em casa e,
     se precisar, agendar uma conversa com o professor."
  • Portal: acesso ao histórico de notas e tendência (gráfico simples)
  • Botão: "Quero conversar com o professor" → agenda online

ALERTA CRÍTICO →
  • Telefonema pelo coordenador (registrado no sistema)
  • Portal: plano de ação individualizado visível ao responsável
  • Formulário: família relata fatores externos relevantes
  • Agendamento obrigatório de reunião presencial (confirmação em 24h)
```

**Granularidade de informação para famílias:**

| O que mostrar | O que NÃO mostrar | Por quê |
|---|---|---|
| Notas por disciplina (N1, N2, N3) | Peso exato de cada feature no modelo | Não agrega valor e pode confundir |
| Tendência em linguagem natural ("melhorando", "estável", "em queda") | Score de probabilidade (ex: 73,4%) | Percentual sem contexto é mal interpretado |
| Ação recomendada concreta | Comparação com outros alunos | Violação de privacidade e estigmatização |
| Canal de retorno para a escola | Log interno de alertas e feedbacks docentes | Dado operacional interno |

#### 3.6 Critérios de Avaliação do Sistema Proposto

| Dimensão | Métrica | Meta |
|---|---|---|
| **Acurácia ML** | Acurácia M3 pós-feedback | ≥ 94,0% (baseline artigo-base) |
| **Cobertura de alertas** | % de alunos reprovados detectados com ≥ 1 alerta prévio | ≥ 80% |
| **Tempo de resposta docente** | Mediana de tempo para confirmação/contestação | ≤ 48 horas |
| **Conformidade LGPD** | Checklist de 12 requisitos obrigatórios | 100% |
| **Usabilidade** | SUS (System Usability Scale) — docentes | ≥ 70 pontos |
| **Satisfação familiar** | Likert 5 pontos — clareza da informação | ≥ 4,0/5,0 |

---

### SEÇÃO 4 — DESENVOLVIMENTO

#### 4.1 Fluxo de Decisão Completo do Sistema

**Diagrama de fluxo (descrever textualmente para o artigo):**

```
[BIMESTRE INICIA]
       ↓
[Professor lança N1]
       ↓
[Sistema gera features → RF_M1 prediz]
       ↓
[Nível INFORMATIVO → professor vê dashboard → nenhuma ação obrigatória]
       ↓
[Professor lança N2]
       ↓
[Sistema gera features → RF_M2 prediz]
       ↓
[Nível ATENÇÃO?]
   Sim → [Notifica professor → Professor confirma/contesta → Se confirmado: notifica coordenação → Coordenação define reforço → Notifica família (e-mail)]
   Não → [Continua monitoramento]
       ↓
[Professor lança N3]
       ↓
[Sistema gera features → RF_M3 prediz]
       ↓
[Nível CRÍTICO?]
   Sim → [Notifica professor + coordenação + família → Reunião presencial → Plano individual → Registro de ação]
   Não → [Alerta informativo ou nenhum]
       ↓
[Professor lança N4 → resultado real conhecido]
       ↓
[Sistema compara predição M3 com resultado real]
       ↓
[Registra acerto/erro → Acumula para retreino]
       ↓
[A cada 50 novos registros → retreino incremental]
       ↓
[BIMESTRE ENCERRA → loop reinicia]
```

#### 4.2 Portal Familiar — Telas Especificadas

**Tela 1 — Visão Geral do Filho (Dashboard):**
```
┌─────────────────────────────────────────────────────────┐
│  Olá, [Nome do Responsável]                             │
│  Acompanhamento de [Nome do Aluno] — 8º Fundamental     │
├─────────────────────────────────────────────────────────┤
│  STATUS GERAL:  🟡 ATENÇÃO — 3 disciplinas monitoradas  │
├───────────────┬─────────────────────────────────────────┤
│ MATEMÁTICA    │ ████░░░░░░  N1: 6.0  N2: 4.5  N3: —    │
│               │ Tendência: ↘ Em queda                   │
│               │ [Ver detalhes] [Falar com professor]    │
├───────────────┼─────────────────────────────────────────┤
│ PORTUGUÊS     │ ███████░░░  N1: 7.5  N2: 7.0  N3: —    │
│               │ Tendência: → Estável                    │
├───────────────┼─────────────────────────────────────────┤
│ HISTÓRIA      │ ██████████  N1: 8.0  N2: 8.5  N3: —    │
│               │ Tendência: ↗ Melhorando                 │
└───────────────┴─────────────────────────────────────────┘
│ [Reportar situação familiar]  [Agendar reunião]         │
└─────────────────────────────────────────────────────────┘
```

**Tela 2 — Formulário de Reporte Familiar (canal de retorno):**

```
Você percebeu algo que pode estar afetando o desempenho do seu filho?
Compartilhe com a escola de forma confidencial.

( ) Problemas de saúde (do aluno ou familiar)
( ) Mudança na rotina familiar (mudança de casa, trabalho dos pais)
( ) Dificuldade com conteúdo específico
( ) Situação de bullying ou conflito com colegas
( ) Outros: _______________

Descreva brevemente (opcional):
[_________________________________________________]

[Enviar para a coordenação — confidencial]
```

> [!TIP] Por que isso é importante metodologicamente
> O formulário de reporte familiar captura **dados socioemocionais estruturados** — exatamente a lacuna identificada no artigo-base (Seção 5.5). Esses dados alimentam a tabela `feedback_docente.fator_externo` e, no médio prazo, podem se tornar features adicionais do modelo.

#### 4.3 Gestão de Consentimento — LGPD

**Formulário de consentimento informado (estrutura):**

```
TERMO DE CONSENTIMENTO PARA USO DE DADOS EDUCACIONAIS
(Art. 14, Lei 13.709/2018 — LGPD)

Finalidade do tratamento:
Os dados de desempenho do estudante serão processados por algoritmos
de aprendizado de máquina com o objetivo exclusivo de:
  (a) identificar precocemente riscos de reprovação ou evasão;
  (b) orientar intervenções pedagógicas direcionadas;
  (c) comunicar situações de risco ao responsável legal.

Dados coletados: notas bimestrais (N1 a N4), série escolar, turma.
Dados NÃO coletados: localização, dados biométricos, dados financeiros.

Compartilhamento: dados NÃO são compartilhados com terceiros.
Retenção: dados retidos durante o período letivo + 5 anos (RES. CFE).
Direitos: acesso, correção, exclusão, revisão de decisão automatizada.

Contato do Encarregado (DPO): [e-mail da escola]

[  ] Concordo com o uso dos dados conforme descrito acima.
[  ] Não concordo — o aluno será excluído do sistema preditivo.

Assinatura do responsável: _______________  Data: ___/___/______
```

---

### SEÇÃO 5 — ANÁLISE E DISCUSSÃO

#### 5.1 Impacto do Feedback no Desempenho dos Modelos

**Hipótese a testar:**
Modelos retreinados com feedback docente tendem a:
1. Melhorar acurácia na classe "Recuperação" (atualmente 62,2%) — por capturar contextos não disponíveis nas features originais
2. Reduzir falsos positivos críticos (alunos classificados como Reprovado que estavam bem)

**Abordagem experimental:**
- Simulação com dataset sintético de 500 feedbacks docentes
- Comparar acurácia M3 original vs M3 pós-feedback (5 ciclos de retreino)
- Medir variação específica na classe Recuperação

#### 5.2 Implicações Éticas — Discussão

**Pontos obrigatórios a abordar:**

1. **Risco de estigmatização:** um aluno classificado como "em risco" pode ser tratado diferentemente por professores (*efeito Pigmalião* inverso). Mitigação: alertas são informativos, não prescritivos; ação é sempre decisão humana.

2. **Viés algorítmico:** se o dataset histórico contém viés socioeconômico (alunos pobres são mais reprovados), o modelo aprende esse padrão e o perpetua. Mitigação: monitorar métricas de equidade (acurácia por subgrupo); incorporar variáveis de contexto social.

3. **Confiança excessiva:** educadores podem aceitar predições sem questionar (*automation bias*). Mitigação: interface sempre mostra incerteza do modelo (probabilidade + IC); protocolo exige confirmação humana.

4. **Exclusão digital:** famílias sem acesso à internet não conseguem usar o portal. Mitigação: SMS como canal alternativo; boletim físico impresso com síntese da análise preditiva.

---

## 5. REFERÊNCIAS BIBLIOGRÁFICAS (ABNT NBR 6023:2018)

> Ordenadas alfabeticamente pelo sobrenome do primeiro autor.

BREIMAN, L. **Random Forests**. *Machine Learning*, v. 45, n. 1, p. 5-32, 2001.

BRASIL. **Lei n. 8.069, de 13 de julho de 1990**. Dispõe sobre o Estatuto da Criança e do Adolescente. *Diário Oficial da União*, Brasília, DF, 16 jul. 1990.

BRASIL. **Lei n. 13.709, de 14 de agosto de 2018**. Lei Geral de Proteção de Dados Pessoais (LGPD). *Diário Oficial da União*, Brasília, DF, 15 ago. 2018.

CASTRO, J. M.; REGATTIERI, M. **Interação escola-família: subsídios para práticas escolares**. Brasília: UNESCO/MEC, 2009.

DOSHI-VELEZ, F.; KIM, B. Towards a rigorous science of interpretable machine learning. *arXiv*, 2017. Disponível em: https://arxiv.org/abs/1702.08608.

EPSTEIN, J. L. **School, family, and community partnerships: Preparing educators and improving schools**. Boulder: Westview Press, 2001.

FLORIDI, L. et al. An ethical framework for a good AI society: Opportunities, risks, principles, and recommendations. *Minds and Machines*, v. 28, n. 4, p. 689-707, 2018.

GABRIEL, C. E. F.; ROCHA, M. F. P. S. **EduPredict: Um Sistema Baseado em Machine Learning para Predição de Desempenho e Evasão Escolar**. São Paulo: Universidade Cruzeiro do Sul, 2026. (Artigo de TGI, Coordenação de Tecnologia).

INEP — INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA. **Microdados do Censo Escolar da Educação Básica**. Brasília: INEP, 2023.

LIMA, A. C. **Mineração de dados educacionais e Machine Learning para análise e prevenção da evasão escolar em um curso de graduação**. Dissertação (Mestrado em Sistemas e Computação) — Universidade Federal do Rio Grande do Norte, Natal, 2021.

LUNDBERG, S. M.; LEE, S. I. A unified approach to interpreting model predictions. In: **Advances in Neural Information Processing Systems (NeurIPS)**, 31., 2017, p. 4765-4774.

MELO, H. R. **MAPEA: Modelo de Análise Preditiva de Estímulos de Aprendizagem**. Tese (Doutorado em Ciências) — Universidade de São Paulo, São Paulo, 2023.

ROMERO, C.; VENTURA, S. Educational data mining and learning analytics: An updated survey. *Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery*, v. 10, n. 3, e1355, 2020.

VELASCO, Y. C. R. Predição de dificuldades educacionais: uma análise crítica do uso de dados e algoritmos no apoio ao ensino. *Revista Internacional Integralize Scientific*, 2022.

---

## 6. APÊNDICES PLANEJADOS

### Apêndice A — Checklist LGPD para Sistemas Preditivos Escolares (12 itens)
### Apêndice B — Schema completo do banco de dados estendido (DDL SQL)
### Apêndice C — Questionário SUS adaptado para docentes
### Apêndice D — Roteiro de entrevista com coordenadores pedagógicos
### Apêndice E — Mockups do portal familiar (telas completas)
### Apêndice F — Pseudocódigo do motor de retreino incremental

---

## 7. CRONOGRAMA SUGERIDO

| Fase | Atividade | Duração estimada |
|---|---|---|
| 1 | Revisão bibliográfica complementar (LGPD, EWS, transparência) | 2 semanas |
| 2 | Especificação técnica completa dos módulos | 1 semana |
| 3 | Implementação do módulo de alertas e feedback | 3 semanas |
| 4 | Implementação do portal familiar (prototipo) | 3 semanas |
| 5 | Simulação com dataset sintético + avaliação | 2 semanas |
| 6 | Redação do artigo (ABNT) | 3 semanas |
| 7 | Revisão e submissão | 1 semana |
| **Total** | | **~15 semanas** |

---

## 8. PALAVRAS-CHAVE SUGERIDAS

`Machine Learning` · `Evasão Escolar` · `Sistema de Alerta Precoce` · `Transparência Algorítmica` · `LGPD` · `Comunicação Escola-Família` · `Feedback Docente` · `Random Forest` · `Mineração de Dados Educacionais` · `Explicabilidade`

---

## Links Internos

- [[Visão Geral ML]] — arquitetura dos modelos M1/M2/M3
- [[Features e Cálculos]] — features usadas nos modelos
- [[Data Leakage]] — mecanismo de detecção implementado
- [[gui_predicoes_improved.py]] — módulo de predições atual
- [[gui_ml_integration.py]] — integração ML com a interface
- [[Melhorias 2026-05-14]] — melhorias recentes na interface
- [[Roadmap]] — próximos passos do projeto
