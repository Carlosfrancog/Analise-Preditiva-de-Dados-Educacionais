# Skill: Go Performance

Performance deve ser comparada, não presumida.

## Baseline

```bash
go test ./...
go test -race ./...
go test -bench=. -benchmem ./...
```

## Benchmark específico

```bash
go test -bench=BenchmarkNome -benchmem -count=5 ./caminho/pacote
```

## CPU

```bash
go test -bench=BenchmarkNome -cpuprofile=cpu.out ./caminho/pacote
go tool pprof -http=:8080 cpu.out
```

## Memória

```bash
go test -bench=BenchmarkNome -memprofile=mem.out ./caminho/pacote
go tool pprof -http=:8080 mem.out
```

## Escape analysis

```bash
go build -gcflags="-m=2" ./...
```

Antes de sugerir `sync.Pool`, observe `allocs/op`, `B/op`, frequência do GC, lifetime dos buffers e ownership.
