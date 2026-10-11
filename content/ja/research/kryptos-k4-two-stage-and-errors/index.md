---
research_id: KRYPTOS-K4-EP-0241
title: 二段階・誤差族の記録では検査範囲内の登録通過なし
date: '2026-10-11'
lang: ja
domain: Kryptos K4
type: Negative Result
status: 完了した有限範囲で登録通過なし。EP-0241 r27は部分集合のみ
evidence_level: 有限探索記録と集計値の整合性確認
peer_reviewed: false
independent_replications: 0
evidence:
  class: 登録済み有限探索の記録と保存済み集計
  source: 公開K4 crib制約およびEP-0227、EP-0236、EP-0238、EP-0240、EP-0241の記録
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: EP-0227、EP-0236、EP-0238、EP-0240の完了した登録範囲、およびEP-0241の登録族とr27の26設定部分集合
source_episode: KRYPTOS-K4/EP-0241
source_episode_sha256: 2bfb1fc591b586fe1323fee84a38d7174ea6ba5a7588a5349179b3cc67acdfc2
publication:
  status: publishable
tags:
- kryptos-k4
- two-stage
- finite-search
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-two-stage-and-errors/" hreflang="en">English</a></p>

## 現在わかっていること

ここでまとめる完了した登録範囲では、登録通過数は0だった。EP-0227のnull記録には診断上のidentity hitが1件あるが、登録規則は非identityを要求していたため、適格な通過には数えない。EP-0236とEP-0241では登録前のK4露出と、それに続く候補族または指標・部分集合の選択が開示されている。EP-0240のB/C列はK4最小hが得られておらず、順位割合は定義できない。

## 図で見る

| 記録 | 完了した範囲 | 記録された結果 |
|---|---|---|
| EP-0227 | null 22対象、88行 | K4とnullの登録通過は0。nullのidentity診断1件は適格外 |
| EP-0236 | 登録設定466件、null 20本 | K4通過0、最小d*=4、null最小d*は3が6本・4が14本。記録割合20/20=1.00 |
| EP-0238 | 結合null 200本 | 結合最小max=4、最小sum=8。null割合0.14と0.505、登録通過0 |
| EP-0240 | 各列の主null 200対象、補助10対象 | K4とnullの登録通過0。Aは最小h=15・0.85、ABは最小h=15・0.87。B/C割合は未定義 |
| EP-0241 | r26、hb、bh、r21は各null 1,000本。r27は26設定・null 100本 | 登録通過なし。r27のnullは登録済み部分集合（1%）で0/100通過。q1全体のK4探索とnull評価は未完了 |

ここでPは指定したK4閾値以下となった記録済みnull標本の割合である。有限標本の記述値であり、確証的なp値ではない。

## この研究が示すこと

表に挙げた有限探索では登録済み通過基準を満たす結果がなかった。null集計とEP-0227のidentity診断は、各記録の適格条件に従って解釈する。EP-0241 r27では100本のnull評価が登録済み26設定（q1の1%）に限られて完了している。q1全体のK4探索もnull評価も未完了である。

## この研究が示さないこと

これらの記録はK4の解読、解の一意性、未検査の族が成立しないことを示さない。独立再現もない。EP-0236とEP-0241ではK4露出後に候補族または指標・部分集合を選んでおり、独立確認ではない。新しいK4 plaintextは生成されていない。

## 何を調べたか

完了した二段階族とcrib誤差族の登録探索から、公開K4制約に対する適格な通過が記録されたか、null比較がどの範囲まで判定可能かを確認した。

## なぜ重要か

通過数0の意味は登録範囲と適格条件の内側に限られる。EP-0227の適格外identity診断、EP-0240で定義できない割合、EP-0241の部分的なq1被覆を分けて示すことで、有限の結果を一般的な結論として誤読しにくくする。

## 方法

5つのEpisode記録と保存済み集計を照合し、登録通過数、標本数、ヒストグラム、未判定の範囲を転記した。軽量検算は保存集計の件数と割合だけを再計算し、元の探索は再実行しない。

## 何が変わったか

5件の記録を日英の公開ノート、集計JSON、限定的な算術検算としてまとめた。新しい探索や独立再現は行っていない。

## 何が失敗したか

表の範囲では登録通過が記録されなかった。EP-0240のB/C列は順位割合を判定できず、EP-0241 r27のnull集合はq1全体を覆っていない。

## 証拠の範囲

主張は完了した有限設定、null標本、適格条件に限る。EP-0236では登録前K4露出が候補族と面設定の選択に影響した。EP-0241でも登録前にK4が露出し、その後に指標とr27部分集合が選ばれた。一方、登録規則・閾値・設定一覧・列分けは露出後に変更されていないと記録されている。EP-0241の実行ごとのcode hashは未検証である。これらの記録を超える主張はしない。

## まだ分からないこと

独立再現はない。EP-0241のq1全体を対象にしたK4探索もnull評価も未完了である。nullが完了したのは26設定の部分集合のみで、実行ごとのcode hashも未検証である。EP-0240のB/C順位割合は定義できない。登録前のK4露出が報告された順位に与えた影響も分からない。

## この結論が崩れるとき

行単位の監査で適格な登録通過が見つかる、保存ヒストグラムから割合を再現できない、または忠実な独立再現で登録件数が変わる場合、有限範囲の記述を改める必要がある。q1全体のnull評価を登録・完了すれば、null比較の範囲に関する記述を更新できる。K4側の全q1探索は未完了であり、null完了とは別に実行・報告が必要である。

## 自分で確かめる

リポジトリのルートから次を実行する。

    python reproduction/kryptos-k4-two-stage-and-errors/verify_two_stage_and_errors.py

この検算は公開集計の算術と範囲フラグだけを確認し、候補族やnull探索は再実行しない。

## 証拠とデータ

参照したEpisode識別子はEP-0227、EP-0236、EP-0238、EP-0240、EP-0241。公開パッケージ:

- reproduction/kryptos-k4-two-stage-and-errors/README.md
- reproduction/kryptos-k4-two-stage-and-errors/results/two-stage-and-errors-20261011.json
- reproduction/kryptos-k4-two-stage-and-errors/verify_two_stage_and_errors.py

## 外部からの検証

独立再現は0件。付属verifyは著者側の集計値整合チェックであり、独立した科学的監査や全探索の再実行ではない。

## 次の実験

K4露出前に候補族・指標・閾値・部分集合を事前登録し、実行ごとのcode hashを保存した独立実装で確認する。q1全体のnull比較を主張するには、q1全体のnull評価を登録し、完了させる。K4側の全q1探索も別途完了させる必要がある。
