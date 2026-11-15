# Sprint 19 — Etapa 2: minimização de dados para IA externa

Apenas as mensagens enviadas aos provedores Groq/OpenAI são minimizadas; os textos originais continuam no banco e na interface. O modo mock não precisa enviar dados a terceiros.

Cobertura: email, CPF formatado, telefones brasileiros usuais, Bearer tokens e chaves comuns `sk-`/`gsk_`. Essa lista é **parcial** e não representa anonimização completa. Nomes, endereços, números de documentos não formatados e outros segredos podem permanecer no texto livre.

O usuário deve revisar o conteúdo antes de solicitar IA externa. Evite inserir senhas, tokens, informações médicas, financeiras ou outros dados sensíveis nos chamados. Para ambientes reais, avaliar base legal, aviso de privacidade, retenção e regras contratuais dos provedores.

## Testes

No diretório `backend`:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_ai_privacy.py -q
.\.venv\Scripts\python.exe -m pytest -q
```

Nenhuma dependência ou migração nova é necessária. Não inclui mudanças de permissão dos agentes.
