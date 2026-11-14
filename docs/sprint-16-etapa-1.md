# Sprint 16 — Etapa 1: triagem simulada no backend

Esta etapa implementa `POST /api/v1/ai/triage`, autenticado via JWT, sem persistência ou migração de banco. O resultado é uma sugestão revisável, não uma decisão automática.

## Exemplo

```json
{"title":"Sistema financeiro fora do ar","description":"Ninguém consegue emitir nota fiscal desde cedo."}
```

Resposta: `priority: high`, `category: software`, `provider: mock` e justificativa.

## Testes

Na pasta `backend`, com `.venv` ativada: `python -m pytest tests/test_ai_triage.py -q` e depois `python -m pytest -q`.

O provedor `mock` é um classificador por palavras-chave, não um modelo de IA generativa. Não exige chave de API nem alterações no `.env`.
