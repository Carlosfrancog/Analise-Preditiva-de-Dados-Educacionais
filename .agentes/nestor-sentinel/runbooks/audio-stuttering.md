# Runbook: Audio Stuttering

Investigue nesta ordem inicial:

1. underrun do player;
2. duração real dos frames;
3. intervalo entre frames recebidos;
4. jitter p50/p95/p99;
5. queue depth;
6. packet loss/retransmissão;
7. consumidor lento bloqueando broadcast;
8. pausas de GC;
9. saturação de CPU;
10. resampling incorreto;
11. sample rate inconsistente;
12. drift de clock.

Não aumente buffer sem calcular o custo de latência introduzido.
