---
name: renova-aura-project-bootstrap
description: Start, recover, or orient a Renova Aura software project without discarding existing work. Use when opening a repository for the first time, resuming interrupted work, validating an imported project, or establishing the minimum project operating structure.
---

# Renova Aura Project Bootstrap

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Goal

Understand the real repository state before creating files, changing architecture or proposing a roadmap. Preserve existing work and produce a safe starting point.

## Modes

- `ORIENT_ONLY`: inspect and report; do not edit.
- `PLAN_THEN_APPLY`: inspect, propose a bounded plan, then apply only authorized low-risk changes.
- `RECOVERY`: reconstruct interrupted work from branch, commits, docs, diffs and tests.
- `NEW_PROJECT`: create only the minimum foundation justified by the validated product scope.

## Discovery sequence

1. Identify repository, default branch, current branch and worktree state.
2. Read root and nested `AGENTS.md`.
3. Read README, product foundation, PRD, decisions, specs, status and handoff documents.
4. Detect stack from manifests and lockfiles; verify versions instead of guessing.
5. Map source, tests, migrations, CI, deployment and env examples.
6. Locate prompts, skills, agent instructions and duplicated governance files.
7. Inspect recent commits and open work when available.
8. Run only safe read-only checks until the environment is understood.

## Existing-work protection

- Never restart a project merely because its structure differs from a preferred template.
- Never overwrite a non-empty file without reading it.
- Never delete an unknown directory, branch, migration, generated artifact or configuration without evidence and approval.
- Do not treat an empty-looking GitHub folder as real: Git does not track empty directories unless a placeholder file exists.
- Preserve user changes, untracked files and stashes.
- Avoid parallel agents editing the same files.

## Minimum project operating structure

Recommend or create only when absent and appropriate:

- `AGENTS.md` with project-local constraints;
- README with purpose, setup, validation and limits;
- product decisions or foundation document;
- PRD/SPEC location and acceptance criteria convention;
- env example without secrets;
- lint, typecheck, test and build commands;
- migration and rollback rules;
- CI definition;
- status/handoff document;
- prompt/skill index only when the project actually uses them.

## Stack-neutral architecture check

Determine the implemented boundaries. Typical examples:

- web: UI -> route/controller -> service/use case -> repository -> database;
- backend: API -> application/service -> domain -> repository/adapter;
- automation: event ingress -> validation -> deterministic orchestration -> outbox/provider;
- local-first: UI -> service -> local repository/storage.

Do not impose a layer that adds no value. Flag business rules in UI/controllers, scattered database access, provider calls bypassing adapters and duplicated domain logic.

## Safe validations

Choose commands from repository evidence. Common categories:

- formatting or diff check;
- lint/static analysis;
- type checking or compilation;
- focused unit tests;
- isolated integration tests;
- production build;
- migration validation in an explicitly disposable database.

Never run destructive cleanup, production tests, real provider calls or migrations against an ambiguous database.

## Required output

### EXECUTAR AGORA

- repository state and sources read;
- what already exists and must be preserved;
- smallest safe action;
- files changed, if authorized;
- validations and literal results.

### PLANEJAR

- missing foundations ranked by risk and value;
- dependencies and approval gates;
- proposed MVP or recovery sequence.

### ARQUIVAR

- confirmed branch/commit state;
- unresolved ambiguity;
- explicitly unperformed delete, merge, deploy or external action.
