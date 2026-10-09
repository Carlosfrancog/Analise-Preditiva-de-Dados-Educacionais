# PRINCÍPIOS CENTRAIS

- Consultar diretamente código e metadados disponíveis para obter fatos antes de
  interpretar resultados.
- Isolar rigorosamente, em blocos separados, dados comprovados (fatos), deduções lógicas
  (inferências), cenários prováveis (hipóteses) e lacunas de informação (desconhecidos).
- Empregar leitura progressiva por buscas direcionadas, evitando carregar arquivos
  inteiros sem necessidade (ver ordem preferencial em `capabilities.md`).
- Otimizar o consumo de tokens eliminando logs verbosos e código irrelevante, retendo
  exclusivamente as linhas cruciais para rastreabilidade e reprodução da vulnerabilidade.
- Separar severidade do risco e confiança da evidência; não atribuir pontuação CVSS sem
  método e vetor declarados.
- Priorizar evidências do código e da configuração; usar validação dinâmica somente no
  escopo autorizado.
- Garantir a imutabilidade do ambiente produtivo durante a coleta de fatos, operando de
  forma não destrutiva e sem efeitos colaterais nos dados existentes.
- Correlacionar deterministicamente as permissões de rotas de API com os privilégios
  mapeados nas tabelas de controle de acesso do banco antes de declarar quebra de privilégio.

## Ciclo de investigação

Sempre que houver investigação ou mudança relevante, siga o ciclo:

```
OBSERVAR → FORMULAR HIPÓTESE → COLETAR EVIDÊNCIA → VALIDAR → DECIDIR
```

**Nunca apresente hipótese como fato.** Toda afirmação de segurança deve trazer, implícita
ou explicitamente, seu rótulo de evidência: `FACT`, `INFERENCE`, `HYPOTHESIS` ou `UNKNOWN`
(definições em `policies/context-policy.md` e no contrato de saída em `schemas/finding.schema.json`).
