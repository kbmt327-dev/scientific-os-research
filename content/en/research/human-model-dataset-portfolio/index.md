---
research_id: HUMAN-MODEL-EP-0005
lang: en
aliases: [/research/human-model-dataset-portfolio/index]
title: A dataset portfolio that keeps development, external validation, and internal-load testing separate
date: 2026-09-14
domain: Scientific Human Model
type: Dataset
status: Dataset roles and participant split fixed; no model result
evidence_level: Source-backed dataset design
peer_reviewed: false
independent_replications: 0
evidence:
  class: source-backed-dataset-design
  source: Primary dataset records, a deterministic 50-participant split, and bounded archive-index inspection
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: Dataset roles, leakage boundaries, and a fixed participant split for the first locomotion benchmark
source_episode: HUMAN-MODEL/EP-0005
source_episode_sha256: d4e7e6e2a2cc0a98f789e396483b5d8c043fd8f6d8a2d2fd1bc6744b63d5f6d3
publication:
  status: publishable
tags: [dataset, human-model, biomechanics, validation, preregistration]
---

<p class="research-area"><b>Human movement model interfaces</b><span>Separating development data from the tests that can challenge it</span><a href="/ja/research/human-model-dataset-portfolio/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Dataset</span><span>Source-backed design</span><span>No model fitted</span><span>No holdout read</span><span>0 external replications</span></div>

Follows [[en/research/human-model/index|the contract that blocks ambiguous model inputs]].

## Dataset decision

No single dataset is treated as the answer for a general human model. The first vertical slice will use three distinct roles:

| Role | Dataset | What it can test |
|---|---|---|
| Development and internal holdout | [Carter et al. 2024](https://doi.org/10.15125/BATH-01341), distributed through [AddBiomechanics](https://addbiomechanics.org/download_data.html) | Locomotion across participants, speeds, and gradients with motion capture and force plates |
| External validation | [OpenCap laboratory validation](https://doi.org/10.1371/journal.pcbi.1011462) | Transfer to a separately collected source with walking, squat, sit-to-stand, and drop-jump laboratory measurements |
| Internal-load stress test | [Knee Grand Challenge](https://doi.org/10.1002/jor.22023) | Whether a later model survives comparison with instrumented-implant knee contact force |

[AMASS](https://arxiv.org/abs/1904.03278) is reserved for kinematic coverage, not force validation. [HuMoD](https://www.informatik.tu-darmstadt.de/sim/forschung_sim/datensaetze_sim/humod_sim/index.en.jsp) is an EMG diagnostic source, not a generalization benchmark.

## Research question

Which public datasets and holdout boundaries allow the first locomotion benchmark to develop a model without silently reusing the sources that are supposed to challenge it?

## Why this matters

Testing development and validation on reprocessed versions of the same raw source can look like external evidence while preserving the same collection and processing assumptions. Dataset roles have to be fixed before large downloads, feature engineering, or model fitting.

## Method

Primary dataset records were compared for participants, activities, measured modalities, licensing, and directness of the target. The first quantity of interest was limited to force-plate-measured three-dimensional ground-reaction force normalized by body weight, plus contact state. Joint torque was not selected as the first ground truth because it depends on inverse dynamics and model parameters.

The 50 Carter participant IDs were stratified using the sex labels in the source table, then sorted within each label by age and participant ID. A deterministic modulo-five rule assigned 30 participants to development, 10 to validation, and 10 to test. Each partition contains equal counts of the two source labels. The upstream test participant P010 remains in test.

B3D is treated only as one source-adapter format. The internal representation is NumPy arrays plus explicit coordinate, unit, frame, processing, missingness, and provenance metadata. The Nimble API is therefore not a dependency for defining or training the Human Model; official-reader parity remains an optional reproducibility check for the adapter.

## Results

The development, validation, and test IDs are now fixed in a public machine-readable manifest. The source participant table is represented by its URL, size, and SHA-256 rather than copied. A previously acquired one-megabyte ZIP64 central-directory tail showed 610 non-empty Carter B3D members and identified P008_split2 as the smallest development-participant With_Arm candidate. That B3D file has not been downloaded.

## What changed

The next gate moved from mandatory Nimble-versus-protobuf reader parity to dataset selection and leakage control. Subject40 remains a contract counterexample and is not used as a prediction benchmark. Development now uses participant holdout, while external validation requires a different raw source.

## What failed

No model or dataset operation failed in this episode because neither model fitting nor holdout evaluation was run. The earlier plan to make Nimble parity the next mandatory gate was rejected: it would test reader agreement, not the scientific usefulness of the Human Model.

## Evidence boundary

**Supported:** the public sources are assigned distinct roles; the Carter participant split is deterministic and internally consistent; the acquisition boundary and leakage rules are machine-checkable.

**Not supported:** B3D numerical extraction, trial usability, input-channel validity, model training, metric thresholds, held-out performance, external validity, internal-load accuracy, or a general human model.

## UNKNOWN

- Whether P008_split2 contains enough frames with usable measured ground-reaction force.
- Which kinematic processing pass is independent of force-plate optimization.
- Exact trial conditions, channel shapes, coordinate conventions, units, and missingness in the selected B3D member.
- Numerical thresholds, resampling, event definitions, and final baseline implementations.
- Whether any learned model will beat the two required simple baselines on held-out participants.

## Falsification targets

- A validation or test participant influences normalization, fitting, feature choice, or threshold selection.
- A dynamics-pass feature optimized against force-plate data is used to predict that trial's force target.
- Reprocessing the same raw source is counted as independent external validation.
- Participant assignments change after missingness or performance is inspected.
- A complex model fails to beat the development-mean waveform and regularized-linear baselines on the sealed participant-level metric.

## Reproduce

~~~bash
python scripts/reproduce.py --quick human-dataset
~~~

This verifies the published manifest, split outputs, counts, hashes, and declared non-execution boundary. It does not download the source datasets or independently reproduce their measurements.

## Evidence / Artifacts

- [Dataset portfolio manifest and validator](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/human-model-dataset-portfolio)
- [Carter source record](https://doi.org/10.15125/BATH-01341)
- Internal source Episode digest: d4e7e6e2a2cc0a98f789e396483b5d8c043fd8f6d8a2d2fd1bc6744b63d5f6d3

## External audit

- Independent replications: 0
- Failed replications: 0
- Confirmed bugs after publication: 0
- Open critiques: 0

## Next experiment

Range-download only P008_split2, inspect it with protobuf and NumPy, and determine trial condition, timebase, channel shapes, processing passes, usable ground-reaction-force fraction, coordinates, and units. Do not read validation or test participants, fit a model, or install Nimble unless that bounded inspection exposes a reader-specific ambiguity.
