# Contrato da API — Proposta v1

**Estado:** contrato planejado; na Sprint 01 somente `/health` está implementado.

Base: `/api/v1` para recursos de negócio. JSON para requisições e respostas.

| Método | Caminho | Sucesso | Finalidade |
|---|---|---|---|
| GET | `/health` | 200 | Verificar que a API responde |
| GET | `/api/v1/tickets` | 200 | Listar chamados |
| POST | `/api/v1/tickets` | 201 | Criar chamado |
| GET | `/api/v1/tickets/{id}` | 200 | Detalhes de um chamado |
| PATCH | `/api/v1/tickets/{id}` | 200 | Editar campos permitidos |
| PATCH | `/api/v1/tickets/{id}/status` | 200 | Atualizar status |

## Exemplo: criar chamado

`POST /api/v1/tickets`

```json
{
  "title": "Erro ao abrir relatório",
  "description": "A página apresenta erro ao carregar o relatório mensal.",
  "priority": "high"
}
```

Resposta ilustrativa `201 Created`:

```json
{
  "id": "4b437a2d-5e42-46d8-9466-7ad36a836ee2",
  "title": "Erro ao abrir relatório",
  "description": "A página apresenta erro ao carregar o relatório mensal.",
  "priority": "high",
  "status": "open",
  "created_at": "2026-11-11T15:00:00Z",
  "updated_at": "2026-11-11T15:00:00Z"
}
```

## Atualizar status

`PATCH /api/v1/tickets/{id}/status`

```json
{"status": "in_progress"}
```

Transições: `open` → `in_progress` → `resolved` → `in_progress`.

## Listagem

`GET /api/v1/tickets?limit=20&offset=0`

Ordenação padrão: `created_at DESC`, com `id` como desempate. Formato da resposta da lista (array ou envelope paginado) será decidido antes da Sprint 03.

## Erros

- `404`: chamado inexistente.
- `422`: parâmetros ou corpo inválidos.
- `409`: transição de status proibida.
- `500`: erro inesperado, sem expor detalhes internos.

O formato final do corpo de erro será definido junto aos schemas, mantendo mensagens úteis ao frontend. O Swagger do FastAPI será a referência para os endpoints efetivamente implementados.
