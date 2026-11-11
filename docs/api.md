# API v1 — implementada na Sprint 03

## Contrato
- `POST /api/v1/tickets`: cria chamado, 201; campos obrigatórios `title` (5–120) e `description` (10–2000), `priority` opcional (`low`, `medium`, `high`), padrão `medium`.
- `GET /api/v1/tickets?limit=20&offset=0`: retorna array JSON ordenado por data de criação decrescente e UUID como desempate; `limit` 1–100 e `offset` >= 0.
- `GET /api/v1/tickets/{uuid}`: retorna chamado ou 404.
- `PATCH /api/v1/tickets/{uuid}`: altera `title`, `description` ou `priority`, ao menos um campo.
- `PATCH /api/v1/tickets/{uuid}/status`: recebe `{"status":"in_progress"}`; aceita apenas `open → in_progress`, `in_progress → resolved`, `resolved → in_progress`. Retorna 409 em transição inválida.
- 422 para dados inválidos, 404 para UUID inexistente.

