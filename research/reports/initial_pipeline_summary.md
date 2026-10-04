# Primeiro experimento da pipeline de pesquisa

> Este relatório é uma verificação técnica inicial. Ele não deve ser
> transcrito como resultado final do Full Paper antes do congelamento do
> protocolo, da calibração e da revisão do orientador.

## Execução

- Registros sintéticos: **62.400**
- Registros legados auditados: **15.613**
- Resultados gerados: **18**
- Seed: **20261004**
- Fonte sintética: dados gerados localmente, sem estudantes reais.

## Observação sobre o legado

O dataset legado possui `status` como alvo: status_encoded, status_label.
Features suspeitas para auditoria: n4_norm, media_pond_norm.
A presença de `n4_norm` e `media_pond_norm` impede usar as métricas antigas como resultado oficial sem reconstrução temporal.

## Próxima validação

1. revisar os rótulos e as faixas de aprovação;
2. adicionar calibração e validação cruzada agrupada;
3. instalar e avaliar o candidato XGBoost ou CatBoost;
4. integrar o snapshot versionado à API;
5. repetir o experimento com o protocolo aprovado para o artigo.
