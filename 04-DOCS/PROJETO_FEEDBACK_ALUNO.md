# 📋 PROJETO: Sistema de Feedback de Aluno & Retreino de Modelos

**Data:** 14 de Abril de 2026  
**Status:** Design & Planning  
**Versão:** 1.0

---

## 🎯 Objetivo

Criar um sistema que permita:
1. **Revisar** previsões do modelo para cada aluno/matéria
2. **Confirmar** se as previsões estão corretas ("agradáveis/apropriadas")
3. **Editar** notas e informações se necessário
4. **Salvar** feedback estruturado no banco de dados
5. **Exportar** dados confirmados (dump)
6. **Retreinar** modelos com dados validados pelo usuário

---

## 📊 Arquitetura Geral

```
┌─────────────────────────────────────────────────────────┐
│                   FEEDBACK ALUNO                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐     ┌──────────────────┐        │
│  │  REVISAR DADOS   │ → │  CONFIRMAR / EDIT │ →       │
│  │ (Cards visuais)  │    │  (Formulários)   │        │
│  └──────────────────┘     └──────────────────┘        │
│           ↓                          ↓                 │
│  ┌──────────────────┐     ┌──────────────────┐        │
│  │ SALVAR FEEDBACK  │ → │   GERAR DUMP     │ →       │
│  │  (BD)            │    │   (CSV/JSON)     │        │
│  └──────────────────┘     └──────────────────┘        │
│                                     ↓                 │
│                          ┌──────────────────┐        │
│                          │  RETREINAR ML    │        │
│                          │  (Novo modelo)   │        │
│                          └──────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Banco de Dados - Schema

### Nova Tabela: `student_feedback`

```sql
CREATE TABLE student_feedback (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Identificação
    aluno_id              INTEGER NOT NULL,
    materia_id            INTEGER NOT NULL,
    aluno_nome            TEXT,
    materia_nome          TEXT,
    
    -- Dados originais (snapshot)
    n1_original           REAL,
    n2_original           REAL,
    n3_original           REAL,
    n4_original           REAL,
    media_pond_original   REAL,
    
    -- Dados editados (se necessário)
    n1_editado            REAL,
    n2_editado            REAL,
    n3_editado            REAL,
    n4_editado            REAL,
    media_pond_editada    REAL,
    
    -- Previsão original do modelo
    status_previsto       TEXT,  -- "Aprovado", "Recuperação", "Reprovado"
    score_confianca       REAL,  -- Confiança 0-100%
    
    -- Feedback do usuário
    status_confirmado     TEXT,  -- Oque usuário acha: "Correto", "Incorreto", "Incerto"
    foi_editado           BOOLEAN,
    motivo_edicao         TEXT,  -- Por que editou?
    
    -- Processamento
    incluir_retrotreinamento BOOLEAN DEFAULT 0,
    data_feedback         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    UNIQUE(aluno_id, materia_id),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
);
```

### Alterações em Tabelas Existentes

**ml_features**: Adicionar coluna
```sql
ALTER TABLE ml_features ADD COLUMN 
    feedback_status TEXT DEFAULT NULL;  -- Referência ao feedback
```

---

## 🎨 UI/UX - Layout da Página

### Divisão da Interface

```
┌─────────────────────────────────────────────────────────────┐
│  📋 FEEDBACK DE ALUNO                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Filtros:  [Turma ▼]  [Status Previsto ▼]  [⏮ Anterior]   │
│                                             [Próximo ⏭]     │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┤
│  │ ALUNO: João Silva [Matrícula: 6F0001]                   │
│  │ MATÉRIA: Matemática                                     │
│  │ TURMA: 6º Fundamental                                   │
│  └─────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐    ┌──────────────────┐             │
│  │ 📊 NOTAS         │    │ 🤖 PREVISÃO      │             │
│  ├──────────────────┤    ├──────────────────┤             │
│  │ N1: [8.5______]  │    │ Status: Aprovado │             │
│  │ N2: [7.2______]  │    │ Confiança: 94%   │             │
│  │ N3: [9.0______]  │    │                  │             │
│  │ N4: [8.8______]  │    │ [Editar]         │             │
│  │                  │    │                  │             │
│  │ Média: 8.4       │    │ [Visualizar IA]  │             │
│  └──────────────────┘    └──────────────────┘             │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐│
│  │ ✅ CONFIRMAR PREVISÃO                                ││
│  ├───────────────────────────────────────────────────────┤│
│  │                                                       ││
│  │ O modelo previu "APROVADO" para este aluno.         ││
│  │ Você concorda com essa previsão?                     ││
│  │                                                       ││
│  │ ◯ Correto  ◯ Incorreto  ◯ Incerto                   ││
│  │                                                       ││
│  │ Motivo (se editou): [Falou com professor...]         ││
│  │                     [≥ 200 caracteres                ││
│  │                     [                                 ││
│  │                     [                                 ││
│  │                                                       ││
│  │ ☐ Incluir este registro no retreino                 ││
│  │                                                       ││
│  │ [ SALVAR ]  [ PRÓXIMO ]  [ CANCELAR ]                ││
│  └───────────────────────────────────────────────────────┘│
│                                                             │
│  Status: 24/150 processados (16%)  [████░░░░░░░]           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Dados

### 1. FASE: CARREGAR DADOS

```
Usuário clica: "📋 Feedback Aluno"
    ↓
Carregar todos os registros de ml_features
    ↓
Filtrar por status previsto (Aprovado/Reprovado/Incerto)
    ↓
Buscar feedback já salvo (se existe)
    ↓
Exibir primeiro aluno que NÃO tem feedback
```

### 2. FASE: REVISAR & EDITAR

```
Usuário vê:
  - Notas originais (N1, N2, N3, N4)
  - Média ponderada
  - Previsão do modelo + confiança
  
Opções do usuário:
  a) Confirmar ("Correto")  → Salva feedback direto
  b) Marcar como incorreto  → Abre form de edição
  c) Editar notas           → Recalcula média → Permite salvar
  d) Incerto               → Marca para revisão manual depois
```

### 3. FASE: SALVAR FEEDBACK

```
Ao clicar SALVAR:
  1. Validar dados (notas 0-10)
  2. Recalcular média se editado
  3. Inserir/atualizar em student_feedback
  4. Marcar ml_features com status feedback
  5. Mostrar confirmação visual
  6. Carregar próximo aluno
```

### 4. FASE: GERAR DUMP

```
Após revisar todos (ou clique "Gerar Dump"):
  1. Query: SELECT * FROM student_feedback 
     WHERE status_confirmado IS NOT NULL
  2. Exportar para:
     - CSV: feedback_YYYY-MM-DD.csv
     - JSON: feedback_YYYY-MM-DD.json
  3. Incluir metadados:
     - Data geração
     - Qtd registros
     - % confirmados
     - Alterações feitas
```

### 5. FASE: RETREINAR

```
Usuário clica: "🚀 Retreinar com Feedback"
    ↓
Validar: Há dados confirmados?
    ↓
Carregar registros marcados para retreino
    ↓
Construir novo dataset (feedback + dados validados)
    ↓
Treinar RF_M1, M2, M3 com novo dataset
    ↓
Comparar acurácia (antes vs depois)
    ↓
Salvar novos modelos (com versão)
    ↓
Popup com resultados
```

---

## 📁 Estrutura de Arquivos

```
04-DOCS/
├── PROJETO_FEEDBACK_ALUNO.md          (este arquivo)
└── [arquivos de design futuros]

02-ML/
├── gui_feedback_aluno.py              (🆕 NOVA PAGE)
├── feedback_processor.py               (🆕 Processador de feedback)
├── dump_generator.py                   (🆕 Exportador de dados)
└── retrain_with_feedback.py           (🆕 Retreino com feedback)

03-GUI/
├── gui_escola.py                      (modificar para adicionar página)
└── gui_predicoes.py                   (BasePage)

01-CORE/
└── cads.py                            (adicionar funções de feedback)
```

---

## 🧩 Componentes Principais

### 1. **FeedbackProcessorPage** (gui_feedback_aluno.py)

```
Responsabilidades:
- Carregar ml_features
- Exibir cards com notas e previsões
- Coletar feedback do usuário
- Salvar em student_feedback
- Navegação prev/próx
- Contador de progresso

Métodos:
- __init__(parent, app)
- _load_data()
- _load_next_aluno()
- _display_aluno()
- _save_feedback()
- _apply_filters()
```

### 2. **FeedbackProcessor** (feedback_processor.py)

```
Responsabilidades:
- Validações de dados
- Cálculos de média ponderada
- Verificar duplicatas
- Marcar para retreino

Métodos:
- validate_notes(n1, n2, n3, n4)
- calculate_media(n1, n2, n3, n4, pesos)
- is_feedback_valid(feedback_dict)
- mark_for_retraining(aluno_id, materia_id)
```

### 3. **DumpGenerator** (dump_generator.py)

```
Responsabilidades:
- Query feedback confirmado
- Exportar CSV/JSON
- Gerar relatório
- Calcular estatísticas

Métodos:
- get_feedback_data()
- export_csv(output_path)
- export_json(output_path)
- get_statistics()
- generate_report()
```

### 4. **RetrainWithFeedback** (retrain_with_feedback.py)

```
Responsabilidades:
- Carregar dados de feedback
- Combinar com dados originais
- Balancear dataset
- Treinar modelos
- Comparar resultados

Métodos:
- load_feedback_data()
- build_training_dataset()
- compare_models(model_old, model_new)
- save_versioned_models()
```

---

## 🔒 Banco de Dados - Operações

### Inserir Feedback

```python
INSERT INTO student_feedback (
    aluno_id, materia_id, aluno_nome, materia_nome,
    n1_original, n2_original, n3_original, n4_original,
    media_pond_original,
    n1_editado, n2_editado, n3_editado, n4_editado,
    media_pond_editada,
    status_previsto, score_confianca,
    status_confirmado, foi_editado, motivo_edicao,
    incluir_retrotreinamento
) VALUES (...)
```

### Consultar Feedback Pendente

```python
SELECT mf.*, sf.status_confirmado
FROM ml_features mf
LEFT JOIN student_feedback sf 
    ON mf.aluno_id = sf.aluno_id 
    AND mf.materia_id = sf.materia_id
WHERE sf.id IS NULL
ORDER BY mf.aluno_nome, mf.materia_nome
LIMIT 1
```

### Exportar para Retreino

```python
SELECT 
    n1, n2, n3, n4,
    media_ponderada,
    n1_norm, n2_norm, n3_norm, n4_norm,
    media_pond_norm,
    slope_notas, variancia_notas,
    media_geral_aluno, serie_num_norm,
    media_turma_norm,
    status_encoded
FROM ml_features mf
JOIN student_feedback sf 
    ON mf.aluno_id = sf.aluno_id
WHERE sf.status_confirmado = 'Correto'
    OR (sf.status_confirmado = 'Correto' AND sf.foi_editado = 1)
```

---

## 🔄 Ciclo Completo

```
SEMANA 1: Revisar dados
┌─────────────────────┐
│ Segunda: 150 alunos │ → 24 processados
│ Terça: 150 alunos   │ → 48 processados (32%)
│ Quarta: 150 alunos  │ → 72 processados (48%)
│ Quinta: 150 alunos  │ → 120 processados (80%)
│ Sexta: 150 alunos   │ → 150 processados (100%)
└─────────────────────┘
        ↓
    GERAR DUMP
┌──────────────────────────┐
│ feedback_2026-04-14.csv  │ (150 registros)
│ feedback_2026-04-14.json │ (metadados)
│ relatorio_feedback.txt   │ (análise)
└──────────────────────────┘
        ↓
   RETREINAR MODELOS
┌────────────────────┐
│ RF_M1': 87.2%      │ (+3.4%)
│ RF_M2': 96.1%      │ (+1.6%)
│ RF_M3': 97.5%      │ (+1.8%)
└────────────────────┘
```

---

## 🎯 Casos de Uso

### Caso 1: Feedback Rápido (Correto)
```
1. Usuário vê: "João Silva - Matemática - Aprovado (94%)"
2. Clica: ◯ Correto
3. ☐ Incluir no retreino
4. [SALVAR]
5. Próximo aluno automático
```

### Caso 2: Feedback com Edição
```
1. Usuário vê: "Maria - Português - Reprovado"
2. Acha estranho, edita: N4 de 4.2 → 5.8
3. Média recalcula: 4.5 → 5.2
4. Clica: ◯ Incorreto (deveria ser Recuperação)
5. Motivo: "Professora confirmou nota errada"
6. ☑ Incluir no retreino (com notas corretas)
7. [SALVAR]
```

### Caso 3: Feedback Incerto
```
1. Usuário vê: "Pedro - Química - Recuperação"
2. Não tem certeza
3. Clica: ◯ Incerto
4. Motivo: "Preciso falar com o aluno"
5. Marca: [PARA REVISÃO]
6. ☐ Não incluir retreino (por enquanto)
7. [SALVAR]
```

---

## 📈 Relatórios & Estatísticas

### Relatório de Feedback

```
╔════════════════════════════════════════╗
║   RELATÓRIO DE FEEDBACK ALUNO         ║
║   Data: 14/04/2026                    ║
╚════════════════════════════════════════╝

📊 RESUMO:
  Total alunos/matérias: 150
  Processados: 150 (100%)
  
  ✅ Corretos:        120 (80%)
  ❌ Incorretos:       20 (13%)
  ❓ Incertos:          10 (7%)

📝 EDIÇÕES:
  Registros editados:  20
  Mudanças de status:  15
  
  Reprovado → Recuperação: 8
  Recuperação → Aprovado:  4
  Aprovado → Recuperação:  3

🎯 PARA RETREINO:
  Registros selecionados: 130 (86%)
  Com edições:            20
  Sem edições:           110

📅 TIMELINE:
  Primeira revisão: 14/04
  Última revisão:   18/04
  Data exportação:  18/04 14:30
```

---

## ⏱️ Cronograma de Implementação

### Fase 1: Backend (3-4 dias)
- [ ] Criar tabela `student_feedback` em cads.py
- [ ] Implementar `FeedbackProcessor`
- [ ] Implementar `DumpGenerator`
- [ ] Testes unitários

### Fase 2: Frontend (3-4 dias)
- [ ] Criar `FeedbackProcessorPage` (GUI)
- [ ] Implementar navegação prev/próx
- [ ] Coletor de feedback
- [ ] Edição de notas com recálculo
- [ ] Testes de UI

### Fase 3: Retreino (2-3 dias)
- [ ] Implementar `RetrainWithFeedback`
- [ ] Integração com página ML
- [ ] Versionamento de modelos
- [ ] Comparação antes/depois
- [ ] Testes completos

### Fase 4: Documentação (1 dia)
- [ ] Guias de uso
- [ ] Exemplos práticos
- [ ] FAQ
- [ ] Troubleshooting

---

## 🔐 Constraints & Validações

### Validações de Notas
```
- Cada nota: 0.0 ≤ n ≤ 10.0
- Mínimo 1 nota preenchida
- Média calculada: (n1*0.20 + n2*0.25 + n3*0.25 + n4*0.30)
- Total pesos: sempre = 1.0
```

### Validações de Feedback
```
- status_confirmado: obrigatório ("Correto", "Incorreto", "Incerto")
- Se editado: motivo obrigatório (mín 10 caracteres)
- Se Incerto: não pode marcar para retreino
- Um único feedback por aluno/matéria (UNIQUE)
```

---

## 📌 Notas Importantes

1. **Integridade de Dados**
   - Sempre manter snapshot das notas originais
   - Nunca sobrescrever ml_features
   - Feedback é imutável após salvar

2. **Performance**
   - Carregar feedback sob demanda (lazy load)
   - Índices em (aluno_id, materia_id)
   - Cache de alunos/matérias já processados

3. **UX**
   - Contador de progresso sempre visível
   - Possibilidade de voltar (anterior)
   - Atalhos de teclado (Enter = próximo)
   - Auto-save parcial?

4. **Segurança**
   - Log de quem fez feedback
   - Data/hora de cada ação
   - Não permitir deletar feedback

---

## ✅ Checklist de Implementação

```
BACKEND:
  ☐ Tabela student_feedback criada
  ☐ FeedbackProcessor implementada
  ☐ CRUD feedback completo
  ☐ Validações funcionando
  ☐ Queries de exportação testadas

FRONTEND:
  ☐ Página FeedbackProcessorPage
  ☐ Layout cards/formulário
  ☐ Navegação prev/próximo
  ☐ Edição notas com recálculo
  ☐ Integração em gui_escola.py
  ☐ Estilos Dark Mode

RETREINO:
  ☐ RetrainWithFeedback implementada
  ☐ Dataset builder funcional
  ☐ Comparação modelos
  ☐ Versionamento
  ☐ Integração com página ML

TESTES:
  ☐ Testes unitários (20+ casos)
  ☐ Testes integração
  ☐ Testes UI/navegação
  ☐ Testes de dados
  ☐ Performance tests

DOCS:
  ☐ README_FEEDBACK.md
  ☐ GUIA_USUARIO_FEEDBACK.md
  ☐ API documentation
  ☐ Exemplos práticos
  ☐ Troubleshooting
```

---

## 🎓 Conclusão

O sistema de Feedback de Aluno fechará um ciclo completo:

```
Dados brutos → Revisão humana → Validação → Dados qualificados 
    ↓                                              ↓
Modelos iniciais                          Modelos melhorados
    ↓                                              ↓
94% acurácia                               97%+ acurácia
```

Isso transforma o sistema de **predição passiva** para **aprendizado ativo** com validação humana!

---

**Próximo passo:** Iniciar Fase 1 (Backend)
