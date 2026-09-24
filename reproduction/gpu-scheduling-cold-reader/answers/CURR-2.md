## Part A

**Q1.** The truthful gate refuses all 240 transition looks as UNKNOWN before inference.

**Q2.** At the 100k look, falsely declaring the transition data stationary produced 80/80 wrong-side decisions (all 80 drift records wrong for both false-declaration methods).

**Q3.** "Tail truth" describes the eventual, post-regime-change stationary classification (overloaded/subcritical) that persists forever after the finite change, as labeled by the exact two-class capacity theorem. It is explicitly not the queue state within the observed (finite) window — the note states "Eventual-tail stability is not finite-window queue state."

**Q4.** No. The note states: "The declaration gate cannot detect a lying or missing manifest from data."

**Q5.** At the 320k look, the service_improve scenario still fails under the false declaration: the scheduled method outputs 20/20 wrong, and the anytime method outputs 20/20 UNKNOWN.

**Q6.** No. "The same common seeds are used across cells, so cell results are dependent, not 120 independent seeds."

**Q7.** The correct "Tail truth" label comes from the existing exact two-class capacity result (Grosof et al.), which labels the stationary regime that persists forever after the finite change.

**Q8.** (a) No — explicitly denied ("no ... new time-varying stability theorem"). (b) No — not claimed; the note explicitly lists "nonexponential/real-GPU transfer" among what it does not show. (c) No — explicitly denied ("established novelty" listed under what the research does not show). (d) No — "External independent replications: zero."

**Q9.** The reproduction command regenerates 72 looks (2 seeds × 2 models × 6 scenarios × 3 looks); it also recomputes 360 recorded looks.

## Part B

Command run (from `reproduction/gpu-scheduling-transition-refusal` inside the cloned repo):
```
python runner_transition.py --verify-recorded --seeds 2
```

Final output line (verbatim):
```
transition-refusal: PASS; 360 recorded looks and 72 regenerated looks; not independent replication
```

(numpy 2.4.2 and scipy 1.17.1 were already installed, so no install step was needed.)

## Part C — URLs and file paths accessed

- `<SCRATCH>/readers/CURR-2.prompt.md` (read)
- `https://github.com/kbmt327-dev/scientific-os-research` (cloned via git into `.../scratchpad/readers/CURR-2`)
- `<SCRATCH>/readers/CURR-2` (directory listing, top level, to confirm clone)
- `<SCRATCH>/readers/CURR-2/reproduction/gpu-scheduling-transition-refusal` (directory listing, and working directory for running the command)
- `.../reproduction/gpu-scheduling-transition-refusal/runner_transition.py` (executed, not read as text)

No other files in the repository were opened or read.
