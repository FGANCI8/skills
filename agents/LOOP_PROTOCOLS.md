# Controlled loop protocols

| Loop | Sequence | Independent evaluator |
|---|---|---|
| implementation | plan → small block → test → review → correct | technical reviewer |
| premium front-end | implement → render → evaluate desktop/mobile → correct | visual evaluator |
| security | threat model → audit → negative cases → re-audit | AppSec |
| quality | test → diagnose → minimal correction → regression | quality/reviewer |
| performance | measure → diagnose → optimize → measure | performance/reviewer |

Each loop has observable acceptance references, bounded rounds/turns/time/tools,
an author, a distinct evaluator, exact artifact bindings and a terminal reason.
No unbounded `while true`, `max_turns=None` or equivalent instruction is valid.

## Cumulative task-chain accounting (`RA-AOS-003`)

Per-agent and per-loop limits are subtotals; they never reset the task ledger.
The ledger persists `task_generation`, `loop_instances`, total rounds, provider
turns, tool calls and budget units, plus start, absolute deadline, reopen count
and append-only terminal history. Usage-at-block-start plus every block delta,
including loop instances, must reconcile exactly with cumulative usage. Unknown
usage is not silently replaced with zero.

The absolute deadline cannot exceed `started_at + absolute_timeout_minutes`.
Terminal events are ordered, bounded by start/deadline/current host time, unique
per generation and tied to the current stop reason. Handoffs preserve the task
ID, start, deadline, limits, counters and history.

## Typed generation decision

After any terminal reason, model text cannot reopen the same generation. A new
generation requires an opaque lookup in a stateful
`SyntheticGenerationDecisionStore`. The stored `GenerationDecisionRecord` is
single-use and bound to task ID, previous stop reason/evidence, from/to
generation and the canonical SHA-256 of the complete prior ledger. The decision
ID is appended to `generation_decision_refs`; all counters and the original
deadline continue.

V1.1 implements only the atomic non-production synthetic fixture. Its record has
`execution_authority: LEDGER_TRANSITION_ONLY` and `executable: false`; it cannot
authorize provider calls, repository writes, deploys or any external side
effect. A string from a prompt, handoff or model is never sufficient.

## Independent evaluation

`EvaluationRecord` binds the reviewed artifact, author, evaluator, paths,
author claims and a separate evaluator-report claim. The evaluator must be a
distinct registered agent with independent-evaluation capability and must have
no write claim covering an evaluated artifact. The report path cannot overlap
the artifact. Evaluation is evidence-only and grants no approval, merge or
release authority.

Terminal reasons are `PASS`, `MAX_ROUNDS`, `TIMEOUT`, `BUDGET_LIMIT`,
`HUMAN_APPROVAL_REQUIRED`, `SECURITY_BLOCK`, `ENVIRONMENT_BLOCK`,
`MISSING_EVIDENCE` and `SCOPE_CHANGE`.
