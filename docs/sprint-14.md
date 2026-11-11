# Sprint 14 — Segurança e preparação para deploy

## Objetivo
Separar configuração de ambiente, revisar segurança e preparar containers para demonstração local. **Não é um deploy público pronto para produção.**

## Passos locais
1. No frontend: `npm install -D vitest@^3.2.7` (se ainda não atualizado), `npm run typecheck`, `npm test`, `npm run build`.
2. No backend: `python -m pytest -q`.
3. Revisar dependências: `npm audit` e `npm audit --omit=dev`; avaliar cada alerta sem `--force`.
4. Copiar `.env.compose.example` para `.env` **na raiz** e substituir senhas e segredo JWT. Nunca versionar `.env`.
5. Rodar `docker compose up --build -d db api`.
6. Criar tabelas: `docker compose exec api alembic upgrade head`.
7. Criar admin: `docker compose exec -it api python -m scripts.create_admin`.
8. Iniciar interface: `docker compose up --build -d web`.
9. Testar `http://localhost:8000/health`, `http://localhost:8000/docs` e `http://localhost:8080`.
10. Finalizar: `docker compose down` (não use `-v`, pois isso apagaria o volume do PostgreSQL).

## Observações de segurança
- A configuração CORS usa `CORS_ORIGINS` com origens explícitas separadas por vírgulas. Não use `*` em produção.
- `APP_ENVIRONMENT=production` exige JWT_SECRET_KEY com pelo menos 32 caracteres e desativa Swagger e ReDoc. Use HTTPS no proxy de produção.
- `VITE_API_URL` é incorporado no **build** do frontend, não é segredo e não pode conter credenciais.
- Docker Compose é apenas um ambiente de demonstração local: a API é exposta em `localhost:8000`, não há HTTPS, backups, rate limiting ou processo de atualização zero-downtime.
- A aplicação ainda armazena o token JWT no navegador; para deploy público, avaliar proteção contra XSS, política CSP, estratégia de autenticação, rate limiting e revogação de tokens.
- Não versionar logs com credenciais, `.env`, banco ou backups.
- O `npm install` do Dockerfile é intencionalmente tolerante à ausência de lockfile no ZIP de origem. Para builds reproduzíveis, versionar `package-lock.json` e trocar por `npm ci`.

## Critérios de aceite
- `pytest` sem falhas; `npm run typecheck`, `npm test`, `npm run build` sem falhas.
- CORS configurável, segredo forte exigido em modo production.
- Login, tickets, usuários e histórico funcionando no Compose.
- `npm audit` analisado e riscos registrados antes de qualquer publicação pública.
