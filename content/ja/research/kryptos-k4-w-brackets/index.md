---
research_id: KRYPTOS-K4-EP-0057
title: K4の2つのcribを挟むWは、構造を持っているか
date: '2026-09-24'
lang: ja
domain: Kryptos K4
type: Finding
status: Observation reproduced; significance downgraded; four readings gave no candidate
evidence_level: Exploratory computation on public ciphertext; not preregistered
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; exact nulls, shuffled-text controls and planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One post hoc observation about W positions in K4 and four cipher families
  built from it; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0057
source_episode_sha256: 0b4f31e6f22ce59f2d590e59e5bf5b5033808acd5df70a98b9fba8382bcfb09a
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- ja
---

<p class="research-area"><b>Kryptos K4</b><a href="/en/research/kryptos-k4-w-brackets/" hreflang="en">English</a></p>

## 現在わかっていること

K4にはWが5つあり、位置は0始まりで20・36・48・58・74です。位置20のWは `EASTNORTHEAST`（21–33）の直前に、位置74のWは `BERLINCLOCK`（63–73）の直後にあります。どちらのcribも、Wに挟まれた15文字の区間2つに収まっています。ここまでは厳密に再現しました。ただし、Wという文字は見た後に選ばれています。文字を固定しなければ、位置20と74が同じ文字になる確率は0.004ではなく0.036です。また、この観察は、W区間の既存の読み `TOKIO` を独立に支える証拠にもなりません。「Wは構造だ」という前提から作った4つの暗号は、どれも復号候補も新しい平文文字も出しませんでした。

## 図で見る

![K4の97文字：5つのW、長さ20・15・11・9・15・22の6区間、15文字の区間に入る2つのcrib](/assets/kryptos-k4-w-brackets.svg)

1マスが暗号文1文字です。区間長を文字に直す（A=1）と T O K I O V になります。

## この研究が示すこと

- 観察に書かれた事実は正しいです。ただし、各cribを挟んでいるのは片側だけです。`NORTHEAST` の後ろには2文字、`BERLIN` の前には4文字があり、その先にWがあります。
- 観察に書かれた確率0.004は、「位置20と74、または34と62がどちらもW」の厳密値（0.0043）に当たります。20と74だけなら0.0021です。「cribに接する4セルのうち2つ以上がW」は、0.02ではなく0.012です。
- Wという文字を選んだこと自体が、見た後の選択です。文字を固定しない場合、確率は0.036（20と74が同じ文字）、または0.071（外側どうしか内側どうしが同じ文字）です。
- `TOKIO` の読みが正しければ、W位置は区間長からすべて決まります。したがってこの観察が述べているのは公開されたcribの位置のことであり、`TOKIO` の証拠と掛け合わせることはできません。
- Wを構造とみなす4つの読みは、試した族ではどれも否定されました（結果を参照）。

## この研究が示さないこと

Wが偶然だとは示しません。鍵の位置ごとに任意の換字alphabetを許す族は、24文字のcribでは区別できないので、否定していません。何も復号していません。

## 何を調べたか

「Wが2つの公開cribを挟んでいる」という観察がこのプロジェクトに寄せられました。これは再現するか、どれくらい珍しいか。Wが設計者の置いた構造だとしたら、どんな単純な暗号が導かれ、それはcribと両立するか。

## なぜ重要か

K4には、見た後に見つかるパターンが多く寄せられます。この研究は、そうしたパターンを信じる前に払うべき3つの値段を示します。文字を選べた自由度、同じ位置についての先行する読みへの従属、そしてそのパターンから作った暗号が既知平文と両立するかどうかです。

## 方法

- **厳密なnull。** 5つのWを97セルに一様に置きます。文字を固定しない版は、K4自身の文字数を使います。
- **B. Wは挿入された空文字。** Wを除いた92文字に、周期鍵・progressive鍵・暗号文／平文autokeyを当てます。方式はVigenère・Beaufort・variant Beaufort、alphabetはA–ZとKRYPTOSです。
- **C. Wごとに鍵が最初に戻る。** 2つのcribはどちらも「O」の区間にあります。鍵が区間の文字と区間内の位置だけで決まるなら、2つのcribは同じ鍵列を持つはずです。共有する9か所で検定します。
- **D. 6つの区間はブロック。** 並べ替え720通り × 反転64通り × 区切り枠の有無で、平文位置に周期46以下の周期鍵を当てます。対照は、K4のW以外の文字を並べ替えたもの3本です。
- **E. Wは素通りし、残りは25文字の暗号。** W抜きのA–Z・KRYPTOS alphabetで、mod 25の周期鍵・progressive鍵・暗号文autokeyを当てます。Playfairには「文字が自分自身に暗号化されない」という性質を使います。

どの検定にも、K4を読まない陽性対照（既知の鍵で作った暗号文）を付けています。作者の作業用repositoryでは、コードをコミットしてからK4に適用しました（履歴は非公開なので、作者の申告として扱ってください）。事前登録はしていません。

## 結果

| 読み | K4 | 対照 | 判定 |
|---|---|---|---|
| B. Wは挿入された空文字 | crib位置どうしで剰余が重ならない周期（25, 26）でだけ両立 | 陽性対照18/18を回収 | 否定 |
| B′. 剰余ごとに任意alphabet | 26周期で両立 | — | 区別できない |
| C. Wごとに鍵が再始動 | 加法鍵は共有9か所中1–2か所で一致（偶然の期待値は約0.35か所） | 陽性対照6/6で9/9 | 否定 |
| C′. 位置ごとに任意の換字 | 違反なし。ただし情報のある位置は1か所だけ | — | 区別できない |
| D. 区間を並べ替えたブロック | 92,160配置で通過0 | 陽性対照3/3。対照の通過はcrib制約1個だけのもの | 否定 |
| E. W素通り＋25文字暗号 | mod 25の鍵は0件（各設定で1件通るprogressiveは、位置21と73の制約1個だけ）。Playfairは、位置32（S）と73（K）でcrib文字が自分自身に暗号化されているので、どの正方形でも不可能 | 陽性対照8/8 | 否定 |

効いている論理が1つあります。区間の文字（T, O, K, I, O, V）で鍵をずらす方式は、2つのcribがどちらもO区間にあるので、どちらにも同じずらしを与えます。したがってcribの上では単なる周期鍵に帰着し、周期鍵はすでに否定されています。

## 何が変わったか

この観察は暫定の観察として記録し、仮説には昇格させません。このプロジェクトの以前の閉鎖（「K4は26文字すべてを使うので、25記号の暗号はすべて不可能」）には抜け道がありました。Wが素通りなら、残り92文字は25記号で足り、実際にちょうど残り25種です。Playfairは、この抜け道の側でも閉じました。

## 何が失敗したか

観察に書かれた「境界4セル中2つ以上」の確率0.02は再現しませんでした（厳密値は0.012）。最初の2つのprobeコミットには、並行セッションがすでに使っていたepisode番号を付けてしまい、後から振り直しました。

## 証拠の範囲

使ったのは公開暗号文と24文字のcribだけです。cribはSanbornがどの語を公開するか選んだもので、その位置は無作為標本ではありません。すべて探索的な検定で、述べた族の範囲では厳密です。

## まだ分からないこと

Wが意図して置かれたかどうか。W素通りの5×5 Bifid、Two-square、Four-squareがcribと両立するか。区間内の転置とブロック移動を組み合わせた形がどうか。外部の独立replicationは0件です。

## この結論が崩れるとき

否定した族のどれかでK4を公開cribへ変える暗号が見つかれば、否定は崩れます。そのときは下の再実行で不一致が出るはずです。見る前に決められる「Wを他の文字より優先する理由」があれば、0.004の一部が戻ります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-brackets)：`python verify_w_brackets.py` は、K4に関わる計算をすべて標準ライブラリだけで数秒で再実行し、記録した結果と照合して `PASS` を出します。作者のコードの再実行であり、独立replicationではありません。

## 証拠とデータ

[probeスクリプト、記録した結果、陽性対照](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-brackets)。コードと結果はMITライセンスです。暗号文とcribは引用であり、ライセンスの対象外です。

## 外部からの検証

外部の独立replicationは0件です。暗号の専門家によるレビューは受けていません。

## 次の実験

W素通りのBifid・Two-square・Four-squareと、区間内の転置とブロック移動の組み合わせ。

## 出典

- K4暗号文：Jim Sanborn, *Kryptos*（1990）、CIA本部（Virginia州Langley）。公開された転記：[Wikipedia「Kryptos」](https://en.wikipedia.org/wiki/Kryptos)、[Elonka DuninのKryptosページ](https://elonka.com/kryptos/)。
- crib：`BERLIN` は[WIRED、2010年11月21日](https://www.wired.com/2010/11/clue-kryptos/)。`CLOCK` は[WIRED、2014年11月20日](https://www.wired.com/2014/11/second-kryptos-clue/)。`NORTHEAST` はNPR *All Things Considered*、2020年1月30日（[transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)）。`EAST` は2020年8月にSanbornが確認したと[Elonka Duninのarchive](https://elonka.com/kryptos/)が記録しています。
- `BERLINCLOCK` がベルリンの世界時計を指すこと：[Scientific American、2025年](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/)。
- W区間の読み `20, 15, 11, 9, 15 → TOKIO`：[matbalez, *Kryptos K4: comprehensive research handoff and restart plan*, GitHub gist, 2026](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0)。
- 「Wがcribを挟む」という観察は、暗号文を見た後にこのプロジェクトへ寄せられたものです。原文は内部記録に保存しています。
