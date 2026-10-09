# Runbook 00 — Triagem e classificação

**Entrada:** objetivo da tarefa, acesso ao projeto e qualquer inventário existente.

1. Classificar como criação, evolução, auditoria, integração, performance ou planejamento de migração.
2. Determinar repo, branch, commit, versões e se há banco real acessível.
3. Consultar `git status` e arquivos de instruções locais. Não ler nem revelar credenciais desnecessárias.
4. Checar `modify_database=false`; planejar somente modificações em código.
5. Definir critérios de aceite e perguntas bloqueantes sobre ownership, dados ou regras.
6. Selecionar skill e runbook relevante.

**Saída:** escopo, versão/ambiente observado ou UNKNOWN, permissões, fontes, limitações e plano curto.

**Parar se:** não houver repositório/fonte suficiente para sustentar uma proposta concreta, ou a operação requerida exigir acesso não autorizado.
