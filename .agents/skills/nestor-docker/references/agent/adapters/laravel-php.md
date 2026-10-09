# Adapter: Laravel / PHP / Nginx

- Distinguir servidor HTTP/PHP-FPM, workers de fila, scheduler, Redis e banco de dados. Não combinar daemons sem justificativa.
- Validar extensões PHP, Composer lockfile, permissões de `storage` e `bootstrap/cache`, variáveis necessárias e entrypoints.
- Tratar cache de configuração/rotas/views com atenção a timing e secrets; não persistir segredos em imagens.
- Não executar automaticamente `php artisan migrate`, `db:wipe`, `queue:flush` ou limpeza de dados. Banco/schema não está autorizado.
- Proteger ambientes de prod de `APP_DEBUG=true`, portas do banco abertas e arquivos `.env` expostos.
- Validar worker shutdown/graceful process handling quando deployar.
