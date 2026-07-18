from __future__ import annotations

import unittest

from renova_aura_agent_os.catalog import build_reference_catalog


EXPECTED_IDS = {
    "technical-director-orchestrator",
    "product-requirements-analyst",
    "saas-architect",
    "premium-frontend-specialist",
    "ux-accessibility-specialist",
    "backend-api-engineer",
    "database-data-engineer",
    "appsec-specialist",
    "quality-test-engineer",
    "independent-technical-reviewer",
    "independent-visual-evaluator",
    "performance-engineer",
    "platform-release-engineer",
    "observability-incident-engineer",
    "ai-automation-specialist",
    "python-engineer",
    "documentation-handoff-specialist",
    "skills-agents-prompts-curator",
}


class CatalogTests(unittest.TestCase):
    def test_catalog_has_exactly_the_canonical_18_ids(self) -> None:
        catalog = build_reference_catalog()
        self.assertEqual(18, len(catalog.agents))
        self.assertEqual(EXPECTED_IDS, {agent.id for agent in catalog.agents})

    def test_independent_reviewers_cannot_author(self) -> None:
        catalog = build_reference_catalog()
        for agent_id in (
            "independent-technical-reviewer",
            "independent-visual-evaluator",
        ):
            agent = catalog.get(agent_id)
            self.assertFalse(agent.can_author)
            self.assertTrue(agent.can_evaluate)


if __name__ == "__main__":
    unittest.main()
