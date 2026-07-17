---
name: renova-aura-engineering-guardian
description: Govern implementation and refactoring across Renova Aura repositories. Use for code changes, focused architecture enforcement, service/repository boundaries, API contracts, migrations, integrations, performance, or technical-debt reduction. Use renova-aura-saas-architect for system-level architecture decisions and keep this skill accountable for the smallest correct implementation diff.
---

# Renova Aura Engineering Guardian

## Mission

Make the smallest correct change that preserves project architecture, contracts, security and operability. Repository evidence and local instructions are authoritative.

For system-wide target-state decisions, identity-model evolution, or cross-module architecture options, obtain the decision from `renova-aura-saas-architect` before implementation.

## Before editing

1. Read applicable `AGENTS.md` and project decisions.
2. Inspect the exact code path, callers, tests, migrations and configuration.
3. Determine current architecture from evidence; do not assume a preferred stack.
4. Identify invariants, trust boundaries and external side effects.
5. Check branch, diff and unrelated work when repository state is available.
6. Consult current official documentation for unstable external APIs or library behavior.

## Architecture principles

Apply only where they fit the project:

- UI or transport layers validate and delegate; they do not own domain rules.
- Services/use cases own orchestration and business behavior.
- Repositories own persistence access, not business policy.
- External providers are behind explicit ports/adapters.
- Domain contracts are typed, validated and versioned when externally consumed.
- Cross-cutting concerns such as auth, logging, rate limiting and idempotency are centralized enough to be consistently enforced.

Do not perform architecture theater. A new abstraction must reduce coupling, duplication, risk or test difficulty.

## Change discipline

- Preserve public contracts unless the spec authorizes a migration.
- Prefer vertical, reviewable slices.
- Do not combine feature work, broad cleanup and dependency upgrades without need.
- Never conceal failure by weakening validation, auth, RLS, tests or types.
- Do not use forceful auto-fix commands without understanding the diff.
- Do not edit published migrations; create a new migration.
- Do not use `git add .` when unrelated changes may exist.
- Keep comments for intent, invariants, non-obvious tradeoffs and safety boundaries; remove narration of obvious code.

## Contract review

For APIs, events, jobs and integrations, verify:

- schema and server-side validation;
- authentication and authorization;
- ownership or tenant context derived from trusted state;
- idempotency and duplicate handling;
- timeout, retry and terminal failure semantics;
- safe errors and response shapes;
- backwards compatibility or migration plan;
- observability and correlation IDs;
- provider calls isolated from persistence transactions when appropriate.

## Database review

When data changes:

- identify source-of-truth schema and migration head;
- specify constraints, defaults, nullability, foreign keys and indexes;
- assess lock, backfill, downtime and rollback;
- preserve ownership/tenant filters and RLS where applicable;
- test on an explicitly isolated disposable database;
- never delete production data or volumes without approval.

## Performance review

Measure or reason from concrete hotspots. Check:

- N+1 queries and unnecessary round trips;
- missing indexes for common filters, joins and RLS predicates;
- oversized public payloads;
- unbounded list endpoints and background jobs;
- repeated provider calls;
- client bundles and rendering boundaries;
- caching that could violate authorization or freshness.

Do not optimize speculative paths at the cost of clarity.

## Validation matrix

Select relevant checks from repository scripts and stack:

- formatting/diff check;
- lint/static analysis;
- typecheck or compilation;
- focused unit tests;
- isolated integration tests;
- contract/webhook/idempotency tests;
- migration upgrade/downgrade where safe;
- production build;
- targeted browser/E2E validation.

Report `PASS`, `FAIL`, `NOT RUN` or `BLOCKED` literally. A build does not prove authorization, data isolation or runtime correctness.

## Required delivery

- objective and root cause/context;
- current architecture and preserved invariants;
- files changed and why;
- validations with exact results;
- security, data and performance impact;
- rollback procedure;
- residual risks and next smallest safe action.
