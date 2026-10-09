# POLÍTICA DE CÓDIGO

Este agente é prioritariamente de análise. Pode propor correções e exemplos mínimos, mas
**não deve alterar arquivos sem autorização** (ver `permissions.md`).

## Regras para análise de código

- Validar o tratamento de exceções para impedir vazamento de stack traces ou detalhes de
  infraestrutura em produção.
- Analisar se middlewares de autenticação e autorização são declarados explicitamente em
  nível de rota ou controlador, impedindo rotas "esquecidas" sem proteção.
- Verificar se o encadeamento de promises/funções assíncronas tem tratamento adequado de
  erros, evitando falhas que resultem em negação de serviço (DoS) local.
- Rastrear código comentado ou funções de depuração (ex.: `console.log` com dados
  confidenciais, `var_dump`) que possam expor informações na resposta da aplicação.
- Certificar que a geração de strings aleatórias para sessão, tokens de redefinição de
  senha ou hashes usa bibliotecas criptograficamente seguras (ex.: módulo `crypto` nativo),
  nunca geradores pseudoaleatórios simples (ex.: `Math.random`).
- Auditar validação e sanitização de dados estruturados recebidos no corpo da requisição
  (ex.: JSON): checagem rigorosa de tipos, propriedades extras indesejadas (Mass
  Assignment) e esquemas de dados.
- Inspecionar desserialização insegura de objetos a partir de entradas do usuário,
  mitigando risco de execução remota de código (RCE).
- Distinguir alertas candidatos de caminhos alcançáveis e documentar controles
  compensatórios ou evidência negativa.
- Garantir que todas as consultas ao banco construídas dinamicamente usem exclusivamente
  mecanismos de escape ou bind parameters fornecidos pelo framework/ORM.

## Regras de domínio

- Verificar se senhas usam algoritmos adequados (Argon2, bcrypt) e nunca são armazenadas
  em texto plano.
- Avaliar expiração, assinatura e revogação dos tokens de autenticação conforme o modelo
  adotado pelo projeto.
- Não exigir assinatura assimétrica para todo JWT; avaliar algoritmo, distribuição de
  chaves, emissor, audiência e rotação conforme o contexto.
- Auditar tabelas de logs e histórico do banco para garantir que dados sensíveis (PII,
  pagamento, senhas) não fiquem armazenados de forma legível.
- Revisar isolamento multi-tenant para identificar exposição de dados entre
  empresas/usuários (IDOR/BOLA).
- Verificar middlewares globais, políticas em serviços e controles do banco antes de
  afirmar ausência de autorização em uma rota.
- Rastrear uso de queries brutas e concatenação de strings em todo o backend, exigindo
  parametrização total ou uso seguro do ORM para prevenir injeção SQL.
- **Não declarar SQL Injection apenas pela existência de SQL bruto**; rastrear entrada
  controlável até a execução e verificar parametrização.
- Revisar limites e validações de upload: tipo MIME, extensão real, tamanho e restrição de
  execução no servidor.
- Analisar políticas de CORS, headers de segurança (HSTS, X-Content-Type-Options, CSP) e
  cookies das rotas web, para mitigar personificação ou roubo de sessão.
- **Não tratar CORS como substituto de autenticação ou autorização.**
- Revisar mecanismos de rate limiting nas rotas críticas; testes de carga exigem
  autorização específica (ver `permissions.md`).
