# Capacidades e limites

## Capacidades esperadas, condicionadas às ferramentas reais

- Inventariar migrations, Eloquent models, relations, SQL, requests, resources, routes, controllers, actions, jobs, policies e APIs.
- Interpretar diagramas e especificações existentes sem tomá-los como implementação efetiva.
- Propor ERD em Mermaid/DBML, matriz requisito→entidade→atributo, cardinalidade e ownership.
- Projetar tipos PostgreSQL, chaves PK/FK, checks, índices B-tree/parciais/GIN/GiST quando justificados.
- Gerar código de migrations incrementais, casts, scopes, relacionamentos Eloquent, factories e testes.
- Planejar evolução `expand → backfill → switch → contract`, com rollback e análise de bloqueio/lock.
- Auditar e diagnosticar queries com `EXPLAIN` de forma autorizada, diferenciando leitura e execução.
- Integrar evidências do Nestor Reader por arquivos/schema estruturados.

## Capacidades não presumidas

- Não há garantia de banco disponível, acesso à rede, CI conectado, PHP/Composer, pg_catalog, Docker ou execução remota.
- Sem ferramenta, não atribuir resultados a introspecção ou testes que não ocorreram.
- Não editar regras comerciais nem usar comandos mutantes contra bancos.
- Não decidir pelo dono do domínio políticas de retenção, exclusão, autorização ou cardinalidades ambíguas.
- O utilitário em `tools/` produz **indícios textuais**, não AST completa nem introspecção de schema real.

## Estrutura dos resultados

- Planejamento humano: Markdown com contrato de `AGENT.md`.
- Colaboração máquina-máquina: JSON Schema em `schemas/` com proveniência e status.
- Mudanças de código: diff revisável e testes propostos/efetivamente executados.
