# EduNotas — Sistema Escolar com Machine Learning

Sistema desktop em Python para gestão escolar com predição de desempenho acadêmico por Random Forest. Prevê se alunos serão **Aprovados**, ficarão em **Recuperação** ou serão **Reprovados** antes do fim do ano letivo.

---

## Início Rápido

```bash
pip install -r 01-CORE/requirements.txt
python 03-GUI/gui_escola.py
```

Ou para rodar o pipeline de ML diretamente:

```bash
python 02-ML/train_simple.py
```

> Guia completo em 5 passos → [04-DOCS/INICIO_RAPIDO.md](04-DOCS/INICIO_RAPIDO.md)

---

## Documentação

| Documento | Conteúdo |
|---|---|
| [Índice Geral](04-DOCS/INDICE_DOCUMENTACAO.md) | Mapa de toda a documentação |
| [Resumo Executivo](04-DOCS/RESUMO_EXECUTIVO.md) | O que foi construído e como funciona |
| [Início Rápido](04-DOCS/INICIO_RAPIDO.md) | Rodar o sistema em 5 minutos |
| [Guia Completo](04-DOCS/GUIA_COMPLETO.md) | Tutorial detalhado passo a passo |
| [Arquitetura do Sistema](04-DOCS/ARQUITETURA_SISTEMA.md) | Fluxo de dados e componentes |
| [Documentação de Cálculos](04-DOCS/DOCUMENTACAO_CALCULOS.md) | Features de ML, fórmulas e normalização |
| [Estrutura do Projeto](04-DOCS/ESTRUTURA_PROJETO.md) | Organização de pastas e módulos |
| [Guia de Predições](04-DOCS/GUIA_PREDICOES.md) | Como funciona o dashboard de predições |
| [README de ML](04-DOCS/ML_README.md) | Referência técnica dos módulos de ML |

---

## Estrutura de Pastas

```
TGI-CODES/
├── 01-CORE/          → cads.py (banco SQLite + geração de features)
├── 02-ML/            → modelos treinados, pipeline, dashboard de ML
├── 03-GUI/           → gui_escola.py (app principal) + páginas
├── 04-DOCS/          → documentação completa
├── 05-TESTS/         → testes e scripts de debug
├── 06-OUTPUT/        → arquivos gerados (JSON, CSV, Excel)
├── 07-BUILD/         → EduNotas.spec (PyInstaller)
└── Obsidian/         → vault de notas do projeto
```

---

## Modelos de ML

| Modelo | Quando usar | Features | Acurácia |
|---|---|---|---|
| RF_M1 | Após N1 | 1 | ~55% |
| RF_M2 | Após N2 | 4 | ~70% |
| **RF_M3** | **Após N3** | **9** | **~94%** |

> Detalhes → [Documentação de Cálculos](04-DOCS/DOCUMENTACAO_CALCULOS.md)

---

## Stack

- **Python 3.8+** / tkinter / SQLite
- **scikit-learn** — Random Forest
- **pandas** / numpy / matplotlib
- **PyInstaller** — build para `.exe`

---

## Notas do Projeto (Obsidian)

Documentação navegável em vault Obsidian em [`Obsidian/TGI-CADU/`](Obsidian/TGI-CADU/MOC%20-%20TGI-CODES.md), com notas interligadas cobrindo arquitetura, módulos e referência de código.
