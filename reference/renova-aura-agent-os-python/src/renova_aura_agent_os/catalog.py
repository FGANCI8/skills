"""Sanitized reference projection of the 18-agent public catalog."""

from __future__ import annotations

from .models import AgentCatalog, AgentDefinition, AllowedAction, RiskLevel


AUTHOR_ACTIONS = (
    AllowedAction.ANALYZE,
    AllowedAction.PLAN,
    AllowedAction.MOCK_EXECUTE,
    AllowedAction.HANDOFF,
)
REVIEW_ACTIONS = (AllowedAction.ANALYZE, AllowedAction.EVALUATE, AllowedAction.HANDOFF)


def _agent(
    agent_id: str,
    name: str,
    capabilities: tuple[str, ...],
    skills: tuple[str, ...],
    risk: RiskLevel,
    *,
    max_rounds: int = 3,
    can_author: bool = True,
    can_evaluate: bool = False,
    can_integrate: bool = False,
) -> AgentDefinition:
    actions = REVIEW_ACTIONS if can_evaluate and not can_author else AUTHOR_ACTIONS
    if can_integrate:
        actions = (*actions, AllowedAction.INTEGRATE)
    if can_evaluate and AllowedAction.EVALUATE not in actions:
        actions = (*actions, AllowedAction.EVALUATE)
    return AgentDefinition(
        id=agent_id,
        name=name,
        capabilities=capabilities,
        associated_skills=skills,
        allowed_actions=actions,
        risk_level=risk,
        max_rounds=max_rounds,
        can_author=can_author,
        can_evaluate=can_evaluate,
        can_integrate=can_integrate,
    )


def build_reference_catalog() -> AgentCatalog:
    """Return generic metadata only; the repository YAML remains canonical."""

    return AgentCatalog(
        agents=(
            _agent(
                "technical-director-orchestrator",
                "Diretor técnico e orquestrador",
                ("routing", "orchestration", "integration", "approval-gates"),
                (
                    "renova-aura-router",
                    "renova-aura-agent-orchestrator",
                    "renova-aura-project-handoff",
                ),
                RiskLevel.HIGH,
                can_integrate=True,
            ),
            _agent(
                "product-requirements-analyst",
                "Analista de produto e requisitos",
                ("product", "requirements", "acceptance-criteria"),
                ("renova-aura-product-spec",),
                RiskLevel.MEDIUM,
                max_rounds=2,
            ),
            _agent(
                "saas-architect",
                "Arquiteto SaaS",
                ("architecture", "contracts", "identity", "system-boundaries"),
                ("renova-aura-saas-architect", "renova-aura-security-data-guardian"),
                RiskLevel.HIGH,
                max_rounds=2,
            ),
            _agent(
                "premium-frontend-specialist",
                "Especialista em front-end premium",
                ("frontend", "visual-design", "responsive-ui"),
                (
                    "renova-aura-premium-frontend",
                    "renova-aura-ux-design-system",
                    "renova-aura-engineering-guardian",
                ),
                RiskLevel.MEDIUM,
            ),
            _agent(
                "ux-accessibility-specialist",
                "Especialista em UX e acessibilidade",
                ("ux", "accessibility", "user-flows"),
                ("renova-aura-ux-design-system", "renova-aura-quality-release"),
                RiskLevel.MEDIUM,
                max_rounds=2,
            ),
            _agent(
                "backend-api-engineer",
                "Engenheiro backend e APIs",
                ("backend", "api", "services", "webhooks"),
                (
                    "renova-aura-backend-api-engineer",
                    "renova-aura-engineering-guardian",
                    "renova-aura-security-data-guardian",
                ),
                RiskLevel.HIGH,
                max_rounds=2,
            ),
            _agent(
                "database-data-engineer",
                "Engenheiro de banco e dados",
                ("database", "migrations", "integrity", "query-performance"),
                (
                    "renova-aura-database-reliability",
                    "renova-aura-security-data-guardian",
                    "renova-aura-quality-release",
                ),
                RiskLevel.CRITICAL,
                max_rounds=2,
            ),
            _agent(
                "appsec-specialist",
                "Especialista AppSec",
                ("security", "threat-model", "authorization", "prompt-injection"),
                ("renova-aura-security-data-guardian",),
                RiskLevel.CRITICAL,
                can_evaluate=True,
            ),
            _agent(
                "quality-test-engineer",
                "Engenheiro de qualidade e testes",
                ("quality", "tests", "negative-tests", "release-evidence"),
                ("renova-aura-quality-release",),
                RiskLevel.HIGH,
                can_evaluate=True,
            ),
            _agent(
                "independent-technical-reviewer",
                "Revisor técnico independente",
                ("technical-review", "evidence-review", "regression-review"),
                ("renova-aura-independent-reviewer", "renova-aura-quality-release"),
                RiskLevel.HIGH,
                can_author=False,
                can_evaluate=True,
            ),
            _agent(
                "independent-visual-evaluator",
                "Avaliador visual independente",
                ("visual-review", "responsive-review", "accessibility-review"),
                (
                    "renova-aura-independent-reviewer",
                    "renova-aura-premium-frontend",
                    "renova-aura-ux-design-system",
                ),
                RiskLevel.MEDIUM,
                can_author=False,
                can_evaluate=True,
            ),
            _agent(
                "performance-engineer",
                "Engenheiro de desempenho",
                ("performance", "profiling", "latency", "measurement"),
                (
                    "renova-aura-performance-engineering",
                    "renova-aura-observability-incident",
                    "renova-aura-quality-release",
                ),
                RiskLevel.HIGH,
            ),
            _agent(
                "platform-release-engineer",
                "Engenheiro de plataforma e release",
                ("platform", "release", "ci", "rollback"),
                ("renova-aura-quality-release", "renova-aura-observability-incident"),
                RiskLevel.HIGH,
                max_rounds=2,
            ),
            _agent(
                "observability-incident-engineer",
                "Engenheiro de observabilidade e incidentes",
                ("observability", "incident", "recovery", "tracing"),
                (
                    "renova-aura-observability-incident",
                    "renova-aura-security-data-guardian",
                ),
                RiskLevel.CRITICAL,
            ),
            _agent(
                "ai-automation-specialist",
                "Especialista em IA e automação",
                ("ai", "agents", "guardrails", "evals"),
                (
                    "renova-aura-ai-integration-guardian",
                    "renova-aura-security-data-guardian",
                    "renova-aura-observability-incident",
                ),
                RiskLevel.CRITICAL,
            ),
            _agent(
                "python-engineer",
                "Engenheiro Python",
                ("python", "typing", "pydantic", "packaging"),
                ("renova-aura-python-engineering", "renova-aura-engineering-guardian"),
                RiskLevel.HIGH,
                max_rounds=2,
            ),
            _agent(
                "documentation-handoff-specialist",
                "Especialista em documentação e handoff",
                ("documentation", "handoff", "continuity"),
                ("renova-aura-project-handoff",),
                RiskLevel.MEDIUM,
                max_rounds=1,
            ),
            _agent(
                "skills-agents-prompts-curator",
                "Curador de skills, agentes e prompts",
                ("curation", "skills", "prompts", "catalog"),
                ("renova-aura-skill-library-curator", "renova-aura-prompt-source-designer"),
                RiskLevel.HIGH,
            ),
        )
    )
