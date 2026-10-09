# Runbook 02 — Modelagem de domínio novo

**Pré-condição:** requisitos e inventário suficientemente confirmados.

1. Desenhar modelo conceitual sem tipos físicos.
2. Criar modelo lógico com entidades, cardinalidades e normalização adequada.
3. Projetar schema físico: tabelas, PK, FK, types, nullability, defaults, CHECK, unique, indices.
4. Traçar evidências por decisão; tratar hipótese pendente como tal.
5. Validar limites de tenant, dados pessoais, idempotência, deletes, relatórios e consultas.
6. Produzir ERD em Mermaid/DBML e proposta com `schemas/domain-model.schema.json`.
7. Gerar migrations/Models Eloquent versionáveis, sem aplicar no banco.
8. Criar testes de constraints/relações (não executar se escreverem no banco).
9. Executar apenas lint, syntax e inspeção não mutante disponível.
10. Entregar plano de execução delegada e lista de decisões.

**Aceite:** cada entidade e constraint importante tem justificativa e consumidor; diff revisado e testes claramente classificados.
