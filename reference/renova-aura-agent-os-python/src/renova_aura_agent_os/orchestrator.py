"""Small composition root for deterministic routing and bounded mock execution."""

from __future__ import annotations

from .catalog import build_reference_catalog
from .evaluation import Evaluator, MockEvaluator
from .execution import MockExecutor
from .handoff import build_handoff
from .loops import BoundedLoopRunner
from .models import AgentCatalog, RunResult, TaskEnvelope
from .planning import build_plan
from .providers.base import Provider
from .providers.mock import MockProvider
from .routing import route_task
from .tracing import InMemoryTraceSink, TraceSink


class AgentOS:
    def __init__(
        self,
        *,
        catalog: AgentCatalog | None = None,
        provider: Provider | None = None,
        evaluator: Evaluator | None = None,
        trace_sink: TraceSink | None = None,
    ) -> None:
        self.catalog = catalog or build_reference_catalog()
        self.provider = provider or MockProvider()
        self.evaluator = evaluator or MockEvaluator()
        self.trace_sink = trace_sink or InMemoryTraceSink()

    async def run(self, task: TaskEnvelope) -> RunResult:
        routing = route_task(task, self.catalog)
        plan = build_plan(task, routing, self.catalog)
        loop = await BoundedLoopRunner(
            executor=MockExecutor(self.provider),
            evaluator=self.evaluator,
            trace_sink=self.trace_sink,
        ).run(task, plan)
        return RunResult(
            routing=routing,
            plan=plan,
            loop=loop,
            handoff=build_handoff(task, loop),
        )
