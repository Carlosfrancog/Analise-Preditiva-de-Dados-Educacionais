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
- `research/reports/initial_pipeline_summary.json`;
- `research/artifacts/M1.pkl`, `M2.pkl`, `M3.pkl` e seus metadados para a API.

## Usar pela API e pela interface

Com o ambiente virtual ativado, instale as dependências da API uma vez:

```powershell
pip install -r .\04-API\requirements.txt
```

Depois de executar a pipeline, inicie o backend entrando na pasta da API:

```powershell
Set-Location .\04-API
python -m uvicorn main:app --host 127.0.0.1 --port 7654
```

Os endpoints novos são:

- `GET /api/research/status` — verifica snapshots e artefatos;
- `GET /api/research/snapshots` — catálogo dos cortes M1/M2/M3;
- `GET /api/research/snapshots/M2/samples?limit=30` — amostras com predição;
- `POST /api/research/predict` — inferência para um vetor de features.

Em outro terminal, para iniciar a interface:

```powershell
Set-Location .\05-WEB
npm install
npm run dev
```

A tela **Pesquisa temporal** aparece no menu lateral e consome exclusivamente
o namespace `/api/research`. Ela exibe dados sintéticos da primeira execução;
esses artefatos continuam identificados como experimentais e não devem ser
apresentados como resultado final do artigo.

## Testes

```bash
pytest -q research/tests
```

## Limite desta versão

Os resultados gerados são um primeiro experimento técnico. Ainda não são os
resultados finais do artigo. Antes da publicação, o protocolo deverá receber a
validação temporal e agrupada final, revisão de qualidade dos rótulos,
calibração, análise de equidade e integração com a API.
