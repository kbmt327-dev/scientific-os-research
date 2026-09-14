---
research_id: GPU-SCHED-EP-0007
title: 実クラスタの位置で測り、4本ぶん載せてきた説明を取り下げた
date: 2026-09-13
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: 探索的
evidence_level: 合成シミュレーション（実測値を入力）
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation-with-measured-inputs
  source: 封印した予測1本（PRED-008、4/6）、同時実行ジョブ数を実クラスタの位置まで伸ばす168回実行
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 256サーバの合成マルチサーバジョブモデル、rho 0.85、指数サービス時間、再開コスト0。実クラスタからは比率と同時実行ジョブ数の実測値のみを入力
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0007
source_episode_sha256: b821fb81d95ecfca2fef66f048b85812d98e15ddf39672b666170522b001d27f
publication:
  status: publishable
tags: [finding, scheduling, simulation, retraction, japanese]
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>サイズ優先方式が壊れる条件を、実データで確かめる</span><a href="/en/research/gpu-scheduling-real-cluster-position/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Finding</span><span>合成シミュレーション（実測値を入力）</span><span>探索的</span><span>査読なし</span><span>外部再現 0</span></div>

> [!warning] ここで出した境界の数値は、後に判定器ごと置き換えられました
> 「同時本数が少ないほど境界は高い」という**形は生き残っています**が、数値（0.875、余裕0.285、害5.1倍）は[[ja/research/gpu-scheduling-blind-detector/index|EP-0011]]で判定器が無効と判明したため引用できません。現在の値は[[ja/research/gpu-scheduling-alpha-boundary/index|EP-0012]]と[[ja/research/gpu-scheduling-one-job/index|EP-0013]]にあります。また「別構成で0格子点の再現」という主張は、[[ja/research/gpu-scheduling-third-variable/index|EP-0010]]で**同じ背景分布族の中に限る**と狭められました。

## 現在わかっていること

前の研究（[[ja/research/gpu-scheduling-concurrency/index|EP-0006]]）が駆動変数を同時実行ジョブ数へ訂正しましたが、測った範囲は28.5本以上でした。実在の仮想クラスタで最も危ない位置にいる11cb48は同時実行ジョブ数10.2で、**測定範囲の外**です。前の研究はそこを外挿で「安全側」と言っていました。

外挿を測定に変えました。同時実行ジョブ数9.8で安全境界は0.875、実測比率0.59に対する余裕は0.285です。方向は変わりませんが、根拠が外挿から測定になりました。

そしてもう一つ、この研究は**自分が4本の研究にわたって載せてきた説明を取り下げています。**

取り下げた説明はこうでした。「プール全体を要するジョブは、優先度順で1位にならなければ起動できない。待っているあいだは残り時間が減らないので、永久に1位にならない。これは**構造的な罠**であり、負荷とは無関係である。」

強すぎました。プール全体ジョブの流量は、同時実行ジョブ数とともに0.078から0.850まで**連続的に変化します**。同時本数が7.4のときは飢餓しません。1位になれるかどうかは競合の数の問題であって、質的に別格な条件ではありませんでした。

## 図で見る

<div class="ratio-figure" aria-label="同時実行ジョブ数ごとの安全境界と実クラスタの位置"><div class="ratio-track"><i style="left:59%"></i><i style="left:87.5%"></i></div><div class="ratio-labels"><span style="left:59%"><b>0.59</b> Philly実測<br>余裕 0.285</span><span style="left:87.5%"><b>0.875</b> 同時9.8での境界</span></div></div>

実在の仮想クラスタは同時実行ジョブ数が少ない側にいます。そこでは一つのジョブがプールの大部分を占めても通ります。測定した曲線の上で、実測比率0.59は境界0.875の左側にあります。

## この研究が示すこと

- この合成モデルでは、安全境界は同時実行ジョブ数の減少関数である。同時本数 7.4 / 9.8 / 14.6 / 28.4 / 54.2 / 98.9 に対し、境界は 0.875 / 0.875 / 0.8125 / 0.625 / 0.50 / 0.50。
- 実在の仮想クラスタ11cb48がいる位置（同時本数約10）は、外挿ではなく測定で安全側にある。
- プール全体を要するジョブの飢餓は、質的に別格の現象ではなく、同時本数に沿った連続量である。

## この研究が示さないこと

- 境界の**数値**は、後に無効と判明した判定器で測られています。
- 実際の到着列でスケジューリング方式を動かしていません。実クラスタからは比率と同時本数の**実測値を入力しただけ**です。
- 「別構成での再現」は、同じ背景分布族の中での再現です。族をまたいだ再現は後の研究で通りませんでした。

## なぜ重要か

「構造的な罠」という言葉は、4本の研究にわたって公開文書に載っていました。質的に強い言葉は、読んだ人の行動を変えます。「構造的で負荷と無関係」なら、負荷を下げても意味がないことになります。実際には負荷——正確には同時に走っている本数——こそが効いていました。

**強い言葉は、その言葉が反例を許さないと主張している軸を掃いてから書く。**1点の観測から「構造的」と書いたのが誤りでした。

## 何を調べたか

1. 実在の仮想クラスタがいる同時実行ジョブ数（約10本）での安全境界はいくつか。
2. プール全体を要するジョブの飢餓は、本当に質的に別格の現象なのか。

## 方法

プールを256サーバに固定し、背景需要の粒度を変えることで同時実行ジョブ数を7.4から98.9まで掃きます。各点で比率を7段階振ります。計168回の実行、rho 0.85です。

PRED-008として封印しています。digestは再現パッケージの `predictions/PRED-008.sha256` にあります。対応する結果ファイルが存在しない状態でコミットしました。

前の研究（EP-0006）はプール規模を変えて背景を相対固定する構成、この研究はプールを固定して背景を粗くする構成です。**別々の作り方で同じ同時本数を作れば、同じ境界が出るはず**という再現の検査を組み込みました。

## 結果

**境界は同時実行ジョブ数の減少関数です。**

| 同時実行ジョブ数 | 7.4 | 9.8 | 14.6 | 28.4 | 54.2 | 98.9 |
|---|---|---|---|---|---|---|
| 安全境界 | 0.875 | 0.875 | 0.8125 | 0.625 | 0.50 | 0.50 |

**別構成で一致しました。**EP-0006（プールを変えて背景を相対固定）とEP-0007（プールを固定して背景を粗く）が、同時本数28.5付近で同じ境界0.625を出しました。格子上の差は0点です。

**プール全体ジョブの飢餓は連続量でした。**

| 同時実行ジョブ数 | 98.9 | 54.2 | 28.4 | 14.6 | 9.8 | 7.4 |
|---|---|---|---|---|---|---|
| プール全体ジョブの流量 | 0.078 | 0.178 | 0.265 | 0.519 | 0.693 | 0.850 |

0.078から0.850まで、段差なく変化します。同時本数が少なければ、プール全体を要するジョブでも通ります。

**実クラスタの位置での害。**比率0.625・同時本数9.8で、大ジョブクラスは背景クラスの**5.1倍**遅くなります。前の2つの見積もり（7.4倍、16.3倍）はどちらも誤った軸の上で測られていました。

## 何が変わったか

- 「プール全体ジョブの飢餓は構造的な罠であり負荷と無関係」という説明を**取り下げ**、同時実行ジョブ数に沿った連続量に置き換えました。この説明は4本の研究にわたって載っていました。
- 実クラスタの位置を外挿から測定へ格上げしました。
- 害の見積もりを、7.4倍（EP-0004）→16.3倍（EP-0005）→**5.1倍**（この研究）と、軸の訂正に合わせて2度改訂しました。

## 何が失敗したか

**PRED-008は6本中4本的中。**情報量が大きいのは外れたW5です。

W5は「プール全体ジョブは同時本数が下がっても飢餓したままである」という、**構造的な罠という説明が正しければ必ず当たるはずの予測**でした。外れました。流量は0.850まで上がります。予測を外した瞬間に、4本ぶんの説明が撤回対象になりました。

もう一つのW6は「その位置での害は5倍未満で軽微」という自分の定義に対する予測で、実測5.1倍で僅差で外れています。

**害の倍率を3度書き換えたことも失敗として記録します。**7.4倍、16.3倍、5.1倍。数字そのものが悪いのではなく、**軸が確定する前に運用へ渡せる形の数字を出し続けた**ことが問題でした。

## 証拠の範囲

**言えること：** この合成モデルの中では、安全境界は同時実行ジョブ数の減少関数で、実在の仮想クラスタがいる位置は測定範囲の内側にあり安全側である。プール全体ジョブの飢餓に質的な境界はない。

**言えないこと：** 境界の数値（判定器が後に無効と判明）。トレース上でのpolicy比較。背景分布族をまたいだ再現。

## まだ分からないこと

- 同時本数が7.4と9.8でどちらも0.875なのは飽和なのか、格子の上端に当たっているだけなのか。
- 同時本数98.9より上での振る舞い。
- 負荷rhoへの依存。
- 背景分布の形を変えたときの再現性。

## この結論が崩れるとき

- 背景の粒度を変えるだけで、同じ比率・同じプール・同じ負荷のまま飢餓が現れたり消えたりする。**これは次の研究でそのまま起きます。**
- より細かい格子で、同時本数7.4と9.8の境界が分離する。
- 別の判定器で測ると曲線の形が変わる。**これも後に起きます。形は残り、値は変わりました。**

## 自分で確かめる

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

完全な再実行：

```bash
cd reproduction/gpu-scheduling-boundary
python run_e9.py
python analyze_e9.py
```

## 証拠とデータ

- [公開再現パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [封印済みPRED-008](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-008.json)
- [E9の採点](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E9_grading.json)
- 内部の元Episodeのハッシュ：`b821fb81d95ecfca2fef66f048b85812d98e15ddf39672b666170522b001d27f`

## 外部からの検証

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決の批判：0

## 次の実験

この研究の看板結論——需要分布のsupportがプール全体を含むと飢餓する——を、自分で壊しにいきます。同じ比率・同じプール・同じ負荷のまま、背景の粒度だけを変えて飢餓が消えるかを測ります。

## ここに至るまで

<div class="revision-chain vertical" aria-label="GPUクラスタのスケジューリング研究の更新履歴">
  <a href="/ja/research/gpu-scheduling/"><b>EP-0001</b><span>推定誤差と再実行コストで、最良の方式が入れ替わる。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>平均は良いのに、一部のジョブクラスが終わらない。安定性の判定器も3回壊れた。</span></a>
  <a href="/ja/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>飢餓を決めるのは平均ジョブ幅ではなく、クラスタ全体を要するジョブの有無。</span></a>
  <a href="/ja/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>実測したプールにその条件はなく、害は飢餓ではなく数倍の遅れだった。</span></a>
  <a href="/ja/research/gpu-scheduling-pool-size/"><b>EP-0005</b><span>安全境界はプールが大きいほど下がる。実規模の害は2倍過小評価だった。</span></a>
  <a href="/ja/research/gpu-scheduling-concurrency/"><b>EP-0006</b><span>効いていたのはプールの大きさではなく、同時に取り合うジョブの本数だった。</span></a>
  <a class="current" href="/ja/research/gpu-scheduling-real-cluster-position/"><b>EP-0007 · 現在地</b><span>実クラスタの位置で測り、4本ぶん載せてきた機構説明を訂正した。</span></a>
  <a href="/ja/research/gpu-scheduling-headline-broken/"><b>EP-0008</b><span>背景の粒度を変えるだけで、この研究の看板結論が消えた。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>代表成果だった相図の軸そのものが、18倍交絡していた。</span></a>
  <a href="/ja/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>「2つの数で決まる」を撤回した。頻度が第三の変数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>判定器が発散を測っていなかった。窓で割っていたので、値が動かなかった。</span></a>
  <a href="/ja/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>動かない境界を持つ統計量へ置き換え、運用数値を戻した。</span></a>
  <a href="/ja/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>実クラスタについての主張は、19,100本中1本のジョブに乗っていた。</span></a>
</div>
