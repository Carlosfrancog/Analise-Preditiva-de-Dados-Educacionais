---
tags: [artigo, shap, explicabilidade, melhorias, ml]
created: 2026-05-16
---

# SHAP — Explicabilidade Local por Aluno

[[INDEX - ARTIGO|← Índice]] | [[Random Forest — Algoritmo e Justificativa]] | [[Feature Importance Detalhada — M3]] | [[Protocolo de Alertas EWS]]

> [!NOTE] Ausente no EduPredict — identificado como lacuna crítica por Romero e Ventura (2020) e pelos trabalhos relacionados

---

## 1. O Problema com Feature Importance Global

O EduPredict reporta feature importance global (médias sobre todo o dataset):
```
n2_norm: 32,3% — importante para a maioria dos alunos
```

O que um professor precisa:
```
Para Maria (aluna específica):
  - N2 = 4,5 contribuiu com +0,38 para risco de Reprovação
  - pct_materias_ok = 0,31 contribuiu com +0,22 para risco
  - slope_notas = +0,15 contribuiu com -0,05 (protetor)
  → "Maria está em risco principalmente por suas notas baixas em N2 
     combinadas com falhas em 7 das 13 matérias"
```

A diferença é a distância entre "o modelo é assim" e "esse aluno específico".

---

## 2. O Que é SHAP

SHAP (SHapley Additive exPlanations) é baseado na teoria dos jogos cooperativos. Para cada predição individual, calcula a contribuição marginal de cada feature:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!} [f(S \cup \{i\}) - f(S)]$$

Onde:
- $\phi_i$ = contribuição da feature $i$ para essa predição específica
- $S$ = subconjunto de features (sem a feature $i$)
- $f(S)$ = predição do modelo com o subconjunto $S$

**Propriedades importantes:**
- Soma à diferença entre a predição e a predição base (média)
- Consistente — se feature é mais importante, SHAP é maior
- Aditivo — soma das contribuições = predição total

---

## 3. SHAP para Random Forest

```python
import shap

# Treinar o modelo (já feito)
model = RandomForestClassifier(...).fit(X_train, y_train)

# Criar explainer TreeSHAP (eficiente para RF)
explainer = shap.TreeExplainer(model)

# Para um aluno específico
aluno_features = pd.DataFrame([{
    'n1_norm': 0.45,
    'n2_norm': 0.35,
    'n3_norm': 0.50,
    'slope_notas': 0.025,
    'variancia_notas': 0.0050,
    'media_geral_aluno': 0.42,
    'pct_materias_ok': 0.31,
    'media_turma_norm': 0.65,
    'serie_num_norm': 0.5
}])

# Calcular SHAP values
shap_values = explainer.shap_values(aluno_features)
# shap_values[k] = array de contribuições para classe k (0=Reprov, 1=Recup, 2=Aprov)

# Visualizar (para desenvolvimento)
shap.waterfall_plot(shap.Explanation(
    values=shap_values[0][0],  # contribuições para Reprovado
    base_values=explainer.expected_value[0],
    data=aluno_features.iloc[0],
    feature_names=aluno_features.columns
))
```

---

## 4. Como Integrar ao EduPredict

### Etapa 1 — Salvar explainer junto com o modelo

```python
# train_simple.py — adicionar ao pipeline de treinamento
import shap
import pickle

# Após treinar o modelo
explainer = shap.TreeExplainer(clf_m3)
pickle.dump(explainer, open('models/explainer_m3.pkl', 'wb'))
```

### Etapa 2 — Usar na predição

```python
# gui_ml_integration.py — adicionar a analyze_student()
def get_shap_explanation(self, aluno_features, model_version='m3'):
    explainer = pickle.load(open(f'models/explainer_{model_version}.pkl', 'rb'))
    shap_values = explainer.shap_values(aluno_features)
    
    # Para a classe de maior risco
    risk_class = 0  # Reprovado
    contributions = dict(zip(
        aluno_features.columns,
        shap_values[risk_class][0]
    ))
    return sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
```

### Etapa 3 — Renderizar na interface

```python
# gui_predicoes_improved.py — mostrar explicação em linguagem natural
def _render_explanation(self, shap_contributions):
    """Converte SHAP values em texto interpretável para professor."""
    messages = []
    for feature, contribution in shap_contributions[:3]:  # top 3
        if feature == 'n2_norm' and contribution > 0.1:
            messages.append(f"Nota do 2º bimestre ({n2:.1f}) está elevando o risco")
        elif feature == 'pct_materias_ok' and contribution > 0.1:
            pct = pct_materias_ok * 100
            messages.append(f"Aluno está em risco em {100-pct:.0f}% das matérias")
        # ... outros mappings
    return "\n".join(messages)
```

---

## 5. Custo Computacional

TreeSHAP para Random Forest tem complexidade $O(T \cdot L \cdot M)$ onde:
- $T$ = número de árvores (100)
- $L$ = profundidade máxima
- $M$ = número de features (9)

Para 9 features e 100 árvores, o cálculo é instantâneo (< 10ms por predição). Não há custo computacional significativo para integrar ao EduPredict.

---

## 6. Exemplos de Output para o Professor

| Feature que mais contribui | Output para professor |
|---|---|
| n2_norm baixo | "A nota do 2º bimestre (3,5) é o principal indicador de risco" |
| pct_materias_ok baixo | "Risco em 9 de 13 matérias indica dificuldade sistêmica, não isolada" |
| slope negativo | "Tendência de queda a cada bimestre aumenta o risco" |
| media_geral_aluno baixo | "Histórico de notas abaixo da média da turma" |
| SHAP positivo (protetor) | "Melhora recente (slope positivo) reduz o risco" |

---

## 7. Por Que o EduPredict Não Implementa SHAP?

Prováveis razões:
1. **Escopo de TGI** — SHAP é uma feature avançada além do MVP
2. **Desconhecimento** — SHAP não é mencionado nos trabalhos relacionados nacionais consultados
3. **Complexidade de UI** — traduzir SHAP values para professores não-técnicos requer design UX cuidadoso

**Para o artigo de extensão:** implementar SHAP seria a contribuição de maior impacto prático — diferencia o EduPredict de todos os trabalhos nacionais consultados.

---

## Links

- [[Random Forest — Algoritmo e Justificativa]]
- [[Feature Importance Detalhada — M3]]
- [[gui predicoes improved py — Interface Preditiva]]
- [[Protocolo de Alertas EWS]]
- [[Análise Comparativa dos Trabalhos]]
- [[Plano de Artigo ABNT]]
