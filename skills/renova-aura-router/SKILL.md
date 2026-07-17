---
name: renova-aura-router
description: Route Renova Aura product and engineering work to the minimum safe set of reusable skills. Use at the start of repository work, feature planning, audits, fixes, releases, incidents, document/PDF artifact work, or prompt-library changes. Inspect project evidence first and never replace project-specific AGENTS.md rules.
---

# Renova Aura Router

## Mission

Classify the real task, inspect the project sources of truth, select one primary skill and only the supporting skills required by risk.

## Mandatory first read

Before routing, inspect when available:

1. root and nested `AGENTS.md` files;
2. README, PRD, SPEC, decisions and current-status documents;
3. package manifests, dependency locks and runtime versions;
4. source code, migrations, tests, CI, env examples and deployment configuration;
5. recent branch, status, log and diff when repository access exists;
6. logs or failures directly related to the request.

Project-local instructions override this generic skill. Historical notes do not override implemented code, migrations and tests unless the project explicitly says otherwise.

## Evidence labels

For every material statement, distinguish:

- `FACT`: directly supported by repository or runtime evidence;
- `HYPOTHESIS`: plausible but not yet verified;
- `RECOMMENDATION`: proposed action or design choice;
- `BLOCKER`: missing evidence, unsafe environment or required approval.

## Task classification

Choose the dominant task type:

- product discovery or prioritization;
- bootstrap or project recovery;
- PRD, SPEC or acceptance criteria;
- architecture or refactor;
- security, identity, isolation or data protection;
- UI, UX or design system;
- AI feature or agent workflow;
- database, migration or data integrity;
- API, webhook or external integration;
- testing, CI, release or deploy;
- observability, incident or rollback;
- prompt or skill library maintenance;
- PDF form creation, repair, compatibility or auditable delivery;
- documentation and handoff.

## Routing table

| Intent or risk | Primary skill | Add when needed |
|---|---|---|
| Start or resume a project | `renova-aura-project-bootstrap` | security, product-spec, quality-release |
| Validate idea, MVP or roadmap | `renova-aura-product-spec` | UX, AI, security |
| Architecture, coupling or refactor | `renova-aura-engineering-guardian` | security, quality-release |
| Auth, RBAC, RLS, tenant, privacy, secrets | `renova-aura-security-data-guardian` | engineering, quality-release |
| UI flow, visual system, responsive behavior | `renova-aura-ux-design-system` | product-spec, quality-release |
| LLM, agent, RAG, classifier or AI automation | `renova-aura-ai-integration-guardian` | security, observability, quality-release |
| Tests, CI, PR, release, deploy | `renova-aura-quality-release` | security, observability |
| Logs, metrics, alerts, outage, recovery | `renova-aura-observability-incident` | quality-release, security |
| Create or improve prompts/skills | `renova-aura-prompt-source-designer` | project-handoff |
| Create, repair, validate or package fillable PDFs | `renova-aura-pdf-forms-router` | security-data for sensitive documents; quality-release when code/scripts change |
| Update status and continuity docs | `renova-aura-project-handoff` | relevant domain skill |

## Mandatory transversal triggers

Always add `renova-aura-security-data-guardian` when touching:

- authentication, sessions, roles, admin or permissions;
- owner or tenant scoped data;
- RLS, service-role credentials or privileged APIs;
- personal, financial, clinical, legal or location data;
- public APIs, uploads, webhooks, rate limits or secrets;
- database deletion, migration, backfill or production data.

Always add `renova-aura-quality-release` when code, migrations, dependencies, CI, deploy configuration or production behavior changes.

Always add `renova-aura-observability-incident` for critical writes, asynchronous jobs, external providers, payments, WhatsApp delivery, retries, background processing or production incidents.

## Scope control

- Select one primary owner.
- Add supporting skills only for explicit cross-cutting risks.
- Do not activate the entire catalog by default.
- Do not broaden a small fix into a platform refactor.
- Do not copy owner-scoped rules into tenant-scoped systems or the inverse.
- Do not assume Next.js, Supabase, Python, FastAPI, Vercel or any provider until detected.

## Approval gates

Stop with `NEEDS_HUMAN_APPROVAL` before:

- destructive database or repository operations;
- production deploy, merge, billing or irreversible migration;
- enabling real AI, WhatsApp, payment or external-message delivery;
- changing identity, authorization, RLS, clinical safety or retention policy;
- exposing private data or moving proprietary instructions into a public repository.

## Required routing output

Return:

1. task type;
2. facts inspected;
3. primary skill;
4. supporting skills;
5. execution order;
6. validation order;
7. approval gates;
8. final state: `SAFE_TO_PLAN`, `SAFE_TO_APPLY`, `SAFE_WITH_CAUTION`, `NEEDS_HUMAN_APPROVAL` or `BLOCKED`.

Mark each selected skill as `SELECTED`, then update to `EXECUTED`, `NOT_APPLICABLE`, `MISSING_REFERENCE` or `BLOCKED` only after evaluation.
