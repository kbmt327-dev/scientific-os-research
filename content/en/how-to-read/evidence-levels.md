---
title: Evidence levels
lang: en
aliases: [/methodology/evidence-levels/, /en/methodology/evidence-levels/]
description: How evidence class limits claim scope.
---

Evidence labels describe what was actually checked, not the importance of the topic.

| Class | Supports | Does not by itself support |
|---|---|---|
| Synthetic simulation | Behavior of the stated model and implementation under stated parameters | Real-world effectiveness or external validity |
| Synthetic blind benchmark | Identification within the disclosed hypothesis family on a hidden instance | Discovery of an unknown hypothesis space |
| Public trace measurement | What was actually recorded in that trace | That the trace represents the population, or that the result holds in live operation |
| Contract validation | Schema, references, guards, and negative-control behavior | Numerical correctness or predictive performance |
| Design and power simulation | A specified protocol and sensitivity under explicit assumptions | Feasibility, ethics approval, an observed effect, or final sample size |
| Independent replication | Reproduction by an independent person or group | General validity outside the replicated conditions |

Evidence levels may be extended. Existing notes retain the label used when published.
