# Runbook: High Latency

Não altere buffers primeiro.

Obtenha timestamps ou métricas equivalentes para:

1. captura;
2. envio;
3. recebimento no servidor;
4. início/fim do processamento;
5. entrada/saída de serviços Speech;
6. distribuição;
7. recebimento do cliente;
8. reprodução.

Calcule o delta por estágio e identifique onde o orçamento está sendo consumido.

Só então altere a etapa dominante.
