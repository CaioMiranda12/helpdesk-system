# Sprint 03 — API de chamados

## Objetivo
Implementar criação, listagem, consulta, edição e transições de status com FastAPI, Pydantic e SQLAlchemy. Sem autenticação e sem frontend nesta sprint.

## Pré-requisitos
Sprint 02 concluída, PostgreSQL em execução, `.env` configurado e `alembic upgrade head` executado.

## Execução
No diretório `backend`, com o ambiente virtual ativo:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`.

## Contrato
- `POST /api/v1/tickets`: cria chamado, 201; campos obrigatórios `title` (5–120) e `description` (10–2000), `priority` opcional (`low`, `medium`, `high`), padrão `medium`.
- `GET /api/v1/tickets?limit=20&offset=0`: retorna array JSON ordenado por data de criação decrescente e UUID como desempate; `limit` 1–100 e `offset` >= 0.
- `GET /api/v1/tickets/{uuid}`: retorna chamado ou 404.
- `PATCH /api/v1/tickets/{uuid}`: altera `title`, `description` ou `priority`, ao menos um campo.
- `PATCH /api/v1/tickets/{uuid}/status`: recebe `{"status":"in_progress"}`; aceita apenas `open → in_progress`, `in_progress → resolved`, `resolved → in_progress`. Retorna 409 em transição inválida.
- 422 para dados inválidos, 404 para UUID inexistente.

## Teste manual sugerido
1. Crie um chamado pelo Swagger.
2. Copie o UUID retornado e consulte o chamado.
3. Liste os chamados e confirme a presença do novo registro.
4. Edite a prioridade e confirme a alteração.
5. Tente mudar `open` direto para `resolved` (409).
6. Mude para `in_progress` e depois `resolved` (200).
7. No Beekeeper execute `SELECT * FROM tickets ORDER BY created_at DESC;`.

## Commits por etapa
Faça commits após validar cada etapa:
1. `feat: add ticket validation schemas` — `backend/app/schemas/`
2. `feat: implement ticket CRUD and status rules` — `backend/app/services/`, `backend/app/api/`, `backend/app/main.py`
3. `test: cover ticket API endpoints and validation` — `backend/tests/test_ticket_api.py`
4. `docs: document ticket API and sprint 03` — `docs/`, `README.md`

Não inclua `.env` ou `.venv` no Git. Os testes da API usam SQLite em memória para serem rápidos e independentes do PostgreSQL; a validação manual pelo Swagger confirma o funcionamento com PostgreSQL local.
