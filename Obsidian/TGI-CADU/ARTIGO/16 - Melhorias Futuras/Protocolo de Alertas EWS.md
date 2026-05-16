---
tags: [artigo, ews, alertas, protocolo, operacional, melhorias]
created: 2026-05-16
---

# Protocolo de Alertas EWS — Early Warning System

[[INDEX - ARTIGO|← Índice]] | [[M3 — Modelo de Produção (Após N3)]] | [[Comparação M1 M2 M3]] | [[Plano de Artigo ABNT]]

> [!NOTE] O EWS existe no código mas sem protocolo operacional formal — o que fazer após o alerta?

---

## 1. O EWS Atual no EduPredict

O EduPredict implementa 3 níveis de alerta baseados em `avg_risk` (probabilidade média de não-Aprovado):

| Nível | Threshold | Rótulo | Cor |
|---|---|---|---|
| **Crítico** | avg_risk > 0,70 | "🔴 CRÍTICO - Atenção imediata" | Vermelho |
| **Em Risco** | avg_risk > 0,40 | "🟡 EM RISCO - Acompanhamento" | Amarelo |
| **Seguro** | avg_risk ≤ 0,40 | "🟢 SEGURO - Desempenho normal" | Verde |

**Problema:** os thresholds 0,70 e 0,40 são arbitrários — não foram validados com especialistas pedagógicos nem com dados históricos de intervenção.

---

## 2. O Que Falta — Protocolo Operacional Completo

### O sistema atual gera o alerta. O que acontece depois?

O artigo não define:
1. **Quem recebe o alerta?** Professor da matéria? Coordenador? Todos?
2. **Como o alerta é comunicado?** Interface no sistema? Email? WhatsApp?
3. **Qual ação é esperada?** Conversa com o aluno? Reunião com pais? Aula de reforço?
4. **Qual o prazo para resposta?** 48h? 1 semana?
5. **Como registrar que o alerta foi atendido?** Loop de feedback ausente.
6. **O que fazer se o alerta for um falso positivo?** Sem mecanismo de contestação.

---

## 3. Proposta de Protocolo Operacional de 3 Níveis

### Nível 1 — Informativo (avg_risk 0,20-0,40)
- **Ação:** Monitoramento passivo — professor mantém atenção especial
- **Comunicação:** Registro no sistema, sem notificação ativa
- **Prazo:** Reavaliar após N2 ou N3
- **Responsável:** Professor da matéria

### Nível 2 — Atenção (avg_risk 0,40-0,70)
- **Ação:** Contato com aluno + registro de conversa
- **Comunicação:** Notificação ativa ao professor E coordenador
- **Prazo:** Ação em até 5 dias úteis
- **Responsável:** Professor + Coordenador
- **Registro:** Ata de atendimento no sistema

### Nível 3 — Crítico (avg_risk > 0,70)
- **Ação:** Reunião com pais/responsáveis + plano de recuperação personalizado
- **Comunicação:** Notificação ao professor, coordenador E direção
- **Prazo:** Reunião em até 2 semanas
- **Responsável:** Equipe pedagógica completa
- **Registro:** Plano de Atendimento Individual (PAI)

---

## 4. Schema SQL para Registro de Alertas

```sql
CREATE TABLE alertas_ews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    materia_id INTEGER,            -- NULL = alerta geral do aluno
    nivel INTEGER NOT NULL,        -- 1=Informativo, 2=Atenção, 3=Crítico
    avg_risk REAL NOT NULL,        -- valor numérico que gerou o alerta
    modelo_usado TEXT,             -- 'M1', 'M2' ou 'M3'
    gerado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atendido_em TIMESTAMP,
    atendido_por TEXT,
    notas_atendimento TEXT,        -- registro livre do professor
    falso_positivo BOOLEAN DEFAULT 0,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
);

CREATE TABLE planos_atendimento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alerta_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    prazo DATE,
    responsavel TEXT,
    concluido BOOLEAN DEFAULT 0,
    FOREIGN KEY (alerta_id) REFERENCES alertas_ews(id)
);
```

---

## 5. Thresholds — Como Calibrar Melhor

O threshold ideal depende do contexto pedagógico. Para calibrar:

```python
# Análise de curva ROC para threshold ótimo
from sklearn.metrics import roc_curve

# Para a classe "em risco" (Recuperação + Reprovado) vs Aprovado
y_binary = (y != 2).astype(int)  # 1=em risco, 0=aprovado
fpr, tpr, thresholds = roc_curve(y_binary, risk_scores)

# Encontrar threshold que maximiza Youden's J = TPR - FPR
j_scores = tpr - fpr
optimal_idx = j_scores.argmax()
optimal_threshold = thresholds[optimal_idx]
print(f"Threshold ótimo: {optimal_threshold:.2f}")
```

Mas mais importante: **validar com pedagogos** — o threshold matemático ótimo pode não corresponder ao threshold operacionalmente viável (capacidade de atendimento da escola).

---

## 6. Loop de Feedback Docente

O EWS atual é unidirecional (sistema → professor). Um EWS robusto seria bidirecional:

```
Sistema → Gera alerta → Professor
                            ↓
                    Professor avalia
                            ↓
              Confirma risco | Contesta alerta
                            ↓
              Feedback → Retreina modelo periodicamente
```

Isso permitiria ao modelo aprender com os casos onde errou — convergência entre julgamento humano e ML. Ver [[Módulo de Feedback Docente]] no Plano de Artigo.

---

## 7. Considerações LGPD para Alertas

Alertas de risco são dados pessoais sensíveis (informações sobre dificuldades acadêmicas de menores). A LGPD exige:

1. **Base legal:** consentimento dos responsáveis OU legítimo interesse institucional (documentado)
2. **Finalidade específica:** alertas para fins pedagógicos, não de controle disciplinar
3. **Proporcionalidade:** alertas apenas para educadores com necessidade de acesso
4. **Direito de contestação:** aluno/responsável pode questionar a predição
5. **Auditoria:** registro de quem acessou quais alertas

---

## Links

- [[M3 — Modelo de Produção (Após N3)]]
- [[Comparação M1 M2 M3]]
- [[Análise Crítica do TGI]]
- [[Plano de Artigo ABNT]]
- [[LGPD e Ética no EduPredict]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
