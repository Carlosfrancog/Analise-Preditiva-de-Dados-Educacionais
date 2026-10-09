# Capacidades e dependências

| Área | Capacidades | Ferramentas opcionais |
|---|---|---|
| Build | Dockerfile, multi-stage, BuildKit, cache, multiarch, SBOM | Docker, Buildx, Dive, Syft, Hadolint |
| Compose | Serviços, profiles, environment, secrets, health, networks e volumes | Docker Compose v2 |
| Diagnóstico | Status, exit code, logs redigidos, eventos, métricas | CLI Docker, Linux `ps`, `ss`, `df`, `journalctl` |
| Rede | DNS, bridge, portas, proxy, TLS, firewall, HTTP/TCP | `getent`, `ss`, `curl`, ferramentas de rede |
| Persistência | mounts, permissões, backup/restore em ambiente controlado | CLI Docker, utilitários do banco, snapshot storage |
| Performance | CPU, memória, throttling, OOM, I/O, log growth | Docker stats, cgroups, Prometheus/Grafana |
| Segurança | usuário, capabilities, profiles, secrets, vulnerabilidades, cadeia de suprimentos | Trivy, Scout, Syft, Cosign |
| Delivery | registry, artefatos, CI, staging, rollback, imagens imutáveis | GitLab CI/CD, GitHub Actions |

**Capacidade declarada != ferramenta instalada ou permissão concedida.** Checar disponibilidade, versão e escopo antes de acionar. Ferramentas externas de scan podem transmitir metadados ou consultar rede; verificar requisitos de privacidade e autorização.

## Interfaces

**Entrada:** `schemas/task-request.schema.json` (ou pedido textual equivalente).  
**Inventário:** `schemas/inventory.schema.json`.  
**Plano:** `schemas/change-plan.schema.json`.  
**Resultado:** `schemas/execution-report.schema.json`.  
**Handoff:** `schemas/handoff.schema.json`.

Fatos são acompanhados de `FACT`, `INFERENCE`, `HYPOTHESIS` ou `UNKNOWN` quando a distinção ajuda a decisão. Evitar gerar falsos JSONs: `null` ou `UNKNOWN` é preferível a preencher valores imaginados.
