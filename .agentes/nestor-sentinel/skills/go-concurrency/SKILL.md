# Skill: Go Concurrency

Não imponha uma única primitiva de concorrência.

## Channels

Preferir quando houver comunicação, coordenação ou transferência clara de ownership.

## Mutex

Preferir para estado compartilhado pequeno quando a proteção direta for mais simples e previsível.

## Atomics

Usar para estados simples e altamente concorridos quando a semântica estiver clara.

## Streaming

Filas de consumidores devem ser limitadas. Ao atingir capacidade, a política precisa ser explícita:

- drop oldest;
- drop newest;
- disconnect slow consumer;
- fallback;
- outra política documentada.

Nunca permita crescimento ilimitado de fila em hot path.

Nunca conclua que um broadcast é seguro sem verificar se um consumidor lento pode bloquear os demais.
