# SKILL — Análise estática de código (SAST)

**Quando usar:** início de qualquer auditoria, ou quando o pedido for genérico ("revise a
segurança deste repositório/módulo").

## Procedimento

1. Inventariar a árvore do projeto por metadados antes de ler arquivos (ver ordem de
   leitura em `../capabilities.md`): manifests (`package.json`, `composer.json`,
   `requirements.txt`, `go.mod`, `pom.xml`, `*.csproj`, `Gemfile`), linguagens
   predominantes, frameworks declarados.
2. Mapear pontos de entrada: controladores/rotas HTTP, handlers de fila, CLIs expostas,
   webhooks.
3. Para cada ponto de entrada, rastrear o caminho de dados: entrada → validação →
   transformação → uso sensível (query, comando de sistema, template, resposta).
4. Procurar padrões estruturais recorrentes de risco:
   - uso de `eval`, `exec`, `child_process`/`subprocess` com entrada não sanitizada;
   - concatenação de strings em queries SQL/NoSQL;
   - desserialização de dados do usuário (`pickle`, `unserialize`, `ObjectInputStream`,
     `yaml.load` sem `safe_load`, etc.);
   - uso de funções inseguras de template (`render` com `autoescape` desativado);
   - geração de identificadores sensíveis com gerador pseudoaleatório fraco.
5. Se houver saída de ferramenta SAST (Semgrep ou outra, ver `../policies/tools-policy.md`),
   correlacionar cada alerta com o código real antes de aceitar — nunca repassar alerta de
   ferramenta como achado verificado sem essa correlação.
6. Classificar cada candidato como alcançável (caminho de dados completo, sem barreira de
   validação/autorização) ou não alcançável (documentar o controle compensatório
   encontrado).

## Critérios de aceitação de achado

- Caminho completo da entrada até o uso sensível está documentado com arquivo e linha.
- Ausência (ou insuficiência) de validação/sanitização está demonstrada, não presumida.
- Rótulo de evidência atribuído conforme `../policies/context-policy.md`.

## Saída

Produza achados no formato de `../schemas/finding.schema.json`, um por vulnerabilidade
candidata ou confirmada. Não agregue vulnerabilidades distintas em um único achado.
