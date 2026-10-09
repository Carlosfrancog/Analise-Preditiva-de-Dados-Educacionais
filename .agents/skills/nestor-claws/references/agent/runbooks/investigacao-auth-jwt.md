# RUNBOOK — Investigação dirigida: autenticação, sessão e JWT

**Quando usar:** o solicitante pede verificação de login, emissão/validação de token, ou
gestão de sessão.

## Sequência

1. Confirmar escopo mínimo: módulo/arquivo de emissão e validação de token ou sessão.
2. Aplicar `../skills/autenticacao-sessao-jwt.md` integralmente.
3. Para cada item avaliado (algoritmo, expiração, revogação, armazenamento de chave,
   flags de cookie), citar o valor exato encontrado no código/configuração — nunca
   assumir um padrão de biblioteca sem confirmar no código do projeto.
4. Classificar como `HYPOTHESIS` qualquer comportamento que dependa de uma biblioteca
   externa cujo código-fonte de validação não foi inspecionado.
5. Se autorizado teste ativo (ver `autorizacao-testes-ativos.md`), descrever e, se
   permitido, testar cenários como: token expirado ainda aceito, token com `alg` alterado,
   ausência de regeneração de sessão pós-login.
6. Preencher `../schemas/finding.schema.json`. Não atribuir CVSS sem declarar método e
   vetor (ver `../principles.md`).
