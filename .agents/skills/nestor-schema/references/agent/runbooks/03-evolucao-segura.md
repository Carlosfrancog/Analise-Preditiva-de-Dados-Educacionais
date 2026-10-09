# Runbook 03 — Evolução de schema já existente

1. Distinguir histórico de migrations, estrutura efetiva do DB e contratos atuais de aplicação.
2. Verificar consumers de tabelas/colunas e compatibilidade com deploy gradual.
3. Analisar nulidade/duplicatas/órfãos/volume somente com leitura limitada, quando autorizada.
4. Escolher estratégia incremental `expand → backfill → switch → contract` ou justificar alternativa.
5. Identificar lock, custo de índice, transações e efeito em versões coexistentes.
6. Criar nova migration; não reescrever migrations executadas.
7. Preparar data backfill idempotente, com checkpoint, limites e recuperação, **sem executar**.
8. Definir pré-condições, testes, rollout por fase, observabilidade, rollback e plano de backup/restore se necessário.
9. Validar arquivos e invariantes estaticamente.
10. Encaminhar migrations para executor autorizado; marcar `executed=false` até receber evidência.

**Não concluir:** se consumidor crítico não mapeado, decisão comercial pendente, sem plano de rollback ou risco de perda de dados não aceito.
