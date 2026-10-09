# SKILL — Gerenciamento de segredos e credenciais

**Quando usar:** sempre incluída em auditoria completa; também sob demanda para revisão
pontual de repositório ou histórico Git.

## Procedimento

1. Usar scanner local de segredos no repositório autorizado (ver
   `../policies/tools-policy.md`) quando disponível; caso contrário, buscar
   manualmente por padrões: chaves de API, tokens, senhas, strings de conexão com
   credenciais embutidas, certificados privados.
2. Verificar arquivos de configuração versionados (`.env` commitado, `appsettings.json`,
   `application.yml`) em busca de segredos hardcoded.
3. Verificar histórico Git (se autorizado) para segredos removidos posteriormente mas
   ainda presentes no histórico de commits.
4. Verificar se variáveis de ambiente sensíveis estão sendo logadas acidentalmente
   (ex.: log de todo o objeto `process.env` ou de configuração completa na inicialização).
5. **Mascarar todo valor de segredo encontrado** antes de incluí-lo em qualquer saída —
   nunca reproduzir o segredo completo no relatório. Usar formato `****` + últimos 4
   caracteres quando necessário para rastreabilidade, e apenas se isso não permitir
   reconstrução do segredo.
6. Não validar credenciais encontradas contra provedores externos (ex.: tentar autenticar
   com a chave encontrada) — isso é teste ativo e está fora do escopo padrão.

## Critérios de aceitação de achado

- Arquivo e linha (ou commit, se no histórico) onde o segredo foi encontrado.
- Tipo de segredo identificado (chave de API, senha, certificado, etc.) sem reproduzir o
  valor.

## Saída

`../schemas/finding.schema.json`, com o campo de evidência contendo o segredo mascarado.
