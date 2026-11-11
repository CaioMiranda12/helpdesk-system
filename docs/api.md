# API v1 — implementada na Sprint 03

## Contrato
- `POST /api/v1/tickets`: cria chamado, 201; campos obrigatórios `title` (5–120) e `description` (10–2000), `priority` opcional (`low`, `medium`, `high`), padrão `medium`.
- `GET /api/v1/tickets?limit=20&offset=0`: retorna array JSON ordenado por data de criação decrescente e UUID como desempate; `limit` 1–100 e `offset` >= 0.
- `GET /api/v1/tickets/{uuid}`: retorna chamado ou 404.
- `PATCH /api/v1/tickets/{uuid}`: altera `title`, `description` ou `priority`, ao menos um campo.
- `PATCH /api/v1/tickets/{uuid}/status`: recebe `{"status":"in_progress"}`; aceita apenas `open → in_progress`, `in_progress → resolved`, `resolved → in_progress`. Retorna 409 em transição inválida.
- 422 para dados inválidos, 404 para UUID inexistente.


## Sprint 06 — parâmetros de listagem
- `search` (opcional, até 120 caracteres): pesquisa parcial no título, sem diferenciar maiúsculas/minúsculas.
- `status` (opcional): `open`, `in_progress`, `resolved`.
- `priority` (opcional): `low`, `medium`, `high`.
- Filtros são combinados por AND e aplicados antes de `limit`/`offset`.
- Exemplo: `GET /api/v1/tickets?search=relatório&status=open&priority=high&limit=11&offset=0`.
- Filtros inválidos retornam 422. Nenhuma migration adicional.

## Dashboard — Sprint 07

`GET /api/v1/dashboard/summary` retorna contagens agregadas de **todos** os chamados (independentemente da paginação e dos filtros da listagem):

```json
{
  "total": 4,
  "by_status": {"open": 2, "in_progress": 1, "resolved": 1},
  "by_priority": {"low": 1, "medium": 1, "high": 2}
}
```

Todos os campos são numéricos e os grupos incluem chaves com valor zero. Não há parâmetros.


## Sprint 08 — Autenticação

- `POST /api/v1/auth/login` — público; `{ "email": "...", "password": "..." }`; retorna `access_token`, `token_type` e `user`. Erro 401 para credenciais inválidas.
- `GET /api/v1/auth/me` — exige `Authorization: Bearer <token>`; retorna usuário atual.
- `POST /api/v1/users` — exige token de administrador; cria conta `{ "email", "name", "password", "role" }`. Retorna 201; 403 para agentes; 409 para e-mail duplicado; 422 para dados inválidos.
- Todos os endpoints de tickets e dashboard exigem Bearer token (401 sem token).


## Sprint 09 — Administração de usuários

`GET /api/v1/users?limit=50&offset=0` exige token JWT de administrador.
Retorna uma lista de usuários (`id`, `email`, `name`, `role`) sem hashes de senha.
`limit` aceita 1–100; `offset` deve ser não negativo. Erros: 401 sem autenticação, 403 agente, 422 paginação inválida.

`POST /api/v1/users` continua exclusivo de administradores, com corpo `{ "name": "...", "email": "...", "password": "...", "role": "agent" }`.
