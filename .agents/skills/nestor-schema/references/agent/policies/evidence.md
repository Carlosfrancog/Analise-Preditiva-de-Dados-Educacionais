# Política de evidências e proveniência

## Labels obrigatórias

- **FACT**: observado em arquivo/linha, manifesto ou consulta read-only efetivamente executada. Escopo limitado ao que a observação prova.
- **INFERENCE**: conclusão plausível derivada de fatos citados, ainda não diretamente demonstrada.
- **HYPOTHESIS**: explicação/solução a testar ou confirmar com o responsável.
- **UNKNOWN**: informação não disponível ou não verificável.

## Proveniência mínima

Para cada entidade/constraint/índice proposto: projeto/repositório, commit (se conhecido), caminho, linha/símbolo quando disponível, afirmação observada, status e consequência na modelagem. Evitar frases como “o banco possui” a partir de `Schema::create` quando não houve introspecção real.

## Evidências conflitantes

1. Diferenciar estado **do código** de estado **do banco** e de **documentação**.
2. Registrar divergências; não reconciliar silenciosamente.
3. Solicitar Reader para análise dirigida; inspecionar amostras necessárias.
4. Decidir somente com evidência ou aprovação do responsável.

Exemplo: `belongsTo(User::class)` prova a relação declarada no modelo, **não** que a FK existe fisicamente ou que todas as linhas são consistentes.
