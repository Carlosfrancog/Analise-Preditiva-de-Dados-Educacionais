# Exemplo de resposta — incidente de reinícios (fictício)

**Objetivo:** diagnosticar reinícios do `api` sem alterar o ambiente.  
**Ambiente:** homologação, contexto pendente de confirmação.  
**Estado:** `NOT VERIFIED`.

## Diagnóstico

- `[UNKNOWN]` Não foi coletado status de containers nem histórico de OOM.
- `[HYPOTHESIS]` O processo pode estar sendo finalizado por limite de memória ou falha de inicialização. Ainda não há evidência para distinguir.

## Próximas evidências (somente leitura, com escopo)

1. Confirmar contexto Docker e projeto Compose.
2. Consultar estado, exit codes/restart count e `OOMKilled` de forma seletiva, sem dumping de `docker inspect` completo.
3. Consultar logs da janela do incidente, com minimização e redação de credenciais.
4. Correlacionar com memória/cpu e mudanças recentes de release.

## Alterações realizadas

Nenhuma. Uma investigação preliminar não autoriza restart, alteração de volume ou nova implantação.

## Validação

Nenhum teste executado; as verificações propostas dependem de acesso e de autorização de leitura ao ambiente específico.

## Risco e autorização

Ausência de causa raiz confirmada; reiniciar pode restaurar serviço temporariamente e apagar evidências. Solicitar confirmação do contexto, sem mudar serviços.
