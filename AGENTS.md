# Agentes Nestor no EPA

As definições locais ficam em `.agentes/`. Consulte `.agentes/registry/agents.json` para ver os agentes locais.

Os pacotes Nestor importados do ScoutOne ficam em `.agents/skills/` (`nestor-claws`, `nestor-docker`, `nestor-front-translator`, `nestor-schema`), `.codex/skills/nestor-reader/` e `.codex/agents/` (quatro adaptadores TOML correspondentes). Leia o `SKILL.md` do pacote pertinente antes de usá-lo. O `nestor-reader` é somente uma skill; não há adaptador TOML para ele na origem.

- Para trabalho na interface web (`05-WEB`) e nos fluxos de alunos e notas, siga `.agentes/nestor-web/AGENT.md` e o contexto em `.agentes/context/project-context.md`.
- Use `.agentes/nestor-sentinel/AGENT.md` somente quando a tarefa envolver suas capacidades declaradas no registro. Sua especialidade atual é Go, áudio e redes; ela não representa a stack principal do EPA.
- Os agentes são instruções e conhecimento versionados, não processos que precisam ser iniciados. Consulte apenas os arquivos relevantes para a tarefa.
- Preserve o núcleo importado do Nestor Sentinel. Registre fatos locais no contexto do projeto e novos aprendizados pela política de memória do pacote.

O objetivo atual informado pelo responsável é organizar os agentes para melhorar a interface web, começando pelos fluxos de alunos e notas. O recorte exato das mudanças visuais e funcionais será definido na contextualização.

O responsável relatou mais de 60 mil registros na base que não aparecem corretamente no frontend. Antes de alterar esse fluxo, investigue em modo somente leitura qual base, tabela, API e consulta fornecem esses números; trate a quantidade como relato até ser verificada. O Nestor Reader pode apoiar esse mapeamento. O Nestor Front Translator é voltado a migração entre frameworks, portanto use-o quando houver tarefa de migração.
