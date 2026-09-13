---
title: Open Research Lab
description: Reproducible, auditable research conducted by Scientific OS.
date: 2026-09-13
---

> **Research conducted by Scientific OS — published for reproduction, audit, challenge, and extension.**

This is an open research lab powered by Scientific OS. Research is published with its hypotheses, evidence, failures, uncertainties, and reproduction paths. Claims are provisional unless independently replicated. Critique, replication, and falsification are welcome.

<div class="lab-principles">
  <div><strong>Reproduce</strong><span>Run the code or follow the protocol.</span></div>
  <div><strong>Audit</strong><span>Trace claims to evidence and sealed predictions.</span></div>
  <div><strong>Falsify</strong><span>Target the conditions that would weaken a claim.</span></div>
  <div><strong>Keep UNKNOWN</strong><span>Do not convert missing evidence into confidence.</span></div>
</div>

## Current research

| Research Note | State | Evidence boundary |
|---|---|---|
| [[research/gpu-scheduling/index\|Scheduling principles reverse under workload mix and preemption friction]] | `Finding` · `Synthetic` · `Exploratory` | Simulator validated against analytic and conservation checks; no real trace validation. |
| [[research/simulation-worlds/index\|Blind identification of batched arrivals and heterogeneous servers]] | `Finding` · `Synthetic blind benchmark` | Hidden instance recovered inside a known mechanism family; not open-world discovery. |
| [[research/human-model/index\|Human Model Contract v0.2]] | `Method` · `Contract validation` | Fail-closed schema and cross-document checks; no human-model predictive performance. |
| [[research/badminton-biomechanics/index\|2×2 preparation-time × backward-CoM protocol]] | `Protocol` · `Not sealed` | Design and power sensitivity only; no confirmatory data. |

## From private research to public evidence

```mermaid
flowchart LR
  A[Scientific OS] --> B[Private Research State]
  B -->|privacy-reviewed projection| C[Public Research Note]
  C --> D[Claim]
  C --> E[Evidence]
  C --> F[Reproduction]
  C --> G[Failures and UNKNOWN]
  C --> H[Falsification targets]
  D & E & F & G & H --> I[External audit and replication]
```

An internal Episode is never replaced by its public projection. See [[about/methodology|methodology]] and [[about/open-research-lab|why the boundary matters]].

## Start here

- **Reproduce a result:** [[contribute/reproduce]]
- **Audit or challenge a claim:** [[contribute/audit]]
- **Collaborate:** [[contribute/collaborate]]
- **Understand evidence labels:** [[methodology/evidence-levels]]
