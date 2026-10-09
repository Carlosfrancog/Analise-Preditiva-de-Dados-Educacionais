# Tooling Roadmap

A futura CLI `nestor` deve priorizar extração determinística de contexto.

Primeiros comandos planejados:

- `nestor repo`: resumo estrutural do repositório;
- `nestor diff`: resumo semântico das mudanças;
- `nestor symbols`: inventário de símbolos;
- `nestor trace <symbol>`: dependências de um símbolo;
- `nestor audio <arquivo>`: análise compacta via ffprobe/FFmpeg;
- `nestor perf`: execução e resumo de benchmarks/profiling;
- `nestor memory ...`: gestão de células;
- `nestor agent create`: Nestor Forge básico.

Regra: não usar LLM internamente para fatos que Git, AST, go/packages, FFprobe, pprof ou métricas conseguem obter deterministicamente.
