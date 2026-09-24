# Public article self-containment audit (EP-0027)

This package scores the two EP-0026 public articles
(`content/{ja,en}/research/gpu-scheduling-transition-refusal/index.md`) against a
12-item regex rubric per language. The rubric, three predictions and a stop rule
were sealed after EP-0026 was published and before baseline scoring. The seal is
a local hash and clock only; there is no external timestamp. The rubric was
designed after reading the article, so the audit is not blinded.

```sh
python verify_self_containment.py
```

The verifier checks that `protocol.json` and `public_self_containment.py` match
`seal.json`, that the baseline snapshots match the sealed baseline hashes, and
rescores both stages. Expected: baseline ja 8/12, en 8/12; corrected ja 12/12,
en 12/12.

- `protocol.json`, `seal.json`, `public_self_containment.py`: sealed bytes.
- `baseline.json`, `remediation.json`: recorded scores.
- `baseline-snapshot/`: the articles as scored at baseline. They are stored with
  CRLF line endings because the sealed hashes were taken on a Windows checkout;
  `.gitattributes` keeps these bytes unchanged. The corrected articles were
  scored on LF bytes, and the verifier normalizes CRLF before comparing them.

Baseline misses in both languages: C06 (the fact was present but the pattern
required a word order), C07 (common-seed dependence not stated), C11 (no link to
the two-class stability source) and C12 (the article said 24 regenerated looks;
the EP-0026 runner regenerates 72). Predictions: 2/3; P1 predicted 9/12.

This is a document-content audit. No reader was recruited. The corrected 12/12
was written against the rubric and is nearly guaranteed by the correction. It is
not evidence of reader comprehension, usability, novelty or independent
replication.
