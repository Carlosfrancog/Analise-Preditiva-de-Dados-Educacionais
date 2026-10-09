# Runbook: validação por mudança

| Tipo | Gates mínimos | Gate de runtime |
|---|---|---|
| Dockerfile | sintaxe, revisão de secrets/contexto, versões, build autorizado | startup, user/perms, arquitetura, shutdown, smoke test |
| Compose | `docker compose config --quiet`, diff, env/ports/volumes/networks | readiness, DNS, health, APIs, persistence |
| Performance | baseline e métricas com janela | carga autorizada e regressões |
| Rede | topologia, DNS, ports, bind, firewall | conexão real de origem→destino |
| Storage | mounts, UID/GID, backup/consistência | persistência sem ação destrutiva; restore só em teste autorizado |
| CI/CD | YAML, permissions, tags/digests, secrets | job real concluído e versão rastreável |
| Segurança | análise de imagem/flags/exposição e secrets | controles ativos e aplicação funcional |

## Estados

`passed`: executado e aprovado; `failed`: executado e reprovado; `blocked`: impossível por permissão/pré-condição; `not_run`: não executado; `inconclusive`: resultado insuficiente. `NOT VERIFIED` não é sinônimo de `FAILED`.

## Checagem final

- Alteração realmente no escopo?
- Houve efeito operacional não autorizado?
- Evidências suficientes para concluir objetivo?
- Rollback específico ou limites de reversão registrados?
- Há secrets em output, imagens, arquivos ou artefatos?
- Há erros desconhecidos ou impacto em serviço adjacente?

Não afirmar deployment estável só porque comando retornou código 0.
