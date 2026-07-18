"""Bounded evaluator-optimizer runtime with mandatory terminal states."""

from __future__ import annotations

import asyncio
import inspect
import time
from collections.abc import Callable

from .evaluation import Evaluator
from .execution import MockExecutor
from .models import (
    EvaluationVerdict,
    ExecutionArtifact,
    ExecutionPlan,
    LoopState,
    PlanStep,
    PlanStepKind,
    StopReason,
    TaskEnvelope,
    TraceErrorCategory,
    TraceEvent,
    TraceEventName,
    TraceOutcome,
)
from .providers.base import ProviderUnavailable
from .tracing import InMemoryTraceSink, TraceSink, task_fingerprint


def _ordered_steps(plan: ExecutionPlan) -> tuple[PlanStep, ...]:
    by_id = {step.id: step for step in plan.steps}
    ordered: list[PlanStep] = []
    visited: set[str] = set()

    def visit(step: PlanStep) -> None:
        if step.id in visited:
            return
        for dependency in step.depends_on:
            visit(by_id[dependency])
        visited.add(step.id)
        ordered.append(step)

    for candidate in plan.steps:
        visit(candidate)
    return tuple(ordered)


class BoundedLoopRunner:
    def __init__(
        self,
        executor: MockExecutor,
        evaluator: Evaluator,
        trace_sink: TraceSink | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.executor = executor
        self.evaluator = evaluator
        self.trace_sink = trace_sink or InMemoryTraceSink()
        self.clock = clock

    def _trace(
        self,
        task: TaskEnvelope,
        plan: ExecutionPlan,
        *,
        event_name: TraceEventName,
        round_number: int,
        outcome: TraceOutcome,
        error: TraceErrorCategory = TraceErrorCategory.NONE,
        agent_id: str | None = None,
        step_id: str | None = None,
    ) -> bool:
        try:
            self.trace_sink.emit(
                TraceEvent(
                    event_name=event_name,
                    run_id=plan.plan_id,
                    task_fingerprint=task_fingerprint(task.objective),
                    objective_chars=len(task.objective),
                    round_number=round_number,
                    outcome=outcome,
                    error_category=error,
                    agent_id=agent_id,
                    step_id=step_id,
                )
            )
        except Exception:
            return False
        return True

    def _terminal(
        self,
        task: TaskEnvelope,
        plan: ExecutionPlan,
        reason: StopReason,
        round_number: int,
        spent: int,
        calls: int,
        artifacts: list[ExecutionArtifact],
        evaluations: list,
        error: TraceErrorCategory = TraceErrorCategory.NONE,
    ) -> LoopState:
        self._trace(
            task,
            plan,
            event_name=TraceEventName.RUN_STOPPED,
            round_number=round_number,
            outcome=TraceOutcome.PASS if reason is StopReason.PASS else TraceOutcome.STOPPED,
            error=error,
        )
        return LoopState(
            round_number=round_number,
            spent_budget_units=spent,
            provider_calls=calls,
            stop_reason=reason,
            artifacts=tuple(artifacts),
            evaluations=tuple(evaluations),
        )

    async def run(self, task: TaskEnvelope, plan: ExecutionPlan) -> LoopState:
        start = self.clock()
        spent = 0
        calls = 0
        all_artifacts: list[ExecutionArtifact] = []
        all_evaluations: list = []
        revision_notes: dict[str, tuple[str, ...]] = {}

        trace_started = self._trace(
            task,
            plan,
            event_name=TraceEventName.RUN_STARTED,
            round_number=0,
            outcome=TraceOutcome.STARTED,
        )
        if not trace_started:
            return self._terminal(
                task,
                plan,
                StopReason.ENVIRONMENT_BLOCK,
                0,
                spent,
                calls,
                all_artifacts,
                all_evaluations,
                TraceErrorCategory.ENVIRONMENT,
            )

        has_critical_step = any(step.critical_actions for step in plan.steps)
        approval_contract_is_valid = (
            plan.approval_required == has_critical_step
            and (
                not plan.routing.human_approval_required
                or plan.approval_required
            )
        )
        if not approval_contract_is_valid:
            return self._terminal(
                task,
                plan,
                StopReason.HUMAN_APPROVAL_REQUIRED,
                0,
                spent,
                calls,
                all_artifacts,
                all_evaluations,
                TraceErrorCategory.APPROVAL,
            )

        ordered = _ordered_steps(plan)
        for round_number in range(1, plan.limits.max_rounds + 1):
            artifacts_this_round: dict[str, ExecutionArtifact] = {}
            revision_requested = False

            for step in ordered:
                if self.clock() - start >= plan.limits.timeout_seconds:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.TIMEOUT,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.TIMEOUT,
                    )

                if step.critical_actions:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.HUMAN_APPROVAL_REQUIRED,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.APPROVAL,
                    )

                if step.kind is PlanStepKind.EVALUATE:
                    target_id = step.evaluates_step_id or ""
                    artifact = artifacts_this_round.get(target_id)
                    if artifact is None:
                        return self._terminal(
                            task,
                            plan,
                            StopReason.MISSING_EVIDENCE,
                            round_number,
                            spent,
                            calls,
                            all_artifacts,
                            all_evaluations,
                            TraceErrorCategory.VALIDATION,
                        )
                    try:
                        if not inspect.iscoroutinefunction(self.evaluator.evaluate):
                            raise TypeError("evaluator must expose an async evaluate method")
                        remaining_seconds = plan.limits.timeout_seconds - (self.clock() - start)
                        if remaining_seconds <= 0:
                            raise TimeoutError
                        evaluation = await asyncio.wait_for(
                            self.evaluator.evaluate(step, artifact),
                            timeout=remaining_seconds,
                        )
                    except TimeoutError:
                        return self._terminal(
                            task,
                            plan,
                            StopReason.TIMEOUT,
                            round_number,
                            spent,
                            calls,
                            all_artifacts,
                            all_evaluations,
                            TraceErrorCategory.TIMEOUT,
                        )
                    except Exception:
                        return self._terminal(
                            task,
                            plan,
                            StopReason.ENVIRONMENT_BLOCK,
                            round_number,
                            spent,
                            calls,
                            all_artifacts,
                            all_evaluations,
                            TraceErrorCategory.ENVIRONMENT,
                        )
                    all_evaluations.append(evaluation)
                    trace_recorded = self._trace(
                        task,
                        plan,
                        event_name=TraceEventName.EVALUATION_COMPLETED,
                        round_number=round_number,
                        outcome=(
                            TraceOutcome.PASS
                            if evaluation.verdict is EvaluationVerdict.PASS
                            else TraceOutcome.REVISE
                            if evaluation.verdict is EvaluationVerdict.REVISE
                            else TraceOutcome.BLOCKED
                        ),
                        agent_id=step.agent_id,
                        step_id=step.id,
                    )
                    if not trace_recorded:
                        return self._terminal(
                            task,
                            plan,
                            StopReason.ENVIRONMENT_BLOCK,
                            round_number,
                            spent,
                            calls,
                            all_artifacts,
                            all_evaluations,
                            TraceErrorCategory.ENVIRONMENT,
                        )
                    if evaluation.verdict is EvaluationVerdict.BLOCK:
                        block_reason = evaluation.block_reason or StopReason.SECURITY_BLOCK
                        error_category = (
                            TraceErrorCategory.VALIDATION
                            if block_reason is StopReason.MISSING_EVIDENCE
                            else TraceErrorCategory.SECURITY
                        )
                        return self._terminal(
                            task,
                            plan,
                            block_reason,
                            round_number,
                            spent,
                            calls,
                            all_artifacts,
                            all_evaluations,
                            error_category,
                        )
                    if evaluation.verdict is EvaluationVerdict.REVISE:
                        revision_notes[target_id] = tuple(
                            finding.required_change for finding in evaluation.findings
                        )
                        revision_requested = True
                        break
                    continue

                if calls >= plan.limits.max_provider_calls:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.BUDGET_LIMIT,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.BUDGET,
                    )
                calls += 1
                try:
                    remaining_seconds = plan.limits.timeout_seconds - (self.clock() - start)
                    if remaining_seconds <= 0:
                        raise TimeoutError
                    artifact, cost = await asyncio.wait_for(
                        self.executor.execute(
                            task,
                            step,
                            revision_notes.get(step.id, ()),
                            plan.limits.max_turns,
                        ),
                        timeout=remaining_seconds,
                    )
                except TimeoutError:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.TIMEOUT,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.TIMEOUT,
                    )
                except ProviderUnavailable:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.ENVIRONMENT_BLOCK,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.ENVIRONMENT,
                    )
                except Exception:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.ENVIRONMENT_BLOCK,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.ENVIRONMENT,
                    )
                spent += cost
                if spent > plan.limits.budget_units:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.BUDGET_LIMIT,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.BUDGET,
                    )
                if artifact.proposal_only:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.MISSING_EVIDENCE,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.VALIDATION,
                    )
                missing_criteria = tuple(
                    criterion
                    for criterion in artifact.required_criteria
                    if criterion not in artifact.completed_criteria
                )
                if missing_criteria:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.MISSING_EVIDENCE,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.VALIDATION,
                    )
                artifacts_this_round[step.id] = artifact
                all_artifacts.append(artifact)
                trace_recorded = self._trace(
                    task,
                    plan,
                    event_name=TraceEventName.STEP_COMPLETED,
                    round_number=round_number,
                    outcome=TraceOutcome.PASS,
                    agent_id=step.agent_id,
                    step_id=step.id,
                )
                if not trace_recorded:
                    return self._terminal(
                        task,
                        plan,
                        StopReason.ENVIRONMENT_BLOCK,
                        round_number,
                        spent,
                        calls,
                        all_artifacts,
                        all_evaluations,
                        TraceErrorCategory.ENVIRONMENT,
                    )

            if not revision_requested:
                return self._terminal(
                    task,
                    plan,
                    StopReason.PASS,
                    round_number,
                    spent,
                    calls,
                    all_artifacts,
                    all_evaluations,
                )

        return self._terminal(
            task,
            plan,
            StopReason.MAX_ROUNDS,
            plan.limits.max_rounds,
            spent,
            calls,
            all_artifacts,
            all_evaluations,
        )
