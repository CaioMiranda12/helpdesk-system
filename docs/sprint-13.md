# Sprint 13 — Testes de frontend e preparação do portfólio

## Objetivos
- Adicionar Vitest + React Testing Library + jsdom ao frontend React/TypeScript.
- Testar formulários e login com interações reais simuladas, sem acessar o PostgreSQL.
- Testar o mapeamento de falhas da API para mensagens compreensíveis.
- Preparar um guia de demonstração e uma narrativa técnica honesta para entrevistas.

## Arquivos principais
- `frontend/package.json`: comandos `npm test` e `npm run test:watch`.
- `frontend/vite.config.ts`: configuração do Vitest em ambiente jsdom.
- `frontend/src/test/setup.ts`: matchers do jest-dom e limpeza entre testes.
- `frontend/src/components/TicketForm.test.tsx`: criação, validação nativa e erro de envio.
- `frontend/src/pages/Login.test.tsx`: login com sucesso e erro usando contexto simulado.
- `frontend/src/services/api.test.ts`: mensagens para conexão, timeout e permissão.
- `docs/portfolio.md`: roteiro de apresentação e limitações reais.

## Execução no Windows / PowerShell

```powershell
cd frontend
npm install
npm run typecheck
npm test
npm run build
```

Em seguida, na pasta `backend`, rode `python -m pytest -q` para verificar regressões.

**Nota:** testes unitários de frontend não substituem testes de integração com API/PostgreSQL nem testes E2E. Os testes usam simulações controladas; não precisam que FastAPI esteja ligado.

## Validação manual
1. Faça login como administrador e abra dashboard, usuários e chamados.
2. Crie um chamado, atribua um agente, comente e altere o status.
3. Verifique se o histórico carrega mais atividades.
4. Entre como agente e confirme a ausência da gestão de usuários.
5. Rode o build de produção e confirme que o projeto compila.

## Commits (branch master)
Na raiz do repositório, após os testes:

```powershell
git add frontend/package.json frontend/vite.config.ts frontend/src/test/setup.ts
git commit -m "test: configure Vitest and React Testing Library"
git push origin master

git add frontend/src/components/TicketForm.test.tsx frontend/src/pages/Login.test.tsx frontend/src/services/api.test.ts
git commit -m "test: cover frontend forms login and API errors"
git push origin master

git add README.md docs/sprint-13.md docs/portfolio.md
git commit -m "docs: prepare portfolio presentation and sprint 13 guide"
git push origin master
```

Se `npm install` gerar `frontend/package-lock.json`, inclua-o no **primeiro** commit com `git add frontend/package-lock.json`.

## Critérios de aceite
- `npm run typecheck`, `npm test` e `npm run build` passam localmente.
- Testes de backend continuam passando.
- Login, chamados e histórico funcionam manualmente.
- README e roteiro de portfólio não afirmam deploy ou recursos ainda inexistentes.
