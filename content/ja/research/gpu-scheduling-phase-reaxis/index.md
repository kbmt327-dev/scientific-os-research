---
research_id: GPU-SCHED-EP-0009
title: 代表成果だった相図の軸そのものが、18倍交絡していた
date: 2026-09-14
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: 探索的
evidence_level: 合成シミュレーション
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation
  source: 封印した予測1本（PRED-010、7/7的中）、旧相図210回の完全再走と等要約対照90回、計300回
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 64サーバの合成マルチサーバジョブモデル、rho 0.7/0.85/0.95、指数サービス時間、再開コスト0
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0009
source_episode_sha256: a2c4be8afc557a71ba447773163d0fcf512d15181a8b235720fc3048b629c6d2
publication:
  status: publishable
tags: [finding, scheduling, simulation, confounding, japanese]
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>サイズ優先方式が壊れる条件を、実データで確かめる</span><a href="/en/research/gpu-scheduling-phase-reaxis/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Finding</span><span>合成シミュレーション</span><span>探索的</span><span>査読なし</span><span>外部再現 0</span></div>

## 現在わかっていること

[[ja/research/gpu-scheduling-phase-diagram/index|EP-0002]]が作った21セルの相図は、この研究の代表成果でした。需要mixを表すパラメータθと負荷rhoの平面上で、どの方式がどこで壊れるかを示した図です。

前の研究が看板結論を壊したあと、同じ疑いが相図にも向きました。**θを動かすと、同時実行ジョブ数も一緒に動いているのではないか。**

動いていました。**θを0.4から2.0へ動かすと、同時実行ジョブ数は全負荷で約18分の1になります。**θは需要mixの形だけでなく、平均ジョブ幅を2.37から43へ変え、到着率と同時実行ジョブ数を18倍動かしていたのです。

封印した飢餓判定では、飢餓セルの同時実行ジョブ数は18.95〜25.71、非飢餓セルは1.05〜11.33で、**重なりがありませんでした。**したがって旧相図の飢餓境界をθの効果として読むことは**撤回**します。

ただし相図を捨てるわけではありません。**二層に分けて読みます。**

1. **安定性の層**：どのクラスが飢餓するかは、最大ジョブ比率と同時実行ジョブ数で整理する。ここではθは代理変数でした。
2. **条件付き順位の層**：どの方式も健全なセルでの平均待ち時間の順位には、ジョブ幅の異質性が残る。等質な大ジョブ群（高θ・rho 0.7）では、greedy SRPTがServerFillingより7〜17%速いという結果はそのまま有効です。

## 図で見る

<div class="ratio-figure" aria-label="旧θ軸と同時実行ジョブ数の交絡"><div class="ratio-track"><i style="left:5%"></i><i style="left:95%"></i></div><div class="ratio-labels"><span style="left:5%"><b>θ=2.0</b><br>同時 1.05〜1.42</span><span style="left:95%"><b>θ=0.4</b><br>同時 19.0〜25.8</span></div></div>

旧相図の横軸θは、そのまま同時実行ジョブ数の軸でもありました。端から端で約18倍です。飢餓が起きるのは右端（同時本数が多い側）に集中しています。

## この研究が示すこと

- 旧相図のθ軸は、全負荷で同時実行ジョブ数を18.1〜18.2倍動かしていた。
- 飢餓セルと非飢餓セルは、同時実行ジョブ数の上で重なりなく分離する（18.95〜25.71 対 1.05〜11.33）。
- 最大ジョブ比率・その頻度・平均ジョブ幅・負荷を揃えて背景分布の**形だけ**を3通りに変えても、飢餓の判定は変わらなかった。
- 旧相図の210回の実行は、主要な測定値の差**0**で完全に再現した。

## この研究が示さないこと

- 同時実行ジョブ数と最大ジョブ比率の2つで、方式間の**平均待ち時間の順位**まで決まるとは示していません。安定性の層についての主張です。
- 対照群では最大ジョブの頻度を群内で固定しているので、頻度が第三の変数でないことは示せていません。次の研究がそれを調べ、**第三の変数であると判明します**。
- 判定に使った統計量は後の研究で無効と判明しました。ただしここでの分離は重なりゼロなので、判定線の位置には依存しません。

## なぜ重要か

相図は「どの条件でどの方式を選ぶか」を読み取るための図です。横軸を需要mixの形だと思って読むと、需要mixを変えられない運用者には打つ手がないように見えます。

実際に効いていたのが同時実行ジョブ数なら、打つ手はあります。同時に走らせる本数は、運用側が調整できる量だからです。**軸のラベルが間違っていると、読者が使える操作が見えなくなります。**

## 何を調べたか

1. 旧相図のθ軸は、同時実行ジョブ数と交絡しているか。
2. 交絡しているなら、飢餓セルと非飢餓セルは新しい軸の上で分離するか。
3. 最大ジョブ比率と同時実行ジョブ数を揃えれば、背景分布の形を変えても飢餓の判定は変わらないか。

## 方法

**再測定の腕。**旧相図のうちgreedy SRPTとServerFilling-SRPTの210回を、同じシード・同じ設定で完全に再走します。旧測定値が差0で再現することを確認してから、新たに保持した同時実行ジョブ数を読みます。

**等要約対照の腕。**64サーバ・rho 0.85で、最大ジョブ比率・その確率・平均ジョブ幅・到着率を群内で揃え、背景分布の形だけを narrow / geometric / wide の3通りに変えます。平均ジョブ幅4（予想同時本数13.6）と16（同3.4）の2群を置きます。計90回。

PRED-010として、SHA-256 `c68cbf56b09da9dfe5a6c1493836979bda716c642dab8788834cbc54d7a741ea` で封印しています。対応する結果ファイルが存在しない状態でコミットしました。

決定予測Y4は「2つの数を揃えれば背景形状を変えても判定は不変」、すなわち**その時点の作業仮説が反証されうる側**に指名してあります。

## 結果

**旧θ軸は同時実行ジョブ数と18倍交絡していました。**

| 負荷 | θ=0.4 | 0.8 | 1.25 | 2.0 | 端点比 |
|---|---|---|---|---|---|
| 0.70 | 19.00 | 4.14 | 1.67 | 1.05 | 18.1倍 |
| 0.85 | 23.03 | 5.02 | 2.03 | 1.27 | 18.1倍 |
| 0.95 | 25.84 | 5.62 | 2.27 | 1.42 | 18.2倍 |

全負荷で厳密に単調です。

**飢餓セルと非飢餓セルは分離します。**飢餓セルの同時実行ジョブ数は18.95〜25.71、非飢餓セルは1.05〜11.33。重なりはありません。

**背景の形を変えても判定は変わりませんでした。**

| 群 | 背景形状 | 同時実行ジョブ数 | 大クラスの流量 | 判定 |
|---|---|---|---|---|
| 高同時 | narrow / geometric / wide | 13.366 / 13.366 / 13.367 | 0.460 / 0.460 / 0.458 | すべて飢餓 |
| 低同時 | narrow / geometric / wide | 3.268 / 3.259 / 3.222 | 0.870 / 0.858 / 0.831 | すべて健全 |

群内の流量の幅は最大0.040で、封印した許容幅0.15の内側です。

**旧相図は差0で再現しました。**210回すべてで、平均待ち時間・利用率・実効負荷・流量の最大絶対差は0でした。

## 何が変わったか

- 相図の**飢餓境界をθの効果として読むことを撤回**し、最大ジョブ比率と同時実行ジョブ数の軸へ置き直しました。
- 相図を一枚の図から**二層**（安定性の層と条件付き順位の層）に分けました。
- 「等質な大ジョブ群ではgreedy SRPTがServerFillingより7〜17%速い」という条件付き順位の結論は**維持**しました。

## 何が失敗したか

**PRED-010は7本中7本的中しました。**

失敗として記録すべきは、やはり過去の側です。**代表成果の軸が交絡していることを、7本の研究のあいだ誰も確かめていませんでした。**θというパラメータは需要mixの形を表す名前がついていたので、形だけを変えていると思い込んでいました。実際には平均ジョブ幅を18倍動かし、負荷を固定するために到着率も18分の1にしていました。

**パラメータの名前は、そのパラメータが何を動かしているかの証拠になりません。**

また、低同時本数群のgreedy SRPTの平均待ち時間が背景形状によって55.1から79.7まで変わったことを観測していますが、これは方向を封印していないので探索的な観測に留めます。

## 証拠の範囲

**言えること：** 旧相図のθ軸は同時実行ジョブ数と強く交絡しており、飢餓境界はその新しい軸の上で分離する。調べた範囲では、最大ジョブ比率と同時実行ジョブ数を揃えれば背景形状によらず飢餓判定は一致する。

**言えないこと：** 方式間の平均待ち時間の順位まで2つの数で決まること。最大ジョブの頻度が第三の変数でないこと（次の研究で第三の変数と判明します）。実トレース上での挙動。

## まだ分からないこと

- 最大ジョブの頻度・比率・同時実行ジョブ数を完全に独立に振ったときも、2変数の整理が保つのか。
- 等要約対照で低同時本数群の平均待ち時間が形状により変わった理由。
- 条件付き順位の層に残る異質性の効果の大きさ。

## この結論が崩れるとき

- 同時実行ジョブ数と最大ジョブ比率を揃えたセルで、最大ジョブの頻度だけを変えて飢餓判定が反転する。**次の研究で、これに近いことが起きます。**
- 飢餓セルと非飢餓セルが同時実行ジョブ数の上で重なる条件が見つかる。

## 自分で確かめる

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

完全な再実行：

```bash
cd reproduction/gpu-scheduling-boundary
python run_e11.py
python analyze_e11.py
```

## 証拠とデータ

- [公開再現パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [封印済みPRED-010](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-010.json)
- [E11の採点](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E11_grading.json)
- 内部の元Episodeのハッシュ：`a2c4be8afc557a71ba447773163d0fcf512d15181a8b235720fc3048b629c6d2`

## 外部からの検証

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決の批判：0

## 次の実験

最大ジョブ比率・その頻度・同時実行ジョブ数を完全に独立に操作する実験を組みます。この研究は頻度を群内で固定したので、2変数で足りるという主張の十分性はまだ確かめていません。

## ここに至るまで

<div class="revision-chain vertical" aria-label="GPUクラスタのスケジューリング研究の更新履歴">
  <a href="/ja/research/gpu-scheduling/"><b>EP-0001</b><span>推定誤差と再実行コストで、最良の方式が入れ替わる。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>平均は良いのに、一部のジョブクラスが終わらない。安定性の判定器も3回壊れた。</span></a>
  <a href="/ja/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>飢餓を決めるのは平均ジョブ幅ではなく、クラスタ全体を要するジョブの有無。</span></a>
  <a href="/ja/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>実測したプールにその条件はなく、害は飢餓ではなく数倍の遅れだった。</span></a>
  <a href="/ja/research/gpu-scheduling-pool-size/"><b>EP-0005</b><span>安全境界はプールが大きいほど下がる。実規模の害は2倍過小評価だった。</span></a>
  <a href="/ja/research/gpu-scheduling-concurrency/"><b>EP-0006</b><span>効いていたのはプールの大きさではなく、同時に取り合うジョブの本数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-real-cluster-position/"><b>EP-0007</b><span>実クラスタの位置で測り、4本ぶん載せてきた機構説明を訂正した。</span></a>
  <a href="/ja/research/gpu-scheduling-headline-broken/"><b>EP-0008</b><span>背景の粒度を変えるだけで、この研究の看板結論が消えた。</span></a>
  <a class="current" href="/ja/research/gpu-scheduling-phase-reaxis/"><b>EP-0009 · 現在地</b><span>代表成果だった相図の軸そのものが、18倍交絡していた。</span></a>
  <a href="/ja/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>「2つの数で決まる」を撤回した。頻度が第三の変数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>判定器が発散を測っていなかった。窓で割っていたので、値が動かなかった。</span></a>
  <a href="/ja/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>動かない境界を持つ統計量へ置き換え、運用数値を戻した。</span></a>
  <a href="/ja/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>実クラスタについての主張は、19,100本中1本のジョブに乗っていた。</span></a>
</div>
