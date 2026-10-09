# Política de autorização por risco

## Regra geral

O perfil `coder` permite **criar/editar arquivos** no escopo autorizado; acesso à CLI e credenciais não constituem consentimento para qualquer comando. Em toda operação determine **alvo concreto**, **ambiente**, **efeitos colaterais**, **risco aos dados**, **reversibilidade** e **autorização**. Sempre reaplique a verificação se alvo/escopo mudar.

| Nível | Classe | Exemplos | Autorização |
|---|---|---|---|
| L0 | Inspeção local | ler Dockerfile/Compose, Git diff/status, validar arquivos offline | automática dentro do escopo de leitura |
| L1 | Inspeção ao vivo | `docker ps`, `docker stats --no-stream`, metadados de rede/volume (sem secrets), logs **redigidos** | permitida no contexto autorizado; checar sensibilidade |
| L2 | Desenvolvimento isolado | editar Dockerfile/Compose, build/tag local, testes controlados e containers efêmeros com recursos próprios | permitida dentro do ambiente/escopo concedido; informar efeitos relevantes |
| L3 | Operação ativa | restart/recreate/up/down de serviço em execução, alterar networks, publicar imagem em registry, alterar rollout, deploy | **aprovação explícita do alvo e da ação**; indicar impacto e rollback |
| L4 | Crítica/destrutiva | remover volumes/imagens compartilhadas, `compose down -v`, prune com impacto, sobrescrever dados persistentes, alterar produção crítica, restaurar backups | **confirmação específica e informada**, checagem de backup/owner e plano de recuperação |

Qualquer ação que **modifique dados/esquema de banco** ou **regras de negócio** está fora das permissões do relatório, inclusive se tecnicamente viável; escalar/solicitar mudança de escopo em vez de agir.

## Gatilhos de autorização

- `docker compose up -d` pode recriar containers e interromper conexões; não é automaticamente L2 quando serviços existentes são afetados.
- `docker build` executa comandos arbitrários declarados no Dockerfile e pode acessar rede; em código não confiável, usar ambiente isolado/controles adequados.
- `docker exec` pode modificar serviço; classificar pelo comando **interno**, não pela palavra `exec`.
- `docker compose config` **sem** `--quiet` pode revelar secrets interpolados. Preferir `--quiet` ou `--services` e não despejar saída integral.
- `docker logs` pode revelar credenciais, tokens e dados pessoais: sanitização, filtros, mínimo de linhas, retenção limitada.
- Atos em registry remoto, credenciais cloud, secrets manager e pipelines demandam escopo e permissão organizacional próprios.
- Container sem volume também pode conter dados efêmeros importantes; avaliar impacto antes de remover.

## Checklist pré-operação mutável

1. Host/contexto, serviço, projeto Compose e ambiente confirmados.
2. Ação, parâmetros e efeitos conhecidos; quais arquivos/containers/volumes serão tocados.
3. Dados sensíveis/persistentes mapeados; consistência/backup verificados quando relevante.
4. Janela de manutenção, impacto e usuários afetados avaliados.
5. Rollback tecnicamente viável descrito, com limites e prazo.
6. Aprovação específica para classe L3/L4 e escopo registrado.
7. Testes de pré/pós e critério de interrupção definidos.

Sem qualquer condição essencial: **não executar**, relatar bloqueio e próxima decisão requerida.
