---
name: renova-aura-backend-api-engineer
description: Design, implement, review, or debug Renova Aura backend services, APIs, server actions, webhooks, queues, and provider adapters. Use for HTTP or event contracts, server validation, authorization integration, idempotency, concurrency, retries, error semantics, and backend tests in the stack detected from the repository. Use renova-aura-python-engineering when Python is dominant and renova-aura-database-reliability for schema or migration ownership.
---

# Renova Aura Backend and API Engineer

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Mission

Deliver a narrow, testable backend slice whose contract, authority, failure behavior, and side effects are explicit.

## When not to use

Do not use for a UI-only change, schema- or migration-only ownership, a system-level architecture decision, or Python-dominant work already owned by the corresponding specialist. Do not activate it for documentation or copy edits with no backend contract.

## Boundary

Own transport and application-service behavior. Use:

- `renova-aura-engineering-guardian` for the implementation diff and architecture discipline;
- `renova-aura-security-data-guardian` for authentication, authorization, isolation, abuse, or sensitive data;
- `renova-aura-database-reliability` for schema, queries, migrations, transactions, or RLS;
- `renova-aura-python-engineering` when Python is the dominant runtime;
- `renova-aura-observability-incident` for critical asynchronous or provider flows.

Do not infer FastAPI, Next.js, queues, or a provider before inspecting the repository.

## Workflow

1. Read local instructions, accepted spec, callers, contracts, services, persistence, tests, configuration, and recent diff.
2. Map trusted identity, authorization source, data ownership, external side effects, and failure boundaries.
3. Define request, response, event, and error schemas with compatibility requirements.
4. Validate input server-side and derive identity or scope from trusted state.
5. Keep domain orchestration outside transport handlers and providers behind explicit adapters.
6. Bound payloads, pagination, time, concurrency, retries, and spend.
7. Add idempotency and reconciliation when retries can duplicate effects.
8. Implement the smallest vertical slice and test success, denial, invalid input, duplicate, timeout, and provider failure.
9. Record observability without secrets or unnecessary payloads.

## Contract quality bar

- Stable status and error semantics.
- Object, property, and function authorization where applicable.
- Safe mass-assignment behavior and closed schemas.
- Explicit transaction boundaries; no provider call hidden inside a long database transaction.
- Backward compatibility or a staged migration plan.
- Correlation and terminal-state evidence for async work.
- No real provider call, message, charge, or production mutation in validation.

## Approval gates

Stop before changing public compatibility, identity or authorization semantics, privileged provider configuration, real external delivery, production data, or an irreversible operation.

## Validation and output

Run repository-defined lint/typecheck/compile, focused units, contract/integration tests in an isolated environment, and relevant negative cases. Use [references/evals.md](references/evals.md).

Return current contract, invariants, files changed, schemas, side effects, validation results, security/data impact, rollback, and status: `READY_TO_IMPLEMENT`, `SAFE_TO_REVIEW`, `NEEDS_HUMAN_APPROVAL`, or `BLOCKED`.
