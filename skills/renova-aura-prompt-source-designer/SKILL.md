---
name: renova-aura-prompt-source-designer
description: Create, refactor, index, and evaluate high-quality source prompts and reusable agent skills for Renova Aura projects. Use when building prompt libraries, master prompts, routers, guardians, project adapters, Codex instructions, or prompt versioning and quality systems.
---

# Renova Aura Prompt Source Designer

## Mission

Create prompts that are clear enough to execute, narrow enough to route correctly, safe enough for real repositories, and structured enough to maintain and evaluate over time.

A good prompt is an operational contract, not decorative prose.

## Before creating a prompt

1. Search the project and central library for overlapping prompts or skills.
2. Read project-local `AGENTS.md`, decisions and architecture.
3. Identify the target agent/tool and supported capabilities.
4. Define the exact trigger, non-trigger and expected output.
5. Identify risks, approval gates and unavailable tools.
6. Decide whether this belongs in:
   - a reusable central skill;
   - a project-specific adapter;
   - a one-time execution prompt;
   - a normative project instruction;
   - documentation rather than a prompt.

Do not create another prompt when an existing prompt can be safely improved or referenced.

## Prompt types

- `ROUTER`: selects the minimum correct workflow.
- `GUARDIAN`: enforces cross-cutting safety or quality.
- `EXECUTOR`: performs a bounded implementation task.
- `AUDITOR`: diagnoses and reports without changing by default.
- `COMMANDER`: coordinates several skills with one explicit owner.
- `ADAPTER`: adds project-specific facts and constraints to reusable skills.
- `TEMPLATE`: produces a repeatable artifact such as PRD, SPEC, report or handoff.

Avoid “super prompts” that combine every role and activate every skill indiscriminately.

## Source prompt structure

Use the following sections when applicable:

1. **Identity / role**: operational responsibility, not fictional personality.
2. **Mission**: one measurable objective.
3. **When to use**: concrete triggers.
4. **When not to use**: prevent accidental routing.
5. **Sources of truth**: files, systems and precedence.
6. **Inputs**: required and optional context.
7. **Operating modes**: audit, plan, apply, release, recovery.
8. **Workflow**: ordered steps with stop conditions.
9. **Invariants**: rules that must remain true.
10. **Approval gates**: destructive, production or sensitive boundaries.
11. **Validation**: tests and evidence required.
12. **Output contract**: exact sections, statuses or schemas.
13. **Failure behavior**: uncertainty, missing references and blocked state.
14. **Examples**: only when they clarify difficult behavior.

## Writing quality

- Use direct imperative language.
- Prefer explicit verbs and observable outcomes.
- Keep project facts out of generic skills.
- Mark assumptions and future work.
- Avoid repeated slogans, excessive capitalization and fake certainty.
- Use tables only when they improve routing or comparison.
- Keep commands, paths and identifiers exact.
- Do not embed secrets, personal data or real customer payloads.
- Do not instruct an agent to claim actions or tests it did not perform.

## Tool and reasoning guidance

State the preferred tool and reasoning level only when it materially affects execution:

- simple documentation or copy: standard reasoning;
- isolated code change: focused repository inspection;
- architecture, auth, RLS, migrations, production or incident: high reasoning with full evidence and approval gates;
- external documentation that may change: official current source verification;
- MCP/app connector: only when connected private data or action is necessary;
- CLI: only when repository or connector capabilities cannot complete the operation safely.

Never prescribe a tool the executing environment does not have.

## Reusable technical prompt template

```markdown
# [PROMPT NAME]

## Objective
[One concrete outcome.]

## Context and sources of truth
- Read: [exact files/systems]
- Precedence: [implemented code/migrations/tests vs docs]
- Current constraints: [facts only]

## Scope
### In scope
- ...

### Out of scope
- ...

## Workflow
1. Inspect ...
2. Report current state ...
3. Propose smallest safe change ...
4. Stop for approval when ...
5. Implement only authorized scope ...
6. Validate ...
7. Update documentation ...

## Invariants
- Preserve ...
- Never ...

## Approval gates
- `NEEDS_HUMAN_APPROVAL` before ...

## Validation
- Command/check: ...
- Required negative case: ...
- Evidence: ...

## Output
### EXECUTAR AGORA
...

### PLANEJAR
...

### ARQUIVAR
...

Final status: `SAFE_TO_PLAN | SAFE_TO_APPLY | NEEDS_HUMAN_APPROVAL | BLOCKED`
```

## Skill packaging

For an Agent Skill:

- create one folder per skill;
- include `SKILL.md` with valid YAML frontmatter;
- use a unique lowercase hyphenated `name`;
- write a trigger-rich `description` that also prevents misuse;
- place long checklists or templates in `references/` only when progressive disclosure improves usability;
- place deterministic utilities in `scripts/` with safe defaults and error handling;
- place user-facing design resources in `assets/` only when needed;
- keep the skill self-contained and public-safe if it lives in a public repository.

## Prompt registry

Track for each prompt/skill:

- canonical name and path;
- purpose and owner;
- version or change date;
- triggers and exclusions;
- dependencies/references;
- project compatibility;
- risk level;
- evaluation cases;
- deprecated or superseded paths.

Never keep two active prompts with the same responsibility without declaring the canonical owner.

## Evaluation checklist

Test prompts against:

- correct routing;
- ambiguous request;
- missing file/reference;
- conflicting project instruction;
- destructive action request;
- sensitive data boundary;
- unsupported tool;
- partial failure;
- evidence and test reporting;
- concise final handoff.

A prompt passes only if it refuses to invent state and stops at defined approval gates.

## Required output

Return:

- prompt type and intended location;
- overlap analysis;
- finished source prompt or skill;
- integration/index updates;
- evaluation cases;
- migration/deprecation note for replaced prompts;
- copyable invocation example.
