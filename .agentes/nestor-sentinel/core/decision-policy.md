# Decision Policy

## Menor alteração possível

Ao corrigir um problema, altere inicialmente apenas o necessário para resolver a causa identificada.

Evite refatorações cosméticas ou arquiteturais não relacionadas durante investigação de bug.

## Ferramenta correta para a hipótese

- comportamento funcional: testes e leitura de fluxo;
- concorrência: race detector, trace, análise de ownership;
- CPU: pprof CPU;
- memória: benchmem, pprof heap, escape analysis;
- áudio: ffprobe, FFmpeg, métricas temporais;
- rede: métricas, tcpdump/Wireshark quando necessário;
- estrutura de código: AST e go/packages.

AST complementa, mas não substitui testes, profiling, logs, traces e leitura do código.

## Concorrência

Não trate channels, mutexes, atomics ou sync.Pool como soluções universais.

Escolha a primitiva de acordo com ownership, contenção, latência e lifetime dos objetos.

Um consumidor lento nunca deve bloquear indefinidamente todos os demais consumidores.
