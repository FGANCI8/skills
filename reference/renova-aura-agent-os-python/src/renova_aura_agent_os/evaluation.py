"""Independent deterministic evaluator with concrete revision findings."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from .models import (
    EvaluationFinding,
    EvaluationResult,
    EvaluationVerdict,
    ExecutionArtifact,
    PlanStep,
    RiskLevel,
    StopReason,
)


class Evaluator(Protocol):
    async def evaluate(
        self,
        evaluation_step: PlanStep,
        artifact: ExecutionArtifact,
    ) -> EvaluationResult:
        """Evaluate one artifact without side effects."""


class MockEvaluator:
    def __init__(
        self,
        scripted_outcomes: Iterable[EvaluationVerdict | StopReason] = (),
    ) -> None:
        self._outcomes = list(scripted_outcomes)
        self.calls = 0

    async def evaluate(
        self,
        evaluation_step: PlanStep,
        artifact: ExecutionArtifact,
    ) -> EvaluationResult:
        self.calls += 1
        outcome = self._outcomes.pop(0) if self._outcomes else EvaluationVerdict.PASS
        missing_criteria = tuple(
            criterion
            for criterion in artifact.required_criteria
            if criterion not in artifact.completed_criteria
        )
        if missing_criteria:
            return EvaluationResult(
                target_step_id=artifact.step_id,
                author_agent_id=artifact.author_agent_id,
                evaluator_agent_id=evaluation_step.agent_id,
                verdict=EvaluationVerdict.BLOCK,
                findings=(
                    EvaluationFinding(
                        criterion=missing_criteria[0],
                        evidence="The artifact returned no evidence for this required criterion.",
                        required_change="Return explicit evidence for every required criterion.",
                        severity=RiskLevel.HIGH,
                    ),
                ),
                block_reason=StopReason.MISSING_EVIDENCE,
            )
        if isinstance(outcome, StopReason):
            if outcome is StopReason.PASS:
                outcome = EvaluationVerdict.PASS
            else:
                return EvaluationResult(
                    target_step_id=artifact.step_id,
                    author_agent_id=artifact.author_agent_id,
                    evaluator_agent_id=evaluation_step.agent_id,
                    verdict=EvaluationVerdict.BLOCK,
                    findings=(
                        EvaluationFinding(
                            criterion=evaluation_step.acceptance_criteria[0],
                            evidence=f"The scripted evaluator stopped with {outcome.value}.",
                            required_change=(
                                "Resolve the terminal condition and provide new evidence."
                            ),
                            severity=RiskLevel.HIGH,
                        ),
                    ),
                    block_reason=outcome,
                )

        if outcome is EvaluationVerdict.REVISE:
            criterion = evaluation_step.acceptance_criteria[0]
            return EvaluationResult(
                target_step_id=artifact.step_id,
                author_agent_id=artifact.author_agent_id,
                evaluator_agent_id=evaluation_step.agent_id,
                verdict=EvaluationVerdict.REVISE,
                findings=(
                    EvaluationFinding(
                        criterion=criterion,
                        evidence="The scripted mock evidence does not yet satisfy the criterion.",
                        required_change="Revise the same bounded artifact and return new evidence.",
                        severity=RiskLevel.MEDIUM,
                    ),
                ),
            )

        if outcome is EvaluationVerdict.BLOCK:
            return EvaluationResult(
                target_step_id=artifact.step_id,
                author_agent_id=artifact.author_agent_id,
                evaluator_agent_id=evaluation_step.agent_id,
                verdict=EvaluationVerdict.BLOCK,
                findings=(
                    EvaluationFinding(
                        criterion=evaluation_step.acceptance_criteria[0],
                        evidence="The scripted security evaluation produced a blocking result.",
                        required_change="Resolve the security block and return negative evidence.",
                        severity=RiskLevel.CRITICAL,
                    ),
                ),
                block_reason=StopReason.SECURITY_BLOCK,
            )

        return EvaluationResult(
            target_step_id=artifact.step_id,
            author_agent_id=artifact.author_agent_id,
            evaluator_agent_id=evaluation_step.agent_id,
            verdict=EvaluationVerdict.PASS,
        )
