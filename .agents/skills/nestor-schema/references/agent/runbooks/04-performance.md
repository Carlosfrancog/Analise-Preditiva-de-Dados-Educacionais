# Runbook 04 — Diagnóstico de consultas e índices

1. Identificar endpoint, consulta real, filtros e objetivo observável (latência, CPU, IO, timeout).
2. Capturar shape de query e índices existentes por fonte verificável.
3. Separar N+1 Eloquent, baixa seletividade, join incorreto, paginação e falta de índice.
4. Obter plano `EXPLAIN` sem execução somente quando autorizado; caso contrário orientar coleta.
5. Recomendar índice/rewriting com trade-offs; não alterar regra de negócio.
6. Desenhar teste reproduzível antes/depois em ambiente controlado para executor autorizado.
7. Preparar migration de índice quando justificada; não aplicar.
8. Registrar resultados medidos vs hipóteses e risco de lock/IO.

**Proibição:** não executar EXPLAIN ANALYZE de DML nem benchmark pesado em produção por conta própria.
