# Publication pipeline

This is an operator-facing implementation note. Public readers should begin with the site's **How to read** pages instead.

## Boundary

An internal Episode is the dated, append-oriented research record. A public Research Note is a narrower, privacy-reviewed projection. Publication never copies a private workspace wholesale and never rewrites a sealed prediction.

```text
Vault Episode (source record)
  → project a blank public-note skeleton and record source SHA-256
  → author parallel Japanese and English views with one research_id
  → register both views in publication-manifest.yaml
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

## Required checks

```bash
python scripts/publish_episode.py validate content
python scripts/check_links.py content
python scripts/check_llms.py quartz/static/llms.txt content
python scripts/privacy_scan.py .
python scripts/reproduce.py --quick all
npx quartz build
python scripts/install_llms.py quartz/static/llms.txt public/llms.txt
python scripts/check_built_site.py public
```

Validation fails closed on missing language counterparts, mismatched or duplicate research identities, missing evidence boundaries, missing scope sections, invalid links, local paths, secret-like strings, and missing public routes. A quick reproduction pass is an internal reproducibility check, not an independent replication.

## Change policy

- Preserve dated claims and artifact history.
- Add prominent forward links when later work narrows or withdraws a claim.
- Keep failed predictions, instrument defects, and `UNKNOWN` visible.
- Distinguish editorial, scientific, domain-expert, and peer review.
- Preserve old public URLs through redirects when canonical paths move.
- Push only after the complete local gate passes.
