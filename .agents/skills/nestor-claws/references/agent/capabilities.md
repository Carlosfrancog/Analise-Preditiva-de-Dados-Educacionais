# CAPACIDADES

## Escopo tecnológico

- JavaScript e TypeScript
- Node.js, NestJS, Express e Next.js
- Python, FastAPI e Flask
- PHP e Laravel
- Java, Go, Rust, .NET e Ruby on Rails
- React, Angular e Vue 3
- ORMs presentes no projeto
- PostgreSQL, MySQL, MariaDB e SQL Server
- MongoDB e Redis
- REST, GraphQL, gRPC e WebSockets
- OAuth 2.0, OpenID Connect, JWT, SAML e cookies de sessão
- Docker, Kubernetes, AWS e CI/CD

Somente tecnologias comprovadas pelos arquivos e manifests do projeto devem orientar cada
auditoria. Versões e tecnologias encontradas em manifests e arquivos do projeto prevalecem
sobre pressupostos.

## Pipeline de análise

1. Registrar repositório, revisão, ambiente, ativos permitidos, ferramentas autorizadas e
   exclusões do escopo (ver `schemas/scope.schema.json`).
2. Inventariar manifests, linguagens, rotas, autenticação, dados sensíveis, dependências e
   infraestrutura — sem executar código do projeto.
3. Mapear entradas, fronteiras de confiança, identidades, tenants e transições de privilégio.
4. Priorizar fluxos de risco e rastrear entrada, validação, autorização e destino, com
   arquivo e linha.
5. Correlacionar alertas de ferramentas com o código real e controles compensatórios antes
   de declarar uma falha.
6. Validar estaticamente os achados; executar testes ativos apenas em ambiente e escopo
   explicitamente autorizados.
7. Classificar separadamente: estado do achado, severidade, confiança, pré-condições,
   impacto e desconhecidos.
8. Entregar achados priorizados, correções sugeridas, passos seguros de verificação e
   cobertura da auditoria.

Aplique o pipeline progressivamente e somente até o nível necessário para responder à
pergunta em questão.

## Hierarquia de decisão (para correções propostas)

Ao propor uma correção, avalie nesta ordem — quando objetivos conflitarem, explicite o
trade-off em vez de escolher silenciosamente:

1. Priorizar correções que eliminem a vulnerabilidade sem alterar o comportamento esperado
   do negócio.
2. Assegurar confiabilidade: a correção não deve introduzir novas brechas, condições de
   corrida ou falhas de concorrência.
3. Favorecer manutenibilidade: seguir padrões de design, convenções de nomenclatura e
   arquitetura já existentes no projeto.
4. Avaliar impacto na performance: rejeitar soluções que degradem severamente tempo de
   resposta das APIs ou sobrecarreguem consultas ao banco.
5. Escolher soluções nativas do framework ou linguagem antes de recomendar novas dependências.
6. Adequar a complexidade do código de remediação ao nível de legibilidade do time,
   evitando refatorações excessivas ou desnecessárias para o escopo do problema.

## Economia de contexto

Prefira fatos extraídos deterministicamente. Ordem preferencial de leitura:

```
METADADOS → MANIFESTS → ESTRUTURA → SÍMBOLOS → RELAÇÕES → FLUXOS → TRECHOS RELEVANTES → ARQUIVO COMPLETO
```

Não carregue código bruto inteiro quando uma representação estrutural responder à pergunta.
