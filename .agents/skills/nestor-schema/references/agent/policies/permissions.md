# Política de autoridade, permissões e efeitos

## Do relatório original

`read_code=true`, `run_analysis_tools=true`, `run_active_tests=true`, `write_code=true`, `modify_business_rules=false`, `modify_database=false`.

## Classes de ação

| Classe | Exemplo | Status com permissões atuais |
|---|---|---|
| Leitura de repositório | grep, AST, inspeção de migrations | Permitida dentro do escopo |
| Leitura de banco | `pg_catalog`, `information_schema`, `EXPLAIN` não executante | Condicional a credenciais read-only e autorização |
| Alteração de arquivos | criar migration/model/teste/ERD | Permitida no escopo |
| Teste sem banco mutante | lint, PHP syntax, verificação estática | Permitido |
| Teste que escreve no banco | PHPUnit/Pest com RefreshDatabase, migrate/test-schema | Não executar com `modify_database=false` |
| Mudança de regra comercial | mudar política de retenção ou visibilidade | Proibida sem nova autorização e mudança de permissões |
| Escrita em banco | `artisan migrate`, `db:seed`, `DROP`, `UPDATE` | Proibida com `modify_database=false` |

**Mesmo banco descartável é banco:** o presente perfil não executa alterações. Produzir plano e script para executor especificamente autorizado; uma autorização verbal não reconfigura uma permissão fixa de ferramenta. Se a plataforma oferecer delegação com limites, essa execução ocorre fora do Nestor Schema e com evidência formal do executor.

Nunca confundir ferramenta disponível com permissão concedida. Não iniciar testes que possam executar migrations implicitamente. Não editar `.env` para redirecionar testes a bancos reais.
