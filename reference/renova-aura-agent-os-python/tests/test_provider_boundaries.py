from __future__ import annotations

import asyncio
import json
import os
import socket
import subprocess
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from pydantic import ValidationError

from renova_aura_agent_os.models import RuntimePolicy, StopReason, TaskEnvelope, TaskFacts
from renova_aura_agent_os.orchestrator import AgentOS
from renova_aura_agent_os.providers.base import ProviderRequest, ProviderUnavailable
from renova_aura_agent_os.providers.openai_agents import (
    OpenAIAgentsProvider,
    OpenAIAgentsSettings,
)
from renova_aura_agent_os.tracing import task_fingerprint


class ProviderBoundaryTests(unittest.TestCase):
    def test_openai_adapter_has_no_model_default_and_is_disabled(self) -> None:
        settings = OpenAIAgentsSettings()
        self.assertFalse(settings.enabled)
        self.assertIsNone(settings.model)

    def test_disabled_adapter_fails_before_lazy_import(self) -> None:
        provider = OpenAIAgentsProvider()
        request = ProviderRequest(
            objective="synthetic",
            agent_id="python-engineer",
            step_id="mock-python",
            task_fingerprint=task_fingerprint("synthetic"),
            required_criteria=("synthetic criterion",),
        )
        with patch(
            "renova_aura_agent_os.providers.openai_agents.import_module"
        ) as import_module:
            with self.assertRaises(ProviderUnavailable):
                asyncio.run(provider.run(request))
        import_module.assert_not_called()

    def test_enabled_adapter_requires_all_gates(self) -> None:
        with self.assertRaises(ValidationError):
            OpenAIAgentsSettings(enabled=True)
        with self.assertRaises(ValidationError):
            RuntimePolicy(external_provider_allowed=True)

    def test_approval_reference_must_match_before_import(self) -> None:
        provider = OpenAIAgentsProvider(
            OpenAIAgentsSettings(
                enabled=True,
                api_key="synthetic-key-not-valid",
                model="synthetic-model",
                human_approval_reference="approval-a",
            )
        )
        request = ProviderRequest(
            objective="synthetic",
            agent_id="python-engineer",
            step_id="mock-python",
            task_fingerprint=task_fingerprint("synthetic"),
            required_criteria=("synthetic criterion",),
            external_calls_allowed=True,
            human_approval_reference="approval-b",
        )
        with patch(
            "renova_aura_agent_os.providers.openai_agents.import_module"
        ) as import_module:
            with self.assertRaises(ProviderUnavailable):
                asyncio.run(provider.run(request))
        import_module.assert_not_called()

    def test_authorized_openai_adapter_is_proposal_only_and_fails_closed(self) -> None:
        captured: dict[str, object] = {}

        class FakeAgent:
            def __init__(self, *, name, instructions, model) -> None:
                captured["name"] = name
                captured["instructions"] = instructions
                captured["model"] = model

        class FakeRunner:
            @staticmethod
            async def run(agent, provider_input, **kwargs):
                captured["input"] = provider_input
                captured["max_turns"] = kwargs["max_turns"]
                return SimpleNamespace(final_output="Synthetic proposal only.")

        fake_agents = SimpleNamespace(
            OpenAIResponsesModel=lambda **kwargs: kwargs,
            Agent=FakeAgent,
            Runner=FakeRunner,
            RunConfig=lambda **kwargs: kwargs,
        )
        fake_openai = SimpleNamespace(AsyncOpenAI=lambda **kwargs: kwargs)

        def fake_import(name: str):
            return fake_agents if name == "agents" else fake_openai

        provider = OpenAIAgentsProvider(
            OpenAIAgentsSettings(
                enabled=True,
                api_key="synthetic-key-not-valid",
                model="synthetic-model",
                human_approval_reference="synthetic-approval",
            )
        )
        task = TaskEnvelope(
            objective="Use OpenAI para propor um exemplo Python sintético.",
            facts=TaskFacts(detected_stacks=("Python",)),
            policy=RuntimePolicy(
                external_provider_allowed=True,
                human_approval_reference="synthetic-approval",
            ),
        )
        with patch(
            "renova_aura_agent_os.providers.openai_agents.import_module",
            side_effect=fake_import,
        ):
            result = asyncio.run(AgentOS(provider=provider).run(task))

        payload = json.loads(str(captured["input"]))
        self.assertEqual(task.objective, payload["objective"])
        self.assertTrue(payload["required_criteria"])
        self.assertEqual([], payload["revision_notes"])
        self.assertIn("proposal", str(captured["instructions"]).casefold())
        self.assertEqual(StopReason.MISSING_EVIDENCE, result.loop.stop_reason)
        self.assertEqual(1, result.loop.provider_calls)

    def test_default_runtime_uses_no_network_or_process(self) -> None:
        task = TaskEnvelope(
            objective="Crie um artefato Python mock.",
            facts=TaskFacts(detected_stacks=("Python",)),
        )
        loop = asyncio.new_event_loop()
        try:
            with (
                patch.object(
                    socket,
                    "create_connection",
                    side_effect=AssertionError("network forbidden"),
                ),
                patch.object(
                    socket,
                    "getaddrinfo",
                    side_effect=AssertionError("network forbidden"),
                ),
                patch.object(subprocess, "run", side_effect=AssertionError("process forbidden")),
                patch.object(subprocess, "Popen", side_effect=AssertionError("process forbidden")),
                patch.object(os, "system", side_effect=AssertionError("shell forbidden")),
            ):
                result = loop.run_until_complete(AgentOS().run(task))
        finally:
            loop.close()
        self.assertEqual("PASS", result.loop.stop_reason)


if __name__ == "__main__":
    unittest.main()
