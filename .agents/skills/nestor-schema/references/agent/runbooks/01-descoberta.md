# Runbook 01 — Descoberta do domínio e inventário

**Pré-condição:** acesso de leitura ao repositório ou inventário auditável do Reader.

1. Solicitar Reader ou coletar evidências de migrations, Models, requests, resources, services, routes, jobs e policies.
2. Capturar commit e caminhos. Usar `tools/inventory_laravel.py` somente como auxílio heurístico de busca.
3. Construir matriz `requisito → evidência → entidade → atributo/relação → status`.
4. Separar atributos persistidos, derivados, efêmeros, cacheados e externos.
5. Identificar ownership, cardinalidade, identificador, unicidade, ciclo de vida e exclusão.
6. Comparar com estado de banco read-only se disponível e autorizado; nunca inferir schema físico apenas de migration.
7. Listar contradições, lacunas, duplicidades e decisões abertas.

**Saída:** inventário rastreável, questões para Reader e limites de confiança.

**Parar se:** uma regra essencial for ambígua ou houver divergência não resolvida que tornaria a modelagem perigosa.
