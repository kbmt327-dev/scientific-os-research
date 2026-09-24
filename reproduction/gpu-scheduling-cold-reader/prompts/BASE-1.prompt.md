You are reviewing a public research note written by someone else. You have no other context about the project.

PART A. Answer questions Q1-Q9 using ONLY the note text below. Do not use any tools during Part A, and do not guess from outside knowledge; if the note does not say, answer 'not stated'. Keep each answer to 1-3 sentences.

Q1. What does the truthful gate do with the transition looks, and how many are affected?
Q2. What happens at the 100k look when the same transition data is falsely declared stationary?
Q3. What does the 'Tail truth' label describe? Is it the queue state within the observed window?
Q4. Can this gate detect an undeclared parameter change from the data alone?
Q5. At the 320k look, which scenario still fails under the false declaration, for which method, and what does the other method output?
Q6. Are the 120 workloads 120 independent replications? Explain.
Q7. Where does the correct 'Tail truth' label come from?
Q8. Does the note claim any of: (a) a new time-varying stability theorem, (b) validity on real GPU clusters, (c) established novelty, (d) independent external replication? Answer for each.
Q9. According to the note, how many looks does the reproduction command regenerate?

PART B. Skip.

PART C. List every URL and file path you accessed.

Return: Part A answers labelled Q1-Q9, Part B command and output line, Part C list.

=== NOTE ===
# When should a stationary diagnostic refuse a permanent parameter transition?

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-transition-refusal/" hreflang="ja">日本語</a></p>

## Current finding

With a truthful permanent-transition manifest, the stationary diagnostic refused all240 transition looks as UNKNOWN before inference. Falsely declaring the same data stationary produced80/80 wrong-side decisions at the first100k look.

## Key figure

![Wrong-side and UNKNOWN counts under a false stationary declaration](/assets/gpu-scheduling-transition-refusal.svg)

Two models times10seeds. Solid: wrong side; dashed: UNKNOWN; maximum20 per series.

## What this research shows

For a sealed synthetic one-change process with truthful provenance, applicability refusal blocks wrong eventual-tail declarations from a stationary diagnostic.

## What this research does not show

No data-driven detection of undeclared drift, new time-varying stability theorem, general U31, nonexponential/real-GPU transfer, established novelty, peer review or external independent replication.

## Research question

After arrival80000, arrival or service rates change once and remain fixed forever. Reports occur at100k,160k and320k arrivals.

## Why this matters

Cumulative full-history statistics mix pre- and post-change regimes. Narrow stationary intervals can target the wrong long-run side after stationarity has failed.

## Method

64 fungible resources, needs32/64, strict nonpreemptive FCFS, two parent models and seeds9301–9310. Existing exact two-class capacity labels the stationary regime that persists forever after the finite change; equality is excluded. The truthful gate sees a transition manifest. Only the misuse arm receives a false stationary attestation.

## Results

| Scenario | Tail truth | H | False scheduled wrong/UNKNOWN/correct | False anytime wrong/UNKNOWN/correct |
|---|---|---:|---:|---:|
| arrival_up | overloaded | 100k | 20/0/0 | 20/0/0 |
| arrival_up | overloaded | 160k | 20/0/0 | 16/4/0 |
| arrival_up | overloaded | 320k | 0/0/20 | 0/0/20 |
| arrival_down | subcritical | 100k | 20/0/0 | 20/0/0 |
| arrival_down | subcritical | 160k | 0/0/20 | 0/2/18 |
| arrival_down | subcritical | 320k | 0/0/20 | 0/0/20 |
| service_degrade | overloaded | 100k | 20/0/0 | 20/0/0 |
| service_degrade | overloaded | 160k | 20/0/0 | 0/0/20 |
| service_degrade | overloaded | 320k | 0/0/20 | 0/0/20 |
| service_improve | subcritical | 100k | 20/0/0 | 20/0/0 |
| service_improve | subcritical | 160k | 20/0/0 | 20/0/0 |
| service_improve | subcritical | 320k | 20/0/0 | 0/20/0 |

All120 stationary control looks were correct under the truthful gate. All240 transition looks were refused without inference. At100k, all80 drift records were wrong for both false-declaration methods. At320k, only service improvement remained: scheduled20/20 wrong, anytime20/20 UNKNOWN.

## What changed

Draftv0.6 adds model applicability before diagnostic accuracy.

## What failed

The declaration gate cannot detect a lying or missing manifest from data. Under service improvement, cumulative-history contamination remained for the scheduled method at320k.

## Evidence boundary

120 workloads,360 fixed looks,1080 method outcomes and5/5 sealed predictions. Seal/source chronology, post-regime exact labels, gate states and36cell aggregates were recomputed.

## UNKNOWN

Gradual/repeated/adaptive change, changing p, structural change, real-log provenance, external-reader comprehension and demand remain UNKNOWN. General detectors: zero.

## Falsification targets

Refusal depends on truthful provenance. Eventual-tail stability is not finite-window queue state and cannot be transferred to another time-varying definition.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-transition-refusal): `python runner_transition.py --verify-recorded --seeds 2` recomputes360 recorded looks and regenerates24 small looks.

## Evidence / Artifacts

[summary, generator, gate and runner](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-transition-refusal). This is a reviewed projection, not original sealed bytes.

## External audit

External independent replications: zero. Linux CI repeats the same design; it is not an independent study.

## Next experiment

Specify an external-reader test of whether truthful/false declarations and the eventual-tail label can be explained and rerun without author assistance.

[[en/research/gpu-scheduling-exposure-checkpoints/index|EP-0025]] → EP-0026

=== END NOTE ===