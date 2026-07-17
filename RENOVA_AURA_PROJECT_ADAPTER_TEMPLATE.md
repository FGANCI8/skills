# Renova Aura — Project Adapter Template

Copy this file into a project and adapt it as `AGENTS.md` or as a normative document referenced by `AGENTS.md`.

Do not keep placeholders after adoption. Do not copy facts from another project without verification.

```markdown
# AGENTS.md — [PROJECT NAME]

## 1. Purpose and current product limits

- Product purpose: [what it does]
- Current target user/operator: [who]
- Current scope: [implemented/approved boundaries]
- Explicit non-goals: [what this project is not]
- Product decisions source: `[path]`

## 2. Sources of truth and precedence

Before editing, read:

1. this file;
2. `[README path]`;
3. `[approved decisions / product foundation]`;
4. `[PRD/SPEC paths]`;
5. relevant code, migrations, tests, CI, env and deployment configuration;
6. recent status/handoff records.

Precedence when sources conflict:

1. [implemented code/configuration];
2. [migrations/database policies];
3. [tests/CI evidence];
4. [approved current decisions/specs];
5. [general docs];
6. [historical notes].

Record conflicts. Do not present proposals as implemented facts.

## 3. Stack and verified versions

- Runtime/language: [detected version]
- Framework: [detected version]
- Database/storage: [system and version]
- Auth/identity: [provider/model]
- Deployment: [provider/environments]
- External integrations: [providers]
- Package manager and lockfile: [tool/path]

Never guess unstable versions or API contracts; check manifests and current official documentation.

## 4. Architecture and boundaries

Implemented flow:

`[UI/API] -> [service/use case] -> [repository/adapter] -> [data/provider]`

Module responsibilities:

- `[path]`: [responsibility]
- `[path]`: [responsibility]

Invariants:

- [business rule]
- [provider boundary]
- [idempotency or state rule]
- [data integrity rule]

Forbidden shortcuts:

- [e.g. direct DB access from UI]
- [e.g. provider call outside adapter]
- [e.g. business rule in repository]

## 5. Identity, authorization and data isolation

Identity model: `[SINGLE_CONTEXT | OWNER_SCOPED | TENANT_SCOPED]`

Evidence:

- [tables/claims/membership/session helpers]

Rules:

- derive identity and scope from trusted server state;
- enforce authorization server-side;
- preserve repository filters and RLS/policies where applicable;
- never expose privileged credentials to the client;
- do not claim tenant isolation without end-to-end evidence.

Critical roles and permissions:

- `[role]`: [allowed actions]

## 6. Sensitive data and LGPD controls

Sensitive categories handled:

- [personal/contact/location/financial/clinical/legal/message content]

Rules:

- use synthetic data in tests and docs;
- minimize payloads and logs;
- never log or version secrets;
- retention/redaction source: `[path or NEEDS_DECISION]`;
- external AI/provider processing: `[approved limits or disabled]`.

## 7. Database and migration rules

- Canonical migration path: `[path]`
- Current head/source of schema: `[path/command]`
- Create new migrations; do not edit published migrations.
- Explain constraints, indexes, locks, backfill and rollback.
- Run migration tests only against explicitly isolated disposable infrastructure.
- Destructive operations require explicit human approval.

## 8. Validation commands

Use the commands that exist in this repository:

- format/diff: `[command]`
- lint/static analysis: `[command]`
- typecheck/compile: `[command]`
- unit tests: `[command]`
- integration tests: `[command + safe test environment]`
- build: `[command]`
- E2E/browser: `[command/environment]`
- migration verification: `[command/environment]`

Report each as `PASS`, `FAIL`, `NOT RUN` or `BLOCKED`.

## 9. Environments and external actions

Known environments:

- local: [details]
- test: [details]
- preview/staging: [details]
- production: [details]

Do not perform without explicit authorization:

- real messages, payments, emails or provider mutations;
- production deploy/merge;
- secret/configuration changes;
- destructive database operations;
- activation of AI or customer-data processing;
- changes to auth, roles, RLS or retention policy.

## 10. Git and change discipline

- inspect branch, status, HEAD, log and diff before resuming;
- preserve unrelated and untracked work;
- use a branch for material changes;
- stage explicit paths; do not default to `git add .`;
- keep commits small and descriptive;
- draft PR by default;
- merge, deploy and branch deletion require explicit approval.

## 11. Reusable skills

Start with `renova-aura-router` and add only the minimum applicable skills.

Project-specific additions:

- [local guardian/prompt path]
- [local router/index path]

If a referenced skill is missing, mark `MISSING_REFERENCE`; do not invent execution.

## 12. Final report

### EXECUTAR AGORA

- objective and authorized scope;
- files changed;
- validations and literal results;
- security/data impact;
- rollback.

### PLANEJAR

- remaining work;
- dependencies and approval gates.

### ARQUIVAR

- branch, commits, PR, merge and deploy state;
- `NOT RUN`, `UNKNOWN` and intentionally unperformed actions;
- final status: `SAFE_TO_PLAN | SAFE_TO_APPLY | SAFE_WITH_CAUTION | NEEDS_HUMAN_APPROVAL | BLOCKED`.
```
