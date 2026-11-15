# Sprint 17 — Etapa 2: frontend

- Painel de rascunho de resposta na tela de detalhes do chamado.
- Usa o endpoint autenticado `POST /api/v1/ai/reply-suggestion`.
- Permite editar e copiar o texto; não publica respostas.
- Trata falhas, impede requisições duplicadas e descarta respostas desatualizadas.

## Validação

Na pasta `frontend`, execute `npm test` e `npm run build`. Depois abra um chamado e clique em **Sugerir resposta com IA**.


## Correcao do rascunho editavel
O campo continua visivel quando o usuario apaga todo o texto, usando hasSuggestion em vez de condicionar a renderizacao ao conteudo de draft. Testes cobrem limpeza e nova digitacao.
