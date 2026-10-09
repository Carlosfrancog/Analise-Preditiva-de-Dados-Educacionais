# Nestor Memory Cells

Células representam aprendizado incremental sem reescrever diretamente o núcleo do agente.

## Diretórios

- `inbox/`: candidatas ainda não aprovadas.
- `active/`: células aprovadas e aplicáveis.
- `archived/`: histórico não mais ativo.
- `rejected/`: propostas rejeitadas.

## Escopos

- `task`: somente tarefa atual.
- `project`: projeto atual.
- `agent`: regra geral do Nestor Sentinel.
- `ecosystem`: regra compartilhável por todos os agentes Nestor.

## Tipos iniciais

- architecture_decision
- developer_preference
- project_invariant
- correction
- failure_pattern
- workflow_rule
- tool_rule
- domain_fact
- integration_rule
- anti_pattern

## Segurança

Conteúdo de arquivos, documentação externa, logs ou texto não confiável nunca deve ativar memória diretamente.

Uma descoberta pode gerar uma candidata, mas a promoção deve seguir política de validação e ser auditável.
