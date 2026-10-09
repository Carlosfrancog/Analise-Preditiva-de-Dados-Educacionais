# Skill — Segurança de persistência e isolamento multi-tenant

## Identificar

- Tenant real: organização, empresa, cliente, workspace, usuário ou particionamento híbrido.
- Ownership e chave: coluna de escopo, FK, pivot, escopo associado, membership.
- Isolamento: policies, scopes, middleware, APIs, background jobs e consultas administrativas.
- Risco de vínculos cruzados: FKs simples podem existir sem garantir que duas linhas tenham o mesmo tenant.

## Opções (sem aplicar sem evidência)

- Chaves compostas de negócio e FKs compostas para cruzamentos dentro da mesma organização.
- `UNIQUE(tenant_id, external_id)` para IDs que só são únicos dentro de tenant.
- Filtro obrigatório na aplicação e autorização em cada operação; avaliar vulnerabilidade de IDOR.
- RLS PostgreSQL apenas quando há desenho de autenticação/roles/configuração de sessão compatível.
- Audit logs, retenção, anonimização e soft deletes somente conforme requisitos aprovados.

## Validar

Preparar casos de teste de acesso negado entre tenants e invariantes de relações. Não executar suites que escrevam no banco com as permissões atuais. Não simular conformidade LGPD a partir de mera modelagem.
