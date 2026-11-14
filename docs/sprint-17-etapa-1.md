# Sprint 17 — Etapa 1: sugestões de respostas (backend)

- `POST /api/v1/ai/reply-suggestion` autenticado com o mesmo JWT da triagem.
- Entrada: `title` (5–120 caracteres), `description` (10–2000 caracteres).
- Saída: `suggestion` (10–1200 caracteres), `provider`.
- `AI_PROVIDER=mock` gera texto fixo para testes; `groq` e `openai` geram rascunho com IA.
- Não persiste, envia ou publica respostas. O usuário deve revisar e decidir o que fazer com o texto.
- Não enviar dados sensíveis ou pessoais nos chamados utilizados com provedores externos.
- Não altera banco, autenticação, triagem nem frontend.

## Testes

`cd backend` e `./.venv/Scripts/python.exe -m pytest tests/test_ai_reply.py -q` no Windows.

Depois execute a suíte completa e valide o endpoint no Swagger com um token válido.
