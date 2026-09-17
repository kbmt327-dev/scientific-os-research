---
title: GPUクラスタのスケジューリング
description: サイズ優先スケジューリングが有効な条件と破綻する条件を調べる研究の概要です。
lang: ja
---

GPUクラスタでは、多数のジョブが限られたGPUを取り合います。この研究では、短いジョブを先に実行するサイズ優先方式が、平均待ち時間を短くできる条件と、一部のジョブを長く待たせる条件を調べています。

## 問い

ジョブサイズ、推定誤差、再開コスト、クラスタ容量の組み合わせが変わると、サイズ優先方式と予約型方式の優劣はどのように変わるのか。とくに、良い平均値の裏で一部のジョブが飢餓していないかを検査します。

## これまでの進展

合成シミュレーションで、クラスタ全体を必要とするジョブが一つあるだけで、サイズ優先と貪欲な詰め込みの組み合わせが飢餓を起こしうることを切り分けました。公開トレース2本を調べると、実運用中の11プールにはクラスタ全体を占めるジョブは観測されませんでした。

その後の7本は、**自分の出した数値を自分で壊す作業**が中心になりました。駆動変数はプール規模ではなく同時実行ジョブ数でした（EP-0006）。看板だった「supportがクラスタ全体を含むと飢餓する」は、背景の粒度だけで消えました（EP-0008）。代表成果だった相図の軸は18倍交絡していました（EP-0009）。「2つの数で決まる」は撤回しました（EP-0010）。

そして**判定器そのものが壊れていました**（EP-0011）。境界の判定に使っていた flow balance は、応答時間を観測窓で割った打ち切り比であり、発散を検出できません。平均待ち時間が3.9倍に伸びるあいだ、判定器は0.562から0.574にしか動きませんでした。運用数値はいったん全部停止しました。

置き換えた統計量 **α**（平均待ち時間の観測窓に対する弾性）は、安定な条件で0を、線形発散で1を読み、観測窓を8倍にしても境界を0.02しか動かしません（EP-0012）。運用数値は**頻度の列を足した形で**戻っています。

<!-- GENERATED: program-current:START -->
## 現在の公開結論

EP-0018で中点queue閾値が既知過負荷を見逃し、EP-0019ではM/M/1負荷1.005が320k×3 seedでもUNKNOWNでした。EP-0020は同質64資源・全need16・FCFSの既知M/M/4へ入力CIを移し、control2/holdout4を正しい側に確定しました。30 workload・10 look、負荷1.01は160k×3 seedが必要で、4 engine fixtureも整合しました。

これは指数/独立入力・全offered true work・機構capacity4に条件付けられる限定transferです。保存失敗後の復旧rerunと既に観測したcontrolを開示しています。**U-31全体、mixed-need/c12容量、実クラスタへの一般化はUNKNOWN、validated general detectorは0件**です。

技術報告草稿を作成しましたが、新規性は未確立です。次の比較は出力だけ・真のwork付き・drain後JCTの情報tierと実時間cutoffを揃えて設計します。旧境界は未監査alphaに条件付けられ、Phillyの頻度実測からの余裕は実trace上のscheduler性能ではありません。

**証拠の境界：** 合成known-model対照とPhilly公開traceの到着数に限定。公開artifactは十分統計・F quantile・CI・停止/engine照合要約の算術検査。generator/simulator再実行、経験的coverage、外部独立再現、公開論文・査読、実クラスタの前向き検証は未完了。

**[現在のResearch Note（EP-0020）を読む →](/ja/research/gpu-scheduling-mmc-transfer/)**
<!-- GENERATED: program-current:END -->

<!-- GENERATED: program-history:START -->
## 公開中のResearch Note

1. [[ja/research/gpu-scheduling/index|EP-0001 — 推定誤差と再実行コストで、GPUスケジューリングの優劣が入れ替わる]]
2. [[ja/research/gpu-scheduling-phase-diagram/index|EP-0002 — 平均は良いのに一部のジョブだけが終わらない。安定性の判定器も3回壊れた]]
3. [[ja/research/gpu-scheduling-starvation-mechanism/index|EP-0003 — 飢餓を決めるのは平均ジョブ幅ではなく、クラスタ全体を要するジョブが1本でもあるかどうか]]
4. [[ja/research/gpu-scheduling-real-traces/index|EP-0004 — 実際のGPUクラスタには、プール全体を占めるジョブが来ていなかった]]
5. [[ja/research/gpu-scheduling-pool-size/index|EP-0005 — 安全境界はプールが大きいほど下がる]]
6. [[ja/research/gpu-scheduling-concurrency/index|EP-0006 — 効いていたのはプールの大きさではなく、同時に取り合うジョブの本数だった]]
7. [[ja/research/gpu-scheduling-real-cluster-position/index|EP-0007 — 実クラスタの位置で測り、4本ぶん載せてきた説明を取り下げた]]
8. [[ja/research/gpu-scheduling-headline-broken/index|EP-0008 — 背景の粒度を変えるだけで、この研究の看板結論が消えた]]
9. [[ja/research/gpu-scheduling-phase-reaxis/index|EP-0009 — 代表成果だった相図の軸そのものが、18倍交絡していた]]
10. [[ja/research/gpu-scheduling-third-variable/index|EP-0010 — 「2つの数で決まる」を撤回した]]
11. [[ja/research/gpu-scheduling-blind-detector/index|EP-0011 — 判定器が発散を測っていなかった。窓で割っていたので、値が動かなかった]]
12. [[ja/research/gpu-scheduling-alpha-boundary/index|EP-0012 — 動かない境界を持つ統計量へ置き換え、運用数値を戻した]]
13. [[ja/research/gpu-scheduling-one-job/index|EP-0013 — 実クラスタについての主張は、19,100本中1本のジョブに乗っていた]]
14. [[ja/research/gpu-scheduling-u31-calibration/index|EP-0017 — 独立した較正でも、容量を決める二つの判定器は一致しなかった]]
15. [[ja/research/gpu-scheduling-known-controls/index|EP-0018 — 既知の過負荷を、中点のqueue閾値が見逃した]]
16. [[ja/research/gpu-scheduling-drift-uncertainty/index|EP-0019 — 小さな過負荷を、有限窓では確定できなかった]]
17. **[[ja/research/gpu-scheduling-mmc-transfer/index|EP-0020 — 固定needの4並列対照へ、入力CIを移せた]]（最新）**
<!-- GENERATED: program-history:END -->
