from __future__ import annotations

import ast
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "renova_aura_agent_os"


class StaticSafetyTests(unittest.TestCase):
    def test_pyproject_keeps_openai_optional(self) -> None:
        with (ROOT / "pyproject.toml").open("rb") as stream:
            project = tomllib.load(stream)["project"]
        self.assertEqual(["pydantic>=2.12.2,<3"], project["dependencies"])
        self.assertEqual(
            ["openai-agents==0.18.2"],
            project["optional-dependencies"]["openai"],
        )

    def test_runtime_has_no_network_shell_git_or_database_imports(self) -> None:
        forbidden_roots = {
            "socket",
            "subprocess",
            "requests",
            "httpx",
            "urllib",
            "git",
            "gitpython",
            "sqlalchemy",
            "psycopg",
        }
        violations: list[str] = []
        for path in SOURCE.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots = {alias.name.split(".", 1)[0].casefold() for alias in node.names}
                elif isinstance(node, ast.ImportFrom) and node.module:
                    roots = {node.module.split(".", 1)[0].casefold()}
                else:
                    continue
                if roots & forbidden_roots:
                    violations.append(f"{path.name}:{node.lineno}:{sorted(roots)}")
        self.assertEqual([], violations)

    def test_public_reference_contains_no_private_absolute_path(self) -> None:
        violations: list[str] = []
        private_windows_prefix = "C:" + "\\Users\\"
        private_profile_prefix = "C:" + "/Users/"
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in {".py", ".md", ".toml"}:
                continue
            text = path.read_text(encoding="utf-8")
            if private_windows_prefix in text or private_profile_prefix in text:
                violations.append(str(path.relative_to(ROOT)))
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
