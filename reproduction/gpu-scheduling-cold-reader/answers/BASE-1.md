## Part A

**Q1.** The truthful gate refused all 240 transition looks, labeling them UNKNOWN before any inference was made.

**Q2.** At the first 100k look, falsely declaring the transition data stationary produced 80/80 wrong-side decisions (all 80 drift records were wrong, across both false-declaration methods).

**Q3.** "Tail truth" labels the eventual, persistent post-change regime (overloaded or subcritical) that holds forever after the finite change, derived from exact two-class capacity. It is explicitly *not* the queue state within the observed window — the note states "Eventual-tail stability is not finite-window queue state."

**Q4.** No. The note states "The declaration gate cannot detect a lying or missing manifest from data," and lists "No data-driven detection of undeclared drift" among what the research does not show.

**Q5.** At 320k, the service_improve scenario still fails under the false declaration: the scheduled method is wrong 20/20, while the anytime method instead outputs UNKNOWN 20/20 (not correct, just non-committal).

**Q6.** Not stated as independent replications. The note describes 120 workloads built from "two parent models and seeds 9301–9310" (10 seeds), i.e. shared/reused seed sets across models and scenarios, but it never characterizes the 120 workloads as independent replications.

**Q7.** From "existing exact two-class capacity," which labels the stationary regime that persists forever after the finite change — an analytic/existing classification, not something derived from the observed data itself (the note separately lists "post-regime exact labels ... were recomputed").

**Q8.** (a) New time-varying stability theorem — No, explicitly listed under "What this research does not show." (b) Validity on real GPU clusters — No, "nonexponential/real-GPU transfer" is explicitly listed as not shown. (c) Established novelty — No, explicitly listed as not shown. (d) Independent external replication — No, "External independent replications: zero."

**Q9.** The reproduction command regenerates 24 small looks (while recomputing 360 recorded looks).

## Part B

Skipped per instructions.

## Part C

- <SCRATCH>/readers/BASE-1.prompt.md

No other files or URLs were accessed (no tool use occurred during Part A, and no tools were used afterward beyond this initial read).
