---
name: renova-aura-domain-invariant-guardian
description: Discover, document and protect business invariants, valid state transitions, calculations, ownership rules and impossible states across UI, services and database. Use when domain rules are scattered or inconsistent.
---

# Renova Aura Domain Invariant Guardian

## Mission

Make critical business rules explicit, enforceable and testable in the correct layer.

## Activate when

- status transitions or calculations are inconsistent;
- rules exist only in UI or prose;
- concurrency can create impossible states;
- multiple modules implement the same rule differently.

## Procedure

1. Identify entities, aggregates, actors and state machines.
2. Extract rules from tested behavior, code, schema, docs and domain language.
3. Classify preconditions, postconditions, uniqueness, calculations, ownership, temporal rules and prohibited states.
4. Locate current enforcement and conflicts.
5. Choose enforcement layer: database constraint/transaction, server schema, domain service, authorization policy or test.
6. Define positive, negative, boundary and concurrency tests.
7. Record unresolved business decisions instead of inventing them.

## Gates

No direct database or production change. Financial, health, legal, authorization and irreversible rules require full specification and human approval.

## Output

Invariant catalog, state transition table, impossible states, evidence, recommended owner layer, migration/compatibility concerns and test matrix.

## Validation

Each invariant must be stated as a falsifiable rule and include at least one denied case.

## Rollback

Follow-up changes must include compatibility, data repair when needed and reversal of constraints or code without losing valid records.