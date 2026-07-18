from __future__ import annotations

import argparse
import json
import sys
import unittest
import warnings
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tests-dir", type=Path, required=True)
    args = parser.parse_args()
    tests_dir = args.tests_dir.resolve()

    with warnings.catch_warnings(record=True) as captured_warnings:
        warnings.simplefilter("always")
        suite = unittest.defaultTestLoader.discover(str(tests_dir))
        result = unittest.TextTestRunner(verbosity=2).run(suite)

    passed = (
        result.testsRun
        - len(result.failures)
        - len(result.errors)
        - len(result.skipped)
        - len(result.expectedFailures)
        - len(result.unexpectedSuccesses)
    )
    summary = {
        "errors": len(result.errors),
        "expected_failures": len(result.expectedFailures),
        "failures": len(result.failures),
        "passed": passed,
        "skipped": len(result.skipped),
        "tests_run": result.testsRun,
        "unexpected_successes": len(result.unexpectedSuccesses),
        "warnings": len(captured_warnings),
    }
    print("RENOVA_AURA_TEST_SUMMARY=" + json.dumps(summary, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
