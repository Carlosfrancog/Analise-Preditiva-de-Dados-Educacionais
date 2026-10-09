# Skill — Modelagem física PostgreSQL

## Projeto em três camadas

1. **Conceitual:** entidade, identidade, relacionamentos, regras e ciclo de vida.
2. **Lógico:** tabelas, chaves, cardinalidades, dependências funcionais, obrigatoriedade e normalização.
3. **Físico:** tipos, constraints, índices, schemas, migrações e características PostgreSQL suportadas.

## Checklist técnico

- Chaves: `bigint` para identidade interna convencional; `UUID`/`ULID` para exposição, integração ou geração distribuída **quando justificados**; não misturar sem estratégia.
- `NULL`/`NOT NULL`: correspondem à evolução do dado. Defaults precisam representar comportamento legítimo.
- `FOREIGN KEY`: indicar coluna, tabela alvo, nulidade e `ON DELETE/UPDATE` de acordo com ciclo de vida. Avaliar índice do lado referenciante.
- `UNIQUE`: escopo exato, incluindo tenant, período, integração ou exclusão lógica. PostgreSQL permite índices únicos parciais quando necessários.
- `CHECK`: restrições monotônicas/documentadas para ranges e estados quando estáveis; não espelhar arbitrariamente validações de UI.
- Dinheiro: `numeric(p,s)` ou unidades inteiras segundo contrato; não escolher float sem justificativa.
- Tempo: distinguir instantes absolutos (`timestamptz` quando apropriado), datas civis e horas locais; alinhar casts e timezone PHP.
- Texto: tamanho máximo real versus `text`; `citext` depende de extensão/instalação autorizada.
- JSONB: útil para payload externo evolutivo ou metadado pouco estruturado, não para FKs centrais.
- Arrays/enum: só quando evolução e consultas justificarem a complexidade.
- Índices B-tree, compostos, parciais, expressão, GIN/GiST: escolher conforme `WHERE`, `JOIN`, `ORDER BY`, seletividade e escrita.
- Polimorfismo Eloquent: considerar falta de FK nativa para vínculos múltiplos e impacto da integridade.
- Particionamento/triggers/RLS: design opcional que precisa de requisitos explícitos e equipe apta a manter.

## Contrato de saída por coluna

Nome, tabela, tipo, nulidade, default, origem de evidência, validações de app, constraints de banco, consultas e decisão em aberto. Não converter hipótese em DDL sem resolver risco.
