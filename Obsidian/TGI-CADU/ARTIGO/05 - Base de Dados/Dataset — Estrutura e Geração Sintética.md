---
tags: [artigo, dataset, sintetico, dados, metodologia]
created: 2026-05-16
---

# Dataset — Estrutura e Geração Sintética

[[INDEX - ARTIGO|← Índice]] | [[Pré-processamento e Normalização]] | [[Distribuição de Classes]]

> [!WARNING] Dataset sintético — limitação metodológica central que o artigo subestima

---

## 1. Composição do Dataset

| Dimensão | Valor | Observação |
|---|---|---|
| **Alunos** | 200 | Número base da população |
| **Matérias** | 13 | Por aluno (currículo completo) |
| **Notas por matéria** | Até 4 (N1-N4) | Algumas séries podem ter menos |
| **Registros brutos** | ~18.200 | 200 × 13 × 7 entradas individuais |
| **Pares (aluno, matéria)** | ~2.600 | Unidade real de observação para ML |
| **Registros ML** | 15.613 | Após filtragem de pares com notas suficientes |

**Discrepância:** o artigo reporta "15.613 registros" mas a unidade de observação independente é o par (aluno, matéria) — ~2.600 pares. Os 15.613 incluem múltiplos bimestres por par.

---

## 2. Como os Dados São Gerados

O sistema EduNotas usa um gerador sintético de dados (`cads.py` ou script auxiliar) que:

1. **Cria alunos** com perfis estatísticos (séries 6º-9º do EF e 1º-3º do EM)
2. **Distribui matérias** conforme grade curricular de cada série
3. **Gera notas** seguindo uma distribuição que simula notas reais:
   - Concentração em notas entre 4,0 e 8,0
   - Correlação moderada inter-bimestres (N2 correlacionada com N1)
   - Correlação fraca inter-matérias (alunos "bons" tendem a ter boas notas em todas)
4. **Calcula status** via média ponderada: $media = 0,2 N1 + 0,25 N2 + 0,25 N3 + 0,30 N4$

O algoritmo exato de geração não é documentado no artigo — é uma lacuna crítica para reprodutibilidade.

---

## 3. Por Que Dados Sintéticos São Problemáticos

### Problema 1 — Correlação Intra-Aluno Artificial

Em dados reais, um aluno "ruim" tem notas abaixo da média em TODAS as matérias de forma correlacionada. O gerador sintético pode criar essa correlação de forma mais perfeita do que na realidade, inflando a importância de `pct_materias_ok`.

### Problema 2 — Ausência de Eventos Externos

Dados reais têm:
- Alunos que melhoram abruptamente após mudança de professor
- Notas atípicas por doenças, eventos familiares
- Desistência seguida de retorno (comportamento errático)
- Efeito "prova difícil" que afeta toda a turma igualmente

O gerador sintético produz notas mais "comportadas" — a distribuição de slope_notas provavelmente tem caudas mais curtas que dados reais.

### Problema 3 — Distribuição de Classes Controlada

No gerador, a proporção de Aprovados/Recuperação/Reprovados pode ter sido definida intencionalmente. Em dados reais, a distribuição depende do contexto específico da escola — pode variar dramaticamente.

---

## 4. Consequências para os Resultados

A acurácia de 94,0% deve ser interpretada com cautela:
- Em dados sintéticos "bem-comportados", RF tende a ter performance maior
- A validação cruzada mede generalização dentro do mesmo dataset sintético, não entre dados sintéticos e reais
- Um experimento de validação externa (treinar em sintéticos, testar em reais) seria necessário

**Hipótese pessimista:** a acurácia real em dados de uma escola parceira poderia ser 10-15% menor (80-85%), que ainda seria competitiva mas não mais excepcional.

---

## 5. Comparação com Trabalhos Relacionados

| Trabalho | Dataset | Tamanho |
|---|---|---|
| Lima (2021) | Real (universitário) | Não especificado |
| Melo (2023) | Real (fundamental) | 500 alunos |
| **EduPredict** | **Sintético** | **200 alunos / 15.613 registros** |

O EduPredict tem mais registros que Melo, mas Melo usa dados reais — o que tem mais valor científico para generalização.

---

## 6. Schema da Tabela `ml_features`

```sql
CREATE TABLE ml_features (
    id INTEGER PRIMARY KEY,
    aluno_id INTEGER,
    materia_id INTEGER,
    -- Notas normalizadas
    n1_norm REAL,
    n2_norm REAL,
    n3_norm REAL,
    n4_norm REAL,          -- armazenada mas excluída do treino (leakage)
    -- Features derivadas
    slope_notas REAL,
    variancia_notas REAL,
    media_geral_aluno REAL,
    pct_materias_ok REAL,
    media_turma_norm REAL,
    serie_num_norm REAL,
    -- Feature de leakage (armazenada para visualização)
    media_pond_norm REAL,  -- excluída do treino
    -- Target
    status_encoded INTEGER,  -- 0=Reprovado, 1=Recuperação, 2=Aprovado
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
)
```

---

## 7. Recomendação para Artigo de Extensão

Para publicação em periódico qualificado, seria necessário:
1. **Coletar dados reais** de pelo menos uma escola parceira (mesmo que 30-50 alunos)
2. **Validação cruzada estudo** — treinar em sintéticos, testar em reais
3. **Análise de distribuição** — comparar distribuição de notas sintéticas vs reais
4. **Obter aprovação CEFET/IRB** para uso de dados de alunos menores

---

## Links

- [[Pré-processamento e Normalização]]
- [[Distribuição de Classes]]
- [[Análise Crítica do TGI]]
- [[Limitações Gerais do Artigo]]
- [[Detecção Automática por Correlação de Pearson]]
- [[Pipeline Completo de Treinamento]]
