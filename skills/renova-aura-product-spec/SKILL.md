---
name: renova-aura-product-spec
description: Turn a Renova Aura product idea or requested feature into a validated problem statement, MVP decision, PRD, technical SPEC, backlog, acceptance criteria, metrics, risks, and explicit defer or do-not-build choices.
---

# Renova Aura Product and Spec

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Mission

Prevent premature construction. Convert ideas into evidence-based product decisions and executable specifications that a solo developer can deliver safely.

## Decision frame

Evaluate in this order:

1. **Problem**: what concrete pain exists and how it is handled today?
2. **User**: who experiences the pain, operates the solution and pays?
3. **Value**: what measurable result improves?
4. **Evidence**: what is fact, customer report, repository evidence or assumption?
5. **Viability**: legal, operational, commercial and support constraints.
6. **Feasibility**: stack, integrations, data, security, time and cost.
7. **Risk**: privacy, safety, abuse, lock-in, reliability and irreversible choices.
8. **Scope**: what is the smallest useful, testable release?

## Mandatory product choices

Classify every proposed capability:

- `EXECUTAR AGORA`: essential to prove value or operate safely;
- `PLANEJAR`: valuable but not required for the current proof;
- `ARQUIVAR`: duplicate, premature, low-value or unsupported by evidence;
- `DO_NOT_BUILD`: unsafe, legally problematic, economically irrational or outside product identity.

Challenge feature accumulation. Prefer one complete critical flow over many shallow screens.

## PRD minimum

A PRD must include:

- context and problem statement;
- target user and operator;
- desired outcome and non-goals;
- current product decisions and constraints;
- user journey and critical paths;
- functional requirements;
- non-functional requirements;
- roles and permissions;
- data handled and sensitivity;
- integrations and failure modes;
- analytics and success metrics;
- rollout, support and rollback assumptions;
- open decisions and owners.

Do not state future features as implemented behavior.

## Technical SPEC minimum

For material changes, define:

- current-state evidence and affected files/modules;
- proposed behavior and invariants;
- architecture boundaries and contracts;
- request/response or event schemas;
- database changes, constraints, indexes and migration strategy;
- auth, authorization, ownership/tenant and RLS behavior;
- server-side validation and idempotency;
- logs, metrics and audit requirements;
- error, retry, timeout and fallback behavior;
- test matrix;
- rollout, feature flag and rollback;
- acceptance criteria traceable to requirements.

## Risk-based spec depth

- `DIRECT_PROMPT`: copy, styling or bounded content with no data/security impact.
- `LIGHT_SPEC`: isolated behavior with known contracts and reversible changes.
- `FULL_SPEC`: database, auth, RLS, roles, billing, AI, external provider, production, clinical/legal data or irreversible workflow.

A full spec always carries basal approval gates for critical implementation. Database, auth, RLS, roles, billing, a real provider, production, external delivery, sensitive clinical/legal data or irreversible workflow cannot proceed merely because local instructions are silent or permissive. Project instructions may require additional approval but never remove this requirement.

## Acceptance criteria discipline

Use observable outcomes. Each criterion must state:

- precondition;
- action;
- expected result;
- denied or failure case when relevant;
- evidence required: test, screenshot, log, query or build result.

Avoid criteria such as “works well”, “secure”, “modern” or “responsive” without measurable evidence.

## Metrics

Choose a small metric set:

- one primary outcome metric;
- leading activation or adoption metric;
- reliability or quality guardrail;
- cost guardrail;
- safety/privacy guardrail when applicable.

Do not invent targets without baseline or business approval. Label suggested targets as hypotheses.

## Backlog output

Break work into vertical slices with:

- user or operational value;
- scope and dependencies;
- owner/module;
- risk level;
- acceptance criteria;
- validation command or evidence;
- rollback note;
- explicit out-of-scope items.

## Final response

Deliver in `EXECUTAR AGORA / PLANEJAR / ARQUIVAR`, followed by a copyable technical execution prompt when implementation is the next safe step.
