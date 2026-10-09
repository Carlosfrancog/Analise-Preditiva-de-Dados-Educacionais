# Evidência, diagnóstico e honestidade operacional

## Etiquetas

- `FACT`: saída observada, trecho de configuração ou comportamento reproduzido, com origem e contexto.
- `INFERENCE`: conclusão fundamentada por fatos, sem prova direta.
- `HYPOTHESIS`: possível explicação que exige teste discriminante.
- `UNKNOWN`: não coletado, inconclusivo ou indisponível.

## Padrão de evidência

Registrar quando útil: host/contexto **não sensível**, ambiente, serviço, versão, timestamp, comando de leitura/consulta e resultado redigido. Evitar transcrever logs enormes: trecho mínimo suficiente e referência temporal. Métricas precisam de janela e unidade (CPU%, bytes, p95 etc.). Um único pico não comprova vazamento.

A causa raiz só pode ser denominada **confirmada** quando evidência e reprodução/contraprova suficientes estiverem disponíveis. Caso contrário usar **provável** ou **não determinada**. Ausência de logs não significa ausência de falha. Exit code 137 sugere SIGKILL/OOM, mas **não prova** OOM sem `OOMKilled`, eventos e métricas coerentes. `unhealthy` não significa necessariamente processo parado.

## Resultado honesto

Diferenciar `passed`, `failed`, `blocked`, `not_run` e `inconclusive` em testes. Distinguir implementação escrita de execução em runtime. Não inventar paths, comando executado, CI aprovado, tempo de build, queda de uso ou saúde.

## Economia de contexto

Ler progressivamente: manifestos → topologia → status → eventos/logs/métricas relevantes → trechos de arquivo/código necessários. Pedir texto bruto grande apenas quando justificável. Resumos operacionais permanecem concisos, sem cortar achados críticos.
