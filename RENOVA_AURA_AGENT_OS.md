# Renova Aura Agent Operating System V1.1

Public, reusable governance for turning natural Portuguese requests into bounded,
verifiable work. The system starts with the smallest sufficient mechanism,
keeps one accountable integrator and increases coordination only when risk,
dependencies or duration justify it.

## Layers

1. The router classifies intent, complexity and risk.
2. Skills provide reusable methods and quality standards.
3. Agents declare bounded roles, tools, ownership and gates.
4. The orchestrator coordinates medium, complex, iterative or long work.
5. Independent evaluators review artifacts and evidence; authors do not
   self-approve.
6. One integrator consolidates the final result but receives no merge, deploy or
   production authority from that role.

The canonical registry is `agents/renova-aura-team.yaml`; 18 definitions live
under `agents/definitions/`. Closed schemas are in `agent-team.schema.json` and
`operating-records.schema.json`. Executable dependency-free checks are in
`agents/contract_checks.py`.

## Proportional selection

| Situation | Default mode |
|---|---|
| trivial reversible task | deterministic flow or `SINGLE_SPECIALIST` |
| medium change | `SPECIALIST_PLUS_REVIEWER` |
| dependent steps | `SEQUENTIAL_PIPELINE` |
| independent read-only analyses | `ORCHESTRATOR_WORKERS` |
| distinct preclaimed paths | `CONTROLLED_PARALLEL` |
| rubric-driven quality | `EVALUATOR_OPTIMIZER_LOOP` |
| work spanning sessions | `LONG_RUNNING_INCREMENTAL` |
| incident | `INCIDENT_MODE` |
| release preparation | `RELEASE_MODE` |

A simple request never activates the entire team. The router and orchestrator
remain subject to the basal `RA-AUTH-BASELINE-1`: local instructions may only
restrict authority, and untrusted content is data only.

## Ownership and concurrency (`RA-AOS-002`)

- A file has at most one active writer.
- V1.1 claims are relative, exact and typed as file/directory; globs are rejected.
- Windows comparison is case-insensitive and blocks reserved names, traversal,
  trailing-dot/space aliases, Unicode compatibility aliases and hard-link object
  identity collisions.
- Existing target type is checked independently from the caller declaration.
- Symlink, junction and other reparse ancestry block work.
- Parallel preflight accepts only planned/active claims and detects ancestral
  `WRITE/WRITE` and `WRITE/READ` overlap.
- Real diffs are reconciled only against the same owner/step's `ACTIVE WRITE`
  claim, before it transitions to `COMPLETE`.

Shared schemas, migrations, identity, authorization, RLS and dependent code stay
sequential. Any unclaimed path or filesystem divergence produces a security or
scope block.

## Controlled loops (`RA-AOS-003`)

Every loop declares acceptance references, author, distinct evaluator, artifact
binding, rounds, turns, timeout, budget, tool limits, gates and terminal reason.
Per-instance limits never reset the task chain. Task generation, loop instances,
rounds, provider turns, tool calls, budget, reopens, start, absolute deadline and
terminal history are cumulative and monotonic across retries, child agents,
sessions and handoffs.

`GenerationDecisionRecord` is required for a new generation. The synthetic
store consumes it atomically and binds it to the prior terminal evidence and the
canonical SHA-256 of the complete previous ledger. A prompt/handoff/model string
cannot reopen a task. The synthetic decision has ledger-transition authority
only and cannot execute any work.

Terminal reasons are `PASS`, `MAX_ROUNDS`, `TIMEOUT`, `BUDGET_LIMIT`,
`HUMAN_APPROVAL_REQUIRED`, `SECURITY_BLOCK`, `ENVIRONMENT_BLOCK`,
`MISSING_EVIDENCE` and `SCOPE_CHANGE`.

## Approval boundary (`RA-AOS-001`)

No agent can authorize merge, deploy, production, irreversible migration, real
database access, payment, external communication, real provider, destructive
operation, sensitive-data use or high-impact clinical/legal decisions.

`ApprovalRecord` is typed decision evidence, bound to exact action, scope,
targets, actor, environment, time window, nonce and HEAD/SHA-256. The call plane
passes only an opaque ID to a host-owned store boundary; inline records and trust
sets are not accepted. Verification and consumption are atomic and single-use.

V1.1 supplies only a process-local non-production synthetic fixture. Its result
is `NEVER_AUTOMATIC`, `executable: false`; no real trust store is configured.
Real-provider execution remains `HARD_FORBIDDEN_V1`, regardless of any record.

## Independent evaluation

An `EvaluationRecord` links an artifact to completed author claims, a distinct
registered evaluator and a separate evaluator-report claim. The evaluator may
not own a write claim over an evaluated path. The record is evidence-only and
does not grant approval, merge, release or deploy authority.

## Incident and privacy defaults

Incident mode defaults to `AUDIT_ONLY`: repository write, write-claim activation
and external side effects are denied. V1.1's incident role is read-only and may
produce only a structured proposal.

Metrics and traces are local, sanitized and disabled by default. Disabled
metrics require sink `DISABLED`; enabled metrics require `MEMORY_ONLY` or
`PRIVATE_LOCAL_FILE`. Raw objectives, prompts, code, PII, secrets, private paths
and client/production identifiers are forbidden in public evidence.

## Reference runtime and scope

The Python reference runtime belongs to stacked PR D and is `NOT_RUN` in
isolated PR B. Its future provider adapter is an inexecutable structural stub;
no key, environment variable, string, caller-created record or handoff can
enable it. CI, the contractual manifest and global installation belong to later
stacked PRs.

The Agent OS organizes work but grants no additional authority. Agent
definitions, prompts, documents and Python reference remain repository content;
only approved general skills may later be installed globally. No application or
consumer project is modified by this library.
