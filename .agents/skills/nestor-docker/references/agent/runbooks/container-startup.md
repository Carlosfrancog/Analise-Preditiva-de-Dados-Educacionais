# Runbook: falha ao iniciar container / restart loop

## Objetivo

Diferenciar falhas da imagem, entrypoint, dependências, permissões, processo, sinais, arquitetura, healthcheck e recursos.

## Roteiro

1. Confirmar serviço, nome do projeto Compose e host.
2. Verificar estado, última saída, restart count e `OOMKilled` via consulta seletiva (evitar `docker inspect` integral).
3. Verificar se houve erro em `docker compose config --quiet`, imagem/tag incorreta ou arquivo/mount ausente.
4. Diferenciar erro de build de falha de runtime: `exec format error` sugere arquitetura; `no such file` pode ser entrypoint, shebang/CRLF, dynamic linker ou caminho.
5. Verificar direitos de execução, usuário efetivo e UID/GID dos mounts.
6. Verificar se processo principal encerra naturalmente e restart policy reinicia; `EXIT 0` não significa sucesso para um serviço daemon.
7. Distinguir healthcheck reprovado de crash do processo; `unhealthy` pode coexistir com running.
8. Se houver exit code 137, investigar SIGKILL/OOM e não presumir memória como única causa.
9. Verificar DNS, readiness e serviços externos somente depois de estabelecer que o processo inicia.
10. Propor correção mínima; não desabilitar healthcheck nem usar sleep eterno para “corrigir”.

## Gate

Não rodar `restart`, `up`, `down`, `exec` mutável ou `rm` em serviço ativo sem autorização da classe correspondente. Testar nova imagem em ambiente isolado, quando possível.

## Aceite

Processo inicia e mantém comportamento esperado, sinais são tratados, healthcheck e rota de aplicação são válidos, logs não expõem dados sensíveis, sem crash loop após janela apropriada.
