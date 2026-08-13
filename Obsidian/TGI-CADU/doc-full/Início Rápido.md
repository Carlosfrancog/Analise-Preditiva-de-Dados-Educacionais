---
tags:
  - guia
  - quickstart
  - tgi-codes
created: 2026-05-13
---

# Início Rápido

[[MOC - TGI-CODES|← Voltar ao índice]]

> [!TIP] Tempo estimado
> ~10 minutos para ter o sistema rodando do zero.

---

## Pré-requisitos

- Python 3.8+
- Banco de dados `escola.db` já populado com alunos e notas

---

## Passo 1 — Instalar Dependências

```bash
pip install -r 01-CORE/requirements.txt
```

**Principais pacotes:**
- `scikit-learn` — modelos Random Forest
- `pandas` — manipulação de dados
- `numpy` — cálculos numéricos
- `matplotlib` / `seaborn` — gráficos
- `shap` — explicabilidade (opcional)
- `openpyxl` — exportação Excel

---

## Passo 2 — Inicializar o Banco

```python
python -c "import cads; cads.init_db()"
```

---

## Passo 3 — Rodar a Aplicação

```bash
python gui_escola.py
```

---

## Passo 4 — Gerar Features ML

Na tela **Machine Learning**:
1. Clique **🔄 Gerar Features**
2. Aguarde: `✅ 15.613 features geradas`

Ou via terminal:
```python
python -c "import cads; cads.gerar_features_ml()"
```

---

## Passo 5 — Treinar os Modelos

Na tela **Machine Learning**:
1. Clique **🚀 Treinar Todos**
2. Aguarde a barra de progresso completar
3. Popup exibe acurácias: M1 ~55%, M2 ~70%, M3 ~94%

Ou via terminal:
```bash
python train_simple.py
# Pipeline completo com debug:
python run_ml_pipeline.py
```

---

## Passo 6 — Analisar um Aluno

Na seção **Analisar Decisões**:
1. Selecione o **Aluno**
2. Selecione a **Matéria**
3. Clique **Analisar**
4. Leia o resultado com notas, features e interpretação

---

## Passo 7 — Ver Prognósticos

1. Navegue para **Predições** na sidebar
2. Selecione um aluno
3. Veja cards por matéria com cores: verde / laranja / vermelho

---

## Comandos Úteis

```bash
# Só treinar M3 (produção)
python -c "from ml_pipeline import train_random_forest; train_random_forest('M3')"

# Debug completo do dataset
python -c "from ml_debug import run_full_debug_report; run_full_debug_report(verbose=True)"

# Menu interativo com 10 exemplos
python example_usage.py

# Exportar notas para Excel
python -c "import cads; cads.exportar_notas_excel()"
```

---

## Troubleshooting

> [!WARNING] "ModuleNotFoundError: No module named 'sklearn'"
> Execute `pip install scikit-learn pandas numpy matplotlib`

> [!WARNING] "Nenhuma feature gerada"
> O banco precisa ter notas registradas. Verifique `escola.db`.

> [!WARNING] "Modelo não encontrado"
> Execute o Passo 5 (treinar modelos) antes de analisar alunos.

---

## Links Relacionados

- [[Pipeline de Treinamento]] — detalhes do processo de treino
- [[Modelos RF (M1-M2-M3)]] — qual modelo usar em cada situação
- [[Módulos ML]] — referência dos módulos Python
