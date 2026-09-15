---
research_id: GPU-SCHED-EP-0013
title: 実クラスタについての主張は、19,100本中1本のジョブに乗っていた
date: 2026-09-14
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: 探索的
evidence_level: 公開トレースの測定（シミュレーションなし）
peer_reviewed: false
independent_replications: 0
evidence:
  class: public-trace-measurement
  source: 封印した予測1本（PRED-014、4/6）、Philly仮想クラスタ11個の到着頻度の実測。新規シミュレーションなし
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Microsoft Phillyの公開トレース、500ジョブ以上の仮想クラスタ11個。容量はピーク同時使用GPU数の実測値
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0013
source_episode_sha256: 990cbc3e360d78ce5f7cd1cde10e7550a97c79bbd88d8cedf3e5417d5f4a32ea
publication:
  status: publishable
tags: [finding, scheduling, traces, scope, japanese]
---

<p class="research-area"><b>GPUクラスタのスケジューリング</b><span>サイズ優先方式が壊れる条件を、実データで確かめる</span><a href="/en/research/gpu-scheduling-one-job/" hreflang="en">English</a></p>

<div class="evidence-strip"><span>Finding</span><span>公開トレースの測定</span><span>探索的</span><span>査読なし</span><span>外部再現 0</span></div>

> [!warning] 2026-09-16以降の検証
> [[ja/research/gpu-scheduling-u31-calibration/index|EP-0017]]でalpha=0.5と別のbacklog判定器が局所的に不一致となりました。このNoteの境界・余裕は合成モデルの未監査閾値に条件付けられます。容量保証として使わないでください。

## 現在わかっていること

前の研究で運用表が戻りましたが、表には頻度の列があります。この分野が実在のクラスタについて唯一している主張——Philly仮想クラスタ11cb48は安全側にいる——には、その頻度が測られていませんでした。表の頻度0.002の行なら安全比率0.92（余裕0.33）、0.02の行なら0.72（余裕0.13）。**2.5倍の幅があります。**

シミュレーションを一切使わず、既にあるトレースから測りました。

**11cb48で容量の半分以上を要求したジョブは、19,100本のうち1本です。**頻度 5.2×10⁻⁵。表の最も低い頻度の行より**38倍稀**です。境界は頻度が下がるほど上がるので、その行の0.92をそのまま下界として使えます。

**余裕は0.33（下界）に確定しました。**

ただし、この研究がいちばんはっきりさせたのは余裕の値ではありません。**射程の狭さ**です。

- 11個の仮想クラスタのうち**10個には、容量の4分の1を超えるジョブが1本も来ていません。**
- 唯一の例外11cb48でも、容量の4分の1超は6本、半分超は**1本**です。
- どのクラスタにも、プール全体を占めるジョブは来ていません（再計数で確認）。

**この分野が実在のクラスタについて主張してきたことは、Philly トレース全体で1本のジョブに乗っています。**

## 図で見る

<div class="ratio-figure" aria-label="Phillyの11仮想クラスタにおける大ジョブの頻度"><div class="ratio-track"><i style="left:59%"></i><i style="left:92%"></i></div><div class="ratio-labels"><span style="left:59%"><b>0.59</b> 11cb48の最大比率<br>該当は19,100本中1本</span><span style="left:92%"><b>0.92</b> α基準の境界<br>余裕 0.33</span></div></div>

11cb48の最大ジョブは128 GPU、容量は217 GPUです。その1本を除くと、このクラスタで容量の4分の1を超えるジョブは5本しかありません。

## 結果

| 仮想クラスタ | ジョブ数 | 同時実行 | 容量 | 最大k | 比率 | P(≥0.25) | P(≥0.5) | P(≥1.0) |
|---|---|---|---|---|---|---|---|---|
| 6214e9 | 51,378 | 81.1 | 603 | 16 | 0.03 | 0 | 0 | 0 |
| **11cb48** | **19,100** | **10.2** | **217** | **128** | **0.59** | **0.000314** | **0.000052** | **0** |
| 6c71a0 | 14,833 | 46.2 | 290 | 48 | 0.17 | 0 | 0 | 0 |
| b436b2 | 9,159 | 22.8 | 340 | 32 | 0.09 | 0 | 0 | 0 |
| ee9e8c | 5,602 | 38.9 | 532 | 128 | 0.24 | 0 | 0 | 0 |
| 他6クラスタ | 10,983 | 4.9–27.6 | 66–360 | 1–32 | 0.02–0.25 | 0 | 0 | 0 |

`P(≥0.5)` の 0.000052 は、19,100本中**1本**です。

## この研究が示すこと

- Philly 11cb48の最大比率クラスの到着頻度は 5.2×10⁻⁵。α基準の運用表の最低頻度行より38倍稀である。
- したがって比率0.59に対する余裕は **0.33（下界）**。前の研究の0.13〜0.33という幅は、広い端に確定した。
- 11個の仮想クラスタのうち10個には、容量の4分の1を超えるジョブが存在しない。
- どのクラスタにもプール全体を占めるジョブは来ていない（[[ja/research/gpu-scheduling-real-traces/index|EP-0004]]の看板結論が再計数で生存）。

## この研究が示さないこと

- **頻度の軸で「2つのリスク要因が同時に現れない」かは検定できていません。**容量の40%を超えるジョブを持つクラスタは11cb48だけで、残る10個は0で並んでいます。変動がないので、相関の向きを主張できません。支持も反証もされていない状態です。
- 連続分布を単一クラスの頻度へ写す方法は一意ではありません。仕事量の割合で写すと別の行になる可能性があります。
- 表は256サーバ・rho 0.85・指数サービス時間で測ったもので、Phillyはそのどれとも一致しません。**実クラスタをモデルの軸の上に置いた評価であり、トレース上でスケジューリング方式を走らせた結果ではありません。**

## なぜ重要か

「実トレースで確認した」という言葉は強く響きます。この研究は、その言葉の中身が実際にはどれくらいの規模かを数字にしました。**1本です。**

実務的な含意は、値そのものより手順にあります。自分のクラスタを評価するなら、まず「容量の半分以上を要求するジョブが年に何本来るか」を数えてください。0本なら、この分野の境界の議論は当面あなたに関係しません。11個中10個がその状態でした。

## 何を調べたか

Philly仮想クラスタで、大きいジョブは実際にどれだけ頻繁に来るのか。11cb48はα基準の表のどの行に落ちるのか。

## 方法

Phillyの `cluster_job_log` から、500ジョブ以上の仮想クラスタごとに、容量（ピーク同時使用GPU数）、同時実行ジョブ数、最大ジョブ幅、そして `P(必要GPU数 ≥ q × 容量)` を q = 0.25 / 0.40 / 0.50 / 0.59 / 0.75 / 1.00 で測ります。**新規シミュレーションはありません。**

PRED-014として、SHA-256 `9fedc330b067f8cc3616f1fcc896f55ba4bb3887ebf523dfcf4493ad539ee281` で封印しています。対応する結果ファイルが存在しない状態でコミットしました。

封印文には測定量の選び方の理由も書いてあります。連続分布を単一クラスの頻度へ写す方法は一意ではないので、選んだ写像が**保守的でない側（上界側）に倒れる**ことを明記しました。容量をピーク同時使用から取ることも、比率を上界側にします。どちらも「測ったリスクを過小に見せない」向きです。

## 何が変わったか

- Phillyの余裕を、0.13〜0.33という幅から **0.33（下界）** へ確定しました。
- 「実トレースで確認した」の中身を、**1本のジョブ**という規模で明記しました。
- 前の研究の「実トレースでは比率と同時実行ジョブ数が負に相関し、2つのリスク要因が同時に現れない」を、**同時実行ジョブ数の軸では有効、頻度の軸では検定できていない**に分けました。

## 何が失敗したか

**PRED-014は6本中4本的中。決定予測K1は的中しました。**

**K2が外れました。そして外れた理由は、私が封印した閾値そのものです。**

11cb48の容量は217 GPU、最大ジョブは128 GPU。比率は 128 ÷ 217 = **0.5899** です。封印文には閾値 `q = 0.59` と書きました。すると `0.59 × 217 = 128.03` となり、**比率を定義しているまさにそのジョブが、0.03 GPUの差で除外されました。**

`P(≥0.59)` が0なのは物理ではなく、**丸めた比率を閾値として書き戻した結果**です。閾値を0.5に置けば該当1本、K2の判定式も満たします。

これは、この分野が繰り返し見つけてきた失敗の**5例目**です。格子丸め、判定線、標本数、窓正規化、そして閾値の丸め。今回は封印時に「該当が0本でないこと」を条件に入れていたので、**採点の瞬間に検出できました。**条件を書いていなければ「該当0本」という強い結論をそのまま出していた可能性が高い。

**K4が外れました。ただし反証ではありません。**比率と頻度の相関は+0.50（p=0.117）で封印基準（≤0）を満たしません。しかし容量の40%を超えるジョブを持つクラスタは11cb48だけで、残る10個は0で並んでいます。**相関は「逆だった」のではなく、「このトレースには変動がない」のです。**事前約束は実行しましたが、書き方は「頻度軸へ広がらない」ではなく「このトレースでは検定できない」としました。

**手続き上の不備。**採点スクリプトを封印コミットに含めませんでした。前の3本では予測ファイルと同じコミットに入れていました。判定式は予測本文に全部書いてあるので採点自体は機械的ですが、規律としては一段落ちます。`results/E15_grading.json` に `grading_script_not_sealed: true` として記録しました。

## 証拠の範囲

**言えること：** Philly 11cb48の最大比率クラスの頻度は19,100本中1本。11個中10個の仮想クラスタには容量の4分の1を超えるジョブが存在しない。どのクラスタにもプール全体ジョブは来ていない。これらはすべてトレースの実測です。

**言えないこと：** 頻度軸での2つのリスク要因の関係（検定不能）。トレース上でのスケジューリング方式の比較。余裕0.33は実測頻度を合成モデルの表へ入力した評価です。

## まだ分からないこと

- 頻度軸で「2つのリスク要因が同時に現れない」か。Phillyだけでは変動がないので、他のトレースが要ります。
- 実クラスタの頻度は表の格子上に来ません。11cb48は最低行よりさらに下にあり、**表の外側に置いて下界として読むしかない**状態です。
- 連続分布から単一クラスの頻度への写し方を変えたときの感度。

## この結論が崩れるとき

- 公表された割当枠が、ピーク同時使用よりはるかに小さい容量を示す。その場合、比率が上がり余裕が縮みます。
- 別の運用トレースに、高い比率と高い頻度を同時に持つプールが見つかる。
- 頻度の写し方を仕事量の割合に変えると、表の別の行に落ちる。

## 自分で確かめる

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

この簡易確認は、**19,100本中1本という測定値**を結果ファイルから再計算し、どの仮想クラスタにもプール全体ジョブが無いことを確かめます。

完全な再実行には生のPhillyトレースが必要です（ここでは再配布していません）。`msr-fiddle/philly-traces` から取得して `data/trace-data/` に置いてください。

```bash
cd reproduction/gpu-scheduling-boundary
python run_e15.py
```

## 証拠とデータ

- [公開再現パッケージ](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [封印済みPRED-014（測定量の選び方の理由を含む）](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-014.json)
- [E15の測定値](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E15.json)
- [E15の採点（封印されなかった採点スクリプトの記録を含む）](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E15_grading.json)
- 内部の元Episodeのハッシュ：`990cbc3e360d78ce5f7cd1cde10e7550a97c79bbd88d8cedf3e5417d5f4a32ea`

## 外部からの検証

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決の批判：0

## 次の実験

運用表の頻度軸を細かくします。現在は0.002と0.02の2行しかなく、実クラスタの実測値5.2×10⁻⁵は**表の外側**にあります。下端を10⁻⁴まで伸ばし、中間の格子を足して、実測頻度を丸めずに読めるようにします。

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
  <a href="/ja/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>代表成果だった相図の軸そのものが、18倍交絡していた。</span></a>
  <a href="/ja/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>「2つの数で決まる」を撤回した。頻度が第三の変数だった。</span></a>
  <a href="/ja/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>判定器が発散を測っていなかった。窓で割っていたので、値が動かなかった。</span></a>
  <a href="/ja/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>動かない境界を持つ統計量へ置き換え、運用数値を戻した。</span></a>
  <a class="current" href="/ja/research/gpu-scheduling-one-job/"><b>EP-0013 · 現在地</b><span>実クラスタについての主張は、19,100本中1本のジョブに乗っていた。</span></a>
</div>
