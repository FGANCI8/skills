from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from renova_aura_agent_os.models import (
    TaskEnvelope,
    TaskFacts,
    TraceEvent,
    TraceEventName,
    TraceOutcome,
)
from renova_aura_agent_os.orchestrator import AgentOS
from renova_aura_agent_os.tracing import JsonlTraceSink, task_fingerprint


class HandoffTracingTests(unittest.TestCase):
    def test_handoff_never_invents_git_or_changed_files(self) -> None:
        result = asyncio.run(
            AgentOS().run(
                TaskEnvelope(
                    objective="Documente este exemplo.",
                    facts=TaskFacts(affected_areas=("documentation",)),
                )
            )
        )
        self.assertEqual("NOT_APPLICABLE", result.handoff.branch)
        self.assertEqual("NOT_APPLICABLE", result.handoff.head)
        self.assertEqual((), result.handoff.changed_files)

    def test_jsonl_trace_contains_no_raw_objective(self) -> None:
        objective = "Sensitive synthetic marker must never appear in a trace"
        run_id = uuid4()
        with tempfile.TemporaryDirectory() as temporary_directory:
            sink = JsonlTraceSink(Path(temporary_directory), run_id)
            sink.emit(
                TraceEvent(
                    event_name=TraceEventName.RUN_STARTED,
                    run_id=run_id,
                    task_fingerprint=task_fingerprint(objective),
                    objective_chars=len(objective),
                    round_number=0,
                    outcome=TraceOutcome.STARTED,
                )
            )
            raw = sink.path.read_text(encoding="utf-8")
            payload = json.loads(raw)
        self.assertNotIn(objective, raw)
        self.assertNotIn("Sensitive synthetic marker", raw)
        self.assertEqual(task_fingerprint(objective), payload["task_fingerprint"])


if __name__ == "__main__":
    unittest.main()
