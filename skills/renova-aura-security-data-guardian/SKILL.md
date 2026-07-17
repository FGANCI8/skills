---
name: renova-aura-security-data-guardian
description: Protect Renova Aura applications that handle authentication, authorization, owner or tenant scoped data, RLS, uploads, public APIs, webhooks, secrets, personal data, migrations, or privileged operations. Use for design, audit, implementation, and release gates.
---

# Renova Aura Security and Data Guardian

## Mission

Preserve confidentiality, integrity, availability, privacy and isolation through defense in depth. Never infer that a system is multi-tenant, owner-scoped or single-user; determine the implemented identity model first.

## Identity model checkpoint

Classify the current project from evidence:

- `SINGLE_CONTEXT`: one trusted operator or one isolated installation;
- `OWNER_SCOPED`: records belong directly to an authenticated owner/user;
- `TENANT_SCOPED`: organizations/accounts contain memberships, roles and tenant-scoped records;
- `UNKNOWN`: evidence is insufficient; block security-sensitive implementation.

Do not add `tenant_id` merely to appear enterprise-ready. Do not call an owner-scoped system tenant-safe. Do not accept client-provided owner, tenant or role context without server verification.

## Threat surface review

Inspect as applicable:

- login, sessions, password reset and OAuth callbacks;
- middleware, server actions, route handlers and APIs;
- roles, permissions, admin/founder paths and support tooling;
- database queries, repositories, RLS policies and privileged clients;
- public search, detail pages, scraping and enumeration risk;
- uploads, storage buckets, signed URLs and metadata;
- webhooks, signatures, replay and idempotency;
- logs, analytics, error reporting and audit trails;
- secrets, env variables, build output and client bundles;
- background jobs, queues, retries and external providers.

## Mandatory controls

- Validate inputs on the server with closed schemas.
- Authenticate before protected access.
- Authorize every sensitive action server-side.
- Derive identity and scope from trusted session/membership state.
- Apply repository filters and database policies consistently.
- Use least privilege for service accounts and privileged database clients.
- Keep secrets out of source, logs, prompts, screenshots and browser code.
- Minimize returned fields and public payloads.
- Rate-limit abuse-prone endpoints using a durable strategy appropriate to deployment.
- Make retry-prone mutations and webhooks idempotent.
- Record security-relevant mutations without storing unnecessary sensitive content.

## RLS and database isolation

When PostgreSQL/Supabase RLS applies:

1. Inventory scoped tables and ownership keys.
2. Verify RLS is enabled and forced where the project requires it.
3. Inspect SELECT, INSERT, UPDATE and DELETE policies separately.
4. Ensure policy predicates match application ownership semantics.
5. Check joins, functions, views, RPCs and storage policies.
6. Verify indexes support ownership and policy predicates.
7. Test authorized, unauthorized and cross-scope cases with synthetic identities.
8. Treat any credible cross-tenant or cross-owner path as a release blocker.

Never weaken RLS to make a failing request pass. Privileged keys must remain server-only and narrowly bounded.

## LGPD and sensitive data

Identify purpose, legal/operational need, collection, retention, access and deletion behavior for personal data. Apply:

- data minimization;
- purpose limitation;
- redaction or hashing where full values are unnecessary;
- explicit retention decisions for messages, payloads, logs and AI traces;
- synthetic data in tests and documentation;
- controlled export/delete workflows when the product requires them;
- special caution for health, financial, legal, precise-location and communication content.

Do not promise legal compliance from a code review alone; report technical controls and unresolved governance decisions separately.

## External integrations

For WhatsApp, payments, email, AI or other providers, verify:

- current official API contract and version;
- signature or token verification;
- secret rotation and storage;
- timeout and retry boundaries;
- duplicate and out-of-order event handling;
- provider status reconciliation;
- safe fallback and human escalation;
- no real message, charge or external mutation without explicit authorization.

## Approval gates

Return `NEEDS_HUMAN_APPROVAL` before changing:

- auth/session semantics;
- role or admin authority;
- owner/tenant model;
- RLS or privileged access;
- retention/deletion policy;
- encryption/key strategy;
- production secrets or provider configuration;
- destructive database operations.

## Required report

- identity model and evidence;
- trust boundaries and sensitive data map;
- findings with severity and concrete file/policy evidence;
- exploit or failure path without speculative exaggeration;
- recommended minimal remediation;
- tests executed and gaps;
- release verdict: `SAFE`, `SAFE_WITH_CAUTION`, `STABILIZE_BEFORE_RELEASE` or `UNSAFE`.
