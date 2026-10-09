# Histórico

## 1.0.0 — 2026-10-09

- Criado pacote modular agnóstico de LLM para Nestor Docker.
- Mantidos identidade, perfil `coder`, missão, especialidades e seis permissões do Nestor Forge.
- Implementado pipeline ausente de investigação, decisão, execução e validação.
- Substituído contrato de saída herdado do Nestor Front Translator por campos de infraestrutura, incluindo contexto Docker, impacto, persistência e rollback.
- Definidas regras concretas de domínio, execução, segurança, análise e testes antes ausentes.
- Resolvida a tensão `token_economy: false` versus comportamento econômico: cobertura completa, resposta proporcional.
- Adicionados schema versionados, runbooks, adapters, exemplos não reais e ferramenta determinística de inventário.
- Restrições preservadas: sem alteração autônoma de regras de negócio ou banco/schema; operações destrutivas/produção exigem autorização específica.
