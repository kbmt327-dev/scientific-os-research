<!-- Harness note: the reader's final report said "Part A answers (given above)" without including them. Part A below was obtained by one follow-up message asking for the original answers verbatim, without tools and without revision. Verbatim fidelity cannot be verified. Part B/C are from the first final report. -->

## Part A (recovered via follow-up)

Q1. The truthful gate refused all 240 transition looks as UNKNOWN before inference (i.e., it did not attempt a stationary-diagnostic decision on any of them).

Q2. All 80 drift records at the 100k look were wrong (80/80 wrong-side decisions) when the same transition data was falsely declared stationary.

Q3. 'Tail truth' describes the eventual, permanent post-change stationary regime (overloaded or subcritical) that persists forever after the finite change, per the exact two-class capacity result. The note explicitly states this is not the finite-window queue state observed within the window ("Eventual-tail stability is not finite-window queue state and cannot be transferred to another time-varying definition").

Q4. No. The note states "The declaration gate cannot detect a lying or missing manifest from data."

Q5. At the 320k look, the service_improve scenario still fails under the false declaration: the "scheduled" method is wrong 20/20, while the "anytime" method outputs UNKNOWN 20/20 (not correct, not wrong-labeled but unresolved).

Q6. No. The note states the 120 workloads use the same common seeds across cells, so "cell results are dependent, not 120 independent seeds."

Q7. From the existing exact two-class capacity result (Grosof et al., cited with a link), which labels the stationary regime that persists forever after the finite change.

Q8. (a) New time-varying stability theorem — not claimed (listed under "What this research does not show"). (b) Validity on real GPU clusters — not claimed (note lists "nonexponential/real-GPU transfer" as not shown). (c) Established novelty — not claimed (explicitly listed as not shown). (d) Independent external replication — not claimed; the note states "External independent replications: zero," and that CI repeats the same design rather than being an independent study.

Q9. The reproduction command regenerates 72 looks (2 seeds x 2 models x 6 scenarios x 3 looks), while separately recomputing 360 recorded looks.

## Part B (first final report)

Execution was blocked by the auto-mode classifier ("Code from External") — running freshly-cloned, untrusted code from this repository was denied. I will not attempt to work around this. Stopping Part B here.

- Command I attempted to run: `python runner_transition.py --verify-recorded --seeds 2` (from `reproduction/gpu-scheduling-transition-refusal/` inside the cloned repo)
- Result: The clone succeeded and numpy/scipy were already installed, but the execution of `runner_transition.py` was **blocked by Claude Code's auto-mode classifier** with reason "Code from External" — it declined to run freshly-cloned, untrusted external code. No output line was produced because the command never ran. This is a safety measure I did not attempt to bypass.

## Part C (first final report)

- `<SCRATCH>/readers/CURR-1.prompt.md` (the task file, read first, per instructions)
- `https://github.com/kbmt327-dev/scientific-os-research` (cloned via git)
- `<SCRATCH>/readers/CURR-1/` (clone target directory — listed top-level contents only)
- `<SCRATCH>/readers/CURR-1/reproduction/gpu-scheduling-transition-refusal/` (directory listing only, to locate the runner script — attempted `python runner_transition.py --verify-recorded --seeds 2` here, which was blocked before executing)

No other repository files were opened or read, and no other local or external files/URLs were accessed.
