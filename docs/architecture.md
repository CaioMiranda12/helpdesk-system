# Arquitetura — Sistema de Gestão de Chamados

**Versão:** 1.1 | **Estratégia:** monólito modular com frontend separado

## Fluxo de uma operação

1. Usuário interage com uma página React.
2. Frontend envia JSON por HTTP à API FastAPI.
3. Pydantic valida os dados recebidos.
4. Serviço aplica as regras de negócio.
5. SQLAlchemy lê/grava no PostgreSQL.
6. API retorna resposta e código HTTP apropriado.
7. Frontend atualiza a interface e apresenta feedback.

```text
React + TypeScript
        |
      HTTP/JSON
        |
FastAPI (rotas e schemas)
        |
Serviços (regras de negócio)
        |
SQLAlchemy + PostgreSQL
```

## Tecnologias e motivos

| Tecnologia | Papel | Justificativa | Trade-off |
|---|---|---|---|
| Python | Linguagem do backend | Alinhada à vaga e adequada a APIs | Nova linguagem a dominar |
| FastAPI | API REST | Schemas, validação e OpenAPI | Menos recursos prontos que Django |
| React + TypeScript | Interface | Reutiliza conhecimento existente | Frontend e backend exigem integração explícita |
| Vite | Build e desenvolvimento frontend | Configuração leve para SPA | Não oferece recursos de framework full stack |
| PostgreSQL | Persistência | Integridade e relações SQL | Exige serviço local |
| SQLAlchemy | ORM | Modelagem e sessões em Python | Requer entender SQL gerado |
| Alembic | Migrações | Versiona esquema do banco | Configuração inicial extra |
| Pytest | Testes | Bom suporte a testes Python | Exige dados e isolamento de testes |

## Estrutura planejada

```text
backend/app/
  main.py
  api/v1/tickets.py
  schemas/ticket.py
  models/ticket.py
  services/ticket_service.py
  db/session.py
  core/config.py
backend/tests/
frontend/src/
  pages/
  components/
  services/
  types/
```

Não criar camada genérica de repositórios até haver necessidade concreta. Começar com SQLAlchemy síncrono para reduzir complexidade.

## Segurança do MVP

Sem autenticação, qualquer pessoa com acesso à API poderá consultar e modificar chamados. Usar dados fictícios e ambiente local. Antes de exposição pública, implementar autenticação, autorização, proteção de configuração, política CORS restritiva e controles de operação.

## Evolução possível

Autenticação JWT, perfis, comentários, histórico, atribuição, Docker Compose, CI, observabilidade e processamento assíncrono. Cada nova stack deve ter requisito e custo documentados.

## Sprint 02 — Persistência
- `app/core/config.py`: configurações por ambiente via `pydantic-settings`.
- `app/db/session.py`: engine e sessões síncronas SQLAlchemy.
- `app/db/base.py`: base declarativa dos modelos.
- `app/models/ticket.py`: tabela `tickets` e restrições de integridade.
- `alembic/`: migrações versionadas.
- Sem endpoints de chamados até a Sprint 03.
