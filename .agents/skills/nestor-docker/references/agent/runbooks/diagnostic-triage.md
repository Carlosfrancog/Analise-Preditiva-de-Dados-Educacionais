# Runbook: triagem de incidente Docker

## Disparador

Container indisponível, erro de build, serviço intermitente, performance degradada ou discrepância entre ambientes.

## Entrada

Ambiente/host/contexto Docker, serviço, impacto e desde quando, mudanças recentes, sintomas. Não receber tokens e secrets brutos.

## Checklist progressivo (somente leitura quando autorizado)

1. Confirmar **contexto** antes de qualquer comando: `docker context show`, `docker version --format '{{.Server.Version}}'` (o daemon pode estar inacessível), `docker compose version`.
2. Ler definição da stack e `docker compose config --quiet` para sintaxe; sem imprimir config interpolada.
3. Consultar `docker compose ps` ou `docker ps --format` em escopo mínimo e identificar `exited`, `restarting`, `unhealthy` ou `running`.
4. Extrair somente metadados de status/exit/OOM de container identificado. Não imprimir `docker inspect` completo.
5. Coletar eventos e logs de intervalo limitado **com redaction local**; `docker logs` bruto pode conter segredos.
6. Coletar métricas por janela, dependências, DNS/ports/mounts. Perguntar o que mudou antes do incidente.
7. Criar hipóteses e escolher teste discriminante de menor risco.
8. Confirmar causa ou declarar inconclusivo, com evidências.
9. Construir plano de ação, impacto, rollback e classificar autorização L0–L4.
10. Implementar somente após gates; verificar health e fluxo funcional.

## Resultado

Sintoma, timeline, `FACT/INFERENCE/HYPOTHESIS/UNKNOWN`, causa raiz confirmada ou provável, riscos, testes executados, ação e estabilidade pós-correção. Não confundir recuperação momentânea por restart com resolução da causa raiz.
