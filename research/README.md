# Pipeline de pesquisa do EduPredict

Esta pasta contém a implementação experimental do TGI II. Ela prepara
artefatos e verificações técnicas iniciais, ainda sem o protocolo de validação
final do artigo. A pipeline é separada do código legado em `02-ML` e `03-GUI`;
a API a expõe em `/api/research` sem convertê-la em resultado acadêmico final.

## Execução rápida

Na raiz do repositório EPA, com as dependências de `04-API/requirements.txt` instaladas:

> Execute apenas quando quiser regenerar o experimento. O comando escreve em `research/data/`, `research/artifacts/` e `research/reports/`.

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

O status identifica explicitamente a fonte como `synthetic`, marca o fluxo como
experimental e só retorna `ready` quando os três snapshots e os respectivos
pares de artefatos (`.pkl` + `.json`) estão disponíveis. A predição manual
rejeita features ausentes, extras, não finitas ou fora do intervalo esperado.

Em outro terminal, para iniciar a interface:

```powershell
Set-Location .\05-WEB
npm install
npm run dev
```

A tela **Pesquisa temporal** aparece no menu lateral e consome exclusivamente
o namespace `/api/research`. Ela exibe a prontidão da pipeline, a fonte dos
dados, filtros por aluno e ano e todas as features disponíveis em cada corte.
Os dados continuam identificados como sintéticos e os artefatos como
experimentais; nenhum deles deve ser apresentado como resultado final do artigo.

## Testes

```bash
pytest -q research/tests
```

## Limite desta versão

Os resultados gerados são um primeiro experimento técnico. Ainda não são os
resultados finais do artigo. Antes da publicação, o protocolo deverá receber a
validação temporal e agrupada final, revisão de qualidade dos rótulos,
calibração, análise de equidade e integração de snapshots versionados com a API.
