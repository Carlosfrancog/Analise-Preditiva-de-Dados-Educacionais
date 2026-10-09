# Skill: performance, métricas e logs

**Quando ativar:** CPU alta, OOM, lentidão, I/O, restart loop, storage saturado, latência.

## Diagnóstico por evidências

- Obter janela temporal, baseline e sintomas percebidos pela aplicação.
- CPU: `docker stats --no-stream`, CPU do host, throttling de cgroup, carga real e limites; um único percentual não prova bug.
- Memória: `memory.current`/limites quando aplicáveis, working set, eventos `oom`, `OOMKilled`, exit code e kernel log; avaliar caches e crescimento.
- I/O: latência de volumes, gargalos de disco, inodes, logs e persistência.
- Rede: bytes, retransmissões, conexões, timeouts e saturação; distinguir overlay/bridge e externo.
- Runtime: GC, pool de conexões, processo filho, watchdog, readiness e fila conforme stack.

## Mudança

Preferir reduzir causa comprovada antes de elevar limites. Alterar recursos somente com baseline, teste de carga autorizado e acompanhamento pós-mudança. Testes de carga não são seguros automaticamente em produção.

## Critérios de aceite

Estabilidade demonstrada por janela apropriada, métricas comparáveis, sem regressões nos endpoints, limites ajustados e risco residual declarado.
