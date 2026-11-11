# Sprint 11 — Comentários e histórico de atividades

## Objetivo
Permitir que usuários autenticados registrem comentários e consultem o histórico de um chamado, incluindo mudanças de status e responsável.

## Arquitetura
- `ticket_activities` registra autor, chamado, tipo (`comment`, `status`, `assignment`), conteúdo e valores anterior/novo.
- `POST /api/v1/tickets/{ticket_id}/comments` valida comentário (1–2000 caracteres após remover espaços), responde 201.
- `GET /api/v1/tickets/{ticket_id}/activities?limit=50&offset=0` retorna eventos mais recentes primeiro (limite máximo 100).
- Ambos exigem JWT. Agentes e administradores podem comentar e visualizar. Somente administradores podem atribuir responsáveis, como na Sprint 10.
- Mudanças de status e responsável gravam histórico na mesma transação da alteração do chamado; transições inválidas não geram eventos.
- Chamados anteriores à migration permanecem intactos e começam com histórico vazio.

## Instalação
1. Preservar `.env`, `.git` e arquivos locais.
2. No backend: `alembic upgrade head`; `alembic current` deve mostrar `0004_create_ticket_activities`.
3. Executar `python -m pytest -q` e `python -m uvicorn app.main:app --reload`.
4. No frontend: `npm run typecheck`, `npm run build`, `npm run dev`.
5. Abrir um chamado, comentar, mudar status, atribuir responsável e conferir a linha do tempo.

## SQL de verificação
```sql
SELECT kind, body, old_value, new_value, created_at
FROM ticket_activities
ORDER BY created_at DESC;
```

## Decisões
- Sem edição ou exclusão de comentários nesta sprint, para manter trilha simples.
- O histórico de atribuição armazena IDs dos usuários, não nomes; a UI exibe um texto genérico para mudanças de responsável.
- A primeira versão lista no máximo 100 atividades na interface. Paginação completa da linha do tempo fica para uma melhoria futura.
- Não expor `password_hash` em nenhuma resposta.
