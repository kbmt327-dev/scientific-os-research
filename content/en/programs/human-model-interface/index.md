---
title: Human movement model interfaces
description: An overview of research into machine-checking the boundary between measured motion data and a model.
lang: en
---

When measured human motion reaches a model, mismatched coordinates, units, or timing can produce an answer that runs but means the wrong thing. This program studies how to protect that boundary with executable checks rather than human attention alone.

## The question

Which input contracts and failure conditions can stop coordinate mix-ups, target leakage, and incomplete conversions before a model runs?

## Current public boundary

A correct bundle passes nine check groups, and all seven deliberately broken variants are rejected. This validates the interface contract, not the numerical conversion or predictive performance of a model. The public adapter remains blocked because a coordinate mismatch is unresolved.

**[[en/research/human-model/index|Read the latest Research Note →]]**
