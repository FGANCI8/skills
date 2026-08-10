# Renova Aura Agent Catalog

All 18 definitions use schema V1.1, inherit `RA-AUTH-BASELINE-1`, reference the
central deny-by-default tool policy, and declare typed approval-gated actions.
Their free-text handoff/input fields never grant authority. Real provider
execution is hard-forbidden in V1.1.

| Agente | Responsabilidade | Skills canônicas |
|---|---|---|
| `technical-director-orchestrator` | equipe, dependências, limites e integração | router, agent-orchestrator, handoff |
| `product-requirements-analyst` | problema, MVP, requisitos e aceite | product-spec |
| `saas-architect` | limites, identidade e evolução | saas-architect, security |
| `premium-frontend-specialist` | identidade visual e composição | premium-frontend, UX, engineering |
| `ux-accessibility-specialist` | jornada, estados e acessibilidade | UX, quality |
| `backend-api-engineer` | serviços, APIs, webhooks e filas | backend-api, engineering, security |
| `database-data-engineer` | schema, migrations, queries e rollback | database-reliability, security, quality |
| `appsec-specialist` | threat model, auth, isolamento e dados | security-data-guardian |
| `quality-test-engineer` | estratégia e evidência de testes | quality-release |
| `independent-technical-reviewer` | revisão adversarial de diff e evidência | independent-reviewer, quality |
| `independent-visual-evaluator` | crítica visual objetiva | independent-reviewer, premium, UX |
| `performance-engineer` | medição e otimização | performance, observability, quality |
| `platform-release-engineer` | Git, CI, PR, ambientes e rollback | quality-release, observability |
| `observability-incident-engineer` | sinais, contenção e recuperação | observability, security |
| `ai-automation-specialist` | agentes, automações, schemas e evals | AI guardian, security, observability |
| `python-engineer` | Python, typing, Pydantic, async e packaging | Python engineering, engineering |
| `documentation-handoff-specialist` | estado real e continuidade | project-handoff |
| `skills-agents-prompts-curator` | catálogo, deduplicação, instalação e publicação | curator, prompt designer |

Os arquivos em `definitions/` são a fonte de tool IDs, leitura, escrita, proibições, risco, conclusão, handoffs e subteto de rodadas de cada papel. `renova-aura-team.yaml` e `operating-records.schema.json` são as fontes de autoridade, limites cumulativos, approval, ownership e métricas.
