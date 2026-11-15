# Sprint 19 — Etapa 1 corrigida

Aplicar este ZIP na raiz de `helpdesk-system`, preservando as pastas.

Correções:
- UUID fixo para o mesmo usuário nos testes de rate limit de IA.
- Limpeza do limitador no início e fim de cada fixture de autenticação.

Testes (a partir da pasta backend):
` .\.venv\Scripts\python.exe -m pytest tests/test_rate_limit.py -q `
` .\.venv\Scripts\python.exe -m pytest -q `

Não inclui .env, .venv, .git ou arquivos compilados.

Validação em ambiente isolado: 71 testes passaram. O ambiente de validação usou um stub local para a importação do SDK Groq (sem chamadas externas); repita os testes no ambiente do projeto.
