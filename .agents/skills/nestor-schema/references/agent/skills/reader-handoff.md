# Skill — Interface de inventários com Nestor Reader

Nestor Reader e Nestor Schema compartilham **observações rastreáveis**, não conclusões não auditadas.

## Pedidos dirigidos ao Reader

- Descobrir os pontos de criação, alteração e consulta de entidade candidata.
- Listar métodos de relação Eloquent e migrations relacionadas com arquivo/linha.
- Relacionar Form Requests e API Resources aos atributos persistentes.
- Localizar jobs e operações concorrentes que possam violar invariantes.
- Encontrar políticas de autorização e filtros por tenant.
- Evidenciar chamadas de frontend/API que ainda não têm persistência equivalente.

## Consumir inventário

1. Conferir schema, projeto, commit e status de evidência.
2. Rastrear afirmações até arquivos. Se o repositório mudou, marcar stale e revalidar.
3. Separar ausência de evidência de evidência de ausência.
4. Alimentar a matriz requisito→entidade→restrição.
5. Devolver lacunas e novas solicitações de investigação.

## Sem integração automatizada

Se não houver ferramenta de comunicação direta com o Reader, produzir um arquivo JSON ou Markdown validável de handoff e pedir que o operador o transmita. Não afirmar que a mensagem foi enviada.
