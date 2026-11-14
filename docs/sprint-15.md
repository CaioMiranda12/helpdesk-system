# Sprint 15 — Integração contínua com GitHub Actions

## Objetivo

Validar automaticamente o backend FastAPI e o frontend React em pushes e pull requests para `master`, além de permitir execução manual pela aba **Actions**.

## Entrega

- `.github/workflows/ci.yml`: dois jobs independentes (`backend` e `frontend`) em Ubuntu.
- Backend: Python 3.13, dependências de `backend/requirements.txt`, `python -m pytest -q`.
- Frontend: Node.js 22, `npm ci`, TypeScript, Vitest e build Vite.
- Permissões mínimas de leitura para o token de CI; cancelamento de execuções redundantes.

## Pré-requisitos

1. Confirmar que `frontend/package-lock.json` está versionado (`git ls-files frontend/package-lock.json`). Se não estiver, dentro de `frontend` execute `npm install`, e depois, na raiz, `git add frontend/package-lock.json`.
2. Não adicionar arquivos `.env` reais ou senhas ao repositório. O job de backend utiliza valores de teste para as variáveis obrigatórias.
3. O backend utiliza SQLite em memória nos testes; a CI não precisa iniciar PostgreSQL ou Docker. Se futuramente houver testes de integração que exigem PostgreSQL, será necessário configurar um service container.

## Validação local

Na pasta `backend` (ambiente virtual ativo):

```powershell
python -m pytest -q
```

Na pasta `frontend`:

```powershell
npm ci
npm run typecheck
npm test
npm run build
```

## Validar no GitHub

1. Faça commit e push do workflow e do arquivo de lock (se necessário).
2. Abra **GitHub → repositório → Actions → CI**.
3. Confira se os jobs **Backend / pytest** e **Frontend / typecheck, tests, build** ficaram verdes.
4. Em caso de falha, abra o job e leia a primeira etapa que falhou; corrija o problema e faça novo push.
5. Opcional: em **Settings → Branches / Rulesets**, configure a exigência dos dois checks antes de permitir merges para `master`.

## Limitações

- A CI verifica testes e build; **não** publica a aplicação nem comprova que o Docker Compose funciona.
- O número de testes pode evoluir; o critério é todos passarem, não uma contagem fixa.
- Não inclua credenciais de produção no workflow. Para um deploy futuro, use GitHub Actions Secrets ou OIDC conforme o provedor.
