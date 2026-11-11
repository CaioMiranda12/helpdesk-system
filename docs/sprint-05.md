# Sprint 05 — Qualidade, tratamento de erros e manutenção

## Objetivo
Melhorar a confiabilidade da aplicação sem acrescentar funcionalidades complexas.

## Alterações
1. **Regressão da API**: testes de paginação, entradas inválidas, persistência após erros e transições de status.
2. **Paginação correta no React**: o frontend solicita `PAGE_SIZE + 1` itens e mostra somente `PAGE_SIZE`. O item extra indica se há uma próxima página; assim, o botão não conduz a uma página vazia quando há exatamente dez registros.
3. **Recuperação de erros**: botão *Tentar novamente* na listagem; mensagens diferentes para timeout e erros 5xx.
4. **Tipagem do Vite**: `src/vite-env.d.ts` incluso para evitar o erro TS2339.

## Testes
No terminal da pasta `backend`, com o ambiente virtual ativo:

```bash
python -m pytest -q
python -m uvicorn app.main:app --reload
```

No terminal da pasta `frontend`:

```bash
npm install
npm run typecheck
npm run build
npm run dev
```

## Testes manuais
- Criar exatamente 10 chamados e confirmar que o botão Próxima fica desabilitado.
- Criar o 11º chamado e confirmar que a segunda página aparece.
- Parar temporariamente a API e usar *Tentar novamente* após religá-la.
- Conferir a criação e edição de chamados no Beekeeper.

## Commits — branch master
Na raiz do projeto, após validar os testes:

```bash
git add backend/tests/test_ticket_api.py
git commit -m "test: expand ticket API regression coverage"
git push origin master

git add frontend/src/pages/TicketList.tsx frontend/src/services/api.ts frontend/src/vite-env.d.ts
git commit -m "fix: improve pagination and API error recovery"
git push origin master

git add backend/app/main.py docs/sprint-05.md README.md
git commit -m "docs: document sprint 05 quality improvements"
git push origin master
```

> Se `vite-env.d.ts` já estiver versionado, `git add` não o incluirá novamente; isso é normal. Não faça commit do `.env`, da `.venv` ou de `node_modules`.
