---
tags: [artigo, limitacoes, socioemocional, engajamento, futuro]
created: 2026-05-16
---

# Ausência de Indicadores Socioemocionais

[← Índice](<../INDEX - ARTIGO.md>) | [[Limitações Gerais do Artigo]] | [[Ausência de Frequência como Feature]] | [[Incorporação de Frequência e Engajamento]]

---

## 1. O Que São Indicadores Socioemocionais

Competências socioemocionais (Big Five, SENNA) e indicadores de engajamento escolar que a literatura educacional reconhece como preditores de desempenho acadêmico:

| Categoria | Indicadores | Método de coleta |
|---|---|---|
| **Engajamento comportamental** | Participação em aula, entrega de atividades | Registros da escola |
| **Engajamento cognitivo** | Qualidade das tarefas, notas de caderno | Avaliação docente |
| **Bem-estar socioemocional** | Autoeficácia, motivação, ansiedade de prova | Questionário SENNA |
| **Contexto familiar** | Renda, escolaridade dos pais | Cadastro socioeconômico |
| **Frequência** | % presença por matéria | Sistema de chamada |

---

## 2. Por Que O EduPredict Ignora Esses Indicadores

### Causa Técnica:
O dataset sintético foi gerado com `gerar_notas_aleatorias()` em `cads.py` — apenas notas, sem nenhuma variável socioeconômica ou de engajamento. Não há estrutura de dados para armazenar esses indicadores.

### Causa Conceitual:
O foco do TGI é **predição de desempenho acadêmico a partir de notas**, não modelagem completa de fatores de risco. A escolha é defensável como escopo delimitado, mas precisa ser explicitada como limitação.

### Causa Prática:
Indicadores socioemocionais requerem instrumentos validados (SENNA, SDQ) e consentimento específico para coleta — barreira significativa para um TGI.

---

## 3. Impacto na Qualidade das Predições

### Cenários onde a ausência de indicadores socioemocionais causa erros:

```
Caso 1 — Aluno "invisível ao risco":
  Notas: N1=7.5, N2=7.0, N3=6.8 → modelo prediz "Aprovado" (correto)
  Mas: alto absenteísmo, baixo engajamento, início de bullying
  → O modelo não detecta o risco real de evasão no próximo semestre

Caso 2 — Alerta falso:
  Notas: N1=5.5, N2=5.2, N3=5.0 → modelo prediz "Reprovação"
  Mas: aluno tem alta autoeficácia, situação familiar temporária
  → Predição tecnicamente correta mas o aluno se recupera sozinho no N4

Caso 3 — Contexto econômico:
  Aluno em situação de vulnerabilidade → notas baixas por falta de material/internet
  Modelo aprende correlação notas baixas → reprovação sem entender a causa
  → Intervenção errada (reforço escolar quando a necessidade é assistência social)
```

---

## 4. Indicadores com Maior Potencial de Impacto

Baseado na literatura EDM (Romero e Ventura, 2020):

1. **Frequência escolar** — preditor mais direto (ver [[Ausência de Frequência como Feature]])
2. **Entrega de atividades/tarefas** — engajamento comportamental mensurável
3. **Participação em recuperação paralela** — indicador de proatividade
4. **Histórico de reprovação anterior** — preditor forte para séries avançadas

Esses 4 indicadores são os mais viáveis de coletar em escolas brasileiras sem instrumentos específicos.

---

## 5. O Que Seria Necessário para Incluí-los

```python
# Nova tabela em cads.py:
CREATE TABLE indicadores_socioemocional (
    aluno_id        INTEGER PRIMARY KEY,
    historico_reprov INTEGER DEFAULT 0,  -- nº de reprovações anteriores
    participacao_rec INTEGER DEFAULT 0,  -- 1=sim, 0=não
    entrega_ativid  REAL,    -- % atividades entregues no bimestre
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
);
```

A maior barreira não é técnica mas **operacional**: como coletar e atualizar esses dados regularmente.

---

## Links

- [[Limitações Gerais do Artigo]]
- [[Ausência de Frequência como Feature]]
- [[Incorporação de Frequência e Engajamento]]
- [[Romero e Ventura 2020 — EDM Survey]]
- [[Velasco 2022 — Análise Crítica de Sistemas EDM]]
- [[Insights para o Artigo de Extensão]]
