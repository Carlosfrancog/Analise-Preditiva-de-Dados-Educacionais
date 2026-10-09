# Skill: redes, DNS, portas, proxy e TLS

**Quando ativar:** erro de conexão, timeout, `connection refused`, DNS, proxy, CORS aparente, websocket/gRPC, certificados.

## Hipóteses por camada

1. DNS: resolução do nome do serviço/hostname na rede correta.
2. Processo: aplicação escutando endereço/interface esperada no namespace do container (0.0.0.0 vs 127.0.0.1).
3. Topologia: origem e destino compartilham rede roteável? bridge, host, overlay, external network.
4. Porta: `expose` é documentação interna; `ports` publica host; verificar mapeamento e bind.
5. Host: firewall, NAT, VPN/WSL2, IPv4/IPv6 e conflito de bind.
6. Camada L7: upstream reverse proxy, Host header, WebSocket upgrade, TLS/SNI, timeouts, health endpoint.

## Ferramentas de baixo risco

`docker network ls`/`inspect` com mínima exibição; `ss -ltn` em ambiente autorizado; `getent hosts`; `curl --head` ou requisição de saúde conhecida; teste TCP direcionado e com timeout. Não realizar varredura de rede fora do escopo.

## Critérios de aceite

Trajeto origem→destino funcional na rede prevista; exposição externa limitada; certificado e headers pertinentes; falhas de rede diferenciadas de falhas da aplicação.
