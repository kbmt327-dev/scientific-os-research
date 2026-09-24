## Part A

**Q1.** The truthful gate refused all 240 transition looks as UNKNOWN before inference (i.e., it withheld a decision rather than classify them).

**Q2.** At the first 100k look, falsely declaring the same transition data stationary produced 80/80 wrong-side decisions (all drift records wrong for both false-declaration methods).

**Q3.** "Tail truth" is the existing exact two-class capacity label for the stationary regime that persists forever after the finite change (e.g., overloaded/subcritical). No — the note explicitly distinguishes it: "Eventual-tail stability is not finite-window queue state," so it is not the queue state within the observed window.

**Q4.** No. The note states directly: "The declaration gate cannot detect a lying or missing manifest from data."

**Q5.** At 320k, the service_improve scenario still fails under the false declaration, specifically for the scheduled method (20/20 wrong). The other method (anytime) outputs UNKNOWN for all cases (0/20 wrong, 20/20 UNKNOWN, 0/20 correct) rather than a wrong-side decision.

**Q6.** Not stated as such. The note describes 120 workloads as two parent models times 10 seeds (9301–9310) across scenarios, but it does not state or characterize these as "120 independent replications" — that framing/term does not appear in the note.

**Q7.** The correct "Tail truth" label comes from the "existing exact two-class capacity" that labels the stationary regime persisting forever after the finite change (described in the Method section as a pre-existing/external labeling method, not derived from the diagnostic itself).

**Q8.**
- (a) New time-varying stability theorem — denied ("does not show... new time-varying stability theorem").
- (b) Validity on real GPU clusters — denied ("does not show... nonexponential/real-GPU transfer").
- (c) Established novelty — denied ("does not show... established novelty").
- (d) Independent external replication — denied ("External independent replications: zero").

**Q9.** The reproduction command recomputes 360 recorded looks and regenerates 24 small looks.

## Part B
Skipped per instructions.

## Part C
Files/URLs accessed:
- `<SCRATCH>/readers/BASE-3.prompt.md` (the only file read; no other tools, URLs, or files were accessed)
