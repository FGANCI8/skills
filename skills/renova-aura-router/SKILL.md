---
name: renova-aura-router
description: Route Renova Aura work expressed in normal Portuguese to the minimum safe set of reusable skills without requiring users to know skill names or technical commands. Use at the start of repository work, planning, architecture, audits, fixes, premium front-end work, security reviews, releases, incidents, prompt or skill-library maintenance, handoffs, or PDF form tasks. Inspect project evidence first and never replace applicable AGENTS.md rules.
---

# Renova Aura Router

## Mission

Understand the user's real objective, choose one primary owner, add only risk-required support, and explain the route in plain language. The user does not need to name a skill.

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
| "audite auth/RLS/tenant/API/dados/segredos" | `renova-aura-security-data-guardian` | architecture, quality |
| "melhore o fluxo/usabilidade/acessibilidade" | `renova-aura-ux-design-system` | premium front end, quality |
| "deixe premium/elegante/sofisticado" | `renova-aura-premium-frontend` | UX, quality |
| "adicione IA/agente/RAG/voz/classificação" | `renova-aura-ai-integration-guardian` | product, security, observability, quality |
| "teste/prepare PR/release/rollback" | `renova-aura-quality-release` | security, observability |
| "investigue incidente/logs/retries" | `renova-aura-observability-incident` | security, quality |
| "crie/melhore um prompt ou uma skill" | `renova-aura-prompt-source-designer` | library curator |
| "inventeie/organize/instale/publique skills" | `renova-aura-skill-library-curator` | prompt designer, quality |
| "crie/repare/valide formulário PDF" | `renova-aura-pdf-forms-router` | security for sensitive content |
| "faça handoff/status/continuação" | `renova-aura-project-handoff` | relevant domain owner |

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

## Approval gates

Stop with `NEEDS_HUMAN_APPROVAL` before destructive database/repository actions, merge/deploy, billing, real external delivery, irreversible migration, production secrets/configuration, identity/RLS/retention changes, or publication of private/proprietary information.

## Required routing output

Return task type, facts inspected, primary owner, supporting skills, execution order, validation order, approval gates, and final state: `SAFE_TO_PLAN`, `SAFE_TO_APPLY`, `SAFE_WITH_CAUTION`, `NEEDS_HUMAN_APPROVAL`, or `BLOCKED`.

Mark skill lifecycle separately as `SELECTED`, `EXECUTED`, `NOT_APPLICABLE`, `MISSING_REFERENCE`, or `BLOCKED`. Selection is not execution.
