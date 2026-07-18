---
name: renova-aura-skill-library-curator
description: Inventory, classify, deduplicate, improve, validate, install, and publish reusable Renova Aura skills and prompt libraries safely. Use when users ask to organize skills, create a master router, compare global/project/backup versions, find prompt conflicts, decide what may be installed globally, sanitize project-derived guidance, maintain a skill catalog, or update a public skill repository without exposing private information.
---

# Renova Aura Skill Library Curator

## Mission

Maintain one discoverable, public-safe source of reusable process while keeping project facts, client information, credentials, proprietary code, and sensitive decisions in their original private context.

Maintain agent definitions and prompt indexes as separate public artifacts. Install only approved skill directories globally; never install root agent manifests, prompts, documentation, templates, or Python references as skills.

## Modes

- `INVENTORY_ONLY`: inspect and report without changing sources.
- `CURATE`: choose canonical owners, improve content, and mark superseded material.
- `INSTALL`: install only approved general skills after validation and dry run.
- `PUBLISH`: stage and publish an explicitly authorized, sanitized library change.

Do not infer permission to move from inventory to installation or publication when the user requested read-only work.

## Source order

Inspect the central repository, global skill directory, backups, project-local skill/prompt locations, applicable instructions, and remote repository trees. Read private content only when necessary to understand a generic pattern.

Never modify project sources during central-library maintenance.

## Classification

Classify every candidate using [references/classification-and-conflicts.md](references/classification-and-conflicts.md):

- `GLOBAL_APPROVED`: generic, public-safe, non-conflicting, validated;
- `PROJECT_ADAPTER`: contains project facts or commands and stays local;
- `PRIVATE_REFERENCE`: useful for analysis but must not be copied;
- `CANONICAL`: owns an active responsibility;
- `SUPERSEDED`: replaced with an explicit successor;
- `QUARANTINE`: invalid, ambiguous, unsafe, or unverifiable;
- `BACKUP_ONLY`: historical comparison source, never auto-restored.

## Inventory contract

For each global skill record folder, `SKILL.md`, declared name, description, auxiliary files, timestamps, byte size, SHA-256, probable function, structure quality, duplicate/conflict status, and disposition.

For project and remote sources, prefer sanitized counts, relative categories, hashes, and canonical mappings. Do not publish private absolute paths or content.

## Duplicate and conflict handling

1. Detect byte-identical files by hash.
2. Detect same-name and same-trigger candidates.
3. Compare responsibility, input, output, side effects, precedence, and approval gates.
4. Select one canonical owner per responsibility.
5. Merge only generic process that improves the canonical owner.
6. Keep project facts in adapters.
7. Mark aliases or successors explicitly; do not silently delete history.

Security and privacy gates outrank release, architecture, domain workflow, UX, aesthetics, growth, and convenience. Project-local truth outranks generic assumptions unless it conflicts with higher-level safety instructions.

## Skill quality gate

Require:

- folder/name agreement and valid lowercase hyphenated name;
- trigger-rich description that says what and when;
- concise imperative instructions;
- progressive disclosure for detailed references;
- no unresolved placeholders;
- explicit scope, non-goals, approvals, validation, failure behavior, and output;
- interface metadata when supported;
- public-safe examples and synthetic data;
- evaluation cases for routing and dangerous requests.

For an agent catalog, also require a valid schema, unique IDs, existing skill references, acyclic dependencies, one accountable integrator, bounded rounds, independent evaluators, exclusive file ownership, and human gates for critical actions.

## Safe global installation

Before writing to the global destination:

1. resolve the exact source and destination;
2. validate the skill and public-safety scan;
3. run a dry comparison;
4. skip byte-identical destinations;
5. block divergent destinations unless replacement was explicitly authorized;
6. back up every replaced destination with timestamp and hashes;
7. install from a clean temporary copy;
8. re-hash and compare source to destination;
9. keep project adapters and private references out of the global set;
10. report restart/reload requirements.

The global manifest contains only `skills/<name>` folders. The Agent OS team catalog and reference runtime remain repository documentation/reference material.

Never restore wildcard backups automatically.

## Public repository gate

Before staging:

- scan for credentials, tokens, private URLs, personal/client data, clinical/legal rules, production identifiers, and proprietary code;
- inspect branch, status, diff, upstream divergence, and exact staged paths;
- exclude private audit artifacts and generated scratch files;
- validate every changed skill and installer;
- state `NOT RUN` checks honestly;
- require explicit authorization for push, PR state changes, merge, or publication when not already granted.

## Required output

Return:

- source inventory and evidence date;
- canonical/superseded/private/approved classifications;
- duplicate and conflict map;
- files created or improved;
- validation and public-safety results;
- installed skills, backups, and hash verification;
- Git branch, commit, push, PR, merge, and deploy state;
- rollback procedure;
- final status: `INVENTORIED`, `CURATED`, `READY_TO_INSTALL`, `INSTALLED`, `READY_TO_PUBLISH`, `NEEDS_HUMAN_APPROVAL`, or `BLOCKED`.
