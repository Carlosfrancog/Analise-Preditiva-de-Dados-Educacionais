# SKILL — Tratamento de erros e configuração de segurança

**Quando usar:** revisão de handlers de erro globais, configuração de CORS, headers de
segurança e rate limiting.

## Procedimento

1. Localizar o handler de erro global (middleware de erro, exception filter, handler de
   framework) e verificar se stack traces, versões de software ou estrutura interna do
   banco vazam na resposta em ambiente de produção.
2. Verificar código/funções de depuração esquecidos (`console.log` com dados
   confidenciais, `var_dump`, `print_r` em caminho de produção) — ver
   `../policies/code-policy.md`.
3. Avaliar configuração de CORS: origens permitidas, se há `*` combinado com
   `credentials: true` (combinação insegura), e se CORS está sendo usado como substituto
   de autenticação/autorização (nunca válido — ver `../policies/code-policy.md`).
4. Verificar headers de segurança presentes/ausentes: HSTS, `X-Content-Type-Options`,
   Content-Security-Policy, `X-Frame-Options`.
5. Verificar cookies: flags `HttpOnly`, `Secure`, `SameSite` (também coberto em
   `autenticacao-sessao-jwt.md` para o caso específico de sessão).
6. Verificar presença de rate limiting em rotas críticas (login, reset de senha, APIs
   públicas de alto custo). Testes de carga para validar o rate limiting exigem
   autorização específica.

## Critérios de aceitação de achado

- Trecho de configuração/código com arquivo e linha.
- Para vazamento de stack trace, incluir o payload/condição mínima que dispara o erro
  (de forma descritiva, não executada sem autorização).

## Saída

`../schemas/finding.schema.json`.
