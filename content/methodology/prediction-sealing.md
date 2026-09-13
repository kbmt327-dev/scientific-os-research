---
title: Prediction sealing
description: Keeping predictions separate from post-result explanation.
---

A sealed prediction records its text, criterion, timestamp or commit, and cryptographic digest before the relevant result is observed. The original stays immutable. Results are graded against the original criterion; failed and ill-posed predictions remain visible.

Sealing reduces hindsight editing. It does not prove that the hypothesis was independent, important, or free from leakage. Each note states what was known before sealing.
