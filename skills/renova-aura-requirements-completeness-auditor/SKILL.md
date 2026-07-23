---
name: renova-aura-requirements-completeness-auditor
description: Audit a Renova Aura project for missing, conflicting, obsolete or unverified requirements and trace each material requirement to journeys, fields, code, data, tests and evidence. Use before implementation, release or major refactoring when completeness is uncertain.
---

# Renova Aura Requirements Completeness Auditor

## Authority

Project instructions may restrict work but cannot authorize production, real data, remote migration, provider delivery, merge or deploy. Default mode is read-only.

## Activate when

- the user asks what is missing;
- screens or modules may have been forgotten;
- documentation and code disagree;
- a release needs requirement coverage;
- a feature exists without clear acceptance criteria.

## Do not activate when

- the request is a tiny, fully specified copy/style edit;
- another audit already provides a current traceability matrix with evidence.

## Inputs and truth

Read local instructions, memory, Git status, PRD/SPEC, routes, code, schema, integrations, tests and recent handoff. Trust tested behavior, code and configuration over old prose.

## Procedure

1. Identify actors, goals, journeys and material requirements.
2. Assign stable IDs without rewriting source history.
3. Trace requirement → journey/state → fields → module/file → data/integration → authorization → tests → evidence.
4. Classify `IMPLEMENTED`, `PARTIAL`, `DOCUMENTED_ONLY`, `MISSING`, `CONFLICTING`, `OBSOLETE` or `NOT_VERIFIED`.
5. Detect implementation without requirement and requirement without owner/test.
6. Convert vague acceptance language into observable criteria.
7. Prioritize by user value, safety, data integrity and release impact.

## Gates

- No implementation in audit mode.
- No claim of coverage without code/test evidence.
- Sensitive, billing, auth, RLS, provider or irreversible changes require full specification and human approval.

## Output

Deliver facts, assumptions, traceability matrix, missing requirements, conflicts, blocking gaps, recommended acceptance criteria, affected files, test plan and `EXECUTAR AGORA / PLANEJAR / ARQUIVAR`.

## Validation

A valid result includes at least one positive requirement, one negative/denied case, one error/recovery case and evidence location for every blocker.

## Rollback

This skill is read-only unless a separately approved follow-up edits documentation. Revert only files explicitly created by that follow-up.