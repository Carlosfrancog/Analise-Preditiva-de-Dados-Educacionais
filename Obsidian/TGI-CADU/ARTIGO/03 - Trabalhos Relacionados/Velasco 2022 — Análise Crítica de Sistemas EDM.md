---
tags: [artigo, trabalhos-relacionados, velasco2022, analise-critica, etica]
aliases: [Velasco 2022 — Análise Crítica]
created: 2026-05-16
---

# Velasco (2022) — Análise Crítica de Sistemas de Predição Escolar

[[INDEX - ARTIGO|← Índice]] | [[Análise Comparativa dos Trabalhos]] | [[Romero e Ventura 2020 — EDM Survey]]

---

## Referência

VELASCO, [nome completo a verificar]. **[Título completo a verificar — análise crítica de sistemas de predição/EDM].** [Dissertação/Artigo], 2022.

> [!WARNING] Referência incompleta
> O artigo do EduPredict cita Velasco (2022) mas os dados completos de publicação não estão disponíveis no texto consultado. Verificar antes de submissão.

---

## 1. Contribuição Principal

Velasco (2022) se diferencia dos outros trabalhos relacionados por ser uma **análise crítica** — não implementa um sistema, mas avalia os riscos e limitações de sistemas de predição já existentes.

**Foco principal:** qualidade dos dados, viés algorítmico e implicações éticas de sistemas ML em educação.

---

## 2. Posicionamento em Relação ao EduPredict

| Dimensão | Velasco (2022) | EduPredict |
|---|---|---|
| **Tipo de contribuição** | Análise crítica | Sistema implementado |
| **Data leakage** | Menciona como risco | ✅ Detecta e remove automaticamente |
| **Viés algorítmico** | Analisa em profundidade | ❌ Não discutido |
| **Explicabilidade** | Recomenda SHAP/LIME | ❌ Apenas feature importance global |
| **LGPD/Ética** | Análise detalhada | ❌ Não abordado |
| **Frequência** | N/A (análise teórica) | ❌ Ausente |

---

## 3. Contribuições para o EduPredict

O trabalho de Velasco funciona como "checklist de riscos" que o EduPredict deveria ter consultado. As lacunas identificadas por Velasco que o EduPredict não endereça:

### Viés Algorítmico
Um modelo treinado em dados históricos reproduz os padrões históricos — incluindo desigualdades. Se historicamente alunos de determinada série têm mais reprovações por falta de recursos (não por capacidade), o modelo aprenderá a "prever reprovação" para aquela série, potencialmente criando um ciclo de expectativas baixas.

O EduPredict usa `serie_num_norm` como feature — um proxy de nível escolar que pode carregar esse viés histórico.

### Transparência Algorítmica
Velasco enfatiza que sistemas de predição devem explicar suas decisões de forma compreensível para professores e responsáveis. O EduPredict fornece feature importance global mas não explicabilidade por aluno (SHAP).

### Direito ao Contraditório
Alunos (e responsáveis) deveriam ter o direito de questionar uma predição desfavorável. O EduPredict não implementa nenhum mecanismo de contestação.

---

## 4. Lacunas que Velasco Identifica em Toda a Literatura

1. **Ausência de avaliação de impacto real** — sistemas são avaliados por acurácia, não por impacto pedagógico real (o modelo melhorou o desempenho dos alunos?)
2. **Falta de participação dos professores no design** — sistemas criados por engenheiros sem input de educadores
3. **Generalização indevida** — modelos treinados em uma escola aplicados em outras
4. **Ausência de protocolo de desativação** — o que fazer quando o modelo começa a errar sistematicamente?

---

## 5. Diferencial do EduPredict vs Velasco

O EduPredict responde parcialmente à crítica de Velasco sobre data leakage — que Velasco identifica como problema frequente na literatura. A detecção automática de leakage é a resposta mais direta ao ponto crítico de Velasco sobre "qualidade metodológica dos estudos de EDM".

---

## Links

- [[Análise Comparativa dos Trabalhos]]
- [[Limitações Gerais do Artigo]]
- [[LGPD e Ética no EduPredict]]
- [[SHAP — Explicabilidade Local por Aluno]]
- [[Análise Crítica do TGI]]
