# Runbook 05 — Validação sem mutação de banco

## Matriz de validação

| Verificação | Neste agente | Observação |
|---|---|---|
| PHP syntax, Laravel Pint --test, PHPStan | Executar se autorizado e disponível | conferir comandos específicos da versão |
| Revisão de SQL gerado por código | Executar como inspeção estática | sem conexão mutante |
| ERD, cardinalidade, constraints e contrato API | Revisão documental/estática | comprovar por evidência |
| Migration em PostgreSQL descartável | **Não executar** | requer executor com `modify_database=true` e isolamento validado |
| Testes com `RefreshDatabase` | **Não executar** | implicitamente escrevem no banco |
| Testes de FK/unique e rollback real | Preparar, não executar | executor autorizado reporta evidências |
| EXPLAIN read-only | Condicional | confirmar conexão e autorização |

## Checklist final

- Verificar versões relevantes e compatibilidade.
- Confirmar que cada tabela/coluna crítica tem justificativa.
- Revisar relação, `onDelete`, unicidade e isolamento por tenant.
- Revisar casts, fillable/guarded, FormRequests e Resources.
- Revisar diff, history de migrations e arquivos não relacionados.
- Classificar validações como PASSED / FAILED / BLOCKED / NOT_RUN.
- Não declarar migração aplicada ou schema validado em PostgreSQL se isto não ocorreu.
