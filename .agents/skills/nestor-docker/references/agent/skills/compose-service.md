# Skill: Compose e lifecycle de serviços

**Quando ativar:** `compose.yaml`, dependências, profiles, ambientes, health, restart ou topologia.

## Diagnóstico

- Identificar projetos Compose e seleção de arquivos (`-f`, `COMPOSE_FILE`, project name) antes de agir.
- Verificar disponibilidade/versionamento de Docker Compose v2 e recursos usados; **não** confiar cegamente em snippets genéricos.
- Analisar serviços, imagens, build, entrypoint, command, env_file, environment, volumes, networks, ports, restart, healthcheck, profiles e depends_on.
- Verificar `docker compose config --quiet` (validação, evitando dump de secrets). `docker compose config --services` pode listar serviços, mas não comprova prontidão.
- Verificar se `depends_on` por ordem de criação é suficiente ou se readiness healthcheck/application retry é necessário.

## Implementação

- Usar configurações ambientais explícitas, paths claros, mounts consistentes e variáveis obrigatórias bem definidas.
- Evitar replicar credenciais em YAML. Separar configuração sensível de arquivo versionado.
- Evitar `container_name` fixo quando impedir escalabilidade/isolamento entre projetos, salvo exigência concreta.
- Não definir `deploy.resources` ou opções avançadas pressupondo efeito idêntico em todas as versões de Compose/plataformas; testar.
- Não criar rede externa, volume ou binding não solicitado sem considerar compartilhamento.

## Critérios de aceite

Arquivo resolve na versão instalada, dependências mapeadas, serviços iniciam quando autorizado, comunicação funciona, mounts preservados e testes da aplicação aprovados. `docker compose up` não é operação meramente sintática e pode alterar containers existentes.
