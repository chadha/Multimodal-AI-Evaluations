# Document-to-audio: one auditable claim

**Version:** 0.2 · **Date:** 2026-10-26 · **Evidence status:** one local audio generation run; semantic and listening evaluation proposed, not run.

A small, synthetic example of DECODE from product intent to a launch decision. It contains authored source documents, reference propositions, an executable offline baseline, a recorded DTA-04 audio generation run, and a review protocol. The baseline reads the document aloud unchanged using local FFmpeg/libflite; no LLM or API key is needed. It does not read reference propositions. Human quality scores remain null. Reference text is test design, never candidate output.

## Product claim — CL-01

> For each supported English text document, every factual proposition spoken in the audio briefing is entailed by that document.

This is one binary claim per output: any unsupported spoken proposition fails CL-01. Omitting everything must not yield a vacuous pass: minimum coverage and usable audio are separate launch prerequisites.

**Assumptions:** an internal listener wants a short briefing; input is UTF-8 plain text up to 500 words; output is a single English narrator with an audit transcript. All six sources are fictional and authored for this example. No customer data or observed failures are represented.

## Follow the evidence

| Artifact | Review question |
|---|---|
| [Eval stub](eval-stub.md) | What exactly is promised, and where can it break? |
| [Six source cases](cases.json) | Which source propositions and edge conditions are covered? |
| [Metrics and run protocol](metrics.md) | How will each judgment be made and reproduced? |
| [Launch gates](launch-gates.md) | What blocks a release, including missing evidence? |
| [Recorded run](evidence/DTA-04-baseline-v1/run.json) and [audio](evidence/DTA-04-baseline-v1/audio.wav) | What was actually generated, with which configuration and hashes? |
| [Evidence ledger](results.json) | Which human quality measurements exist? None yet; all remain proposed. |
| [T-14 decision memo](decision-memo.md) | What decision does the available evidence support? |

Example audit path: CL-01 → DTA-03 (negation) → reference “automatic renewal is disabled” → compare extracted text, script, and timestamped listening transcript → M2/M3 → G2/G3 → Hold until evidence exists. Saying “renewal is automatic” would fail; this is a hypothetical failure, not an observation.

## DECODE in miniature

| Step | Concrete output |
|---|---|
| Decompose | CL-01; coverage and audio usability kept as separate guardrails |
| Enumerate | Text document → extracted text → script → audio + audit transcript; six slices in cases.json |
| Classify | Five contracts, safety overlay, three prioritized failure modes in the stub |
| Operationalize | M1–M6 with explicit units, denominators, references, and reviewers |
| Define | Proposed G1–G6 gates with fail-closed missing-data behavior |
| Express | This linked package and the proposed Hold memo |

## Pipeline boundary

Use the root README's nine-stage naming. Stage 1 Ingestion loads text; Stage 2 Normalization preserves source IDs and propositions; Stage 3 Indexing and Stage 4 Retrieval are bypassed (one full document); Stage 5 Reasoning selects propositions; Stage 6 Generation writes the script; Stage 7 Synthesis renders speech; Stage 8 Guardrails checks output; Stage 9 Delivery exposes playable audio and its audit record. The runner implements a minimal source read → identity script → local speech → artifact logging path. Stages 3–4 are bypassed; stage 5 selects the full document. Stage 8 only checks containers and literal script sentinels, so it cannot approve delivery. Stage 9 writes local artifacts for review; no product delivery platform is implemented.

## Reproduce the vertical slice

Requires Python 3.10+ and FFmpeg with the `flite` filter and `slt` voice. Python uses only its standard library. Check availability with `ffmpeg -filters`; FFmpeg builds differ.

From the repository root:

```bash
python -m unittest discover -s reports/document-to-audio-showcase -p 'test_*.py' -v
python reports/document-to-audio-showcase/run.py --case DTA-04 --out /tmp/dta-review-01
```

Use a new output directory for each attempt; overwrites are rejected. A successful command means artifact generation succeeded, never that launch gates passed. On failure, retain the partial directory and error; do not omit failed attempts from an evaluation. No source text is executed as code or sent to an external provider.

The recorded [DTA-04 run](evidence/DTA-04-baseline-v1/run.json) includes the [source](evidence/DTA-04-baseline-v1/source.txt), [extraction](evidence/DTA-04-baseline-v1/extracted.txt), [script](evidence/DTA-04-baseline-v1/script.txt), and [generated WAV](evidence/DTA-04-baseline-v1/audio.wav). Its manifest records the runner/dataset/artifact SHA-256 hashes, base revision, engine configuration, environment and time. WAV structure, duration and nonzero PCM are actual observations, **not** evidence of intelligibility, pronunciation or entailment. The linked Flite voice binary is not pinned; byte-identical regeneration on another machine is not promised.

Seven regression tests cover six fixture slices, missing evidence, altered negation/decimals, an exact sentinel breach, unsupported input, a silent WAV, and the recorded artifact hashes. These are engineering checks, not seven product evaluations. The identity baseline deliberately echoes DTA-06's malicious attachment: its literal sentinel makes G5 FAIL in that regression test. Other gates stay BLOCKED; a clean sentinel scan cannot produce a safety PASS. No DTA-06 audio run is claimed.

## Complete the human evaluation

1. Freeze this package's commit SHA and all configuration listed in metrics.md. Assign actual reviewers and approve gates before execution.
2. Process every source_text in cases.json once through the candidate. Save extracted text, script, audio, timing, and configuration; do not substitute reference propositions for candidate output.
3. Two independent reviewers score all six traces using metrics.md, including listening to the actual audio. Adjudicate disagreements and retain original labels.
4. Populate results.json with measured counts, artifact hashes, timestamps and reviewer records. Evaluate each gate per case and slice; missing evidence stays blocked.
5. Update the memo from the resulting evidence. Six synthetic cases support a smoke-test decision only; production launch requires representative held-out documents, calibrated evaluators and operational validation.

**Limits:** no PDF/OCR/layout, images, multilingual speech, multiple sources, streaming, production scale, engagement, cost or latency claims. This fixture cannot establish factual correctness about the real world. Passing it is necessary for an internal smoke test, insufficient for GA.

## Attribution

Framework and original templates by Harsha Srivatsa; this fork adds the showcase implementation. Adapted from the existing [T-19](../../templates/T-19-eval-stub-template.md), [T-22](../../templates/T-22-decode-translation-worksheet.md), [T-10](../../templates/T-10-gate-thresholds-alert-rule.md), and [T-14](../../templates/T-14-decision-memo.md). Original templates remain unchanged. Thresholds here are proposed local test criteria, not calibrated production recommendations.
