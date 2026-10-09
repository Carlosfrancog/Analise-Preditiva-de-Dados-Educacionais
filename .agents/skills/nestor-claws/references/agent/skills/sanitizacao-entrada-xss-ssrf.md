# SKILL — Sanitização de entrada: XSS, SSRF e injeção de comandos

**Quando usar:** formulários, campos de texto livre renderizados posteriormente,
funcionalidades que fazem requisição HTTP a partir de URL fornecida pelo usuário, ou
qualquer chamada a shell/processo externo com argumento do usuário.

## Procedimento

1. **XSS:** localizar pontos de renderização de conteúdo gerado pelo usuário (templates,
   `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, resposta de API consumida sem escape
   no frontend). Verificar se o framework de template aplica autoescape por padrão e se
   foi desativado em algum ponto.
2. **SSRF:** localizar funcionalidades que fazem requisição de saída (fetch/HTTP client)
   para uma URL/host fornecido total ou parcialmente pelo usuário (ex.: importação de
   imagem por URL, webhook de teste, proxy de conteúdo). Verificar allowlist de
   host/protocolo, bloqueio de IPs internos/metadados de nuvem (ex.: `169.254.169.254`) e
   validação de redirecionamento.
3. **Injeção de comando:** localizar chamadas a `exec`/`spawn`/`subprocess`/`system` que
   incorporam entrada do usuário no comando ou em seus argumentos sem uso de API que separe
   argumentos de shell.
4. Verificar validação e sanitização de dados estruturados recebidos no corpo da
   requisição: checagem rigorosa de tipos, rejeição de propriedades extras (Mass
   Assignment) e aderência a schema declarado — ver `../policies/code-policy.md`.
5. Não supor middleware de sanitização global que não esteja explicitamente visível no
   escopo analisado — ver `../policies/context-policy.md`.

## Critérios de aceitação de achado

- Ponto de entrada e ponto de uso sensível (sink) documentados com arquivo e linha.
- Para SSRF, citar se há ou não allowlist/denylist de destino e seu mecanismo exato.
- Para injeção de comando, citar a API usada (string de shell vs. array de argumentos).

## Saída

`../schemas/finding.schema.json`. Classifique XSS como refletido, armazenado ou DOM-based
no campo `title`/`root_cause` conforme aplicável.
