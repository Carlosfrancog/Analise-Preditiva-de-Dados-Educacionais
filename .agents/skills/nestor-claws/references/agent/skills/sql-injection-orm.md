# SKILL — SQL/NoSQL Injection em queries e ORMs

**Quando usar:** o projeto usa SQL bruto, query builders, ORM, ou acesso a banco
documento (MongoDB) com filtros construídos a partir de entrada do usuário.

## Procedimento

1. Localizar todos os pontos onde queries são montadas: SQL bruto, métodos de ORM que
   aceitam string crua (`.raw()`, `.query()`, interpolação em template literal), e
   filtros dinâmicos em bancos documento (MongoDB `$where`, operadores construídos a
   partir de chaves do payload).
2. Para cada ponto, rastrear a origem do valor até a entrada do usuário (query string,
   body, header, path param, campo de formulário).
3. Verificar o mecanismo de parametrização:
   - bind parameters / prepared statements → risco mitigado, registrar como controle
     compensatório;
   - concatenação de string com valor do usuário, mesmo que "escapado" manualmente →
     candidato a SQL Injection;
   - uso de ORM sem escape adicional em cláusula `orderBy`/`groupBy` dinâmica → candidato
     a Injection fora do caminho óbvio de `WHERE`.
4. **Nunca declarar SQL Injection apenas pela existência de SQL bruto.** O achado só é
   aceito se a entrada controlável chegar à execução sem parametrização.
5. Verificar se mensagens de erro de banco retornam ao cliente (stack trace, nome de
   tabela/coluna) — tratar como achado correlato de "Information Disclosure", não como
   SQL Injection.
6. Checar se há vazamento inadvertido de dados sensíveis via `SELECT *` em endpoints que
   expõem a resposta diretamente ao cliente.

## Critérios de aceitação de achado

- Trecho de código com arquivo e linha mostrando concatenação/interpolação não
  parametrizada.
- Confirmação de que o valor é controlável pelo usuário (origem rastreada).
- Se blind (sem retorno direto de dados), explicitar a hipótese e marcar como
  `HYPOTHESIS` até reprodução controlada autorizada.

## Reprodução controlada (apenas com autorização)

Descreva a PoC (payload, rota/parâmetro, resposta esperada vs. observada) sem executá-la
a menos que `run_active_tests` esteja autorizado para este alvo — ver
`../runbooks/autorizacao-testes-ativos.md`.

## Saída

`../schemas/finding.schema.json`, com `root_cause` descrevendo o mecanismo de
parametrização ausente/insuficiente.
