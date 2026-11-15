# Sprint 19 — Etapa 1: rate limiting

- Login: `LOGIN_RATE_LIMIT_PER_MINUTE` (padrão 5) por IP de conexão.
- IA: `AI_RATE_LIMIT_PER_MINUTE` (padrão 20) por usuário autenticado, compartilhado entre triagem, resposta e resumo.
- Excesso: HTTP 429 e cabeçalho `Retry-After`.
- A regra de negócio continua permitindo que todos os agentes autenticados visualizem todos os chamados.

## Limitações

A implementação é **em memória e por processo**. Reinícios zeram os contadores; múltiplos workers/instâncias possuem contadores independentes. **Não considerar esta implementação proteção suficiente para deploy multi-instância**: migrar para Redis ou rate limiting no gateway antes de publicar.

O IP usa `request.client.host`, sem confiar diretamente em `X-Forwarded-For`. Para produção atrás de proxy, configurar a lista de proxies confiáveis no servidor, ou aplicar rate limiting no gateway.

A limitação de login é por IP, não por conta; pode afetar usuários que compartilham uma mesma origem. A proteção de IA é por usuário, não por IP.

## Validação

Na pasta backend: `python -m pytest tests/test_rate_limit.py -q` e depois `python -m pytest -q`.
