## Part A

**Q1.** The truthful gate refuses all 240 transition looks, labeling them UNKNOWN before inference (each of the 12 scenario/H rows shows 0 wrong/0 correct under the truthful "Tail truth"/gate framing — the note states "All 240 transition looks were refused without inference").

**Q2.** At the 100k look, falsely declaring the transition data stationary produces 80/80 wrong-side decisions ("At 100k, all 80 drift records were wrong for both false-declaration methods").

**Q3.** "Tail truth" labels the eventual, forever-persisting post-change regime (overloaded or subcritical) from the exact two-class capacity result — not the queue state observed within the finite window. The note explicitly says this label is not finite-window queue state ("Eventual-tail stability is not finite-window queue state").

**Q4.** No. "The declaration gate cannot detect a lying or missing manifest from data" — it relies on a truthful provenance manifest, not data-driven detection.

**Q5.** At 320k, only the service_improve scenario still fails under the false declaration: the scheduled method gives 20/20 wrong, and the anytime method gives 20/20 UNKNOWN (not correct). Every other transition was correct at 320k.

**Q6.** No. The same common seeds (9301–9310, i.e., 10 seeds × 2 models × 6 scenarios = 120 workload cells) are reused across cells, so results are dependent, not 120 independent replications — the note states this directly.

**Q7.** It comes from the existing exact two-class capacity result (Grosof et al.), which labels the stationary regime that persists forever after the finite change (equality excluded) — not from the note's own diagnostic.

**Q8.** (a) New time-varying stability theorem: not claimed — explicitly listed under "does not show." (b) Real GPU clusters: not claimed — "nonexponential/real-GPU transfer" is explicitly listed as not shown. (c) Established novelty: not claimed — explicitly excluded. (d) Independent external replication: not claimed — "External independent replications: zero."

**Q9.** The reproduction command (`python runner_transition.py --verify-recorded --seeds 2`) recomputes 360 recorded looks and regenerates 72 looks (2 seeds × 2 models × 6 scenarios × 3 looks).

## Part B

Command run (from `reproduction/gpu-scheduling-transition-refusal` inside the cloned repo):
```
python runner_transition.py --verify-recorded --seeds 2
```

Final output line (verbatim):
```
transition-refusal: PASS; 360 recorded looks and 72 regenerated looks; not independent replication
```

(numpy and scipy were already installed for this Python interpreter, so no install step was needed.)

## Part C

URLs accessed:
- https://github.com/kbmt327-dev/scientific-os-research (cloned via git)

File paths accessed:
- `<SCRATCH>/readers/CURR-3.prompt.md` (task instructions)
- `<SCRATCH>/readers/CURR-3/` (git clone destination, directory listing only)
- `<SCRATCH>/readers/CURR-3/reproduction/gpu-scheduling-transition-refusal/` (directory listing only — files not individually opened)
- Ran `runner_transition.py` in that directory (not opened/read; executed only)
