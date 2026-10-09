# RUNBOOK — Investigação dirigida: SQL/NoSQL Injection

**Quando usar:** o solicitante já suspeita ou pede especificamente uma investigação de
injeção em um endpoint, query ou tabela.

## Sequência

1. Confirmar escopo mínimo: arquivo(s) ou rota(s) alvo, e se há acesso ao schema do banco
   relevante. Se faltar o schema e ele for necessário para avaliar impacto, listar a
   lacuna (ver `../policies/context-policy.md`) em vez de presumir estrutura.
2. Aplicar `../skills/sql-injection-orm.md` integralmente sobre o(s) ponto(s) indicado(s).
3. Classificar o achado:
   - **FACT**: entrada controlável chega à execução sem parametrização — demonstrado por
     arquivo e linha.
   - **HYPOTHESIS**: suspeita plausível, mas sem confirmação de alcançabilidade (ex.:
     depende de middleware de validação cujo código não foi fornecido).
   - **UNKNOWN**: impossível avaliar sem informação adicional (nomear exatamente o que
     falta).
4. Se o achado for `FACT` e o solicitante autorizar teste ativo (ver
   `autorizacao-testes-ativos.md`), descrever a PoC com `../skills/poc-e-testes-manuais.md`
   antes de qualquer execução, e usar SQLMap apenas em homologação isolada autorizada
   (ver `../policies/tools-policy.md`).
5. Propor correção seguindo a hierarquia de decisão de `../capabilities.md`: preferir
   parametrização nativa do ORM/driver já usado no projeto, sem introduzir nova
   dependência.
6. Preencher `../schemas/finding.schema.json` e entregar conforme formato de resposta em
   `../AGENT.md`.
