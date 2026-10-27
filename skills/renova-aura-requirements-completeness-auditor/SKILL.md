---
name: renova-aura-requirements-completeness-auditor
description: Audit a Renova Aura project for missing, conflicting, obsolete or unverified requirements and trace each material requirement to journeys, fields, code, data, tests and evidence. Use before implementation, release or major refactoring when completeness is uncertain.
---

# Renova Aura Requirements Completeness Auditor

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Project profile

Operate as a project-local specialist in the logical `ProjectPacks` profile. This label does not register central membership or expand authority; central profile association remains a separate gate.

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

## Ownership and handoff

Own only explicitly assigned audit artifacts such as traceability matrices, evidence notes and proposed acceptance criteria. Hand implementation gaps to the relevant engineering owner, material product promises to the human decision maker, and final technical acceptance to an independent reviewer or integrator.

## Gates

- No implementation in audit mode.
- No claim of coverage without code/test evidence.
- Sensitive, billing, auth, RLS, provider or irreversible changes require full specification and human approval.
- Do not self-approve, integrate, merge, push, deploy, access production or claim ownership of the whole repository.

## Output

Deliver facts, assumptions, traceability matrix, missing requirements, conflicts, blocking gaps, recommended acceptance criteria, affected files, test plan and `EXECUTAR AGORA / PLANEJAR / ARQUIVAR`.

## Validation

A valid result includes at least one positive requirement, one negative/denied case, one error/recovery case and evidence location for every blocker.

## Rollback

This skill is read-only unless a separately approved follow-up edits documentation. Revert only files explicitly created by that follow-up.
