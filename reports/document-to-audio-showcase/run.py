#!/usr/bin/env python3
"""Offline document-to-audio smoke runner. No semantic or listening judge."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import wave
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
METRICS = tuple(f"M{i}" for i in range(1, 7))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_document(text):
    if not text.strip() or len(text.split()) > 500:
        raise ValueError("Supported input is nonempty UTF-8 text up to 500 words")
    return text


def make_script(extracted):
    # Deliberately simple readout baseline, not a summarizer or an LLM.
    # No access to required_propositions, invariants, or reference answers.
    return extracted.strip()


def inspect_wav(path):
    with wave.open(str(path), "rb") as audio:
        frames = audio.getnframes()
        rate = audio.getframerate()
        pcm = audio.readframes(frames)
        if frames <= 0 or len(pcm) != frames * audio.getsampwidth() * audio.getnchannels():
            raise ValueError("Empty or truncated WAV")
        return {"frames": frames, "sample_rate_hz": rate,
                "channels": audio.getnchannels(), "sample_width_bytes": audio.getsampwidth(),
                "duration_seconds": frames / rate,
                "nonzero_pcm": any(pcm)}


def evaluate_stub(case, extracted, script, wav_info):
    """Only mechanical evidence; unknowns block, known sentinel breach fails."""
    matches = [marker for marker in case.get("forbidden_output", []) if marker in script]
    checks = {"extraction_exact_match": extracted == case["source_text"],
              "script_exact_match_after_strip": script == extracted.strip(),
              "wav_structurally_valid": wav_info is not None,
              "literal_sentinel_matches_in_script": matches}
    gates = {f"G{i}": "BLOCKED" for i in range(1, 7)}
    if matches:
        gates["G5"] = "FAIL"
    return {"status": "mechanical_checks_only_human_evaluation_proposed",
            "mechanical_checks": checks,
            "metrics": {name: None for name in METRICS},
            "reviewers": None, "annotations": None,
            "gate_outcomes": gates, "proposed_decision": "HOLD"}


def run(case_id, output):
    dataset = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    case = next((c for c in dataset["cases"] if c["id"] == case_id), None)
    if case is None:
        raise ValueError(f"Unknown case: {case_id}")
    # Refuse overwrite so an earlier attempt's evidence cannot silently change.
    output.mkdir(parents=True, exist_ok=False)
    source = output / "source.txt"
    extracted_path = output / "extracted.txt"
    script_path = output / "script.txt"
    source.write_text(case["source_text"], encoding="utf-8")
    extracted = read_document(source.read_text(encoding="utf-8"))
    extracted_path.write_text(extracted, encoding="utf-8")
    script = make_script(extracted)
    script_path.write_text(script, encoding="utf-8")
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
               "-f", "lavfi", "-i", "flite=textfile=script.txt:voice=slt",
               "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", "audio.wav"]
    # Fixed relative filenames; source text is never interpreted as shell/filter code.
    subprocess.run(command, cwd=output, check=True, capture_output=True, timeout=60)
    info = inspect_wav(output / "audio.wav")
    version = subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True,
                             text=True, timeout=10).stdout.splitlines()[0]
    git_revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                  capture_output=True, text=True, timeout=10)
    record = {"schema_version": "0.2", "run_id": output.name,
              "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "case_id": case_id, "slice": case["slice"], "claim_id": "CL-01",
              "dataset_id": dataset["dataset_id"],
              "candidate": "identity-readout-v1 (no LLM; source text only)",
              "manifest": {"base_git_revision": git_revision.stdout.strip(),
                           "dataset_sha256": sha256(ROOT / "cases.json"),
                           "runner_sha256": sha256(__file__),
                           "python": sys.version, "platform": platform.platform(),
                           "tts": version, "voice": "flite/slt", "command": command,
                           "provider": "local FFmpeg/libflite", "prompt": None,
                           "seed": "not exposed", "temperature": "not applicable",
                           "engine_note": "Linked libflite/voice binary not pinned; audio hashes identify this run."},
              "artifacts": {p.name: {"path": p.name, "sha256": sha256(p)} for p in
                            (source, extracted_path, script_path, output / "audio.wav")},
              "audio_container_observations": info,
              "human_verified_transcript": None,
              "evaluation": evaluate_stub(case, extracted, script, info)}
    (output / "run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default="DTA-04")
    parser.add_argument("--out", type=Path, help="New evidence directory; must not exist")
    args = parser.parse_args()
    output = args.out or Path(tempfile.mkdtemp(prefix="dta-parent-")) / "run"
    try:
        record = run(args.case, output.resolve())
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"Run failed; retain any partial evidence: {exc}", file=sys.stderr)
        return 1
    print(f"Evidence: {output.resolve() / 'run.json'}")
    print("HOLD: M1–M6 unmeasured; human review and approvals missing.")
    # Success means artifact generation, never launch approval.
    return 0


if __name__ == "__main__":
    sys.exit(main())
