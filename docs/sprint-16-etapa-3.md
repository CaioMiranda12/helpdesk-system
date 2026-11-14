# Sprint 16 — Etapa 3: provedor real opcional

- `AI_PROVIDER=mock` mantém comportamento existente, sem custos e sem acesso externo.
- `AI_PROVIDER=openai` usa a API OpenAI e requer `OPENAI_API_KEY` no `backend/.env` (nunca no frontend nem no Git).
- `OPENAI_MODEL=gpt-4.1-mini` é configurável; confirme disponibilidade e preços na sua conta antes de usar.
- O servidor envia título e descrição do chamado ao provedor externo. **Não use dados pessoais/sensíveis sem autorização.**
- Resposta é validada; erros externos viram HTTP 503 sem vazar segredos. Não há fallback silencioso para mock.
- Endpoint continua autenticado; nenhuma migração de banco.
- Sugestões devem ser revisadas por um humano antes de aplicar.

## Validação

1. Testar primeiro com `AI_PROVIDER=mock`: `python -m pytest -q`.
2. Testar `npm test` e `npm run build` no frontend.
3. Opcional: configurar chave e `AI_PROVIDER=openai` no `.env`, reiniciar FastAPI e chamar o endpoint autenticado.
4. Testar login, criação de chamado e dashboard.

**Atenção:** uso de API externa pode gerar custos; não coloque chave no repositório.
