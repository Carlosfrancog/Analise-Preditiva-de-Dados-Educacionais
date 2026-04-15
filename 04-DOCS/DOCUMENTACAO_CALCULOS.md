# 📊 DOCUMENTAÇÃO COMPLETA DE CÁLCULOS - SISTEMA EDUCACIONAL COM ML

**Versão:** 2.0  
**Data:** Abril 2026  
**Objetivo:** Explicar TODAS as fórmulas, features, e lógica de predição do sistema

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Entrada de Dados](#entrada-de-dados)
3. [Features para Machine Learning](#features-para-machine-learning)
4. [Normalização de Dados](#normalização-de-dados)
5. [Modelos de ML](#modelos-de-ml)
6. [Análise de Desempenho](#análise-de-desempenho)
7. [Prognóstico e Tendências](#prognóstico-e-tendências)
8. [Legendas e Símbolos](#legendas-e-símbolos)
9. [Fluxo Completo](#fluxo-completo)

---

## 🎯 VISÃO GERAL

O sistema usa **Machine Learning (Random Forest)** para prever o desempenho futuro de alunos baseado em:
- **Notas parciais**: N1, N2, N3, N4 (escala 0-10)
- **Dados agregados**: média por aluno, média da turma
- **Tendências**: slope (inclinação das notas), variância (inconsistência)
- **Contexto**: série/ano escolar, percentage de matérias aprovadas

**Fluxo Principal:**
```
Notas (N1-N4) 
    ↓
Calcular Features Brutas
    ↓
Normalizar Features (0-1)
    ↓
Treinar/Usar Modelo ML
    ↓
Gerar Prognóstico
    ↓
Exibir no Dashboard
```

---

## 📥 ENTRADA DE DADOS

### Estrutura de Notas

| Campo | Tipo | Escala | Descrição |
|-------|------|--------|-----------|
| **N1** | Real | 0-10 | Primeira avaliação (bimestre 1) |
| **N2** | Real | 0-10 | Segunda avaliação (bimestre 2) |
| **N3** | Real | 0-10 | Terceira avaliação (bimestre 3) |
| **N4** | Real | 0-10 | Quarta avaliação / Recuperação (bimestre 4) |

### Contexto do Aluno

| Campo | Descrição |
|-------|-----------|
| **Série** | 6º ao 3º Médio (códigos: 6F, 7F, ..., 3M) |
| **Sala/Turma** | Classe do aluno |
| **Matéria** | Disciplina específica |

---

## 🧮 FEATURES PARA MACHINE LEARNING

O sistema usa **9 features** como entrada para os modelos de ML.

### 📍 Localização do Cálculo de Features

- **Arquivo 1:** `cads.py` → função `gerar_features_ml()` (linha ~400)
- **Arquivo 2:** `gui_ml_integration.py` → função `analyze_student()` (linha ~200-280)

### 📊 Lista Completa de Features

#### **Grupo 1: Notas Normalizadas (4 features)**

```
Feature 1: n1_norm
├─ Fórmula: n1_norm = N1 / 10
├─ Intervalo: [0, 1]  (0 = nota 0, 1 = nota 10)
├─ Propósito: Primeira avaliação normalizada
├─ Por quê: Modelo precisa de entradas entre 0-1
└─ Arquivo: cads.py (linha 513), gui_ml_integration.py (linha 267)

Feature 2: n2_norm
├─ Fórmula: n2_norm = N2 / 10
├─ Intervalo: [0, 1]
├─ Propósito: Segunda avaliação normalizada
└─ Por quê: Idem n1_norm

Feature 3: n3_norm
├─ Fórmula: n3_norm = N3 / 10
├─ Intervalo: [0, 1]
├─ Propósito: Terceira avaliação normalizada
├─ Nota: Se N3 ainda não preenchida, usa 0
└─ Por quê: Idem n1_norm

Feature 4: n4_norm
├─ Fórmula: n4_norm = N4 / 10
├─ Intervalo: [0, 1]
├─ Propósito: Quarta avaliação normalizada
├─ Nota: Geralmente 0 durante a predição (não foi preenchida)
└─ Por quê: Idem n1_norm
```

#### **Grupo 2: Média Ponderada (1 feature)**

```
Feature 5: media_pond_norm (Média Ponderada Normalizada)
├─ Fórmula Base: MP = (N1×0.20 + N2×0.25 + N3×0.25 + N4×0.30) / ΣPesos
├─ Onde:
│  ├─ 0.20 = peso de N1 (20%)
│  ├─ 0.25 = peso de N2 (25%)
│  ├─ 0.25 = peso de N3 (25%)
│  └─ 0.30 = peso de N4 (30%)
├─ ΣPesos = soma dos pesos das notas preenchidas
├─ Intervalo: [0, 1]
├─ Exemplo:
│  ├─ Se N1=8, N2=9, N3=?, N4=?
│  ├─ MP = (8×0.20 + 9×0.25) / (0.20 + 0.25) = 4.0 / 0.45 = 8.89
│  └─ media_pond_norm = 8.89 / 10 = 0.889
├─ Propósito: Desempenho geral normalizado
└─ Por quê:
   ├─ Pesos refletem importância (recuperação vale menos)
   ├─ Normalização em relação às notas preenchidas (não penaliza N4 vazio)
   └─ Essencial para determinar aprovação/recuperação/reprovação
```

**Pesos das Notas (Constante PESOS_NOTAS):**
```python
PESOS_NOTAS = {
    "n1": 0.20,  # Primeira avaliação
    "n2": 0.25,  # Segunda avaliação
    "n3": 0.25,  # Terceira avaliação
    "n4": 0.30   # Recuperação (peso maior!)
}
```

**Status Baseado em Média Ponderada:**
| Faixa MP | Código | Rótulo | Cor |
|----------|--------|--------|-----|
| MP < 5.0 | 0 | Reprovado | Vermelho (#C62828) |
| 5.0 ≤ MP < 6.0 | 1 | Recuperação | Laranja (#FF9800) |
| MP ≥ 6.0 | 2 | Aprovado | Verde (#2E7D32) |

#### **Grupo 3: Tendência (1 feature)**

```
Feature 6: slope_notas (Inclinação das Notas)
├─ Fórmula: Regressão Linear Simples
│  ├─ xs = [0, 1, 2, 3] (índices das notas)
│  ├─ ys = [N1, N2, N3, N4] (valores preenchidos)
│  ├─ Usar apenas pares (x, y) onde y ≠ None
│  ├─ Calcular:
│  │  ├─ mx = média dos xs
│  │  ├─ my = média dos ys
│  │  ├─ coef_raw = Σ[(x - mx)(y - my)] / Σ[(x - mx)²]
│  │  └─ slope = max(-1, min(1, coef_raw / (10/max(len_xs-1, 1))))
│  └─ Normaliza para [-1, 1]
├─ Intervalo: [-1, 1]
│  ├─ -1 = máxima piora (nota cai 10 pontos a cada período)
│  ├─  0 = notas estáveis
│  └─ +1 = máxima melhora (nota sobe 10 pontos a cada período)
├─ Exemplos:
│  ├─ N1=2, N2=5: slope ≈ +0.5 (tendência positiva)
│  ├─ N1=8, N2=4: slope ≈ -0.5 (tendência negativa)
│  └─ N1=7, N2=7: slope ≈ 0 (estável)
├─ Propósito: Detectar se aluno está melhorando ou piorando
└─ Por quê:
   ├─ Importante para prognóstico (tendência ajuda predição)
   ├─ Alunos em alta têm melhor chance de recuperação
   └─ Alunos em queda precisam intervenção imediata

CÓDIGO PYTHON (cads.py linha 370):
def _slope(vals):
    xs = [i for i, v in enumerate(vals) if v is not None]
    ys = [v for v in vals if v is not None]
    if len(xs) < 2:
        return 0.0
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    raw = (num / den) if den else 0.0
    return max(-1.0, min(1.0, raw / (10 / max(len(xs) - 1, 1))))
```

#### **Grupo 4: Consistência (1 feature)**

```
Feature 7: variancia_notas (Inconsistência das Notas)
├─ Fórmula: Desvio Padrão Normalizado
│  ├─ Calcular desvio padrão das notas preenchidas
│  ├─ σ = √[Σ(N - média)² / n]
│  ├─ Normalizar: σ_norm = min(1.0, σ / 5.0)
│  └─ Máximo teórico: σ = 5 (notas oscilando entre 0 e 10)
├─ Intervalo: [0, 1]
│  ├─  0 = notas muito consistentes
│  └─  1 = notas muito oscilantes
├─ Exemplos:
│  ├─ N1=7, N2=7, N3=7: variancia ≈ 0 (muito consistente)
│  ├─ N1=2, N2=9, N3=2: variancia ≈ 0.8 (muito oscilante)
│  └─ N1=5, N2=6, N3=5: variancia ≈ 0.1 (pouco oscilante)
├─ Propósito: Detectar alunos imprevisíveis
└─ Por quê:
   ├─ Alunos oscilantes são impreviáveis
   ├─ Ajuda o modelo a não confiar cegamente em slope
   └─ Facilita identificação de problemas inconsistentes (falta, saúde mental)

CÓDIGO PYTHON (cads.py linha 383):
def _std(vals):
    clean = [v for v in vals if v is not None]
    if len(clean) < 2:
        return 0.0
    m = sum(clean) / len(clean)
    variance = sum((v - m) ** 2 for v in clean) / len(clean)
    return min(1.0, (variance ** 0.5) / 5.0)
```

#### **Grupo 5: Contexto do Aluno (2 features)**

```
Feature 8: media_geral_aluno (Desempenho Geral)
├─ Fórmula: Média simples de TODAS as matérias do aluno
│  ├─ medias_aluno = [MP_mat1, MP_mat2, ..., MP_matN]
│  └─ media_geral = Σ medias_aluno / N
├─ Intervalo: [0, 1] (após normalização por 10)
├─ Propósito: Ver se aluno é "forte" ou "fraco" em geral
├─ Exemplo:
│  ├─ Aluno tem 5 matérias: 8.5, 7.0, 6.5, 5.0, 4.5
│  ├─ media_geral = (8.5+7+6.5+5+4.5) / 5 = 6.3
│  └─ Aluno é "médio-forte"
└─ Por quê:
   ├─ Contexto importante (aluno forte pode ter dificuldade em 1 matéria)
   └─ Ajuda modelo a diferenciar anomalias de padrões

Feature 9: media_turma_norm (Desempenho da Turma)
├─ Fórmula: Média simples da turma EM CADA MATÉRIA
│  ├─ medias_turma_materia = [MP_aluno1, MP_aluno2, ..., MP_alunoN]
│  └─ media_turma = Σ / N
├─ Intervalo: [0, 1] (após normalização por 10)
├─ Propósito: Contexto social (turma está indo bem ou mal?)
├─ Exemplo:
│  ├─ Turma 7º B em Matemática: 15 alunos com média 4.5
│  ├─ Aluno X tem nota 5.0 em Matemática
│  ├─ Aluno está ACIMA da média da turma
│  └─ Pode ser que Matemática seja difícil pra turma toda
└─ Por quê:
   ├─ Evita enviesar análise por qualidade da turma
   ├─ Identify problemas globais vs. estudante específico
   └─ Ajuda a diferenciar "difícil pro aluno" vs "difícil pra turma"

Feature "extra" (não listado acima): serie_num_norm
├─ Fórmula: Normalizar série escolar de [6, 12]
│  ├─ SERIE_MAP = {6F: 6, 7F: 7, ..., 3M: 12}
│  ├─ serie_num_norm = (serie_raw - 6) / (12 - 6)
│  └─ Intervalo: [0, 1]
├─ Propósito: Contexto de maturidade (6º é mais difícil que 3º?)
└─ Por quê:
   ├─ Diferentes séries têm dificuldade diferente
   └─ Expectativas mudam conforme a idade
```

---

## 🔄 NORMALIZAÇÃO DE DADOS

### Por quê normalizar?

Os modelos de ML (Random Forest) funcionam melhor quando features estão **na mesma escala**. Sem isso:
- Features em escala maior (0-100) dominam features em escala menor (0-10)
- O modelo fica enviesado
- Interpretabilidade fica confusa

### Técnica: Min-Max Scaling para [0, 1]

**Fórmula Geral:**
```
feature_normalizado = (valor_bruto - valor_min) / (valor_max - valor_min)
```

### Features Normalizadas

| Feature | Valor Mín | Valor Máx | Fórmula |
|---------|-----------|-----------|---------|
| n1_norm | 0 | 10 | N1 / 10 |
| n2_norm | 0 | 10 | N2 / 10 |
| n3_norm | 0 | 10 | N3 / 10 |
| n4_norm | 0 | 10 | N4 / 10 |
| media_pond_norm | 0 | 10 | MP / 10 |
| slope_notas | -10/3 | +10/3 | raw_slope / (10/len) clipped [-1,1] |
| variancia_notas | 0 | 5 | σ / 5 clipped [0,1] |
| serie_num_norm | 6 | 12 | (serie - 6) / 6 |
| media_turma_norm | 0 | 10 | media_turma / 10 |

---

## 🤖 MODELOS DE ML

### Arquitetura Geral

**Arquivo:** `train_simple.py`  
**Tipo de Modelo:** Random Forest Classifier (Árvores de Decisão Aleatórias)  
**Output:** 3 classes (Reprovado=0, Recuperação=1, Aprovado=2)

### Modelos Disponíveis

| Modelo | n_estimators | max_depth | Acurácia | Quando Usar |
|--------|--------------|-----------|----------|------------|
| **RF_M1** | 100 | 5 | ~84% | Teste rápido (menor) |
| **RF_M2** | 150 | 10 | ~92% | Produção média |
| **RF_M3** | 200 | ilimitado | ~94% | Produção (usado) |

### Dados de Treinamento

```
Total de registros: 15,613 (aluno × matéria)
Base de dados: 200+ alunos, 13 matérias, 7 séries diferentes

Distribuição de Classes:
├─ Reprovado (0):    ~20%
├─ Recuperação (1):  ~15%
└─ Aprovado (2):     ~65%

Split: 80% treino, 20% teste
Random State: 42 (reprodutibilidade)
```

### Processo de Treinamento (Pipeline)

```
1. Geração de Features
   ├─ SQL query de todas as notas + metadados
   ├─ Calcular agregados (média aluno, média turma)
   └─ Salvar em tabela ml_features

2. Exportação para CSV
   ├─ ml_dataset.csv
   └─ Estrutura: [n1_norm, n2_norm, ..., status_encoded]

3. Carregamento em Pandas
   ├─ pd.read_csv("ml_dataset.csv")
   └─ 15,613 linhas × 9 colunas

4. Separação Treino/Teste
   ├─ X_train: 12,490 amostras (80%)
   ├─ X_test: 3,123 amostras (20%)
   └─ Estratificação mantém proporção de classes

5. Treinamento do Modelo
   ├─ RandomForestClassifier (199 árvores)
   ├─ Cada árvore: regra "if feature > threshold then direção"
   └─ Ensemble: média as predições de todas árvores

6. Avaliação
   ├─ Accuracy: % correto
   ├─ F1-Score: precisão + recall
   └─ Matriz de Confusão: detalhamento de erros

7. Salvamento
   ├─ ml_models/RF_M3.pkl (modelo)
   └─ ml_models/RF_M3_metadata.json (features, accuracy, etc.)
```

### Como o Modelo Faz uma Predição

```
Input: 9 features [n1_norm, n2_norm, ..., media_turma_norm]
                           ↓
        Passar por 200 árvores de decisão em paralelo
        Cada árvore vota em uma classe (0, 1 ou 2)
                           ↓
        Contar votos:
        ├─ Votos para 0: V0
        ├─ Votos para 1: V1
        └─ Votos para 2: V2
                           ↓
        Probabilidades:
        ├─ P(0) = V0 / 200
        ├─ P(1) = V1 / 200
        └─ P(2) = V2 / 200
                           ↓
        Predição Final: argmax(P(0), P(1), P(2))
        Exemplo: P=[0.2, 0.3, 0.5] → Prediz 2 (Aprovado)
                           ↓
        Output: (classe_predita, probabilidades)
```

---

## 📈 ANÁLISE DE DESEMPENHO

### Localização

**Arquivo:** `gui_ml_integration.py`  
**Função:** `DisciplinePerformanceAnalyzer.analyze_student()` (linha ~135)

### Cálculo de Status Atual

Para cada disciplina do aluno, calcular:

```
1. Média Ponderada (já explicado)
   MP = (N1×0.20 + N2×0.25 + N3×0.25 + N4×0.30) / ΣPesos

2. Status Baseado em MP
   if MP < 5.0:
       status = 0 (Reprovado)
   elif MP < 6.0:
       status = 1 (Recuperação)
   else:
       status = 2 (Aprovado)

3. Risk Score (Risco de Reprovação)
   risk_score = max(0, min(1, 1 - (MP / 10)))
   ├─ MP = 10 → risk_score = 0   (seguro)
   ├─ MP = 5  → risk_score = 0.5 (em risco)
   └─ MP = 0  → risk_score = 1   (reprovado)
```

---

## 🔮 PROGNÓSTICO E TENDÊNCIAS

### Localização

**Arquivo:** `gui_ml_integration.py`  
**Função:** `DisciplinePerformanceAnalyzer.analyze_student()` (linha ~280-390)

### Dois Cenários

#### **Cenário 1: Tem N3 e/ou N4 (Retrospectiva)**

```
Uso Caso: Análise do desempenho APÓS algumas notas serem lançadas

Dados Disponíveis:
├─ N1 e N2: sempre completados
├─ N3: pode estar preenchido (bimestre 3)
└─ N4: pode estar preenchido (recuperação)

Lógica:
1. Calcular status real com N3 e/ou N4 (se preenchidos)
   status_n34 = classificar(media(N3, N4))

2. Calcular status previsto com modelo
   features_pred = [n1_norm, n2_norm, 0, 0, slope, variancia, media, serie, turma]
   predicted_status = RF_M3.predict(features_pred)

3. Comparar: Aluno superou expectativas?
   if predicted_status < status_n34:
       → [+] Superou Previsão (status melhor que esperado)
   elif predicted_status > status_n34:
       → [-] Piou Previsão (status pior que esperado)
   else:
       → [-] Como Esperado (acertou previsão)

Exemplo Real:
├─ N1=2, N2=5
├─ Modelo prevê: status=1 (Recuperação)
├─ Mas N3=8, N4=8 → real status=2 (Aprovado)
├─ predicted_status (1) < status_real (2)
└─ Resultado: [+] Superou Previsão! ✓
```

#### **Cenário 2: Só tem N1 e N2 (Prospectiva)**

```
Uso Caso: Predição do desempenho FUTURO (N3 e N4 não preenchidos ainda)

Dados Disponíveis:
├─ N1: obrigatório
├─ N2: obrigatório
├─ N3 e N4: vazios (ainda não foram)

Lógica:
1. Calcular status atual baseado em N1 e N2
   media_n12 = (N1 + N2) / 2
   status_n12 = classificar(media_n12)

2. Calcular slope (tendência real)
   slope_pct = ((N2 - N1) / N1) × 100

3. Análise Baseada em Slope
   if slope_pct > 20%:
       → [*] Vai Melhorar (melhora significativa)
       Motivo: N2 > N1, e a diferença é > 20%
       
   elif slope_pct < -20%:
       → [!] Vai Piorar (queda significativa)
       Motivo: N2 < N1, e a diferença é > 20%
       
   else:  # -20% ≤ slope_pct ≤ 20%
       → Estável, usar modelo como desempate
       if predicted_status > status_n12:
           → [*] Vai Melhorar (modelo prevê melhor que atual)
       elif predicted_status < status_n12:
           → [!] Vai Piorar (modelo prevê pior que atual)
       else:
           → [-] Estável (mantém a mesma categoria)

Exemplos Reais:

Exemplo 1: Melhora Forte
├─ N1 = 2
├─ N2 = 5
├─ slope_pct = (5-2)/2 × 100 = 150%
├─ 150% > 20%
└─ Prognóstico: [*] Vai Melhorar

Exemplo 2: Piora Forte
├─ N1 = 9
├─ N2 = 4
├─ slope_pct = (4-9)/9 × 100 = -55.5%
├─ -55.5% < -20%
└─ Prognóstico: [!] Vai Piorar

Exemplo 3: Estável (Modelo é Desempate)
├─ N1 = 6
├─ N2 = 6.5
├─ slope_pct = (6.5-6)/6 × 100 = 8.3%
├─ -20% < 8.3% < 20% → ESTÁVEL
├─ Enquanto isso, modelo prevê status=2 (Aprovado)
├─ status_n12 = 2 (média de 6.25 → Aprovado)
├─ predicted_status (2) = status_n12 (2)
└─ Prognóstico: [-] Estável
```

### Fórmula Slope Percentual

```
slope_pct = ((N2 - N1) / N1) × 100

Esse é um percentual de MUDANÇA relativa:
├─ Positivo = nota subiu
├─ Negativo = nota caiu
└─ Magnitude = quão grande foi a mudança

Exemplos:
├─ N1=2, N2=5: (5-2)/2×100 = 150% (nota triplicou!)
├─ N1=10, N2=8: (8-10)/10×100 = -20% (nota caiu 20%)
├─ N1=9, N2=9: (9-9)/9×100 = 0% (nota manteve)
└─ N1=1, N2=10: (10-1)/1×100 = 900% (transformação!)
```

### Limiares de Significância

```
Limiar de ±20%:
├─ Por quê 20%?
│  ├─ Estatisticamente significante (muda de categoria)
│  ├─ N1=5: N2=6 (+20%) pode ir de Recuperação para Aprovado
│  └─ N1=8: N2=6.4 (-20%) pode ir de Aprovado para Recuperação
├─ Implementação:
│  ├─ if slope_pct > 20:  SERÁ MELHOR
│  ├─ if slope_pct < -20: SERÁ PIOR
│  └─ else:               USAR MODELO E SLOPE VALOR
```

---

## 🎨 LEGENDAS E SÍMBOLOS

### Status de Desempenho

| Rótulo | Código | Intervalo MP | Cor | Significado |
|--------|--------|--------------|-----|-------------|
| Reprovado | 0 | < 5.0 | 🔴 #C62828 (Vermelho) | Reprovação garantida |
| Recuperação | 1 | 5.0 - 5.9 | 🟠 #FF9800 (Laranja) | Pode recuperar |
| Aprovado | 2 | ≥ 6.0 | 🟢 #2E7D32 (Verde) | Passou |

### Símbolos de Tendência

| Símbolo | Significado | Contexto |
|---------|-------------|---------|
| `[*]` | Vai Melhorar | Slope > +20% ou modelo >= status atual |
| `[!]` | Vai Piorar | Slope < -20% ou modelo < status atual |
| `[-]` | Estável | -20% ≤ slope ≤ +20% e modelo = status |
| `[+]` | Superou! | Resultado N3/N4 melhor que previsto |
| `[X]` | Não Alcançou | Resultado N3/N4 pior que previsto |
| `[ok]` | Normal | Resultado N3/N4 como esperado |
| `[->]` | Mantém | Continua na mesma categoria |

### Descrição de Prognósticos

```python
prognosis_dict = {
    "will_improve":           "Tendência positiva, vai melhorar",
    "will_decline":           "Tendência negativa, vai piorar",
    "stable":                 "Desempenho mantém estável",
    "better_than_expected":   "Superou a previsão do modelo",
    "worse_than_expected":    "Ficou abaixo da previsão",
    "as_expected":            "Resultou como esperado"
}
```

---

## 📊 FLUXO COMPLETO

### Fluxo 1: Geração de Features (Treino)

```
┌─────────────────────────────────────────┐
│ 1. Consultar Banco de Dados             │
│    SELECT notas, aluno, materia, sala   │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 2. Pré-calcular Agregados               │
│    - media_aluno: média por aluno       │
│    - media_turma: média turma × materia │
│    - pct_ok: % de matérias aprovadas    │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 3. Para cada (aluno, materia):          │
│    a) Calcular MP com formula           │
│    b) Normalizar notas (÷ 10)           │
│    c) Calcular slope com regressão      │
│    d) Calcular variancia com σ          │
│    e) Classificar status (0, 1, 2)      │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 4. Salvar em Tabela ml_features         │
│    (upsert = insert or update)          │
│    Total: 15,613 registros              │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 5. Exportar para CSV                    │
│    ml_dataset.csv                       │
│    [n1_norm, n2_norm, ..., status]      │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 6. Treinar 3 Modelos                    │
│    - RF_M1: 100 árvores, profund. 5     │
│    - RF_M2: 150 árvores, profund. 10    │
│    - RF_M3: 200 árvores (melhor)        │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 7. Salvar Modelos                       │
│    - ml_models/RF_M3.pkl                │
│    - ml_models/RF_M3_metadata.json      │
└─────────────────────────────────────────┘
```

**Arquivo Responsável:** `train_simple.py`

### Fluxo 2: Análise e Dashboard (Predição)

```
┌──────────────────────────────────────────┐
│ 1. Usuário Abre Dashboard                │
│    Seleciona um aluno                    │
└────────────────┬─────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│ 2. Buscar Todas as Matérias do Aluno     │
│    SELECT materia, n1, n2, n3, n4        │
└────────────────┬─────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│ 3. Para cada Materia:                    │
│                                          │
│    a) Calcular Média Ponderada (MP)      │
│    b) Determinar Status Atual (0,1,2)    │
│    c) Normalizar Features                │
│    d) Passar pelo modelo RF_M3           │
│    e) Obter probabilidades               │
│    f) Interpretar Prognóstico            │
└────────────────┬─────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│ 4. Analisar Tendência                    │
│                                          │
│    if tem N3 e/ou N4:                    │
│        Comparar com previsão             │
│        → Superou? Piou?                  │
│                                          │
│    elif só tem N1 e N2:                  │
│        Calcular slope_pct                │
│        if slope > 20:  Vai Melhorar      │
│        elif slope < -20: Vai Piorar      │
│        else: Usar modelo                 │
└────────────────┬─────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│ 5. Agrupar por Status (Filtros)          │
│    - Todas                               │
│    - Aprovadas                           │
│    - Recuperação                         │
│    - Reprovadas                          │
│    - Vai Melhorar                        │
│    - Vai Piorar                          │
└────────────────┬─────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│ 6. Gerar Recomendações                   │
│    Ordenar por Prioridade:               │
│    1. Matérias com "Reprovado" + Piorando│
│    2. Matérias com "Recuperação"         │
│    3. Matérias com "Vai Melhorar" (low)  │
└────────────────┬─────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│ 7. Exibir no Dashboard                   │
│    - Cards com matérias lado-a-lado      │
│    - Filtros por status                  │
│    - Preview de N4 se não preenchido     │
│    - Recomendações ordenadas por risco   │
└──────────────────────────────────────────┘
```

**Arquivos Responsáveis:**
- `gui_ml_integration.py` (análise)
- `gui_predicoes_improved.py` (exibição)
- `gui_escola.py` (integração)

---

## 📝 EXEMPLO WALKTHROUGH COMPLETO

### Cenário Real: Aluno João em Matemática

**Step 1: Input**
```
Aluno: João (ID=5)
Materia: Matemática (ID=3)
Notas: N1=6, N2=8, N3=9, N4=?
```

**Step 2: Cálculo da Média Ponderada**
```
MP = (6×0.20 + 8×0.25 + 9×0.25) / (0.20 + 0.25 + 0.25)
   = (1.2 + 2.0 + 2.25) / 0.70
   = 5.45 / 0.70
   = 7.79 → Aprovado (≥ 6)
```

**Step 3: Normalização de Features**
```
n1_norm = 6.0 / 10 = 0.60
n2_norm = 8.0 / 10 = 0.80
n3_norm = 9.0 / 10 = 0.90
n4_norm = 0.0 / 10 = 0.00 (ainda não preenchido)

slope = regressão_linear([6, 8, 9])
      = função_slope([None, 6, 8, 9])
      = ... = +0.75 (forte melhora)

variancia = std([6, 8, 9]) / 5
          = 1.25 / 5
          = 0.25 (pouca inconsistência)

media_aluno = média de todas matérias de João
            = (7.5 + 7.0 + 7.79 + ...) / N
            = 7.2 → media_aluno_norm = 0.72

media_turma = média da turma em Matemática
            = 6.5 → media_turma_norm = 0.65

serie = série de João = 7º = 7F
serie_num_norm = (7 - 6) / (12 - 6) = 1/6 = 0.167
```

**Step 4: Passar pelo Modelo**
```
features = [0.60, 0.80, 0.90, 0.00, 0.75, 0.25, 0.72, 0.167, 0.65]

RF_M3.predict(features)
↓
200 árvores votam:
├─ Árvore 1: vota 2 (Aprovado)
├─ Árvore 2: vota 2 (Aprovado)
├─ Árvore 3: vota 1 (Recuperação)
├─ ...
└─ Total: 190 votos em 2, 10 votos em 1, 0 votos em 0

Resultado:
├─ P(Reprovado) = 0 / 200 = 0.00
├─ P(Recuperação) = 10 / 200 = 0.05
└─ P(Aprovado) = 190 / 200 = 0.95

predicted_status = argmax = 2 (Aprovado com 95% confiança)
```

**Step 5: Análise de Tendência**
```
Situação: Tem N3 preenchido

Status Real (com N3):
├─ media_n3 = (6 + 8 + 9) / 3 = 7.67
├─ status_real = 2 (Aprovado)

Comparação:
├─ predicted_status = 2 (Aprovado)
├─ status_real = 2 (Aprovado)
└─ predicted_status (2) = status_real (2)

Resultado: [ok] Normal - Acertou a previsão

Caso N4 fosse preenchido como 10:
├─ media_final = (6 + 8 + 9 + 10) / 4 = 8.25
├─ status_real = 2 (Aprovado)
└─ Mesmo resultado: [ok]

Se N4 fosse 3:
├─ media_final = (6 + 8 + 9 + 3) / 4 = 6.5
├─ status_real = 2 (Aprovado)
└─ Mesmo resultado: [ok]
```

**Step 6: Resultado Final**

```
┌─────────────────────────────────────────┐
│ MATEMÁTICA                              │
├─────────────────────────────────────────┤
│ Notas: N1=6, N2=8, N3=9, N4=?          │
│ Média: 7.79                             │
│ Status: [ok] Aprovado                   │
│ Prognóstico: [-] Estável (vai manter)   │
│ Confiança: 95%                          │
├─────────────────────────────────────────┤
│ Próximos Passos:                        │
│ João está indo bem! Manter o ritmo.     │
└─────────────────────────────────────────┘
```

---

## 📌 RESUMO RÁPIDO

### 9 Features Utilizadas

1. **n1_norm** (0-1): Primeira nota normalizada
2. **n2_norm** (0-1): Segunda nota normalizada
3. **n3_norm** (0-1): Terceira nota normalizada
4. **n4_norm** (0-1): Quarta nota normalizada
5. **media_pond_norm** (0-1): Média ponderada normalizada
6. **slope_notas** (-1 a +1): Tendência linear das notas
7. **variancia_notas** (0-1): Desvio padrão normalizado
8. **media_geral_aluno** (0-1): Desempenho geral do aluno
9. **media_turma_norm** (0-1): Desempenho da turma

### 3 Modelos Treinados

- **RF_M1**: 100 árvores, profundidade máx 5
- **RF_M2**: 150 árvores, profundidade máx 10
- **RF_M3**: 200 árvores, sem limite (PRODUÇÃO) - 94% acurácia

### 6 Filtros de Análise

1. Todas as matérias
2. Aprovadas (status = 2)
3. Recuperação (status = 1)
4. Reprovadas (status = 0)
5. Vai Melhorar (slope > 20%)
6. Vai Piorar (slope < -20%)

### 4 Comparações de Tendência

1. **[ok] Normal**: Resultado = Previsão
2. **[+] Superou**: Resultado > Previsão
3. **[X] Piou**: Resultado < Previsão
4. **[-], [*], [!]**: Estável, Melhora, Piora

---

## 📚 REFERÊNCIAS

| Arquivo | Função | Linha |
|---------|--------|-------|
| cads.py | `_slope()` | 370 |
| cads.py | `_std()` | 383 |
| cads.py | `gerar_features_ml()` | 396 |
| cads.py | Constante PESOS_NOTAS | 362 |
| gui_ml_integration.py | `predict()` | 97 |
| gui_ml_integration.py | `analyze_student()` | 135 |
| train_simple.py | Script completo | Início |
| gui_predicoes_improved.py | `_prever_n4()` | 529 |

---

**FIM DA DOCUMENTAÇÃO**

Data de Atualização: 14 de Abril de 2026
