# Sprint 18 — Etapa 2: frontend

Adiciona geração sob demanda de resumo de atividades no painel de histórico de um chamado.

- Usa `POST /api/v1/tickets/{ticket_id}/activities/ai-summary` com autenticação existente.
- Mostra provedor, quantidade de atividades consideradas e resumo.
- Desabilita geração quando não há atividades carregadas.
- Invalida o resumo após mudanças de chamado, status, atribuição ou publicação de comentário.
- Mantém comentários, paginação e histórico originais; nenhuma ação automática.

## Validação

```bash
cd frontend
npm test
npm run build
```

## Commit sugerido

`feat: integra resumo de atividades com IA ao historico de chamados`
