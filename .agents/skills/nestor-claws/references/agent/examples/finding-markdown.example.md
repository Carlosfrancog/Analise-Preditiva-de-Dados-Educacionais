# Exemplo de saída em Markdown — formato preferencial

Este exemplo representa a mesma informação de `finding.example.json`, no formato de
resposta padrão do agente (Markdown — ver `spec.json#output_contract.preferred`).

---

## Escopo e cobertura

- Repositório: `billing-api` @ `a1b2c3d`
- Ambiente: código estático (sem execução)
- Rotas em escopo: `/api/v1/invoices/*`
- Fora do escopo: `billing-web`, testes de carga
- Testes ativos: não autorizados nesta sessão

## Resumo executivo

1 vulnerabilidade de alta severidade confirmada estaticamente: SQL Injection na busca de
faturas. Nenhum teste ativo foi executado.

## Evidências — NC-2026-001: SQL Injection em `POST /api/v1/invoices/search`

**Estado:** verificado · **Severidade:** alta (CVSS 3.1 `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` = 7.1) · **Confiança:** alta

- `FACT` — `src/billing/invoices.controller.ts:142`: a query é montada como
  `SELECT * FROM invoices WHERE customer = '${customer}'` e passada a `pg.query()` sem
  placeholders.
- `FACT` — `src/billing/invoices.controller.ts:128-140`: nenhuma validação/allowlist é
  aplicada ao valor de `customer` antes da montagem da query.
- `HYPOTHESIS` — não foi possível confirmar se um middleware global de sanitização
  intercepta este payload antes do controller; `src/middlewares/*.ts` não foi fornecido.

**Ativos afetados:** serviço `billing-api`, tabela `invoices`.
**Causa raiz:** concatenação direta de entrada do usuário na cláusula `WHERE`, sem bind
parameters do driver `pg`.
**Ponto de entrada:** campo `customer` do corpo JSON.
**Fronteira de confiança:** usuário autenticado (nível `customer`) → dados de faturamento
de qualquer cliente.

## Impacto

Exposição de dados de faturamento (valores, status de pagamento, identificadores)
pertencentes a outros clientes. Pré-condição: usuário autenticado com acesso à rota.

## Reprodução controlada

Não executada — sem autorização para testes ativos nesta sessão.

PoC descrita (não executada): enviar `POST /api/v1/invoices/search` com
`{"customer": "' OR '1'='1"}`. Esperado em sistema seguro: erro de validação ou nenhum
resultado. Comportamento hipotético no código atual: retorno de todos os registros da
tabela `invoices`.

## Correção sugerida

Substituir a concatenação por parâmetro vinculado nativo do driver `pg`:

```ts
// antes
db.query(`SELECT * FROM invoices WHERE customer = '${customer}'`);

// depois
db.query('SELECT * FROM invoices WHERE customer = $1', [customer]);
```

**Controles compensatórios:** nenhum identificado no código analisado.
**Validação segura pós-correção:** reenviar o mesmo payload de teste e confirmar erro de
parâmetro inválido ou ausência de resultado, em vez do retorno de todos os registros.

## Desconhecidos e próximos passos

- Confirmar com a equipe se existe middleware global de sanitização para o corpo da
  requisição; se existir, reavaliar este achado.
- Obter autorização de ambiente de homologação para reprodução controlada da PoC, se
  desejado.
- Estender a mesma verificação de parametrização às demais rotas de `billing-api`.
