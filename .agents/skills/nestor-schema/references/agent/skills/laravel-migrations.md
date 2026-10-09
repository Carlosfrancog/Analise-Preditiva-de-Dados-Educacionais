# Skill — Evolução segura com Laravel migrations

## Tipos de tarefa

- **Novo schema:** migrations iniciais ordenadas por dependências; validar relações e constraints.
- **Schema existente:** novas migrations; evitar editar antigas já aplicadas; demonstrar compatibilidade.
- **Data migration/backfill:** especificar script idempotente separado e plano; **não executar**.

## Expand → Backfill → Switch → Contract

1. **Expand:** criar estrutura compatível (nullable, novas tabelas/colunas, sem remoções precipitadas).
2. **Backfill:** planejar lotes, controle de progresso, idempotência, duplicados e concorrência.
3. **Switch:** coordenar leitura/escrita da aplicação, versões coexistentes e monitoramento.
4. **Contract:** remover legado só após verificação de dependências e autorização.

## Regras PostgreSQL

- `ALTER TABLE` pode adquirir locks; não assumir custo desprezível.
- Criar constraint pode demandar validação de dados legados.
- `CREATE INDEX CONCURRENTLY` não pode ocorrer dentro de transação comum; tratar separadamente e consultar recursos da versão.
- `NOT NULL` em dados legados precisa diagnóstico de nulos e estratégia segura.
- `down()` não recupera dados; oferecer rollback de aplicação e/ou recuperação de backup quando necessário.
- Para tabelas grandes, planejar observabilidade, estimativa de duração e limites de manutenção.

## Artefatos obrigatórios

Pré-condições, diferença proposta do schema, migrations, scripts de backfill propostos, validação pré/pós, riscos, compatibilidade, caminho de rollback e responsáveis. **Aplicação ao banco bloqueada neste perfil.**
