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

## これまでに調べた族（2026-09-25時点）

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
| 周期鍵のあとの7×7回転グリル2枚 | 2.09×10¹⁰通りで候補なし |
| 波の帯で読む経路、正弦波の強度そのものを鍵にする形 | 候補なし |
| 固定点をもたない装置（反射板つきEnigma、M-94・M-138-Aの円盤とストリップ、HC-9） | 平文と暗号文の位置が一致するなら不可能。cribの中に S→S と K→K の自己暗号化がある |
| Hagelin M-209（重なりのないラグ籠、標準の定数） | cribには合うが、残り73文字は英語にならない。cribに合う籠の多さは、シャッフル対照と区別できない（p≈0.06） |
| Hagelin CX-52（規則歩進） | 標本の範囲では、cribで区別できない |
| 銅板を珪化木に巻き、重なった層の文字を鍵にする | 候補なし（一周は写真から19〜25列と測った） |
| 高さによらない物理鍵（表面の向き、弧に沿った距離など） | 形を測らずに否定。同じ列に来るcribの組（位置32と63、33と64）が同じ鍵を要求し、どの規約でも成り立たない |
| 平文をMorseにして3記号ずつ文字にする形、Berlin Clockを1文字ずつ進めて点灯数を鍵にする形、継ぎ目で折る・鏡に映す重ね方、裏から読む順 | 候補なし |
| 影の縁が文字を横切る時刻、立ち位置から見たtableauとの重なり（隣り合う文字で鍵が滑らかになるかで判定） | K4のcrib上の鍵は無作為な鍵と同じくらい粗く、こうした滑らかな鍵とは合わない |
| 3D模型の形の範囲全体で：穴越しに見える奥の文字、日が当たり始める／終わる時刻、決まった点からの距離 | cribに合う設定なし。最高点はシャッフル対照と区別できない |

W区間を `TOKIO`（Tokyoのドイツ語綴りで、ベルリンの世界時計に刻まれている）と読むのは、凍結した外部の標的リストに対して通った唯一のパターンです（p ≤ 1.5×10⁻³、[Note](/ja/research/kryptos-k4-tokio-price/)）。暫定であり、平文は1文字も出ていません。

この研究は、K4はprimer 57973の反転Gromark暗号だという主張の監査から始まりました。数値は再現しますが、公開cribではそれを偶然と区別できません（[Note](/ja/research/kryptos-k4-57973-audit/)）。

## 彫刻の物理記録と3D模型（2026-09-25）

鍵が文字ではなく彫刻そのものの形から来る可能性を調べるため、公開写真と航空写真から、彫刻の物理的な情報を推定して3D模型にしました（v0.5）。銅板の組み方（4枚が2×2で、横の継ぎ目がK2とK3の境と一致）、S字の形、方位（暗号文側がおおむね南）、珪化木の太さ、入口のMorse（K0）が刻まれた3つの石の配置を含みます。ラングレーの日付と時刻を選ぶと、太陽の位置から、切り抜いた文字の光が床に落ちる様子を見られます。

v0.5では、写真の文字にカメラと円筒を当てはめて列の間隔を測り直し、両端の間が公表の幅20 ft（6.1 m）になるようにしました。入口のMorseの穴は写真で測った比率で描き、コンパス図の向きも写真から測り直しました。画面は日本語と英語を切り替えられ、模型をglTF（.glb）で、K4の97文字の物理量をCSVで保存できます。

寸法と方位のほとんどは推定（確度C）で、目安です。模型の形はcribを見ずに写真だけで決めました。研究用の計算は、形の不確かさの範囲（半径1.4〜2.4 mなど）全体で回しています。公開版では、K4の97文字とMorseの7句のほかは彫刻の文字を伏せ、切り抜きの位置だけを示しています。

**[3D模型を開く →](https://kbmt327-dev.github.io/scientific-os-research/static/kryptos-k4-model.html)**（日本語／English）

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
