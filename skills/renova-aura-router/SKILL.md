---
name: renova-aura-router
description: Route Renova Aura work expressed in normal Portuguese to the minimum safe set of reusable skills and, only when justified, a bounded agent team. Use at the start of repository work, planning, architecture, audits, fixes, full-stack or Python work, premium front-end work, backend or database changes, security reviews, releases, incidents, performance work, prompt or skill-library maintenance, handoffs, or PDF form tasks. Inspect project evidence first and never replace applicable AGENTS.md rules.
---

# Renova Aura Router

## Mission

Understand the user's real objective, choose one primary owner, add only risk-required support, and explain the route in plain language. The user does not need to name a skill.

Default to a deterministic workflow or one specialist. Escalate to `renova-aura-agent-orchestrator` only for medium, complex, cross-domain, iterative, parallel, incident, release, or long-running work.

## Mandatory first read

Before routing, inspect when available:

1. root and nested `AGENTS.md` or override files;
2. README, current product decisions, PRD, SPEC, status, and handoff documents;
3. manifests, locks, source, migrations, tests, CI, environment examples, and deployment configuration relevant to the request;
4. branch, status, log, diff, and failures directly related to the task.

Project-local truth overrides generic assumptions. Higher-level privacy, security, authorization, and production gates still apply.

## Evidence labels

Use:

- `FACT`: directly supported;
- `HYPOTHESIS`: plausible and unverified;
- `DECISION`: selected trade-off within authority;
- `RECOMMENDATION`: proposed future action;
- `BLOCKER`: missing evidence, unsafe environment, or required approval.

## Natural-language routing

| What the user says or means | Primary owner | Add only when needed |
|---|---|---|
| "comece", "entenda", "retome de onde parou" | `renova-aura-project-bootstrap` | handoff, security, quality |
| "vale a pena?", "defina MVP/PRD/SPEC" | `renova-aura-product-spec` | architecture, UX, security |
| "desenhe/evolua a arquitetura", "torne SaaS" | `renova-aura-saas-architect` | product, security, engineering |
| "implemente", "corrija", "refatore" | `renova-aura-engineering-guardian` | domain owner, security, quality |
| "faça o backend/API/webhook/fila" | `renova-aura-backend-api-engineer` | engineering, security, database, quality |
| "revise schema/migration/query/RLS" | `renova-aura-database-reliability` | security, engineering, quality |
| "crie este projeto/serviço em Python" | `renova-aura-python-engineering` | backend, engineering, security, quality |
| "meça/melhore desempenho, bundle ou consulta" | `renova-aura-performance-engineering` | engineering, database, observability, quality |
| "faça revisão independente" | `renova-aura-independent-reviewer` | quality, relevant domain owner |
| "audite auth/RLS/tenant/API/dados/segredos" | `renova-aura-security-data-guardian` | architecture, quality |
| "melhore o fluxo/usabilidade/acessibilidade" | `renova-aura-ux-design-system` | premium front end, quality |
| "deixe premium/elegante/sofisticado" | `renova-aura-premium-frontend` | UX, quality |
| "adicione IA/agente/RAG/voz/classificação" | `renova-aura-ai-integration-guardian` | product, security, observability, quality |
| "teste/prepare PR/release/rollback" | `renova-aura-quality-release` | security, observability |
| "investigue incidente/logs/retries" | `renova-aura-observability-incident` | security, quality |
| "crie/melhore um prompt ou uma skill" | `renova-aura-prompt-source-designer` | library curator |
| "inventarie/organize/instale/publique skills" | `renova-aura-skill-library-curator` | prompt designer, quality |
| "crie/repare/valide formulário PDF" | `renova-aura-pdf-forms-router` | security for sensitive content |
| "faça handoff/status/continuação" | `renova-aura-project-handoff` | relevant domain owner |
| "monte uma equipe/use vários agentes/cada agente faz uma parte" | `renova-aura-agent-orchestrator` | minimum domain specialists and reviewer |
| "trabalhe em loop/continue por várias etapas" | `renova-aura-agent-orchestrator` | independent evaluator, handoff |

## Responsibility boundaries

- Product decides **why and what**.
- SaaS architecture decides **system boundaries and evolution**.
- Engineering owns **the implementation diff**.
- Security owns **trust, authorization, isolation, privacy, and release blockers**.
- UX owns **journeys, states, comprehension, and accessibility**.
- Premium front end owns **visual identity and expression**.
- Quality owns **validation, PR, release, and rollback evidence**.
- Prompt design owns **prompt/skill content**.
- Library curation owns **catalog, deduplication, installation, and public-safe publication**.

## Mandatory transversal triggers

Add security for authentication, sessions, roles, owner/tenant data, RLS, public APIs, uploads, webhooks, secrets, personal/sensitive data, migrations, billing, or privileged operations.

Add quality whenever code, dependencies, migrations, infrastructure, CI, deployment configuration, or production behavior changes.

Add observability for asynchronous jobs, critical writes, provider callbacks, payments, external delivery, retries, or incidents.

## Conflict precedence

Resolve conflicts by evidence and risk:

1. privacy, explicit authorization, and irreversible-action gates;
2. security and data isolation;
3. release and operational safety;
4. project-local architecture and product decisions;
5. primary domain owner;
6. UX, visual polish, growth, and convenience.

Do not activate a long mandatory chain for a small task. One primary owner remains accountable.

## Complexity and orchestration gate

- `TRIVIAL` or `SMALL`: deterministic path or `SINGLE_SPECIALIST`.
- `MEDIUM`: `SPECIALIST_PLUS_REVIEWER` when code or material judgment changes.
- `COMPLEX`: `SEQUENTIAL_PIPELINE` or bounded orchestrator-workers.
- `LONG`: incremental blocks plus persistent handoff.
- `INCIDENT` or `RELEASE`: use the matching controlled mode and human gates.

Parallel work is allowed only for independent read-only analysis or preassigned, non-overlapping files. Shared contracts, migrations, schema, identity, RLS, and dependent code remain sequential. Every loop has a distinct author/evaluator and at most three rounds by default.

## Approval gates

Stop with `NEEDS_HUMAN_APPROVAL` before destructive database/repository actions, merge/deploy, billing, real external delivery, irreversible migration, production secrets/configuration, identity/RLS/retention changes, or publication of private/proprietary information.

## Required routing output

Return task type, facts inspected, complexity, risk, primary owner, supporting skills, whether orchestration is justified, selected mode, execution order, validation order, approval gates, limits, and final state: `SAFE_TO_PLAN`, `SAFE_TO_APPLY`, `SAFE_WITH_CAUTION`, `NEEDS_HUMAN_APPROVAL`, or `BLOCKED`.

Mark skill lifecycle separately as `SELECTED`, `EXECUTED`, `NOT_APPLICABLE`, `MISSING_REFERENCE`, or `BLOCKED`. Selection is not execution.
