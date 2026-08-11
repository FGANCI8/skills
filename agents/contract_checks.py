"""Dependency-free contract checks for Renova Aura Agent OS records.

The module validates governance evidence. It never executes an approved action,
grants real-world authority, reopens a real task, or calls an external provider.
The two in-memory stores are deliberately restricted to non-production synthetic
tests; a real trusted-store adapter is outside the V1.1 implementation.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import stat
from threading import Lock
from typing import Any, Callable, Iterable, Mapping, Sequence
import unicodedata


class ContractError(ValueError):
    """Raised when a governance record fails closed."""


STOP_REASONS = {
    "PASS",
    "MAX_ROUNDS",
    "TIMEOUT",
    "BUDGET_LIMIT",
    "HUMAN_APPROVAL_REQUIRED",
    "SECURITY_BLOCK",
    "ENVIRONMENT_BLOCK",
    "MISSING_EVIDENCE",
    "SCOPE_CHANGE",
}

APPROVAL_KEYS = {
    "kind",
    "schema_version",
    "approval_id",
    "task_id",
    "request_id",
    "action",
    "scope",
    "targets",
    "environment",
    "actor_ref",
    "trusted_source",
    "issued_at",
    "expires_at",
    "nonce",
    "single_use",
    "max_uses",
    "use_count",
    "consumed_at",
    "justification",
    "artifact_or_head",
    "decision",
    "decision_at",
    "approver_ref",
    "execution_authority",
    "executable",
}

GENERATION_DECISION_KEYS = {
    "kind",
    "schema_version",
    "decision_id",
    "task_id",
    "action",
    "prior_stop_reason",
    "prior_terminal_evidence_ref",
    "prior_ledger_sha256",
    "from_generation",
    "to_generation",
    "environment",
    "trusted_source",
    "issued_at",
    "expires_at",
    "nonce",
    "single_use",
    "max_uses",
    "use_count",
    "consumed_at",
    "decision",
    "decision_at",
    "approver_ref",
    "execution_authority",
    "executable",
}

EVALUATION_KEYS = {
    "kind",
    "schema_version",
    "evaluation_id",
    "task_id",
    "author_agent_id",
    "evaluator_agent_id",
    "evaluator_capability",
    "evaluated_paths",
    "report_path",
    "artifact_or_head",
    "decision",
    "finding_refs",
    "evaluation_at",
    "author_claim_refs",
    "evaluator_report_claim_ref",
    "execution_authority",
    "executable",
}

LEDGER_KEYS = {
    "kind",
    "schema_version",
    "task_id",
    "objective_ref",
    "objective_category",
    "status",
    "mode",
    "accountable_owner",
    "acceptance_criteria_refs",
    "current_block",
    "accounting_scope",
    "cumulative_limits",
    "cumulative_usage_at_block_start",
    "block_delta",
    "cumulative_usage",
    "started_at",
    "absolute_deadline",
    "terminal_history",
    "previous_checkpoint",
    "approval_record_refs",
    "generation_decision_refs",
    "allowed_tool_refs",
    "file_ownership_ref",
    "completed_artifact_refs",
    "pending_action_codes",
    "blocked_reason_codes",
    "stop_reason",
    "next_action_code",
    "local_metrics",
}

OPAQUE_ID = re.compile(r"^[a-z][a-z0-9-]{1,31}_[a-f0-9]{32}$")
SAFE_CODE = re.compile(r"^[A-Z][A-Z0-9_]{1,63}$")
SAFE_REF = re.compile(r"^[a-z][a-z0-9-]{1,31}_[A-Za-z0-9._:-]{8,160}$")
GIT_OBJECT_ID = re.compile(r"^(?:[a-f0-9]{40}|[a-f0-9]{64})$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
AGENT_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _require_exact_keys(record: Mapping[str, Any], expected: set[str]) -> None:
    if not isinstance(record, Mapping):
        raise ContractError("record must be a mapping")
    missing = expected.difference(record)
    extra = set(record).difference(expected)
    if missing or extra:
        raise ContractError(
            f"record keys mismatch: missing={sorted(missing)} extra={sorted(extra)}"
        )


def _normalize_now(now: datetime) -> datetime:
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise ContractError("now must be a timezone-aware datetime")
    return now.astimezone(timezone.utc)


def _parse_utc(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ContractError(f"{field} must be an RFC3339 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"{field} is not RFC3339") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ContractError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _require_opaque(value: Any, field: str) -> str:
    if not isinstance(value, str) or not OPAQUE_ID.fullmatch(value):
        raise ContractError(f"{field} must be an opaque random identifier")
    return value


def _require_safe_ref(value: Any, field: str) -> str:
    if not isinstance(value, str) or not SAFE_REF.fullmatch(value):
        raise ContractError(f"{field} must be a sanitized opaque reference")
    return value


def _require_agent_id(value: Any, field: str) -> str:
    if not isinstance(value, str) or not AGENT_ID.fullmatch(value):
        raise ContractError(f"{field} must be a canonical agent ID")
    return value


def _validate_artifact_binding(binding: Any) -> None:
    if not isinstance(binding, Mapping) or set(binding) != {"kind", "value"}:
        raise ContractError("invalid artifact binding")
    kind = binding["kind"]
    value = binding["value"]
    if kind == "HEAD":
        if not isinstance(value, str) or not GIT_OBJECT_ID.fullmatch(value):
            raise ContractError("HEAD binding must be a full 40- or 64-hex Git object ID")
    elif kind == "SHA256":
        if not isinstance(value, str) or not SHA256.fullmatch(value):
            raise ContractError("SHA256 binding must contain exactly 64 lowercase hex characters")
    else:
        raise ContractError("artifact binding kind must be HEAD or SHA256")


def _validate_trusted_source(source: Any, trusted_source_refs: frozenset[str]) -> None:
    if not isinstance(source, Mapping) or set(source) != {
        "source_ref",
        "issuer_ref",
        "verifier_ref",
        "verification_ref",
        "result",
    }:
        raise ContractError("trusted_source is incomplete")
    source_ref = _require_safe_ref(source["source_ref"], "trusted_source.source_ref")
    _require_safe_ref(source["issuer_ref"], "trusted_source.issuer_ref")
    _require_safe_ref(source["verifier_ref"], "trusted_source.verifier_ref")
    _require_safe_ref(source["verification_ref"], "trusted_source.verification_ref")
    if source_ref not in trusted_source_refs or source["result"] != "VALID":
        raise ContractError("record source is not trusted by the store")


def _require_allowlisted_ref(
    value: Any,
    field: str,
    allowed: frozenset[str],
) -> str:
    reference = _require_safe_ref(value, field)
    if reference not in allowed:
        raise ContractError(f"{field} is not trusted by the store")
    return reference


@dataclass(frozen=True)
class ApprovalEvidence:
    approval_id: str
    nonce: str
    decision_evidence: str = "VALID_SYNTHETIC_EVIDENCE_ONLY"
    execution_authority: str = "NEVER_AUTOMATIC"
    executable: bool = False


def _validate_stored_approval_record(
    record: Mapping[str, Any],
    *,
    expected_task_id: str,
    expected_request_id: str,
    expected_action: str,
    expected_scope: Sequence[str],
    expected_targets: Sequence[str],
    expected_environment: str,
    expected_actor_ref: str,
    expected_artifact_or_head: Mapping[str, str],
    trusted_source_refs: frozenset[str],
    trusted_issuer_refs: frozenset[str],
    trusted_verifier_refs: frozenset[str],
    trusted_approver_refs: frozenset[str],
    now: datetime,
) -> ApprovalEvidence:
    _require_exact_keys(record, APPROVAL_KEYS)
    if record["kind"] != "ApprovalRecord" or record["schema_version"] != "1.1.0":
        raise ContractError("unsupported approval record")
    approval_id = _require_opaque(record["approval_id"], "approval_id")
    _require_opaque(record["task_id"], "task_id")
    _require_opaque(record["request_id"], "request_id")
    nonce = _require_opaque(record["nonce"], "nonce")

    if record["decision"] != "APPROVED":
        raise ContractError("approval decision is not APPROVED")
    if record["execution_authority"] != "NEVER_AUTOMATIC" or record["executable"] is not False:
        raise ContractError("approval evidence can never be executable")
    if record["single_use"] is not True or record["max_uses"] != 1:
        raise ContractError("approval evidence must be single-use")
    if type(record["use_count"]) is not int or record["use_count"] != 0 or record["consumed_at"] is not None:
        raise ContractError("approval evidence was already consumed")

    issued_at = _parse_utc(record["issued_at"], "issued_at")
    expires_at = _parse_utc(record["expires_at"], "expires_at")
    decision_at = _parse_utc(record["decision_at"], "decision_at")
    normalized_now = _normalize_now(now)
    if not issued_at <= decision_at <= normalized_now < expires_at:
        raise ContractError("approval evidence is not currently valid")

    _validate_trusted_source(record["trusted_source"], trusted_source_refs)
    _require_allowlisted_ref(
        record["trusted_source"]["issuer_ref"],
        "trusted_source.issuer_ref",
        trusted_issuer_refs,
    )
    _require_allowlisted_ref(
        record["trusted_source"]["verifier_ref"],
        "trusted_source.verifier_ref",
        trusted_verifier_refs,
    )
    if record["task_id"] != expected_task_id:
        raise ContractError("approval task mismatch")
    if record["request_id"] != expected_request_id:
        raise ContractError("approval request mismatch")
    if not isinstance(record["action"], str) or not SAFE_CODE.fullmatch(record["action"]):
        raise ContractError("approval action is invalid")
    if record["action"] != expected_action:
        raise ContractError("approval action mismatch")
    if not isinstance(record["scope"], list) or not record["scope"]:
        raise ContractError("approval scope must be a non-empty list")
    if not isinstance(record["targets"], list) or not record["targets"]:
        raise ContractError("approval targets must be a non-empty list")
    for index, reference in enumerate(record["scope"]):
        _require_safe_ref(reference, f"scope[{index}]")
    for index, reference in enumerate(record["targets"]):
        _require_safe_ref(reference, f"targets[{index}]")
    if list(record["scope"]) != list(expected_scope):
        raise ContractError("approval scope mismatch")
    if list(record["targets"]) != list(expected_targets):
        raise ContractError("approval target mismatch")
    if record["environment"] != expected_environment:
        raise ContractError("approval environment mismatch")
    if record["artifact_or_head"] != dict(expected_artifact_or_head):
        raise ContractError("approval artifact or HEAD mismatch")
    _validate_artifact_binding(record["artifact_or_head"])
    _require_safe_ref(record["actor_ref"], "actor_ref")
    if record["actor_ref"] != expected_actor_ref:
        raise ContractError("approval actor mismatch")
    _require_allowlisted_ref(record["approver_ref"], "approver_ref", trusted_approver_refs)

    justification = record["justification"]
    if not isinstance(justification, Mapping) or set(justification) != {"code", "evidence_refs"}:
        raise ContractError("justification must be structured")
    if not isinstance(justification["code"], str) or not SAFE_CODE.fullmatch(justification["code"]):
        raise ContractError("justification code is invalid")
    if not isinstance(justification["evidence_refs"], list) or not justification["evidence_refs"]:
        raise ContractError("justification requires sanitized evidence refs")
    for index, reference in enumerate(justification["evidence_refs"]):
        _require_safe_ref(reference, f"justification.evidence_refs[{index}]")

    return ApprovalEvidence(approval_id=approval_id, nonce=nonce)


class SyntheticApprovalStore:
    """Process-local, atomic store for synthetic contract tests only."""

    def __init__(
        self,
        records: Sequence[Mapping[str, Any]],
        *,
        trusted_source_refs: frozenset[str],
        trusted_issuer_refs: frozenset[str],
        trusted_verifier_refs: frozenset[str],
        trusted_approver_refs: frozenset[str],
        clock: Callable[[], datetime],
    ) -> None:
        self._records: dict[str, Mapping[str, Any]] = {}
        for record in records:
            approval_id = _require_opaque(record.get("approval_id"), "approval_id")
            if approval_id in self._records:
                raise ContractError("duplicate approval ID in synthetic store")
            self._records[approval_id] = deepcopy(dict(record))
        self._trusted_source_refs = frozenset(trusted_source_refs)
        self._trusted_issuer_refs = frozenset(trusted_issuer_refs)
        self._trusted_verifier_refs = frozenset(trusted_verifier_refs)
        self._trusted_approver_refs = frozenset(trusted_approver_refs)
        self._clock = clock
        self._consumed_ids: set[str] = set()
        self._consumed_nonces: set[str] = set()
        self._lock = Lock()

    def verify_and_consume(
        self,
        approval_id: str,
        *,
        expected_task_id: str,
        expected_request_id: str,
        expected_action: str,
        expected_scope: Sequence[str],
        expected_targets: Sequence[str],
        expected_environment: str,
        expected_actor_ref: str,
        expected_artifact_or_head: Mapping[str, str],
    ) -> ApprovalEvidence:
        _require_opaque(approval_id, "approval_id")
        if expected_environment != "NON_PRODUCTION_SYNTHETIC" or not expected_action.startswith("SYNTHETIC_"):
            raise ContractError("V1.1 store accepts synthetic actions and environment only")
        with self._lock:
            if approval_id in self._consumed_ids:
                raise ContractError("approval ID was already consumed")
            record = self._records.get(approval_id)
            if record is None:
                raise ContractError("approval ID is absent from the trusted synthetic store")
            nonce = record.get("nonce")
            if nonce in self._consumed_nonces:
                raise ContractError("approval nonce was already consumed")
            evidence = _validate_stored_approval_record(
                record,
                expected_task_id=expected_task_id,
                expected_request_id=expected_request_id,
                expected_action=expected_action,
                expected_scope=expected_scope,
                expected_targets=expected_targets,
                expected_environment=expected_environment,
                expected_actor_ref=expected_actor_ref,
                expected_artifact_or_head=expected_artifact_or_head,
                trusted_source_refs=self._trusted_source_refs,
                trusted_issuer_refs=self._trusted_issuer_refs,
                trusted_verifier_refs=self._trusted_verifier_refs,
                trusted_approver_refs=self._trusted_approver_refs,
                now=self._clock(),
            )
            self._consumed_ids.add(evidence.approval_id)
            self._consumed_nonces.add(evidence.nonce)
            return evidence


def validate_approval_evidence(
    approval_id: str,
    *,
    store: SyntheticApprovalStore,
    expected_task_id: str,
    expected_request_id: str,
    expected_action: str,
    expected_scope: Sequence[str],
    expected_targets: Sequence[str],
    expected_environment: str,
    expected_actor_ref: str,
    expected_artifact_or_head: Mapping[str, str],
) -> ApprovalEvidence:
    """Verify and atomically consume one synthetic decision by opaque ID.

    Callers cannot submit a record or trust anchors to this boundary. Exact type
    checking prevents a caller-supplied verifier from masquerading as the only
    V1.1 implementation. No real-store implementation is provided.
    """

    if type(store) is not SyntheticApprovalStore:
        raise ContractError("untrusted approval-store implementation")
    return store.verify_and_consume(
        approval_id,
        expected_task_id=expected_task_id,
        expected_request_id=expected_request_id,
        expected_action=expected_action,
        expected_scope=expected_scope,
        expected_targets=expected_targets,
        expected_environment=expected_environment,
        expected_actor_ref=expected_actor_ref,
        expected_artifact_or_head=expected_artifact_or_head,
    )


@dataclass(frozen=True)
class GenerationDecisionEvidence:
    decision_id: str
    nonce: str
    decision_evidence: str = "VALID_SYNTHETIC_LEDGER_EVIDENCE_ONLY"
    execution_authority: str = "LEDGER_TRANSITION_ONLY"
    executable: bool = False


def _validate_stored_generation_decision(
    record: Mapping[str, Any],
    *,
    expected_task_id: str,
    expected_prior_stop_reason: str,
    expected_prior_terminal_evidence_ref: str,
    expected_prior_ledger_sha256: str,
    expected_from_generation: int,
    expected_to_generation: int,
    trusted_source_refs: frozenset[str],
    trusted_issuer_refs: frozenset[str],
    trusted_verifier_refs: frozenset[str],
    trusted_approver_refs: frozenset[str],
    now: datetime,
) -> GenerationDecisionEvidence:
    _require_exact_keys(record, GENERATION_DECISION_KEYS)
    if record["kind"] != "GenerationDecisionRecord" or record["schema_version"] != "1.1.0":
        raise ContractError("unsupported generation decision record")
    decision_id = _require_opaque(record["decision_id"], "decision_id")
    _require_opaque(record["task_id"], "task_id")
    nonce = _require_opaque(record["nonce"], "nonce")
    if record["action"] != "REOPEN_SYNTHETIC_TASK":
        raise ContractError("generation decision action is not synthetic")
    if record["environment"] != "NON_PRODUCTION_SYNTHETIC":
        raise ContractError("generation decision environment is not synthetic")
    if record["decision"] != "APPROVED":
        raise ContractError("generation decision is not APPROVED")
    if record["execution_authority"] != "LEDGER_TRANSITION_ONLY" or record["executable"] is not False:
        raise ContractError("generation decision cannot execute work")
    if record["single_use"] is not True or record["max_uses"] != 1:
        raise ContractError("generation decision must be single-use")
    if type(record["use_count"]) is not int or record["use_count"] != 0 or record["consumed_at"] is not None:
        raise ContractError("generation decision was already consumed")
    issued_at = _parse_utc(record["issued_at"], "issued_at")
    expires_at = _parse_utc(record["expires_at"], "expires_at")
    decision_at = _parse_utc(record["decision_at"], "decision_at")
    normalized_now = _normalize_now(now)
    if not issued_at <= decision_at <= normalized_now < expires_at:
        raise ContractError("generation decision is not currently valid")
    _validate_trusted_source(record["trusted_source"], trusted_source_refs)
    _require_allowlisted_ref(
        record["trusted_source"]["issuer_ref"],
        "trusted_source.issuer_ref",
        trusted_issuer_refs,
    )
    _require_allowlisted_ref(
        record["trusted_source"]["verifier_ref"],
        "trusted_source.verifier_ref",
        trusted_verifier_refs,
    )
    _require_safe_ref(record["prior_terminal_evidence_ref"], "prior_terminal_evidence_ref")
    _require_allowlisted_ref(record["approver_ref"], "approver_ref", trusted_approver_refs)
    expected = {
        "task_id": expected_task_id,
        "prior_stop_reason": expected_prior_stop_reason,
        "prior_terminal_evidence_ref": expected_prior_terminal_evidence_ref,
        "prior_ledger_sha256": expected_prior_ledger_sha256,
        "from_generation": expected_from_generation,
        "to_generation": expected_to_generation,
    }
    for field, value in expected.items():
        if record[field] != value:
            raise ContractError(f"generation decision binding mismatch: {field}")
    if record["prior_stop_reason"] not in STOP_REASONS:
        raise ContractError("generation decision prior stop reason is invalid")
    if type(record["from_generation"]) is not int or type(record["to_generation"]) is not int:
        raise ContractError("generation values must be integers")
    if record["from_generation"] < 1 or record["to_generation"] != record["from_generation"] + 1:
        raise ContractError("generation decision must increment exactly once")
    return GenerationDecisionEvidence(decision_id=decision_id, nonce=nonce)


class SyntheticGenerationDecisionStore:
    """Process-local, atomic generation-decision store for synthetic tests."""

    def __init__(
        self,
        records: Sequence[Mapping[str, Any]],
        *,
        trusted_source_refs: frozenset[str],
        trusted_issuer_refs: frozenset[str],
        trusted_verifier_refs: frozenset[str],
        trusted_approver_refs: frozenset[str],
        clock: Callable[[], datetime],
    ) -> None:
        self._records: dict[str, Mapping[str, Any]] = {}
        for record in records:
            decision_id = _require_opaque(record.get("decision_id"), "decision_id")
            if decision_id in self._records:
                raise ContractError("duplicate decision ID in synthetic store")
            self._records[decision_id] = deepcopy(dict(record))
        self._trusted_source_refs = frozenset(trusted_source_refs)
        self._trusted_issuer_refs = frozenset(trusted_issuer_refs)
        self._trusted_verifier_refs = frozenset(trusted_verifier_refs)
        self._trusted_approver_refs = frozenset(trusted_approver_refs)
        self._clock = clock
        self._consumed_ids: set[str] = set()
        self._consumed_nonces: set[str] = set()
        self._lock = Lock()

    def verify_and_consume(
        self,
        decision_id: str,
        *,
        expected_task_id: str,
        expected_prior_stop_reason: str,
        expected_prior_terminal_evidence_ref: str,
        expected_prior_ledger_sha256: str,
        expected_from_generation: int,
        expected_to_generation: int,
    ) -> GenerationDecisionEvidence:
        _require_opaque(decision_id, "decision_id")
        with self._lock:
            if decision_id in self._consumed_ids:
                raise ContractError("generation decision ID was already consumed")
            record = self._records.get(decision_id)
            if record is None:
                raise ContractError("generation decision is absent from the trusted synthetic store")
            nonce = record.get("nonce")
            if nonce in self._consumed_nonces:
                raise ContractError("generation decision nonce was already consumed")
            evidence = _validate_stored_generation_decision(
                record,
                expected_task_id=expected_task_id,
                expected_prior_stop_reason=expected_prior_stop_reason,
                expected_prior_terminal_evidence_ref=expected_prior_terminal_evidence_ref,
                expected_prior_ledger_sha256=expected_prior_ledger_sha256,
                expected_from_generation=expected_from_generation,
                expected_to_generation=expected_to_generation,
                trusted_source_refs=self._trusted_source_refs,
                trusted_issuer_refs=self._trusted_issuer_refs,
                trusted_verifier_refs=self._trusted_verifier_refs,
                trusted_approver_refs=self._trusted_approver_refs,
                now=self._clock(),
            )
            self._consumed_ids.add(evidence.decision_id)
            self._consumed_nonces.add(evidence.nonce)
            return evidence


GLOB_CHARS = set("*?[]{}")
WINDOWS_FORBIDDEN_CHARS = set('<>"|')
WINDOWS_RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL"} | {
    f"{prefix}{number}" for prefix in ("COM", "LPT") for number in range(1, 10)
}


def _claim_path_parts(value: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not isinstance(value, str) or not value:
        raise ContractError("claim path must be a non-empty relative path")
    if value != value.strip():
        raise ContractError("leading or trailing path whitespace is forbidden")
    candidate = value.replace("\\", "/")
    if candidate.startswith("/") or candidate.startswith("//") or re.match(r"^[A-Za-z]:", candidate):
        raise ContractError("absolute, UNC and drive paths are forbidden")
    if any(char in candidate for char in GLOB_CHARS):
        raise ContractError("glob claims are forbidden in V1.1; enumerate exact paths")
    raw_segments = candidate.split("/")
    original_segments: list[str] = []
    normalized_segments: list[str] = []
    for segment in raw_segments:
        if segment in {"", ".", ".."}:
            raise ContractError("empty, dot and traversal segments are forbidden")
        if segment.startswith(" ") or segment.endswith((".", " ")):
            raise ContractError("Windows leading-space, trailing-dot or trailing-space aliases are forbidden")
        if ":" in segment:
            raise ContractError("alternate streams and colon syntax are forbidden")
        if "~" in segment:
            raise ContractError("Windows short-name aliases are forbidden")
        if any(char in WINDOWS_FORBIDDEN_CHARS for char in segment):
            raise ContractError("Windows-forbidden path characters are forbidden")
        if any(unicodedata.category(char).startswith("C") for char in segment):
            raise ContractError("control, format and private-use path characters are forbidden")
        compatible = unicodedata.normalize("NFKC", segment)
        if compatible != segment:
            raise ContractError("Unicode compatibility path aliases are forbidden")
        device_base = segment.split(".", 1)[0].upper()
        if device_base in WINDOWS_RESERVED_NAMES:
            raise ContractError("Windows reserved device names are forbidden")
        original_segments.append(segment)
        normalized_segments.append(compatible.casefold())
    return tuple(original_segments), tuple(normalized_segments)


def normalize_claim_path(value: str) -> tuple[str, ...]:
    """Return the Windows comparison key without rewriting filesystem input."""

    return _claim_path_parts(value)[1]


def _is_reparse(path: Path) -> bool:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    attributes = getattr(info, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return path.is_symlink() or bool(attributes & reparse_flag)


def _repository_path(repository_root: Path, claim_path: str) -> Path:
    root = repository_root.absolute()
    original_segments, _ = _claim_path_parts(claim_path)
    return root.joinpath(*original_segments)


def assert_no_reparse_ancestors(
    repository_root: Path,
    claim_path: str,
    *,
    known_reparse_paths: frozenset[str] = frozenset(),
) -> None:
    original_segments, compare_segments = _claim_path_parts(claim_path)
    root = repository_root.absolute()
    if not root.exists() or not root.is_dir():
        raise ContractError("repository root must be an existing directory")
    if _is_reparse(root):
        raise ContractError("repository root is a reparse point")
    normalized_known = {"/".join(normalize_claim_path(item)) for item in known_reparse_paths}
    current = root
    for original_segment, compare_segment in zip(original_segments, compare_segments):
        current = current / original_segment
        prior = current.parent.relative_to(root).as_posix().casefold()
        relative = compare_segment if prior == "." else f"{prior}/{compare_segment}"
        if relative in normalized_known or _is_reparse(current):
            raise ContractError(f"reparse point in claim ancestry: {relative}")


def _claim_shape(
    claim: Mapping[str, Any],
) -> tuple[tuple[str, ...], str, str, str, str, str]:
    required = {
        "claim_id",
        "path",
        "path_type",
        "path_scope",
        "owner",
        "access",
        "step",
        "dependencies",
        "status",
    }
    _require_exact_keys(claim, required)
    path = normalize_claim_path(claim["path"])
    path_type = claim["path_type"]
    access = claim["access"]
    status = claim["status"]
    if path_type not in {"FILE", "DIRECTORY"} or claim["path_scope"] != "EXACT":
        raise ContractError("claims require exact FILE or DIRECTORY scope")
    if access not in {"READ", "WRITE"}:
        raise ContractError("claim access must be READ or WRITE")
    if status not in {"PLANNED", "ACTIVE", "COMPLETE", "BLOCKED"}:
        raise ContractError("claim status is invalid")
    claim_id = _require_opaque(claim["claim_id"], "claim_id")
    owner = _require_agent_id(claim["owner"], "owner")
    step = _require_safe_ref(claim["step"], "step")
    if not isinstance(claim["dependencies"], list):
        raise ContractError("dependencies must be a list")
    for index, dependency in enumerate(claim["dependencies"]):
        _require_safe_ref(dependency, f"dependencies[{index}]")
    return path, path_type, access, owner, status, claim_id + ":" + step


def _assert_existing_claim_type(repository_root: Path, claim: Mapping[str, Any]) -> None:
    _, path_type, _, _, _, _ = _claim_shape(claim)
    assert_no_reparse_ancestors(repository_root, claim["path"])
    target = _repository_path(repository_root, claim["path"])
    if not target.exists():
        raise ContractError("preflight claims require an existing unambiguous target")
    actual_type = "DIRECTORY" if target.is_dir() else "FILE" if target.is_file() else "OTHER"
    if actual_type != path_type:
        raise ContractError(
            f"declared path_type {path_type} does not match existing target type {actual_type}"
        )


def _existing_path_identity(repository_root: Path, claim: Mapping[str, Any]) -> tuple[int, int]:
    target = _repository_path(repository_root, claim["path"])
    info = target.stat(follow_symlinks=False)
    return int(info.st_dev), int(info.st_ino)


def _paths_overlap(left_path: tuple[str, ...], right_path: tuple[str, ...]) -> bool:
    return (
        left_path[: len(right_path)] == right_path
        or right_path[: len(left_path)] == left_path
    )


def claims_overlap(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    left_path = _claim_shape(left)[0]
    right_path = _claim_shape(right)[0]
    return _paths_overlap(left_path, right_path)


def validate_parallel_claims(
    claims: Sequence[Mapping[str, Any]],
    *,
    repository_root: Path,
) -> None:
    shaped = [_claim_shape(claim) for claim in claims]
    claim_ids = [claim["claim_id"] for claim in claims]
    if len(set(claim_ids)) != len(claim_ids):
        raise ContractError("claim IDs must be unique")
    for claim, shape in zip(claims, shaped):
        if shape[4] not in {"PLANNED", "ACTIVE"}:
            raise ContractError("parallel preflight accepts only PLANNED or ACTIVE claims")
        _assert_existing_claim_type(repository_root, claim)
    for index, left in enumerate(claims):
        for right_index in range(index + 1, len(claims)):
            right = claims[right_index]
            same_object = _existing_path_identity(repository_root, left) == _existing_path_identity(
                repository_root, right
            )
            if not claims_overlap(left, right) and not same_object:
                continue
            if shaped[index][2] == "WRITE" or shaped[right_index][2] == "WRITE":
                raise ContractError("parallel WRITE/WRITE or WRITE/READ ancestry conflict")


def _claim_covers_path(claim: Mapping[str, Any], path: tuple[str, ...]) -> bool:
    claim_path, path_type, _, _, _, _ = _claim_shape(claim)
    return path == claim_path or (
        path_type == "DIRECTORY" and path[: len(claim_path)] == claim_path
    )


def assert_diff_within_write_claims(
    changed_paths: Iterable[str],
    claims: Sequence[Mapping[str, Any]],
    *,
    repository_root: Path,
    owner: str,
    step: str,
) -> None:
    _require_agent_id(owner, "owner")
    _require_safe_ref(step, "step")
    write_claims = []
    for claim in claims:
        shape = _claim_shape(claim)
        if shape[2] == "WRITE" and shape[3] == owner and shape[4] == "ACTIVE" and claim["step"] == step:
            assert_no_reparse_ancestors(repository_root, claim["path"])
            write_claims.append(claim)
    if not write_claims:
        raise ContractError("post-diff reconciliation requires an ACTIVE WRITE claim for owner and step")
    for changed in changed_paths:
        assert_no_reparse_ancestors(repository_root, changed)
        changed_path = normalize_claim_path(changed)
        if not any(_claim_covers_path(claim, changed_path) for claim in write_claims):
            raise ContractError(f"real diff path is outside ACTIVE WRITE claims: {changed}")


def validate_claim_transition(previous: Mapping[str, Any], current: Mapping[str, Any]) -> None:
    previous_shape = _claim_shape(previous)
    current_shape = _claim_shape(current)
    immutable_fields = {
        "claim_id",
        "path",
        "path_type",
        "path_scope",
        "owner",
        "access",
        "step",
        "dependencies",
    }
    if any(previous[field] != current[field] for field in immutable_fields):
        raise ContractError("claim identity and authority fields are immutable")
    allowed = {
        "PLANNED": {"ACTIVE", "BLOCKED"},
        "ACTIVE": {"COMPLETE", "BLOCKED"},
        "COMPLETE": set(),
        "BLOCKED": set(),
    }
    if current_shape[4] not in allowed[previous_shape[4]]:
        raise ContractError("invalid or terminal claim status transition")


CUMULATIVE_COUNTERS = (
    "task_generation",
    "loop_instances",
    "total_rounds",
    "total_provider_turns",
    "total_tool_calls",
    "total_budget_units",
    "reopen_count",
)

LIMIT_FOR_COUNTER = {
    "task_generation": "max_task_generations",
    "loop_instances": "max_loop_instances",
    "total_rounds": "max_total_rounds",
    "total_provider_turns": "max_total_provider_turns",
    "total_tool_calls": "max_total_tool_calls",
    "total_budget_units": "max_total_budget_units",
    "reopen_count": "max_reopens",
}

LIMIT_KEYS = set(LIMIT_FOR_COUNTER.values()) | {"absolute_timeout_minutes"}
BLOCK_DELTA_KEYS = {
    "loop_instances",
    "rounds",
    "provider_turns",
    "tool_calls",
    "budget_units",
    "elapsed_time_ms",
}
TERMINAL_EVENT_KEYS = {"generation", "reason", "at", "evidence_ref"}


def _validate_ledger_time_and_history(record: Mapping[str, Any], *, now: datetime) -> None:
    _require_exact_keys(record, LEDGER_KEYS)
    if record["kind"] != "TaskLedger" or record["schema_version"] != "1.1.0":
        raise ContractError("unsupported task ledger")
    _require_opaque(record["task_id"], "task_id")
    normalized_now = _normalize_now(now)
    started_at = _parse_utc(record["started_at"], "started_at")
    deadline = _parse_utc(record["absolute_deadline"], "absolute_deadline")
    if normalized_now < started_at:
        raise ContractError("ledger cannot be evaluated before started_at")
    limits = record["cumulative_limits"]
    _require_exact_keys(limits, LIMIT_KEYS)
    timeout_minutes = limits["absolute_timeout_minutes"]
    if type(timeout_minutes) is not int or timeout_minutes < 1:
        raise ContractError("absolute timeout must be a positive integer")
    if not started_at < deadline <= started_at + timedelta(minutes=timeout_minutes):
        raise ContractError("absolute_deadline exceeds the configured absolute timeout")

    for usage_name in ("cumulative_usage_at_block_start", "cumulative_usage"):
        usage = record[usage_name]
        _require_exact_keys(usage, set(CUMULATIVE_COUNTERS))
        for counter, value in usage.items():
            if type(value) is not int or value < (1 if counter == "task_generation" else 0):
                raise ContractError(f"invalid cumulative counter: {usage_name}.{counter}")
    _require_exact_keys(record["block_delta"], BLOCK_DELTA_KEYS)
    for field, value in record["block_delta"].items():
        if type(value) is not int or value < 0:
            raise ContractError(f"invalid block delta: {field}")

    history = record["terminal_history"]
    if not isinstance(history, list):
        raise ContractError("terminal history must be a list")
    last_at = started_at
    seen_generations: set[int] = set()
    current_generation = record["cumulative_usage"]["task_generation"]
    for index, event in enumerate(history):
        _require_exact_keys(event, TERMINAL_EVENT_KEYS)
        generation = event["generation"]
        if type(generation) is not int or not 1 <= generation <= current_generation:
            raise ContractError("terminal event generation is outside ledger generations")
        if generation in seen_generations:
            raise ContractError("each task generation may have at most one terminal event")
        seen_generations.add(generation)
        reason = event["reason"]
        if reason not in STOP_REASONS:
            raise ContractError("terminal event reason is invalid")
        event_at = _parse_utc(event["at"], f"terminal_history[{index}].at")
        if not last_at <= event_at <= deadline or event_at > normalized_now:
            raise ContractError("terminal event time is outside the monotonic task window")
        last_at = event_at
        _require_safe_ref(event["evidence_ref"], f"terminal_history[{index}].evidence_ref")

    current_stop = record.get("stop_reason")
    if current_stop is not None:
        if current_stop not in STOP_REASONS or not history:
            raise ContractError("terminal ledger requires a terminal event")
        last = history[-1]
        if last["reason"] != current_stop or last["generation"] != current_generation:
            raise ContractError("terminal history must end with the current generation and stop reason")
    elif history and history[-1]["generation"] == current_generation:
        raise ContractError("current generation cannot be running after its terminal event")
    if normalized_now >= deadline and current_stop != "TIMEOUT":
        raise ContractError("ledger at or past the absolute deadline must terminate with TIMEOUT")

    generation_refs = record["generation_decision_refs"]
    if not isinstance(generation_refs, list):
        raise ContractError("generation_decision_refs must be a list")
    for index, decision_ref in enumerate(generation_refs):
        _require_opaque(decision_ref, f"generation_decision_refs[{index}]")


def canonical_ledger_sha256(record: Mapping[str, Any]) -> str:
    """Hash the complete prior ledger with deterministic UTF-8 JSON."""

    try:
        encoded = json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractError("ledger is not canonically serializable") from exc
    return hashlib.sha256(encoded).hexdigest()


def validate_ledger_transition(
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    now: datetime,
    generation_decision_store: SyntheticGenerationDecisionStore | None = None,
    generation_decision_id: str | None = None,
) -> None:
    _validate_ledger_time_and_history(previous, now=now)
    _validate_ledger_time_and_history(current, now=now)
    if previous["task_id"] != current["task_id"]:
        raise ContractError("task_id cannot change across a handoff")
    if previous["started_at"] != current["started_at"]:
        raise ContractError("started_at cannot be reset")
    if previous["absolute_deadline"] != current["absolute_deadline"]:
        raise ContractError("absolute_deadline cannot be extended by a handoff")
    if previous["cumulative_limits"] != current["cumulative_limits"]:
        raise ContractError("global limits cannot be reset or expanded")
    if current["cumulative_usage_at_block_start"] != previous["cumulative_usage"]:
        raise ContractError("usage at block start must equal the previous cumulative usage")

    prior_history = previous["terminal_history"]
    current_history = current["terminal_history"]
    if current_history[: len(prior_history)] != prior_history:
        raise ContractError("terminal history must be append-only")
    if len(current_history) > len(prior_history) + 1:
        raise ContractError("a transition may append at most one terminal event")

    for counter in CUMULATIVE_COUNTERS:
        before = previous["cumulative_usage"][counter]
        after = current["cumulative_usage"][counter]
        if after < before:
            raise ContractError(f"cumulative counter reset: {counter}")
        limit = current["cumulative_limits"][LIMIT_FOR_COUNTER[counter]]
        if type(limit) is not int or limit < 0 or after > limit:
            raise ContractError(f"cumulative limit exceeded: {counter}")

    generation_delta = (
        current["cumulative_usage"]["task_generation"]
        - previous["cumulative_usage"]["task_generation"]
    )
    if generation_delta not in {0, 1}:
        raise ContractError("task_generation may increase only once per trusted decision")
    prior_stop = previous.get("stop_reason")
    if prior_stop is not None and generation_delta == 0:
        raise ContractError("a terminal task cannot be reopened in the same generation")
    prior_decision_refs = previous["generation_decision_refs"]
    current_decision_refs = current["generation_decision_refs"]
    if generation_delta == 1:
        if prior_stop not in STOP_REASONS or not prior_history:
            raise ContractError("only a terminal task can enter a new generation")
        if type(generation_decision_store) is not SyntheticGenerationDecisionStore:
            raise ContractError("new task generation requires the trusted synthetic decision store")
        decision_id = _require_opaque(generation_decision_id, "generation_decision_id")
        if current_decision_refs != prior_decision_refs + [decision_id]:
            raise ContractError("generation decision reference must append exactly once")
        if current["cumulative_usage"]["reopen_count"] != previous["cumulative_usage"]["reopen_count"] + 1:
            raise ContractError("reopen_count must increment with task_generation")
    else:
        if generation_decision_store is not None or generation_decision_id is not None:
            raise ContractError("generation evidence is forbidden without a generation increment")
        if current_decision_refs != prior_decision_refs:
            raise ContractError("generation decision references are append-only and transition-bound")
        if current["cumulative_usage"]["reopen_count"] != previous["cumulative_usage"]["reopen_count"]:
            raise ContractError("reopen_count cannot change without task_generation")

    delta_fields = {
        "loop_instances": "loop_instances",
        "total_rounds": "rounds",
        "total_provider_turns": "provider_turns",
        "total_tool_calls": "tool_calls",
        "total_budget_units": "budget_units",
    }
    for cumulative_field, delta_field in delta_fields.items():
        expected_total = (
            current["cumulative_usage_at_block_start"][cumulative_field]
            + current["block_delta"][delta_field]
        )
        if current["cumulative_usage"][cumulative_field] != expected_total:
            raise ContractError(f"block delta does not reconcile: {cumulative_field}")

    if generation_delta == 1:
        assert generation_decision_store is not None
        assert generation_decision_id is not None
        generation_decision_store.verify_and_consume(
            generation_decision_id,
            expected_task_id=previous["task_id"],
            expected_prior_stop_reason=prior_stop,
            expected_prior_terminal_evidence_ref=prior_history[-1]["evidence_ref"],
            expected_prior_ledger_sha256=canonical_ledger_sha256(previous),
            expected_from_generation=previous["cumulative_usage"]["task_generation"],
            expected_to_generation=current["cumulative_usage"]["task_generation"],
        )


def validate_evaluation_independence(
    record: Mapping[str, Any],
    claims: Sequence[Mapping[str, Any]],
    *,
    agent_capabilities: Mapping[str, Mapping[str, Any]],
    repository_root: Path,
    now: datetime,
) -> None:
    _require_exact_keys(record, EVALUATION_KEYS)
    if record["kind"] != "EvaluationRecord" or record["schema_version"] != "1.1.0":
        raise ContractError("unsupported evaluation record")
    _require_opaque(record["evaluation_id"], "evaluation_id")
    _require_opaque(record["task_id"], "task_id")
    author = _require_agent_id(record["author_agent_id"], "author_agent_id")
    evaluator = _require_agent_id(record["evaluator_agent_id"], "evaluator_agent_id")
    if author == evaluator:
        raise ContractError("author and evaluator must be distinct")
    if record["evaluator_capability"] != "INDEPENDENT_EVALUATOR":
        raise ContractError("evaluator lacks the independent-evaluator capability")
    evaluator_capabilities = agent_capabilities.get(evaluator)
    if not isinstance(evaluator_capabilities, Mapping):
        raise ContractError("evaluator is absent from the trusted agent registry")
    if evaluator_capabilities.get("can_evaluate") is not True or evaluator_capabilities.get(
        "must_be_independent_from_author"
    ) is not True:
        raise ContractError("trusted agent registry does not grant independent evaluation capability")
    if record["execution_authority"] != "EVIDENCE_ONLY" or record["executable"] is not False:
        raise ContractError("evaluation records are evidence-only")
    if record["decision"] not in {"PASS", "CHANGES_REQUIRED", "BLOCKED"}:
        raise ContractError("evaluation decision is invalid")
    evaluation_at = _parse_utc(record["evaluation_at"], "evaluation_at")
    if evaluation_at > _normalize_now(now):
        raise ContractError("evaluation_at cannot be in the future")
    _validate_artifact_binding(record["artifact_or_head"])
    for index, finding_ref in enumerate(record["finding_refs"]):
        _require_safe_ref(finding_ref, f"finding_refs[{index}]")

    evaluated_paths_raw = record["evaluated_paths"]
    if not isinstance(evaluated_paths_raw, list) or not evaluated_paths_raw:
        raise ContractError("evaluation requires at least one evaluated path")
    evaluated_paths = [normalize_claim_path(path) for path in evaluated_paths_raw]
    if len(set(evaluated_paths)) != len(evaluated_paths):
        raise ContractError("evaluated paths must be unique after Windows normalization")
    report_path = normalize_claim_path(record["report_path"])
    if any(_paths_overlap(report_path, path) for path in evaluated_paths):
        raise ContractError("evaluation report path must be separate from evaluated artifacts")
    for raw_path in [*evaluated_paths_raw, record["report_path"]]:
        assert_no_reparse_ancestors(repository_root, raw_path)

    claim_by_id = {claim["claim_id"]: claim for claim in claims}
    if len(claim_by_id) != len(claims):
        raise ContractError("claim IDs must be unique")
    author_claim_ids = record["author_claim_refs"]
    if not isinstance(author_claim_ids, list) or not author_claim_ids:
        raise ContractError("evaluation requires author claim references")
    author_claims = []
    for index, claim_id in enumerate(author_claim_ids):
        _require_opaque(claim_id, f"author_claim_refs[{index}]")
        claim = claim_by_id.get(claim_id)
        if claim is None:
            raise ContractError("referenced author claim is absent")
        shape = _claim_shape(claim)
        if shape[2] != "WRITE" or shape[3] != author or shape[4] != "COMPLETE":
            raise ContractError("author claim must be a COMPLETE WRITE claim owned by the author")
        _assert_existing_claim_type(repository_root, claim)
        author_claims.append(claim)
    for evaluated_path in evaluated_paths:
        if not any(_claim_covers_path(claim, evaluated_path) for claim in author_claims):
            raise ContractError("evaluated artifact is not covered by an author claim")

    report_claim_id = _require_opaque(
        record["evaluator_report_claim_ref"], "evaluator_report_claim_ref"
    )
    report_claim = claim_by_id.get(report_claim_id)
    if report_claim is None:
        raise ContractError("evaluator report claim is absent")
    report_shape = _claim_shape(report_claim)
    if report_shape[2] != "WRITE" or report_shape[3] != evaluator or report_shape[4] != "COMPLETE":
        raise ContractError("report claim must be a COMPLETE WRITE claim owned by the evaluator")
    _assert_existing_claim_type(repository_root, report_claim)
    if not _claim_covers_path(report_claim, report_path):
        raise ContractError("evaluation report is outside the evaluator report claim")
    for claim in claims:
        shape = _claim_shape(claim)
        if shape[2] == "WRITE" and shape[3] == evaluator:
            if any(_claim_covers_path(claim, path) for path in evaluated_paths):
                raise ContractError("evaluator has a WRITE claim over an evaluated artifact")


METRIC_ENUMS = {
    "routing_mode": {
        "SINGLE_SPECIALIST",
        "SPECIALIST_PLUS_REVIEWER",
        "SEQUENTIAL_PIPELINE",
        "ORCHESTRATOR_WORKERS",
        "CONTROLLED_PARALLEL",
        "EVALUATOR_OPTIMIZER_LOOP",
        "LONG_RUNNING_INCREMENTAL",
        "INCIDENT_MODE",
        "RELEASE_MODE",
    },
    "stop_reason": STOP_REASONS,
}

METRIC_NUMBERS = {
    "selected_agent_count",
    "selected_skill_count",
    "rounds",
    "reopen_count",
    "provider_calls",
    "tool_calls",
    "reviewer_findings",
    "elapsed_time_ms",
    "budget_units",
    "approval_gate_hits",
}


def validate_metrics_configuration(*, enabled: bool, sink: str) -> None:
    if type(enabled) is not bool:
        raise ContractError("metrics enabled must be a boolean")
    if enabled is False and sink != "DISABLED":
        raise ContractError("disabled metrics require the DISABLED sink")
    if enabled is True and sink not in {"MEMORY_ONLY", "PRIVATE_LOCAL_FILE"}:
        raise ContractError("enabled metrics require a private local sink")


def validate_local_metrics(metrics: Mapping[str, Any]) -> None:
    allowed = set(METRIC_ENUMS) | METRIC_NUMBERS
    extra = set(metrics).difference(allowed)
    if extra:
        raise ContractError(f"metrics contain non-allowlisted fields: {sorted(extra)}")
    for field, allowed_values in METRIC_ENUMS.items():
        if field in metrics and metrics[field] not in allowed_values:
            raise ContractError(f"invalid metric enum: {field}")
    for field in METRIC_NUMBERS:
        if field in metrics and (
            not isinstance(metrics[field], int) or isinstance(metrics[field], bool) or metrics[field] < 0
        ):
            raise ContractError(f"metric must be a non-negative integer: {field}")


__all__ = [
    "ApprovalEvidence",
    "ContractError",
    "GenerationDecisionEvidence",
    "SyntheticApprovalStore",
    "SyntheticGenerationDecisionStore",
    "assert_diff_within_write_claims",
    "assert_no_reparse_ancestors",
    "canonical_ledger_sha256",
    "claims_overlap",
    "normalize_claim_path",
    "validate_approval_evidence",
    "validate_claim_transition",
    "validate_evaluation_independence",
    "validate_ledger_transition",
    "validate_local_metrics",
    "validate_metrics_configuration",
    "validate_parallel_claims",
]
