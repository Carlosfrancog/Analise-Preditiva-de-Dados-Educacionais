# Política de segurança de schema e dados

## Restrições

- Não executar `migrate`, `migrate:fresh`, `migrate:refresh`, `migrate:reset`, `migrate:rollback`, `db:wipe`, `db:seed`, SQL mutante, backfill ou testes com escrita em banco.
- Não aplicar `ALTER`, `DROP`, `CREATE INDEX`, `TRUNCATE`, nem migrar banco “de teste” por conta própria.
- Não alterar schemas ou dados apenas porque a LLM tem acesso ao terminal.
- Não imprimir conteúdo de `.env`, tokens, dumps reais ou registros pessoais.
- Antes de prescrever rollout, conhecer backup, retenção, tamanho, locks, consumidores e rollback.
- A ausência de permissões de banco **não impede escrever arquivos** de migration, SQL proposto, testes e checklists de execução delegada.

## Risco de evolução

- Novas colunas `NOT NULL` exigem plano de preenchimento ou defaults de domínio.
- Renomeações e exclusões exigem verificação de consumidores e janela de compatibilidade.
- `UNIQUE` pode falhar devido a duplicados existentes; planejar diagnóstico prévio read-only.
- FKs podem falhar por órfãos; programar detecção e correção autorizada.
- Índices e alterações em tabelas grandes podem gerar locks, IO e latência.
- `CREATE INDEX CONCURRENTLY` tem restrições transacionais e regras específicas de recuperação.
- Soft deletes podem exigir índice parcial de registros ativos, em vez de `UNIQUE` ingênuo.
- Mudanças de tipos monetários, timezone e JSONB precisam plano explícito de conversão.
- `down()` não recupera dados deletados; rollback lógico e restauração de backup são conceitos distintos.

## Handoff de execução autorizada

Quando necessária mutação, entregar: scripts versionados, pré-checks, plano/ordem, estimativa de impacto, critérios de parada, validação pós-aplicação e método de recuperação. Marcar a execução como pendente até receber evidência externa.
