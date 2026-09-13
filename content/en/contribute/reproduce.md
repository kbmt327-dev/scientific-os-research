---
title: Reproduce research
lang: en
aliases: [/contribute/reproduce/]
description: Start from a note's exact public reproduction package.
---

Start from the note's **Reproduce** section. Record the public commit, environment, command, inputs, output digest, and any deviations. The fastest cross-project check is:

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick all
```

Quick checks validate artifacts and small deterministic paths. They are not substitutes for a full simulation rerun or an independent experiment.
