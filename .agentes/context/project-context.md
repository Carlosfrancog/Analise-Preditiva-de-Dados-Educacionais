# Contexto do EPA

## Estado observado no repositório

- O projeto EduNotas reúne um núcleo Python/SQLite em `01-CORE`, modelos e pipeline de ML em `02-ML`, interface desktop tkinter em `03-GUI`, API FastAPI em `04-API` e interface React/Vite/Tailwind em `05-WEB`.
- A interface web usa `05-WEB/src/App.jsx` para rotas e `05-WEB/src/api.js` para chamadas a `/api`. A API registra suas rotas em `04-API/main.py`.
- Os fluxos web de alunos e notas estão em `05-WEB/src/pages/Alunos.jsx`, `AlunoDetalhe.jsx` e `Notas.jsx`. Os endpoints relacionados estão em `04-API/routers/alunos.py` e `notas.py`; salas e matérias também participam desses fluxos.
- A área `research` contém uma pipeline experimental separada do código legado. Segundo `research/README.md`, seus dados são sintéticos e seus artefatos não representam resultados finais do artigo.
- `README.md` e notas antigas descrevem principalmente a aplicação desktop. Para o estado atual da interface web, confira o código e a documentação mais recente de `research`.

## Intenção confirmada pelo responsável

- Organizar os agentes Nestor para apoiar a melhoria da interface web.
- Priorizar os fluxos de alunos e notas.
- O responsável relatou que uma base teria mais de 60 mil registros e que o frontend não os carrega ou reflete corretamente. Ainda não foram confirmados a base, a tabela, a contagem nem o ponto do fluxo em que os dados divergem.

## Rastreio inicial da divergência (somente leitura)

- `01-CORE/cads.py` aponta a API operacional para `01-CORE/escola.db`; esse arquivo não está presente nesta cópia do workspace. Não foi possível conferir a contagem real.
- `GET /api/alunos` usa `cads.get_alunos()` e retorna linhas da tabela `alunos`, com filtro opcional de turma. A página `Alunos.jsx` chama esse endpoint.
- `GET /api/notas/turma/{sala_id}` retorna linhas da tabela `notas` para uma turma. A página `Notas.jsx` consulta esse endpoint após a escolha de turma e matéria.
- O dashboard conta `alunos` e `notas` separadamente. Uma contagem de registros de notas ou de ML não equivale ao número de alunos exibidos na lista. É preciso identificar a tabela e o ambiente da contagem relatada antes de atribuir a divergência ao frontend.

## Fluxos web identificados

- Em `Alunos.jsx`, a pessoa usuária consulta alunos, busca pelo nome, filtra por situação quando há uma turma selecionada, cadastra e remove alunos, e abre o detalhe de cada um.
- Em `AlunoDetalhe.jsx`, consulta notas e análises de um aluno e pode editar as notas por matéria.
- Em `Notas.jsx`, seleciona turma e matéria, visualiza notas da turma e edita/salva o conjunto em lote.
- Essas telas dependem das chamadas em `05-WEB/src/api.js` e das rotas de alunos/notas da API. A melhoria deve considerar os estados de carregamento, erro e salvamento em cada caminho.

## Ainda por definir

- Problemas específicos percebidos nesses fluxos e o resultado esperado.
- Referência visual ou critérios de aceitação para a interface.
