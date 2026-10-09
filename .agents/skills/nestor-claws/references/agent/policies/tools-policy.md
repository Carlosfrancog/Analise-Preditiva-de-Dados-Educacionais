# FERRAMENTAS

Escolha a ferramenta pela informação necessária, não por preferência. Use apenas
ferramentas disponíveis no ambiente e dentro das permissões definidas em `permissions.md`.
Nenhuma ferramenta abaixo autoriza, por si só, teste ativo — a autorização específica
continua sendo exigida separadamente.

| Ferramenta                        | Uso autorizado                                                                 |
|------------------------------------|----------------------------------------------------------------------------------|
| Semgrep ou SAST local               | Somente se disponível, autorizada e configurada para não enviar código/segredos a terceiros. |
| Scanner local de segredos (código e histórico Git) | Somente no repositório autorizado; mascarar valores encontrados. |
| Análise de dependências local       | Quando disponível; consultas de rede e envio de manifests exigem autorização específica. |
| cURL                                 | Reproduções controladas, somente após autorização para testes ativos. |
| Postman CLI / Newman                 | Baterias de testes dinâmicos, somente autorizadas. |
| SQLMap                               | Somente em homologação isolada e no escopo autorizado — nunca em produção. |
| `psql` / `mysql`                     | Somente com conexão aprovada e credenciais de leitura; preferir metadados e evitar linhas com dados pessoais. |
| `jq` e utilitários de tratamento de dados via terminal | Filtrar, estruturar e extrair informação útil de respostas JSON complexas — sem restrição de autorização adicional. |

Não presumir que adapters, scanners externos ou integração com Sentinel estão instalados
ou funcionando.
