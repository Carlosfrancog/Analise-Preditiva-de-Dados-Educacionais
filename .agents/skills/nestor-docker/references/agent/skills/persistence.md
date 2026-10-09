# Skill: volumes, arquivos e dados persistentes

**Quando ativar:** permissão negada, dados desaparecendo, migração entre hosts, backup, bind mounts, storage cheio.

## Classificação

- `volume` nomeado: ciclo de vida distinto do container.
- `bind`: caminho do host compartilhado, sujeito a permissões, SELinux/AppArmor e diferenças WSL2/Windows.
- `tmpfs`: memória/armazenamento efêmero, dados não persistem após remoção.
- Camada gravável do container: não é repositório confiável de dados persistentes.

## Procedimento

1. Inventariar mounts sem publicar nomes sensíveis; identificar owner e criticidade.
2. Investigar permissões UID/GID, ACL, user namespaces e modos de montagem.
3. Verificar capacidade, inodes, crescimento e rotação de logs.
4. Distinguir backup de aplicação/banco consistente de cópia de diretórios ativa.
5. Planejar testes de restauração em **ambiente isolado** e com responsáveis; respeitar `modify_database=false`.
6. Exigir confirmação para exclusões, rotações destrutivas, substituição de mount e restore em serviço ativo.

## Critérios de aceite

Dados íntegros, retenção compreendida, permissão correta, procedimento de backup consistente e rollback claro. Jamais executar `down -v` como limpeza de rotina.
