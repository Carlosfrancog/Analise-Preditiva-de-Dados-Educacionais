---
tags:
  - gui
  - tgi-codes
created: 2026-05-13
---

# Componentes e Páginas — Interface GUI

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## Aplicação Principal — `gui_escola.py`

Ponto de entrada. Gerencia navegação, sidebar e tema.

```
App.__init__()
├── cads.init_db()         → inicializa banco
├── _build_ui()            → cria layout
└── Instancia todas as páginas:
    ├── DashboardPage
    ├── AlunosPage
    ├── SalasPage
    ├── MateriasPage
    ├── NotasPage
    ├── PredictionPageImproved   ← GUI de predições
    ├── RelatorioPage
    └── MLAdvancedPage           ← GUI de ML
```

Para adicionar uma nova página:
```python
from meu_modulo import MinhaPagina
# Na lista de pages em gui_escola.py:
(MinhaPagina, "minha_chave"),
```

---

## Dashboard de Predições — `gui_predicoes_improved.py`

Classe `PredictionPageImproved`. Mostra análise por aluno.

**Funcionalidades:**
- Filtra disciplinas por: Aprovadas / Recuperação / Reprovadas / Todas
- Card por disciplina com notas, status e prognóstico
- Preview de N4 quando ainda não foi lançada
- Motor de recomendações pedagógicas
- Usa `DisciplinePerformanceAnalyzer` de `gui_ml_integration.py`

---

## Dashboard de ML — `gui_ml_advanced.py`

Classe `MLAdvancedPage`. Permite treinar e analisar modelos.

**4 Seções:**

### Seção 1 — Modelos Treinados
Cards com RF_M1, RF_M2, RF_M3 mostrando acurácia e data do último treino.

### Seção 2 — Treinar Modelos
| Botão | Ação |
|---|---|
| 🔄 Gerar Features | `cads.gerar_features_ml()` |
| 🚀 Treinar Todos | RF_M1 + RF_M2 + RF_M3 |
| 📈 Treinar RF_M3 | Apenas o modelo de produção |

Barra de progresso + status label durante o treino.

### Seção 3 — Analisar Decisões
Seletor Aluno + Matéria → clique Analisar → widget de texto com:
- Notas N1–N4 e normalizadas
- Features: slope, variância
- Status real vs predito
- Interpretação em linguagem natural

### Seção 4 — Configurar Pesos
Sliders N1-N4 (0–50%). O sistema normaliza para somar 100%.

**Métodos principais:**
```python
MLAdvancedPage
├── _build()                  → monta interface
├── _create_model_card()      → card de modelo
├── _load_model_info()        → lê metadata.json
├── _generate_features()      → chama cads
├── _train_all_models()       → RF_M1, M2, M3
├── _train_m3_only()          → apenas produção
├── _analyze_decision()       → analisa aluno+matéria
├── _interpret_slope()        → texto sobre slope
├── _interpret_variance()     → texto sobre variância
└── refresh()                 → recarrega comboboxes
```

---

## Componentes Legados — `gui_predicoes.py`

Contém a classe base `BasePage` que todas as páginas herdam. Também tem `SalasPage` e a `PredictionPage` original (substituída pela `_improved`).

---

## Links Relacionados

- [[Fluxos de Execução]] — sequência de chamadas para cada ação
- [[Arquitetura do Sistema]] — como as páginas se conectam com o backend
- [[cads.py — Core do Sistema]] — módulo chamado pelas páginas GUI
