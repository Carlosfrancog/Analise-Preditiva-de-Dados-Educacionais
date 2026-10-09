# Skill — Laravel/Eloquent e contratos de API

**Verificar antes:** versão PHP/Laravel, convenções de diretório, conexão PostgreSQL, modelos, traits e relações existentes.

## Mapeamento

- Modelo Eloquent → tabela e conexão reais; `getTable()`, `getKeyName()`, `$primaryKey`, `$keyType`, `$incrementing` quando aplicável.
- `belongsTo`, `hasMany`, `hasOne`, `belongsToMany` → nome de FK/pivot, chaves locais, timestamps e constraints reais.
- `morphTo`/`morphMany` → verificar representação e riscos de integridade referencial.
- `$casts`, atributos, accessors/mutators e enums PHP → tipos reais e serialização em API Resources.
- `FormRequest`/Rules → validação de UX e pré-condições; `UNIQUE`, `CHECK`, FKs → invariantes duráveis.
- `Policies`, Gates e global scopes → autorização, isolamento de tenant e filtros obrigatórios; revisar bypass administrativos.
- Jobs, events e observers → concorrência, idempotência, efeitos colaterais e limites transacionais.
- DTOs, Resources e frontend Inertia/Vue → contratos de entrada/saída sem reescrever frontend por conta própria.

## Antipadrões

- `fillable` expondo `organization_id`, `role`, `is_admin` indiscriminadamente.
- `exists` no request tratado como prova suficiente de relação válida entre tenants.
- Usar `sync` de pivots ignorando atributos, auditoria e regras do domínio.
- Criar N+1 com loops sem `with`/`load` e sem análise dos dados.
- Supor que `cascadeOnDelete()` é opção padrão.

## Artefatos

Planilha de contrato schema ↔ Eloquent ↔ request ↔ resource ↔ API, arquivos PHP propostos, teste de constraint/integração (não executar quando escrever em banco), e evidência de comparação.
