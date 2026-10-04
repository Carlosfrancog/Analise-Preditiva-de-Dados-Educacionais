# Pipeline de pesquisa do EduPredict

Esta pasta contém a implementação experimental usada para produzir as
evidências do Full Paper. Ela é separada do código legado em `02-ML`, `03-GUI`
e `04-API`.

## Execução rápida

Na raiz de `repo-analysis`:

```bash
python -m research.run_initial_pipeline
```

O comando gera:

- `research/data/generated/experimental_dataset.csv`;
- `research/data/generated/experimental_dataset.manifest.json`;
- `research/data/snapshots/experimental_dataset_M1.csv`;
- `research/data/snapshots/experimental_dataset_M2.csv`;
- `research/data/snapshots/experimental_dataset_M3.csv`;
- `research/reports/legacy_audit.json`;
- `research/reports/initial_benchmark.json`;
- `research/reports/initial_pipeline_summary.json`.

## Testes

```bash
pytest -q research/tests
```

## Limite desta versão

Os resultados gerados são um primeiro experimento técnico. Ainda não são os
resultados finais do artigo. Antes da publicação, o protocolo deverá receber a
validação temporal e agrupada final, revisão de qualidade dos rótulos,
calibração, análise de equidade e integração com a API.

