---
name: renova-aura-python-engineering
description: Create, implement, review, or repair Python-dominant Renova Aura projects, services, automations, CLIs, and agent runtimes using modern typing, Pydantic or detected validation tools, async discipline, packaging, tests, security, and measurable performance. Use when Python is the primary runtime; keep generic API ownership with renova-aura-backend-api-engineer and AI policy with renova-aura-ai-integration-guardian.
---

# Renova Aura Python Engineering

## Mission

Produce idiomatic, typed, testable Python that fails clearly, isolates side effects, and respects the repository's supported runtime and packaging choices.

## When not to use

Do not use when Python is incidental, when the task is only a language-neutral API or architecture decision, or when a repository contains no Python surface. Do not introduce Python into a project merely to trigger this workflow.

## Discovery

Read local instructions, `pyproject.toml` or other manifests, lockfiles, supported Python versions, package layout, entry points, configuration, tests, typing and lint rules. Detect existing FastAPI, Pydantic, asyncio, task queues, or agent libraries; do not add them by assumption.

## Workflow

1. Define the boundary, public types, invariants, side effects, and failure modes.
2. Model external input with explicit validation and bounded fields.
3. Use precise type annotations and small composable functions; avoid dynamic escape hatches without evidence.
4. Keep I/O behind interfaces or adapters so tests use fakes without network, shell, Git, database, or provider calls.
5. Use async only for real concurrent I/O; never block the event loop with synchronous work.
6. Handle cancellation, timeout, retries, resource cleanup, and partial failure explicitly.
7. Package with the repository's existing tool, narrow dependencies, and supported version bounds.
8. Add unit and contract tests for success, invalid input, exceptions, cancellation or timeout, and disabled providers.
9. Run formatting/lint, type checks, tests, build, and security checks that the project actually defines.

## Python quality rules

- Prefer standard library before adding a dependency that has no clear maintenance benefit.
- Keep secrets out of arguments, tracebacks, logs, examples, and fixtures.
- Never use unrestricted `eval`, `exec`, pickle from untrusted sources, or free-form shell execution.
- Validate paths and outbound destinations before I/O.
- Keep model or provider output untrusted until validated.
- Do not mask failures with broad exception swallowing.

## Human gates

Stop before real credentials, external API calls, production jobs, destructive filesystem/database work, package publication, or runtime-version migration with material compatibility risk.

## Validation and output

Use [references/evals.md](references/evals.md). Return runtime and package evidence, interfaces and models, files changed, exact checks, side-effect isolation, security/performance impact, rollback, and status: `READY_TO_IMPLEMENT`, `SAFE_TO_REVIEW`, `NEEDS_HUMAN_APPROVAL`, or `BLOCKED`.
