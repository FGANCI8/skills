# Renova Aura agents

This directory defines the Renova Aura Agent Operating System team. Agents are
bounded operational roles; skills are reusable methods. Natural-language work is
routed to the smallest safe set of roles and skills.

## Canonical sources

- `renova-aura-team.yaml`: registry, basal authority, policies, limits and modes.
- `agent-team.schema.json`: closed team/agent contract.
- `operating-records.schema.json`: approval, generation, ownership, ledger,
  evaluation and local-metrics records.
- `contract_checks.py`: dependency-free fail-closed checks and synthetic stores.
- `definitions/*.yaml`: 18 individual role definitions.
- `TEAM_ROUTING.md`: natural-language routing.
- `FILE_OWNERSHIP_AND_CONCURRENCY.md`: claim lifecycle and parallel safety.
- `LOOP_PROTOCOLS.md`: cumulative loops, typed reopen and independent review.
- `HUMAN_APPROVAL_GATES.md`: human-decision evidence and hard boundaries.
- `LONG_RUNNING_HANDOFF.md`: sanitized continuity between sessions.
- `templates/`: non-authoritative request/evidence examples.

Skill interface metadata under `skills/*/agents/openai.yaml` does not replace
these governance definitions.

## V1.1 authority boundary

The V1.1 implementation has no real trusted approval store and no real
generation-decision store. Its process-local fixtures accept only synthetic,
non-production evidence, consume it atomically and return non-executable
records. Real provider execution is hard-forbidden. Incident mode defaults to
`AUDIT_ONLY` with no repository-write tool or external side effect.

## Isolated PR B validation

These tests use no network, provider, application project, database or real
data:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
python -m unittest discover -s agents/tests -p 'test_*.py' -v
```

They cover atomic approval/generation replay, exact bindings, Windows aliases,
hard links, reparse gates, claim lifecycle, cumulative ledger history,
independent evaluation and metrics configuration. Full JSON Schema validation,
the Python reference runtime, integrated contract manifest, PowerShell wrapper,
Ruff and CI belong to later stacked PRs and remain `NOT_RUN` in PR B.
