<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0221,40:1a0533,70:2d1b69,100:4a0e8f&height=220&section=header&text=EduNotas&fontSize=62&fontColor=e879f9&animation=twinkling&fontAlignY=38&desc=Sistema%20Escolar%20com%20Machine%20Learning&descAlignY=60&descAlign=50&descSize=20&descColor=c084fc" width="100%" />

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=2800&pause=900&color=A855F7&center=true&vCenter=true&random=false&width=580&lines=Previs%C3%A3o+de+desempenho+acad%C3%AAmico+com+Random+Forest;94%25+de+acur%C3%A1cia+no+modelo+RF_M3;Detecta+data+leakage+automaticamente;Python+%C2%B7+scikit-learn+%C2%B7+tkinter+%C2%B7+SQLite" alt="Typing SVG" />

<br/><br/>

![Python](https://img.shields.io/badge/Python-3.8+-8b5cf6?style=flat-square&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-7c3aed?style=flat-square&logo=scikitlearn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-6d28d9?style=flat-square&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/status-produção-4ade80?style=flat-square)
![Accuracy](https://img.shields.io/badge/acurácia_RF_M3-94%25-a855f7?style=flat-square)

</div>

---

## O que é

Aplicativo desktop para gestão escolar que usa **Machine Learning** para prever — com antecedência — se cada aluno será **Aprovado**, ficará em **Recuperação** ou será **Reprovado**. Permite ao professor intervir antes que seja tarde.

```
Notas parciais (N1, N2, N3)
        ↓
  9 features calculadas
  (slope, variância, contexto)
        ↓
  Random Forest  →  Aprovado / Recuperação / Reprovado
        ↓
  Dashboard visual com prognóstico por disciplina
```

---

## Modelos

<div align="center">

| Modelo | Momento | Features | Acurácia |
|:---:|:---:|:---:|:---:|
| RF_M1 | Após N1 | 1 | ~55% |
| RF_M2 | Após N2 | 4 | ~70% |
| **RF_M3** ⭐ | **Após N3** | **9** | **~94%** |

</div>

> O RF_M3 usa `n1_norm`, `n2_norm`, `n3_norm`, `slope_notas`, `variancia_notas`, `media_geral_aluno`, `serie_num_norm`, `pct_materias_ok` e `media_turma_norm` — sem data leakage.

---

## Início Rápido

```bash
# Instalar dependências
pip install -r 01-CORE/requirements.txt

# Rodar aplicação
python 03-GUI/gui_escola.py

# Ou treinar modelos direto pelo terminal
python 02-ML/train_simple.py
```

---

## Estrutura

```
TGI-CODES/
├── 01-CORE/     → cads.py — banco SQLite + geração de features
├── 02-ML/       → modelos treinados, pipeline, dashboard ML
├── 03-GUI/      → app principal e todas as páginas tkinter
├── 04-DOCS/     → documentação completa
├── 05-TESTS/    → testes e scripts de debug
├── 06-OUTPUT/   → arquivos gerados (JSON, CSV, Excel)
└── Obsidian/    → vault de notas do projeto
```

---

## Documentação

<div align="center">

| | Documento | Conteúdo |
|:---:|---|---|
| 🚀 | [Início Rápido](04-DOCS/INICIO_RAPIDO.md) | Rodar em 5 minutos |
| 📊 | [Resumo Executivo](04-DOCS/RESUMO_EXECUTIVO.md) | O que foi construído |
| 🏗️ | [Arquitetura](04-DOCS/ARQUITETURA_SISTEMA.md) | Fluxo e componentes |
| 🧮 | [Cálculos de ML](04-DOCS/DOCUMENTACAO_CALCULOS.md) | Features e fórmulas |
| 📁 | [Estrutura do Projeto](04-DOCS/ESTRUTURA_PROJETO.md) | Organização de pastas |
| 📖 | [Guia Completo](04-DOCS/GUIA_COMPLETO.md) | Tutorial detalhado |
| 🤖 | [ML README](04-DOCS/ML_README.md) | Referência técnica |
| 📑 | [Índice Geral](04-DOCS/INDICE_DOCUMENTACAO.md) | Mapa de toda a doc |

</div>

---

## Stack

<div align="center">

<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" height="40" title="Python" />
&nbsp;
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sqlite/sqlite-original.svg" height="40" title="SQLite" />
&nbsp;
<img src="https://skillicons.dev/icons?i=sklearn" height="40" title="scikit-learn" />
&nbsp;
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg" height="40" title="pandas" />
&nbsp;
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg" height="40" title="NumPy" />
&nbsp;
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/matplotlib/matplotlib-original.svg" height="40" title="Matplotlib" />

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4a0e8f,40:2d1b69,70:1a0533,100:0d0221&height=130&section=footer" width="100%" />
