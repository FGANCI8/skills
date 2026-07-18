"""Provider interface. There is deliberately no generic tool interface."""

from __future__ import annotations

from typing import Protocol

from pydantic import Field, model_validator

from ..models import SafeModel


class ProviderUnavailable(RuntimeError):
    """Raised when a requested provider cannot run safely."""


class ProviderRequest(SafeModel):
    objective: str = Field(min_length=1, max_length=4_000)
    agent_id: str
    step_id: str
    task_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    required_criteria: tuple[str, ...] = Field(min_length=1)
    max_turns: int = Field(default=3, ge=1, le=3)
    revision_notes: tuple[str, ...] = ()
    external_calls_allowed: bool = False
    human_approval_reference: str | None = Field(default=None, min_length=1, max_length=200)


class ProviderResponse(SafeModel):
    summary: str = Field(min_length=1, max_length=1_000)
    completed_criteria: tuple[str, ...] = ()
    budget_units: int = Field(default=1, ge=1, le=100)
    proposal_only: bool = False

    @model_validator(mode="after")
    def validate_proposal_evidence(self) -> ProviderResponse:
        if self.proposal_only and self.completed_criteria:
            raise ValueError("proposal-only responses cannot claim completed criteria")
        return self


class Provider(Protocol):
    name: str

    async def run(self, request: ProviderRequest) -> ProviderResponse:
        """Produce a structured result without implicit side effects."""
