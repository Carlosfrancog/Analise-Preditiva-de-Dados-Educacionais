# Adapter: GitLab CI/CD

- Verificar runners, executor, serviço DinD/rootless e compatibilidade de versões antes de desenhar pipeline.
- Minimizar permissões de tokens do registry; mascarar variáveis protegidas; restringir jobs de deploy por ambiente/branch/regra.
- Rastrear imagem por commit SHA e preferencialmente digest; preservar estratégia de cache e rollback.
- Não executar prune remoto, deploy ou database migration apenas pela existência de script no repositório.
- Diferenciar falha de runner, rede, rate limit, registry auth, build e aplicação.
