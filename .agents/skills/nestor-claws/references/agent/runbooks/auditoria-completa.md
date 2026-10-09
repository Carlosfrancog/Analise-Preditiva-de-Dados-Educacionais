# RUNBOOK — Auditoria completa

**Objetivo:** executar o pipeline de análise descrito em `../capabilities.md` do início ao
fim, produzindo um relatório estruturado conforme `../schemas/audit-report.schema.json`.

## Pré-requisitos

- Repositório/ativos definidos e acessíveis em modo leitura.
- Escopo preenchido conforme `../schemas/scope.schema.json` (repositório, revisão,
  ambiente, ativos permitidos, ferramentas autorizadas, exclusões).
- Confirmar se há autorização para testes ativos nesta sessão (padrão: não — ver
  `autorizacao-testes-ativos.md`).

## Sequência

1. **Registrar escopo.** Preencher `scope` do relatório. Se faltarem dados essenciais
   (ex.: ambiente, ativos permitidos), listar as lacunas e interromper até obtê-los — não
   presumir.
2. **Inventário (sem executar código do projeto).** Rodar a skill
   `../skills/sast-analise-estatica.md`, passo 1–2, para mapear manifests, linguagens,
   rotas e dependências.
3. **Mapeamento de entradas e fronteiras.** Identificar identidades, tenants e transições
   de privilégio (ver `../capabilities.md`, pipeline passo 3).
4. **Priorização de fluxos de risco.** Para cada fluxo priorizado, aplicar a skill
   específica:
   - entrada de dados → `../skills/sast-analise-estatica.md` e
     `../skills/sanitizacao-entrada-xss-ssrf.md`;
   - acesso a banco → `../skills/sql-injection-orm.md`;
   - autenticação/sessão → `../skills/autenticacao-sessao-jwt.md`;
   - autorização entre usuários/tenants → `../skills/idor-bola-multitenant.md`;
   - configuração/erros → `../skills/configuracao-tratamento-erros.md`;
   - segredos → `../skills/segredos-credenciais.md` (sempre incluída).
5. **Correlação.** Antes de declarar qualquer achado, correlacionar alertas de ferramenta
   com o código real e controles compensatórios (ver `../principles.md`).
6. **Validação estática.** Confirmar achados por leitura de código/configuração. Testes
   ativos somente se autorizados (`autorizacao-testes-ativos.md`).
7. **Classificação.** Para cada achado, preencher todos os campos obrigatórios de
   `../schemas/finding.schema.json`: estado, severidade, confiança, localização,
   evidências rotuladas, pré-condições, impacto, reprodução, correção, lacunas.
8. **Montagem do relatório.** Agregar achados em `../schemas/audit-report.schema.json`,
   com cobertura da auditoria (o que foi e o que não foi analisado) e lista de
   desconhecidos/próximos passos.
9. **Entrega.** Responder usando apenas as seções necessárias entre: Escopo e cobertura,
   Resumo executivo, Evidências, Impacto, Reprodução controlada, Correção sugerida,
   Desconhecidos e próximos passos (ver `../AGENT.md`).

## Critério de parada

Se, a qualquer momento, uma exploração lógica puder comprometer disponibilidade de APIs
ou integridade de dados em produção, interromper imediatamente e reportar o risco em vez
de prosseguir (ver `../policies/final-rules.md`).
