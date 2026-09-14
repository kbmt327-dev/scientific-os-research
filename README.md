# Open Research Lab repository

Source, validation, and bounded reproduction packages for the [Open Research Lab](https://kbmt327-dev.github.io/scientific-os-research/), the public research interface of Scientific OS.

## Repository map

- `content/ja/` and `content/en/` — parallel human-readable Research Notes and guide pages.
- `publication-manifest.yaml` — the source Episode digest and public language views for each research identity.
- `program-current.yaml` — the single editable authority for each Program's current claim, evidence boundary, and current Note.
- `reproduction/` — versioned public artifacts, sealed predictions, results, and rerun code.
- `scripts/` — publication-contract, pair, link, privacy, built-site, and bounded-reproduction checks.
- `docs/PUBLICATION_PIPELINE.md` — operator-facing publication flow.

Program pages are authoritative for mutable current claims, while Research Notes are authoritative for their dated records. Home, Research, `llms.txt`, Program current-state blocks, and the research log are generated from `program-current.yaml` plus the publication manifest; they are not independent claim databases.

## Validate locally

```bash
python -m pip install -r requirements-reproduce.txt
npm ci
npx quartz plugin install
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

The quick reproduction command validates public digests and bounded deterministic paths. It is not an independent replication and does not replace each note's full rerun.

## Contribution boundary

Use Issues for concrete defects and Discussions for replication reports, counterexamples, interpretations, and collaboration. See [CONTRIBUTING.md](CONTRIBUTING.md).

Do not silently change sealed artifacts, erase failed predictions, broaden a claim beyond its evidence class, or submit confidential data. The original code and datasets do not share one blanket reuse license; see [LICENSES.md](LICENSES.md).
