---
tags:
  - projeto
  - roadmap
  - tgi-codes
created: 2026-05-13
---

# Roadmap

[[MOC - TGI-CODES|← Voltar ao índice]]

---

## Concluído — 14/05/2026

> Ver [[Melhorias 2026-05-14]] para detalhes completos de cada item.

- [x] Corrigir lógica de status (Reprovado/Recuperação/Aprovado) em `NotasPage` e `RelatorioPage`
- [x] Dashboard com card "Em Risco (ML)" e barra de status dos modelos IA
- [x] Acentuação e lógica de cor do perfil em `gui_predicoes_improved.py`
- [x] Tratamento de erro quando modelos ML não estão treinados

---

## Curto Prazo (Esta Semana)

- [ ] Integrar modelos treinados com a GUI de predições (RF_M3 já integrado, testar com dados reais)
- [ ] Testar com dados reais de alunos
- [ ] Validar acurácia dos modelos no ambiente de produção
- [ ] Documentar processo de retreino para a equipe

---

## Médio Prazo (Este Mês)

- [ ] Deploy em produção (compilar com PyInstaller)
- [ ] Configurar monitoramento de performance dos modelos
- [ ] Retreinar mensalmente com novos dados
- [ ] Adicionar alertas automáticos para alunos em risco

---

## Longo Prazo

- [ ] **API REST** (Flask/FastAPI) para integração mobile
- [ ] **Dashboard Web** (Streamlit ou Dash) com visualizações interativas
- [ ] **GPU Support** com CuPy/RAPIDS para treino mais rápido
- [ ] **PostgreSQL** para escalabilidade além do SQLite
- [ ] **CI/CD** com GitHub Actions para testes automáticos
- [ ] **Modelos avançados**: XGBoost, Gradient Boosting, Stacking
- [ ] Incluir frequência do aluno como feature adicional

---

## Melhorias Técnicas

- [ ] Testes unitários com cobertura mínima de 80%
- [ ] Padrão MVC: separar lógica de UI de lógica de negócio
- [ ] `__init__.py` para cada módulo
- [ ] Testes de integração contra banco de dados real

---

## Links Relacionados

- [[Visão Geral]] — status atual do projeto
- [[Arquitetura do Sistema]] — como expandir o sistema
- [[Como Contribuir]] — padrões para novos módulos
