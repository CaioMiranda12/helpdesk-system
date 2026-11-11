# Helpdesk System — Sistema de Gestão de Chamados

Projeto de portfólio full-stack: **FastAPI + SQLAlchemy + PostgreSQL + React + TypeScript + Vite**.

## Funcionalidades (Sprint 09)
- CRUD parcial de chamados (criação, listagem, consulta, edição e mudança de status).
- Pesquisa, filtros por status/prioridade e paginação.
- Dashboard com totais por status e prioridade.
- Login JWT e dois papéis: `admin` e `agent`.
- Criação e listagem de usuários exclusivamente por administradores, agora também pela interface React; sem cadastro público.
- Testes Pytest e migrations Alembic.

## Como executar

### Backend
```powershell
cd backend
python -m pip install -r requirements.txt
```
Copie `backend/.env.example` para `backend/.env` (se ainda não existir), preservando sua `DATABASE_URL` válida. Adicione `JWT_SECRET_KEY` gerada com:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```
Não envie `.env` ao GitHub. Com o PostgreSQL ligado:
```powershell
alembic upgrade head
python -m scripts.create_admin
python -m pytest -q
python -m uvicorn app.main:app --reload
```

### Frontend (outro terminal)
```powershell
cd frontend
npm install
npm run typecheck
npm run build
npm run dev
```
Acesse `http://localhost:5173/login`. API e Swagger em `http://127.0.0.1:8000/docs`.

## Documentação
- [Sprint 09 — Gestão de usuários](docs/sprint-09.md)
- [Sprint 09 — Autenticação](docs/sprint-08.md)
- [Contrato da API](docs/api.md)
- [Arquitetura](docs/architecture.md)
- [Histórico de decisões](docs/decisions.md)

**Atenção:** autenticação educacional/MVP; não pronta para produção. Consulte os limites de segurança em `docs/sprint-08.md`.


### Sprint 10 — Atribuição de responsáveis

Execute `alembic upgrade head` no backend para adicionar `assignee_id` sem apagar chamados existentes. Atribuições são feitas por administradores na página de detalhes; agentes apenas visualizam. Veja [docs/sprint-10.md](docs/sprint-10.md).

### Sprint 11 — Comentários e histórico

Execute `alembic upgrade head` no backend (migration `0004_create_ticket_activities`). A página de detalhes agora mostra comentários e eventos de status/atribuição. Consulte `docs/sprint-11.md`.

## Sprint 12 — Histórico paginado

A tela de detalhes agora carrega 10 atividades por vez e permite buscar eventos anteriores. O backend ganhou índice de consulta para o histórico. Veja [docs/sprint-12.md](docs/sprint-12.md).

## Sprint 13 — Testes de frontend e apresentação

O frontend agora inclui testes de componentes com **Vitest + React Testing Library**. Em `frontend/`, execute `npm install`, `npm run typecheck`, `npm test` e `npm run build`. Veja [guia da Sprint 13](docs/sprint-13.md) e [roteiro de portfólio](docs/portfolio.md). Os testes não substituem uma validação ponta a ponta com FastAPI e PostgreSQL.


## Sprint 14 — Preparação para deploy

Consulte [docs/sprint-14.md](docs/sprint-14.md) e [docs/security-checklist.md](docs/security-checklist.md). Ambiente Docker Compose destinado a demonstração local, não produção.
