---
title: Prediction sealing
lang: en
aliases: [/methodology/prediction-sealing/, /en/methodology/prediction-sealing/]
description: Keeping predictions separate from post-result explanation.
---

A sealed prediction records its text, criterion, timestamp or commit, and cryptographic digest before the relevant result is observed. The original stays immutable. Results are graded against the original criterion; failed and ill-posed predictions remain visible.

Sealing reduces hindsight editing. It does not prove three other things:

- that the hypotheses were independent of each other;
- that the prediction measured the quantity that matters;
- that no information leaked.

The second one bites. In [[en/research/gpu-scheduling-real-traces/index|EP-0004]] the pre-registered retraction trigger did not fire, because the quantity chosen at sealing time was a poor proxy for the question it was meant to settle. Sealing is a procedure, not a guarantee of correctness.

Each note states what was known before sealing.
