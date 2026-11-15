# Sprint 18 — Etapa 1: resumo de atividades (backend)

`POST /api/v1/tickets/{ticket_id}/activities/ai-summary` exige JWT e consulta o histórico no servidor.

- Confirma que o chamado existe (404 se não existir).
- Responde 409 quando não há atividades.
- Considera até 50 atividades recentes, em ordem cronológica, para limitar custos e contexto.
- Não envia IDs de autores, nomes, emails ou tokens ao provedor; comentários podem conter informações pessoais inseridas livremente, portanto revise a política de dados antes de usar IA externa com dados reais.
- `AI_PROVIDER=mock` funciona sem chave; `groq` usa SDK oficial; `openai` usa a API existente.
- Não persiste, modifica ou publica atividades.
- Respostas inválidas/indisponibilidade retornam 503 sem expor detalhes externos.

## Testes

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/test_ai_activity_summary.py -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Exemplo

```json
{"summary":"O atendimento foi iniciado e está em andamento.","provider":"groq","activities_considered":2}
```
