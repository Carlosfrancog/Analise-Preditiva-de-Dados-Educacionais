# SKILL — IDOR/BOLA e isolamento multi-tenant

**Quando usar:** rotas/consultas que recebem um identificador (ID, slug, UUID) e retornam
ou alteram um recurso específico; sistemas com mais de um tenant/empresa/usuário
compartilhando o mesmo schema ou banco.

## Procedimento

1. Mapear rotas que recebem identificador de recurso via path, query ou body
   (`GET /orders/:id`, `GET /users/:id/invoices`, etc.).
2. Para cada rota, verificar se existe checagem de posse/pertencimento do recurso ao
   usuário autenticado (ex.: `WHERE user_id = :current_user AND id = :id`) — e não apenas
   checagem de autenticação genérica.
3. Verificar middlewares globais, políticas de serviço e controles do banco (row-level
   security, filtros automáticos por tenant) **antes de afirmar ausência de autorização**
   em uma rota — ver `../policies/code-policy.md`.
4. Correlacionar deterministicamente as permissões da rota com os privilégios mapeados nas
   tabelas de controle de acesso do banco antes de declarar quebra de privilégio (ver
   `../principles.md`).
5. Para sistemas multi-tenant, verificar se o identificador de tenant é derivado do
   contexto autenticado (token/sessão) ou se é aceito como parâmetro confiável vindo do
   cliente — este último é um candidato direto de vazamento entre tenants.
6. Repetir a checagem para operações de escrita/exclusão, não apenas leitura.

## Critérios de aceitação de achado

- Rota e método HTTP específicos.
- Trecho de código mostrando a consulta/autorização (ou sua ausência) com arquivo e linha.
- Se a rota tiver proteção via middleware global não visível no trecho analisado, marcar
  como `UNKNOWN` e solicitar o arquivo do middleware antes de concluir.

## Reprodução controlada (apenas com autorização)

Descreva o teste (requisição com ID de outro usuário/tenant, usando credenciais de teste
de dois níveis de privilégio distintos) sem executá-lo sem autorização — ver
`../runbooks/autorizacao-testes-ativos.md`.

## Saída

`../schemas/finding.schema.json`, com `trust_boundary` explicitando a fronteira
(usuário↔usuário ou tenant↔tenant) violada ou preservada.
