from __future__ import annotations

import unittest

from pydantic import ValidationError

from renova_aura_agent_os.models import (
    AccessMode,
    Complexity,
    EvaluationFinding,
    EvaluationResult,
    EvaluationVerdict,
    ExecutionPlan,
    FileClaim,
    LoopLimits,
    OrchestrationMode,
    PlanStep,
    PlanStepKind,
    RiskLevel,
    RoutingDecision,
    StopReason,
    TaskFacts,
)


class ModelInvariantTests(unittest.TestCase):
    def test_turn_limit_is_explicit_and_bounded(self) -> None:
        self.assertEqual(3, LoopLimits().max_turns)
        with self.assertRaises(ValidationError):
            LoopLimits(max_turns=4)

    def test_rejects_absolute_and_traversal_paths(self) -> None:
        for path in (
            "C:/private/file.py",
            "../secret.txt",
            "/etc/passwd",
            "//server/share",
            "src/file.py. ",
            "src/CON.txt",
            "src/a|b.py",
            "src/a<b.py",
            'src/a"b.py',
        ):
            with self.subTest(path=path), self.assertRaises(ValidationError):
                TaskFacts(candidate_files=(path,))

    def test_rejects_glob_ownership_paths(self) -> None:
        for path in ("src/*.py", "**/*.ts", "src/?odule.py", "src/[ab].py"):
            with self.subTest(path=path), self.assertRaises(ValidationError):
                TaskFacts(candidate_files=(path,))

    def test_candidate_file_uniqueness_is_windows_case_insensitive(self) -> None:
        with self.assertRaises(ValidationError):
            TaskFacts(candidate_files=("src/File.py", "src/file.py"))

    def test_normalizes_windows_separators_without_accessing_disk(self) -> None:
        claim = FileClaim(
            path="src\\module.py",
            owner_agent_id="python-engineer",
            access=AccessMode.WRITE,
        )
        self.assertEqual("src/module.py", claim.path)

    def test_author_cannot_self_approve(self) -> None:
        with self.assertRaises(ValidationError):
            EvaluationResult(
                target_step_id="step",
                author_agent_id="same-agent",
                evaluator_agent_id="same-agent",
                verdict=EvaluationVerdict.PASS,
            )

    def test_evaluation_verdict_and_findings_are_consistent(self) -> None:
        finding = EvaluationFinding(
            criterion="synthetic criterion",
            evidence="synthetic evidence",
            required_change="synthetic correction",
        )
        with self.assertRaises(ValidationError):
            EvaluationResult(
                target_step_id="step",
                author_agent_id="author",
                evaluator_agent_id="reviewer",
                verdict=EvaluationVerdict.PASS,
                findings=(finding,),
            )
        with self.assertRaises(ValidationError):
            EvaluationResult(
                target_step_id="step",
                author_agent_id="author",
                evaluator_agent_id="reviewer",
                verdict=EvaluationVerdict.BLOCK,
                block_reason=StopReason.SECURITY_BLOCK,
            )

    def test_two_agents_cannot_write_the_same_file(self) -> None:
        route = RoutingDecision(
            complexity=Complexity.MEDIUM,
            risk_level=RiskLevel.MEDIUM,
            mode=OrchestrationMode.CONTROLLED_PARALLEL,
            primary_agent_id="author-one",
            participant_agent_ids=("author-one", "author-two"),
            reasons=("synthetic concurrency test",),
        )
        first = PlanStep(
            id="first",
            title="First synthetic writer",
            agent_id="author-one",
            kind=PlanStepKind.MOCK_EXECUTE,
            file_claims=(
                FileClaim(
                    path="src/Shared.py",
                    owner_agent_id="author-one",
                    access=AccessMode.WRITE,
                ),
            ),
            acceptance_criteria=("first criterion",),
        )
        second = PlanStep(
            id="second",
            title="Second synthetic writer",
            agent_id="author-two",
            kind=PlanStepKind.MOCK_EXECUTE,
            file_claims=(
                FileClaim(
                    path="src/shared.py",
                    owner_agent_id="author-two",
                    access=AccessMode.WRITE,
                ),
            ),
            acceptance_criteria=("second criterion",),
        )
        with self.assertRaises(ValidationError):
            ExecutionPlan(
                routing=route,
                integrator_agent_id="author-one",
                steps=(first, second),
                parallel_groups=(("first", "second"),),
            )

    def test_declared_human_gate_requires_an_explicit_critical_step(self) -> None:
        route = RoutingDecision(
            complexity=Complexity.SMALL,
            risk_level=RiskLevel.HIGH,
            mode=OrchestrationMode.SINGLE_SPECIALIST,
            primary_agent_id="author",
            participant_agent_ids=("author",),
            reasons=("synthetic external-plan gate",),
            human_approval_required=True,
        )
        step = PlanStep(
            id="bounded-step",
            title="Bounded synthetic step",
            agent_id="author",
            kind=PlanStepKind.MOCK_EXECUTE,
            acceptance_criteria=("synthetic criterion",),
        )
        with self.assertRaises(ValidationError):
            ExecutionPlan(
                routing=route,
                integrator_agent_id="author",
                steps=(step,),
                approval_required=True,
            )


if __name__ == "__main__":
    unittest.main()
