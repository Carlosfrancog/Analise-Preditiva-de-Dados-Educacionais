---
tags: [artigo, insights, trade-offs, decisoes, design]
created: 2026-05-16
---

# Decisões Técnicas e Trade-offs — EduPredict

[[INDEX - ARTIGO|← Índice]] | [[Análise Crítica do TGI]] | [[Limitações Gerais do Artigo]] | [[Plano de Artigo ABNT]]

> [!INFO] Análise das escolhas de design e seus trade-offs — o que justifica cada decisão e o que ela custa

---

## 1. Random Forest vs Outras Opções

**Decisão:** usar RandomForestClassifier do sklearn.

| Alternativa | Ganho | Custo |
|---|---|---|
| **Gradient Boosting (XGBoost)** | +1-2% acurácia | Mais hiperparâmetros, overfitting mais fácil |
| **Regressão Logística** | Mais interpretável | -8-10% acurácia, assume linearidade |
| **SVM** | Bom em alta dimensão | Lento, não fornece probabilidades diretamente |
| **Rede Neural** | Potencial de +2-3% | Precisa mais dados, caixa-preta total |

**Veredicto:** RF é a escolha correta para o contexto — robusto, interpretável em nível global, nativo para multiclasse, e sem necessidade de normalização extensiva.

---

## 2. Dataset Sintético vs Coleta Real

**Decisão:** gerar dados sintéticos em vez de coletar dados reais.

| Aspecto | Sintético (escolhido) | Real |
|---|---|---|
| **Facilidade** | ✅ Gerar em código | ❌ Processo longo (CEFET, LGPD) |
| **Volume** | ✅ Ilimitado | ❌ Dependente de escola parceira |
| **Controle** | ✅ Distribuição conhecida | ❌ Viés desconhecido |
| **Validade externa** | ❌ Questionável | ✅ Alta |
| **Reprodutibilidade** | ✅ Determinístico | ❌ Privacidade dificulta compartilhamento |

**Veredicto:** para um TGI, sintético é justificável. Para publicação científica, é uma limitação séria que precisa ser endereçada.

---

## 3. Três Modelos Temporais vs Um Modelo Único

**Decisão:** M1, M2, M3 separados vs um único modelo adaptativo.

| Abordagem | Prós | Contras |
|---|---|---|
| **3 modelos separados** (escolhido) | Simples, interpretável, permite comparação | 3× espaço em disco, 3× manutenção |
| **Modelo único com features opcionais** | Simples de manter | Pode confundir o modelo com features nulas |
| **Modelo sequencial (online learning)** | Atualiza conforme chegam dados | Complexo de implementar e validar |

**Veredicto:** 3 modelos separados é a escolha correta para o contexto acadêmico — permite análise explícita do trade-off antecedência × acurácia, que é contribuição metodológica real.

---

## 4. Pearson vs Métricas Mais Sofisticadas para Leakage

**Decisão:** usar correlação de Pearson com threshold 0,9 para detecção de leakage.

| Método | Detecta | Custo computacional |
|---|---|---|
| **Pearson** (escolhido) | Relações lineares | O(n × p) — trivial |
| **Spearman** | Relações monotônicas | O(n × p × log n) |
| **Informação Mútua** | Relações não-lineares | O(n × p²) — maior |
| **SHAP-based** | Impacto causal no modelo | O(T × L × M) — requer modelo treinado |

**Veredicto:** Pearson é suficiente para os casos identificados (media_pond_norm e n4_norm têm relações altamente lineares com o target). Para leakage indireto e não-linear, seria necessário complementar com Informação Mútua.

---

## 5. `class_weight='balanced'` vs SMOTE

**Decisão:** usar `class_weight='balanced'` para tratar desbalanceamento.

| Técnica | Como funciona | Resultado no recall de Recuperação |
|---|---|---|
| **Nada** | Ignora desbalanceamento | ~10-20% recall |
| **`class_weight='balanced'`** (escolhido) | Ajusta pesos | 62,2% recall |
| **SMOTE** | Gera amostras sintéticas | Estimado: 65-70% recall |
| **Limiar ajustado** | Threshold de decisão | Variável — depende do threshold |

**Veredicto:** `class_weight='balanced'` é a escolha mínima correta. SMOTE poderia melhorar o recall de Recuperação em ~3-8 pp com custo de implementação moderado.

---

## 6. SQLite vs PostgreSQL

**Decisão:** usar SQLite como banco de dados.

| Banco | Prós | Contras |
|---|---|---|
| **SQLite** (escolhido) | Zero configuração, arquivo único, portável | Sem suporte a múltiplos usuários concorrentes |
| **PostgreSQL** | Escalável, concorrência, JSON nativo | Requer servidor, configuração |
| **MySQL** | Popular, suporte amplo | Licença, requer servidor |

**Veredicto:** para um sistema desktop de escola pequena (1 instância por máquina), SQLite é a escolha correta. Se evoluir para um sistema web multi-escola, PostgreSQL seria necessário.

---

## 7. tkinter vs Framework Web

**Decisão:** usar tkinter para a interface desktop.

| Framework | Prós | Contras |
|---|---|---|
| **tkinter** (escolhido) | Zero dependências extras, Python puro | Visual datado, sem responsividade |
| **PyQt/PySide** | Visual moderno, mais widgets | Licença (PyQt) ou mais complexo |
| **Flask + HTML** | Web-native, acessível de qualquer lugar | Requer servidor web, maior complexidade |
| **Streamlit** | Rápido para ML dashboards | Limitações de UI |

**Veredicto:** tkinter é adequado para MVP acadêmico. Para versão de produção em escola real, um aplicativo web (Flask + React ou Streamlit) seria mais apropriado.

---

## 8. Acurácia vs Recall como Métrica Primária

**Decisão:** usar acurácia global como métrica principal (94,0%).

**Custo:** mascara o recall baixo de Recuperação (62,2%).

**Melhor alternativa:** usar macro-recall ou F1 macro como métrica primária, com acurácia como métrica secundária.

**Por que a decisão foi tomada:** acurácia é a métrica mais fácil de comunicar. Para um TGI, "o modelo acerta 94% das vezes" é mais compreensível que "o modelo tem macro-F1 de 0,83".

**Para o artigo de extensão:** reportar ambas as métricas, com ênfase pedagógica no recall de cada classe.

---

## Links

- [[Análise Crítica do TGI]]
- [[Random Forest — Algoritmo e Justificativa]]
- [[Matriz de Confusão M3 — Análise Detalhada]]
- [[Dataset — Estrutura e Geração Sintética]]
- [[Limitações Gerais do Artigo]]
- [[Plano de Artigo ABNT]]
