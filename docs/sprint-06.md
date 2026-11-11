# Sprint 06 — Pesquisa e filtros de chamados

## Objetivo
Permitir pesquisa por título e filtros por status e prioridade, aplicados no PostgreSQL antes da paginação.

## Contrato
`GET /api/v1/tickets?search=relatório&status=open&priority=high&limit=11&offset=0`

- `search`: opcional, até 120 caracteres, sem distinção de maiúsculas/minúsculas; espaços nas extremidades são ignorados; `%` e `_` são tratados como texto literal.
- `status`: opcional, `open`, `in_progress` ou `resolved`.
- `priority`: opcional, `low`, `medium` ou `high`.
- Filtros combinam por **E** (AND).
- `limit`: 1–100; `offset`: 0 ou maior.
- Resposta: array de chamados (mesmo contrato anterior); filtros inválidos retornam 422.
- A busca não considera a descrição, apenas o título.

## Implementação
- Router FastAPI recebe e valida os query params.
- Service monta a consulta SQLAlchemy usando `ilike` e condições `where`.
- O frontend mantém filtros e página na URL, para permitir compartilhamento e recarregamento.
- Ao alterar filtros, a paginação volta para a primeira página.
- A listagem pede 11 registros e exibe 10 para identificar se existe uma próxima página.
- Nenhuma migration é necessária: o schema do banco permanece inalterado.

## Execução
1. PostgreSQL em execução.
2. `cd backend && python -m pytest -q`.
3. `python -m uvicorn app.main:app --reload`.
4. Em outro terminal: `cd frontend && npm install && npm run typecheck && npm run build && npm run dev`.
5. Abra `http://localhost:5173`, teste cada filtro e combinações; verifique o Swagger em `/docs`.

## Cenários de aceite
- Pesquisar `relatório` encontra `RELATÓRIO` mesmo em outras páginas.
- `status=in_progress&priority=high` retorna somente chamados correspondentes.
- Um filtro sem resultados mostra mensagem e opção de limpar.
- Ao mudar o filtro, a página volta para 1.
- Filtros persistem na URL; atualizar a página mantém a seleção.
- Com 11 resultados filtrados, a segunda página fica disponível; com 10, não.
- Erro de conexão continua oferecendo `Tentar novamente`.

## Commits (branch master)
1. `feat: add ticket search and filters to API` — `backend/app/api/v1/tickets.py`, `backend/app/services/tickets.py`.
2. `test: cover ticket search and combined filters` — `backend/tests/test_ticket_filters.py`.
3. `feat: add search and filters to ticket list` — `frontend/src/pages/TicketList.tsx`, `frontend/src/services/api.ts`, `frontend/src/styles.css`.
4. `docs: document sprint 06 ticket filtering` — `docs/sprint-06.md`, `docs/api.md`, `README.md`.

Faça `git push origin master` após cada commit e somente depois de validar a respectiva etapa.
