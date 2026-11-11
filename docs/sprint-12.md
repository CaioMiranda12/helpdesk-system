# Sprint 12 — Paginação e desempenho do histórico

## Objetivo
Evitar carregar todas as atividades de um chamado de uma vez e melhorar a consulta do PostgreSQL. Preservar a autenticação, os dados e o contrato da API da Sprint 11.

## Alterações
- A tela de detalhes mostra inicialmente **10 atividades**, da mais recente para a mais antiga.
- O botão **Carregar atividades anteriores** acrescenta mais 10 por vez, sem substituir o histórico já exibido.
- A interface pede `limit=11` para detectar se existem mais resultados, exibindo somente 10. Na próxima chamada, utiliza `offset=10`, depois `offset=20`, etc.
- O botão fica desabilitado durante o carregamento; há mensagens de erro e opção de tentar novamente.
- Ao publicar um comentário, mudar de chamado ou atualizar status/responsável, a linha do tempo volta à primeira página para exibir os eventos recentes.
- A migration `0005_index_ticket_activities` cria índice composto em `(ticket_id, created_at, id)` para favorecer o filtro por chamado e a ordenação cronológica. Não remove nem altera atividades.

## API (sem mudanças de contrato)
`GET /api/v1/tickets/{ticket_id}/activities?limit=11&offset=0`

- `limit`: 1 a 100 (padrão 50); `offset`: inteiro >= 0 (padrão 0).
- Resposta: lista de atividades ordenadas por `created_at DESC, id DESC`.
- Autenticação JWT obrigatória. Um chamado inexistente retorna 404.

## Passo a passo
1. Faça backup do banco se houver dados importantes e incorpore a atualização mantendo `.env`, `.git` e `node_modules`.
2. Na pasta `backend`, execute `alembic upgrade head` e `alembic current` (esperado: `0005_index_ticket_activities`).
3. Execute `python -m pytest -q` e inicie o FastAPI.
4. Na pasta `frontend`, execute `npm run typecheck`, `npm run build`, `npm run dev`.
5. Abra um chamado com 25+ comentários. Confirme 10 eventos, carregue mais duas vezes e verifique a ordem sem duplicações.
6. Publique um novo comentário e confira que ele aparece no topo. Pare o backend e teste o tratamento de erro.

## Consultas Beekeeper
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'ticket_activities';
```

```sql
SELECT kind, created_at
FROM ticket_activities
WHERE ticket_id = 'COLE_AQUI_UM_UUID_VALIDO'
ORDER BY created_at DESC, id DESC
LIMIT 11 OFFSET 0;
```

## Decisões e limitações
- Paginação por `OFFSET` é adequada ao tamanho atual do MVP. Em alto volume, pode ser melhor migrar para paginação por cursor, evitando custo de offsets elevados.
- Se novas atividades forem adicionadas por outra pessoa durante a paginação, `OFFSET` pode repetir ou pular itens. A UI remove IDs duplicados, mas não garante consistência de snapshot.
- Não criamos uma nova tabela e não alteramos permissões.

## Commits (branch master)
1. `perf: add index for ticket activity timeline`
2. `test: cover activity pagination and privacy`
3. `feat: paginate ticket activity timeline`
4. `docs: document sprint 12 activity pagination`
