# Helpdesk System — roteiro de portfólio

## Resumo (30 segundos)
Sistema de gestão de chamados desenvolvido para praticar manutenção e evolução de uma aplicação full-stack. Backend em FastAPI com PostgreSQL e SQLAlchemy; frontend em React e TypeScript. Inclui autenticação JWT, perfis admin/agente, atribuição de responsáveis, comentários, histórico paginado e dashboard.

## Demonstração sugerida (5 minutos)
1. Entre como administrador e apresente o dashboard.
2. Filtre chamados por status, prioridade e texto.
3. Crie um chamado e atribua um agente.
4. Atualize status, escreva comentário e mostre a linha do tempo.
5. Demonstre a diferença entre permissões de administrador e agente.
6. Abra Swagger e explique os contratos da API.
7. Mostre `alembic/versions`, testes Pytest e testes React.

## Decisões técnicas para explicar
- **FastAPI/Pydantic:** validação de entrada e contrato HTTP.
- **SQLAlchemy/Alembic:** persistência e evolução controlada do esquema.
- **PostgreSQL:** filtros e agregações feitos no banco; índice para histórico.
- **React/TypeScript:** interface tipada e separação de páginas, componentes e serviços.
- **Testes:** Pytest para backend e Vitest + Testing Library para componentes.
- **Permissões:** validação real no servidor, não apenas ocultação de links no frontend.

## Limitações atuais — mencionar com transparência
- MVP educacional, não pronto para produção.
- Sem recuperação de senha por e-mail, limitação de tentativas de login ou revogação centralizada de tokens.
- Testes de frontend são unitários/de componentes; não há suíte E2E.
- Sem deploy público configurado por esta sprint.

## Capturas de tela sugeridas
Salve capturas **suas** em `docs/screenshots/` (não incluídas automaticamente): `login.png`, `dashboard.png`, `tickets.png`, `ticket-detail.png`, `users.png`. Remova nomes, e-mails e outros dados pessoais antes de publicar.

## Checklist antes de compartilhar no GitHub
- [ ] `git status` limpo e branch `master` atualizada.
- [ ] Nenhum `.env`, senha, token ou dado pessoal versionado.
- [ ] README descreve a versão atual.
- [ ] `npm test`, `npm run build` e `python -m pytest -q` passam.
- [ ] Capturas reais sem dados sensíveis.
- [ ] Consigo explicar a arquitetura e as principais regras de negócio.
