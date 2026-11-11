# Requisitos — Sistema de Gestão de Chamados

**Versão:** 1.1 | **Estado:** MVP definido

## Problema

Solicitações técnicas dispersas em mensagens e planilhas dificultam o acompanhamento do atendimento. O sistema centralizará o registro e a atualização dos chamados.

## Objetivo do MVP

Permitir criar, listar, consultar, editar e atualizar o status de chamados por uma interface web simples, com API Python e persistência PostgreSQL.

## Dentro do escopo

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RF01 | Criar chamado | Título, descrição e prioridade válidos; status inicial `open` |
| RF02 | Listar chamados | Ordenados do mais recente ao mais antigo, com `limit` e `offset` |
| RF03 | Consultar chamado | Busca por UUID; retorna 404 quando não existe |
| RF04 | Editar chamado | Atualização parcial de título, descrição ou prioridade |
| RF05 | Alterar status | Respeita transições permitidas; rejeita transição inválida |
| RF06 | Interface web | Permite executar RF01–RF05 e exibe erros/carregamento |
| RF07 | Testes | Cobrem validações, consultas e transições de status |

## Fora do escopo inicial

Autenticação, usuários, perfis, atribuição, comentários, anexos, notificações, dashboard avançado e exclusão de chamados.

## Campos do chamado

- `id`: UUID, gerado pelo backend
- `title`: texto obrigatório de 5 a 120 caracteres, após remoção de espaços externos
- `description`: texto obrigatório de 10 a 2000 caracteres, após remoção de espaços externos
- `priority`: `low`, `medium`, `high`; padrão `medium`
- `status`: `open`, `in_progress`, `resolved`; padrão `open`
- `created_at`, `updated_at`: timestamps com fuso, armazenados em UTC

## Transições permitidas

- `open` → `in_progress`
- `in_progress` → `resolved`
- `resolved` → `in_progress` (reabertura)

Demais transições são rejeitadas com HTTP 409. Repetir o mesmo status não deve atualizar o registro; a política exata de resposta será fixada antes da implementação da rota.

## Requisitos não funcionais

- Validação obrigatória no backend, independente do frontend.
- Mensagens de erro compreensíveis.
- Código organizado em rotas, schemas, serviços e modelos.
- Migrações versionadas do banco.
- Testes automatizados de regras importantes.
- Dados fictícios enquanto não houver autenticação e autorização.

## Definição de pronto

Uma pessoa consegue realizar todo o fluxo na interface; os dados persistem após recarregar; erros são tratados; testes passam; documentação permite executar o sistema localmente.
