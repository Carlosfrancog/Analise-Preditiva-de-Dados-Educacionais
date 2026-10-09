# RUNBOOK — Investigação dirigida: IDOR/BOLA

**Quando usar:** o solicitante pede verificação de controle de acesso em uma rota, recurso
ou cenário multi-tenant específico.

## Sequência

1. Confirmar escopo mínimo: rota(s) alvo e, se multi-tenant, o modelo de isolamento
   declarado pelo projeto (schema por tenant, coluna `tenant_id`, banco separado).
2. Aplicar `../skills/idor-bola-multitenant.md` integralmente.
3. Antes de declarar ausência de autorização, verificar explicitamente middlewares
   globais, políticas de serviço e controles de banco (row-level security) — se não
   estiverem visíveis no escopo fornecido, classificar o achado como `HYPOTHESIS` ou
   `UNKNOWN` e solicitar os arquivos faltantes (nunca presumir ausência de proteção só
   pela não visibilidade).
4. Correlacionar deterministicamente a permissão declarada na rota com os privilégios
   mapeados no controle de acesso do banco antes de declarar quebra de privilégio (ver
   `../principles.md`).
5. Se autorizado teste ativo (ver `autorizacao-testes-ativos.md`), descrever e, se
   permitido, executar o teste com duas identidades de privilégio distinto, documentando
   requisição e resposta de cada uma.
6. Preencher `../schemas/finding.schema.json`, com `trust_boundary` explicitando a
   fronteira (usuário↔usuário ou tenant↔tenant).
