"""Build continuity records from runtime evidence, never from conversation memory."""

from __future__ import annotations

from .models import HandoffRecord, LoopState, StopReason, TaskEnvelope


def build_handoff(task: TaskEnvelope, loop: LoopState) -> HandoffRecord:
    passed = loop.stop_reason is StopReason.PASS
    blockers = () if passed else (f"Runtime stopped with {loop.stop_reason}.",)
    next_block = (
        "Review the synthetic artifacts; authorize a separate implementation before real changes."
        if passed
        else f"Resolve {loop.stop_reason} before starting another bounded round."
    )
    return HandoffRecord(
        objective=task.objective,
        state=loop.stop_reason,
        changed_files=(),
        decisions=("Mock-only execution preserved all external safety boundaries.",),
        tests_executed=(),
        not_executed=(
            "Network or real provider calls",
            "Shell or Git commands",
            "Database, deploy, payment, or message operations",
            "Real project file access",
        ),
        risks=("This reference run does not prove real application behavior.",),
        blockers=blockers,
        exact_next_block=next_block,
        next_files_to_read=(),
        rollback=(
            "Discard the in-memory mock artifacts and local sanitized trace file, "
            "if one was enabled."
        ),
    )
