---
title: 研究
description: 分野ごとの研究テーマ、現在の結論、証拠の種類。
lang: ja
---

<p class="site-lede">分野ごとにまとめています。各項目には、いま何が言えているかと、証拠の種類を添えました。<a href="/en/research/" hreflang="en">English</a></p>

分類は自信の強さではなく、研究が何を足すかで決めています。**Finding** は観測から得た結果、**Method** は研究を進めるための仕組み、**Protocol** は確証データを取る前に固定した将来の検査です。

## GPUクラスタのスケジューリング

**テーマ：** 短いジョブを先に通す「サイズ優先」のスケジューリングは、どの条件で壊れるか。

**現在の結論：** 壊れる仕組みは合成シミュレーションの中で確かに存在します。クラスタ全体を要するジョブが1本でも混じると、サイズ優先＋貪欲な詰め込みの組み合わせがそのジョブを永久に待たせます。ただし公開トレース2本を測ったところ、実際に運用されているプールにそのようなジョブは来ていませんでした。現在見るべき指標は「最大ジョブがプール容量の何割か」で、安全側の目安は0.75、実測された最悪値は0.59です。害は飢餓ではなく数倍の遅れでした。

**[最新の結論を読む（EP-0004）→](/ja/research/gpu-scheduling-real-traces/)**

<details class="series-history" id="gpu-scheduling-program">
<summary>ここに至るまでの4本</summary>

<div class="revision-chain vertical" aria-label="GPUクラスタのスケジューリング研究の更新履歴">
  <a href="/ja/research/gpu-scheduling/"><b>EP-0001 · 合成シミュレーション</b><span>推定誤差と再実行コストで、最良の方式が入れ替わる。2つの主張は後続で条件付きになった。</span></a>
  <a href="/ja/research/gpu-scheduling-phase-diagram/"><b>EP-0002 · 合成シミュレーション</b><span>平均は良いのに一部のジョブクラスが終わらない。安定性の判定器が3回壊れた。</span></a>
  <a href="/ja/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003 · 仕組みの切り分け</b><span>平均を揃えた対照群で原因を分離。ただしここで出した運用規則は後に取り下げた。</span></a>
  <a class="current" href="/ja/research/gpu-scheduling-real-traces/"><b>EP-0004 · トレース測定＋合成 · 現在地</b><span>実測プールに条件を満たすジョブはゼロ。劣化は連続で、モデル上の暫定的な目安は0.75。</span></a>
</div>

主張がどう変わったかを調べるときは、EP-0004から逆向きに読んでください。この4本は公開している更新履歴であり、内部の更新がすべて公開済みであることを意味しません。

</details>

## 待ち行列のシステム同定

**テーマ：** 中身の仕組みを隠した待ち行列の世界に対し、外から見える記録だけでどこまで仕組みを言い当てられるか。

**現在の結論：** あらかじめ開示された候補集合の中で、隠された1事例を正しく同定できました。構造の5要素すべてが正解と一致しています。ただしこれは「与えられた選択肢から選ぶ」検査であり、未知の仮説空間からの発見ではありません。

**[この研究を読む →](/ja/research/simulation-worlds/)** — Finding

## 人体運動モデルのデータ接続

**テーマ：** 計測した人体の動きをmodelへ渡す前に、座標の取り違え、答えの漏れ、見かけだけの外部検証を、明示的な契約とdataset境界で止められるか。

**現在地：** 接続契約は意図的に壊した7つの変種を拒否します。さらに最初のdataset gateを固定しました。Carterをdevelopment 30人、validation 10人、test 10人へ分け、OpenCapの実験室dataは外部検証、Knee Grand Challengeは内部荷重のstress testにだけ使います。B3Dはsource adapter形式で、Nimbleは必須ではありません。model fittingもholdout読込もまだ実施していません。

**[現在のdataset判断を読む（EP-0005）→](/ja/research/human-model-dataset-portfolio/)** — Dataset

以前の方法：**[曖昧な接続を止める契約（EP-0004）→](/ja/research/human-model/)**

## バドミントンのバイオメカニクス

**テーマ：** スマッシュで、準備時間の短さと後方重心の効果を切り分けられるか。

**現在の状態：** 実験計画と検出力の感度解析まで。**観測はまだありません。** 交互作用を検出するには主効果よりずっと多い参加者が必要と分かり、人数を決められていません。機器の実行可能性と倫理審査も未解決なので、封印せず、データ取得も承認していません。

**[この計画を読む →](/ja/research/badminton-biomechanics/)** — Protocol

---

将来は、既存の研究の識別子を変えないまま、Replication、Negative Result、Dataset、Benchmarkを追加できます。
