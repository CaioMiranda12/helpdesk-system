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
