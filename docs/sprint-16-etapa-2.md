# Sprint 16 — Etapa 2: integração React

- O botão **Sugerir com IA (simulação)** consulta `POST /api/v1/ai/triage` com o JWT existente.
- Sugestões exibem prioridade, categoria e motivo; **somente a prioridade** pode ser aplicada ao formulário.
- A sugestão não altera o banco nem envia o chamado automaticamente.
- Mudanças no título/descrição descartam sugestões antigas.
- Erros de rede e campos incompletos são tratados.
- `mock` representa regras determinísticas, não IA generativa.

Validar com `npm test -- --run` e `npm run build`, além de testar login, criação e edição de chamados manualmente.
