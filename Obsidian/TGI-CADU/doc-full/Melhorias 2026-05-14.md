---
tags:
  - projeto
  - melhorias
  - bugfix
  - tgi-codes
created: 2026-05-14
---

# Melhorias — 14/05/2026

[[MOC - TGI-CODES|← Voltar ao índice]] | [[Roadmap]] | [[Visão Geral]]

> [!SUCCESS] Sessão de melhorias de UI e correção de bugs
> Quatro itens implementados: 1 bug crítico de status, 1 melhoria de dashboard, 1 correção de acentuação/lógica e 1 melhoria de UX.

---

## 1. Bug Crítico — Lógica de Status de Notas

**Arquivos:** [[gui_escola.py]] → `NotasPage._load_notas()` e `RelatorioPage._load()`

### Problema

A lógica original tratava **qualquer** média abaixo de 6 como "Recuperação", ignorando completamente o estado "Reprovado":

```python
# ANTES — errado
status = "Aprovado" if media >= 6 else "Recuperação" if isinstance(media, float) else "-"
```

### Correção

```python
# DEPOIS — correto
if isinstance(media, float):
    if media >= 6:
        status, tag = "Aprovado",    "aprov"   # verde
    elif media >= 5:
        status, tag = "Recuperação", "recup"   # amarelo ← novo
    else:
        status, tag = "Reprovado",   "reprov"  # vermelho
else:
    status, tag = "-", "alt" if i % 2 else ""
```

### O que mudou no código

| Arquivo | Mudança |
|---|---|
| `gui_escola.py` | Adicionada constante `WARN_L = "#FFF8E1"` (amarelo claro) |
| `NotasPage._build()` | Adicionada tag `"recup"` com `background=WARN_L` |
| `RelatorioPage._build()` | Adicionada tag `"recup"` com `background=WARN_L` |
| `NotasPage._load_notas()` | Lógica de status corrigida |
| `RelatorioPage._load()` | Lógica de status corrigida |

> [!WARNING] Impacto
> Antes da correção, alunos com média < 5 apareciam como "Recuperação" nas páginas Notas e Relatório. O módulo ML já calculava corretamente (via `status_encoded`). A interface estava inconsistente com o banco.

---

## 2. Dashboard — Stats de IA e Alunos em Risco

**Arquivo:** [[gui_escola.py]] → `DashboardPage.refresh()` e novo método `_build_ml_status()`

### O que foi adicionado

**4º card de estatística:** "Em Risco (ML)" — conta registros em `ml_features` com `status_encoded IN (0, 1)`.

**Barra de status dos modelos IA:** Lê os arquivos `RF_M*_metadata.json` em `02-ML/ml_models/` e exibe acurácia de cada modelo treinado. Aparece automaticamente — oculta se nenhum modelo existir.

**Coluna "Em Risco" na tabela de turmas:** Query estendida com `LEFT JOIN ml_features` para mostrar quantos registros de risco cada sala tem.

```sql
-- Query nova no DashboardPage.refresh()
SELECT s.nome, s.codigo, COUNT(DISTINCT a.id) as cnt,
       SUM(CASE WHEN f.status_encoded IN (0,1) THEN 1 ELSE 0 END) as risco
FROM salas s
LEFT JOIN alunos a ON a.sala_id = s.id
LEFT JOIN ml_features f ON f.aluno_id = a.id
GROUP BY s.id ORDER BY s.id
```

> [!TIP] Dependência
> O card "Em Risco" mostra `0` quando `ml_features` está vazia (antes de [[cads.py#gerar_features_ml|gerar features]]). Incentiva o usuário a rodar a geração de features.

---

## 3. Predições — Acentuação e Lógica de Perfil

**Arquivo:** [[gui_predicoes_improved.py]]

### Strings corrigidas

| Antes | Depois |
|---|---|
| `"Predicoes de Desempenho"` | `"Predições de Desempenho"` |
| `"[Pred]"` (icon) | `"🎯"` |
| `"Identifique deficits logo no comeco..."` | `"Identifique déficits logo no início..."` |
| `"Recuperacao"` (filtro) | `"Recuperação"` |
| `"Atencao"` (messagebox) | `"Atenção"` |
| `"Analise por Disciplina (layout horizontal)"` | `"Análise por Disciplina"` |
| `"RECOMENDACOES"` | `"RECOMENDAÇÕES"` |
| `"Reforco imediato"` | `"reforço imediato"` |
| `"Manutencao:"` | `"Manutenção positiva:"` |
| `"SUSPENSAO"` | `"SUSPENSÃO"` |
| `"PREVENCAO"` | `"PREVENÇÃO"` |
| `"Recuperacao"` (status card) | `"Recuperação"` |

### Bug de lógica — cor do perfil

O código verificava strings que nunca existiam nos dados reais:

```python
# ANTES — strings erradas, nunca coloriam
if "Emrisco" in analise['profile']:      # profile nunca continha "Emrisco"
    profile_color = DANGER
elif "Equilibrado" in analise['profile']: # nem "Equilibrado"
    ...
```

O [[gui_ml_integration.py#analyze_student|DisciplinePerformanceAnalyzer]] retorna:
- `"🔴 CRÍTICO - Atenção imediata"` (risk > 0.7)
- `"🟡 EM RISCO - Acompanhamento"` (risk > 0.4)
- `"🟢 SEGURO - Desempenho normal"` (padrão)

```python
# DEPOIS — correto
if "CRÍTICO" in profile:
    profile_color = DANGER    # vermelho
elif "EM RISCO" in profile:
    profile_color = WARN      # laranja
else:
    profile_color = SUCCESS   # verde
```

### Ícones de prognóstico melhorados

| Antes | Depois |
|---|---|
| `"[*] Vai Melhorar"` | `"↗ Vai Melhorar"` |
| `"[!] Vai Piorar"` | `"↘ Vai Piorar"` |
| `"[-] Estavel"` | `"→ Estável"` |
| `"[+] Superou Previsao"` | `"↑ Superou Previsão"` |
| `"[-] Abaixo Previsao"` | `"↓ Abaixo do Previsto"` |
| `"[-] Como Previsto"` | `"= Como Previsto"` |

---

## 4. UX — Tratamento de Erro para Modelos não Treinados

**Arquivo:** [[gui_predicoes_improved.py]] → `_load_student_analysis()`

### Problema

Quando nenhum modelo ML estava treinado, o sistema analisava o aluno silenciosamente sem nenhuma previsão, sem avisar o usuário.

### Solução

Dialog informativo antes de executar a análise:

```python
if not self.ml_loader.is_available("RF_M3") and \
   not self.ml_loader.is_available("RF_M2") and \
   not self.ml_loader.is_available("RF_M1"):
    resp = messagebox.askyesno(
        "Modelos não treinados",
        "Nenhum modelo de IA foi treinado ainda.\n\n"
        "A análise será feita apenas com as notas atuais, sem previsões.\n\n"
        "Deseja continuar mesmo assim?\n"
        "(Para treinar, acesse 🤖 Machine Learning)"
    )
    if not resp:
        return
```

Também adicionado `try/except` em volta de `DisciplinePerformanceAnalyzer.analyze_student()` com mensagem de erro descritiva.

> [!NOTE] db_path
> O parâmetro `db_path` de `analyze_student()` foi alterado de `"escola.db"` para `None` — o método internamente já usa [[cads.py#get_conn|cads.get_conn()]] com o path absoluto correto, tornando o parâmetro irrelevante.

---

## Links Relacionados

- [[gui_escola.py]] — arquivo principal modificado
- [[gui_predicoes_improved.py]] — página de predições modificada
- [[gui_ml_integration.py#analyze_student]] — analisador de desempenho
- [[cads.py#gerar_features_ml]] — geração das features usadas no dashboard
- [[Roadmap]] — itens concluídos marcados
- [[Componentes e Páginas]] — documentação atualizada das páginas GUI
