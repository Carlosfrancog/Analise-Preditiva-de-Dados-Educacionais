---
tags: [artigo, implementacao, gui_predicoes, interface, predicao]
created: 2026-05-16
---

# gui_predicoes_improved.py — Interface Preditiva de Desempenho

[[INDEX - ARTIGO|← Índice]] | [← Código](../../07%20-%20Código/gui_predicoes_improved.py.md) | [[gui ml integration py — Motor de Predição]] | [[Arquitetura Modular — Visão Geral]]

> Arquivo: `03-GUI/gui_predicoes_improved.py` | Importado por: `gui_escola.py` como `PredictionPageImproved`

---

## 1. Responsabilidade no Sistema

`gui_predicoes_improved.py` é a página principal de predições da interface. Exibe:
- Seletor de sala → aluno
- Perfil de risco geral do aluno (`🔴 CRÍTICO / 🟡 EM RISCO / 🟢 SEGURO`)
- Cards por disciplina com notas, status ML e prognóstico

É o ponto de contato entre o professor e as predições do Random Forest.

---

## 2. Estrutura de Classes

```python
class PredictionPageImproved(BasePage):
    def __init__(self, parent, app):
        self.ml_loader = MLModelLoader()   # carrega RF_M1/M2/M3 do disco
        self.aluno_var  = tk.StringVar()
        self.aluno_data = {}               # nome → aluno_id
        self.sala_map   = {}               # nome → sala_id
        self.analise_atual = None          # dict retornado por analyze_student()
        self.filter_var = tk.StringVar(value="all")
        self._build_ui()
```

---

## 3. Fluxo Completo de Análise

```
Usuário seleciona aluno
        ↓
_load_aluno() → _load_student_analysis()
        ↓
DisciplinePerformanceAnalyzer.analyze_student(db_path, aluno_id, ml_loader)
        ↓
Retorna dict: {aluno, disciplinas[], strengths[], weaknesses[], at_risk[], profile}
        ↓
_render_cards(analise) → loop sobre disciplinas
        ↓
_create_discipline_card(parent, disc_data) por cada matéria
```

---

## 4. Lógica de Cor do Perfil — Corrigida em 2026-05-14

O perfil retornado por `analyze_student()` usa strings com emoji. A verificação correta:

```python
# CORRETO (pós correção):
if "CRÍTICO" in profile:
    profile_color = DANGER   # vermelho
elif "EM RISCO" in profile:
    profile_color = WARN     # laranja
else:
    profile_color = SUCCESS  # verde

# ERRADO (antes da correção) — nunca correspondia:
if profile == "Emrisco":     # string que nunca existe
    ...
```

Os valores reais retornados por `analyze_student()` são:
- `"🔴 CRÍTICO - Atenção imediata"` (avg_risk > 0,70)
- `"🟡 EM RISCO - Acompanhamento"` (avg_risk > 0,40)
- `"🟢 SEGURO - Desempenho normal"` (padrão)

---

## 5. Cards de Disciplina — Dados Exibidos

Cada `DisciplineCard` recebe `disc_data` com:

```python
{
    "id": 3,
    "nome": "Matemática",
    "n1": 7.0,  "n2": 6.5,  "n3": 8.0,  "n4": None,
    "media": 7.1,
    "status": 2,               # 0=Reprovado, 1=Recuperação, 2=Aprovado
    "status_name": "Aprovado",
    "status_color": "#2E7D32",
    "risk_score": 0.29,        # 0=seguro, 1=em risco
    "trend": "->",             # "[+]", "[-]", "->"
    "prognosis": "as_expected",# "will_improve", "will_decline", "stable", ...
    "predicted_status": 2,
    "predicted_proba": [0.02, 0.11, 0.87],
    "explicacao": "Aluno mantém bom desempenho."
}
```

---

## 6. Ícones de Prognóstico

| Chave `prognosis` | Label exibido | Trigger |
|---|---|---|
| `will_improve` | `↗ Vai Melhorar` | slope_pct > 20% ou modelo prevê acima do atual |
| `will_decline` | `↘ Vai Piorar` | slope_pct < -20% ou modelo prevê abaixo |
| `stable` | `→ Estável` | slope_pct -20% a +20%, modelo confirma |
| `better_than_expected` | `↑ Superou Previsão` | N3+N4 melhor que predição de N1+N2 |
| `worse_than_expected` | `↓ Abaixo do Previsto` | N3+N4 pior que predição de N1+N2 |
| `as_expected` | `= Como Previsto` | N3+N4 igual à predição de N1+N2 |

---

## 7. Filtros de Exibição

O usuário pode filtrar os cards por status:

| Botão | `filter_var` | Matérias exibidas |
|---|---|---|
| Todos | `"all"` | Todas as matérias |
| Aprovados | `"aprovados"` | status == 2 |
| Recuperação | `"recuperacao"` | status == 1 |
| Reprovados | `"reprovados"` | status == 0 |

---

## 8. Dependências

```python
from gui_ml_integration import DisciplinePerformanceAnalyzer, MLModelLoader
# DisciplinePerformanceAnalyzer → analyze_student()
# MLModelLoader → carrega RF_M1/M2/M3 dos .pkl

import cads
# cads.DB_PATH → passado para analyze_student (mas ignorado internamente)
# cads.get_salas(), cads.get_alunos() → populam os comboboxes
```

---

## 9. Problema Crítico — Features Incorretas no Modelo

A página passa `db_path=cads.DB_PATH` para `analyze_student()`, mas este parâmetro é **ignorado** — sempre usa `cads.get_conn()`. Isso não causa erro mas é uma interface enganosa.

Mais grave: o `analyze_student()` monta as features para o modelo assim (linhas 285-295):
```python
slope     = (n2 - n1)               # diferença simples, NÃO regressão
variancia = abs(n1 - n2)            # absoluto, NÃO desvio padrão
media_norm = (n1_raw + n2_raw) / 2 / 10  # apenas 2 notas

features_pred = [n1, n2, 0, 0, slope, variancia, media_norm, 0.5, 0.5]
#                                                              ^^^  ^^^
#                                               serie_num_norm=0.5 (hardcoded!)
#                                               pct_materias_ok=0.5 (hardcoded!)
```

O modelo RF_M3 foi treinado com 9 features reais; na predição em tempo real recebe features simplificadas. Ver [Débitos Técnicos — DT-01](<../18 - Refatorações Necessárias/Débitos Técnicos Identificados.md>).

---

## 10. Relação com Arquivo de Documentação de Código

Para detalhes de cada método (assinaturas, calls, sequências), ver a documentação de código:

[gui_predicoes_improved.py.md (07 - Código)](../../07%20-%20Código/gui_predicoes_improved.py.md)

---

## Links

- [[gui ml integration py — Motor de Predição]]
- [[Arquitetura Modular — Visão Geral]]
- [[Débitos Técnicos Identificados]]
- [[M3 — Modelo de Produção (Após N3)]]
- [[Mapeamento Teoria-Código]]
