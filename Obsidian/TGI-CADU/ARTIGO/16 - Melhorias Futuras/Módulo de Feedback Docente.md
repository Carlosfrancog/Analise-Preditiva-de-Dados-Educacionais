---
tags: [artigo, melhorias, feedback, docente, interface]
created: 2026-05-16
---

# Módulo de Feedback Docente

[← Índice](<../INDEX - ARTIGO.md>) | [[Protocolo de Alertas EWS]] | [[SHAP — Explicabilidade Local por Aluno]] | [[LGPD e Ética no EduPredict]]

---

## 1. Problema Atual

O EduPredict é **unidirecional**: o modelo faz predições, o professor vê os resultados, mas não há mecanismo para:
- O professor indicar se a predição foi útil
- O professor registrar que tomou ação pedagógica
- O sistema aprender com o feedback do professor
- Registrar quando uma predição estava errada

Isso cria um sistema que não aprende com o domínio especializado do professor.

---

## 2. O Que É o Módulo de Feedback

Proposta de extensão: uma camada de feedback que permite ao professor registrar:

```
1. "Estou ciente deste aluno" (acknowledges o alerta)
2. "Tomei ação: [conversa / contato família / reforço]"
3. "A predição estava [correta / incorreta / parcialmente correta]"
4. Observação livre: "Aluno tem problema familiar, não é dificuldade acadêmica"
```

---

## 3. Schema de Banco Proposto

```sql
CREATE TABLE feedback_docente (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id      INTEGER NOT NULL,
    materia_id    INTEGER NOT NULL,
    professor_id  INTEGER,  -- futuro: autenticação de professores
    data_feedback DATETIME DEFAULT CURRENT_TIMESTAMP,
    predicao_vista TEXT,    -- snapshot da predição no momento do feedback
    utilidade     INTEGER,  -- 1=útil, 0=não útil, -1=incorreta
    acao_tomada   TEXT,     -- 'conversa'|'familia'|'reforco'|'nenhuma'
    observacao    TEXT,     -- texto livre
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
);

CREATE TABLE acoes_pedagogicas (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id     INTEGER NOT NULL,
    materia_id   INTEGER,
    data_acao    DATE,
    tipo_acao    TEXT,  -- 'reforco_extra'|'conversa'|'contato_familia'|'encaminhamento'
    resultado    TEXT,  -- observação sobre o resultado da ação
    nota_pos_acao REAL, -- nota no bimestre seguinte (preenchida depois)
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
);
```

---

## 4. Interface Proposta na GUI

Cada card de disciplina em `gui_predicoes_improved.py` recebe um botão de feedback:

```
[Card: Matemática — 🔴 CRÍTICO]
  Notas: N1=4.5 | N2=3.8 | slope: ↘
  Predição: Reprovado (94%)
  
  [✓ Ciente] [📝 Registrar Ação] [👍 Útil] [👎 Incorreta]
```

O feedback é armazenado em `feedback_docente` e pode ser consultado em um dashboard de eficácia.

---

## 5. Dashboard de Eficácia do Sistema

Com os dados de feedback coletados, seria possível calcular:

```python
# Métricas de eficácia em produção:
taxa_acerto_real    = feedbacks_uteis / total_feedbacks
taxa_acao_docente   = acoes_tomadas / alertas_criticos_emitidos
impacto_real        = melhora_nota_apos_acao / total_acoes_tomadas
```

Isso permite responder a questão de Velasco (2022): **o sistema melhora o desempenho dos alunos?** — atualmente sem resposta.

---

## 6. Aprendizado Ativo (Active Learning)

Uma versão avançada do módulo permitiria aprendizado ativo:

```python
# Casos em que o professor discordou da predição (modelo estava errado):
discordancias = feedback.filter(utilidade=-1)

# Re-treinar com peso maior para esses casos:
sample_weight = np.ones(len(X_train))
for idx in discordancias.indices:
    sample_weight[idx] = 3.0  # triplo peso para casos onde professor discordou

model.fit(X_train, y_train, sample_weight=sample_weight)
```

Este é um exemplo de **Human-in-the-Loop ML** — o especialista de domínio corrige o modelo iterativamente.

---

## 7. Relação com LGPD

O módulo de feedback cria **novos dados pessoais** (observações sobre alunos específicos por professores identificados). Isso exige:
- Controle de acesso: apenas professores da matéria/turma veem o feedback
- Anonimização para fins de análise agregada
- Direito de acesso: alunos/responsáveis podem ver as observações sobre eles?

Ver: [[LGPD e Ética no EduPredict]]

---

## 8. Compatibilidade com Arquitetura Atual

**Nível de invasividade:** Médio — requer:
1. Nova(s) tabela(s) em `cads.py` → baixo impacto
2. Novo widget em `gui_predicoes_improved.py` → médio impacto
3. Nova página "Dashboard de Eficácia" → novo arquivo GUI

**Pré-requisito:** DT-01 corrigido — feedback sobre predições incorretas só faz sentido se as predições estiverem sendo geradas corretamente.

---

## Links

- [[Protocolo de Alertas EWS]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[LGPD e Ética no EduPredict]]
- [[Compatibilidade Arquitetural]]
- [[gui predicoes improved py — Interface Preditiva]]
- [[Velasco 2022 — Análise Crítica de Sistemas EDM]]
- [[Insights para o Artigo de Extensão]]
