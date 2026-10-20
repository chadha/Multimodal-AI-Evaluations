# Document-to-audio: one auditable claim

**Version:** 0.1 · **Date:** 2026-10-20 · **Evidence status:** proposed; product evaluation not run.

A small, synthetic example of DECODE from product intent to a launch decision. It contains authored source documents, reference propositions, a review protocol, and an empty evidence ledger. No product, parser, model, TTS service, or listener panel has been evaluated. Reference text is test design, never generated output.

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
| [Evidence ledger](results.json) | Which measurements actually exist? Currently none. |
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

Use the root README's nine-stage naming. Stage 1 Ingestion loads text; Stage 2 Normalization preserves source IDs and propositions; Stage 3 Indexing and Stage 4 Retrieval are bypassed (one full document); Stage 5 Reasoning selects propositions; Stage 6 Generation writes the script; Stage 7 Synthesis renders speech; Stage 8 Guardrails checks output; Stage 9 Delivery exposes playable audio and its audit record. This is a proposed logical path, not an implemented platform.

## Run the smallest real evaluation

1. Freeze this package's commit SHA and all configuration listed in metrics.md. Assign actual reviewers and approve gates before execution.
2. Process every source_text in cases.json once through the candidate. Save extracted text, script, audio, timing, and configuration; do not substitute reference propositions for candidate output.
3. Two independent reviewers score all six traces using metrics.md, including listening to the actual audio. Adjudicate disagreements and retain original labels.
4. Populate results.json with measured counts, artifact hashes, timestamps and reviewer records. Evaluate each gate per case and slice; missing evidence stays blocked.
5. Update the memo from the resulting evidence. Six synthetic cases support a smoke-test decision only; production launch requires representative held-out documents, calibrated evaluators and operational validation.

**Limits:** no PDF/OCR/layout, images, multilingual speech, multiple sources, streaming, production scale, engagement, cost or latency claims. This fixture cannot establish factual correctness about the real world. Passing it is necessary for an internal smoke test, insufficient for GA.

## Attribution

Adapted from Harsha Srivatsa's existing [T-19](../../templates/T-19-eval-stub-template.md), [T-22](../../templates/T-22-decode-translation-worksheet.md), [T-10](../../templates/T-10-gate-thresholds-alert-rule.md), and [T-14](../../templates/T-14-decision-memo.md). Original templates remain unchanged. Thresholds here are proposed local test criteria, not calibrated production recommendations.
