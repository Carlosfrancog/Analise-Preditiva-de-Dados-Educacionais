# Skill — Consultas, índices e desempenho

## Fluxo

1. Obter consultas reais, filtro, sort, joins, volume e cardinalidade (não inventar métricas).
2. Investigar índices existentes (migrations e/ou catálogos PostgreSQL somente leitura).
3. Usar `EXPLAIN` sem `ANALYZE` quando apropriado para previsão não executante.
4. Reservar `EXPLAIN ANALYZE` para executor autorizado e ambiente seguro; em DML executa e pode modificar dados.
5. Propor índice B-tree/composto/parcial/GIN/GiST somente após associar a padrão de acesso.
6. Considerar custo de escrita, espaço e manutenção. Avaliar eager loading para N+1 Eloquent.
7. Especificar benchmark comparável antes/depois, sem declarar resultados não observados.

## Exemplos de observações

- `JOIN` por FK: verificar se a coluna referenciante está indexada; PostgreSQL não cria automaticamente índice nela.
- Tenant + status + ordenação: avaliar índice composto baseado em consulta, filtro e estatísticas.
- JSONB: avaliar GIN só com operadores e frequência verificados.
- Soft delete: índice parcial pode ser útil para unicidade/consultas de registros ativos.

## Entrega

Hipótese de gargalo, consultas e planos realmente vistos, evidências, recomendações e testes pendentes. Nunca executar query de carga pesada em produção sem autorização.
