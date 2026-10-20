# T-14 decision memo — document-to-audio

Adapted from [T-14](../../templates/T-14-decision-memo.md). **Version:** 0.1 · **Date:** 2026-10-20  
**Author:** AI-assisted showcase draft; no stakeholder approval implied.  
**Feature:** CL-01, source-grounded audio briefing · **Candidate:** not selected.

## Decision

**Proposed HOLD.** Reversibility: easy (no rollout). This is an illustrative evidence-based recommendation, not an executed product decision. All gates are BLOCKED by absent evidence; no measured failure is asserted.

## Evidence summary — contracts

| Contract | Current score | Baseline / delta | Evidence status |
|---|---|---|---|
| Ingestion Fidelity | Not measured | Unavailable | Proposed M1 |
| Faithfulness | Not measured | Unavailable | Proposed M2/M5 |
| Factuality | Not measured | Unavailable | Proposed M3; local numeric scope only |
| Cross-Modal Consistency | Not measured | Unavailable | Proposed M4 |
| Output Quality | Not measured | Unavailable | Proposed M6; MOS not collected |

[results.json](results.json) contains null observations for all six cases. The sources and reference propositions are authored fixtures, not evaluated outputs.

## Consumption signals

Listen-through, visual export rate and 7-day return: not measured; no users/cohorts. Visual export is out of scope. No conflict between automated metrics and behavior can be assessed because neither exists. After a pilot, any such conflict requires Hold and manual review; the inherited T-14 protocol calls for 20 recent traces, not an invented six-case behavior study.

## Zero-tolerance events

**Unknown / not tested**, not “none detected.” Proposed events and immediate reversal actions are defined in [launch-gates.md](launch-gates.md). DTA-06 is synthetic and cannot establish real PII protection.

## Options considered

| Option | Benefit | Risk |
|---|---|---|
| A — Ship now | Fast exposure | Unsupported claim and no audio evidence; reject |
| B — Hold, run six cases | Smallest auditable next step | Synthetic suite cannot justify GA; recommend |
| C — Build platform integrations first | Larger tooling surface | Delays basic evidence without resolving the claim |

## Recommendation and accepted risks

Choose B: assign reviewers, approve the proposed gates, freeze a candidate and execute the protocol. Keep production disabled. No user-facing quality risk is accepted by this unsigned draft. Accepted limitation for documentation use: tiny fictional text-only corpus; audio, visual/PDF ingestion and operational performance remain unvalidated.

## Reversal conditions (precommitted proposal)

| Trigger | Action | Window |
|---|---|---|
| During any later pilot, any zero-tolerance event | Immediate rollback / stop delivery | Immediately; proposed containment target 15 minutes, untested |
| Any other gate breach, missing trace, unresolved reviewer dispute or configuration change | Pause delivery; regenerate evidence against pinned version | Before next delivery |
| To reconsider current Hold | Complete G1–G6 with reviewable evidence and signatures | Before any internal pilot; GA requires expanded release evidence |

Reversal owner: Engineering Lead, unassigned. No rollback mechanism is currently deployed or tested.

## Sign-off

The inherited template requires six signatures before execution; none is supplied. Visual Judge must explicitly acknowledge the absence of visual output rather than silently disappear from approval.

| Role | Name | Signature / date |
|---|---|---|
| Content Judge | Unassigned | Pending |
| Ingestion Judge | Unassigned | Pending |
| Audio Judge | Unassigned | Pending |
| Visual Judge | Unassigned | Pending scope acknowledgement |
| Product Lead | Unassigned | Pending |
| Engineering Lead | Unassigned | Pending |

## Decision history

| Date | Version | Recommendation | Evidence | Execution |
|---|---|---|---|---|
| 2026-10-20 | 0.1 | Proposed Hold | Authored fixtures and protocol; no run | None |
