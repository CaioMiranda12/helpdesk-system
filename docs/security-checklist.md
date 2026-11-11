# Checklist de segurança — Helpdesk System

- [ ] Credenciais reais apenas em `.env` ou gerenciador de segredos
- [ ] JWT_SECRET_KEY aleatória com pelo menos 32 caracteres
- [ ] HTTPS e origem CORS explícita no deploy público
- [ ] `APP_ENVIRONMENT=production` no deploy público
- [ ] `npm audit` e `npm audit --omit=dev` revisados
- [ ] Dependências Python revisadas e atualizadas com testes
- [ ] Proteção contra força bruta no login (pendente)
- [ ] Política CSP e revisão de XSS (pendente)
- [ ] Política de armazenamento/revogação de JWT (pendente)
- [ ] Backup e restauração do PostgreSQL testados (pendente)
- [ ] Logs sem segredos, monitoramento e alertas (pendente)
- [ ] Limites de requisições e proteção de infraestrutura (pendente)

Este checklist diferencia o ambiente local de demonstração de um serviço seguro para acesso público.
