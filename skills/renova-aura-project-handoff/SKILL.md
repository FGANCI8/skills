---
name: renova-aura-project-handoff
description: Produce accurate project status, documentation updates, continuity prompts, decision records, and handoffs for Renova Aura repositories. Use after features, audits, incidents, interrupted work, agent sessions, PR preparation, or when moving context between ChatGPT, Codex, and another developer.
---

# Renova Aura Project Handoff

## Mission

Preserve the real project state so work can continue without rediscovery, duplicated implementation or invented progress.

## Source precedence

Use project instructions first. Unless the repository defines another order, prefer:

1. implemented code and configuration;
2. migrations and database policies;
3. executable tests and CI results;
4. approved decisions and current specs;
5. README and operational documentation;
6. chronological notes, task logs and prior conversation summaries.

When sources conflict, record the conflict. Do not silently choose the most convenient version.

## Handoff inputs

Inspect when available:

- current branch, HEAD, status and diff;
- commits and PR state;
- changed files;
- commands and validations actually run;
- failures, blockers and environment limitations;
- product decisions and acceptance criteria;
- migrations, env/config and deployment state;
- screenshots or runtime evidence;
- approval gates and actions explicitly not performed.

## Status vocabulary

Use literal states:

- `DONE`: implemented and validated with stated evidence;
- `PARTIAL`: some acceptance criteria remain;
- `PLANNED`: documented but not implemented;
- `BLOCKED`: cannot continue safely;
- `NOT_RUN`: validation or action was not executed;
- `NEEDS_HUMAN_APPROVAL`: explicit decision is required;
- `UNKNOWN`: evidence is unavailable or conflicting.

Never convert “documented”, “selected”, “created a prompt” or “build passed” into “feature complete”.

## Required handoff structure

### 1. Project snapshot

- purpose and current product limits;
- repository and branch;
- last confirmed commit;
- environment inspected;
- relevant stack versions when verified.

### 2. What was requested

State the user objective and exact authorized scope.

### 3. What was completed

For each item include:

- behavior or artifact delivered;
- files changed;
- acceptance criterion covered;
- validation evidence;
- risk or limitation.

### 4. What remains

Separate:

- required to finish current scope;
- recommended follow-up;
- deferred product ideas;
- blocked items and required decision.

### 5. Safety and operations

- auth/RBAC/RLS/ownership impact;
- sensitive data impact;
- migration and rollback;
- external calls, messages, charges or production actions;
- items deliberately not performed.

### 6. Exact continuation point

Provide the smallest next action, target files and the validation that should follow.

## Decision record

For material human decisions, capture:

- decision ID or short title;
- date and decision maker when known;
- context and options considered;
- approved choice;
- consequences and non-goals;
- implementation status: `NOT_STARTED`, `PARTIAL` or `IMPLEMENTED_WITH_EVIDENCE`;
- superseded decision reference when applicable.

A decision document does not prove code or database alignment.

## Continuity prompt

When the next session needs a copyable prompt, generate one that instructs the agent to:

1. recover the existing repository and branch;
2. read `AGENTS.md` and named sources;
3. inspect status, diff, commits and tests before editing;
4. summarize completed, pending and blocked work;
5. avoid restarting or duplicating implementation;
6. continue from the exact next action;
7. stop at approval gates;
8. report files, validations, risk and rollback.

Do not embed secrets, real customer data or unsupported claims in the continuity prompt.

## Documentation update rules

- Update canonical documents rather than creating near-duplicates.
- Link to detailed specs instead of copying long sections.
- Mark future work clearly.
- Preserve historical decisions; supersede them explicitly.
- Keep paths, commands and names executable and current.
- Remove stale status only after confirming the replacement source.

## Final format

### EXECUTAR AGORA

- confirmed current state;
- completed work and evidence;
- exact continuation action.

### PLANEJAR

- remaining scope, dependencies and decisions;
- tests, rollout and rollback still needed.

### ARQUIVAR

- branch/commit/PR/deploy state;
- `NOT_RUN`, `UNKNOWN` and intentionally unperformed actions;
- finished continuity prompt when requested.
