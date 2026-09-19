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

EP-0026は一回の永久parameter遷移を監査。truthful manifestは240/240遷移lookを推論前に拒否。定常と偽ると100kで80/80誤側、service improveは320kでもscheduled20/20誤側でした。gateは未申告driftをデータ検知しません。一般U31/実GPU/時変理論・新規性・査読はUNKNOWN、general detector0。

**証拠の境界：** 既知2block指数strict FCFS、一回の永久切替、eventual-tail label、正しいprovenance manifestに限定。同設計実行は独立外部replicationではありません。

**[現在のResearch Note（EP-0026）を読む →](/ja/research/gpu-scheduling-transition-refusal/)**
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
17. [[ja/research/gpu-scheduling-mmc-transfer/index|EP-0020 — 固定needの4並列対照へ、入力CIを移せた]]
18. [[ja/research/gpu-scheduling-information-tiers/index|EP-0021 — 同じ窓でも、情報が違えば誤り方が違う]]
19. [[ja/research/gpu-scheduling-critical-loss/index|EP-0022 — 棄権の価格と、臨界負荷での定義]]
20. [[ja/research/gpu-scheduling-two-class-control/index|EP-0023 — 二クラスFCFSでは、名目負荷1未満でも過負荷を見逃す]]
21. [[ja/research/gpu-scheduling-past-only-learning/index|EP-0024 — 母パラメータを知らずに、過去の完了から容量を学習する]]
22. [[ja/research/gpu-scheduling-exposure-checkpoints/index|EP-0025 — 固定完了数の露出checkpointで、判定時点と棄権を比較する]]
23. **[[ja/research/gpu-scheduling-transition-refusal/index|EP-0026 — 永久parameter遷移を、定常診断はいつ拒否すべきか]]（最新）**
<!-- GENERATED: program-history:END -->
