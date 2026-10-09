# Contrato de colaboração: Nestor Reader ↔ Nestor Schema

## Reader deve fornecer

- Identificação do projeto/repositório e commit de referência (ou `UNKNOWN`).
- Inventário de migrations, models, requests, resources, policies, jobs, queries, rotas e contratos de frontend relevantes.
- Evidências verificáveis: caminho, linha, símbolo, resumo estritamente factual.
- Lacunas/ambiguidades e perguntas específicas.
- Diferenciação entre elementos observados em código, inferidos e vistos no banco real.

## Schema deve fazer

- Verificar os achados críticos nos arquivos atuais antes de cristalizá-los em DDL.
- Produzir lista de entidades, ciclo de vida, cardinalidades e constraints propostas com evidências.
- Indicar tarefas de investigação específicas ao Reader quando faltar contexto.
- Não pedir que Reader decida regras de negócio ou execute alterações de banco.
- Entregar handoff ao Sentinel/usuário quando necessário: hipótese, risco, decisão requerida, opções e impacto.

## Protocolo

1. Checar `repository` e `commit` do inventário.
2. Confirmar estado atual `git rev-parse HEAD` quando possível.
3. Revalidar arquivos modificados desde a extração; marcar dados defasados.
4. Correlacionar evidência por identificador com entidades e migrations propostas.
5. Exportar resultados em `schemas/domain-model.schema.json` e `schemas/agent-handoff.schema.json` quando integração máquina-máquina for necessária.

O Nestor Reader não se torna automaticamente fonte de verdade; seu papel é descoberta e auditoria.
