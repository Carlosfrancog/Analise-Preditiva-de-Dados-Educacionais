# Missão inicial opcional — Scout-One / Livt

> Contexto informado pelo usuário em conversa anterior, **não verificado neste pacote**. Não constitui inventário do banco nem proposta de novas tabelas.

## Objetivo

Analisar o sistema Scout-One e propor a modelagem PostgreSQL e as integrações Laravel necessárias para converter os fluxos hoje simulados ou locais em persistência confiável dentro de `Livt`, reutilizando estruturas já existentes. Trabalhar em conjunto com Nestor Reader e respeitar `modify_database=false`.

## Pontos de partida informados

- `Scout-One-v51`: aplicação de origem React/Next/Vinext, com módulos de atletas, oportunidades, empresas, profissionais, clubes, mercados, administração e Player 360.
- `Scout-One-Vue`: migração frontend parcial, com componentes que ainda dependem de estado local ou dados demonstrativos.
- `Livt`: aplicação Laravel/Inertia/Vue de destino.
- Foi relatado um contrato frontend inicial em `resources/js/types/scout-one.ts`, mas o backend efetivo e o schema de produção **não foram verificados aqui**.

## Ordem da investigação

1. Reader: mapear migrations/modelos/policies/serviços reais de `Livt` e os contratos nas aplicações Scout-One.
2. Schema: classificar dados persistentes versus externos/derivados/efêmeros; não replicar indiscriminadamente dados SportsBase ou shards de atletas.
3. Reader: encontrar criação, edição, validação, ownership e consultas reais em cada módulo; devolver evidências por arquivo/linha/commit.
4. Schema: propor matriz entidade/atributo/constraint com status FACT/INFERENCE/HYPOTHESIS/UNKNOWN.
5. Validar com responsável: escopo de organização, regras de acesso, workflow comercial, retenção, catálogos externos e cardinalidades incertas.
6. Somente depois gerar migrations incrementais, Eloquent, Form Requests e testes relacionados. Não executar migrations.

## Critérios de aceite

- Nenhuma tabela nova sem evidência ou hipótese aprovada.
- Nenhuma decisão de autorização/tenant baseada apenas no frontend.
- Aproveitamento de schema e migrations já existentes.
- Rastreabilidade até origem e contratos de dados reais.
- Testes classificados corretamente; execução em banco permanece bloqueada até delegação autorizada.

## Pedido de handoff ao Reader

"Inventarie os modelos, migrations, controllers, requests, resources, jobs, policies e consultas usados pelos módulos Scout-One em Livt. Compare os contratos existentes com os fluxos React/Vue relevantes. Indique caminhos, linhas, commit, dados atualmente persistidos versus simulados e perguntas sem resposta. Não proponha schema físico nem modifique arquivos." 
