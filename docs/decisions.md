# Registro de decisões técnicas

Registre aqui as escolhas, alternativas, motivos e consequências. Reavalie uma decisão quando o requisito mudar.

## ADR-001 — MVP enxuto

**Decisão:** começar com CRUD parcial (sem exclusão), atualização de status e interface simples.

**Motivo:** priorizar a entrega ponta a ponta e a aderência à vaga.

**Consequência:** comentários, atribuição e autenticação ficam para versões posteriores.

## ADR-002 — FastAPI e Python

**Decisão:** FastAPI no backend.

**Alternativa:** Django REST Framework.

**Motivo:** foco em endpoints, validação e integração REST; Python é requisito relevante da vaga.

**Consequência:** autenticação e administração exigirão implementação/integração posterior.

## ADR-003 — React, TypeScript e Vite

**Decisão:** SPA React separada da API.

**Alternativa:** Next.js.

**Motivo:** painel interno não exige SEO ou renderização no servidor.

**Consequência:** configurar chamadas HTTP e CORS adequadamente.

## ADR-004 — PostgreSQL e SQLAlchemy

**Decisão:** banco relacional e ORM com migrações Alembic.

**Alternativa:** SQLite e SQL puro.

**Motivo:** prática de persistência relacional e evolução de esquema.

**Consequência:** mais configuração local e necessidade de conhecer SQL.

## ADR-005 — Sem autenticação no MVP

**Decisão:** executar localmente com dados fictícios.

**Motivo:** validar primeiro as regras de negócio.

**Consequência:** não utilizar com dados reais nem expor publicamente uma API de escrita sem controles de acesso.

## ADR-006 — Sem exclusão de chamados

**Decisão:** não criar `DELETE` no MVP.

**Motivo:** preservar histórico e reduzir escopo.

**Consequência:** eventual arquivamento ou exclusão lógica poderá ser avaliado no futuro.

## ADR-007 — SQLAlchemy síncrono e sem camada de repositórios inicial

**Decisão:** sessões síncronas e serviços separados das rotas.

**Motivo:** diminuir abstrações enquanto as regras são simples.

**Consequência:** reavaliar extração de repositórios e async se surgir necessidade demonstrável.

## Template para novas decisões

```text
## ADR-XXX — Título
Contexto:
Decisão:
Alternativas:
Motivo:
Consequências e riscos:
Quando revisar:
```
