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

合成MSJモデルでは、最大ジョブの容量比、同時本数、大ジョブ頻度がpolicy間の順位とクラス飢餓を左右します。以前の境界値はalpha=0.5の判定線に条件付けられ、その閾値の意味はまだ独立較正できていません。

飽和throughputは打ち切りと全ジョブ同時投入による無制限のpacking選択があり、容量measureとして停止しました。開放到着の二分法へ移した保存値も未validatedです。EP-0016の局所監査とEP-0017の独立grid較正は別のbacklog判定との不一致を観測しました。EP-0017は最初の不一致で停止しています。**容量値、判定器の物理的な閾値、実クラスタへの一般化はUNKNOWN**です。

Philly公開トレースで容量の半分超を要求したジョブが19,100本中1本だったという到着頻度の実測は残ります。そこからの余裕の数値は合成モデルの未監査閾値に条件付けられ、実トレース上のscheduler性能ではありません。

**証拠の境界：** 合成モデルとPhilly公開トレースの到着数に限る。EP-0017の公開再現物は集計の算術と停止分岐の検算のみで、raw runやsimulation source、外部独立再現、実クラスタの前向き運用検証はない。

**[現在のResearch Note（EP-0017）を読む →](/ja/research/gpu-scheduling-u31-calibration/)**
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
14. **[[ja/research/gpu-scheduling-u31-calibration/index|EP-0017 — 独立した較正でも、容量を決める二つの判定器は一致しなかった]]（最新）**
<!-- GENERATED: program-history:END -->
