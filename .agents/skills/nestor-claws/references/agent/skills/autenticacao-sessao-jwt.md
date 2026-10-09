# SKILL — Autenticação, sessão e tokens (JWT)

**Quando usar:** o projeto implementa login, sessão, emissão/validação de JWT, OAuth2/OIDC
ou SAML.

## Procedimento

1. Identificar o mecanismo de autenticação em uso (sessão de servidor + cookie, JWT
   stateless, OAuth2/OIDC delegado, SAML).
2. Para armazenamento de senha: verificar algoritmo de hash (Argon2/bcrypt esperado),
   ausência de texto plano, e presença/ausência de salt gerenciado pela própria lib.
3. Para JWT, avaliar — **sem exigir assinatura assimétrica por padrão**:
   - algoritmo declarado (`alg`) e se o verificador aceita `alg: none` ou permite
     confusão de algoritmo (ex.: aceitar HS256 quando esperava RS256 com a chave pública
     como segredo);
   - expiração (`exp`) presente e validada no lado do servidor;
   - emissor (`iss`) e audiência (`aud`) validados quando aplicável;
   - mecanismo de revogação/rotação (blacklist, versão de token, refresh token rotation);
   - distribuição/armazenamento da chave de assinatura.
4. Para sessão baseada em cookie: verificar flags `HttpOnly`, `Secure`, `SameSite`,
   regeneração do identificador de sessão após login (mitigação de fixação de sessão), e
   geração do identificador com fonte criptograficamente segura (ver
   `../policies/code-policy.md`).
5. Verificar geração de tokens de redefinição de senha: entropia, expiração de uso único,
   e se o token é invalidado após uso.
6. Checar tempo de expiração e janela de reautenticação para operações sensíveis.

## Critérios de aceitação de achado

- Trecho de código/configuração mostrando o mecanismo avaliado, com arquivo e linha.
- Para "algoritmo fraco" ou "ausência de expiração": citar o valor exato configurado.
- Classificar como `HYPOTHESIS` qualquer dependência de biblioteca externa cujo
  comportamento de validação não foi inspecionado diretamente.

## Saída

`../schemas/finding.schema.json`. Severidade deve considerar separadamente o algoritmo em
si e o contexto de distribuição de chaves (não pontuar CVSS sem vetor declarado — ver
`../principles.md`).
