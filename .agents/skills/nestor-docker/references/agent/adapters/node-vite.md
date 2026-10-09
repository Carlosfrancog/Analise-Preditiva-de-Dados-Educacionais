# Adapter: Node / Vite / frontend SSR

- Respeitar lockfile existente e versão Node; preferir `npm ci`/equivalente para builds previsíveis.
- Distinguir Vite dev server, build estático, SSR Node e assets publicados; não servir dev server como produção automaticamente.
- Variáveis `VITE_*` embutidas no bundle são públicas; **não** colocar segredos nelas.
- Confirmar host bind apropriado quando dev server deve ser acessível de fora do container.
- Otimizar cache de dependências sem copiar `node_modules` local ou credenciais para imagem.
- Validar rotas, assets e URLs de base/reverse proxy.
