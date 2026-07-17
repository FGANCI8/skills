---
name: renova-aura-quality-release
description: Plan and execute risk-based validation, CI, pull request, release, deploy, and rollback for Renova Aura projects. Use whenever code, dependencies, migrations, infrastructure, external integrations, or production behavior changes.
---

# Renova Aura Quality and Release

## Mission

Produce evidence that a change is correct enough for its risk and can be safely reviewed, released and reversed. Never equate compilation with product, security or operational correctness.

## Change inventory

Before validation, identify:

- user-visible behavior changed;
- modules, APIs, schemas and migrations touched;
- auth, ownership/tenant, sensitive data or privileged operations affected;
- external providers and side effects;
- environment and deployment target;
- rollback mechanism;
- unrelated changes that must stay outside the release.

## Risk levels

- `LOW`: documentation, copy or isolated reversible UI change.
- `MEDIUM`: bounded application behavior, API contract or internal refactor.
- `HIGH`: auth, roles, RLS, database structure, billing, external delivery, background jobs, AI in production, sensitive data or infrastructure.
- `CRITICAL`: credible isolation failure, destructive migration, production data risk, secret exposure or safety-policy breach.

Higher risk requires deeper evidence and explicit approval.

## Validation pyramid

Choose repository-defined commands and run the smallest sufficient set in this order:

1. diff/format integrity;
2. lint or static analysis;
3. typecheck or compilation;
4. focused unit tests;
5. isolated integration/contract tests;
6. migration tests in disposable infrastructure;
7. browser/E2E or provider-sandbox tests;
8. production build;
9. security/dependency checks interpreted by policy.

Report each as `PASS`, `FAIL`, `NOT RUN` or `BLOCKED`. Include the command and relevant result. Do not hide pre-existing failures; separate them from regressions introduced by the change.

## Required negative tests

Add denied and failure cases when applicable:

- unauthenticated and unauthorized access;
- cross-owner or cross-tenant access;
- invalid and oversized input;
- duplicate submit or webhook replay;
- timeout, provider failure and out-of-order callback;
- stale version or concurrent update;
- migration rollback or partial rollout;
- empty, error and session-expired UI states.

## CI expectations

CI should be deterministic and avoid real production dependencies. Prefer:

- pinned runtime/dependency behavior;
- isolated ephemeral databases;
- synthetic fixtures;
- secret scanning;
- no real WhatsApp, payment, email or AI calls;
- clear required checks;
- artifact or report retention only when useful and safe.

A green CI run proves only the checks configured for that commit.

## Release plan

Define:

- branch and PR scope;
- release order for app, database and configuration;
- compatibility window between old and new versions;
- feature flag or dark launch when risk warrants it;
- migration preflight and backup assumptions;
- smoke tests after deployment;
- metrics/logs to watch;
- rollback trigger and exact rollback path;
- owner of the release decision.

Do not deploy, merge or enable production integrations without explicit authorization.

## Database release rules

- use forward-compatible migrations when possible;
- separate schema expansion, backfill and contract removal;
- estimate locks and long-running operations;
- do not edit published migrations;
- test against an isolated database;
- avoid rollback instructions that would destroy newly written data;
- require human review for destructive or irreversible changes.

## PR quality

A draft PR should state:

- what changed and why;
- files/modules affected;
- architecture and security impact;
- validation table;
- screenshots or evidence for UI changes;
- migration and rollback;
- known gaps and `NOT RUN` items;
- explicit non-goals.

## Final verdict

Return one:

- `SAFE_TO_REVIEW`;
- `SAFE_TO_RELEASE_WITH_APPROVAL`;
- `STABILIZE_BEFORE_RELEASE`;
- `BLOCKED`;
- `UNSAFE`.

Include the evidence that drives the verdict and the smallest next action.
