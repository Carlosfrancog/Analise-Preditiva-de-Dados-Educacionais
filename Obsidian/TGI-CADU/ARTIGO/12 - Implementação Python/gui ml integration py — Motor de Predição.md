---
tags: [artigo, implementacao, gui_ml_integration, ml, predicao]
created: 2026-05-16
---

# gui_ml_integration.py — Motor de Predição em Tempo Real

[[INDEX - ARTIGO|← Índice]] | [[cads.py — Análise Profunda]] | [[gui predicoes improved py — Interface Preditiva]] | [[Mapeamento Teoria-Código]]

---

## 1. Papel no Sistema

`gui_ml_integration.py` é a **ponte entre os modelos treinados e a interface**:
- Carrega os modelos PKL do disco (`MLModelLoader`)
- Seleciona automaticamente o modelo correto (M1/M2/M3) baseado nas notas disponíveis
- Executa a predição em tempo real para cada (aluno, matéria)
- Consolida resultados em um perfil de risco do aluno (`DisciplinePerformanceAnalyzer`)

---

## 2. Classe MLModelLoader

```python
class MLModelLoader:
    """Carrega e seleciona o modelo ML apropriado."""
    
    def __init__(self, models_dir='02-ML/models'):
        self.models = {}
        self.features = {}
        
        for version in ['m1', 'm2', 'm3']:
            model_path = f"{models_dir}/model_{version}.pkl"
            features_path = f"{models_dir}/features_{version}.pkl"
            
            if os.path.exists(model_path):
                self.models[version] = pickle.load(open(model_path, 'rb'))
                self.features[version] = pickle.load(open(features_path, 'rb'))
    
    def load_model(self, n1, n2, n3):
        """Seleciona o modelo mais avançado disponível."""
        if n3 is not None and 'm3' in self.models:
            return self.models['m3'], self.features['m3'], 'M3'
        elif n2 is not None and 'm2' in self.models:
            return self.models['m2'], self.features['m2'], 'M2'
        elif n1 is not None and 'm1' in self.models:
            return self.models['m1'], self.features['m1'], 'M1'
        return None, None, None
```

**Sem tratamento de FileNotFoundError** — se os modelos não foram treinados, a interface falha.

---

## 3. Classe DisciplinePerformanceAnalyzer

```python
class DisciplinePerformanceAnalyzer:
    
    def analyze_student(self, db_path, aluno_id, model_loader):
        """Analisa todas as matérias de um aluno e consolida perfil."""
        
        # PROBLEMA: db_path é ignorado
        conn = cads.get_conn()  # ← sempre usa cads.DB_PATH
        
        materias = cads.get_materias()
        results = {}
        
        for materia in materias:
            mat_id = materia['id']
            
            # Buscar notas
            notas = cads.get_notas_materia(aluno_id, mat_id, conn)
            n1, n2, n3, n4 = notas  # ou None se não lançadas
            
            # Selecionar modelo
            model, features_list, version = model_loader.load_model(n1, n2, n3)
            
            if model is None:
                results[mat_id] = {'status': 'sem_dados'}
                continue
            
            # Construir vetor de features
            feature_values = self._extract_features(
                aluno_id, mat_id, n1, n2, n3, n4, conn
            )
            X = pd.DataFrame([feature_values])[features_list]
            
            # Predição
            prediction = model.predict(X)[0]
            probas = model.predict_proba(X)[0]
            
            # Prognóstico (INCONSISTENTE — usa slope_pct em vez de _slope)
            n1_raw = n1 or 0
            n2_raw = n2 or 0
            slope_pct = ((n2_raw - n1_raw) / n1_raw) * 100 if n1_raw > 0 else 0
            
            prognosis = 'stable'
            if slope_pct > 20:
                prognosis = 'will_improve'
            elif slope_pct < -20:
                prognosis = 'will_decline'
            
            results[mat_id] = {
                'prediction': prediction,
                'probas': probas,
                'prognosis': prognosis,
                'model_version': version
            }
        
        # Consolidar perfil de risco
        avg_risk = self._calculate_avg_risk(results)
        profile = self._classify_profile(avg_risk)
        
        return {'disciplines': results, 'profile': profile, 'avg_risk': avg_risk}
    
    def _classify_profile(self, avg_risk):
        if avg_risk > 0.7:
            return "🔴 CRÍTICO - Atenção imediata"
        elif avg_risk > 0.4:
            return "🟡 EM RISCO - Acompanhamento"
        else:
            return "🟢 SEGURO - Desempenho normal"
```

---

## 4. Inconsistência Crítica do slope_pct

```python
# O que o treino usa (cads.py → train_simple.py):
slope_notas = _slope([n1/10, n2/10, n3/10])  # regressão linear

# O que a interface usa para prognóstico (gui_ml_integration.py):
slope_pct = ((n2_raw - n1_raw) / n1_raw) * 100  # variação percentual N2→N1
```

São medidas diferentes:
- `_slope()` com N1=4, N2=7, N3=5 → slope ≈ +0,05 (levemente positivo)
- `slope_pct` com N1=4, N2=7 → slope_pct = +75% (muito positivo)

O prognóstico exibido na interface pode ser "vai melhorar" enquanto o modelo ML usa um slope próximo a zero — mensagens contraditórias para o professor.

Ver [[Débitos Técnicos Identificados#DT-01]] para a correção proposta.

---

## 5. Cálculo de Risco

```python
def _calculate_avg_risk(self, results):
    """
    Calcula risco médio do aluno como probabilidade média de não-Aprovado.
    """
    risks = []
    for mat_id, result in results.items():
        if 'probas' in result:
            # probas = [p_reprovado, p_recuperacao, p_aprovado]
            risk = result['probas'][0] + result['probas'][1]  # p(não-Aprovado)
            risks.append(risk)
    
    return sum(risks) / len(risks) if risks else 0.0
```

**Problema:** média aritmética de risco por matéria não pondera matérias por importância ou carga horária. Uma reprovação em Matemática pesa igual a uma em Educação Física.

---

## 6. Fluxo de Predição — Diagrama Completo

```
analyze_student(aluno_id)
    ├── Para cada matéria:
    │   ├── get_notas(aluno_id, materia_id)
    │   ├── load_model(n1, n2, n3) → M1/M2/M3
    │   ├── extract_features() → DataFrame
    │   ├── model.predict(X) → 0/1/2
    │   ├── model.predict_proba(X) → [p0, p1, p2]
    │   └── slope_pct cálculo (⚠ inconsistente)
    └── _calculate_avg_risk() → consolidação
    └── _classify_profile() → "🔴/🟡/🟢 ..."
```

---

## 7. Qualidade do Código

**Positivo:**
- Separação entre carregamento (MLModelLoader) e análise (DisciplinePerformanceAnalyzer)
- Seleção automática de modelo baseada em dados disponíveis
- Retorna probabilidades, não apenas predição binária

**Negativo:**
- db_path ignorado (ver DT-02)
- slope_pct inconsistente com cads.py (ver DT-01)
- Sem tratamento de FileNotFoundError para modelos
- Risco médio não ponderado por matéria
- Thresholds arbitrários (0,7 e 0,4)

---

## Links

- [[cads.py — Análise Profunda]]
- [[Arquitetura Modular — Visão Geral]]
- [[gui predicoes improved py — Interface Preditiva]]
- [[slope notas — Tendência Temporal]]
- [[Débitos Técnicos Identificados]]
- [[M3 — Modelo de Produção (Após N3)]]
