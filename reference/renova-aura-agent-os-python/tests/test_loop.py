from __future__ import annotations

import asyncio
import unittest

from renova_aura_agent_os.catalog import build_reference_catalog
from renova_aura_agent_os.evaluation import MockEvaluator
from renova_aura_agent_os.execution import MockExecutor
from renova_aura_agent_os.loops import BoundedLoopRunner
from renova_aura_agent_os.models import (
    EvaluationVerdict,
    LoopLimits,
    RuntimePolicy,
    StopReason,
    TaskEnvelope,
    TaskFacts,
)
from renova_aura_agent_os.orchestrator import AgentOS
from renova_aura_agent_os.planning import build_plan
from renova_aura_agent_os.providers.base import ProviderResponse
from renova_aura_agent_os.providers.mock import MockProvider
from renova_aura_agent_os.routing import route_task


def run(coro):
    return asyncio.run(coro)


class LoopTests(unittest.TestCase):
    def test_simple_mock_run_passes_in_one_round(self) -> None:
        result = run(
            AgentOS().run(
                TaskEnvelope(
                    objective="Crie um exemplo Python pequeno.",
                    facts=TaskFacts(detected_stacks=("Python",)),
                )
            )
        )
        self.assertEqual(StopReason.PASS, result.loop.stop_reason)
        self.assertEqual(1, result.loop.round_number)

    def test_revision_returns_to_author_then_passes(self) -> None:
        evaluator = MockEvaluator((EvaluationVerdict.REVISE, EvaluationVerdict.PASS))
        result = run(
            AgentOS(evaluator=evaluator).run(
                TaskEnvelope(
                    objective="Melhore a tela.",
                    facts=TaskFacts(affected_areas=("frontend",)),
                )
            )
        )
        self.assertEqual(StopReason.PASS, result.loop.stop_reason)
        self.assertEqual(2, result.loop.round_number)
        self.assertEqual(2, evaluator.calls)
        finding = result.loop.evaluations[0].findings[0]
        self.assertTrue(finding.criterion)
        self.assertTrue(finding.evidence)
        self.assertTrue(finding.required_change)
        self.assertEqual(
            result.loop.evaluations[0].author_agent_id,
            result.loop.evaluations[1].author_agent_id,
        )

    def test_loop_stops_at_max_rounds(self) -> None:
        evaluator = MockEvaluator((EvaluationVerdict.REVISE, EvaluationVerdict.REVISE))
        result = run(
            AgentOS(evaluator=evaluator).run(
                TaskEnvelope(
                    objective="Melhore a interface.",
                    facts=TaskFacts(affected_areas=("frontend",)),
                )
            )
        )
        self.assertEqual(StopReason.MAX_ROUNDS, result.loop.stop_reason)
        self.assertEqual(2, result.loop.round_number)

    def test_migration_gate_stops_before_provider(self) -> None:
        provider = MockProvider()
        result = run(
            AgentOS(provider=provider).run(
                TaskEnvelope(
                    objective="Execute uma migration.",
                    facts=TaskFacts(migration=True),
                )
            )
        )
        self.assertEqual(StopReason.HUMAN_APPROVAL_REQUIRED, result.loop.stop_reason)
        critical_steps = {step.id for step in result.plan.steps if step.critical_actions}
        self.assertTrue(provider.requests)
        self.assertTrue(critical_steps)
        self.assertTrue(critical_steps.isdisjoint(request.step_id for request in provider.requests))

    def test_real_external_action_stops_before_provider(self) -> None:
        provider = MockProvider()
        result = run(
            AgentOS(provider=provider).run(
                TaskEnvelope(objective="Use um provider real para esta tarefa.")
            )
        )
        self.assertEqual(StopReason.HUMAN_APPROVAL_REQUIRED, result.loop.stop_reason)
        critical_steps = {step.id for step in result.plan.steps if step.critical_actions}
        executed_steps = {request.step_id for request in provider.requests}
        self.assertTrue(critical_steps)
        self.assertTrue(critical_steps.isdisjoint(executed_steps))

    def test_natural_critical_actions_stop_before_the_critical_step(self) -> None:
        objectives = (
            "Envie uma mensagem para o cliente.",
            "Envie um WhatsApp.",
            "Faça um pagamento.",
            "Cobre o cartão.",
            "Use OpenAI.",
            "Apague dados pessoais.",
            "Exclua o repositório.",
        )
        for objective in objectives:
            with self.subTest(objective=objective):
                provider = MockProvider()
                result = run(AgentOS(provider=provider).run(TaskEnvelope(objective=objective)))
                critical_steps = {
                    step.id for step in result.plan.steps if step.critical_actions
                }
                executed_steps = {request.step_id for request in provider.requests}
                self.assertEqual(
                    StopReason.HUMAN_APPROVAL_REQUIRED,
                    result.loop.stop_reason,
                )
                self.assertTrue(critical_steps)
                self.assertTrue(critical_steps.isdisjoint(executed_steps))

    def test_approved_external_provider_policy_satisfies_the_plan_gate(self) -> None:
        provider = MockProvider()
        result = run(
            AgentOS(provider=provider).run(
                TaskEnvelope(
                    objective="Use um provider real para esta tarefa.",
                    policy=RuntimePolicy(
                        external_provider_allowed=True,
                        human_approval_reference="synthetic-approval",
                    ),
                )
            )
        )
        self.assertEqual(StopReason.PASS, result.loop.stop_reason)
        self.assertGreater(provider.calls, 0)
        self.assertTrue(all(request.external_calls_allowed for request in provider.requests))

    def test_runner_rejects_an_unrepresented_external_human_gate(self) -> None:
        task = TaskEnvelope(
            objective="Crie um exemplo Python pequeno.",
            facts=TaskFacts(detected_stacks=("Python",)),
        )
        catalog = build_reference_catalog()
        plan = build_plan(task, route_task(task, catalog), catalog)
        invalid_external_plan = plan.model_copy(update={"approval_required": True})
        provider = MockProvider()
        state = run(
            BoundedLoopRunner(
                executor=MockExecutor(provider),
                evaluator=MockEvaluator(),
            ).run(task, invalid_external_plan)
        )
        self.assertEqual(StopReason.HUMAN_APPROVAL_REQUIRED, state.stop_reason)
        self.assertEqual(0, provider.calls)

    def test_release_never_merges_or_deploys(self) -> None:
        provider = MockProvider()
        result = run(
            AgentOS(provider=provider).run(
                TaskEnvelope(
                    objective="Prepare a PR para release.",
                    facts=TaskFacts(release_related=True),
                )
            )
        )
        self.assertEqual(StopReason.HUMAN_APPROVAL_REQUIRED, result.loop.stop_reason)
        critical_steps = {step.id for step in result.plan.steps if step.critical_actions}
        self.assertTrue(provider.requests)
        self.assertTrue(critical_steps.isdisjoint(request.step_id for request in provider.requests))

    def test_long_running_plan_executes_handoff_before_integration(self) -> None:
        result = run(
            AgentOS().run(
                TaskEnvelope(
                    objective="Continue este trabalho longo por várias etapas.",
                    facts=TaskFacts(long_running=True),
                )
            )
        )
        artifact_ids = [artifact.step_id for artifact in result.loop.artifacts]
        self.assertEqual(StopReason.PASS, result.loop.stop_reason)
        self.assertIn("record-handoff", artifact_ids)
        self.assertIn("integrate-result", artifact_ids)
        self.assertLess(
            artifact_ids.index("record-handoff"),
            artifact_ids.index("integrate-result"),
        )

    def test_provider_budget_is_bounded(self) -> None:
        catalog = build_reference_catalog()
        task = TaskEnvelope(
            objective="Faça um exemplo Python.",
            facts=TaskFacts(detected_stacks=("Python",)),
        )
        plan = build_plan(task, route_task(task, catalog), catalog)
        provider = MockProvider((ProviderResponse(summary="synthetic", budget_units=100),))
        loop = run(
            BoundedLoopRunner(
                MockExecutor(provider),
                MockEvaluator(),
            ).run(task, plan)
        )
        self.assertEqual(StopReason.BUDGET_LIMIT, loop.stop_reason)
        self.assertEqual(100, loop.spent_budget_units)

    def test_missing_provider_evidence_stops_without_fabricating_acceptance(self) -> None:
        provider = MockProvider((ProviderResponse(summary="synthetic without evidence"),))
        result = run(
            AgentOS(provider=provider).run(
                TaskEnvelope(
                    objective="Faça um exemplo Python.",
                    facts=TaskFacts(detected_stacks=("Python",)),
                )
            )
        )
        self.assertEqual(StopReason.MISSING_EVIDENCE, result.loop.stop_reason)
        self.assertEqual(1, result.loop.provider_calls)

    def test_provider_exception_becomes_sanitized_environment_block(self) -> None:
        class FailingProvider:
            name = "failing-synthetic"

            async def run(self, _request):
                raise RuntimeError("synthetic internal detail")

        result = run(
            AgentOS(provider=FailingProvider()).run(
                TaskEnvelope(
                    objective="Faça um exemplo Python.",
                    facts=TaskFacts(detected_stacks=("Python",)),
                )
            )
        )
        self.assertEqual(StopReason.ENVIRONMENT_BLOCK, result.loop.stop_reason)
        self.assertEqual(1, result.loop.provider_calls)

    def test_trace_failure_becomes_sanitized_environment_block(self) -> None:
        class FailingTraceSink:
            def emit(self, _event):
                raise OSError("synthetic trace failure detail")

        result = run(
            AgentOS(trace_sink=FailingTraceSink()).run(
                TaskEnvelope(objective="Faça um exemplo Python pequeno.")
            )
        )
        self.assertEqual(StopReason.ENVIRONMENT_BLOCK, result.loop.stop_reason)
        self.assertEqual(0, result.loop.provider_calls)

    def test_evaluator_exception_becomes_sanitized_environment_block(self) -> None:
        class FailingEvaluator:
            def evaluate(self, _step, _artifact):
                raise RuntimeError("synthetic evaluator detail")

        result = run(
            AgentOS(evaluator=FailingEvaluator()).run(
                TaskEnvelope(
                    objective="Crie uma tela premium.",
                    facts=TaskFacts(affected_areas=("frontend",)),
                )
            )
        )
        self.assertEqual(StopReason.ENVIRONMENT_BLOCK, result.loop.stop_reason)

    def test_evaluator_is_cancelled_at_timeout(self) -> None:
        class SlowEvaluator:
            async def evaluate(self, _step, _artifact):
                await asyncio.sleep(1)
                raise AssertionError("synthetic evaluator was not cancelled")

        catalog = build_reference_catalog()
        task = TaskEnvelope(
            objective="Crie uma tela premium.",
            facts=TaskFacts(affected_areas=("frontend",)),
        )
        plan = build_plan(task, route_task(task, catalog), catalog).model_copy(
            update={"limits": LoopLimits(timeout_seconds=0.01)}
        )
        loop = run(
            BoundedLoopRunner(
                MockExecutor(MockProvider()),
                SlowEvaluator(),
            ).run(task, plan)
        )
        self.assertEqual(StopReason.TIMEOUT, loop.stop_reason)

    def test_timeout_is_bounded(self) -> None:
        catalog = build_reference_catalog()
        task = TaskEnvelope(
            objective="Faça um exemplo Python.",
            facts=TaskFacts(detected_stacks=("Python",)),
        )
        plan = build_plan(task, route_task(task, catalog), catalog)
        ticks = iter((0.0, 100.0))
        loop = run(
            BoundedLoopRunner(
                MockExecutor(MockProvider()),
                MockEvaluator(),
                clock=lambda: next(ticks),
            ).run(task, plan)
        )
        self.assertEqual(StopReason.TIMEOUT, loop.stop_reason)

    def test_provider_call_is_cancelled_at_timeout(self) -> None:
        class SlowProvider:
            name = "slow-synthetic"

            async def run(self, _request):
                await asyncio.sleep(1)
                return ProviderResponse(summary="late synthetic response")

        catalog = build_reference_catalog()
        task = TaskEnvelope(
            objective="Faça um exemplo Python.",
            facts=TaskFacts(detected_stacks=("Python",)),
        )
        plan = build_plan(task, route_task(task, catalog), catalog).model_copy(
            update={"limits": LoopLimits(timeout_seconds=0.01)}
        )
        loop = run(
            BoundedLoopRunner(
                MockExecutor(SlowProvider()),
                MockEvaluator(),
            ).run(task, plan)
        )
        self.assertEqual(StopReason.TIMEOUT, loop.stop_reason)
        self.assertEqual(1, loop.provider_calls)


if __name__ == "__main__":
    unittest.main()
