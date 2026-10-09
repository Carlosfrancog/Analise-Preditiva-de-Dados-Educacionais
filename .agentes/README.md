# Ecossistema Nestor

A pasta `.agentes` contém a definição portátil dos agentes Nestor.

## Princípios

1. O núcleo do agente não deve ser alterado silenciosamente por aprendizado temporário.
2. Aprendizados novos entram como células de memória versionáveis.
3. Skills contêm conhecimento operacional reutilizável.
4. Runbooks descrevem investigação de sintomas recorrentes.
5. Adapters expõem o agente a ferramentas como Claude e Codex sem duplicar o conhecimento central.
6. Futuramente vários agentes poderão trocar artefatos estruturados por capability routing.

## Uso neste projeto

O registro em `registry/agents.json` contém o Nestor Sentinel importado do pacote v0.1 e o Nestor Web criado para o EPA. O arquivo `../AGENTS.md` indica qual definição consultar em cada tipo de tarefa. O contexto compartilhado fica em `context/project-context.md`.
