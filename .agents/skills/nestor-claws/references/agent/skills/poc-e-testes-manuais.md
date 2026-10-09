# SKILL — Documentação de PoC e guias de teste manual

**Quando usar:** para toda falha classificada como `verified` (ver
`schemas/finding.schema.json`) ou quando a equipe de desenvolvimento precisa reproduzir o
problema.

## Procedimento

1. Formular a PoC como uma sequência determinística: pré-condições → ação → resultado
   esperado (vulnerável) → resultado esperado (corrigido).
2. Descrever a PoC de forma completa e reproduzível (requisição, payload, rota, método)
   **sem executá-la**, a menos que `run_active_tests` esteja autorizado para este alvo e
   ambiente — ver `../runbooks/autorizacao-testes-ativos.md`.
3. Se a PoC depender de estrutura de dados de uma rota ainda não mapeada, **interromper a
   geração da PoC** e reportar a lacuna imediatamente (ver `../policies/context-policy.md`),
   em vez de inventar o payload.
4. Para guias de teste manual, estruturar passo a passo com:
   - ferramenta/cliente a usar (ex.: cURL, Postman);
   - requisição exata (método, rota, headers relevantes, body);
   - comportamento esperado em um sistema seguro;
   - comportamento observado (quando a reprodução já foi autorizada e executada) ou "não
     executado — aguardando autorização" (quando não foi).
5. Ao final, indicar o passo seguro de verificação pós-correção: como confirmar que a
   correção elimina a falha sem reintroduzir regressão (ligado ao campo
   `remediation.safe_validation` do schema de achado).

## Saída

Seção "Reprodução controlada" do relatório (ver `../AGENT.md` → formato de resposta) e
campo `reproduction` de `../schemas/finding.schema.json`.
