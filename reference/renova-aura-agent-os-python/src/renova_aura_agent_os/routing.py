"""Auditable deterministic routing for normal Portuguese requests."""

from __future__ import annotations

import re
import unicodedata

from .models import (
    AgentCatalog,
    Complexity,
    OrchestrationMode,
    RiskLevel,
    RoutingDecision,
    StopReason,
    TaskEnvelope,
)
from .safety import critical_actions_from_objective


TECHNICAL_DIRECTOR = "technical-director-orchestrator"
TECHNICAL_REVIEWER = "independent-technical-reviewer"
VISUAL_REVIEWER = "independent-visual-evaluator"


class MissingAgentReference(RuntimeError):
    stop_reason = StopReason.MISSING_EVIDENCE


def _normalized_text(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text.casefold())
    return "".join(char for char in folded if not unicodedata.combining(char))


def _normalized_tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", _normalized_text(text)))


def _contains_phrase(text: str, *phrases: str) -> bool:
    normalized = _normalized_text(text)
    return any(phrase in normalized for phrase in phrases)


def _unique(*agent_ids: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(agent_ids))


def _validated_decision(catalog: AgentCatalog, **values: object) -> RoutingDecision:
    decision = RoutingDecision(**values)
    for agent_id in decision.participant_agent_ids:
        try:
            catalog.get(agent_id)
        except KeyError as exc:
            raise MissingAgentReference(f"required agent is unavailable: {agent_id}") from exc
    return decision


def _domain_author(
    *,
    python: bool,
    frontend: bool,
    database: bool,
    performance: bool,
    automation: bool,
) -> str:
    if performance:
        return "performance-engineer"
    if database:
        return "database-data-engineer"
    if frontend:
        return "premium-frontend-specialist"
    if python:
        return "python-engineer"
    if automation:
        return "ai-automation-specialist"
    return "backend-api-engineer"


def _candidate_owner(path: str) -> str:
    lowered = path.casefold().replace("\\", "/")
    if any(marker in lowered for marker in ("db/", "migration", "schema", ".sql")):
        return "database-data-engineer"
    if lowered.endswith(".py"):
        return "python-engineer"
    if any(marker in lowered for marker in ("app/api/", "api/", "server/", "route.ts")):
        return "backend-api-engineer"
    if any(marker in lowered for marker in ("ui/", "component", ".tsx", ".css", ".scss")):
        return "premium-frontend-specialist"
    return "backend-api-engineer"


def route_task(task: TaskEnvelope, catalog: AgentCatalog) -> RoutingDecision:
    """Choose the smallest safe team; external context is deliberately ignored."""

    tokens = _normalized_tokens(task.objective)
    critical_intent = bool(
        critical_actions_from_objective(
            task.objective,
            external_provider_allowed=task.policy.external_provider_allowed,
        )
    )
    areas = {_normalized_text(area) for area in task.facts.affected_areas}
    stacks = {_normalized_text(stack) for stack in task.facts.detected_stacks}
    candidate_paths = tuple(
        path.casefold().replace("\\", "/") for path in task.facts.candidate_files
    )
    file_database = any(
        any(marker in path for marker in ("db/", "database/", "supabase/", ".sql"))
        for path in candidate_paths
    )
    file_migration = any("migration" in path or "migrations/" in path for path in candidate_paths)
    file_python = any(path.endswith(".py") for path in candidate_paths)
    file_frontend = any(
        any(marker in path for marker in ("ui/", "component", ".tsx", ".css", ".scss"))
        for path in candidate_paths
    )
    file_backend = any(
        any(marker in path for marker in ("app/api/", "api/", "server/", "route.ts"))
        for path in candidate_paths
    )

    incident = task.facts.incident or bool(
        tokens & {"incidente", "outage", "indisponivel"}
    ) or _contains_phrase(task.objective, "fora do ar")
    release = task.facts.release_related or bool(
        tokens & {"release", "deploy", "merge", "pr", "producao", "production"}
    )
    security = task.facts.security_sensitive or bool(
        tokens
        & {
            "seguranca",
            "auth",
            "autenticacao",
            "autenticada",
            "autenticado",
            "autorizacao",
            "login",
            "sessao",
            "tenant",
            "owner",
            "rbac",
            "rls",
            "csrf",
            "ssrf",
            "upload",
            "segredo",
            "segredos",
            "vulnerabilidade",
            "appsec",
        }
    ) or _contains_phrase(
        task.objective,
        "api key",
        "credencial",
        "dados clinicos",
        "dados pessoais",
        "token de acesso",
        "token de autenticacao",
    )
    security_review_intent = bool(
        tokens & {"audite", "auditoria", "revise", "revisao", "analise", "verifique"}
    )
    migration = task.facts.migration or file_migration or bool(
        tokens & {"migration", "migrations", "migracao", "migracoes"}
    )
    python = file_python or bool(stacks & {"python", "fastapi"}) or bool(
        tokens & {"python", "fastapi", "django", "flask"}
    )
    frontend = file_frontend or bool(areas & {"frontend", "ui", "ux"}) or bool(
        tokens & {"frontend", "interface", "tela", "responsivo", "premium", "visual"}
    ) or _contains_phrase(task.objective, "design system", "token de design")
    backend = file_backend or bool(areas & {"backend", "api"}) or bool(
        tokens & {"backend", "api", "webhook", "endpoint", "servico", "server", "servidor"}
    )
    database = file_database or bool(areas & {"database", "banco", "dados", "schema"}) or bool(
        tokens & {"banco", "database", "schema", "postgresql", "supabase", "sql", "tabela"}
    )
    performance = bool(areas & {"performance", "desempenho"}) or bool(
        tokens & {"performance", "desempenho", "latencia", "bundle", "profiling", "otimize"}
    )
    automation = bool(
        tokens
        & {
            "automacao",
            "workflow",
            "n8n",
            "make",
            "mcp",
            "openai",
            "provider",
            "provedor",
            "llm",
            "rag",
        }
    ) or bool(
        _contains_phrase(task.objective, "agente de ia", "agente com ia", "ai agent")
    )
    full_stack = (frontend and backend) or _contains_phrase(
        task.objective,
        "front e back",
        "full stack",
        "full-stack",
        "funcionalidade completa",
        "ponta a ponta",
    )
    security_mutation = security and (
        full_stack
        or bool(
            tokens
            & {
                "adicione",
                "altere",
                "corrija",
                "corrigir",
                "crie",
                "criar",
                "implemente",
                "implementar",
                "mude",
                "refatore",
                "remova",
            }
        )
    )
    security_audit_only = security and security_review_intent and not security_mutation
    security_human_gate = security and not security_audit_only
    documentation = bool(tokens & {"documentacao", "handoff", "readme"})
    curation = bool(tokens & {"skill", "skills", "prompt", "prompts", "catalogo", "curadoria"})
    technical_context = bool(areas or stacks) or bool(
        tokens
        & {
            "codigo",
            "endpoint",
            "api",
            "frontend",
            "backend",
            "runtime",
            "aplicacao",
            "server",
            "servidor",
        }
    )
    bug = bool(tokens & {"bug", "regressao", "crash", "excecao"}) or (
        technical_context and bool(tokens & {"erro", "falha", "corrija", "corrigir"})
    )
    independent_review = _contains_phrase(
        task.objective,
        "revisao independente",
        "revise independentemente",
        "revisor independente",
    )
    team_requested = _contains_phrase(
        task.objective,
        "monte uma equipe",
        "use varios agentes",
        "varios agentes",
        "cada agente faz uma parte",
        "equipe multiagente",
    )
    loop_requested = _contains_phrase(
        task.objective,
        "trabalhe em loop",
        "execute um loop",
        "loop de qualidade",
        "ate ficar bom",
    )
    parallel_requested = "paralelo" in tokens or "paralelamente" in tokens
    long_running = task.facts.long_running or _contains_phrase(
        task.objective,
        "varias etapas",
        "varias sessoes",
        "trabalho longo",
        "continue trabalhando",
        "continue de onde",
    )
    python_project = python and (
        bool(tokens & {"completo", "completa"})
        or _contains_phrase(task.objective, "projeto python completo")
    )

    if incident:
        return _validated_decision(
            catalog,
            complexity=Complexity.COMPLEX,
            risk_level=RiskLevel.CRITICAL,
            mode=OrchestrationMode.INCIDENT_MODE,
            primary_agent_id="observability-incident-engineer",
            participant_agent_ids=(
                "observability-incident-engineer",
                "appsec-specialist",
                TECHNICAL_REVIEWER,
                TECHNICAL_DIRECTOR,
            ),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Incident evidence takes precedence.", "Non-essential change is frozen."),
            human_approval_required=critical_intent,
        )

    if release:
        return _validated_decision(
            catalog,
            complexity=Complexity.COMPLEX,
            risk_level=RiskLevel.CRITICAL,
            mode=OrchestrationMode.RELEASE_MODE,
            primary_agent_id="platform-release-engineer",
            participant_agent_ids=(
                "platform-release-engineer",
                "quality-test-engineer",
                "appsec-specialist",
                TECHNICAL_REVIEWER,
                TECHNICAL_DIRECTOR,
            ),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Release work prepares evidence but preserves merge and deploy gates.",),
            human_approval_required=True,
        )

    if migration and not full_stack:
        return _validated_decision(
            catalog,
            complexity=Complexity.COMPLEX,
            risk_level=RiskLevel.CRITICAL,
            mode=OrchestrationMode.SEQUENTIAL_PIPELINE,
            primary_agent_id="database-data-engineer",
            participant_agent_ids=(
                "database-data-engineer",
                "appsec-specialist",
                "quality-test-engineer",
                TECHNICAL_REVIEWER,
                TECHNICAL_DIRECTOR,
            ),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("A migration requires sequential review and a human gate.",),
            human_approval_required=True,
        )

    if full_stack:
        participants = [
            TECHNICAL_DIRECTOR,
            "product-requirements-analyst",
            "saas-architect",
        ]
        if database:
            participants.append("database-data-engineer")
        participants.append("backend-api-engineer")
        if python:
            participants.append("python-engineer")
        participants.extend(
            (
                "premium-frontend-specialist",
                "ux-accessibility-specialist",
            )
        )
        if security or migration:
            participants.append("appsec-specialist")
        participants.extend(("quality-test-engineer", TECHNICAL_REVIEWER, VISUAL_REVIEWER))
        return _validated_decision(
            catalog,
            complexity=Complexity.COMPLEX,
            risk_level=RiskLevel.CRITICAL if migration else RiskLevel.HIGH,
            mode=OrchestrationMode.SEQUENTIAL_PIPELINE,
            primary_agent_id=TECHNICAL_DIRECTOR,
            participant_agent_ids=tuple(participants),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Full-stack scope requires ordered contracts and independent reviews.",),
            human_approval_required=migration or security_human_gate or critical_intent,
        )

    author_id = _domain_author(
        python=python,
        frontend=frontend,
        database=database,
        performance=performance,
        automation=automation,
    )

    if long_running:
        participants = [
            TECHNICAL_DIRECTOR,
            author_id,
            "documentation-handoff-specialist",
            TECHNICAL_REVIEWER,
        ]
        if frontend:
            participants.extend(("ux-accessibility-specialist", VISUAL_REVIEWER))
        if security:
            participants.append("appsec-specialist")
        return _validated_decision(
            catalog,
            complexity=Complexity.LONG_RUNNING,
            risk_level=RiskLevel.HIGH,
            mode=OrchestrationMode.LONG_RUNNING_INCREMENTAL,
            primary_agent_id=TECHNICAL_DIRECTOR,
            participant_agent_ids=_unique(*participants),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Long work requires bounded blocks and persistent handoff.",),
            human_approval_required=security_human_gate or critical_intent,
        )

    if loop_requested:
        reviewer_id = VISUAL_REVIEWER if frontend else TECHNICAL_REVIEWER
        participants = [TECHNICAL_DIRECTOR, author_id, reviewer_id]
        if automation or security:
            participants.extend(("appsec-specialist", "quality-test-engineer"))
        return _validated_decision(
            catalog,
            complexity=Complexity.MEDIUM,
            risk_level=RiskLevel.HIGH if security or automation else RiskLevel.MEDIUM,
            mode=OrchestrationMode.EVALUATOR_OPTIMIZER_LOOP,
            primary_agent_id=author_id,
            participant_agent_ids=_unique(*participants),
            reviewer_agent_id=reviewer_id,
            reasons=("The requested loop is bounded and uses an independent evaluator.",),
            human_approval_required=security_human_gate or critical_intent,
        )

    if parallel_requested:
        parallel_owners = tuple(
            dict.fromkeys(_candidate_owner(path) for path in task.facts.candidate_files)
        )
        safe_parallel = (
            task.facts.independent_workstreams
            and len(task.facts.candidate_files) >= 2
            and len(parallel_owners) >= 2
            and not (security or database)
        )
        mode = (
            OrchestrationMode.CONTROLLED_PARALLEL
            if safe_parallel
            else OrchestrationMode.SEQUENTIAL_PIPELINE
        )
        if safe_parallel:
            participant_list = [TECHNICAL_DIRECTOR, *parallel_owners]
            if "premium-frontend-specialist" in parallel_owners:
                participant_list.extend(("ux-accessibility-specialist", VISUAL_REVIEWER))
            participant_list.append(TECHNICAL_REVIEWER)
            participants = _unique(*participant_list)
        else:
            participant_list = [TECHNICAL_DIRECTOR, author_id]
            if security:
                participant_list.append("appsec-specialist")
            participant_list.append(TECHNICAL_REVIEWER)
            participants = _unique(*participant_list)
        return _validated_decision(
            catalog,
            complexity=Complexity.COMPLEX,
            risk_level=RiskLevel.HIGH,
            mode=mode,
            primary_agent_id=TECHNICAL_DIRECTOR,
            participant_agent_ids=participants,
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=(
                (
                    "Parallel work is allowed only with distinct preassigned files."
                    if safe_parallel
                    else "Parallel work was downgraded because exclusive ownership is unproven."
                ),
            ),
            human_approval_required=security_human_gate or critical_intent,
        )

    if team_requested:
        participants = [TECHNICAL_DIRECTOR, author_id]
        if security:
            participants.append("appsec-specialist")
        participants.append(TECHNICAL_REVIEWER)
        return _validated_decision(
            catalog,
            complexity=Complexity.COMPLEX,
            risk_level=RiskLevel.HIGH,
            mode=OrchestrationMode.ORCHESTRATOR_WORKERS,
            primary_agent_id=TECHNICAL_DIRECTOR,
            participant_agent_ids=_unique(*participants),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("The explicit team request is reduced to the smallest useful team.",),
            human_approval_required=security_human_gate or critical_intent,
        )

    if security:
        return _validated_decision(
            catalog,
            complexity=Complexity.MEDIUM,
            risk_level=RiskLevel.HIGH,
            mode=OrchestrationMode.SPECIALIST_PLUS_REVIEWER,
            primary_agent_id="appsec-specialist",
            participant_agent_ids=("appsec-specialist", TECHNICAL_REVIEWER),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Security-sensitive work takes precedence over convenience.",),
            human_approval_required=security_human_gate or critical_intent,
        )

    if performance and database:
        return _validated_decision(
            catalog,
            complexity=Complexity.COMPLEX,
            risk_level=RiskLevel.HIGH,
            mode=OrchestrationMode.SEQUENTIAL_PIPELINE,
            primary_agent_id="performance-engineer",
            participant_agent_ids=(
                "performance-engineer",
                "database-data-engineer",
                "observability-incident-engineer",
                "quality-test-engineer",
                TECHNICAL_REVIEWER,
                TECHNICAL_DIRECTOR,
            ),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Measured SQL performance needs database ownership and remeasurement.",),
            human_approval_required=critical_intent,
        )

    if database:
        return _validated_decision(
            catalog,
            complexity=Complexity.MEDIUM,
            risk_level=RiskLevel.HIGH,
            mode=OrchestrationMode.SEQUENTIAL_PIPELINE,
            primary_agent_id="database-data-engineer",
            participant_agent_ids=(
                "database-data-engineer",
                "appsec-specialist",
                "quality-test-engineer",
                TECHNICAL_REVIEWER,
                TECHNICAL_DIRECTOR,
            ),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Data integrity needs database ownership and negative review.",),
            human_approval_required=critical_intent,
        )

    if performance:
        return _validated_decision(
            catalog,
            complexity=Complexity.MEDIUM,
            risk_level=RiskLevel.HIGH,
            mode=OrchestrationMode.SPECIALIST_PLUS_REVIEWER,
            primary_agent_id="performance-engineer",
            participant_agent_ids=(
                "performance-engineer",
                "observability-incident-engineer",
                "quality-test-engineer",
                TECHNICAL_REVIEWER,
            ),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Performance work requires a baseline and comparable remeasurement.",),
            human_approval_required=critical_intent,
        )

    if automation:
        return _validated_decision(
            catalog,
            complexity=Complexity.COMPLEX,
            risk_level=RiskLevel.HIGH,
            mode=OrchestrationMode.SEQUENTIAL_PIPELINE,
            primary_agent_id="ai-automation-specialist",
            participant_agent_ids=(
                "ai-automation-specialist",
                "appsec-specialist",
                "observability-incident-engineer",
                "quality-test-engineer",
                TECHNICAL_REVIEWER,
                TECHNICAL_DIRECTOR,
            ),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Automation stays mock-first with security and quality evidence.",),
            human_approval_required=critical_intent,
        )

    if independent_review:
        review_agent = VISUAL_REVIEWER if frontend or "visual" in tokens else TECHNICAL_REVIEWER
        return _validated_decision(
            catalog,
            complexity=Complexity.SMALL,
            risk_level=RiskLevel.MEDIUM,
            mode=OrchestrationMode.SINGLE_SPECIALIST,
            primary_agent_id=review_agent,
            participant_agent_ids=(review_agent,),
            reasons=("The request is itself an independent read-only review.",),
            human_approval_required=critical_intent,
        )

    if bug:
        reviewer_id = VISUAL_REVIEWER if frontend else TECHNICAL_REVIEWER
        return _validated_decision(
            catalog,
            complexity=Complexity.MEDIUM,
            risk_level=RiskLevel.MEDIUM,
            mode=OrchestrationMode.SPECIALIST_PLUS_REVIEWER,
            primary_agent_id=author_id,
            participant_agent_ids=_unique(author_id, "quality-test-engineer", reviewer_id),
            reviewer_agent_id=reviewer_id,
            reasons=("A bug fix requires reproduced evidence and regression review.",),
            human_approval_required=critical_intent,
        )

    if frontend:
        return _validated_decision(
            catalog,
            complexity=Complexity.MEDIUM,
            risk_level=RiskLevel.MEDIUM,
            mode=OrchestrationMode.SPECIALIST_PLUS_REVIEWER,
            primary_agent_id="premium-frontend-specialist",
            participant_agent_ids=(
                "premium-frontend-specialist",
                "ux-accessibility-specialist",
                VISUAL_REVIEWER,
            ),
            reviewer_agent_id=VISUAL_REVIEWER,
            reasons=("Visual work requires an independent visual evaluator.",),
            human_approval_required=critical_intent,
        )

    if python_project:
        return _validated_decision(
            catalog,
            complexity=Complexity.COMPLEX,
            risk_level=RiskLevel.HIGH,
            mode=OrchestrationMode.SEQUENTIAL_PIPELINE,
            primary_agent_id=TECHNICAL_DIRECTOR,
            participant_agent_ids=(
                TECHNICAL_DIRECTOR,
                "product-requirements-analyst",
                "python-engineer",
                "quality-test-engineer",
                TECHNICAL_REVIEWER,
            ),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("A complete Python project needs bounded requirements and review.",),
            human_approval_required=critical_intent,
        )

    if python:
        return _validated_decision(
            catalog,
            complexity=Complexity.SMALL,
            risk_level=RiskLevel.MEDIUM,
            mode=OrchestrationMode.SINGLE_SPECIALIST,
            primary_agent_id="python-engineer",
            participant_agent_ids=("python-engineer",),
            reasons=("Python is the dominant detected stack.",),
            human_approval_required=critical_intent,
        )

    if backend:
        return _validated_decision(
            catalog,
            complexity=Complexity.MEDIUM,
            risk_level=RiskLevel.MEDIUM,
            mode=OrchestrationMode.SPECIALIST_PLUS_REVIEWER,
            primary_agent_id="backend-api-engineer",
            participant_agent_ids=(
                "backend-api-engineer",
                "quality-test-engineer",
                TECHNICAL_REVIEWER,
            ),
            reviewer_agent_id=TECHNICAL_REVIEWER,
            reasons=("Backend work needs contract and regression evidence.",),
            human_approval_required=critical_intent,
        )

    if documentation:
        return _validated_decision(
            catalog,
            complexity=Complexity.SMALL,
            risk_level=RiskLevel.LOW,
            mode=OrchestrationMode.SINGLE_SPECIALIST,
            primary_agent_id="documentation-handoff-specialist",
            participant_agent_ids=("documentation-handoff-specialist",),
            reasons=("The request is bounded documentation or handoff work.",),
            human_approval_required=critical_intent,
        )

    if curation:
        return _validated_decision(
            catalog,
            complexity=Complexity.SMALL,
            risk_level=RiskLevel.MEDIUM,
            mode=OrchestrationMode.SINGLE_SPECIALIST,
            primary_agent_id="skills-agents-prompts-curator",
            participant_agent_ids=("skills-agents-prompts-curator",),
            reasons=("The request concerns reusable skills, agents, prompts, or catalogs.",),
            human_approval_required=critical_intent,
        )

    return _validated_decision(
        catalog,
        complexity=Complexity.SMALL,
        risk_level=RiskLevel.LOW,
        mode=OrchestrationMode.SINGLE_SPECIALIST,
        primary_agent_id="product-requirements-analyst",
        participant_agent_ids=("product-requirements-analyst",),
        reasons=("No cross-domain or critical-risk signal requires a larger team.",),
        human_approval_required=critical_intent,
    )
