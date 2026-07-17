# Classification and conflict rules

## Placement decision

| Signal | Placement |
|---|---|
| Reusable workflow, no product facts, synthetic examples | global candidate |
| Exact project commands, paths, roles, schema, provider state, or product decisions | project adapter |
| Client, clinical, legal, financial, commercial, credential, production, or personal information | private reference only |
| Old version retained solely for comparison | backup or superseded |
| Invalid metadata, missing source, unsafe instruction, or ambiguous owner | quarantine |

## Canonical owner test

Two artifacts conflict when they can both trigger for the same request and disagree about scope, authority, side effects, precedence, validation, or completion status.

Choose the canonical owner by:

1. safety and privacy coverage;
2. evidence and project compatibility;
3. narrowness of responsibility;
4. explicit inputs and outputs;
5. validation quality;
6. maintenance cost.

Do not solve semantic duplication by keeping several active aliases with different rules.

## Recommended responsibility map

| Responsibility | Canonical Renova Aura owner |
|---|---|
| natural-language task routing | `renova-aura-router` |
| library inventory/install/publication | `renova-aura-skill-library-curator` |
| prompt and skill content design | `renova-aura-prompt-source-designer` |
| system architecture decision | `renova-aura-saas-architect` |
| implementation/refactor discipline | `renova-aura-engineering-guardian` |
| application/data security | `renova-aura-security-data-guardian` |
| user journey and state semantics | `renova-aura-ux-design-system` |
| premium visual identity | `renova-aura-premium-frontend` |
| tests/release/rollback | `renova-aura-quality-release` |
| PDF task routing | `renova-aura-pdf-forms-router` |

## Status layering

- Skill lifecycle: `SELECTED`, `EXECUTED`, `NOT_APPLICABLE`, `MISSING_REFERENCE`, `BLOCKED`.
- Check result: `PASS`, `FAIL`, `NOT_RUN`, `NOT_VERIFIED`, `BLOCKED`.
- Delivery decision: use the final-status vocabulary defined by the primary skill.

Never translate one layer into another. A selected skill is not executed; an executed check is not automatically a safe release.
