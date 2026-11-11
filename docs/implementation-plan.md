# Plano de implementação

## Sprint 01 — Ambiente e primeira API

- [ ] Criar repositório e estrutura de diretórios.
- [ ] Criar ambiente virtual Python.
- [ ] Instalar dependências de `backend/requirements.txt`.
- [ ] Executar `python -m uvicorn app.main:app --reload` dentro de `backend`.
- [ ] Verificar `/health` e `/docs`.
- [ ] Executar `python -m pytest -q` dentro de `backend`.
- [ ] Registrar primeiro commit.

**Aceite:** `/health` retorna `200` e `{"status":"ok"}`; teste automatizado passa.

## Sprint 02 — Persistência

- [ ] Configurar PostgreSQL e `DATABASE_URL`.
- [ ] Adicionar SQLAlchemy, driver PostgreSQL e Alembic.
- [ ] Criar modelo `Ticket`.
- [ ] Gerar e aplicar migration inicial.
- [ ] Verificar tabela e conexão.

**Aceite:** tabela `tickets` criada por migration e acessível pelo backend.

## Sprint 03 — Criação e leitura

- [ ] Criar schemas Pydantic de entrada e saída.
- [ ] Implementar `POST /api/v1/tickets`.
- [ ] Implementar `GET /api/v1/tickets` com paginação.
- [ ] Implementar `GET /api/v1/tickets/{id}`.
- [ ] Testar sucesso, validações e `404`.

**Aceite:** criar, listar e consultar chamados no Swagger.

## Sprint 04 — Edição e regras

- [ ] Implementar edição parcial.
- [ ] Implementar atualização de status.
- [ ] Aplicar e testar transições válidas e inválidas.
- [ ] Garantir que `updated_at` reflita alterações reais.

**Aceite:** API mantém consistência das regras de negócio.

## Sprint 05 — Frontend

- [ ] Inicializar React + TypeScript + Vite.
- [ ] Criar lista, formulário e página de detalhes.
- [ ] Integrar endpoints via Axios.
- [ ] Adicionar loading, mensagens de erro e sucesso.
- [ ] Validar fluxo completo no navegador.

**Aceite:** uso completo pela interface sem recorrer ao Swagger.

## Sprint 06 — Qualidade e apresentação

- [ ] Revisar testes e documentação.
- [ ] Demonstrar cenário de bug e sua correção.
- [ ] Preparar instruções de execução.
- [ ] Revisar README, screenshots e histórico de commits.

**Aceite:** outro desenvolvedor consegue executar e entender o projeto.
