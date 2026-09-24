# AI cold-reader pilot on the EP-0026 note (EP-0028)

Six fresh AI reader sessions (Claude Code subagents on sonnet; the author is
opus) answered nine presealed questions using only the English EP-0026 note.
Arm BASE read the note as first published; arm CURR read it after the EP-0027
correction. CURR readers were also asked to clone this repository and run the
note's reproduction command.

```sh
python verify_cold_reader.py
```

The verifier checks `protocol.json` and `materials/` against `seal.json`,
rebuilds all six prompts from the sealed template, and recomputes the totals and
prediction grades from `scores.json`. It does not rerun readers or rescore the
free-text answers; `answers/` is published so anyone can rescore.

- `protocol.json`, `seal.json`, `materials/`: sealed bytes.
- `prompts/`, `answers/`: verbatim except that the local scratch directory is
  replaced by `<SCRATCH>`.
- `scores.json`: sealed-key scores, flags, harness events and a separate post-hoc
  substance column that is not the sealed result.

Result: the arms differed only on Q6 (seed dependence, 0/3 vs 3/3) and Q9
(regenerated look count, 0/3 vs 3/3; forced by the text). Q3 (eventual tail vs
finite window) was 6/6. Sealed predictions 3/5. Seven of 13 sealed misses were
caused by key phrasing on Q4 and Q7. One CURR run was blocked by the harness
permission classifier; one reader's Part A was recovered by a follow-up message.

Boundary: same-family AI readers, self-reported isolation, author scoring without
blinding. Not a human study, not external readers, not independent replication.
