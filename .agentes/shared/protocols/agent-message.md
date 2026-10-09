# Nestor Agent Message v1

Formato futuro para comunicação entre agentes.

```json
{
  "protocol": "nestor.agent-message.v1",
  "from": "nestor-sentinel",
  "to": "capability:infrastructure.analysis",
  "type": "analysis-request",
  "context": {},
  "artifacts": [],
  "expected_output": []
}
```

Agentes devem preferir artefatos estruturados e compactos em vez de transcrições longas.
