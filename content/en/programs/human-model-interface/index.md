---
title: Human movement model interfaces
description: An overview of research into machine-checking the boundary between measured motion data and a model.
lang: en
---

When measured human motion reaches a model, mismatched coordinates, units, or timing can produce an answer that runs but means the wrong thing. This program studies how to protect that boundary with executable checks rather than human attention alone.

## The question

Which input contracts, dataset boundaries, and failure conditions can stop coordinate mix-ups, target leakage, and false external validation before a model runs?

## Current public boundary

A correct contract bundle passes nine check groups, and all seven deliberately broken variants are rejected. The next dataset gate is now fixed: develop on a 30-participant Carter split, reserve 10 participants each for validation and test, use OpenCap laboratory data only for external validation, and reserve Knee Grand Challenge for internal-load stress testing. B3D is a source-adapter format; NumPy plus explicit semantics is the internal representation, and Nimble is not a mandatory Human Model dependency. No model has been fitted and no holdout has been read.

**[[en/research/human-model-dataset-portfolio/index|Read the latest Research Note →]]**
