"""Closed Pydantic contracts used by the reference runtime."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


WINDOWS_RESERVED_NAMES = {
    "aux",
    "con",
    "nul",
    "prn",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}


class SafeModel(BaseModel):
    """Default contract: immutable, closed, and whitespace-normalized."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class Complexity(StrEnum):
    TRIVIAL = "TRIVIAL"
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    COMPLEX = "COMPLEX"
    LONG_RUNNING = "LONG_RUNNING"


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class OrchestrationMode(StrEnum):
    SINGLE_SPECIALIST = "SINGLE_SPECIALIST"
    SPECIALIST_PLUS_REVIEWER = "SPECIALIST_PLUS_REVIEWER"
    SEQUENTIAL_PIPELINE = "SEQUENTIAL_PIPELINE"
    ORCHESTRATOR_WORKERS = "ORCHESTRATOR_WORKERS"
    CONTROLLED_PARALLEL = "CONTROLLED_PARALLEL"
    EVALUATOR_OPTIMIZER_LOOP = "EVALUATOR_OPTIMIZER_LOOP"
    LONG_RUNNING_INCREMENTAL = "LONG_RUNNING_INCREMENTAL"
    INCIDENT_MODE = "INCIDENT_MODE"
    RELEASE_MODE = "RELEASE_MODE"


class StopReason(StrEnum):
    PASS = "PASS"
    MAX_ROUNDS = "MAX_ROUNDS"
    TIMEOUT = "TIMEOUT"
    BUDGET_LIMIT = "BUDGET_LIMIT"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    SECURITY_BLOCK = "SECURITY_BLOCK"
    ENVIRONMENT_BLOCK = "ENVIRONMENT_BLOCK"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    SCOPE_CHANGE = "SCOPE_CHANGE"


class AccessMode(StrEnum):
    READ = "READ"
    WRITE = "WRITE"


class PlanStepKind(StrEnum):
    ANALYZE = "ANALYZE"
    PLAN = "PLAN"
    MOCK_EXECUTE = "MOCK_EXECUTE"
    EVALUATE = "EVALUATE"
    INTEGRATE = "INTEGRATE"
    HANDOFF = "HANDOFF"


class CriticalAction(StrEnum):
    MERGE = "MERGE"
    DEPLOY = "DEPLOY"
    PRODUCTION = "PRODUCTION"
    MIGRATION = "MIGRATION"
    REAL_DATABASE = "REAL_DATABASE"
    PAYMENT = "PAYMENT"
    REAL_MESSAGE = "REAL_MESSAGE"
    EXTERNAL_PROVIDER = "EXTERNAL_PROVIDER"
    SECURITY_CRITICAL = "SECURITY_CRITICAL"
    PRIVATE_DATA = "PRIVATE_DATA"
    DESTRUCTIVE_ACTION = "DESTRUCTIVE_ACTION"


class EvaluationVerdict(StrEnum):
    PASS = "PASS"
    REVISE = "REVISE"
    BLOCK = "BLOCK"


class ArtifactStatus(StrEnum):
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class TraceEventName(StrEnum):
    RUN_STARTED = "RUN_STARTED"
    STEP_COMPLETED = "STEP_COMPLETED"
    EVALUATION_COMPLETED = "EVALUATION_COMPLETED"
    RUN_STOPPED = "RUN_STOPPED"


class TraceOutcome(StrEnum):
    STARTED = "STARTED"
    PASS = "PASS"
    REVISE = "REVISE"
    BLOCKED = "BLOCKED"
    STOPPED = "STOPPED"


class TraceErrorCategory(StrEnum):
    NONE = "NONE"
    VALIDATION = "VALIDATION"
    APPROVAL = "APPROVAL"
    SECURITY = "SECURITY"
    ENVIRONMENT = "ENVIRONMENT"
    BUDGET = "BUDGET"
    TIMEOUT = "TIMEOUT"
    UNKNOWN = "UNKNOWN"


class AllowedAction(StrEnum):
    ANALYZE = "ANALYZE"
    PLAN = "PLAN"
    MOCK_EXECUTE = "MOCK_EXECUTE"
    EVALUATE = "EVALUATE"
    INTEGRATE = "INTEGRATE"
    HANDOFF = "HANDOFF"
    TRACE_SAFE_LOCAL = "TRACE_SAFE_LOCAL"


class ExternalContext(SafeModel):
    origin: Literal["file", "web", "issue", "message"]
    content: str = Field(min_length=1, max_length=8_000)
    trusted: Literal[False] = False


class RuntimePolicy(SafeModel):
    shell_allowed: Literal[False] = False
    git_allowed: Literal[False] = False
    database_allowed: Literal[False] = False
    deployment_allowed: Literal[False] = False
    real_messages_allowed: Literal[False] = False
    real_project_access_allowed: Literal[False] = False
    external_provider_allowed: bool = False
    human_approval_reference: str | None = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def validate_external_provider_gate(self) -> RuntimePolicy:
        if self.external_provider_allowed and not self.human_approval_reference:
            raise ValueError("external provider access requires a human approval reference")
        return self


def normalize_relative_path(value: str) -> str:
    """Normalize a modeled project path without touching the filesystem."""

    text = value.strip().replace("\\", "/")
    path = PurePosixPath(text)
    if not text or path.is_absolute() or text.startswith("//"):
        raise ValueError("path must be relative")
    if any(marker in text for marker in ("*", "?", "[", "]", "{", "}")):
        raise ValueError("path cannot contain glob syntax")
    if any(character in text for character in ('<', '>', '"', '|')):
        raise ValueError("path contains a character forbidden by Windows")
    if ":" in text or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("path contains an unsafe segment")
    for part in path.parts:
        if part.rstrip(" .") != part or any(ord(char) < 32 for char in part):
            raise ValueError("path contains a Windows-ambiguous segment")
        if part.split(".", 1)[0].casefold() in WINDOWS_RESERVED_NAMES:
            raise ValueError("path contains a reserved Windows device name")
    return path.as_posix()


def canonical_path_key(value: str) -> str:
    """Return a Windows-safe comparison key while preserving the display path."""

    return normalize_relative_path(value).casefold()


class TaskFacts(SafeModel):
    detected_stacks: tuple[str, ...] = ()
    affected_areas: tuple[str, ...] = ()
    candidate_files: tuple[str, ...] = ()
    migration: bool = False
    security_sensitive: bool = False
    release_related: bool = False
    incident: bool = False
    long_running: bool = False
    independent_workstreams: bool = False

    @field_validator("candidate_files")
    @classmethod
    def validate_candidate_files(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(normalize_relative_path(value) for value in values)
        if len({canonical_path_key(value) for value in normalized}) != len(normalized):
            raise ValueError("candidate files must be unique")
        return normalized


class TaskEnvelope(SafeModel):
    request_id: UUID = Field(default_factory=uuid4)
    objective: str = Field(min_length=1, max_length=4_000)
    facts: TaskFacts = Field(default_factory=TaskFacts)
    external_context: tuple[ExternalContext, ...] = ()
    policy: RuntimePolicy = Field(default_factory=RuntimePolicy)


class AgentDefinition(SafeModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9-]*$", max_length=80)
    name: str = Field(min_length=3, max_length=120)
    capabilities: tuple[str, ...] = Field(min_length=1)
    associated_skills: tuple[str, ...] = ()
    allowed_actions: tuple[AllowedAction, ...] = Field(min_length=1)
    risk_level: RiskLevel
    max_rounds: int = Field(ge=1, le=3)
    can_author: bool = True
    can_evaluate: bool = False
    can_integrate: bool = False


class AgentCatalog(SafeModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    agents: tuple[AgentDefinition, ...]

    @model_validator(mode="after")
    def validate_unique_agents(self) -> AgentCatalog:
        ids = [agent.id for agent in self.agents]
        if len(set(ids)) != len(ids):
            raise ValueError("agent ids must be unique")
        return self

    def get(self, agent_id: str) -> AgentDefinition:
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        raise KeyError(f"unknown agent: {agent_id}")


class RoutingDecision(SafeModel):
    complexity: Complexity
    risk_level: RiskLevel
    mode: OrchestrationMode
    primary_agent_id: str
    participant_agent_ids: tuple[str, ...] = Field(min_length=1)
    reviewer_agent_id: str | None = None
    reasons: tuple[str, ...] = Field(min_length=1)
    human_approval_required: bool = False

    @model_validator(mode="after")
    def validate_participants(self) -> RoutingDecision:
        if len(set(self.participant_agent_ids)) != len(self.participant_agent_ids):
            raise ValueError("participants must be unique")
        if self.primary_agent_id not in self.participant_agent_ids:
            raise ValueError("primary agent must be a participant")
        if self.reviewer_agent_id is not None:
            if self.reviewer_agent_id == self.primary_agent_id:
                raise ValueError("author and reviewer must differ")
            if self.reviewer_agent_id not in self.participant_agent_ids:
                raise ValueError("reviewer must be a participant")
        return self


class FileClaim(SafeModel):
    path: str
    owner_agent_id: str
    access: AccessMode

    @field_validator("path")
    @classmethod
    def validate_path(cls, value: str) -> str:
        return normalize_relative_path(value)


class PlanStep(SafeModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9-]*$", max_length=80)
    title: str = Field(min_length=3, max_length=160)
    agent_id: str
    kind: PlanStepKind
    depends_on: tuple[str, ...] = ()
    file_claims: tuple[FileClaim, ...] = ()
    acceptance_criteria: tuple[str, ...] = Field(min_length=1)
    validation_commands: tuple[str, ...] = ()
    critical_actions: tuple[CriticalAction, ...] = ()
    evaluates_step_id: str | None = None

    @model_validator(mode="after")
    def validate_evaluation_target(self) -> PlanStep:
        if self.kind is PlanStepKind.EVALUATE and self.evaluates_step_id is None:
            raise ValueError("evaluation steps require a target")
        if self.kind is not PlanStepKind.EVALUATE and self.evaluates_step_id is not None:
            raise ValueError("only evaluation steps may have a target")
        return self


class LoopLimits(SafeModel):
    max_rounds: int = Field(default=3, ge=1, le=3)
    max_turns: int = Field(
        default=3,
        ge=1,
        le=3,
        description="Maximum turns per delegated provider invocation.",
    )
    timeout_seconds: float = Field(default=60.0, gt=0, le=3_600)
    budget_units: int = Field(default=20, ge=1, le=1_000)
    max_provider_calls: int = Field(default=20, ge=1, le=100)


class ExecutionPlan(SafeModel):
    plan_id: UUID = Field(default_factory=uuid4)
    routing: RoutingDecision
    integrator_agent_id: str
    steps: tuple[PlanStep, ...] = Field(min_length=1)
    limits: LoopLimits = Field(default_factory=LoopLimits)
    parallel_groups: tuple[tuple[str, ...], ...] = ()
    approval_required: bool = False

    @model_validator(mode="after")
    def validate_plan(self) -> ExecutionPlan:
        by_id = {step.id: step for step in self.steps}
        if len(by_id) != len(self.steps):
            raise ValueError("step ids must be unique")
        if self.integrator_agent_id not in self.routing.participant_agent_ids:
            raise ValueError("integrator must be a participant")

        for step in self.steps:
            if step.agent_id not in self.routing.participant_agent_ids:
                raise ValueError(f"step agent is not a participant: {step.agent_id}")
            if any(claim.owner_agent_id != step.agent_id for claim in step.file_claims):
                raise ValueError("a step may claim files only for its own agent")
            for dependency in step.depends_on:
                if dependency not in by_id or dependency == step.id:
                    raise ValueError(f"invalid dependency: {dependency}")
            if step.kind is PlanStepKind.EVALUATE:
                target = by_id.get(step.evaluates_step_id or "")
                if target is None:
                    raise ValueError("evaluation target does not exist")
                if target.agent_id == step.agent_id:
                    raise ValueError("an author cannot evaluate their own step")

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(step_id: str) -> None:
            if step_id in visiting:
                raise ValueError("plan dependencies contain a cycle")
            if step_id in visited:
                return
            visiting.add(step_id)
            for dependency in by_id[step_id].depends_on:
                visit(dependency)
            visiting.remove(step_id)
            visited.add(step_id)

        for step_id in by_id:
            visit(step_id)

        write_owners: dict[str, str] = {}
        for step in self.steps:
            for claim in step.file_claims:
                if claim.access is AccessMode.WRITE:
                    path_key = canonical_path_key(claim.path)
                    owner = write_owners.setdefault(path_key, claim.owner_agent_id)
                    if owner != claim.owner_agent_id:
                        raise ValueError(f"multiple writers for {claim.path}")

        for group in self.parallel_groups:
            if len(set(group)) != len(group) or any(step_id not in by_id for step_id in group):
                raise ValueError("parallel group contains an invalid step")
            group_paths: set[str] = set()
            for step_id in group:
                paths = {
                    canonical_path_key(claim.path)
                    for claim in by_id[step_id].file_claims
                    if claim.access is AccessMode.WRITE
                }
                if group_paths.intersection(paths):
                    raise ValueError("parallel steps have overlapping writes")
                group_paths.update(paths)

        has_critical_action = any(step.critical_actions for step in self.steps)
        if has_critical_action and not self.approval_required:
            raise ValueError("critical actions require human approval")
        if self.approval_required and not has_critical_action:
            raise ValueError("human approval requires an explicit critical step")
        if self.routing.human_approval_required and not self.approval_required:
            raise ValueError("routing gate must be preserved in the plan")
        return self


class ExecutionArtifact(SafeModel):
    step_id: str
    author_agent_id: str
    status: ArtifactStatus
    summary: str = Field(min_length=1, max_length=1_000)
    required_criteria: tuple[str, ...] = Field(min_length=1)
    completed_criteria: tuple[str, ...] = ()
    proposal_only: bool = False
    synthetic: Literal[True] = True

    @model_validator(mode="after")
    def validate_proposal_evidence(self) -> ExecutionArtifact:
        if self.proposal_only and self.completed_criteria:
            raise ValueError("proposal-only artifacts cannot claim completed criteria")
        return self


class EvaluationFinding(SafeModel):
    criterion: str = Field(min_length=1, max_length=300)
    evidence: str = Field(min_length=1, max_length=500)
    required_change: str = Field(min_length=1, max_length=500)
    severity: RiskLevel = RiskLevel.MEDIUM


class EvaluationResult(SafeModel):
    target_step_id: str
    author_agent_id: str
    evaluator_agent_id: str
    verdict: EvaluationVerdict
    findings: tuple[EvaluationFinding, ...] = ()
    block_reason: StopReason | None = None

    @model_validator(mode="after")
    def validate_independent_evaluation(self) -> EvaluationResult:
        if self.author_agent_id == self.evaluator_agent_id:
            raise ValueError("an author cannot approve their own work")
        if self.verdict is EvaluationVerdict.REVISE and not self.findings:
            raise ValueError("revision requires concrete findings")
        if self.verdict is EvaluationVerdict.BLOCK and not self.findings:
            raise ValueError("blocked evaluation requires concrete findings")
        if self.verdict is EvaluationVerdict.PASS and self.findings:
            raise ValueError("passing evaluation cannot carry open findings")
        if self.verdict is EvaluationVerdict.BLOCK and self.block_reason is None:
            raise ValueError("blocked evaluation requires a stop reason")
        if self.verdict is not EvaluationVerdict.BLOCK and self.block_reason is not None:
            raise ValueError("only blocked evaluations may carry a stop reason")
        return self


class LoopState(SafeModel):
    round_number: int = Field(ge=0, le=3)
    spent_budget_units: int = Field(ge=0)
    provider_calls: int = Field(ge=0)
    stop_reason: StopReason
    artifacts: tuple[ExecutionArtifact, ...] = ()
    evaluations: tuple[EvaluationResult, ...] = ()


class TestEvidence(SafeModel):
    command: str = Field(min_length=1, max_length=500)
    result: Literal["PASS", "FAIL", "NOT RUN", "BLOCKED"]
    evidence: str = Field(min_length=1, max_length=1_000)


class HandoffRecord(SafeModel):
    objective: str = Field(min_length=1, max_length=4_000)
    state: StopReason
    branch: Literal["NOT_APPLICABLE"] = "NOT_APPLICABLE"
    head: Literal["NOT_APPLICABLE"] = "NOT_APPLICABLE"
    changed_files: tuple[str, ...] = ()
    decisions: tuple[str, ...] = ()
    tests_executed: tuple[TestEvidence, ...] = ()
    not_executed: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    exact_next_block: str = Field(min_length=1, max_length=1_000)
    next_files_to_read: tuple[str, ...] = ()
    rollback: str = Field(min_length=1, max_length=1_000)
    context_limit: int = Field(default=4_000, ge=500, le=20_000)

    @field_validator("changed_files", "next_files_to_read")
    @classmethod
    def validate_handoff_paths(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(normalize_relative_path(value) for value in values)


class TraceEvent(SafeModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    event_name: TraceEventName
    run_id: UUID
    task_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    objective_chars: int = Field(ge=0, le=4_000)
    round_number: int = Field(ge=0, le=3)
    outcome: TraceOutcome
    error_category: TraceErrorCategory = TraceErrorCategory.NONE
    agent_id: str | None = Field(default=None, max_length=80)
    step_id: str | None = Field(default=None, max_length=80)


class RunResult(SafeModel):
    routing: RoutingDecision
    plan: ExecutionPlan
    loop: LoopState
    handoff: HandoffRecord
