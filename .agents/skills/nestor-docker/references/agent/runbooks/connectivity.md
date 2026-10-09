# Runbook: falha de conectividade

## Problema

Container não acessa outro serviço, host não acessa container ou proxy retorna 502/504.

## Sequência

1. Identificar o sentido do tráfego: origem → destino, protocolo e porta.
2. Confirmar que os containers estão no mesmo contexto/host e a rede é roteável.
3. Verificar rede Compose, `networks`, aliases e resolução DNS por nome de serviço.
4. Confirmar processo escutando na interface adequada; processo em `127.0.0.1` no container pode ser inacessível por outro container.
5. Distinguir `EXPOSE`, portas internas e `ports` publicados no host.
6. Investigar firewall, publish address, NAT, IPv4/IPv6, WSL2/VM e conflitos de porta.
7. Investigar upstream do proxy, TLS/SNI, Host header, timeout e regras de websocket/upgrade.
8. Usar somente testes direcionados e autorizados, com timeout; não realizar varredura indiscriminada.
9. Classificar erro: DNS, refused, timeout, TLS, HTTP 4xx/5xx ou aplicação.
10. Validar conexão na mesma origem real do usuário e registrar evidência.

## Nota

Não publicar PostgreSQL/Redis em 0.0.0.0 para resolver conectividade interna. Não desabilitar firewall/TLS sem avaliação e autorização.
