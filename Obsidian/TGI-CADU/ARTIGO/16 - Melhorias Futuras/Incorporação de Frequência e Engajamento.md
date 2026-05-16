---
tags: [artigo, melhorias, frequencia, engajamento, features, futuro]
created: 2026-05-16
---

# Incorporação de Frequência e Engajamento

[[INDEX - ARTIGO|← Índice]] | [[Limitações Gerais do Artigo]] | [[Análise Comparativa dos Trabalhos]] | [[Plano de Artigo ABNT]]

> [!NOTE] A melhoria de maior impacto potencial no EduPredict — frequência é o preditor mais precoce de evasão

---

## 1. Por Que Frequência é Crítica

Lima (2021) e Melo (2023) incluem frequência como feature — e ela é frequentemente a variável mais preditiva de evasão escolar precoce:

**Padrão típico de aluno em evasão:**
```
Mês 1: presença 85% → notas normais
Mês 2: presença 70% → notas caindo levemente
Mês 3: presença 50% → notas abaixo de 5,0 em várias matérias
Mês 4: abandono
```

Notas só caem **depois** da frequência. Um sistema baseado em notas é inerentemente reativo — detecta o problema após a frequência já ter sinalizado.

---

## 2. Features de Frequência Propostas

### Feature 1 — Frequência Atual por Matéria
```python
# Nova coluna em ml_features
freq_atual = presencas / total_aulas  # [0, 1]
```

### Feature 2 — Tendência de Frequência (slope)
```python
# Slope da frequência ao longo do ano
freq_slope = _slope([freq_q1, freq_q2, freq_q3])
```

### Feature 3 — Frequência Mínima nas Últimas 4 Semanas
```python
# Captura abandono recente
freq_recente = presencas_ultimas_4_semanas / aulas_ultimas_4_semanas
```

### Feature 4 — Percentual de Faltas Justificadas
```python
# Distingue ausência voluntária vs forçada (doença, evento)
pct_faltas_justificadas = faltas_justificadas / total_faltas
```

---

## 3. Schema de Banco para Frequência

```sql
-- Nova tabela para registro de frequência
CREATE TABLE presencas (
    id INTEGER PRIMARY KEY,
    aluno_id INTEGER NOT NULL,
    materia_id INTEGER NOT NULL,
    data DATE NOT NULL,
    presente BOOLEAN NOT NULL DEFAULT 1,
    justificada BOOLEAN DEFAULT 0,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
);

-- Índice para queries de frequência
CREATE INDEX idx_presencas_aluno_data ON presencas(aluno_id, data);
```

---

## 4. Impacto Esperado no Modelo

Com frequência incluída:
- Feature importance estimada de `freq_atual`: 15-25%
- Feature importance estimada de `freq_slope`: 8-12%
- Ganho esperado em recall de Recuperação: +5-10 pp
- Ganho esperado em acurácia geral: +2-3 pp

Mais importante: frequência permite **detecção mais precoce** — um aluno com M1 e frequência baixa (após N1) tem risco muito mais alto que M1 sugere sozinho.

---

## 5. Integração no EduPredict

### Modificações em cads.py

```python
def gerar_features_ml_v2():
    """Versão com features de frequência."""
    # ... features existentes ...
    
    # Adicionar frequência
    freq_query = """
        SELECT 
            aluno_id, materia_id,
            COUNT(CASE WHEN presente = 1 THEN 1 END) * 1.0 / COUNT(*) as freq_atual,
            -- Calcular slope de frequência por trimestre
            -- ...
        FROM presencas
        GROUP BY aluno_id, materia_id
    """
    freq_data = conn.execute(freq_query).fetchall()
    
    # Merge com features existentes
    # ...
```

### Modificações na GUI

Na interface de predições, exibir frequência atual e tendência:
```
📅 Frequência: 72% (↘ queda de 15% nas últimas 4 semanas)
```

---

## 6. Desafios de Implementação

### Desafio 1 — Coleta de Dados
Registrar frequência requer integração com o processo de chamada. Professores precisariam registrar presença pelo sistema — mudança de processo.

### Desafio 2 — Granularidade
Frequência por dia vs por semana vs por mês — qual granularidade é mais preditiva?

### Desafio 3 — Sincronização Temporal
Frequência e notas têm temporalidades diferentes. Um aluno pode ter frequência alta mas nota baixa (presente, mas não aprende).

### Desafio 4 — LGPD
Registros de presença/ausência de menores têm sensibilidade adicional — geolocalização implícita, padrões de comportamento.

---

## 7. Priorização no Roadmap

Para o **artigo de extensão**, incorporar frequência é a melhoria de maior impacto identificada:
1. Resolve a lacuna comparativa com Lima (2021) e Melo (2023)
2. Habilita detecção precoce verdadeira (antes das notas caírem)
3. Alinha com a justificativa de "prevenção de evasão" do artigo original

**Timeline estimado:** 4-6 semanas de desenvolvimento (schema + coleta + features + retreino).

---

## Links

- [[Limitações Gerais do Artigo]]
- [[Lima 2021 — Random Forest e SVM]]
- [[Melo 2023 — MAPEA]]
- [[Análise Comparativa dos Trabalhos]]
- [[Plano de Artigo ABNT]]
- [[Débitos Técnicos Identificados]]
- [[Evasão Escolar no Brasil — Contexto e Dados]]
