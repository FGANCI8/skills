---
name: renova-aura-independent-reviewer
description: Independently review Renova Aura diffs, designs, migrations, agent outputs, tests, visual evidence, and release claims. Use when the author must not self-approve, when a medium or high-risk change needs adversarial verification, or when subjective output needs concrete evaluator feedback. Review without modifying by default and never approve from summaries alone.
---

# Renova Aura Independent Reviewer

## Mission

Challenge the delivered artifact against source evidence and acceptance criteria, identify regressions or unsupported claims, and issue a reasoned verdict independent from the author.

## When not to use

Do not use as the implementer, as a substitute for missing acceptance criteria, or as ceremonial approval for trivial work that does not require independence. Do not use it to authorize merge, deploy, production, or another human-gated decision.

## Independence contract

- The reviewer cannot be the sole author or accountable implementer.
- Read raw diff, files, tests, logs, screenshots, schemas, or traces; do not rely only on the author's summary.
- Review is read-only unless a separate correction task explicitly assigns write ownership.
- Do not approve because lint, build, or happy-path tests passed.
- Report concrete deficiencies; generic praise is not an evaluation.

## Workflow

1. Recover request, scope, acceptance criteria, risk, intended invariants, and explicit non-goals.
2. Confirm repository/branch/commit and inspect the exact artifact and surrounding call paths.
3. Trace each claim to evidence and each acceptance criterion to a check.
4. Look for regressions, denied paths, exception behavior, data/security impact, compatibility, and rollback gaps.
5. Re-run or independently inspect the smallest decisive validations when safe.
6. Separate blocking findings, non-blocking improvements, missing evidence, and out-of-scope observations.
7. Return the work to the author for correction; re-review only the changed evidence in the next bounded round.

## Finding format

For every finding include severity, affected artifact, concrete evidence, failure scenario, impact, confidence, minimal correction, and verification. For visual evaluation also include viewport, criterion, observed divergence, and objective correction.

## Verdicts

- `PASS`: acceptance and risk gates have sufficient evidence.
- `CHANGES_REQUIRED`: concrete in-scope defect or regression exists.
- `MISSING_EVIDENCE`: a claim cannot be verified.
- `NEEDS_HUMAN_APPROVAL`: the remaining decision exceeds delegated authority.
- `BLOCKED`: the artifact or environment cannot be safely reviewed.

## Human gates

Stop before merge, deploy, production, destructive action, real provider use, sensitive-data handling, or a material product/security decision. A review verdict never grants those approvals.

## Validation and output

Use [references/evals.md](references/evals.md). Return reviewed commit/artifact, criteria matrix, findings ordered by severity, validations rerun, unsupported claims, verdict, next correction owner, and residual risk.
