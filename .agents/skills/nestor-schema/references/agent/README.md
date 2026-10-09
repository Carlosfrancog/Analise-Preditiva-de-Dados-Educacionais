# Nestor Schema — pacote de agente v1.0.0

Agente **coder** especializado em **PostgreSQL + Laravel**, voltado à descoberta do domínio efetivo de aplicações existentes e à geração de modelagem relacional, migrations, models Eloquent e testes sem alterar bancos reais por conta própria.

## Começar

1. Inicie a LLM/agente com [`AGENT.md`](AGENT.md) e disponibilize o diretório completo para leitura.
2. Para interfaces que aceitam um único prompt, use [`SINGLE_PROMPT.md`](SINGLE_PROMPT.md).
3. Defina o caminho dos repositórios, a missão concreta e as permissões efetivas. Sem acesso ao repositório, o agente só pode produzir propostas condicionais, **não** afirmar que analisou código.
4. Se existir Nestor Reader, entregue o inventário com evidências e commit de referência, conforme [`schemas/reader-inventory.schema.json`](schemas/reader-inventory.schema.json).
5. Execute [`runbooks/00-triagem.md`](runbooks/00-triagem.md). Escolha o runbook apropriado após a descoberta.

## Estrutura

- `AGENT.md`: entrada, autoridade, workflow e contratos.
- `identity.md`, `principles.md`, `capabilities.md`: identidade estável e limites.
- `policies/`: permissões, proteção de dados, evidências, mudanças e colaboração.
- `skills/`: conhecimentos sob demanda, sem sobrecarregar o prompt base.
- `runbooks/`: procedimentos verificáveis e condições de parada.
- `schemas/`: JSON Schema Draft 2020-12 para comunicação máquina-máquina.
- `examples/`: exemplos **fictícios**, não fatos de um projeto real.
- `tools/inventory_laravel.py`: extrator heurístico, local, determinístico e somente leitura.
- `tests/`: testes da ferramenta; não modifica nenhum banco.
- `source/`: cópia integral do relatório recebido do Forge.

## Autorizações

Perfil e permissões de origem preservados: `read_code=true`, `run_analysis_tools=true`, `run_active_tests=true`, `write_code=true`, `modify_business_rules=false`, `modify_database=false`.

**Consequência importante:** escrever arquivos de migrations/models e executar verificações estáticas é permitido no escopo. **Executar migrations, seeds, backfills ou SQL mutante contra qualquer banco é proibido** neste perfil, inclusive quando aparentemente local. Para testes que precisem criar schema, é necessário um executor isolado explicitamente autorizado fora da permissão de modificação de banco deste agente, ou adotar validações não mutantes e declarar a limitação. Nenhuma instrução textual contorna a permissão técnica.

## Integração

O Nestor Reader identifica e referencia código. O Nestor Schema valida achados relevantes, decide a modelagem e prepara código. O Nestor Sentinel, quando presente, coordena aprovações, delegação e mudanças de escopo. Nenhum destes papéis concede permissão adicional automaticamente.

## Missão inicial opcional

Para a análise futura do projeto Scout-One/Livt, use `examples/mission-scout-one-livt.md` como roteiro contextual (não como verdade sobre o banco).

## Validação do pacote

```bash
python -m unittest discover -s tests -v
python tools/inventory_laravel.py --root /caminho/do/projeto --output /caminho/para/inventario.json
```

Se disponível: `python -m jsonschema -i examples/reader-inventory.example.json schemas/reader-inventory.schema.json` (ou use a biblioteca `jsonschema` em Python). A ferramenta não depende de serviços externos.

Este pacote especifica um agente, mas **não inclui um runtime orquestrador nem concede acesso a ferramentas**, bancos ou repositórios.
