---
tags: [artigo, melhorias, familia, transparencia, portal, lgpd]
created: 2026-05-16
---

# Portal de Transparência Familiar

[← Índice](<../INDEX - ARTIGO.md>) | [[LGPD e Ética no EduPredict]] | [[Módulo de Feedback Docente]] | [[SHAP — Explicabilidade Local por Aluno]]

---

## 1. Lacuna Atual

O EduPredict é um sistema **para professores**, não **para famílias**. Responsáveis legais:
- Não sabem que um modelo ML avalia seu filho
- Não têm acesso às predições
- Não podem contestar uma classificação desfavorável
- Não recebem alertas proativos

Isso viola tanto princípios éticos (transparência) quanto o Art. 20 da LGPD.

---

## 2. Conceito do Portal

Um portal web (ou relatório PDF gerado pela GUI) que oferece aos responsáveis:

```
Dashboard do Aluno — [Nome do Aluno]
Período: 2026 — 1º Semestre

Desempenho por Disciplina:
  Matemática:  N1=6.5 | N2=7.0 | Tendência: ↗ Melhorando
  Português:   N1=5.5 | N2=5.2 | Tendência: ↘ Atenção necessária
  História:    N1=8.0 | N2=7.5 | Tendência: → Estável

Avaliação do Sistema (linguagem simples):
  "Com base no desempenho observado até agora, o sistema identificou
   que Português merece atenção especial. Esta avaliação é baseada
   nas notas dos bimestres anteriores. Você pode contestar esta
   classificação conversando com o professor da matéria."

[Contestar avaliação] [Ver mais detalhes] [Baixar PDF]
```

---

## 3. Requisitos Técnicos para Implementação

### Opção A — Relatório PDF (menor investimento)
```python
# Adicionar a gui_escola.py:
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph

def gerar_relatorio_familiar(aluno_id, output_path):
    # Ler dados do banco
    # Gerar PDF com notas, tendências e aviso sobre IA
    pass
```

### Opção B — Portal Web (maior investimento)
```python
# Nova aplicação Flask/FastAPI:
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/aluno/<token>')
def portal_familiar(token):
    aluno_id = validar_token_acesso(token)
    dados = cads.get_aluno_completo(aluno_id)
    return render_template('portal.html', dados=dados)
```

O token é único por aluno e enviado via e-mail/SMS ao responsável pelo professor.

---

## 4. Requisito de Linguagem Simples

A linguagem técnica do EduPredict ("RF_M3", "risk_score=0.73", "slope_notas=-0.12") precisa ser traduzida para responsáveis:

| Técnico | Familiar |
|---|---|
| `risk_score > 0.70` → CRÍTICO | "Seu filho pode precisar de apoio em Matemática" |
| `slope_notas = -0.15` | "As notas de Português caíram nos últimos bimestres" |
| `predicted_status = 0` (Reprovado) | "O sistema identificou risco de reprovação — converse com o professor" |
| `proba = [0.03, 0.18, 0.79]` | "79% de probabilidade de aprovação em História" |

---

## 5. SHAP Familiar — Explicação da Predição

Para atender o Art. 20 da LGPD (direito de explicação sobre decisão automatizada), o portal deve mostrar os fatores da predição em linguagem acessível:

```
Por que o sistema está preocupado com Português?

Os 3 fatores principais:
1. 📉 Queda nas notas (peso: 35%)
   Sua nota caiu de 6.5 no 1º bimestre para 5.2 no 2º bimestre.

2. 📊 Média geral abaixo da turma (peso: 28%)
   Sua média em todas as matérias está um pouco abaixo da média da sala.

3. 📚 Histórico de dificuldade na matéria (peso: 20%)
   Nos bimestres anteriores, Português foi a matéria com menor nota.
```

Isso é basicamente SHAP (ver [[SHAP — Explicabilidade Local por Aluno]]) traduzido para linguagem não-técnica.

---

## 6. Mecanismo de Contestação — Art. 20 LGPD

O portal deve incluir mecanismo de contestação formal:

```
[Se você acredita que esta avaliação está incorreta, você tem o
 direito de solicitar revisão. Clique aqui para enviar uma
 solicitação de revisão ao professor responsável.]
```

No backend, isso gera um registro na tabela `feedback_docente` com `tipo='contestacao_familiar'`, notificando o professor.

---

## 7. Viabilidade no Contexto do TGI

O portal web está **fora do escopo do TGI** — o artigo não o menciona. É uma proposta para:
- Artigo de extensão (ver [[Insights para o Artigo de Extensão]])
- Projeto de Iniciação Científica separado

A versão PDF, porém, poderia ser implementada como extensão imediata do GUI atual com bibliotecas como `reportlab` ou `fpdf2`.

---

## Links

- [[LGPD e Ética no EduPredict]]
- [[Módulo de Feedback Docente]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Protocolo de Alertas EWS]]
- [[Insights para o Artigo de Extensão]]
- [[Velasco 2022 — Análise Crítica de Sistemas EDM]]
