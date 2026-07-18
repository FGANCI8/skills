"""Mock executor that cannot access tools, projects, shell, Git, or network."""

from __future__ import annotations

from .models import ArtifactStatus, ExecutionArtifact, PlanStep, TaskEnvelope
from .providers.base import Provider, ProviderRequest
from .tracing import task_fingerprint


class MockExecutor:
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    async def execute(
        self,
        task: TaskEnvelope,
        step: PlanStep,
        revision_notes: tuple[str, ...] = (),
        max_turns: int = 3,
    ) -> tuple[ExecutionArtifact, int]:
        response = await self.provider.run(
            ProviderRequest(
                objective=task.objective,
                agent_id=step.agent_id,
                step_id=step.id,
                task_fingerprint=task_fingerprint(task.objective),
                required_criteria=step.acceptance_criteria,
                max_turns=max_turns,
                revision_notes=revision_notes,
                external_calls_allowed=task.policy.external_provider_allowed,
                human_approval_reference=task.policy.human_approval_reference,
            )
        )
        return (
            ExecutionArtifact(
                step_id=step.id,
                author_agent_id=step.agent_id,
                status=ArtifactStatus.COMPLETE,
                summary=response.summary,
                required_criteria=step.acceptance_criteria,
                completed_criteria=response.completed_criteria,
                proposal_only=response.proposal_only,
            ),
            response.budget_units,
        )
