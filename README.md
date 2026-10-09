# EduPredict Analytics (EPA)

O EPA reúne uma **plataforma escolar em desenvolvimento** e uma **pesquisa acadêmica em andamento no TGI II**. A plataforma web usa React, FastAPI e SQLite; a área `research/` contém uma pipeline experimental separada. Os números do TGI I e dos dados sintéticos não são resultados finais do TGI II.

## Por onde começar

| Objetivo | Entrada | Estado |
| --- | --- | --- |
| Desenvolver a plataforma web | `05-WEB/` + `04-API/` | Caminho principal de desenvolvimento |
| Examinar os modelos usados pela plataforma | `ml_models/`, `04-API/ml_service.py` | Artefatos legados RF_M1, RF_M2 e RF_M3 |
| Estudar a pipeline temporal | `research/` | Experimento sintético, separado da base escolar |
| Consultar o aplicativo anterior | `03-GUI/` e `run.py` | Interface desktop histórica |
| Consultar o site público | `EPA-page/` | Submódulo Git independente |

Os guias em `04-DOCS/` descrevem principalmente a fase anterior do aplicativo. Para executar a **plataforma web atual**, siga as instruções abaixo.

## Executar a plataforma web no Windows

Na raiz do EPA, em PowerShell, instale as dependências uma vez. Este workspace tem `uv` e Python 3.11 disponíveis. O `python` encontrado no PATH é do MSYS2, por isso use o interpretador escolhido pelo `uv`:

```powershell
uv venv --python 3.11 .venv-win
uv pip install --python .\.venv-win\Scripts\python.exe -r .\04-API\requirements.txt
Set-Location .\05-WEB
npm ci
```

Abra **dois terminais**. Em ambos, parta da raiz do EPA. Não é necessário ativar o ambiente virtual.

**Terminal 1 — API:**

```powershell
Set-Location .\04-API
..\.venv-win\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 7654 --reload
```

**Terminal 2 — interface:**

```powershell
Set-Location .\05-WEB
npm run dev
```

Abra `http://localhost:5173/`. A API responde em `http://127.0.0.1:7654/api/health` e documenta as rotas em `http://127.0.0.1:7654/docs`. O Vite encaminha chamadas `/api` para a porta 7654. Para parar cada processo, use `Ctrl+C`.

No WSL/Linux, use um ambiente separado (`.venv-wsl`). Nesta máquina o Python do WSL é 3.12, mas o pacote `python3.12-venv` ainda não está instalado; ele é necessário antes de `python3 -m venv .venv-wsl`. Depois, ative com `source .venv-wsl/bin/activate` e instale `04-API/requirements.txt` com `python -m pip`.

### O que acontece no primeiro início

- A API cria ou atualiza `01-CORE/escola.db` e cria um usuário de desenvolvimento se a tabela de usuários estiver vazia. As credenciais locais aparecem no log da API. Esse banco não vem no Git; uma instalação nova começa sem alunos e notas.
- Os modelos legados em `ml_models/` são carregados pela API quando disponíveis. Eles servem à plataforma anterior e não equivalem aos artefatos temporais de `research/`.
- `04-API/requirements.txt` fixa o scikit-learn em 1.8.0, versão gravada nos modelos `.pkl` atuais; versões diferentes emitiram aviso de incompatibilidade durante a verificação.
- A tela **Pesquisa temporal** consulta `/api/research`. Ela informa que a pipeline não está pronta quando os snapshots e artefatos experimentais ainda não foram gerados.
- Não execute `01-CORE/seed_escola.py` para apenas abrir o projeto: esse script insere dados no banco. O antigo `reorganizar.py` foi arquivado em `04-DOCS/legacy/` apenas para consulta.

## Pesquisa experimental

`research/` tem [instruções próprias](research/README.md). O comando `python -m research.run_initial_pipeline`, executado na raiz do EPA, **gera dados sintéticos, snapshots, modelos e relatórios**; por isso, é uma etapa optativa e deliberada. Os 62.400 registros citados no relatório inicial são linhas desse experimento, não alunos carregados na interface escolar.

Antes de redigir ou publicar resultados do TGI II, será necessário fixar as regras da pesquisa, os dados e rótulos elegíveis, o protocolo de validação, as métricas e os critérios de revisão acadêmica. O primeiro relatório do TGI II registra planejamento e atividades iniciais; ele não encerra essa definição.

## Mapa do repositório

| Caminho | Responsabilidade |
| --- | --- |
| `01-CORE/` | Persistência SQLite, cadastro, notas e cálculos do sistema escolar |
| `02-ML/` | Treinamento e artefatos da fase anterior de ML |
| `03-GUI/` | Aplicativo desktop anterior |
| `04-API/` | API FastAPI, autenticação e serviço dos modelos legados |
| `05-WEB/` | Interface React/Vite da plataforma atual |
| `research/` | Experimentos temporais do TGI II, isolados da base operacional |
| `04-DOCS/`, `05-TESTS/` | Documentação e scripts de teste da fase anterior |
| `Obsidian/` | Notas de trabalho e histórico do projeto |
| `EPA-page/` | Site público em submódulo; possui seu próprio README |
| `prototypes/` | Estudos visuais que não participam da aplicação |
| `.agentes/`, `.agents/`, `.codex/` | Agentes e skills Nestor para desenvolvimento |

Os nomes numerados são mantidos por enquanto porque imports, caminhos de arquivos e documentos os referenciam. Mudanças de estrutura dos módulos ativos devem ser feitas com uma migração própria e verificadas nos fluxos da API e da interface.

## Próximo foco de desenvolvimento

1. Confirmar qual base e tabela sustentam a contagem de mais de 60 mil registros mencionada no projeto; `escola.db` não está nesta cópia do repositório.
2. Mapear a passagem de alunos e notas entre SQLite, rotas `/api/alunos` e `/api/notas`, e telas `05-WEB/src/pages/Alunos.jsx` e `Notas.jsx`.
3. Recuperar ou reconstruir os metadados versionados dos modelos legados: os arquivos `.pkl` carregam, mas seus arquivos de metadados não estão nesta cópia, e a API exibe acurácia `0` como valor padrão.
4. Definir o contrato entre os modelos de pesquisa e a plataforma sem apresentar experimentos sintéticos como predições validadas para uso pedagógico.

O histórico acadêmico publicado está no [site EPA-page](https://carlosfrancog.github.io/EPA-page/).
