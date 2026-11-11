# Sprint 02 — Persistência com PostgreSQL

## Objetivo
Configurar o acesso ao PostgreSQL, definir a tabela `tickets` com SQLAlchemy e aplicar a primeira migration Alembic. **Não há CRUD nesta sprint.**

## Pré-requisitos
- Python 3.11+ e PostgreSQL instalado e em execução (ou banco PostgreSQL em container).
- Sprint 01 concluída; executar comandos a partir de `backend/`.
- Nunca versionar `.env` ou senhas.

## Etapa 2.1 — Configurar conexão
1. Atualize `backend/requirements.txt` e instale: `python -m pip install -r requirements.txt`.
2. Crie um usuário e banco de desenvolvimento (via `psql` conectado como administrador):

```sql
CREATE USER helpdesk WITH PASSWORD 'change-me';
CREATE DATABASE helpdesk OWNER helpdesk;
```

3. Copie `.env.example` para `.env` dentro de `backend/`, ajuste credenciais e teste:

```bash
python -c "from app.db.session import engine; from sqlalchemy import text; c = engine.connect(); print(c.execute(text('SELECT 1')).scalar()); c.close()"
```

Resultado esperado: `1`. O arquivo `.env` não deve entrar no Git.

**Commit após validar:** `chore: configure PostgreSQL database connection`
Arquivos: `backend/requirements.txt`, `backend/.env.example`, `backend/app/core/`, `backend/app/db/`.

## Etapa 2.2 — Criar modelo
Inspecione `backend/app/models/ticket.py`. Os campos são UUID, título, descrição, prioridade, status e timestamps com fuso. Restrições SQL protegem valores válidos e comprimento dos textos. A atualização de `updated_at` será feita explicitamente na Sprint 03 (evitando atualizações em operações sem mudanças).

Valide com `python -m pytest -q`.

**Commit após validar:** `feat: add ticket database model`
Arquivos: `backend/app/models/`, `backend/tests/test_ticket_model.py`.

## Etapa 2.3 — Criar a migration
A primeira migration já está versionada em `backend/alembic/versions/0001_create_tickets.py`. **Não rode `alembic revision --autogenerate` para recriar esta migration.**

```bash
alembic upgrade head
alembic current
```

Verifique a tabela no `psql` conectado ao banco `helpdesk`:

```sql
\d tickets
SELECT * FROM alembic_version;
```

**Commit após validar:** `chore: setup Alembic database migrations`
Arquivos: `backend/alembic.ini`, `backend/alembic/`.

## Etapa 2.4 — Documentação
Leia `docs/architecture.md`, `docs/decisions.md`, `docs/api.md` e este guia. Faça o commit de documentação após revisar as instruções.

**Commit:** `docs: document database setup and architecture`

## Comandos Git para cada etapa

```bash
git status
git add <arquivos-da-etapa>
git commit -m "<mensagem-da-etapa>"
git push origin main
```

Evite `git add .` se existirem alterações de etapas posteriores ainda não validadas.

## Critérios de conclusão
- Conexão real com PostgreSQL validada por `SELECT 1`.
- Testes locais passam.
- `alembic upgrade head` aplica a migration sem erros.
- `alembic current` mostra `0001_create_tickets`.
- `.env` não está versionado.

## Limitações
Testes automatizados aqui verificam o modelo e o DDL; não substituem a execução real da migration no PostgreSQL. Sem autenticação, use apenas dados fictícios.
