---
title: About Scientific OS
description: The internal research workflow behind the published notes.
---

Scientific OS is an internal research workflow for moving from a question to competing hypotheses, sealed predictions, evidence, diagnosis, model revision, and the next observation. It keeps `UNKNOWN` and `UNRESOLVED` as valid outputs when the available evidence cannot identify an answer.

This public repository does **not** demonstrate that Scientific OS autonomously produces correct science, improves itself, or transfers across real-world domains. Each public note stands or falls on its own evidence and reproduction path.

```mermaid
flowchart TD
  Q[Question] --> H[Competing hypotheses]
  H --> P[Predictions sealed before observation]
  P --> O[Observation or experiment]
  O --> E[Evidence]
  E --> F{Falsified or identifiable?}
  F -->|No| U[UNKNOWN / request new observation]
  F -->|Yes| R[Revise or retain model]
  U --> Q
  R --> Q
```
