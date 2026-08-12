import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "project-packs" / "MANIFEST.json"

EXPECTED_SKILLS = [
    "renova-aura-requirements-completeness-auditor",
    "renova-aura-data-contract-field-auditor",
    "renova-aura-workflow-integration-auditor",
    "renova-aura-domain-invariant-guardian",
    "renova-aura-android-kotlin-engineering",
    "renova-aura-whatsapp-automation-reliability",
    "renova-aura-voice-ai-evaluation",
    "renova-aura-accessibility-mobile-qa",
]

EXPECTED_ADAPTERS = [
    "requirements-completeness-analyst",
    "data-contract-integration-reviewer",
    "android-kotlin-engineer",
    "messaging-reliability-engineer",
]


class ManifestContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with MANIFEST_PATH.open(encoding="utf-8") as handle:
            cls.manifest = json.load(handle)

    def test_versions_and_current_contract_fields(self):
        self.assertEqual(self.manifest["version"], "1.1.0-draft")
        self.assertEqual(self.manifest["schema_version"], "1.1.0")
        self.assertEqual(self.manifest["profile"], "ProjectPacks")
        self.assertIsInstance(self.manifest["counts"], dict)
        self.assertIsInstance(self.manifest["skills"], list)
        self.assertIsInstance(self.manifest["project_adapters"], list)

        self.assertNotIn("agents", self.manifest)
        self.assertNotIn("new_skills", self.manifest["counts"])
        self.assertNotIn("new_agents", self.manifest["counts"])

    def test_counts_are_reconciled(self):
        counts = self.manifest["counts"]
        self.assertEqual(counts["base_skills"], 25)
        self.assertEqual(counts["extension_skills"], 8)
        self.assertEqual(counts["combined_skills"], 33)
        self.assertEqual(counts["canonical_agents"], 18)
        self.assertEqual(counts["project_adapters"], 4)
        self.assertEqual(
            counts["base_skills"] + counts["extension_skills"],
            counts["combined_skills"],
        )

    def test_extension_skills_are_exact_unique_and_present(self):
        skills = self.manifest["skills"]
        self.assertEqual(skills, EXPECTED_SKILLS)
        self.assertEqual(len(skills), 8)
        self.assertEqual(len(set(skills)), len(skills))

        for skill_id in skills:
            skill_root = REPO_ROOT / "skills" / skill_id
            self.assertTrue(skill_root.is_dir(), skill_id)
            self.assertTrue((skill_root / "SKILL.md").is_file(), skill_id)
            self.assertTrue((skill_root / "agents" / "openai.yaml").is_file(), skill_id)

    def test_project_adapters_are_exact_unique_and_present(self):
        adapters = self.manifest["project_adapters"]
        self.assertEqual(adapters, EXPECTED_ADAPTERS)
        self.assertEqual(len(adapters), 4)
        self.assertEqual(len(set(adapters)), len(adapters))

        adapters_root = REPO_ROOT / "project-packs" / "agents"
        for adapter_id in adapters:
            self.assertTrue((adapters_root / f"{adapter_id}.yaml").is_file(), adapter_id)


if __name__ == "__main__":
    unittest.main()
