# Skill: registries, CI/CD, deploy e rollback

**Quando ativar:** pipeline quebrado, push, tags, builds em runner, cache, rollout ou rollback.

## Pipeline seguro

- Identificar sistema GitLab/GitHub e versão do runner/engine; analisar permissões e separação de ambientes.
- Gerar imagem rastreável por commit/SHA e versão; tag não substitui digest imutável.
- Separar build, lint/scan, teste, publicação e deploy com gates adequados.
- Autenticar registry via mecanismo de CI e secrets, jamais inline em logs/arquivos.
- Considerar BuildKit/Buildx, cache import/export e riscos de caches públicos/compartilhados.
- Evitar pipelines que façam `prune`, rollout ou migração de dados automaticamente sem autorização organizacional.
- Considerar política de retenção e capacidade de rollback; não sobrescrever sem rastreabilidade a última imagem estável.

## Validação

Configuração YAML válida, jobs condicionais adequados, versão buildada corresponde ao código, secrets redigidos, artefatos íntegros e deploy autorizado confirmado em ambiente escolhido. Não afirmar CI verde sem run ID/resultado verificado.
