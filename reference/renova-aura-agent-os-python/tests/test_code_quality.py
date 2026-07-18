from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON_FILES = tuple(sorted((ROOT / "src").rglob("*.py"))) + tuple(
    sorted((ROOT / "tests").glob("test_*.py"))
)


class CodeQualityTests(unittest.TestCase):
    def test_python_lines_fit_the_declared_limit(self) -> None:
        violations: list[str] = []
        for path in PYTHON_FILES:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if len(line) > 100:
                    violations.append(f"{path.relative_to(ROOT)}:{number}:{len(line)}")
        self.assertEqual([], violations)

    def test_python_files_have_no_trailing_whitespace_or_tabs(self) -> None:
        violations: list[str] = []
        for path in PYTHON_FILES:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if line != line.rstrip() or "\t" in line:
                    violations.append(f"{path.relative_to(ROOT)}:{number}")
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
