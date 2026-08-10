from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timezone
import inspect
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_ROOT = REPO_ROOT / "agents"
sys.path.insert(0, str(AGENTS_ROOT))

from contract_checks import (  # noqa: E402
    ContractError,
    SyntheticApprovalStore,
    SyntheticGenerationDecisionStore,
    assert_diff_within_write_claims,
    assert_no_reparse_ancestors,
    canonical_ledger_sha256,
    claims_overlap,
    normalize_claim_path,
    validate_approval_evidence,
    validate_claim_transition,
    validate_evaluation_independence,
    validate_ledger_transition,
    validate_local_metrics,
    validate_metrics_configuration,
    validate_parallel_claims,
)


NOW = datetime(2030, 1, 1, 12, 6, tzinfo=timezone.utc)
TASK_ID = "task_22222222222222222222222222222222"
REQUEST_ID = "request_33333333333333333333333333333333"
APPROVAL_ID = "approval_11111111111111111111111111111111"
DECISION_ID = "decision_77777777777777777777777777777777"
TRUSTED_SOURCE = "store_dddddddd"
TRUSTED_ISSUER = "issuer_eeeeeeee"
TRUSTED_VERIFIER = "verifier_ffffffff"
TRUSTED_APPROVER = "approver_iiiiiiii"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fixed_clock() -> datetime:
    return NOW


def trusted_source() -> dict:
    return {
        "source_ref": TRUSTED_SOURCE,
        "issuer_ref": TRUSTED_ISSUER,
        "verifier_ref": TRUSTED_VERIFIER,
        "verification_ref": "verification_gggggggg",
        "result": "VALID",
    }


def approval_record(
    *,
    approval_id: str = APPROVAL_ID,
    nonce: str = "nonce_44444444444444444444444444444444",
) -> dict:
    return {
        "kind": "ApprovalRecord",
        "schema_version": "1.1.0",
        "approval_id": approval_id,
        "task_id": TASK_ID,
        "request_id": REQUEST_ID,
        "action": "SYNTHETIC_EXTERNAL_DELIVERY",
        "scope": ["scope_aaaaaaaa"],
        "targets": ["target_bbbbbbbb"],
        "environment": "NON_PRODUCTION_SYNTHETIC",
        "actor_ref": "actor_cccccccc",
        "trusted_source": trusted_source(),
        "issued_at": "2030-01-01T12:00:00Z",
        "expires_at": "2030-01-01T12:10:00Z",
        "nonce": nonce,
        "single_use": True,
        "max_uses": 1,
        "use_count": 0,
        "consumed_at": None,
        "justification": {
            "code": "BOUNDED_SYNTHETIC_DECISION",
            "evidence_refs": ["evidence_hhhhhhhh"],
        },
        "artifact_or_head": {"kind": "HEAD", "value": "a" * 40},
        "decision": "APPROVED",
        "decision_at": "2030-01-01T12:01:00Z",
        "approver_ref": TRUSTED_APPROVER,
        "execution_authority": "NEVER_AUTOMATIC",
        "executable": False,
    }


def approval_store(records: list[dict] | None = None) -> SyntheticApprovalStore:
    return SyntheticApprovalStore(
        [approval_record()] if records is None else records,
        trusted_source_refs=frozenset({TRUSTED_SOURCE}),
        trusted_issuer_refs=frozenset({TRUSTED_ISSUER}),
        trusted_verifier_refs=frozenset({TRUSTED_VERIFIER}),
        trusted_approver_refs=frozenset({TRUSTED_APPROVER}),
        clock=fixed_clock,
    )


def validate_approval(store: SyntheticApprovalStore, **overrides):
    kwargs = {
        "expected_task_id": TASK_ID,
        "expected_request_id": REQUEST_ID,
        "expected_action": "SYNTHETIC_EXTERNAL_DELIVERY",
        "expected_scope": ["scope_aaaaaaaa"],
        "expected_targets": ["target_bbbbbbbb"],
        "expected_environment": "NON_PRODUCTION_SYNTHETIC",
        "expected_actor_ref": "actor_cccccccc",
        "expected_artifact_or_head": {"kind": "HEAD", "value": "a" * 40},
    }
    kwargs.update(overrides)
    return validate_approval_evidence(APPROVAL_ID, store=store, **kwargs)


def claim(
    path: str,
    *,
    claim_id: str,
    path_type: str = "FILE",
    access: str = "WRITE",
    owner: str = "technical-director-orchestrator",
    status: str = "PLANNED",
    step: str = "step_bounded-action",
) -> dict:
    return {
        "claim_id": claim_id,
        "path": path,
        "path_type": path_type,
        "path_scope": "EXACT",
        "owner": owner,
        "access": access,
        "step": step,
        "dependencies": [],
        "status": status,
    }


def usage(**changes) -> dict:
    result = {
        "task_generation": 1,
        "loop_instances": 1,
        "total_rounds": 1,
        "total_provider_turns": 2,
        "total_tool_calls": 3,
        "total_budget_units": 4,
        "reopen_count": 0,
    }
    result.update(changes)
    return result


def ledger(*, stop_reason=None) -> dict:
    terminal_history = []
    if stop_reason:
        terminal_history.append(
            {
                "generation": 1,
                "reason": stop_reason,
                "at": "2030-01-01T12:05:00Z",
                "evidence_ref": "evidence_terminal-event",
            }
        )
    return {
        "kind": "TaskLedger",
        "schema_version": "1.1.0",
        "task_id": TASK_ID,
        "objective_ref": "objective_bounded-synthetic-example",
        "objective_category": "LIBRARY_GOVERNANCE",
        "status": "BLOCKED" if stop_reason else "PARTIAL",
        "mode": "SINGLE_SPECIALIST",
        "accountable_owner": "technical-director-orchestrator",
        "acceptance_criteria_refs": ["criterion_bounded-synthetic-pass"],
        "current_block": "block_bounded-inspection",
        "accounting_scope": "CUMULATIVE_TASK_CHAIN",
        "cumulative_limits": {
            "max_task_generations": 2,
            "max_loop_instances": 6,
            "max_total_rounds": 9,
            "max_total_provider_turns": 60,
            "max_total_tool_calls": 200,
            "max_total_budget_units": 300,
            "absolute_timeout_minutes": 240,
            "max_reopens": 1,
        },
        "cumulative_usage_at_block_start": usage(
            loop_instances=0,
            total_rounds=0,
            total_provider_turns=0,
            total_tool_calls=0,
            total_budget_units=0,
        ),
        "block_delta": {
            "loop_instances": 1,
            "rounds": 1,
            "provider_turns": 2,
            "tool_calls": 3,
            "budget_units": 4,
            "elapsed_time_ms": 100,
        },
        "cumulative_usage": usage(),
        "started_at": "2030-01-01T12:00:00Z",
        "absolute_deadline": "2030-01-01T16:00:00Z",
        "terminal_history": terminal_history,
        "previous_checkpoint": {"ref": None, "sha256": None},
        "approval_record_refs": [],
        "generation_decision_refs": [],
        "allowed_tool_refs": ["tool_repository-read-authorized-root"],
        "file_ownership_ref": "ownership_bounded-synthetic-example",
        "completed_artifact_refs": [],
        "pending_action_codes": ["INSPECT_AUTHORIZED_WORKSPACE"],
        "blocked_reason_codes": [],
        "stop_reason": stop_reason,
        "next_action_code": "INSPECT_AUTHORIZED_WORKSPACE",
        "local_metrics": {"enabled": False, "sink": "DISABLED"},
    }


def next_block(previous: dict) -> dict:
    current = deepcopy(previous)
    current["status"] = "PARTIAL"
    current["cumulative_usage_at_block_start"] = deepcopy(previous["cumulative_usage"])
    current["block_delta"] = {
        "loop_instances": 1,
        "rounds": 1,
        "provider_turns": 1,
        "tool_calls": 2,
        "budget_units": 3,
        "elapsed_time_ms": 200,
    }
    current["cumulative_usage"]["loop_instances"] += 1
    current["cumulative_usage"]["total_rounds"] += 1
    current["cumulative_usage"]["total_provider_turns"] += 1
    current["cumulative_usage"]["total_tool_calls"] += 2
    current["cumulative_usage"]["total_budget_units"] += 3
    current["stop_reason"] = None
    return current


def generation_decision(previous: dict) -> dict:
    return {
        "kind": "GenerationDecisionRecord",
        "schema_version": "1.1.0",
        "decision_id": DECISION_ID,
        "task_id": TASK_ID,
        "action": "REOPEN_SYNTHETIC_TASK",
        "prior_stop_reason": previous["stop_reason"],
        "prior_terminal_evidence_ref": previous["terminal_history"][-1]["evidence_ref"],
        "prior_ledger_sha256": canonical_ledger_sha256(previous),
        "from_generation": previous["cumulative_usage"]["task_generation"],
        "to_generation": previous["cumulative_usage"]["task_generation"] + 1,
        "environment": "NON_PRODUCTION_SYNTHETIC",
        "trusted_source": trusted_source(),
        "issued_at": "2030-01-01T12:00:00Z",
        "expires_at": "2030-01-01T12:10:00Z",
        "nonce": "nonce_88888888888888888888888888888888",
        "single_use": True,
        "max_uses": 1,
        "use_count": 0,
        "consumed_at": None,
        "decision": "APPROVED",
        "decision_at": "2030-01-01T12:02:00Z",
        "approver_ref": TRUSTED_APPROVER,
        "execution_authority": "LEDGER_TRANSITION_ONLY",
        "executable": False,
    }


def generation_store(record: dict) -> SyntheticGenerationDecisionStore:
    return SyntheticGenerationDecisionStore(
        [record],
        trusted_source_refs=frozenset({TRUSTED_SOURCE}),
        trusted_issuer_refs=frozenset({TRUSTED_ISSUER}),
        trusted_verifier_refs=frozenset({TRUSTED_VERIFIER}),
        trusted_approver_refs=frozenset({TRUSTED_APPROVER}),
        clock=fixed_clock,
    )


class ApprovalRecordTests(unittest.TestCase):
    def test_valid_store_evidence_is_single_use_and_nonexecutable(self):
        store = approval_store()
        evidence = validate_approval(store)
        self.assertEqual(evidence.decision_evidence, "VALID_SYNTHETIC_EVIDENCE_ONLY")
        self.assertEqual(evidence.execution_authority, "NEVER_AUTOMATIC")
        self.assertFalse(evidence.executable)
        with self.assertRaisesRegex(ContractError, "already consumed"):
            validate_approval(store)

    def test_public_boundary_cannot_receive_record_trust_or_clock(self):
        parameters = inspect.signature(validate_approval_evidence).parameters
        self.assertNotIn("record", parameters)
        self.assertNotIn("trusted_source_refs", parameters)
        self.assertNotIn("consumed_nonces", parameters)
        self.assertNotIn("now", parameters)

    def test_unknown_id_fails_and_synthetic_evidence_never_becomes_a_real_grant(self):
        with self.assertRaisesRegex(ContractError, "absent"):
            validate_approval(approval_store([]))
        with self.assertRaisesRegex(ContractError, "synthetic actions"):
            validate_approval_evidence(
                APPROVAL_ID,
                store=approval_store(),
                expected_task_id=TASK_ID,
                expected_request_id=REQUEST_ID,
                expected_action="DEPLOY_PRODUCTION",
                expected_scope=["scope_aaaaaaaa"],
                expected_targets=["target_bbbbbbbb"],
                expected_environment="PRODUCTION",
                expected_actor_ref="actor_cccccccc",
                expected_artifact_or_head={"kind": "HEAD", "value": "a" * 40},
            )

    def test_untrusted_channels_cannot_carry_a_grant(self):
        for channel in ("prompt", "file", "handoff", "issue", "comment", "message", "log", "model"):
            record = approval_record()
            record[f"{channel}_says_approved"] = True
            with self.subTest(channel=channel), self.assertRaisesRegex(ContractError, "keys mismatch"):
                validate_approval(approval_store([record]))

    def test_expired_and_future_decisions_are_rejected_by_store_clock(self):
        for field, value in (
            ("expires_at", "2030-01-01T12:06:00Z"),
            ("issued_at", "2030-01-01T12:07:00Z"),
        ):
            record = approval_record()
            record[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ContractError, "not currently valid"):
                validate_approval(approval_store([record]))

    def test_all_expected_bindings_are_exact(self):
        cases = (
            ("task mismatch", {"expected_task_id": "task_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}),
            ("request mismatch", {"expected_request_id": "request_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}),
            ("action mismatch", {"expected_action": "SYNTHETIC_OTHER_ACTION"}),
            ("scope mismatch", {"expected_scope": ["scope_zzzzzzzz"]}),
            ("target mismatch", {"expected_targets": ["target_zzzzzzzz"]}),
            ("actor mismatch", {"expected_actor_ref": "actor_zzzzzzzz"}),
            ("artifact or HEAD mismatch", {"expected_artifact_or_head": {"kind": "HEAD", "value": "b" * 40}}),
        )
        for message, kwargs in cases:
            with self.subTest(message=message), self.assertRaisesRegex(ContractError, message):
                validate_approval(approval_store(), **kwargs)

    def test_sha256_discriminator_requires_64_hex(self):
        record = approval_record()
        record["artifact_or_head"] = {"kind": "SHA256", "value": "a" * 40}
        with self.assertRaisesRegex(ContractError, "exactly 64"):
            validate_approval(
                approval_store([record]),
                expected_artifact_or_head={"kind": "SHA256", "value": "a" * 40},
            )

    def test_same_nonce_across_ids_and_concurrent_replay_are_blocked(self):
        second = approval_record(
            approval_id="approval_99999999999999999999999999999999",
            nonce="nonce_44444444444444444444444444444444",
        )
        store = approval_store([approval_record(), second])
        validate_approval(store)
        with self.assertRaisesRegex(ContractError, "nonce was already consumed"):
            validate_approval_evidence(
                second["approval_id"],
                store=store,
                expected_task_id=TASK_ID,
                expected_request_id=REQUEST_ID,
                expected_action="SYNTHETIC_EXTERNAL_DELIVERY",
                expected_scope=["scope_aaaaaaaa"],
                expected_targets=["target_bbbbbbbb"],
                expected_environment="NON_PRODUCTION_SYNTHETIC",
                expected_actor_ref="actor_cccccccc",
                expected_artifact_or_head={"kind": "HEAD", "value": "a" * 40},
            )

        concurrent_store = approval_store()
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(validate_approval, concurrent_store) for _ in range(2)]
        outcomes = []
        for future in futures:
            try:
                future.result()
                outcomes.append("PASS")
            except ContractError:
                outcomes.append("BLOCKED")
        self.assertEqual(sorted(outcomes), ["BLOCKED", "PASS"])


class OwnershipTests(unittest.TestCase):
    def test_ancestor_and_windows_case_collisions_are_detected(self):
        directory = claim(
            "SRC\\API",
            claim_id="claim_11111111111111111111111111111111",
            path_type="DIRECTORY",
        )
        child = claim(
            "src/api/route.py",
            claim_id="claim_22222222222222222222222222222222",
        )
        sibling = claim(
            "src/api2/route.py",
            claim_id="claim_33333333333333333333333333333333",
        )
        self.assertTrue(claims_overlap(directory, child))
        self.assertFalse(claims_overlap(directory, sibling))

    def test_windows_aliases_globs_and_traversal_fail_closed(self):
        unsafe_paths = (
            "safe/.. /secret",
            "src/api/file.py.",
            "src/ api/x",
            "NUL.txt",
            "COM¹.log",
            "file:$DATA",
            "\\\\?\\C:\\safe\\file",
            "src/*.py",
            "../secret",
            "/root/file",
            "C:\\repo\\file",
        )
        for unsafe in unsafe_paths:
            with self.subTest(unsafe=unsafe), self.assertRaises(ContractError):
                normalize_claim_path(unsafe)

    def test_known_reparse_ancestor_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ContractError, "reparse point"):
                assert_no_reparse_ancestors(
                    Path(directory),
                    "src/link/file.py",
                    known_reparse_paths=frozenset({"src/link"}),
                )

    def test_existing_path_type_spoof_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "agents").mkdir()
            (root / "file.txt").write_text("safe", encoding="utf-8")
            for bad_claim in (
                claim("agents", claim_id="claim_11111111111111111111111111111111", path_type="FILE"),
                claim("file.txt", claim_id="claim_22222222222222222222222222222222", path_type="DIRECTORY"),
            ):
                with self.subTest(path=bad_claim["path"]), self.assertRaisesRegex(ContractError, "path_type"):
                    validate_parallel_claims([bad_claim], repository_root=root)

    def test_parallel_preflight_rejects_overlap_and_terminal_statuses(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src" / "api").mkdir(parents=True)
            (root / "src" / "api" / "route.py").write_text("safe", encoding="utf-8")
            claims = [
                claim(
                    "src/api",
                    claim_id="claim_11111111111111111111111111111111",
                    path_type="DIRECTORY",
                ),
                claim("src/api/route.py", claim_id="claim_22222222222222222222222222222222"),
            ]
            with self.assertRaisesRegex(ContractError, "ancestry conflict"):
                validate_parallel_claims(claims, repository_root=root)
            claims[1]["status"] = "COMPLETE"
            with self.assertRaisesRegex(ContractError, "preflight"):
                validate_parallel_claims([claims[1]], repository_root=root)

    def test_hardlink_identity_conflicts_even_with_distinct_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first.txt"
            second = root / "second.txt"
            first.write_text("safe", encoding="utf-8")
            try:
                os.link(first, second)
            except OSError as exc:
                self.skipTest(f"hard links unavailable: {exc}")
            claims = [
                claim("first.txt", claim_id="claim_11111111111111111111111111111111"),
                claim("second.txt", claim_id="claim_22222222222222222222222222222222"),
            ]
            with self.assertRaisesRegex(ContractError, "conflict"):
                validate_parallel_claims(claims, repository_root=root)

    def test_real_diff_requires_active_write_owner_and_step(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src" / "api").mkdir(parents=True)
            active = claim(
                "src/api",
                claim_id="claim_11111111111111111111111111111111",
                path_type="DIRECTORY",
                status="ACTIVE",
            )
            assert_diff_within_write_claims(
                ["src/api/route.py"],
                [active],
                repository_root=root,
                owner=active["owner"],
                step=active["step"],
            )
            for status in ("PLANNED", "COMPLETE", "BLOCKED"):
                inactive = deepcopy(active)
                inactive["status"] = status
                with self.subTest(status=status), self.assertRaisesRegex(ContractError, "ACTIVE WRITE"):
                    assert_diff_within_write_claims(
                        ["src/api/route.py"],
                        [inactive],
                        repository_root=root,
                        owner=inactive["owner"],
                        step=inactive["step"],
                    )
            with self.assertRaisesRegex(ContractError, "outside ACTIVE WRITE"):
                assert_diff_within_write_claims(
                    ["src/auth.py"],
                    [active],
                    repository_root=root,
                    owner=active["owner"],
                    step=active["step"],
                )

    def test_claim_lifecycle_is_one_way_and_authority_is_immutable(self):
        planned = claim("src/api", claim_id="claim_11111111111111111111111111111111", path_type="DIRECTORY")
        active = deepcopy(planned)
        active["status"] = "ACTIVE"
        complete = deepcopy(active)
        complete["status"] = "COMPLETE"
        validate_claim_transition(planned, active)
        validate_claim_transition(active, complete)
        with self.assertRaisesRegex(ContractError, "terminal"):
            validate_claim_transition(complete, active)
        changed_owner = deepcopy(active)
        changed_owner["owner"] = "python-engineer"
        with self.assertRaisesRegex(ContractError, "immutable"):
            validate_claim_transition(planned, changed_owner)


class CumulativeLedgerTests(unittest.TestCase):
    def test_usage_is_monotonic_and_all_block_deltas_reconcile(self):
        previous = ledger()
        current = next_block(previous)
        validate_ledger_transition(previous, current, now=NOW)

    def test_counter_reset_deadline_extension_and_loop_mismatch_are_rejected(self):
        previous = ledger()
        cases = []
        current = next_block(previous)
        current["cumulative_usage"]["total_tool_calls"] = 1
        cases.append(("counter reset", current))
        current = next_block(previous)
        current["absolute_deadline"] = "2030-01-01T17:00:00Z"
        cases.append(("absolute_deadline", current))
        current = next_block(previous)
        current["block_delta"]["loop_instances"] = 0
        cases.append(("does not reconcile", current))
        for message, current in cases:
            with self.subTest(message=message), self.assertRaisesRegex(ContractError, message):
                validate_ledger_transition(previous, current, now=NOW)

    def test_handoff_cannot_hide_usage_or_rewrite_history(self):
        previous = ledger()
        current = next_block(previous)
        current["cumulative_usage_at_block_start"]["total_rounds"] = 0
        with self.assertRaisesRegex(ContractError, "block start"):
            validate_ledger_transition(previous, current, now=NOW)

        previous = ledger(stop_reason="SECURITY_BLOCK")
        current = next_block(previous)
        current["terminal_history"] = []
        current["cumulative_usage"]["task_generation"] = 2
        current["cumulative_usage"]["reopen_count"] = 1
        with self.assertRaisesRegex(ContractError, "append-only"):
            validate_ledger_transition(previous, current, now=NOW)

    def test_terminal_model_text_or_safe_reference_cannot_reopen_task(self):
        previous = ledger(stop_reason="MAX_ROUNDS")
        current = next_block(previous)
        with self.assertRaisesRegex(ContractError, "same generation|terminal event"):
            validate_ledger_transition(previous, current, now=NOW)

        current["cumulative_usage"]["task_generation"] = 2
        current["cumulative_usage"]["reopen_count"] = 1
        current["generation_decision_refs"] = [DECISION_ID]
        with self.assertRaisesRegex(ContractError, "trusted synthetic decision store"):
            validate_ledger_transition(
                previous,
                current,
                now=NOW,
                generation_decision_id=DECISION_ID,
            )
        self.assertNotIn("external_generation_decision_ref", inspect.signature(validate_ledger_transition).parameters)

    def test_typed_generation_decision_is_bound_and_single_use(self):
        previous = ledger(stop_reason="SECURITY_BLOCK")
        current = next_block(previous)
        current["cumulative_usage"]["task_generation"] = 2
        current["cumulative_usage"]["reopen_count"] = 1
        current["generation_decision_refs"] = [DECISION_ID]
        store = generation_store(generation_decision(previous))
        validate_ledger_transition(
            previous,
            current,
            now=NOW,
            generation_decision_store=store,
            generation_decision_id=DECISION_ID,
        )
        with self.assertRaisesRegex(ContractError, "already consumed"):
            validate_ledger_transition(
                previous,
                current,
                now=NOW,
                generation_decision_store=store,
                generation_decision_id=DECISION_ID,
            )

    def test_generation_decision_digest_task_reason_and_generation_mismatches_fail(self):
        previous = ledger(stop_reason="SECURITY_BLOCK")
        current = next_block(previous)
        current["cumulative_usage"]["task_generation"] = 2
        current["cumulative_usage"]["reopen_count"] = 1
        current["generation_decision_refs"] = [DECISION_ID]
        for field, value in (
            ("prior_ledger_sha256", "0" * 64),
            ("task_id", "task_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
            ("prior_stop_reason", "MAX_ROUNDS"),
            ("to_generation", 3),
        ):
            decision = generation_decision(previous)
            decision[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ContractError, "mismatch"):
                validate_ledger_transition(
                    previous,
                    current,
                    now=NOW,
                    generation_decision_store=generation_store(decision),
                    generation_decision_id=DECISION_ID,
                )

    def test_deadline_and_terminal_history_semantics_fail_closed(self):
        previous = ledger()
        current = next_block(previous)
        current["absolute_deadline"] = "2099-01-01T00:00:00Z"
        with self.assertRaisesRegex(ContractError, "absolute_deadline"):
            validate_ledger_transition(previous, current, now=NOW)

        terminal = ledger(stop_reason="SECURITY_BLOCK")
        terminal["terminal_history"][0]["generation"] = 999
        terminal["terminal_history"][0]["at"] = "1990-01-01T00:00:00Z"
        with self.assertRaises(ContractError):
            validate_ledger_transition(terminal, next_block(terminal), now=NOW)

    def test_terminal_transition_appends_exact_current_event(self):
        previous = ledger()
        current = next_block(previous)
        current["status"] = "DONE"
        current["stop_reason"] = "PASS"
        current["terminal_history"].append(
            {
                "generation": 1,
                "reason": "PASS",
                "at": "2030-01-01T12:06:00Z",
                "evidence_ref": "evidence_current-terminal",
            }
        )
        validate_ledger_transition(previous, current, now=NOW)


def evaluation_record() -> dict:
    return {
        "kind": "EvaluationRecord",
        "schema_version": "1.1.0",
        "evaluation_id": "evaluation_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "task_id": TASK_ID,
        "author_agent_id": "python-engineer",
        "evaluator_agent_id": "independent-technical-reviewer",
        "evaluator_capability": "INDEPENDENT_EVALUATOR",
        "evaluated_paths": ["src/artifact.txt"],
        "report_path": "reviews/report.txt",
        "artifact_or_head": {"kind": "SHA256", "value": "a" * 64},
        "decision": "CHANGES_REQUIRED",
        "finding_refs": ["finding_contract-gap"],
        "evaluation_at": "2030-01-01T12:05:00Z",
        "author_claim_refs": ["claim_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"],
        "evaluator_report_claim_ref": "claim_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "execution_authority": "EVIDENCE_ONLY",
        "executable": False,
    }


def evaluation_claims() -> list[dict]:
    return [
        claim(
            "src/artifact.txt",
            claim_id="claim_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            owner="python-engineer",
            status="COMPLETE",
        ),
        claim(
            "reviews/report.txt",
            claim_id="claim_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            owner="independent-technical-reviewer",
            status="COMPLETE",
        ),
    ]


def capabilities() -> dict:
    return {
        "independent-technical-reviewer": {
            "can_evaluate": True,
            "must_be_independent_from_author": True,
        }
    }


class EvaluationTests(unittest.TestCase):
    def run_validation(self, record: dict, claims: list[dict], root: Path, registry=None):
        return validate_evaluation_independence(
            record,
            claims,
            agent_capabilities=capabilities() if registry is None else registry,
            repository_root=root,
            now=NOW,
        )

    def test_independent_author_and_separate_report_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "reviews").mkdir()
            (root / "src" / "artifact.txt").write_text("artifact", encoding="utf-8")
            (root / "reviews" / "report.txt").write_text("report", encoding="utf-8")
            self.run_validation(evaluation_record(), evaluation_claims(), root)

    def test_same_author_or_untrusted_evaluator_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "reviews").mkdir()
            (root / "src" / "artifact.txt").write_text("artifact", encoding="utf-8")
            (root / "reviews" / "report.txt").write_text("report", encoding="utf-8")
            record = evaluation_record()
            record["evaluator_agent_id"] = record["author_agent_id"]
            with self.assertRaisesRegex(ContractError, "distinct"):
                self.run_validation(record, evaluation_claims(), root)
            with self.assertRaisesRegex(ContractError, "trusted agent registry"):
                self.run_validation(evaluation_record(), evaluation_claims(), root, registry={})

    def test_evaluator_write_overlap_and_report_overlap_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "reviews").mkdir()
            (root / "src" / "artifact.txt").write_text("artifact", encoding="utf-8")
            (root / "reviews" / "report.txt").write_text("report", encoding="utf-8")
            overlap = claim(
                "src",
                claim_id="claim_cccccccccccccccccccccccccccccccc",
                path_type="DIRECTORY",
                owner="independent-technical-reviewer",
                status="ACTIVE",
            )
            with self.assertRaisesRegex(ContractError, "WRITE claim"):
                self.run_validation(evaluation_record(), evaluation_claims() + [overlap], root)
            record = evaluation_record()
            record["report_path"] = "src/artifact.txt"
            with self.assertRaisesRegex(ContractError, "separate"):
                self.run_validation(record, evaluation_claims(), root)


class MetricsTests(unittest.TestCase):
    def test_allowlisted_sanitized_metrics_and_sink_pairs_pass(self):
        validate_local_metrics(
            {
                "routing_mode": "SINGLE_SPECIALIST",
                "selected_agent_count": 1,
                "selected_skill_count": 1,
                "rounds": 1,
                "provider_calls": 0,
                "tool_calls": 3,
                "stop_reason": "PASS",
                "elapsed_time_ms": 12,
            }
        )
        validate_metrics_configuration(enabled=False, sink="DISABLED")
        validate_metrics_configuration(enabled=True, sink="MEMORY_ONLY")
        validate_metrics_configuration(enabled=True, sink="PRIVATE_LOCAL_FILE")

    def test_raw_content_invalid_numbers_and_sink_mismatches_fail(self):
        for metrics in (
            {"objective": "raw user text"},
            {"prompt": "raw prompt"},
            {"private_path": "C:/private"},
            {"tool_calls": -1},
            {"provider_calls": True},
        ):
            with self.subTest(metrics=metrics), self.assertRaises(ContractError):
                validate_local_metrics(metrics)
        for enabled, sink in ((False, "PRIVATE_LOCAL_FILE"), (True, "DISABLED"), (True, "NETWORK")):
            with self.subTest(enabled=enabled, sink=sink), self.assertRaises(ContractError):
                validate_metrics_configuration(enabled=enabled, sink=sink)


class StaticGovernanceTests(unittest.TestCase):
    def test_json_schemas_parse_are_closed_and_discriminate_sha256(self):
        team_schema = load_json(AGENTS_ROOT / "agent-team.schema.json")
        records = load_json(AGENTS_ROOT / "operating-records.schema.json")
        self.assertEqual(records["$defs"]["approvalRecord"]["additionalProperties"], False)
        self.assertEqual(records["$defs"]["approvalRecord"]["properties"]["executable"]["const"], False)
        self.assertEqual(records["$defs"]["generationDecisionRecord"]["properties"]["environment"]["const"], "NON_PRODUCTION_SYNTHETIC")
        self.assertEqual(records["$defs"]["evaluationRecord"]["properties"]["execution_authority"]["const"], "EVIDENCE_ONLY")
        sha_branch = records["$defs"]["artifactBinding"]["oneOf"][1]["properties"]
        self.assertEqual(sha_branch["kind"]["const"], "SHA256")
        self.assertEqual(sha_branch["value"]["pattern"], "^[a-f0-9]{64}$")
        self.assertEqual(team_schema["$defs"]["agent"]["properties"]["authority_contract"]["const"], "RA-AUTH-BASELINE-1")

    def test_team_and_all_agents_have_v11_basal_contract(self):
        schema = load_json(AGENTS_ROOT / "agent-team.schema.json")
        team = load_yaml(AGENTS_ROOT / "renova-aura-team.yaml")
        definitions = sorted((AGENTS_ROOT / "definitions").glob("*.yaml"))
        agents = [load_yaml(path) for path in definitions]

        self.assertEqual(len(agents), 18)
        self.assertEqual(team["schema_version"], "1.1.0")
        self.assertEqual(team["authority_contract"]["id"], "RA-AUTH-BASELINE-1")
        self.assertEqual(team["tool_policy"]["real_provider"], "HARD_FORBIDDEN_V1")
        self.assertFalse(team["approval_policy"]["caller_self_grant"])
        self.assertEqual(team["hard_forbidden_actions"], ["REAL_PROVIDER_EXECUTION"])

        allowed_tools = set(schema["$defs"]["toolId"]["enum"])
        approval_actions = set(schema["$defs"]["approvalAction"]["enum"])
        ids = [agent["id"] for agent in agents]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(sum(bool(agent["accountable_integrator"]) for agent in agents), 1)
        for path, agent in zip(definitions, agents):
            self.assertEqual(path.stem, agent["id"])
            self.assertEqual(agent["schema_version"], "1.1.0")
            self.assertEqual(agent["authority_contract"], "RA-AUTH-BASELINE-1")
            self.assertEqual(agent["tool_policy_ref"], "team.tool_policy")
            self.assertTrue(set(agent["allowed_tools"]).issubset(allowed_tools))
            self.assertTrue(set(agent["approval_gated_actions"]).issubset(approval_actions))
            self.assertNotIn("REAL_PROVIDER_EXECUTION", agent["approval_gated_actions"])
            self.assertIn("hard_forbidden_actions", agent)
            self.assertNotIn("human_approval", agent)
            self.assertNotIn("forbidden_actions", agent)

        registry = {entry["id"]: entry["file"] for entry in team["agents"]}
        self.assertEqual(set(registry), set(ids))
        for agent_id, relative in registry.items():
            self.assertEqual(relative, f"definitions/{agent_id}.yaml")

    def test_dependencies_are_known_and_acyclic(self):
        agents = {
            data["id"]: data
            for data in (
                load_yaml(path) for path in sorted((AGENTS_ROOT / "definitions").glob("*.yaml"))
            )
        }
        for agent in agents.values():
            self.assertTrue(set(agent["dependencies"]).issubset(agents))

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(agent_id: str):
            if agent_id in visiting:
                self.fail(f"dependency cycle at {agent_id}")
            if agent_id in visited:
                return
            visiting.add(agent_id)
            for dependency in agents[agent_id]["dependencies"]:
                visit(dependency)
            visiting.remove(agent_id)
            visited.add(agent_id)

        for agent_id in agents:
            visit(agent_id)

    def test_incident_audit_only_has_zero_write_or_side_effect_authority(self):
        agent = load_yaml(AGENTS_ROOT / "definitions" / "observability-incident-engineer.yaml")
        policy = agent["incident_policy"]
        self.assertEqual(policy["default_mode"], "AUDIT_ONLY")
        self.assertEqual(policy["audit_only_repository_write"], "DENY")
        self.assertEqual(policy["audit_only_external_side_effects"], "DENY")
        self.assertEqual(policy["audit_only_write_claim_activation"], "DENY")
        self.assertFalse(agent["capabilities"]["can_write"])
        self.assertNotIn("REPOSITORY_WRITE_CLAIMED", agent["allowed_tools"])

    def test_templates_are_sanitized_and_non_authoritative(self):
        approval = load_yaml(AGENTS_ROOT / "templates" / "APPROVAL_RECORD.yaml")
        generation = load_yaml(AGENTS_ROOT / "templates" / "GENERATION_DECISION_RECORD.yaml")
        evaluation = load_yaml(AGENTS_ROOT / "templates" / "EVALUATION_RECORD.yaml")
        task = load_yaml(AGENTS_ROOT / "templates" / "TASK_LEDGER.yaml")
        metrics = load_json(AGENTS_ROOT / "templates" / "LOCAL_METRICS.json")
        handoff = (AGENTS_ROOT / "templates" / "HANDOFF.md").read_text(encoding="utf-8")

        self.assertEqual(approval["decision"], "REQUESTED")
        self.assertFalse(approval["executable"])
        self.assertEqual(generation["decision"], "REQUESTED")
        self.assertFalse(generation["executable"])
        self.assertEqual(evaluation["execution_authority"], "EVIDENCE_ONLY")
        self.assertNotIn("objective", task)
        self.assertEqual(task["accounting_scope"], "CUMULATIVE_TASK_CHAIN")
        self.assertEqual(task["generation_decision_refs"], [])
        self.assertFalse(metrics["enabled"])
        self.assertIn("never a grant", handoff.lower())
        self.assertNotIn("- Objective:", handoff)

    def test_eval_document_has_30_not_run_contract_rows(self):
        text = (REPO_ROOT / "RENOVA_AURA_AGENT_OS_EVALS.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| (A\d{2}) \|.*?\| `(eval_a\d{2}_[a-z0-9_]+)` \| `NOT_RUN` \|$", text, re.MULTILINE)
        self.assertEqual(len(rows), 30)
        self.assertEqual([row[0] for row in rows], [f"A{index:02d}" for index in range(1, 31)])
        self.assertEqual(len({row[1] for row in rows}), 30)


if __name__ == "__main__":
    unittest.main()
