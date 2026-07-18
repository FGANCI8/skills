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

## Canonical responsibility map

`Writer` means the final owner of changed files. A supporting skill may propose a patch or contract but cannot write a path already assigned to another owner. The accountable integrator validates the actual diff against exact claims.

| Responsibility | Primary owner | Supporting skills | Writer | Reviewer / exclusions |
|---|---|---|---|---|
| natural-language task routing | `renova-aura-router` | risk-required owner only | none for routing | reviewer when routing changes; no domain implementation |
| bounded multi-agent coordination | `renova-aura-agent-orchestrator` | minimum routed specialists | assigned accountable integrator | independent reviewer; no all-agents default |
| project orientation/recovery | `renova-aura-project-bootstrap` | handoff, security as needed | bootstrap for isolated files or engineering integrator | independent reviewer for recovery writes; no deletion/reset |
| product problem, PRD and SPEC | `renova-aura-product-spec` | architecture, UX, security | product-spec for approved documents | independent reviewer; no implementation authority |
| system architecture decision | `renova-aura-saas-architect` | product, security, engineering | architect for ADR/SPEC only | independent reviewer; no unapproved code migration |
| implementation/refactor integration | `renova-aura-engineering-guardian` | relevant domain methods | `renova-aura-engineering-guardian` for the combined diff | `renova-aura-independent-reviewer`; no broad cleanup |
| backend/API method | `renova-aura-backend-api-engineer` | engineering, security, database | backend owner for isolated files; engineering for combined diff | quality/reviewer; no UI/database-policy ownership |
| database reliability | `renova-aura-database-reliability` | security, engineering, quality | one sequential database writer | independent reviewer; no production execution |
| Python-dominant engineering | `renova-aura-python-engineering` | engineering, security, quality | Python owner for isolated package; engineering for combined diff | independent reviewer; no real provider by default |
| measured performance | `renova-aura-performance-engineering` | engineering, database, observability | owner of exact optimized files | independent reviewer; no speculative rewrite |
| independent technical evaluation | `renova-aura-independent-reviewer` | relevant domain context | none by default | cannot review its own authorship or grant release authority |
| application/data security | `renova-aura-security-data-guardian` | architecture, domain owner, quality | security owner for isolated controls; engineering for combined diff | distinct reviewer; no weakening gates to pass tests |
| user journey/state/accessibility | `renova-aura-ux-design-system` | premium frontend, quality | UX owner for exact interface files | visual/technical reviewer; no backend or brand takeover |
| premium visual identity | `renova-aura-premium-frontend` | UX, quality | frontend owner for exact presentation files | independent visual evaluator; no false production claims |
| AI policy, provider boundary and evals | `renova-aura-ai-integration-guardian` | product, security, observability, engineering | AI owner for isolated AI files; engineering owns combined diff | independent reviewer; no direct authority or real provider |
| tests, CI, release and rollback evidence | `renova-aura-quality-release` | security, platform, domain owner | quality owner for tests/CI only | independent reviewer; no merge/deploy authority |
| observability and incident response | `renova-aura-observability-incident` | security, quality | observability owner for isolated telemetry files | independent reviewer; production action requires approval |
| prompt/skill source design | `renova-aura-prompt-source-designer` | curator, security | prompt designer for exact content files | curator/reviewer; no publication or installation authority |
| project handoff/status | `renova-aura-project-handoff` | current domain owner | handoff owner for canonical status files | independent evidence check; handoff never grants approval |
| library inventory/install/publication | `renova-aura-skill-library-curator` | prompt designer, security, quality | curator for catalog/installer scope | independent reviewer; no private/project content publication |
| PDF task routing | `renova-aura-pdf-forms-router` | minimum PDF specialist | none for routing | compatibility/security review; no universal claim |
| fillable PDF creation/repair | `renova-aura-fillable-pdf-architect` | auditor, delivery | architect for approved working copy | compatibility auditor; never modify immutable source |
| PDF structural compatibility audit | `renova-aura-pdf-compatibility-auditor` | architect only after proven defect | none during audit | delivery/reviewer; no repair without authority |
| PDF viewer/device validation | `renova-aura-pdf-viewer-validation-runbook` | compatibility auditor | none except local synthetic test artifacts | reviewer; no external sharing without approval |
| PDF delivery package | `renova-aura-pdf-delivery-guardian` | compatibility auditor | delivery owner for approved package | independent manifest/hash review; no real delivery authority |

## Status layering

- Invocation lifecycle: `SELECTED`, `EXECUTED`, `NOT_APPLICABLE`, `MISSING_REFERENCE`, `BLOCKED`.
- Check result: `PASS`, `FAIL`, `NOT_RUN`, `NOT_VERIFIED`, `BLOCKED`.
- Delivery decision: use the final-status vocabulary defined by the primary skill.

Never translate one layer into another. A selected skill is not executed; an executed check is not automatically a safe release.
