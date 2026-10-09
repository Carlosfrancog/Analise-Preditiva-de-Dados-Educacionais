# Skill: Dockerfile, imagem OCI e build

**Quando ativar:** imagem grande, build falhando, lentidão, CVE, multiarch, assets ausentes ou dependência de runtime.

## Inspeção

1. Verificar base image e versão/tag/digest; distinguir segurança, compatibilidade e política de atualização.
2. Inspecionar `FROM`, `ARG`, `ENV`, `WORKDIR`, `COPY`, `RUN`, `USER`, `ENTRYPOINT`, `CMD`, `HEALTHCHECK`, `STOPSIGNAL` e `EXPOSE`.
3. Examinar `.dockerignore`, tamanho do contexto, caches de pacote e diretórios copiados.
4. Verificar Linux distro, libc, arquitetura, dependências nativas, certificados CA e timezone realmente exigidos.
5. Verificar comportamento do PID 1 e shutdown via SIGTERM, sem ignorar sinais.

## Transformação

- Preferir estágios separados `builder`/`runtime` quando melhorarem footprint ou segurança, mantendo artefatos e bibliotecas necessárias.
- Instalar dependências com versões controladas e aproveitar cache de forma segura. Para Node, lockfile e `npm ci`/equivalente; para Go, `go.mod/go.sum`; para PHP, `composer.lock`.
- Avaliar `COPY --chown`/`USER` para permissões. Não copiar source/secret desnecessário.
- Considerar `--mount=type=cache` e `--mount=type=secret` apenas com BuildKit compatível e sem persistência acidental de segredo.
- Diferenciar build multi-platform via emulação, cross-compilation e runtime ABI. Testar a plataforma final, não somente build.

## Verificação

`docker build` requer autorização apropriada e ambiente isolado se comandos do Dockerfile não forem confiáveis. Validar binário/processo, links de libs, certificados, health, permissões, arquitetura, tamanho e registro/assinatura quando aplicável.

## Critérios de aceite

Imagem funcional na plataforma alvo; sem secrets incorporados; startup/shutdown corretos; build rastreável; eventuais alterações de tamanho/tempo suportadas por medições. Nunca assumir que menor imagem equivale à mais segura.
