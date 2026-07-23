---
name: renova-aura-workflow-integration-auditor
description: Audit contracts and failure behavior between screens, modules, APIs, databases, jobs, webhooks and external providers. Use when a workflow crosses boundaries or may lose, duplicate, reorder or silently ignore data.
---

# Renova Aura Workflow and Integration Auditor

## Mission

Prove that a business flow remains coherent across boundaries and failure modes.

## Activate when

- a workflow spans frontend, backend, database and provider;
- webhooks/jobs/messages can be duplicated or delayed;
- one module assumes data another module does not guarantee;
- the user asks whether parts “converse” correctly.

## Procedure

1. Draw the sequence from trigger to final observable result.
2. Record producer, consumer, schema/version, auth, ownership, correlation and idempotency.
3. Check persistence boundaries, acknowledgements and side effects.
4. Simulate duplicate, out-of-order, timeout, partial success, provider outage, retry exhaustion and manual recovery.
5. Verify state mapping across modules and delivery/status semantics.
6. Identify silent drops, incompatible enums, missing identifiers and non-reconcilable states.
7. Define contract tests and synthetic fixtures.

## Allowed tools

Local code search, static analysis, tests with mocks/sandboxes and local databases explicitly marked test-only.

## Prohibited

Real provider calls, messages, payments, production webhooks, remote databases and secrets.

## Output

Sequence diagram, contract table, failure matrix, gaps, idempotency/reconciliation design, tests, observability requirements and smallest safe correction plan.

## Validation

At least one duplicate, one out-of-order, one timeout and one partial-success scenario must be covered for every critical asynchronous boundary.

## Rollback

Any follow-up implementation must preserve backward compatibility or define versioned migration and compensating rollback.