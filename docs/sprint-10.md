# Sprint 10 — Atribuição de chamados

## Objetivo
Permitir que administradores atribuam, troquem e removam responsáveis dos chamados, mantendo agentes com acesso de leitura.

## Regras
- O responsável é opcional (`assignee_id = null`), inclusive para chamados anteriores.
- Apenas usuários com papel `agent` podem ser responsáveis.
- Somente administradores podem modificar a atribuição; agentes podem visualizar.
- Um chamado possui no máximo um responsável nesta versão.
- A mudança não altera o status automaticamente.
- Ao excluir um usuário diretamente no banco, a FK usa `ON DELETE SET NULL`; o projeto não disponibiliza exclusão de usuários pela API.

## Banco de dados
Migration `0003_add_ticket_assignee`: adiciona `tickets.assignee_id UUID NULL`, FK para `users.id` e índice. Não recria a tabela de chamados.

```powershell
cd backend
alembic upgrade head
alembic current
python -m pytest -q
```

Verificação no Beekeeper:

```sql
SELECT t.title, t.status, u.name AS responsavel
FROM tickets t LEFT JOIN users u ON u.id = t.assignee_id
ORDER BY t.created_at DESC;
```

## API
- `GET /api/v1/agents`: lista agentes para qualquer usuário autenticado; não retorna hash de senha.
- `PATCH /api/v1/tickets/{id}/assignee`: somente administrador, JSON `{ "assignee_id": "UUID" }` ou `{ "assignee_id": null }`.
- Respostas: 200 sucesso; 401 sem login; 403 sem permissão; 404 chamado/agente inexistente; 409 usuário não é agente; 422 dados inválidos.
- As respostas de chamados agora incluem `assignee_id` e `assignee` (id, nome, e-mail), ambos nulos se não houver responsável.

## Frontend
Na tela de detalhes, administradores podem escolher o agente ou `Sem responsável`. Agentes visualizam o nome do responsável. A listagem exibe coluna `Responsável`.

```powershell
cd frontend
npm install
npm run typecheck
npm run build
npm run dev
```

## Commits — master
1. `feat: add ticket assignee relation and migration`
2. `feat: implement ticket assignment API and permissions`
3. `test: cover ticket assignment and access rules`
4. `feat: add ticket assignee controls to frontend`
5. `docs: document sprint 10 ticket assignment`

## Testes manuais
1. Verificar que chamados anteriores continuam sem responsável.
2. Cadastrar dois agentes na área Usuários.
3. Entrar como administrador, atribuir e trocar o responsável de um chamado.
4. Remover o responsável usando `Sem responsável`.
5. Entrar como agente, confirmar leitura do responsável e ausência do seletor.
6. No Swagger, tentar atribuir com token de agente e confirmar 403.
7. Comparar dados no Beekeeper.
