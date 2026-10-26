"""Regression tests for audit honesty and fail-closed behavior, not product scores."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import wave

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("dta_run", ROOT / "run.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((ROOT / "cases.json").read_text())["cases"]

    def test_all_slices_preserve_source_without_reference_leakage(self):
        self.assertEqual(len({c["slice"] for c in self.cases}), 6)
        for case in self.cases:
            with self.subTest(case=case["id"]):
                extracted = runner.read_document(case["source_text"])
                self.assertEqual(extracted, case["source_text"])
                self.assertEqual(runner.make_script(extracted), extracted.strip())

    def test_missing_audio_and_reviews_never_produce_a_pass(self):
        for case in self.cases:
            result = runner.evaluate_stub(case, case["source_text"], "", None)
            self.assertTrue(all(v is None for v in result["metrics"].values()))
            self.assertEqual(set(result["gate_outcomes"].values()), {"BLOCKED"})
            self.assertEqual(result["proposed_decision"], "HOLD")

    def test_known_injection_baseline_fails_safety(self):
        case = self.cases[-1]
        result = runner.evaluate_stub(case, case["source_text"],
                                      runner.make_script(case["source_text"]), None)
        self.assertEqual(result["gate_outcomes"]["G5"], "FAIL")
        self.assertEqual(result["mechanical_checks"]["literal_sentinel_matches_in_script"],
                         case["forbidden_output"])

    def test_numeric_and_negation_mutations_are_not_certified(self):
        for index, old, new in [(2, "disabled", "enabled"), (3, "4.5", "45")]:
            case = self.cases[index]
            result = runner.evaluate_stub(case, case["source_text"],
                                          case["source_text"].replace(old, new), None)
            self.assertFalse(result["mechanical_checks"]["script_exact_match_after_strip"])
            self.assertIsNone(result["metrics"]["M2"])
            self.assertEqual(result["gate_outcomes"]["G3"], "BLOCKED")

    def test_empty_or_oversized_document_rejected(self):
        for text in ["", "  ", "word " * 501]:
            with self.assertRaises(ValueError):
                runner.read_document(text)

    def test_container_check_cannot_certify_speech(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "silent.wav"
            with wave.open(str(path), "wb") as audio:
                audio.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
                audio.writeframes(b"\0\0" * 1600)
            info = runner.inspect_wav(path)
            self.assertFalse(info["nonzero_pcm"])
            result = runner.evaluate_stub(self.cases[0], "", "", info)
            self.assertIsNone(result["metrics"]["M6"])
            self.assertEqual(result["gate_outcomes"]["G4"], "BLOCKED")

    def test_committed_evidence_hashes_and_unrun_scores(self):
        evidence = ROOT / "evidence" / "DTA-04-baseline-v1"
        record = json.loads((evidence / "run.json").read_text())
        self.assertEqual(record["manifest"]["runner_sha256"], runner.sha256(ROOT / "run.py"))
        self.assertEqual(record["manifest"]["dataset_sha256"], runner.sha256(ROOT / "cases.json"))
        for artifact in record["artifacts"].values():
            self.assertEqual(artifact["sha256"], runner.sha256(evidence / artifact["path"]))
        self.assertEqual(runner.inspect_wav(evidence / "audio.wav"), record["audio_container_observations"])
        self.assertTrue(all(v is None for v in record["evaluation"]["metrics"].values()))
        self.assertEqual(set(record["evaluation"]["gate_outcomes"].values()), {"BLOCKED"})
        self.assertIsNone(record["human_verified_transcript"])


if __name__ == "__main__":
    unittest.main()
