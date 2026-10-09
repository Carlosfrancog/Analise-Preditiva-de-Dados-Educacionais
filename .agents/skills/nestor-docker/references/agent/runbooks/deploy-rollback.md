# Runbook: deploy e rollback de container

## Atenção

Deploy e rollback modificam serviços ativos. **Exigem aprovação direcionada** para alvo, versão, janela e impacto. Este documento não concede autorização.

## Antes

1. Identificar host/contexto, projeto Compose, ambiente e owner operacional.
2. Confirmar versão de origem, imagem candidata (digest/tag), mudanças e dependências.
3. Verificar disponibilidade/retorno de dados, backup consistente quando relevante, schema compatível e impossibilidade de automatizar migrações de DB sem permissão.
4. Definir gates pré e pós deploy: build, CI, smoke tests, health, métricas e janela.
5. Planejar reversão de imagem/config, limitação de alterações de dados e tempo de recovery; rollback de código **não reverte** dados por si só.
6. Confirmar aprovação específica antes de executar ação mutável.

## Durante (somente autorizado)

- Registrar versão e horários; aplicar de maneira incremental quando ambiente suportar.
- Monitorar sinais de inicialização, perda de conexões, health e fluxos críticos.
- Interromper/rollback se thresholds acordados forem violados; não inventar zero downtime.

## Depois

Executar testes de rota de usuário, erros, métricas e logs redigidos. Registrar evidências e pendências. Se rollback ocorrer, registrar causa, versão retomada e estado dos dados.
