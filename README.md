# Open Research Lab

Machine-generated research, published with enough evidence for humans to reproduce, audit, challenge, and build upon.

## 1. What is this?

Open Research Lab is the public research surface of Scientific OS. It publishes bounded research notes, evidence, failure records, and the shortest currently available reproduction path. It is not a mirror of the private research environment: an internal Episode remains an append-only research record, while a public Research Note is a privacy-reviewed projection.

The public site is: <https://kbmt327-dev.github.io/scientific-os-research/>

## 2. Research principles

- Claims remain provisional unless independently replicated.
- Sealed predictions are separated from post-result interpretation.
- Negative results, failed predictions, analysis bugs, and instrument defects remain visible.
- `UNKNOWN` is an acceptable result and an explicit next-observation request.
- Evidence class and claim scope are stated on every Research Note.
- Publication fails closed on private paths, credential-like strings, missing evidence boundaries, or missing reproduction status.

## 3. Current research

| Note | Type | Evidence | Status | External replications |
|---|---|---|---|---:|
| [Scheduling principles reverse under workload mix and preemption friction](content/research/gpu-scheduling/index.md) | Finding | Synthetic simulation | Exploratory | 0 |
| [Blind identification of batched arrivals and heterogeneous servers](content/research/simulation-worlds/index.md) | Finding | Synthetic blind benchmark | Exploratory | 0 |
| [Human Model Contract v0.2](content/research/human-model/index.md) | Method | Contract validation | Validated contract only | 0 |
| [2x2 preparation-time x backward-CoM protocol](content/research/badminton-biomechanics/index.md) | Protocol | Design and power simulation | Draft, not sealed | 0 |

## 4. How to reproduce

Clone the repository, install Python dependencies, and run the public checks:

```bash
git clone https://github.com/kbmt327-dev/scientific-os-research.git
cd scientific-os-research
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick all
```

The GPU and queueing Findings include fuller packages and exact commands under [`reproduction/`](reproduction/). A quick check validates published artifacts; a full simulation rerun takes longer and is deliberately explicit.

## 5. How to audit / challenge

Found a bug? Failed to reproduce a result? Have a counterexample? Open an Issue for a concrete defect in code, data, metadata, or the site. Use [Discussions](https://github.com/kbmt327-dev/scientific-os-research/discussions) for replication reports, critique and falsification, research ideas, collaboration, and applications. Include the note ID, environment, command, observed output, and expected output.

## 6. How to contribute

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions that weaken uncertainty labels, remove failed predictions, or silently change a sealed artifact will not be accepted. New research types can be added without changing existing notes.

## 7. About Scientific OS

Scientific OS is the internal research workflow that records questions, competing hypotheses, predictions, evidence, model changes, and unresolved uncertainty. This repository publishes selected projections from that workflow. The existence of an automated workflow is not evidence that its scientific claims are correct.

## 8. Disclaimer

This repository contains exploratory research and methods, not peer-reviewed conclusions or professional advice. The content, original code, and datasets do not yet share one blanket reuse license; see [LICENSES.md](LICENSES.md). Quartz retains its upstream MIT license in [LICENSE.txt](LICENSE.txt).
