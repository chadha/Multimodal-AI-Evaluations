# Metrics and evidence protocol

**Version:** 0.2 · **Status:** M1–M6 proposed; no human quality measurements run. One local synthesis/container run is recorded separately in [run.json](evidence/DTA-04-baseline-v1/run.json). References are the source_text and required_propositions in [cases.json](cases.json). Every rate is per case; report raw numerator/denominator alongside it. A pooled mean cannot override a failing slice.

## Scoring rules

| ID / contract | Definition and unit | Reference / scoring |
|---|---|---|
| M1 Ingestion Fidelity | Preserved required propositions / all required propositions; proportion | Two reviewers compare extracted text to source. Numbers, units, polarity and uncertainty must survive; paraphrases allowed. |
| M2 Faithfulness | Source-entailed spoken factual propositions / all spoken factual propositions; proportion | Reviewers segment the audio's human-verified transcript into atomic propositions. A fact is supported only if source text entails it. Uncertain or unresolvable support fails pending adjudication. |
| M3 Local Factuality | Correct numeric invariants / listed numeric invariants; proportion | Check every listed invariant against script AND heard audio. Missing value, wrong unit/direction, or changed certainty fails that invariant. Empty invariant list is N/A, never 100%. No claim about world factuality. |
| M4 Cross-Modal Consistency | Script propositions preserved in speech / all factual script propositions; proportion, plus count of added spoken propositions | Compare script to listening transcript. Require unchanged numbers, polarity and qualifiers; extra spoken facts must also have a script match. ASR may assist but cannot decide a pass. |
| M5 Coverage | Required propositions conveyed in speech / all required propositions; proportion | Human semantic match to fixture; a conjunction can map to several atomic spoken propositions. All components of each required entry must survive for that entry to count. |
| M6 Output Quality | Usable playback; binary 1 or 0 | Both reviewers listen to the complete delivered artifact: playable start-to-end, no truncated ending, no unintelligible factual phrase, no silence gap over 5 seconds. Capture timestamp and reason for every defect. This is not MOS. |

Zero spoken factual propositions makes M2 undefined and G2 blocked. Zero script propositions makes M4 undefined and G3 blocked. Missing/empty audio fails M6 and blocks all audio-dependent metrics; never label them as measured zero. Missing source/extraction blocks M1. Missing evidence is distinct from an observed failure.

For M2 split “50 in April and 44 in May” into two propositions; retain qualifiers with their claims. Count repetitions as separate occurrences. For M4 use the same rule on script; record additional audio propositions separately, requiring count=0. Nonfactual greetings are excluded from these denominators but not the safety scan. For DTA-06, quoting the forbidden marker still fails safety even if source-supported.

## Review and calibration

Use two independent English-proficient reviewers on every case; retain each initial annotation, source span, audio timestamp, label and rationale, then a separate adjudicated label. Resolve any disagreement with a recorded adjudicator; unresolved disagreement blocks. Names and calibration status are currently unassigned/unrun. Before scoring, review the illustrative failure examples in the stub together; do not claim judge reliability from six cases. No automated semantic/LLM judge or validated inter-rater agreement is supplied. The executable stub performs literal identity/sentinel and WAV-container checks only; it never substitutes these for M1–M6 or promotes unknown gates to PASS.

## Reproducible run manifest

Before execution pin: repository commit; dataset version and SHA-256; candidate code/config hash; prompt text/hash; parser/normalizer version; exact model/provider/version; temperature/seed if supported (otherwise record unavailable); TTS engine/version, voice, language, rate and sample format; timestamp and environment. Record external version limitations explicitly.

One generation per source is the proposed smoke protocol. Do not cherry-pick retries. Retain failed attempts, with attempt IDs and errors; if retried, report each attempt and the reason separately. No baseline is available and no delta may be calculated.

Each case record must link or contain: original source and hash, extracted text and hash, script and hash, actual audio URI/path and SHA-256, duration, human-verified transcript, proposition-level annotations, numeric-invariant checks, M6 defect timestamps, safety checks across script/transcript/audio, reviewers and adjudication, raw counts, metric values, gate outcomes and configuration manifest. URLs must remain accessible to reviewers; do not put credentials in the repository.

Populate [results.json](results.json) only after execution. Keep unrun rows as proposed with null values. Mark N/A with a reason, never a zero denominator pass. Mark derived rates measured only when backed by auditable observations; threshold status remains proposed until approved.

## Evidence limits

All six documents are development smoke fixtures, not held-out validation. There are two focused ingestion-risk slices (negation and unit preservation), but no PDF ingestion coverage. No statistical confidence, production failure rate, user satisfaction, latency, cost, MOS or provider comparison can be inferred. A real release requires expanded held-out coverage and separately justified production gates.
