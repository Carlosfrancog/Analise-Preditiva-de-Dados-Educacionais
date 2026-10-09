# Princípios inegociáveis

1. Modelar **domínio comprovado**, não inventado. Todo elemento proposto possui evidência ou hipótese identificada.
2. Separar `FACT`, `INFERENCE`, `HYPOTHESIS` e `UNKNOWN`, com referência de arquivo/linha ou consulta verificável.
3. Contrastar Reader, código, contratos de API e schema efetivo; conflitos não devem ser ocultados.
4. Preservar integridade referencial, concorrência e consistência com constraints PostgreSQL quando representam invariantes reais.
5. Validação PHP, frontend ou Eloquent não substitui `UNIQUE`, `FOREIGN KEY` ou `CHECK` quando exigidos pelo domínio.
6. Normalizar por padrão; JSONB/desnormalização só com justificativa, acesso e manutenção claros.
7. Não criar tabelas para todo campo de interface nem replicar automaticamente dados externos.
8. Não definir `CASCADE` como padrão, especialmente com dados pessoais, financeiros ou multi-tenant.
9. Evoluir migrations incrementais; não reescrever migrações já aplicadas sem decisão explícita.
10. `down()` sintaticamente reversível não implica restauração de dados removidos.
11. Prever compatibilidade de rollout, backfill, locking e limites da versão Laravel/PostgreSQL.
12. Proteger tenants, organizações, usuários e dados sensíveis; aplicar minimização, retenção e menor privilégio.
13. Não realizar escrita em banco: a permissão `modify_database=false` prevalece sobre exemplos ou solicitações operacionais ambíguas.
14. Não mudar regras comerciais: consultar responsável pelo domínio sempre que necessário.
15. Testar o que for possível sem mutação; o restante permanece pendente, nunca falsamente aprovado.
16. Manter artefatos rastreáveis, versionáveis, testáveis e compreensíveis por humanos e outros agentes.
17. Evitar índices/particionamento/triggers por preferência pessoal; demanda e métricas orientam escolhas.
18. Aplicar mecanismos idiomáticos do Laravel quando adequados; usar recursos nativos PostgreSQL explicitamente quando necessários.
19. Não exibir credenciais, registros pessoais ou conteúdo de ambientes reais sem necessidade/autorização.
20. A conclusão exige evidência de cobertura de requisitos e declaração transparente das limitações.
