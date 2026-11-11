# Sprint 04 — Interface React integrada à API

## Objetivo

Criar uma interface funcional para listar, cadastrar, consultar, editar e alterar o status dos chamados. O backend e o banco da Sprint 03 permanecem como fonte de dados.

## Stack

- React 18, TypeScript, Vite 6
- React Router para rotas
- Axios para HTTP
- CSS puro para evitar configuração extra no MVP

## Pré-requisitos

- Sprint 03 concluída e migrations aplicadas ao PostgreSQL.
- Node.js 20+ e npm.
- Python e PostgreSQL funcionando.

## Instalação

No terminal 1 (dentro de `backend`, com ambiente virtual ativo):

```bash
python -m uvicorn app.main:app --reload
```

No terminal 2 (dentro de `frontend`):

```bash
npm install
```

Copie `.env.example` para `.env` se quiser configurar a URL da API (padrão `http://127.0.0.1:8000`). Depois:

```bash
npm run typecheck
npm run build
npm run dev
```

Acesse `http://localhost:5173`.

## CORS

O arquivo `backend/app/main.py` permite requisições dos endereços `http://localhost:5173` e `http://127.0.0.1:5173`. Isso é necessário porque a interface e a API estão em portas diferentes. Reinicie o Uvicorn após alterar o arquivo. Não use `allow_origins=["*"]` sem avaliar os riscos.

## Funcionalidades e critérios de aceite

1. **Listagem:** exibe chamados, prioridade, status e data; paginação de 10 em 10. A API não retorna total de registros, então o botão Próxima fica desativado quando a página possui menos de 10 itens (uma página vazia pode ocorrer se o total for múltiplo de 10).
2. **Cadastro:** valida título (5–120), descrição (10–2000), prioridade e envia `POST /api/v1/tickets`; navega para os detalhes após receber `201`.
3. **Detalhes:** abre `GET /api/v1/tickets/{id}` e exibe campos do chamado.
4. **Edição:** usa `PATCH /api/v1/tickets/{id}` e atualiza a tela.
5. **Status:** oferece apenas as transições permitidas: `open → in_progress`, `in_progress → resolved`, `resolved → in_progress`. O backend permanece responsável por validar a regra.
6. **Erros:** mostra falhas de conexão, 404, 409 e 422 sem travar a interface.
7. **Responsividade:** layout se adapta a telas pequenas.

## Teste manual sugerido

1. Com backend e frontend ativos, abra `http://localhost:5173`.
2. Clique em **Novo chamado** e cadastre um chamado de teste.
3. Confirme a navegação para os detalhes.
4. Clique em **Editar chamado**, altere o título e salve.
5. Clique em **Mover para: Em andamento** e depois **Mover para: Resolvido**.
6. Retorne à listagem e confirme os dados.
7. No Beekeeper, execute `SELECT * FROM tickets ORDER BY created_at DESC;` e confira a persistência.
8. Pare o backend e recarregue a listagem; confirme que aparece mensagem de conexão indisponível.

## Limitações conscientes do MVP

Sem autenticação, busca, filtros, exclusão, testes de interface automatizados ou dashboard. Esses itens podem entrar em sprints posteriores.

## Commits — sempre na branch `master`

Execute os comandos na raiz `helpdesk-system` e apenas após validar a etapa:

**1. Base do frontend:**

```bash
git add frontend/package.json frontend/tsconfig.json frontend/vite.config.ts frontend/index.html frontend/.env.example frontend/.gitignore frontend/src/main.tsx frontend/src/App.tsx frontend/src/styles.css frontend/src/components/Layout.tsx
git commit -m "chore: setup React TypeScript frontend"
git push origin master
```

**2. Cliente HTTP, tipos e CORS:**

```bash
git add frontend/src/types.ts frontend/src/services/api.ts backend/app/main.py
git commit -m "feat: connect frontend to ticket API"
git push origin master
```

**3. Telas e formulário:**

```bash
git add frontend/src/components/TicketForm.tsx frontend/src/pages/
git commit -m "feat: add ticket management screens"
git push origin master
```

**4. Documentação:**

```bash
git add README.md docs/sprint-04.md
git commit -m "docs: document frontend setup and sprint 04"
git push origin master
```

> O frontend utiliza `npm install`, que gera `package-lock.json`. Inclua esse arquivo no commit 1 (`git add frontend/package-lock.json`) para travar versões. Se `npm install` falhar, não commite até resolver o problema.
