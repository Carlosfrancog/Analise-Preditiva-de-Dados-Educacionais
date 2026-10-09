# Nestor Docker — pacote modular de agente

**Versão:** 1.0.0  
**Perfil:** coder  
**Idioma:** pt-BR  
**Modelo:** agnóstico de LLM (ChatGPT, Codex, Claude, Gemini e afins)

## Uso

1. Forneça `AGENT.md` à LLM como instrução principal.
2. Dê acesso aos documentos de `policies/` sempre que houver operações no ambiente.
3. Carregue **somente as skills e runbooks relevantes** para o problema; evite carregar todos sem necessidade.
4. Informe caminho do repositório, ambiente, contexto Docker, objetivo, restrições e se está autorizado apenas analisar ou também alterar.
5. Para execução em CLI, disponibilize terminal com as **permissões mínimas necessárias**. O prompt por si só não instala ferramentas, não concede acesso, nem implementa controle técnico de autorização.
6. Use `schemas/` para integração máquina-máquina; `examples/` contém modelos ilustrativos, não fatos de um ambiente real.

## Exemplos de solicitação

- `Analise os Dockerfiles e o compose.yaml deste repositório, sem alterar nada. Entregue inventário de risco, evidências e plano de otimização.`
- `Investigue a reinicialização do serviço web no ambiente de homologação; apenas comandos de leitura até eu aprovar a mudança.`
- `Atualize o Dockerfile Go para build multi-stage; mantenha compatibilidade com CGO e faça o build de validação em ambiente isolado.`

## Arquitetura do pacote

```
AGENT.md                  instrução principal
identity.md               identidade, limites e perfis
principles.md             decisões e prioridades
capabilities.md           catálogo de competências sem prometer ferramentas
policies/                 autorização, proteção de dados e evidências
skills/                   conhecimento especializado por domínio
runbooks/                 procedimentos de investigação e operação
adapters/                 diferenças por stack/ambiente
schemas/                  JSON Schema de entrada, plano, inventário, relatório e handoff
examples/                 entradas e saídas fictícias para referência
tools/                    utilitário de inventário determinístico e não mutável
tests/                    verificações de integridade do pacote
CHANGELOG.md              histórico e correções de origem do Forge
```

## Verificar o pacote

```bash
python3 tests/verify_package.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tools/docker_inventory.py --help
```

Dependências do utilitário: biblioteca padrão Python. **Nenhum comando de mutação é executado por ele.** Não utiliza Docker automaticamente: exige `--live --project NOME --expected-context CONTEXTO`. `--offline` produz apenas inventário documental de caminhos fornecidos.

Exemplo opcional de inventário local (somente metadados e com alvo explícito):

```bash
python3 tools/docker_inventory.py --offline . --environment dev
# Antes de usar --live, verificar o contexto com docker context show.
python3 tools/docker_inventory.py --live --project app-dev --expected-context default --environment dev
```

## Observações sobre produção

- Este pacote é **uma especificação operacional e artefatos de suporte**, não substitui IAM/RBAC, ACLs, secrets manager, políticas de rede nem supervisão humana.
- Logs, `docker inspect`, `docker compose config` completo e `.env` podem conter credenciais; não colar essas saídas indiscriminadamente em uma LLM.
- A aplicação das permissões requer enforcement pela ferramenta/orquestrador que executa comandos.
- Comandos exemplificativos são sugestões condicionais, nunca autorização para executá-los.
