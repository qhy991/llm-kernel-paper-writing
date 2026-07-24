from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_evidence_ledger.py"


class EvidenceLedgerTests(unittest.TestCase):
    def run_validator(self, ledger: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(ledger), "--strict"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_filled_example_passes_strict_validation(self) -> None:
        result = self.run_validator(ROOT / "assets" / "example-solar-ledger.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        summary = json.loads(result.stdout.splitlines()[-1])
        self.assertEqual(summary, {"errors": 0, "warnings": 0, "strict": True})

    def test_blank_template_is_rejected(self) -> None:
        result = self.run_validator(ROOT / "assets" / "evidence-ledger.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("paper_contract.paper_type: must be filled", result.stdout)
        summary = json.loads(result.stdout.splitlines()[-1])
        self.assertGreater(summary["errors"], 0)


if __name__ == "__main__":
    unittest.main()
