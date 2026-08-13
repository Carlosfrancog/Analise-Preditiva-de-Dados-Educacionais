---
tags:
  - arquitetura
  - tgi-codes
created: 2026-05-13
---

# Arquitetura do Sistema

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## Visão Geral

O sistema é dividido em 5 camadas principais que se comunicam de forma hierárquica:

```
gui_escola.py  (Aplicação Principal)
      │
      ├── cads.py          (Core: BD + CRUD + Features)
      ├── gui_predicoes_improved.py   (Dashboard de Predições)
      ├── gui_ml_advanced.py          (Dashboard de ML — Treino)
      └── gui_predicoes.py            (Componentes legacy)
              │
              └── gui_ml_integration.py  (Análise de desempenho)
                        │
                        └── ml_models/  (RF_M*.pkl + metadata.json)
```

---

## Componentes Principais

### 1. Core — `cads.py`

Responsável por tudo que envolve o banco de dados.

| Função | O que faz |
|---|---|
| `init_db()` | Cria o schema SQLite |
| `get_alunos()` / `get_notas()` | CRUD de dados escolares |
| `_slope(vals)` | Calcula tendência linear das notas |
| `_std(vals)` | Calcula desvio padrão |
| `gerar_features_ml()` | Gera as 9 features para ML |
| `exportar_ml_csv()` | Salva dataset em `ml_dataset.csv` |

> [!NOTE] Pesos configuráveis
> `PESOS_NOTAS` é uma variável global em `cads.py` que define os pesos de N1-N4 na média ponderada. A GUI de ML avançada permite alterá-la via sliders.

---

### 2. ML Dashboard — `gui_ml_advanced.py`

Interface modernizada para treinar e analisar modelos.

**Seções da UI:**
- Cards com RF_M1, RF_M2, RF_M3 e acurácia de cada um
- Botões para gerar features e treinar modelos
- Barra de progresso durante treinamento
- Seletor Aluno + Matéria para analisar decisão individual
- Sliders N1-N4 para configurar pesos da média ponderada

---

### 3. Análise de Desempenho — `gui_ml_integration.py`

Classe `DisciplinePerformanceAnalyzer` que:
1. Carrega modelo RF_M3 do disco
2. Calcula features normalizadas em tempo real
3. Gera prognóstico (vai melhorar / piorar / estável)
4. Retorna cores para o dashboard (verde / laranja / vermelho)

---

### 4. Treinamento — `train_simple.py`

Pipeline de treino autônomo:

```
gerar_features_ml() → exportar_ml_csv() → pd.read_csv()
→ train_test_split(80/20) → RandomForestClassifier().fit()
→ pickle.dump() + json.dump()
```

| Modelo | Árvores | Max Depth |
|---|---|---|
| RF_M1 | 100 | 5 |
| RF_M2 | 150 | 10 |
| RF_M3 | 200 | sem limite |

---

## Ciclo de Vida

```
1. INICIALIZAÇÃO → cads.init_db() cria schema
2. OPERAÇÃO      → usuário adiciona alunos, matérias, notas
3. TREINO        → gerar features → treinar RF_M1/M2/M3
4. PREDIÇÃO      → cada aluno recebe prognóstico contínuo
5. INTERVENÇÃO   → professor identifica alunos em risco
```

---

## Links Relacionados

- [[Modelo de Dados]] — schema detalhado da tabela `ml_features`
- [[Fluxos de Execução]] — sequência de chamadas por ação do usuário
- [[cads.py — Core do Sistema]] — referência completa do módulo core
- [[Módulos ML]] — detalhes dos módulos de machine learning
