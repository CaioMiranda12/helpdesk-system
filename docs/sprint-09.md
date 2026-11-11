# Sprint 09 — Gestão de usuários

## Objetivo
Permitir que administradores listem e cadastrem usuários pela interface React, sem usar o Swagger.

## Regras
- Somente `admin` acessa `GET /api/v1/users` e `POST /api/v1/users`.
- Agentes não veem o menu **Usuários**. A API continua aplicando autorização, independentemente da interface.
- A resposta da API nunca inclui senhas ou hashes.
- Cadastro exige nome de 2–120 caracteres, e-mail válido e senha de 12–128 caracteres.
- E-mail duplicado retorna HTTP 409.
- A lista exibe até 100 usuários no MVP; paginação de UI e edição ficam fora do escopo.
- Não há alteração de schema, portanto nenhuma nova migration.

## Execução
No `backend`, execute `python -m pytest -q` e `python -m uvicorn app.main:app --reload`.
No `frontend`, execute `npm run typecheck`, `npm run build` e `npm run dev`.
Entre como administrador e abra `http://localhost:5173/users`.

## Testes manuais
1. Administrador vê **Usuários** no menu e consegue cadastrar um agente.
2. E-mail duplicado mostra mensagem e não cria outro usuário.
3. Agente não vê o menu, e a URL `/users` redireciona para `/`.
4. Mesmo chamando a API diretamente, o agente recebe HTTP 403.
5. A senha nunca aparece na tabela nem no JSON de listagem.

## Commits (branch master)
1. `feat: add admin-only user listing endpoint`
2. `test: cover user listing authorization`
3. `feat: add user management interface`
4. `docs: document sprint 09 user management`

## Limitações
Não há redefinição de senha, desativação de usuários, auditoria, revogação de JWT nem paginação visual. Não publicar em produção sem reforços de segurança.
