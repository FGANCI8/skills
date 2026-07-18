"""Deterministic provider used by default and throughout the test suite."""

from __future__ import annotations

from collections.abc import Iterable

from .base import ProviderRequest, ProviderResponse


class MockProvider:
    name = "mock"

    def __init__(self, responses: Iterable[ProviderResponse] = ()) -> None:
        self._responses = list(responses)
        self.calls = 0
        self.requests: list[ProviderRequest] = []

    async def run(self, request: ProviderRequest) -> ProviderResponse:
        self.calls += 1
        self.requests.append(request)
        if self._responses:
            return self._responses.pop(0)
        return ProviderResponse(
            summary=f"Synthetic artifact for step {request.step_id}.",
            completed_criteria=request.required_criteria,
            budget_units=1,
        )
