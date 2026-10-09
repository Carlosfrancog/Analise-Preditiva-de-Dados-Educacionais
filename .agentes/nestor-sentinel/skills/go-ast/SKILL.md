# Skill: Go AST

Use AST para responder perguntas estruturais sem ler arquivos inteiros desnecessariamente.

Ferramentas base:

```bash
go vet ./...
staticcheck ./...
```

Com `go/parser`, `go/ast`, `go/token` e `go/packages`, procurar por:

- criação de goroutines;
- criação de channels;
- chamadas específicas;
- uso de `append` em hot paths;
- I/O de disco;
- `time.After` recorrente;
- símbolos e dependências;
- possíveis padrões proibidos.

AST complementa análise runtime; não substitui profiling, race detector, testes ou métricas.
