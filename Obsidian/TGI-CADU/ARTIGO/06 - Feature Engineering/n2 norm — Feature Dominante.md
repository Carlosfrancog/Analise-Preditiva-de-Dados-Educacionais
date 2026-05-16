---
tags: [artigo, feature-engineering, n2_norm, features, nota]
created: 2026-05-16
---

# n2_norm — Feature Dominante (32,3% de Importância)

[[INDEX - ARTIGO|← Índice]] | [[Visão Geral das 9 Features]] | [[Feature Importance Detalhada — M3]] | [[n1 n3 norm — Notas Bimestrais]]

> [!SUCCESS] A feature mais importante do M3 — domina o modelo com quase 1/3 da importância total

---

## 1. Definição

$$n2\_norm = \frac{N2}{10}$$

Normalização simples da nota do 2º bimestre para escala [0, 1].

---

## 2. Por Que N2 Domina com 32,3%?

Três fatores convergentes:

### Fator 1 — Ponto de Equilíbrio Temporal
N2 é o ponto temporal "de equilíbrio". N1 pode ser distorcida (alunos não se adaptaram ao ritmo, prova de sondagem). N3 pode ser distorcida (alunos estudam intensamente após N2 ruim). N2 representa o comportamento mais estável do aluno durante o ano.

### Fator 2 — Correlação com o Resultado Final
Com dados sintéticos, a correlação entre N2 e o resultado final (média ponderada = 0,2N1 + 0,25N2 + 0,25N3 + 0,30N4) é governada pelos pesos. N2 tem peso 0,25 — mesmo peso que N3. Mas N2 tem 3 bimestres restantes para "confirmar" o padrão, enquanto N3 tem apenas N4.

### Fator 3 — Correlação com slope_notas
slope_notas é calculado sobre todas as notas disponíveis. Em M3, inclui N1, N2, N3. A variação de N2 afeta diretamente o slope — o Random Forest distribui importância entre N2 e slope, mas N2 absorve a maior parte.

---

## 3. Implicações Práticas

**Para professores:**
A nota do 2º bimestre é o indicador mais crítico. Um aluno com N2 abaixo de 4,0 tem risco muito alto, independentemente de como foi N1.

**Para o sistema EWS:**
Após o lançamento de N2, o sistema deveria escalar automaticamente para M2 e disparar alertas mais precisos. O momento de maior urgência de alerta é justamente após N2.

**Para o calendário escolar:**
Uma intervenção pedagógica intensiva após N2 (e antes de N3) tem a janela mais longa e o modelo mais preciso. M2 com 92,5% de acurácia e 6 meses de antecedência é o cenário ideal.

---

## 4. Risco de Dependência Excessiva

32,3% é muita importância concentrada em uma única feature. Riscos:

1. **Prova atípica de N2:** se N2 foi uma prova muito fácil ou difícil, o modelo pode sistematicamente errar em determinadas turmas ou anos
2. **Estratégias de "gaming":** um aluno que entende o sistema poderia focar apenas em N2 para enganar o modelo (embora isso não seja um problema real em contexto escolar)
3. **Missing values:** se N2 não foi lançada para um aluno específico, o modelo cai para M1 — perda grande de precisão

---

## 5. Comparação com n3_norm

| Aspecto | n2_norm (32,3%) | n3_norm (8,7%) |
|---|---|---|
| Bimestre | 2º | 3º |
| Proximidade ao resultado | Longe | Próxima |
| Importância no modelo | Alta | Baixa |
| Estabilidade | Alta | Pode ser ruidosa |
| Tempo para intervir | 6 meses (via M2) | 3 meses (via M3) |

A menor importância de n3_norm é contraintuitiva mas plausível — N3 pode ter mais ruído (estudantes estudam mais para N3 em reação a N2 ruim, distorcendo o padrão real).

---

## Links

- [[Visão Geral das 9 Features]]
- [[Feature Importance Detalhada — M3]]
- [[M2 — Modelo Intermediário]]
- [[M3 — Modelo de Produção (Após N3)]]
- [[n1 n3 norm — Notas Bimestrais]]
- [[slope notas — Tendência Temporal]]
