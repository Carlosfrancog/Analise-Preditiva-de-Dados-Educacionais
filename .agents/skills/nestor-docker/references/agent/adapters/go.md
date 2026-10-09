# Adapter: Go em containers

- Decidir CGO_ENABLED, arquitetura/GOOS e libc a partir das dependências efetivas. `CGO_ENABLED=0` não é universal; bindings C/audio/SQLite podem exigir CGO e libs nativas.
- Cache de `go.mod`/`go.sum` e módulos, separar build/runtime quando compatível.
- Garantir artefatos embedded, assets, certificados e localização esperada dos arquivos.
- Confirmar SIGTERM, context cancellation e graceful shutdown de HTTP/WS/UDP.
- Em serviços de áudio/rede em tempo real, preservar portas UDP/TCP, MTU, permissões e comportamento de latência antes de otimizar.
- Validar runtime no host/plataforma de destino; compile success não basta.
