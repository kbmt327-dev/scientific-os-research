---
title: Open Research Lab
description: Research published with its conditions, evidence, limits, and reproduction path.
lang: en
---

<p class="site-lede">This is a place where research is published — not only the conclusion, but the conditions it holds under, what turned out wrong, and where you can check it yourself. <a href="/ja/" hreflang="ja">日本語</a></p>

Scientific OS is an autonomous research workflow. This lab publishes the part of its output that a third party can verify, reproduce, or refute. Conclusions stay provisional until someone outside replicates them.

## What we know right now

<div class="feature-finding">
  <p class="eyebrow">GPU cluster scheduling</p>
  <h3>Real GPU clusters never received a job that filled the pool</h3>
  <p>Running the shortest job first lowers mean wait time, but a job that needs the whole cluster can wait forever behind it. Measuring two public traces showed that none of the 11 pools actually in production ever received such a job.</p>
  <p>So the thing to check is no longer "do whole-cluster jobs arrive" but "<b>what fraction of the pool does the largest job need</b>". The safe boundary is 0.75; the worst measured ratio was 0.59. The predicted harm is not an unbounded wait but a delay — about 7.4× a single-GPU job.</p>
  <p class="feature-meta"><b>Evidence strength:</b> two public traces measured, plus synthetic simulation. No policy was run on a real arrival stream. Zero external replications.</p>
  <p class="feature-actions"><a href="/en/research/gpu-scheduling-real-traces/">Read this study →</a></p>
</div>

## The research

<div class="research-list">
  <a href="/en/research/gpu-scheduling-real-traces/">
    <b>GPU cluster scheduling</b>
    <span>When size-based scheduling breaks. Simulation isolated the mechanism; public traces then tested whether its precondition occurs. Four studies of revision history.</span>
    <small>Finding · current claim is EP-0004</small>
  </a>
  <a href="/en/research/simulation-worlds/">
    <b>Queueing system identification</b>
    <span>A queueing world with its mechanism hidden, and only external records to work from. Can the structure be recovered? Checked against the withheld truth.</span>
    <small>Finding · hypothesis family disclosed</small>
  </a>
  <a href="/en/research/human-model/">
    <b>Human movement model interfaces</b>
    <span>A contract that machine-checks coordinate mix-ups and target leakage when measured data reaches a model, and blocks instead of warning. The public adapter is currently blocked.</span>
    <small>Method · not evidence of predictive performance</small>
  </a>
  <a href="/en/research/badminton-biomechanics/">
    <b>Badminton biomechanics</b>
    <span>A 2×2 design assigning preparation time and backward CoM independently in the smash. Not sealed; data collection is not authorized.</span>
    <small>Protocol · no observations yet</small>
  </a>
</div>

[See the full research index →](/en/research/)

## How to read this

Every study separates the finding from its reach: what changed, what failed, what is still `UNKNOWN`, and the shortest honest reproduction path. You do not need to read all of it.

Start with **[[en/how-to-read/index|How to read a Research Note]]**. Go to [[en/about/scientific-os|the Scientific OS loop]] only when you want the workflow behind it.

## Contribute evidence

The valuable next event is not a star. It is an independent rerun, a failed reproduction, a counterexample, or a better observation. **[[en/contribute/index|Reproduce, challenge, extend, or collaborate →]]**

<p class="quiet-meta"><a href="/en/about/open-research-lab/">About this lab and the person building it</a>. Editorially reviewed; not scientifically, domain-expert, or peer reviewed unless a study says otherwise.</p>
