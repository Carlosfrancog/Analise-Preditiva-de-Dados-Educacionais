# Skill — Descoberta do domínio por evidências

**Acionar quando:** houver pedido para modelar tabelas a partir de aplicação existente, auditar uma estrutura proposta ou conciliar fonte frontend/backend.

## Fontes de inspeção progressiva

1. Manifestos (composer.json, config/database.php sem secrets) e estrutura de diretórios.
2. Migrations, Models, relation methods, casts e scopes.
3. Form Requests, Rules, Policies/Gates, API Resources, DTOs.
4. Controllers, Actions, Services, Repositories, Jobs, Events/Listeners e comandos Artisan.
5. Rotas HTTP, contratos de frontend, formulários, filtros, paginação, relatórios e integrações externas.
6. Introspecção do schema real **read-only**, somente se autorizada e possível.

## Critério para entidade persistente

Para cada candidata, responder: o que representa; quem cria; quem mantém; quanto tempo vive; qual chave a identifica; quem a referencia; escopo de usuário/tenant; que consultas exigem persistência; se já existe em outro serviço; se é calculada ou cacheada.

Não transformar em tabela automaticamente: campo de formulário, opção visual, resultado calculado, objeto transitório, cache reconstruível ou payload externo replicado sem requisito.

## Matriz de rastreabilidade

| Evidência | Requisito observado | Entidade | Campo/relação | Status | Decisão pendente |
|---|---|---|---|---|---|
| `app/Http/...:42` | validação de email | `accounts` (hipótese) | email | INFERENCE | unicidade global/tenant? |

Os nomes da tabela são **apenas ilustrativos**. Preencher com arquivos reais no projeto analisado.

## Entrega

Inventário com proveniência, separação factual e dúvidas de domínio, schema conceitual sem DDL prematuro e tarefas de pesquisa para o Reader.
