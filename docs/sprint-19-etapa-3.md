# Sprint 19 — Etapa 3: endurecimento inicial de containers

## Alterações
- Backend executa como usuário não privilegiado (`appuser`) dentro do container.
- Frontend usa `npm ci` com `package-lock.json` para instalação reproduzível.
- Novo `compose.production.yaml` independente do `compose.yaml` de desenvolvimento, que permanece inalterado.
- Exemplo de produção publica API e frontend somente em `127.0.0.1` e não publica a porta do PostgreSQL.
- Ambiente de produção desativa documentação interativa conforme `app/main.py` existente e exige chave JWT forte.

## Limitações e pré-requisitos
- **Não é um deploy pronto para a internet**. É necessário configurar proxy reverso, HTTPS/TLS, DNS, backups, migrações Alembic e monitoramento na Sprint 20.
- O frontend usa `VITE_API_URL` em tempo de build; informe a URL pública HTTPS correta antes de construir a imagem. Não coloque segredos em variáveis `VITE_*`.
- `DATABASE_URL` deve apontar para `db:5432`, usando usuário e senha corretos. Se a senha contiver caracteres especiais, faça URL encoding nela.
- Configure `POSTGRES_PASSWORD`, `DATABASE_URL`, `JWT_SECRET_KEY` (aleatória com pelo menos 32 caracteres), `CORS_ORIGINS` (origem HTTPS do frontend) e `VITE_API_URL` em um `.env` privado no servidor; nunca comite o arquivo.
- O limitador da Sprint 19 Etapa 1 é em memória por processo: para múltiplos workers/instâncias, substituir por Redis ou limitador compartilhado antes de escalar.
- As regras de acesso aos chamados não foram modificadas.

## Validação local (não precisa de credenciais reais)
```powershell
docker compose -f compose.yaml config --quiet
docker compose -f compose.yaml build api web
```

## Validação de sintaxe do compose de produção
Com variáveis de teste **não reais**, apenas para validar a configuração:
```powershell
$env:POSTGRES_PASSWORD='senha-teste-local'
$env:DATABASE_URL='postgresql+psycopg://helpdesk_user:senha-teste-local@db:5432/helpdesk'
$env:JWT_SECRET_KEY='chave-apenas-para-validacao-123456789012345'
$env:CORS_ORIGINS='https://helpdesk.example.com'
$env:VITE_API_URL='https://api.helpdesk.example.com'
docker compose -f compose.production.yaml config --quiet
```
**Não suba produção com esses valores de exemplo.**

## Testes de regressão
```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
cd ../frontend
npm test
npm run build
```
