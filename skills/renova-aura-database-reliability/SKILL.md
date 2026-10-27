---
name: renova-aura-database-reliability
description: Design, audit, implement, or review Renova Aura database schemas, PostgreSQL or Supabase queries, constraints, indexes, transactions, migrations, RLS policies, backups, performance, and rollback. Use when data integrity, owner or tenant isolation, concurrency, migration safety, query plans, or recovery is in scope. Do not execute against a real or ambiguous database without explicit approval.
---

# Renova Aura Database Reliability

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Mission

Preserve data integrity, isolation, availability, and reversibility through evidence-based schema and query changes.

## When not to use

Do not use for transport-only API behavior, UI state, or generic architecture with no schema, query, transaction, policy, migration, recovery, or database-performance surface. Do not infer database access merely because an application stores data.

## Entry gate

Read local instructions, canonical schema and migration history, application queries, RLS or authorization policy, tests, environment configuration, backup assumptions, and release constraints. Classify the database as isolated disposable, local shared, staging, production, or unknown. Treat `unknown` as blocked for writes.

## Workflow

1. State the invariant or failure being addressed and the current evidence.
2. Map tables, keys, constraints, ownership or tenant predicates, transactions, and dependent code.
3. Design the smallest forward-compatible change, including nullability, defaults, foreign keys, indexes, locks, backfill, and compatibility window.
4. Create a new migration; never edit an already published migration.
5. Analyze transaction isolation, concurrent writes, partial failure, retry, and rollback.
6. Verify RLS and application filtering for select, insert, update, and delete separately when applicable.
7. Test upgrade and safe recovery only in explicitly isolated disposable infrastructure.
8. Measure query plans or timing before adding a performance optimization.
9. Prepare release order, monitoring, rollback trigger, and human gate.

## Reliability rules

- Prefer constraints for durable integrity and application validation for clear errors.
- Add indexes for demonstrated filters, joins, uniqueness, foreign keys, or RLS predicates.
- Separate expand, backfill, switch, and contract phases when compatibility matters.
- Do not use destructive rollback that would erase valid new writes.
- Treat cross-owner or cross-tenant access as a release blocker.
- Do not run migrations, containers, or database commands when the user authorized only design or audit.

## Human approval

Require approval before real database access, production or shared-environment migration, destructive SQL, irreversible backfill, RLS or identity change, backup restore, retention/deletion change, or accepting downtime.

## Validation and output

Validate SQL/migration syntax with project tools, constraints and negative cases, authorization isolation, upgrade/rollback in disposable infrastructure, query plan where relevant, and application compatibility. Use [references/evals.md](references/evals.md).

Return current model, invariant, proposed diff, lock/backfill/index analysis, tests and literal results, environment, security impact, rollout, rollback, and status: `DESIGN_READY`, `SAFE_IN_ISOLATED_TEST`, `NEEDS_HUMAN_APPROVAL`, or `BLOCKED`.
