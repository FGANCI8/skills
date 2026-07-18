"""Local, allowlisted tracing with a closed sanitized event schema."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Protocol
from uuid import UUID

from .models import TraceEvent


def task_fingerprint(objective: str) -> str:
    return hashlib.sha256(objective.encode("utf-8")).hexdigest()


class TraceSink(Protocol):
    def emit(self, event: TraceEvent) -> None:
        """Store a schema-closed event without raw task content."""


class InMemoryTraceSink:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    def emit(self, event: TraceEvent) -> None:
        self.events.append(event)


class JsonlTraceSink:
    """Write only beneath an existing caller-provided directory."""

    def __init__(self, trace_root: Path, run_id: UUID) -> None:
        root = trace_root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("trace root must be an existing directory")
        target = (root / f"{run_id}.jsonl").resolve()
        if target.parent != root:
            raise ValueError("trace target escaped the allowlisted root")
        self.run_id = run_id
        self.path = target

    def emit(self, event: TraceEvent) -> None:
        if event.run_id != self.run_id:
            raise ValueError("trace event run id does not match the sink")
        payload = event.model_dump(mode="json")
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
            stream.write("\n")
