# Publication pipeline

This is an operator-facing implementation note. Public readers should begin with the site's **How to read** pages instead.

## Boundary

An internal Episode is the dated, append-oriented research record. A public Research Note is a narrower, privacy-reviewed projection. Publication never copies a private workspace wholesale and never rewrites a sealed prediction.

```text
Vault Episode (source record)
  → project a blank public-note skeleton and record source SHA-256
  → author parallel Japanese and English views with one research_id
  → register both views in publication-manifest.yaml
  → if the Note changes a Program's current claim, update program-current.yaml
  → generate Program, Research, Home, llms.txt, and research-log views
  → freeze or add the bounded reproduction package
  → validate schema, language pairs, required sections, links, llms.txt, and privacy
  → run bounded reproduction checks
  → build, inspect, deploy
```

## Project a note

```bash
python scripts/publish_episode.py project <episode.md> content/en/research/<slug>/index.md --type Finding
```

The compiler records the Episode digest but does not copy the Episode body or decide scientific validity. Author the public claim from evidence, with explicit `Shows`, `Does not show`, `UNKNOWN`, falsification, and reproduction sections. Create a Japanese view with the same `research_id`; neither language is designated the master.

## Manifest contract

Each entry identifies one research object and its two public views:

```yaml
- research_id: GPU-SCHED-EP-0004
  source_episode: GPU-SCHEDULING/EP-0004
  source_episode_sha256: <sha256>
  views:
    en: content/en/research/gpu-scheduling-real-traces/index.md
    ja: content/ja/research/gpu-scheduling-real-traces/index.md
  type: Finding
  publication:
    status: publishable
```

The source digest protects the relationship to the internal record. It is not a scientific-validity seal.

## One current-claim authority

`program-current.yaml` is the only editable source for each Program's current public claim, evidence boundary, and current Research Note. The following are generated views and must not be edited independently:

- the current-state and note-history blocks on `content/{lang}/programs/.../index.md`;
- the research-area blocks on `content/{lang}/research/index.md`;
- the Program cards and current-note links on each language home;
- the research-area section in `quartz/static/llms.txt`;
- `content/{lang}/research-notes/index.md`.

After updating the manifest or current claim, run:

```bash
python scripts/sync_current_state.py
```

`python scripts/sync_current_state.py --check` fails if a derived view differs, if a current Research Note is missing, or if a newer manifest entry in that Program exists. Research Notes remain immutable dated records; a Program page is authoritative only for the mutable current claim.

## Required checks

```bash
python scripts/publish_episode.py validate content
python scripts/sync_current_state.py --check
python scripts/check_links.py content
python scripts/check_llms.py quartz/static/llms.txt content
python scripts/privacy_scan.py .
python scripts/reproduce.py --quick all
npx quartz build
python scripts/install_llms.py quartz/static/llms.txt public/llms.txt
python scripts/check_built_site.py public
```

Validation fails closed on missing language counterparts, mismatched or duplicate research identities, stale current-state projections, missing evidence boundaries, missing scope sections, invalid source and built links, local paths, secret-like strings, and missing public routes. A quick reproduction pass is an internal reproducibility check, not an independent replication.

## Change policy

- Preserve dated claims and artifact history.
- Add prominent forward links when later work narrows or withdraws a claim.
- Keep failed predictions, instrument defects, and `UNKNOWN` visible.
- Distinguish editorial, scientific, domain-expert, and peer review.
- Preserve old public URLs through redirects when canonical paths move.
- Push only after the complete local gate passes.
