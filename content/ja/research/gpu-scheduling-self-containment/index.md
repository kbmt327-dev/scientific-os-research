---
research_id: GPU-SCHED-EP-0027
title: 公開記事は、自分の主張を読み違えないための事実を載せていたか
date: '2026-09-24'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: Lexical document audit; reader comprehension UNKNOWN
evidence_level: Sealed document-content rubric
peer_reviewed: false
independent_replications: 0
evidence:
  class: document-content-audit
  source: Sealed 12-item lexical rubric scored on the EP-0026 public articles
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Presence of predeclared facts in two public articles; no reader recruited;
  no comprehension, usability or novelty claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0027
source_episode_sha256: f2942bad6a89de109b28064272123d1ad31416785fecdcf901340b62d2699af0
publication:
  status: publishable
tags:
- gpu-scheduling
- reporting-audit
- reproducibility
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-self-containment/" hreflang="en">English</a></p>

## 現在わかっていること

EP-0026の日英公開記事を、公開後・採点前に封印した12項目の字句rubricで採点すると、両言語とも8/12でした。欠けていた4項目のうち1件は数値の誤りで、再現手順が「24 lookを再生成」と書いていましたが、公開runnerは72 lookを再生成します。

## 図で見る

![封印rubricの項目別の合否（是正前・是正後）](/assets/gpu-scheduling-self-containment.svg)

塗りつぶしは項目あり、白抜きは欠落または誤り。2段階でrubricは変えていません。

## この研究が示すこと

表示確認・hash一致・CIを通った公開記事にも、主張の境界を読むのに必要な事実の欠落と、再現手順の数値誤りが残っていました。hashは記事の中身の正しさを検査しません。

## この研究が示さないこと

読者は採用していません。読者の理解、使いやすさ、新規性、需要、独立外部replicationは示しません。是正後の12/12はrubricを見ながら書いたので、ほぼ是正行為そのもので達成されます。

## 何を調べたか

EP-0026記事が、推定対象（eventual-tail）と有限窓の区別、正しいprovenanceの前提、未申告driftを検出しないこと、主要件数、反復単位の従属性、モデル構造、独立replication数、general detector数、正解labelの一次文献、再現コマンドと再生成look数を明示しているか。

## なぜ重要か

外部読者の理解テストより前に、記事に必要な事実が載っていなければ、読者の誤解と記事の欠落を区別できません。

## 方法

12項目×2言語の正規表現rubric、予測3本、停止規則をbaseline採点前に封印しました（local hashのみ、外部timestampなし）。rubricはEP-0026記事を読んで設計したので盲検ではありません。baseline後はrubricを変えず、同じrubricが要求する文だけを追記・訂正しました。

## 結果

| 項目 | baseline | 原因 | 是正 |
|---|---|---|---|
| C06 service improveの320k持続 | 両言語× | 事実は記載済み。rubricが語順を測っていた（予測外） | 語順を変え、他の遷移が320kで全件正解と明記 |
| C07 共通seedとcell間従属 | 両言語× | 反復単位の従属性が未記載 | 独立120seedではないと追記 |
| C11 正解labelの一次文献 | 両言語× | 定理名だけでlinkなし | Grosof et al.へlink |
| C12 再生成look数 | 両言語× | 24と誤記 | 72（2seed×2モデル×6scenario×3look） |

封印予測は2/3。P1（baseline各言語9/12）は8/12で外れ、P2（是正後12/12）とP3（24→72、記録360 lookは不変）は当たりました。

## 何が変わったか

EP-0026記事を訂正しました。以前の記事を読んだ方は、再生成look数を72と読み替えてください。

## 何が失敗したか

P1が外れました。C06の失敗は記事の欠落ではなく、rubricのpatternが事実の有無でなく語順を測っていたためです。baselineの失敗は消さずに残しています。

## 証拠の範囲

2記事×12項目＝24記録。baseline snapshotは封印hashと一致するbytesで保存。rubricの字句一致であり、意味の正しさの判定ではありません。

## まだ分からないこと

作者の補助なしに外部読者がtruthful/false declarationの差とeventual-tail labelを説明・再実行できるかはUNKNOWN。独立外部replication0、general detector0。

## この結論が崩れるとき

12項目が読者の誤解の主因を外していれば、12/12でも理解テストで失敗します。字句一致は解釈の正しさを保証しません。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-self-containment)で`python verify_self_containment.py`。封印hashを照合し、baseline snapshotを8/12、現行記事を12/12と再採点します。

## 証拠とデータ

[protocol、seal、runner、baseline/是正後の採点、baseline snapshot](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-self-containment)。protocol・seal・runnerは封印時と同一bytesです。

## 外部からの検証

独立外部replication0。読者0人。同じ作者による再採点で、第三者の検証ではありません。

## 次の実験

作者を含まない読者に公開ページだけを渡し、事前封印した設問で理解と再実行を採点する仕様を作ります。AI読者を使う場合は人間の外部読者と区別して報告します。

[[ja/research/gpu-scheduling-transition-refusal/index|EP-0026]] → EP-0027
