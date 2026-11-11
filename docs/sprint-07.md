# Sprint 07 — Dashboard de chamados

## Objetivo
Exibir indicadores reais dos chamados registrados no PostgreSQL, com agregação feita no banco (SQLAlchemy `GROUP BY`) e interface React responsiva.

## Entregas
- `GET /api/v1/dashboard/summary`: total geral, totais por status e prioridade.
- Dashboard em `/dashboard` com quatro indicadores e barras de prioridade.
- Estados de carregamento, erro, atualização manual e base vazia.
- Testes automatizados de agregação, base vazia, mudança de status e independência da paginação.

## Decisões técnicas
- A API retorna números agregados, **não** a lista completa de chamados.
- Zero aparece explicitamente em todas as categorias, inclusive sem chamados.
- Dashboard representa todos os chamados, sem filtros, para não confundir com a listagem filtrada.
- Sem biblioteca de gráficos externa: barras CSS são suficientes para o MVP.
- Sem migration: não há alteração no modelo de dados.

## Implementação por etapas e commits (branch master)
Execute todos os comandos Git na raiz `helpdesk-system`. Teste antes de commitar.

1. **Endpoint e agregação:** `backend/app/schemas/dashboard.py`, `backend/app/services/dashboard.py`, `backend/app/api/v1/dashboard.py`, `backend/app/main.py`.
   `git commit -m "feat: add dashboard summary API"`
2. **Testes:** `backend/tests/test_dashboard.py`.
   `git commit -m "test: cover dashboard summary aggregation"`
3. **Frontend:** `frontend/src/pages/Dashboard.tsx`, `frontend/src/services/api.ts`, `frontend/src/types.ts`, `frontend/src/App.tsx`, `frontend/src/components/Layout.tsx`, `frontend/src/styles.css`.
   `git commit -m "feat: add ticket dashboard interface"`
4. **Documentação:** `README.md`, `docs/api.md`, `docs/sprint-07.md`.
   `git commit -m "docs: document dashboard sprint 07"`

Após cada commit, execute `git push origin master`.

## Validação

```powershell
# Terminal 1 — backend, com ambiente virtual ativo
python -m pytest -q
python -m uvicorn app.main:app --reload

# Terminal 2 — frontend
npm install
npm run typecheck
npm run build
npm run dev
```

Abra `http://localhost:5173/dashboard` e confirme:
1. Dashboard vazio: total e categorias iguais a zero, convite para criar chamado.
2. Crie três chamados com prioridades distintas; clique em Atualizar e confira as contagens.
3. Altere o status de um chamado e confira os novos números.
4. Pare a API, clique em Atualizar, observe o erro; reinicie e use Tentar novamente.
5. Compare com `SELECT status, count(*) FROM tickets GROUP BY status;` no Beekeeper.

## Próxima sprint sugerida
Autenticação e permissões, depois de discutir escopo e segurança.
