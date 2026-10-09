# Política de dados pessoais, multi-tenant e segredos

- Identificar quem pode ler/escrever cada registro: organização, usuário, escopo, policy e origem externa.
- Modelar constraints que impeçam associação cruzada entre tenants quando justificadas; não confiar apenas em filtros de frontend.
- Diferenciar autorização (`Policy/Gate`) de integridade (`FK/CHECK/UNIQUE`) e isolamento físico/lógico.
- Minimizar PII, retenção e cópias; nunca puxar dados pessoais reais para exemplos.
- Não derivar política LGPD ou prazo de retenção sem requisito jurídico/operacional confirmado.
- Evitar tokens e senhas em texto puro, migrations, factories, logs e relatórios.
- Em exemplos, usar identificadores e dados totalmente fictícios.
- PostgreSQL RLS, roles e schemas distintos são alternativas específicas de arquitetura, não obrigatoriedades universais.
- Para jobs e sincronizações externas, considerar idempotência, duplicação e isolamento de tenants.
