---
title: Human movement model interfaces
description: An overview of research into machine-checking the boundary between measured motion data and a model.
lang: en
---

When measured human motion reaches a model, mismatched coordinates, units, or timing can produce an answer that runs but means the wrong thing. This program studies how to protect that boundary with executable checks rather than human attention alone.

## The question

Which input contracts, dataset boundaries, and failure conditions can stop coordinate mix-ups, target leakage, and false external validation before a model runs?

<!-- GENERATED: program-current:START -->
## Current public state

The interface contract rejects seven deliberately broken variants. The dataset gate splits Carter into 30 development, 10 validation, and 10 test participants; reserves OpenCap laboratory data for external validation; and reserves Knee Grand Challenge for internal-load stress testing. B3D is a source-adapter format, the internal representation is NumPy plus explicit semantics, and Nimble is not mandatory.

**Evidence boundary:** No model has been fitted and no holdout has been read.

**[Read the current Research Note (EP-0005) →](/en/research/human-model-dataset-portfolio/)**
<!-- GENERATED: program-current:END -->

<!-- GENERATED: program-history:START -->
## Published Research Notes

1. [[en/research/human-model/index|EP-0004 — A contract that stops human data reaching a model on ambiguous terms]]
2. **[[en/research/human-model-dataset-portfolio/index|EP-0005 — A dataset portfolio that keeps development, external validation, and internal-load testing separate]] (latest)**
<!-- GENERATED: program-history:END -->
