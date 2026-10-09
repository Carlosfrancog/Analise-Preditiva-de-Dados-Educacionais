# Runbook: CPU/RAM/disco elevados

## Entrada

Serviço, período, baseline, SLA/SLO, limitações do host, cargas de trabalho e mudanças recentes.

## Roteiro

1. Confirmar pressão no **host** e no **container**; `docker stats --no-stream` é uma amostra, não tendência.
2. Avaliar CPU%, cgroup CPU quota/throttling, processos, carga e correlacionar com tráfego real.
3. Avaliar memória por RSS/working set quando disponível, eventos cgroup e kill do kernel; diferenciar cache e uso efetivo.
4. Coletar códigos de saída e histórico de OOM sem inferir somente de `137`.
5. Avaliar latência do storage, espaço/inodes, crescimento de logs e volume, conexões e I/O.
6. Verificar leaks, retry storms, hot loops, gargalos de DB/rede e pool de processos.
7. Gerar hipóteses e testes pequenos; benchmark ou carga só em ambiente autorizado.
8. Propor correção no ponto causal (app, configuração, recurso, infraestrutura).
9. Validar com janela e carga comparáveis; registrar trade-offs.

## Não fazer

Não aumentar limites cegamente; não reiniciar para “esconder” vazamento como resolução definitiva; não rodar load test agressivo em produção sem autorização.
