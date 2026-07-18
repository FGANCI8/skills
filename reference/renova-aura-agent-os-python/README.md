# Renova Aura Agent OS — Python reference

This directory is a demonstrative, public-safe implementation of the Renova Aura
Agent Operating System. It models routing, planning, independent evaluation,
bounded loops, handoff, and sanitized local tracing. It is not a service and does
not operate on real projects.

## Safe defaults

- `MockProvider` is the only default provider.
- No network, shell, Git, database, deploy, payment, or message tool exists.
- Candidate file paths are modeled only; the runtime never opens them.
- External file, web, issue, and message content is always untrusted data.
- Critical actions stop before provider execution with `HUMAN_APPROVAL_REQUIRED`.
- Every loop has a maximum of three rounds, a timeout, a budget, and a provider-call limit.
- Every delegated provider invocation has at most three turns; this is not a whole-plan step limit.
- An author cannot be their own evaluator.
- Traces contain a request fingerprint and bounded metadata, never the request text.

The 18-agent catalog in `catalog.py` is a reference projection. The repository-level
`agents/renova-aura-team.yaml` remains the canonical catalog.

## Architecture

1. `routing.py` classifies structured facts and normal Portuguese into the smallest safe team.
2. `planning.py` produces a validated DAG with one accountable integrator and
   exclusive write claims.
3. `MockExecutor` requests synthetic artifacts from the provider port.
4. `MockEvaluator` returns `PASS`, concrete revision findings, or an explicit block.
5. `BoundedLoopRunner` stops on the first mandatory terminal condition.
6. `handoff.py` records only evidence available from the run.
7. `tracing.py` supports in-memory tracing and an opt-in JSONL sink beneath an
   allowlisted directory.

Common deterministic logic stays outside an LLM. LangGraph is intentionally absent;
it would be justified only by a proven need for durable execution, persistence, and
complex resumption.

## Local validation

The runtime dependency is Pydantic v2. Tests use the standard-library `unittest`
API and are also collectible by pytest.

From the repository root, prefer `tools/test-renova-aura-agent-os.ps1` and pass
separate Python 3.11+ executables when PyYAML and Pydantic 2 live in isolated
runtimes. The wrapper reports Ruff as `NOT RUN (dependency unavailable)` instead
of claiming a lint result when Ruff is absent.

```powershell
$env:PYTHONPATH = (Resolve-Path .\src)
python -m unittest discover -s tests -v
python -m compileall -q src tests
python -m pytest
python -m ruff check .
```

The first two commands do not require pytest or Ruff. If Pydantic is unavailable,
do not substitute a local shim: run TOML parsing, `compileall`, and
`tests/test_static_safety.py`, then report runtime tests as `BLOCKED`.

Tests use synthetic data and must pass with network and process creation disabled.

## Optional OpenAI adapter

`openai-agents==0.18.2` is declared only in the `openai` extra and is not installed
by default. Importing the package does not import the SDK.

The adapter refuses to run unless all gates are present:

- explicit `enabled=True`;
- an explicitly supplied model name — there is no default model;
- a `SecretStr` API key;
- the same non-empty human-approval reference in settings and the provider request;
- `external_calls_allowed=True` on the provider request;
- the optional SDK is installed.

The adapter is deliberately **proposal-only**. It sends the objective, acceptance
criteria, and revision notes as untrusted JSON data, but it never marks a criterion
complete. The bounded loop therefore terminates with `MISSING_EVIDENCE`; a proposal
cannot become implementation or approval evidence. A future production adapter
would need a separate structured-evidence contract and independent validation.

External SDK tracing is always disabled by this reference adapter. A synthetic test
uses fake local SDK modules to exercise the complete gate set and prove the
proposal-only terminal behavior. No test performs a network or real API call.

## Non-goals

- production orchestration;
- autonomous repository editing;
- persistence or durable queues;
- real provider evaluation;
- security, release, or legal approval;
- proof that an application is correct because a mock run passed.
