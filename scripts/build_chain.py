#!/usr/bin/env python3
"""Rewrite the shared revision chain in every GPU-scheduling Research Note.

The chain is the point of this series: each entry is a study that changed or
retracted something the one before it published. Keeping it by hand across 13
notes in two languages is how it goes stale, so it is generated from one list.

Usage: python scripts/build_chain.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# slug, EP label, one-line JA summary, one-line EN summary
CHAIN = [
    ("gpu-scheduling", "EP-0001",
     "推定誤差と再実行コストで、最良の方式が入れ替わる。",
     "Estimate error and restart cost swap which policy is best."),
    ("gpu-scheduling-phase-diagram", "EP-0002",
     "平均は良いのに、一部のジョブクラスが終わらない。安定性の判定器も3回壊れた。",
     "Good averages hide a job class that never finishes. Three stability detectors broke."),
    ("gpu-scheduling-starvation-mechanism", "EP-0003",
     "飢餓を決めるのは平均ジョブ幅ではなく、クラスタ全体を要するジョブの有無。",
     "Starvation is set by whether whole-cluster jobs exist, not by mean gang size."),
    ("gpu-scheduling-real-traces", "EP-0004",
     "実測したプールにその条件はなく、害は飢餓ではなく数倍の遅れだった。",
     "Measured pools never meet that condition; the harm is a multiple, not starvation."),
    ("gpu-scheduling-pool-size", "EP-0005",
     "安全境界はプールが大きいほど下がる。実規模の害は2倍過小評価だった。",
     "The safe ratio falls as the pool grows; the harm at real scale was underestimated."),
    ("gpu-scheduling-concurrency", "EP-0006",
     "効いていたのはプールの大きさではなく、同時に取り合うジョブの本数だった。",
     "The driver was never pool size. It is how many jobs compete at once."),
    ("gpu-scheduling-real-cluster-position", "EP-0007",
     "実クラスタの位置で測り、4本ぶん載せてきた機構説明を訂正した。",
     "Measured at the real cluster's position, and corrected a mechanism claim carried for four studies."),
    ("gpu-scheduling-headline-broken", "EP-0008",
     "背景の粒度を変えるだけで、この研究の看板結論が消えた。",
     "Changing only the granularity of the background made the headline result disappear."),
    ("gpu-scheduling-phase-reaxis", "EP-0009",
     "代表成果だった相図の軸そのものが、18倍交絡していた。",
     "The axis of the flagship phase diagram was confounded by a factor of 18."),
    ("gpu-scheduling-third-variable", "EP-0010",
     "「2つの数で決まる」を撤回した。頻度が第三の変数だった。",
     "Retracted \\\"two numbers decide this\\\". Frequency is a third variable."),
    ("gpu-scheduling-blind-detector", "EP-0011",
     "判定器が発散を測っていなかった。窓で割っていたので、値が動かなかった。",
     "The detector was not measuring divergence. It divided by the window, so it never moved."),
    ("gpu-scheduling-alpha-boundary", "EP-0012",
     "動かない境界を持つ統計量へ置き換え、運用数値を戻した。",
     "Replaced it with a statistic whose boundary stays put, and restored the numbers."),
    ("gpu-scheduling-one-job", "EP-0013",
     "実クラスタについての主張は、19,100本中1本のジョブに乗っていた。",
     "The real-cluster claim rests on one job out of 19,100."),
]

BLOCK = re.compile(
    r'<div class="revision-chain vertical".*?</div>', flags=re.DOTALL)


def render(lang: str, current: str) -> str:
    label = ("GPUクラスタのスケジューリング研究の更新履歴"
             if lang == "ja" else
             "revision history of the GPU cluster scheduling research")
    lines = [f'<div class="revision-chain vertical" aria-label="{label}">']
    for slug, ep, ja, en in CHAIN:
        summary = ja if lang == "ja" else en
        if slug == current:
            marker = f"{ep} · 現在地" if lang == "ja" else f"{ep} · current"
            lines.append(
                f'  <a class="current" href="/{lang}/research/{slug}/">'
                f'<b>{marker}</b><span>{summary}</span></a>')
        else:
            lines.append(
                f'  <a href="/{lang}/research/{slug}/">'
                f'<b>{ep}</b><span>{summary}</span></a>')
    lines.append("</div>")
    return "\n".join(lines)


def main() -> int:
    changed = 0
    for lang in ("ja", "en"):
        for slug, *_ in CHAIN:
            path = ROOT / "content" / lang / "research" / slug / "index.md"
            if not path.exists():
                print(f"  skip (not written yet): {path.relative_to(ROOT)}")
                continue
            text = path.read_text(encoding="utf-8")
            block = render(lang, slug)
            if BLOCK.search(text):
                new = BLOCK.sub(lambda _: block, text, count=1)
            else:
                print(f"  no chain block in {path.relative_to(ROOT)}")
                continue
            if new != text:
                path.write_text(new, encoding="utf-8", newline="\n")
                changed += 1
    print(f"revision chain rewritten in {changed} note(s); "
          f"{len(CHAIN)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
