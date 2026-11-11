# Sistema de Gestão de Chamados

Aplicação Full Stack para registrar, acompanhar e atualizar chamados técnicos. Projeto de portfólio orientado a Python, React, APIs REST, banco de dados e manutenção de sistemas.

## Estado atual

**Sprint 01:** estrutura inicial do backend, endpoint de saúde e teste automatizado. Ainda não há CRUD, banco de dados, autenticação ou frontend implementados.

## Stack planejada

- Backend: Python, FastAPI, Pydantic, SQLAlchemy e Alembic
- Frontend: React, TypeScript e Vite
- Banco: PostgreSQL
- Testes: Pytest

Somente FastAPI e ferramentas de execução/testes estão instaladas na Sprint 01.

## Executar localmente

Requer Python 3.11+.

```bash
cd backend
python -m venv .venv
```

Ative o ambiente virtual:

- Windows PowerShell: `.\\.venv\\Scripts\\Activate.ps1`
- Linux/macOS: `source .venv/bin/activate`

Instale as dependências e execute:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

- API: http://localhost:8000/health
- Swagger: http://localhost:8000/docs
- OpenAPI: http://localhost:8000/openapi.json

Para testar (em outro terminal, com o ambiente ativo):

```bash
cd backend
python -m pytest -q
```

## Documentação

- [Requisitos](docs/requirements.md)
- [Arquitetura](docs/architecture.md)
- [Contrato da API](docs/api.md)
- [Decisões técnicas](docs/decisions.md)
- [Plano de implementação](docs/implementation-plan.md)

## Observação de segurança

O MVP inicial não terá autenticação. Use apenas dados fictícios e não publique uma instância com dados reais ou acesso irrestrito de escrita.

## Sprint 02 — Banco de dados
Leia [docs/sprint-02.md](docs/sprint-02.md) para configurar PostgreSQL, validar a conexão e aplicar a migration. A API de chamados será implementada na Sprint 03.

## Sprint 03
API de chamados implementada. Consulte `docs/sprint-03.md` para endpoints, testes e commits.

## Sprint 04 — Interface React

Frontend integrado à API, com listagem, cadastro, detalhes, edição e transições de status. Leia [docs/sprint-04.md](docs/sprint-04.md) para instalar, testar e commitar usando a branch `master`.

```bash
# Terminal 1 — dentro de backend
python -m uvicorn app.main:app --reload

# Terminal 2 — dentro de frontend
npm install
npm run dev
```

Abra http://localhost:5173. Configure `frontend/.env` a partir de `.env.example` somente se necessário.

## Sprint 05 — Qualidade

Testes de regressão da API, paginação confiável, recuperação de erros na listagem e tipagem de ambiente do Vite. Consulte [docs/sprint-05.md](docs/sprint-05.md).

## Sprint 06 — pesquisa e filtros
A listagem de chamados permite pesquisar por título e filtrar por status e prioridade, com filtros aplicados pelo backend antes da paginação. Consulte `docs/sprint-06.md`.
