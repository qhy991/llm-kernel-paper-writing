from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACTOR = ROOT / "scripts" / "extract_arxiv_evidence.py"
FIXTURE = ROOT / "tests" / "fixtures" / "minimal_arxiv.html"


class ExtractArxivEvidenceTests(unittest.TestCase):
    def test_local_html_extraction_is_network_free_and_source_located(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "evidence"
            result = subprocess.run(
                [
                    sys.executable,
                    str(EXTRACTOR),
                    "--id",
                    "2606.26383v1",
                    "--html-file",
                    str(FIXTURE),
                    "--source-url",
                    "https://arxiv.org/html/2606.26383v1",
                    "--output-dir",
                    str(output),
                    "--download-images",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            evidence_path = (
                output / "papers" / "2606.26383v1" / "evidence.json"
            )
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            self.assertEqual(evidence["arxiv_id"], "2606.26383")
            self.assertEqual(evidence["requested_ref"], "2606.26383v1")
            self.assertEqual(evidence["provider"], "local-html")
            self.assertEqual(evidence["paper_type_hint"], "agent-or-search")
            self.assertEqual(len(evidence["figures"]), 1)
            self.assertEqual(
                evidence["figures"][0]["assets"][0]["status"], "extracted"
            )
            self.assertTrue(evidence["claim_candidates"])
            self.assertTrue(evidence["rhetorical_cues"])

            summary = json.loads(
                (output / "summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(summary["statuses"], {"ok": 1})
            self.assertEqual(summary["figure_count"], 1)


if __name__ == "__main__":
    unittest.main()
