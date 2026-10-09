# Política de alterações no código

1. Ler `git status`, arquivos envolvidos, histórico de migrations e padrões locais.
2. Preservar alterações não relacionadas; não aplicar formatadores no repositório inteiro.
3. Não editar migrations já usadas em ambientes compartilhados por padrão; criar novas migrations incrementais.
4. Converter requisitos comprovados em comentários/constraints com nomes úteis e rastreáveis.
5. Separar alteração de schema de população de dados quando reduz risco.
6. Não adicionar triggers, enum nativo, extensão, particionamento ou JSONB sem justificativa de manutenção.
7. Analisar necessidade de índices das FKs e combinações de consultas, mas não indexar todas as colunas automaticamente.
8. Criar testes que detectem violação de invariantes, sem executá-los se mutarem banco.
9. Revisar diff, registrar incompatibilidades e produzir plano de rollout.
10. Não executar commits, reset, rebase, limpeza ou alteração de branch sem autorização.
