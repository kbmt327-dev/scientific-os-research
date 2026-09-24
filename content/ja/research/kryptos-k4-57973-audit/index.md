---
research_id: KRYPTOS-K4-EP-0001
title: modelの自由度を数えても、primer 57973は際立つか
date: '2026-09-19'
lang: ja
domain: Kryptos K4
type: Finding
status: Claimed numbers reproduced; the cribs do not single out 57973
evidence_level: Exact reproduction plus three controls on public ciphertext
peer_reviewed: false
independent_replications: 0
evidence:
  class: audit
  source: Public K4 ciphertext, the 24 public crib letters, and the numeric claims of a research handoff
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Whether the public cribs discriminate the reverse-Gromark-57973 hypothesis;
  not whether K4 is a Gromark-type cipher
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0001
source_episode_sha256: ba7dc182c8f4c5aadbb63686e21a4ebcf6e06ba349566086a8bea66e598dad13
publication:
  status: publishable
tags:
- kryptos-k4
- audit
- capacity
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-57973-audit/" hreflang="en">English</a></p>

## 現在わかっていること

ある研究引き継ぎ資料は、K4はprimer 57973・鍵列を反転・任意の26文字alphabet 2つを使うGromark暗号だと論じていました。資料が挙げた数値はすべて厳密に再現します。反転した場合のprimer 100,000個のうち23個がcribに合い、57973はその1つで、平文を13文字強制します。しかし、これらの数値は57973を際立たせません。ランダムな数字列もGromarkと同じ頻度でcribに合い、13文字は経路なし・ずらしなしの1通りでだけ現れ、経路を許せば無作為に選んだprimerもすべて合います。公開cribでは、この仮説を偶然と区別できません。K4がGromark型の暗号ではない、ということは示していません。

## 図で見る

![cribに合う率：ランダムなmask 4.07e-4、Gromark順方向 3.90e-4、反転 2.30e-4。下段は57973が強制する文字で、恒等経路では13文字、列経路28・ずらし50では21文字](/assets/kryptos-k4-57973-audit.svg)

上：2つのalphabetを自由にしたとき、鍵列が24文字のcribに合う頻度。下：強制される文字は経路によってまったく変わります。

## この研究が示すこと

- 資料の数値は正しく、資料が明記していなかった定義も1つ特定しました。「反転」とは、97桁を順に生成してから数列を逆順にすることです。資料が挙げた13桁のmaskすべてに合うのはこの読みだけで、ほかの読みは最大3桁しか合いません。
- 一様ランダムなmaskは4.07×10⁻⁴（2,000,000本中813本）の率でcribに合い、Gromarkの順方向3.90×10⁻⁴、反転2.30×10⁻⁴と変わりません。23という数は、任意のalphabet 2つが吸収できる自由度を測っているのであって、Gromarkの性質ではありません。
- 13文字の強制には、恒等経路とずらし0が必要です。経路・ずらし・向きの55,096通りでは482通りが合い、最大21文字が強制され、その中身は毎回違います。資料自身が経路は必要だと論じており、そうすると13文字は消えます。
- 無作為に選んだprimer 40個すべてに、合う経路があります。どちらの指標でも57973は中央値以下です。

## この研究が示さないこと

K4がGromarkやその類の暗号ではないこと、57973が誤りであること、別のprimerが正しいことは示しません。否定したのは、「公開cribがこの仮説を判別する」という主張だけです。

## 何を調べたか

reverse-Gromark-57973のために示された数値は公開データだけで再現するか。そしてそれは仮説を偶然から判別するか。

## なぜ重要か

26文字のalphabetを2つ自由にするmodelは、24文字の既知平文で拘束できる量よりはるかに大きな自由度を持ちます（拘束は約113 bit、自由度は210 bit以上）。この状況ではほとんどどんな鍵列も「合う」ので、合うprimerの数はK4よりもmodelについて語ります。ここでの対照は、それを見えるようにするための検査です。

## 方法

- 公開暗号文とcribだけから実装し直しました。鍵列は5桁のprimerから d_i = (d_{i−5} + d_{i−4}) mod 10、関係式は CA(C_i) − PA(P_i) = d_i (mod 26) で、2つのalphabetは自由です。両立するかどうかは、mod 26のoffset付きのunion-find（52文字）で厳密に判定します。
- primer 100,000個すべてを両方向で調べ、両立するprimerごとに強制文字を数え、57973のalphabet配置数を数えました。
- 対照1：一様ランダムな97桁のmaskを2,000,000本、同じ判定にかけました。
- 対照2：57973について、紙で実行できる経路284本 × 巡回ずらし97通り × 向き2通り。
- 対照3：無作為なprimer 40個を、同じ経路の族で試しました。

## 結果

| 主張 | 資料 | 再現 |
|---|---|---|
| 両立するprimer（順方向／反転） | 39 / 23 | 39 / 23（同じprimer） |
| 57973（順方向／反転） | 不可／可 | 不可／可 |
| 57973のalphabet配置数 | 29,120 | 29,120（連結成分5） |
| 強制文字の最大 | 13（3個のprimer） | 13（57928, 57973, 59346） |

| 対照 | 結果 |
|---|---|
| ランダムなmask | 4.07×10⁻⁴、Gromarkと同じ高さ |
| 57973の経路 | 55,096通り中482通りが両立、強制は最大21文字 |
| 無作為なprimer | 40個中40個に両立する経路がある |

## 何が変わったか

reverse-Gromark-57973の線を「有力な仮説」から「公開cribでは判別されない」に分類し直しました。内部記録では、alphabetをkeyword由来のものに制限しても役に立ちませんでした。合う最短のkeywordは、実際の配置で16文字、ランダムな配置でも16文字で、制限は本物もランダムも同じように落とします。

## 何が失敗したか

alphabetを制限する最初の試みでは、keyword alphabet 1,300個で生存0件となり、一時的に「線が閉じた」と読みました。これには検出力がありませんでした。偶然の期待値が0.053件で、0件はありふれた結果だったからです。撤回し、対応するnullを持つ構造的な検定に置き換えました。

## 証拠の範囲

使ったのは公開暗号文、24文字のcrib、資料の数値主張です。経路の族は作者が選んだ、紙で実行できる経路の有限リストで、すべての経路ではありません。対照は作者自身によるもので、独立ではありません。

## まだ分からないこと

K4がそもそもGromark型の鍵列を使っているか。資料の出典が `TOKIO` から57973をどう導いたか（後の内部episodeで扱い、ここでは公開していません）。外部の独立replicationは0件です。

## この結論が崩れるとき

K4を見る前に固定した規則で57973と経路が導かれ、それが未公開の平文文字を正しく当てれば、仮説は復活します。否定した恒等経路modelからの封印予測（PRED-001、SHA-256 `daea50e3e4de55539d9e96c89577d2c7c45658776eaef9ebe2f7571bfb743c12`、2026-09-19封印）は、平文が公開されるまで未採点です。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-57973-audit)：`python verify_57973_audit.py` は、primerの全走査、強制文字、配置数、経路の掃引を標準ライブラリで1分以内に再実行し、記録した結果と一致すれば `PASS` を出します。`--full` を付けると2つの乱数対照も再実行します。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[監査スクリプトと記録した出力](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-57973-audit)。コードと結果はMITライセンスです。暗号文とcribは引用であり、ライセンスの対象外です。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

Gromark型の主張をするなら、まず、見る前に決めたどの規則がprimerと経路を与え、どの未公開文字を予測するのかを示すべきです。

## 出典

- K4暗号文：Jim Sanborn, *Kryptos*（1990）。公開された転記：[Wikipedia「Kryptos」](https://en.wikipedia.org/wiki/Kryptos)、[Elonka DuninのKryptosページ](https://elonka.com/kryptos/)。
- crib：[WIRED、2010年11月21日](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED、2014年11月20日](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR *All Things Considered*、2020年1月30日（[transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)）、`EAST` は[Elonka Duninのarchive](https://elonka.com/kryptos/)の記録。
- 監査した仮説：2026-09-18にこのプロジェクトへ渡された研究引き継ぎ資料。これは[matbalez, *Kryptos K4: comprehensive research handoff and restart plan*, GitHub gist, 2026](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0)に基づいています。ここでは数値主張だけを再掲しています。
