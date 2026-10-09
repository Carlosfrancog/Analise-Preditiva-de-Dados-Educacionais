# RUNBOOK — Autorização para testes ativos

**Objetivo:** definir as condições sob as quais `run_active_tests` pode ser considerado
`true` para uma investigação pontual, e como conduzir o teste com segurança quando
autorizado.

Por padrão, `run_active_tests = false` (ver `../policies/permissions.md`). Este runbook
só se aplica quando o solicitante concede autorização explícita **dentro da sessão
corrente**.

## Checklist de autorização mínima

Antes de executar qualquer requisição ativa, PoC ou ferramenta dinâmica (cURL, Postman/
Newman, SQLMap, consultas de escrita), confirmar que todos os itens abaixo foram
fornecidos explicitamente pelo solicitante:

- [ ] Alvo nomeado explicitamente (host/ambiente específico — nunca inferir produção por
      padrão).
- [ ] Ambiente autorizado (ex.: homologação isolada) — nunca produção, salvo autorização
      explícita e justificada para o item específico.
- [ ] Escopo do teste (quais rotas/funcionalidades podem ser exercitadas).
- [ ] Credenciais de teste fornecidas (se aplicável), com nível de privilégio conhecido.
- [ ] Confirmação de que o teste não terá efeito destrutivo não reversível, ou aceitação
      explícita do risco pelo solicitante.

Se qualquer item estiver ausente, **não execute** — descreva a PoC/teste como
procedimento (ver `../skills/poc-e-testes-manuais.md`) e solicite o item faltante.

## Durante o teste autorizado

1. Executar apenas dentro do alvo, ambiente e escopo autorizados — nunca estender a outros
   hosts, rotas ou ambientes "enquanto já está testando".
2. Preferir metadados e evitar retornar linhas com dados pessoais ao consultar banco
   diretamente (`psql`/`mysql` — ver `../policies/tools-policy.md`).
3. Registrar comportamento observado vs. esperado, com timestamp e comando exato usado.
4. Interromper imediatamente se houver sinal de impacto em disponibilidade ou integridade
   de dados não planejado.

## Após o teste

1. Mascarar segredos e dados pessoais coletados antes de incluí-los no relatório.
2. Destruir dados temporários obtidos durante o teste ao final da sessão (ver
   `../policies/final-rules.md`).
3. Preencher `reproduction.controlled = true` e os detalhes da execução em
   `../schemas/finding.schema.json`.
4. Se a equipe aplicar uma correção, comparar resultados antes/depois sem executar
   mudanças por conta própria (ver `../policies/final-rules.md` e
   `../skills/poc-e-testes-manuais.md`).
