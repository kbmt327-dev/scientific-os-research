---
id: SIM-WORLD-EP-0001-JA
title: バッチ到着と不均質serverを盲検同定する
date: 2026-09-13
lang: ja
translation_of: SIM-WORLD-EP-0001
domain: Sim World / Queueing
type: Finding
status: 探索的
evidence_level: 合成blind benchmark
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-blind-benchmark
  source: 公開hidden-world generator、観測、sealed prediction、fitted simulator、reveal
review:
  peer_reviewed: false
  human_reviewed: true
replication:
  independent: 0
  failed: 0
claim_scope: 開示済みの有限mechanism family内にある1つのhidden instance
source_episode: SIM-WORLD/EP-0001
source_episode_sha256: 0c632eb5cad1431953bcbfbe3a067925fea3d7caac6bb21547ce53cb03a7931f
publication:
  status: publishable
tags: [finding, queueing, blind-benchmark, model-selection, japanese]
---

<p class="language-switch">English: <a href="/scientific-os-research/research/simulation-worlds/">Original Research Note</a></p>

<div class="evidence-strip"><span>Finding</span><span>合成blind benchmark</span><span>探索的</span><span>peer reviewなし</span><span>外部再現 0</span></div>

## 要約

hidden queueing worldでは、見かけ上のM/M/c baselineに対し、観測平均sojourn timeが解析予測の234倍で時間とともに増加しました。安価な検査で同時刻の幾何batchを特定し、server-level観測をsealed requestした後、不均質service rateと単一の誤ったnominal rateを区別しました。batch arrival・指数service・rateを一部tieした不均質server modelは、out-of-sample統計10個中8個を95%予測区間内に置き、最終的なhidden-world revealと一致しました。このbenchmarkが検査したのは既知mechanism family内の同定であり、未知の仮説空間の発見ではありません。

## 研究質問

予測不一致、必要な追加観測、sealed out-of-sample test、複製、model ladderを用いて、hidden simulated worldを説明する最小のqueueing modelを同定できるか。

## なぜ重要か

不一致の後に複雑性を加えるのは簡単です。このbenchmarkでは、まず安価な代替説明を除外し、新しい観測channelを要求する理由を示し、modelを拡張する前に残差を複製することを求めました。

## 競合仮説

候補族にはarrival process、service law、server構造、customer behaviorの代替を含めました。主な候補はabandonment／balking、congestion-dependent slowdown、batch arrival、誤った共通service rate、不均質server rate、非指数serviceでした。

## 予測

- **PRED-001：** 既存の同一runをobservation level 1から3へ上げる前にseal。強いserver-rate heterogeneityを含む6予測すべてが支持。
- **PRED-002：** 2つのout-of-sample条件前にseal。報告統計10個中8個が95%予測区間内。
- **PRED-003：** 1つの残差が新mechanismを要するか判定する8回の同条件複製前にseal。複製平均は区間内へ戻った。
- **FINAL-MODEL：** hidden worldをrevealする前にseal。

## 方法

worldは実行時に16-byte seedを生成し、seedとSHA-256 commitmentだけを保存しました。mechanismとparameterはseedから導出されます。Observation levelは段階的に情報を公開しました。最初はarrivalとdepartureだけで分析し、service start、server ID、exit reason、queue-length sampleは要求と6予測をsealした後にだけ追加しました。

Model ladderではnominal M/M/c、fitted-rate M/M/c、均質batch arrival、不均質batch-arrival modelを比較しました。選択modelは統計的に区別できない2つのserver rateをtieし、完全heterogeneous modelよりparameterを1つ減らしました。

## 結果

- Baseline M/M/4は平均sojourn `W=1.335`を予測したが、観測は`W=311.8`で線形増加。
- arrivalの49.5%が正確に同じtimestampを共有し、batch sizeは幾何分布に近かった。
- server rateは約`0.693 / 0.361 / 0.364 / 1.028`で、均質rate説明を棄却。
- parsimonious heterogeneous modelは予測区間hit 8/10、相対誤差median 0.102。
- revealした構造は宣言した5 componentすべてと一致。mean batch size誤差0.53%、server-rate最大誤差2.29%、`c=3,4,6`のcapacity誤差は0.3%未満。

## 何が変わったか

- cheap testでabandonmentとslowdownを除外した後、観測追加を1つのchannel upgradeに限定しました。
- 1 runのwaiting-time残差に対し、新mechanism追加ではなく複製を選びました。
- 近い2 rateはexact equalityと主張せず、経済的なtieとして表現しました。

## 何が失敗したか

初期analysisは、末尾の不完全time binを含めたためarrival epochをover-dispersedと報告しました。完全binと経験的Poisson nullを使うと見かけの効果は消えました。修正しなければ不要なmodulated／periodic arrival processを追加していました。

候補mechanism familyと割当規則は事前に与えられていました。hidden instanceはblindでしたが、仮説空間はblindではありません。

## 証拠境界

**支持されること：** 宣言済みの有限family内にある1つの合成hidden instanceを同定し、sealed predictionとout-of-sample check後の最終構造・parameterがrevealと一致した。

**支持されないこと：** open-world mechanism discovery、実queueでの性能、hidden seed間の一般性、benchmark designerとresearcherの独立性。

## UNKNOWN

- 独立に拡張されたmechanism familyでも同じ手順が成功するか。
- 観測windowが10分の1のときの検出力。
- heterogeneous serverとcongestion-dependent slowdownなど複数逸脱が相互作用するときの識別可能性。
- 新しいhidden seed、独立researcherへの一般化。

## 反証条件

- 同じfamilyの新しいsealed seedで誤った構造を繰り返し選ぶ。
- 高load条件のcapacityがfitted rate総和と一致しない。
- server identityのpermutationで予測rate trackingが壊れる。
- 独立再解析でseedまたはrevealからpredictionへのleakを発見する。

## 再現

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick queue
```

新しいblind run全体を行う場合は新sealを生成し、final modelをsealするまでanalystに`reveal`を渡さないでください。同梱した完了runは公開計算を再現できますが、revealが公開済みなのでblindではありません。

## 証拠 / Artifacts

- [World generatorとobservation data](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/simulation-worlds)
- [Sealed predictions](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/simulation-worlds/predictions)
- [Analysis ladder](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/simulation-worlds/analysis)
- Hidden-world commitment：`7c4e47709de366e295aec26be7fac462100d1c6bf3d49fcd9ec03e40930b663a`
- 内部source Episode digest：`0c632eb5cad1431953bcbfbe3a067925fea3d7caac6bb21547ce53cb03a7931f`

## 外部監査

- 独立再現：0
- 再現失敗：0
- 公開後に確認されたbug：0
- 未解決critique：0

## 次の実験

独立processにmechanism familyを拡張してもらい、複数のsealed instanceを作り、truthやfamily-construction logicをanalystへ共有せず構造回復を評価します。
