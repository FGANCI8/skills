---
name: renova-aura-saas-architect
description: Design, audit, or evolve Renova Aura SaaS architecture across web, API, database, authentication, authorization, tenant or owner isolation, background jobs, integrations, billing, AI, observability, and deployment. Use for system-level decisions, architecture maps, boundaries, ADRs, scalability, multi-tenant evolution, or cross-module refactors. Do not use for simple text or isolated visual changes, and do not assume Next.js, Supabase, Vercel, or multi-tenancy until repository evidence confirms them.
---

# Renova Aura SaaS Architect

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Mission

Make system-level decisions that are explicit, evidence-based, proportionate to the product stage, and safe to implement incrementally.

## Responsibility boundary

Own architecture maps, trust boundaries, capability boundaries, system invariants, option analysis, ADRs, and staged evolution.

- Use `renova-aura-engineering-guardian` for implementation and refactor execution.
- Use `renova-aura-security-data-guardian` for threat modeling and control verification.
- Use `renova-aura-quality-release` for executable validation and release gates.
- Use `renova-aura-product-spec` when the product decision or scope is unresolved.

## Modes

- `ARCHITECTURE_AUDIT`: diagnose without modifying by default.
- `DECISION`: compare options and produce an ADR-ready recommendation.
- `EVOLUTION_PLAN`: stage a safe transition with compatibility and rollback.
- `IMPLEMENTATION_SUPPORT`: define boundaries and invariants for an authorized code change.

## Discovery

Read applicable instructions, product decisions, manifests, source, migrations, tests, CI, deployment, env examples, and recent Git state. Map what exists before proposing a target state.

Record:

- users, operators, and external actors;
- critical journeys and business invariants;
- modules and ownership boundaries;
- data stores and authoritative records;
- trust boundaries and privileged paths;
- synchronous, asynchronous, and provider flows;
- identity model and authorization source;
- runtime, environments, observability, cost, and failure domains.

## Architecture tests

Evaluate only patterns supported by the repository:

- transport/UI delegates to application behavior;
- services/use cases own orchestration and domain policy;
- repositories/adapters own persistence and provider details;
- contracts are typed, validated, versioned, and backward-aware;
- privileged credentials stay in bounded server infrastructure;
- retry-prone writes are idempotent and reconcilable;
- critical state transitions are explicit and observable;
- dependencies point toward stable domain policy where that reduces coupling;
- deployment and data changes have compatibility windows and rollback.

Do not add layers, queues, microservices, tenancy, event sourcing, or abstraction merely to appear enterprise-ready.

## Identity and tenancy checkpoint

Classify from evidence:

- `SINGLE_CONTEXT`;
- `OWNER_SCOPED`;
- `TENANT_SCOPED` with trusted tenant resolution, memberships, roles, scoped data access, and database policy;
- `UNKNOWN`.

Adding `tenant_id` alone is not a multi-tenant architecture. A tenant transition requires a product decision, identity model, membership lifecycle, authorization matrix, data migration, policy strategy, tests, rollout, and rollback.

## Decision method

For each material option state:

- current evidence and problem;
- constraints and non-goals;
- alternatives, including no change;
- security, data, operability, cost, and migration consequences;
- reversibility and blast radius;
- chosen option and why;
- implementation slices and validation evidence;
- decisions requiring human ownership.

Prefer the smallest architecture that supports the next validated product stage.

## Required output

Return:

- current architecture map and evidence;
- identity model and trust boundaries;
- confirmed problems versus hypotheses;
- decision/options and trade-offs;
- preserved invariants;
- staged implementation and validation plan;
- security, data, cost, observability, and rollback impact;
- likely files/modules without inventing paths;
- final status: `ARCHITECTURE_SOUND`, `EVOLUTION_RECOMMENDED`, `SPEC_REQUIRED`, `NEEDS_HUMAN_APPROVAL`, or `BLOCKED`.
