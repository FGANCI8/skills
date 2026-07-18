"""Deterministic plan construction with explicit ownership and review."""

from __future__ import annotations

import re
from collections import defaultdict

from .models import (
    AccessMode,
    AgentCatalog,
    AllowedAction,
    CriticalAction,
    ExecutionPlan,
    FileClaim,
    LoopLimits,
    OrchestrationMode,
    PlanStep,
    PlanStepKind,
    RoutingDecision,
    TaskEnvelope,
)
from .safety import critical_actions_from_objective


ACTION_FOR_KIND = {
    PlanStepKind.ANALYZE: AllowedAction.ANALYZE,
    PlanStepKind.PLAN: AllowedAction.PLAN,
    PlanStepKind.MOCK_EXECUTE: AllowedAction.MOCK_EXECUTE,
    PlanStepKind.EVALUATE: AllowedAction.EVALUATE,
    PlanStepKind.INTEGRATE: AllowedAction.INTEGRATE,
    PlanStepKind.HANDOFF: AllowedAction.HANDOFF,
}

IMPLEMENTATION_AGENTS = (
    "database-data-engineer",
    "python-engineer",
    "backend-api-engineer",
    "premium-frontend-specialist",
    "performance-engineer",
    "ai-automation-specialist",
    "platform-release-engineer",
    "observability-incident-engineer",
    "skills-agents-prompts-curator",
)

SUPPORT_ORDER = (
    "product-requirements-analyst",
    "saas-architect",
    "appsec-specialist",
    "ux-accessibility-specialist",
    "observability-incident-engineer",
    "quality-test-engineer",
)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug[:48] or "step"


def _make_step(
    catalog: AgentCatalog,
    *,
    step_id: str,
    title: str,
    agent_id: str,
    kind: PlanStepKind,
    depends_on: tuple[str, ...] = (),
    files: tuple[str, ...] = (),
    acceptance: tuple[str, ...],
    critical_actions: tuple[CriticalAction, ...] = (),
    evaluates_step_id: str | None = None,
) -> PlanStep:
    agent = catalog.get(agent_id)
    if ACTION_FOR_KIND[kind] not in agent.allowed_actions:
        raise ValueError(f"agent {agent_id} cannot perform {kind}")
    claims = tuple(
        FileClaim(path=path, owner_agent_id=agent_id, access=AccessMode.WRITE)
        for path in files
    )
    return PlanStep(
        id=step_id,
        title=title,
        agent_id=agent_id,
        kind=kind,
        depends_on=depends_on,
        file_claims=claims,
        acceptance_criteria=acceptance,
        validation_commands=("mock-validation",),
        critical_actions=critical_actions,
        evaluates_step_id=evaluates_step_id,
    )


def _owner_for_path(path: str, route: RoutingDecision) -> str:
    lowered = path.casefold()
    participants = set(route.participant_agent_ids)
    candidates = (
        ("database-data-engineer", ("migration", "supabase", "database", "db/", ".sql")),
        ("python-engineer", (".py", "python/")),
        ("backend-api-engineer", ("app/api/", "api/", "server", "backend", "route.ts")),
        (
            "premium-frontend-specialist",
            ("frontend", "component", "ui/", "app/", ".tsx", ".css", ".scss"),
        ),
        ("documentation-handoff-specialist", ("docs/", "readme", ".md")),
    )
    for agent_id, markers in candidates:
        if agent_id in participants and any(marker in lowered for marker in markers):
            return agent_id
    fallback_order = (
        "backend-api-engineer",
        "python-engineer",
        "premium-frontend-specialist",
        "database-data-engineer",
        "performance-engineer",
        "ai-automation-specialist",
        "platform-release-engineer",
        "observability-incident-engineer",
        "skills-agents-prompts-curator",
    )
    for agent_id in fallback_order:
        if agent_id in participants:
            return agent_id
    return route.primary_agent_id


def _default_rounds(mode: OrchestrationMode) -> int:
    return {
        OrchestrationMode.SINGLE_SPECIALIST: 1,
        OrchestrationMode.SPECIALIST_PLUS_REVIEWER: 2,
        OrchestrationMode.SEQUENTIAL_PIPELINE: 3,
        OrchestrationMode.ORCHESTRATOR_WORKERS: 2,
        OrchestrationMode.CONTROLLED_PARALLEL: 2,
        OrchestrationMode.EVALUATOR_OPTIMIZER_LOOP: 3,
        OrchestrationMode.LONG_RUNNING_INCREMENTAL: 3,
        OrchestrationMode.INCIDENT_MODE: 3,
        OrchestrationMode.RELEASE_MODE: 2,
    }[mode]


def _limits_for(
    mode: OrchestrationMode,
    steps: list[PlanStep],
    catalog: AgentCatalog,
) -> LoopLimits:
    active_agents = {
        step.agent_id for step in steps if step.kind is not PlanStepKind.HANDOFF
    }
    agent_cap = min(catalog.get(agent_id).max_rounds for agent_id in active_agents)
    rounds = min(_default_rounds(mode), agent_cap)
    return LoopLimits(
        max_rounds=rounds,
        max_turns=3,
        timeout_seconds=60,
        budget_units=30,
        max_provider_calls=30,
    )


def _critical_actions(
    task: TaskEnvelope,
    route: RoutingDecision,
) -> tuple[CriticalAction, ...]:
    actions: list[CriticalAction] = []
    file_migration = any(
        "migration" in path.casefold() or "migrations/" in path.casefold().replace("\\", "/")
        for path in task.facts.candidate_files
    )
    if task.facts.migration or file_migration:
        actions.extend((CriticalAction.MIGRATION, CriticalAction.REAL_DATABASE))
    if task.facts.release_related or route.mode is OrchestrationMode.RELEASE_MODE:
        actions.extend((CriticalAction.MERGE, CriticalAction.DEPLOY, CriticalAction.PRODUCTION))
    actions.extend(
        critical_actions_from_objective(
            task.objective,
            external_provider_allowed=task.policy.external_provider_allowed,
        )
    )
    if route.human_approval_required and not actions:
        actions.append(CriticalAction.SECURITY_CRITICAL)
    return tuple(dict.fromkeys(actions))


def _append_full_stack_steps(
    task: TaskEnvelope,
    route: RoutingDecision,
    catalog: AgentCatalog,
    files_by_owner: dict[str, list[str]],
) -> list[PlanStep]:
    participants = set(route.participant_agent_ids)
    steps: list[PlanStep] = []
    steps.append(
        _make_step(
            catalog,
            step_id="clarify-requirements",
            title="Clarify synthetic requirements",
            agent_id="product-requirements-analyst",
            kind=PlanStepKind.ANALYZE,
            acceptance=("Acceptance criteria are explicit and bounded.",),
        )
    )
    steps.append(
        _make_step(
            catalog,
            step_id="define-contract",
            title="Define the shared contract",
            agent_id="saas-architect",
            kind=PlanStepKind.PLAN,
            depends_on=("clarify-requirements",),
            acceptance=("The shared contract and trust boundaries are explicit.",),
        )
    )
    support_tail = "define-contract"

    if "appsec-specialist" in participants:
        steps.append(
            _make_step(
                catalog,
                step_id="analyze-security-boundaries",
                title="Analyze security boundaries",
                agent_id="appsec-specialist",
                kind=PlanStepKind.ANALYZE,
                depends_on=(support_tail,),
                acceptance=("Threats, trust boundaries, and negative cases are explicit.",),
            )
        )
        support_tail = "analyze-security-boundaries"

    steps.append(
        _make_step(
            catalog,
            step_id="define-test-strategy",
            title="Define risk-based test strategy",
            agent_id="quality-test-engineer",
            kind=PlanStepKind.ANALYZE,
            depends_on=(support_tail,),
            acceptance=("Positive, negative, and regression checks are explicit.",),
        )
    )
    support_tail = "define-test-strategy"
    technical_targets: list[str] = []

    if "database-data-engineer" in participants:
        steps.append(
            _make_step(
                catalog,
                step_id="mock-database",
                title="Produce the mock database artifact",
                agent_id="database-data-engineer",
                kind=PlanStepKind.MOCK_EXECUTE,
                depends_on=(support_tail,),
                files=tuple(files_by_owner.get("database-data-engineer", ())),
                acceptance=("Database invariants and rollback are explicit.",),
                critical_actions=_critical_actions(task, route),
            )
        )
        support_tail = "mock-database"
        technical_targets.append("mock-database")

    steps.append(
        _make_step(
            catalog,
            step_id="mock-backend",
            title="Produce the mock backend artifact",
            agent_id="backend-api-engineer",
            kind=PlanStepKind.MOCK_EXECUTE,
            depends_on=(support_tail,),
            files=tuple(files_by_owner.get("backend-api-engineer", ())),
            acceptance=("Backend behavior matches the shared contract.",),
        )
    )
    backend_tail = "mock-backend"
    technical_targets.append("mock-backend")

    if "python-engineer" in participants:
        steps.append(
            _make_step(
                catalog,
                step_id="mock-python-backend",
                title="Produce the mock Python implementation",
                agent_id="python-engineer",
                kind=PlanStepKind.MOCK_EXECUTE,
                depends_on=(backend_tail,),
                files=tuple(files_by_owner.get("python-engineer", ())),
                acceptance=("Python implementation preserves the reviewed API contract.",),
            )
        )
        backend_tail = "mock-python-backend"
        technical_targets.append("mock-python-backend")

    steps.append(
        _make_step(
            catalog,
            step_id="analyze-ux-accessibility",
            title="Analyze UX and accessibility requirements",
            agent_id="ux-accessibility-specialist",
            kind=PlanStepKind.ANALYZE,
            depends_on=("clarify-requirements",),
            acceptance=("Keyboard, states, errors, and accessibility needs are explicit.",),
        )
    )
    steps.append(
        _make_step(
            catalog,
            step_id="mock-frontend",
            title="Produce the mock frontend artifact",
            agent_id="premium-frontend-specialist",
            kind=PlanStepKind.MOCK_EXECUTE,
            depends_on=(backend_tail, "analyze-ux-accessibility"),
            files=tuple(files_by_owner.get("premium-frontend-specialist", ())),
            acceptance=("Frontend consumes the contract and covers required UI states.",),
        )
    )
    technical_targets.append("mock-frontend")

    review_ids: list[str] = []
    for target_id in technical_targets:
        review_id = f"review-{target_id}"
        steps.append(
            _make_step(
                catalog,
                step_id=review_id,
                title=f"Review {target_id} independently",
                agent_id="independent-technical-reviewer",
                kind=PlanStepKind.EVALUATE,
                depends_on=(target_id,),
                acceptance=("Findings cite evidence and a required change.",),
                evaluates_step_id=target_id,
            )
        )
        review_ids.append(review_id)

    steps.append(
        _make_step(
            catalog,
            step_id="review-mock-frontend-visually",
            title="Review desktop and mobile renders independently",
            agent_id="independent-visual-evaluator",
            kind=PlanStepKind.EVALUATE,
            depends_on=("mock-frontend",),
            acceptance=("Desktop, mobile, states, and visual accessibility are evaluated.",),
            evaluates_step_id="mock-frontend",
        )
    )
    review_ids.append("review-mock-frontend-visually")
    steps.append(
        _make_step(
            catalog,
            step_id="integrate-result",
            title="Integrate reviewed results",
            agent_id="technical-director-orchestrator",
            kind=PlanStepKind.INTEGRATE,
            depends_on=tuple(review_ids),
            acceptance=("The accountable integrator preserves gates and evidence.",),
        )
    )
    return steps


def _append_generic_steps(
    task: TaskEnvelope,
    route: RoutingDecision,
    catalog: AgentCatalog,
    files_by_owner: dict[str, list[str]],
) -> tuple[list[PlanStep], tuple[tuple[str, ...], ...]]:
    participants = list(route.participant_agent_ids)
    reviewer_ids = [
        agent_id
        for agent_id in (route.reviewer_agent_id, "independent-visual-evaluator")
        if agent_id is not None and agent_id in participants
    ]
    reviewer_ids = list(dict.fromkeys(reviewer_ids))

    author_ids = [
        agent_id
        for agent_id in IMPLEMENTATION_AGENTS
        if agent_id in participants
        and catalog.get(agent_id).can_author
        and (files_by_owner.get(agent_id) or agent_id == route.primary_agent_id)
    ]
    if route.primary_agent_id == "technical-director-orchestrator" and not author_ids:
        author_ids = [
            agent_id
            for agent_id in IMPLEMENTATION_AGENTS
            if agent_id in participants and catalog.get(agent_id).can_author
        ][:1]
    if (
        route.primary_agent_id != "technical-director-orchestrator"
        and route.primary_agent_id != "documentation-handoff-specialist"
        and route.primary_agent_id not in reviewer_ids
        and catalog.get(route.primary_agent_id).can_author
        and route.primary_agent_id not in author_ids
    ):
        author_ids.insert(0, route.primary_agent_id)

    steps: list[PlanStep] = []
    support_ids = [
        agent_id
        for agent_id in participants
        if agent_id not in author_ids
        and agent_id not in reviewer_ids
        and agent_id != route.primary_agent_id
        and agent_id
        not in {"technical-director-orchestrator", "documentation-handoff-specialist"}
    ]
    ordered_support = [agent_id for agent_id in SUPPORT_ORDER if agent_id in support_ids]
    ordered_support.extend(agent_id for agent_id in support_ids if agent_id not in ordered_support)

    support_tail: tuple[str, ...] = ()
    for agent_id in ordered_support:
        step_id = f"analyze-{_slug(agent_id)}"
        kind = PlanStepKind.PLAN if agent_id == "saas-architect" else PlanStepKind.ANALYZE
        steps.append(
            _make_step(
                catalog,
                step_id=step_id,
                title=f"Produce bounded support from {agent_id}",
                agent_id=agent_id,
                kind=kind,
                depends_on=support_tail,
                acceptance=("Support output is bounded, evidenced, and safe for the author.",),
            )
        )
        support_tail = (step_id,)

    author_step_ids: list[str] = []
    parallel_mode = route.mode in {
        OrchestrationMode.CONTROLLED_PARALLEL,
        OrchestrationMode.ORCHESTRATOR_WORKERS,
    }
    author_dependency = support_tail
    for index, agent_id in enumerate(author_ids):
        step_id = f"mock-{_slug(agent_id)}"
        dependencies = support_tail if parallel_mode else author_dependency
        critical = _critical_actions(task, route) if index == 0 else ()
        acceptance = ("The synthetic artifact satisfies the bounded request.",)
        if agent_id == "appsec-specialist":
            acceptance = (
                "Threats, trust boundaries, denied paths, and negative cases are explicit.",
            )
        steps.append(
            _make_step(
                catalog,
                step_id=step_id,
                title=f"Produce a bounded synthetic artifact with {agent_id}",
                agent_id=agent_id,
                kind=PlanStepKind.MOCK_EXECUTE,
                depends_on=dependencies,
                files=tuple(files_by_owner.get(agent_id, ())),
                acceptance=acceptance,
                critical_actions=critical,
            )
        )
        author_step_ids.append(step_id)
        if not parallel_mode:
            author_dependency = (step_id,)

    if not author_step_ids:
        agent_id = route.primary_agent_id
        step_id = f"analyze-{_slug(agent_id)}"
        steps.append(
            _make_step(
                catalog,
                step_id=step_id,
                title="Produce a bounded read-only analysis",
                agent_id=agent_id,
                kind=PlanStepKind.ANALYZE,
                depends_on=support_tail,
                acceptance=("The analysis cites concrete evidence and limitations.",),
                critical_actions=_critical_actions(task, route),
            )
        )
        author_step_ids.append(step_id)

    terminal_ids: list[str] = []
    for reviewer_id in reviewer_ids:
        eligible_targets = author_step_ids
        if reviewer_id == "independent-visual-evaluator":
            eligible_targets = [
                step.id
                for step in steps
                if step.agent_id == "premium-frontend-specialist"
                and step.kind is PlanStepKind.MOCK_EXECUTE
            ]
        for target_id in eligible_targets:
            review_id = f"review-{_slug(reviewer_id)}-{_slug(target_id)}"
            review_acceptance = (
                "Findings cite a criterion, evidence, and required change.",
            )
            if reviewer_id == "independent-visual-evaluator":
                review_acceptance = (
                    "Desktop, mobile, states, and visual accessibility are evaluated.",
                )
            steps.append(
                _make_step(
                    catalog,
                    step_id=review_id,
                    title=f"Evaluate {target_id} independently",
                    agent_id=reviewer_id,
                    kind=PlanStepKind.EVALUATE,
                    depends_on=(target_id,),
                    acceptance=review_acceptance,
                    evaluates_step_id=target_id,
                )
            )
            terminal_ids.append(review_id)
    if not terminal_ids:
        terminal_ids.extend(author_step_ids)

    if "documentation-handoff-specialist" in participants:
        steps.append(
            _make_step(
                catalog,
                step_id="record-handoff",
                title="Record a bounded persistent handoff",
                agent_id="documentation-handoff-specialist",
                kind=PlanStepKind.HANDOFF,
                depends_on=tuple(terminal_ids),
                acceptance=("The next block, evidence, gaps, risks, and rollback are explicit.",),
            )
        )
        terminal_ids = ["record-handoff"]

    if "technical-director-orchestrator" in participants:
        steps.append(
            _make_step(
                catalog,
                step_id="integrate-result",
                title="Integrate reviewed results",
                agent_id="technical-director-orchestrator",
                kind=PlanStepKind.INTEGRATE,
                depends_on=tuple(terminal_ids),
                acceptance=("The accountable integrator preserves gates and evidence.",),
            )
        )

    parallel_groups: tuple[tuple[str, ...], ...] = ()
    if route.mode is OrchestrationMode.CONTROLLED_PARALLEL and len(author_step_ids) > 1:
        parallel_groups = (tuple(author_step_ids),)
    return steps, parallel_groups


def build_plan(
    task: TaskEnvelope,
    route: RoutingDecision,
    catalog: AgentCatalog,
) -> ExecutionPlan:
    """Build a small DAG; it describes work but never performs filesystem access."""

    files_by_owner: dict[str, list[str]] = defaultdict(list)
    for path in task.facts.candidate_files:
        files_by_owner[_owner_for_path(path, route)].append(path)

    full_stack = route.mode is OrchestrationMode.SEQUENTIAL_PIPELINE and {
        "product-requirements-analyst",
        "saas-architect",
        "backend-api-engineer",
        "premium-frontend-specialist",
        "independent-visual-evaluator",
    }.issubset(route.participant_agent_ids)
    if full_stack:
        steps = _append_full_stack_steps(task, route, catalog, files_by_owner)
        parallel_groups: tuple[tuple[str, ...], ...] = ()
    else:
        steps, parallel_groups = _append_generic_steps(
            task,
            route,
            catalog,
            files_by_owner,
        )

    planned_agents = {step.agent_id for step in steps}
    missing_agents = set(route.participant_agent_ids) - planned_agents
    if missing_agents:
        raise ValueError(f"selected participants have no plan step: {sorted(missing_agents)}")

    integrator_id = (
        "technical-director-orchestrator"
        if "technical-director-orchestrator" in route.participant_agent_ids
        else route.primary_agent_id
    )
    approval_required = route.human_approval_required or bool(_critical_actions(task, route))
    return ExecutionPlan(
        routing=route,
        integrator_agent_id=integrator_id,
        steps=tuple(steps),
        limits=_limits_for(route.mode, steps, catalog),
        parallel_groups=parallel_groups,
        approval_required=approval_required,
    )
