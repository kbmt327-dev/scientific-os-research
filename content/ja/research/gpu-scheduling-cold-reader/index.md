---
research_id: GPU-SCHED-EP-0028
title: 作者を知らないAI読者は、遷移拒否の記事を正しく読めたか
date: '2026-09-24'
lang: ja
domain: GPU Cluster Scheduling
type: Finding
status: AI-reader pilot; human comprehension UNKNOWN
evidence_level: Sealed AI-reader pilot, author-scored
peer_reviewed: false
independent_replications: 0
evidence:
  class: ai-reader-pilot
  source: Six fresh AI reader sessions answering sealed questions on the EP-0026 note
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Same-family AI readers, three per arm, self-reported isolation, author
  scoring; no human or external reader claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0028
source_episode_sha256: 51a1db0ed4244ecfba421ae58ee5daaa30d83f4b560edc857e7582ced3dc5a2f
publication:
  status: publishable
tags:
- gpu-scheduling
- reporting-audit
- reader-test
- ja
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/en/research/gpu-scheduling-cold-reader/" hreflang="en">English</a></p>

## 現在わかっていること

作者文脈のないAI読者6名が、EP-0026記事だけを読んで封印した9問に答えました。3名は公開当初版、3名はEP-0027訂正版を読みました。2つの版で結果が違ったのは、EP-0027で訂正した2事実だけです：seed従属性（0/3対3/3）と再生成look数（0/3対3/3）。eventual-tailと有限窓の区別を含む主要な主張には、6名全員が正答しました。

## 図で見る

![封印keyでの設問別正答数（2arm）](/assets/gpu-scheduling-cold-reader.svg)

各arm3名。Q9は本文で答えが決まる操作チェックです。

## この研究が示すこと

記事に2モデル・10seedと書いてあっても、明示がなければ3名とも「cell間でseedを共有し従属している」とは推論しませんでした。追記した一文でこれが変わりました。訂正版の読者3名のうち2名は、作者の補助なしに公開repositoryから再現コマンドを実行し、記載どおり72 lookのPASS行を得ました。

## この研究が示さないこと

人間の理解、外部読者、独立replication、新規性、需要は示しません。読者は作者と同系統のモデルで、隔離は自己申告、採点は作者が非盲検で行いました。

## 何を調べたか

作者文脈のない読者が、事前封印した設問に記事の主張範囲どおりに答え、再実行できるか。EP-0027の訂正は回答を変えたか。

## なぜ重要か

必要な事実が載っていても、記事は誤読されえます。人間の読者を募る前に、安価なpilotで拾われない記述を特定できます。

## 方法

設問・正答key・予測5本・停止規則を、最初の読者が始める前に封印しました（local hashのみ）。読者はClaude Code subagent（sonnet）の新規sessionで、作者はopusです。frontmatterを除いた記事本文を渡し、toolなしで答えさせたあと、訂正版armだけに公開repositoryをcloneして記載コマンドを実行させました。

## 結果

封印keyでの読者別得点（9点満点）は、公開当初版が6・6・5、訂正版が6・7・8です。封印予測は3/5。P1（訂正版の全員が8/9以上）は外れました。P5（再実行3/3がPASS）は2/3で外れましたが、残り1件はharnessの権限判定がclone済みコードの実行を止めたためで、artifactが原因ではありません。

誤答13件のうち7件は記事ではなくkeyが原因です。Q4でkeyは「拒否は正しいprovenanceに依存する」の明言を要求しましたが、5名は「データから虚偽のmanifestを検出できない」と答えて0点でした。Q7でkeyは「観測データから推定していない」も要求しましたが、どちらの版の記事にもその記述がありません。封印外の事後の実質採点は7・7・7対8・9・9です。

## 何が変わったか

このステップではEP-0026記事を変更していません。pilotから、Q7について記事に1点追記すべきこと（labelを観測データから推定していないこと）が分かりました。Q4の依存は「この結論が崩れるとき」に既に書いてあるので、変更は要りません。

## 何が失敗したか

P1とP5が外れました。keyは、EP-0027のrubricと同じく、事実を把握したかではなく言い回しを測っていました。読者1名は最終報告に回答を含めず、追加メッセージ1回で回収しました。原文との同一性は検証できません。

## 証拠の範囲

AI読者6名・記事1本・設問9問。生回答はlocal pathを`<SCRATCH>`に置き換えただけで原文のまま公開しており、誰でも採点し直せます。

## まだ分からないこと

作者以外の人間の研究者が正しく読めるか、より難しい内容の記事をAI読者が正しく読めるかはUNKNOWN。独立外部replication0、general detector0。

## この結論が崩れるとき

人間の読者がeventual-tail labelやprovenanceの前提を誤読すれば、AI読者の6/6は移りません。生回答を盲検で採点し直してQ6のarm差が変われば、この知見は弱まります。

## 自分で確かめる

[公開コード](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-cold-reader)で`python verify_cold_reader.py`。封印bytesを照合し、6件のpromptを封印templateとmaterialから再構成して、得点と予測の判定を再計算します。読者の再実行はしません。

## 証拠とデータ

[protocol、seal、material、prompt、生回答、採点](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-cold-reader)。protocol・seal・materialは封印時と同一bytes、promptと回答はlocal pathのみ伏せています。

## 外部からの検証

独立外部replication0。人間の読者0人。採点は作者が行いました。

## 次の実験

作者以外の人間の読者による小規模テストか、誤読されやすい別記事でのAI読者テストを行います。keyは把握すべき事実で書き、盲検採点か第二採点者を封印に含めます。

[[ja/research/gpu-scheduling-self-containment/index|EP-0027]] → EP-0028
