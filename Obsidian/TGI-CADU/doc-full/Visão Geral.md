---
tags:
  - projeto
  - tgi-codes
created: 2026-05-13
---

# Visão Geral do Projeto

[[MOC - TGI-CODES|← Voltar ao índice]]

> [!NOTE] Status
> **Versão:** 2.1 | **Status:** Completo e pronto para produção | **Data:** Abril 2026

---

## O que é o TGI-CODES?

O **EduNotas** é um sistema desktop em Python para gestão escolar com predição de desempenho acadêmico por Machine Learning. Ele permite:

- Cadastrar alunos, matérias, salas e notas
- Prever se um aluno será **Aprovado**, ficará em **Recuperação** ou será **Reprovado**
- Treinar e configurar modelos de ML direto pela interface gráfica
- Exportar relatórios em Excel

---

## Estrutura de Pastas

```
TGI-CODES/
├── 01-CORE/        → cads.py (BD + CRUD), requirements.txt
├── 02-ML/          → modelos treinados, pipeline, dataset
├── 03-GUI/         → gui_escola.py, gui_predicoes_improved.py
├── 04-DOCS/        → toda a documentação em markdown
├── 05-TESTS/       → testes e scripts de debug
├── 06-OUTPUT/      → arquivos gerados (JSON, CSV, Excel)
├── 07-BUILD/       → EduNotas.spec, compilação PyInstaller
└── Obsidian/       → este vault
```

---

## Stack Técnico

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.8+ |
| GUI | tkinter |
| Banco de Dados | SQLite (`escola.db`) |
| ML | scikit-learn (Random Forest) |
| Dados | pandas, numpy |
| Visualização | matplotlib, seaborn |
| Explicabilidade | SHAP (opcional) |
| Build | PyInstaller |

---

## Estatísticas

- **~2.000 linhas** de código Python na GUI/ML avançada
- **~3.000 linhas** nos módulos de ML debug/pipeline
- **15.613 registros** no dataset de features
- **3 modelos** treinados (RF_M1, RF_M2, RF_M3)
- **94% acurácia** no modelo RF_M3

---

## Links Relacionados

- [[Arquitetura do Sistema]] — como os módulos se conectam
- [[Modelos RF (M1-M2-M3)]] — detalhes dos modelos
- [[Início Rápido]] — rodar o sistema agora
- [[Roadmap]] — próximos passos
