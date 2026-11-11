# Sprint 08 — Autenticação e permissões

## Objetivo
Adicionar autenticação com JWT e autorização por papel, sem excluir os chamados existentes.

## Papéis e regras
- `admin`: acesso aos chamados, dashboard e criação de contas por `POST /api/v1/users`.
- `agent`: acesso aos chamados e dashboard; não pode criar contas (403).
- Todos os endpoints `/api/v1/tickets` e `/api/v1/dashboard` exigem Bearer token.
- `GET /health` e `POST /api/v1/auth/login` são públicos.
- Não existe cadastro público, recuperação de senha, refresh token ou revogação de tokens nesta sprint.

## Configuração local
1. Na pasta `backend`, execute `python -m pip install -r requirements.txt`.
2. Preserve a `DATABASE_URL` atual do seu `.env` e adicione:
   ```dotenv
   JWT_SECRET_KEY=COLOQUE_AQUI_UMA_CHAVE_GERADA
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```
3. Gere uma chave aleatória no PowerShell com:
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(48))"
   ```
   Copie o resultado para `JWT_SECRET_KEY`. Não compartilhe nem versione essa chave.
4. Confirme que o PostgreSQL está ligado. Execute `alembic upgrade head` e depois `alembic current`; a revisão deve ser `0002_create_users`.
5. Crie a primeira conta de administrador:
   ```powershell
   python -m scripts.create_admin
   ```
   Informe nome, e-mail e uma senha com pelo menos 12 caracteres. A senha não é exibida no terminal.
6. Execute `python -m pytest -q` e `python -m uvicorn app.main:app --reload`.
7. Em outro terminal, `cd frontend`, `npm install`, `npm run typecheck`, `npm run build`, `npm run dev`.
8. Acesse `http://localhost:5173/login` e entre com a conta criada.

## Testar via Swagger
1. Faça `POST /api/v1/auth/login` com e-mail e senha; copie o `access_token`.
2. Clique em **Authorize** no Swagger e cole o token no campo Bearer (conforme o formulário).
3. Faça `GET /api/v1/auth/me` e `GET /api/v1/tickets`.
4. Crie um agente via `POST /api/v1/users`:
   ```json
   {"email":"agente@example.com","name":"Agente Suporte","password":"senha-com-12-caracteres","role":"agent"}
   ```
5. Entre como agente e tente criar outro usuário: a resposta esperada é **403**.
6. Sem token, `GET /api/v1/tickets` deve retornar **401**.
7. Verifique se os chamados antigos permanecem na tabela `tickets`.

## Arquitetura
- `models/user.py`: tabela `users` com e-mail único, nome, hash Argon2 e papel.
- `schemas/auth.py`: validação e respostas sem expor hashes.
- `core/security.py`: hash de senha, criação e validação JWT e dependências de autorização.
- `api/v1/auth.py`: login, perfil e cadastro administrativo.
- `alembic/versions/0002_create_users.py`: nova tabela, sem alterar `tickets`.
- `scripts/create_admin.py`: criação local e interativa da primeira conta.
- `frontend/src/contexts/AuthContext.tsx`: sessão e login/logout.
- `frontend/src/services/api.ts`: envia o Bearer token nas chamadas autenticadas.

## Segurança e limites do MVP
- O hash Argon2 é armazenado, nunca a senha em texto puro.
- O JWT é assinado com segredo local; use segredo forte e mantenha-o fora do Git.
- O token fica em `sessionStorage` e é apagado ao sair ou ao receber 401. Isso reduz persistência, mas **não elimina risco de XSS**.
- JWTs já emitidos continuam válidos até expirar mesmo após logout; logout limpa somente o navegador. Não há revogação no servidor.
- A autenticação não possui limitação de tentativas de login, bloqueio de conta, HTTPS configurado, logs de auditoria ou recuperação de senha; **não é uma configuração pronta para produção**.
- Em produção, use HTTPS, rate limiting, controles de sessão e política de segredos.
- O administrador tem papel `admin`; o agente tem `agent`. Não existe atribuição de chamados a usuários nesta sprint.

## Commits (branch master)
Na raiz do repositório, faça após validar cada etapa:
1. `feat: add user model and authentication migration`
2. `feat: implement JWT login and role authorization`
3. `test: cover authentication and access permissions`
4. `feat: add frontend login and protected routes`
5. `docs: document sprint 08 authentication setup`
