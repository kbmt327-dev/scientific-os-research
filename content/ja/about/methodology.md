---
title: 公開方法
description: 内部Episodeをpublic Research Noteへ変換する方法。
lang: ja
---

公開は自動copyではなく、fail-closedなprojectionです。

1. 内部Episodeを選び、識別子とSHA-256 digestを固定する。
2. private pathや無関係な内部contextをコピーせずpublic noteを作る。
3. 結果前の予測と、結果後の解釈を分ける。
4. 証拠が支持することと、支持しないことを書く。
5. 現時点で正直に示せる最短の再現経路を公開する。未公開ならその旨を書く。
6. schema、必須section、link、secret、private pathを検査する。
7. 実siteをbuildし、desktopとmobileで確認する。
8. public repositoryの検査が通った後だけ公開する。

現在のPublication Compilerは空のprojection skeletonを生成し、完成済みnoteを検証します。主張の要約や科学的な公開可否は自動決定せず、人間判断に残しています。
