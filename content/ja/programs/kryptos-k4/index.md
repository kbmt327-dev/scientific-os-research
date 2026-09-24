---
title: Kryptos K4
description: Jim Sanbornの彫刻Kryptosの未解読部分K4を、監査を優先して調べる研究の概要です。
lang: ja
---

K4は、Jim Sanbornが1990年にCIA本部へ設置した彫刻 *Kryptos* の第4部で、97文字の暗号文です。平文のうち24文字（`EASTNORTHEAST` と `BERLINCLOCK`）が公開されています。2025年に平文が資料の中から見つかりましたが、公開されておらず、暗号化の方法も明かされていません。正解は存在し、伏せられている状態です。

この研究はK4を解いたとは主張しません。公開された証拠でどの暗号の族を否定できるか、主張されたパターンが、探した側の自由度を払った後にどれだけの価値を持つか、そしてcribではそもそも答えられない問いはどれかを記録します。

## 問い

97文字の暗号文と24文字のcribで、どの仕組みを否定できるか。見つけるのに使った自由度を数えた後で、生き残るパターンはどれか。

## 証拠の種類

使うのは公開された暗号文とcribだけです。Noteで事前封印を明記していない検定は、すべて探索的です。「否定」は、述べた範囲のどの設定もcribを再現せず、しかも陽性対照（既知の鍵で作った暗号文）で検定が当たりを見つけられることを確かめた、という意味です。「区別できない」は、族の自由度が24文字で拘束できる量を超えているという意味で、否定ではありません。

## これまでに調べた族（2026-09-24時点）

内部記録の要約です。現在、公開の再実行があるのはNoteへのリンクがある行だけです。

| 族 | 結果 |
|---|---|
| 単一alphabetの周期鍵（周期1–96） | 検定できる49周期すべてで否定。残りは、同じ剰余に入るcrib文字の組がない周期 |
| 剰余ごとに任意alphabetの周期鍵（周期24以下） | cribまたは列の文字統計で否定 |
| 英語のrunning key全般 | 族として否定 |
| progressive鍵・Gromark型の差分鍵 | 否定。任意alphabetのGromarkは区別できない |
| 並べ替えだけの方式（転置・経路・折り） | 否定。K4の文字数の分布は英語になりえない |
| 鍵付き列転置、K3型の回転（それぞれ周期鍵と組み合わせ） | 候補なし |
| Hill（n=2–4）と転置、単語cubeのTrifid | 候補なし |
| 出力が25記号以下の方式 | K4は26文字すべてを使うので不可能。Wが素通りでもPlayfairは不可能（[Note](/ja/research/kryptos-k4-w-brackets/)） |
| 単語鍵の二層重ね | 1.4×10¹⁰通りで候補なし |
| Wを空文字・鍵の再始動点・ブロック境界・25文字暗号の素通り記号とみなす読み | 候補なし（[Note](/ja/research/kryptos-k4-w-brackets/)） |
| 行転置と周期鍵 | シャッフル対照と区別できない |

W区間を `TOKIO`（Tokyoのドイツ語綴りで、ベルリンの世界時計に刻まれている）と読むのは、凍結した外部の標的リストに対して通った唯一のパターンです（p ≤ 1.5×10⁻³、[Note](/ja/research/kryptos-k4-tokio-price/)）。暫定であり、平文は1文字も出ていません。

この研究は、K4はprimer 57973の反転Gromark暗号だという主張の監査から始まりました。数値は再現しますが、公開cribではそれを偶然と区別できません（[Note](/ja/research/kryptos-k4-57973-audit/)）。

<!-- GENERATED: program-current:START -->
## 現在の公開結論

復号はしていません。新しい平文文字は0です。EP-0057は「5つのWのうち2つが公開cribを外側から挟む」という観察を再現しましたが、Wという文字を選ばなければ確率は0.036で、W区間のTOKIO読みとも独立ではありません。Wを空文字・鍵の再始動点・ブロック境界・25文字暗号の素通り記号とみなす読みは、どれも候補を出しませんでした。

**証拠の境界：** 公開暗号文と24文字のcribだけを使った探索的な計算です。事前登録はなく、外部の独立replicationも暗号専門家のレビューもありません。正解は存在しますが公開されていません。

**[現在のResearch Note（EP-0057）を読む →](/ja/research/kryptos-k4-w-brackets/)**
<!-- GENERATED: program-current:END -->

<!-- GENERATED: program-history:START -->
## 公開中のResearch Note

1. [[ja/research/kryptos-k4-57973-audit/index|EP-0001 — modelの自由度を数えても、primer 57973は際立つか]]
2. [[ja/research/kryptos-k4-tokio-price/index|EP-0011 — K4のWをTOKIOと読むことには、どれだけの価値があるか]]
3. **[[ja/research/kryptos-k4-w-brackets/index|EP-0057 — K4の2つのcribを挟むWは、構造を持っているか]]（最新）**
<!-- GENERATED: program-history:END -->

## 出典

Jim Sanborn, *Kryptos*（1990）。暗号文は[Wikipedia](https://en.wikipedia.org/wiki/Kryptos)と[Elonka Dunin](https://elonka.com/kryptos/)の転記による。cribの公開：[WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/)、[WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/)、NPR 2020（[transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)）、`EAST` は[Elonka Duninのarchive](https://elonka.com/kryptos/)。Sanbornの2025年のヒント：[Scientific American](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/)。2025年の資料での発見：[RR Auction](https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/)。暗号文とcribは研究と論評のための引用であり、このサイトのライセンスの対象外です。
