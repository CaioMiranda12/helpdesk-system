# Sprint 16 — Etapa 4: Groq

Adiciona `groq` como terceiro provedor de triagem, sem modificar a rota, o frontend ou o banco.

## Configuração

No `backend/.env`, configure:

```dotenv
AI_PROVIDER=groq
GROQ_API_KEY=sua-chave-groq
GROQ_MODEL=openai/gpt-oss-20b
```

Obtenha a chave em https://console.groq.com/keys. Não faça commit do `.env`.

O provedor `mock` continua sendo o padrão. Para usar OpenAI, configure `AI_PROVIDER=openai` e as variáveis existentes.

## Verificação

Execute `python -m pytest tests/test_ai_provider.py -q` no backend e depois toda a suíte. Teste o formulário com um chamado fictício. Se a conta estiver sem cota ou a API indisponível, o backend retorna HTTP 503 sem expor a chave. A prioridade sugerida continua dependendo de confirmação humana.

**Privacidade:** título e descrição são enviados ao Groq quando esse provedor é selecionado; não use dados pessoais ou confidenciais no teste.
