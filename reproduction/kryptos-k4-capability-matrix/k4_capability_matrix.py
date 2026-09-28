"""The capability coverage matrix of EP-0142: which abstract capabilities the recorded tests
covered, read from results/capability-matrix-20260928.csv (one row per catalogue family or EP;
no K4 data, no K4 test).  Standard library only.

Columns (values in Japanese, as recorded; '|' joins several values):
  unit   文字 letter / 塊2, 塊3, 塊, 位置の対 block / 語 word / 可変長 variable / 全文 whole text
  state  なし none / 位置 position / 平文履歴 plaintext history / 暗号文履歴 ciphertext history /
         外の状態 external state (machines)
  sync   厳密 exact / eN up to N crib errors / 1回のずれ one slip / cribごと per crib / 2回以上 two or more slips
  verdict 閉 closed / 除 excluded / 不 undecidable / 未 untested / 済 done / STOP
  chrono あり existed at encryption / 計画値 planned value / 施工後 only after installation
  origin Scheidt / Sanborn / 施工 installation / 復号後 after decryption / なし none (constructed)
"""
import csv
import itertools
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
UNITS = ["文字", "塊", "語"]
STATES = ["なし", "位置", "平文履歴", "暗号文履歴", "外の状態"]
SYNCS = ["厳密", "誤り", "1回のずれ", "cribごと", "2回以上"]
EN = {"文字": "letter", "塊": "block", "語": "word", "なし": "none", "位置": "position",
      "平文履歴": "plaintext history", "暗号文履歴": "ciphertext history", "外の状態": "machine state",
      "厳密": "exact", "誤り": "errors", "1回のずれ": "one slip", "cribごと": "per crib", "2回以上": "2+ slips"}


def rows():
    with open(HERE / "results" / "capability-matrix-20260928.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def unit_class(u):
    return {"塊2": "塊", "塊3": "塊", "塊": "塊", "位置の対": "塊", "文字": "文字", "語": "語"}.get(u)


def sync_class(s):
    return "誤り" if s.startswith("e") else s


def closed(v):
    return any(x in ("閉", "除") for x in v.split("|"))


def cube(rs):
    """(unit, state, sync) -> ids of rows that closed or excluded it, and of rows that touched it only."""
    cov, part = defaultdict(list), defaultdict(list)
    for d in rs:
        if "—" in (d["unit"], d["state"], d["sync"]):
            continue
        us = {unit_class(u) for u in d["unit"].split("|")} - {None}
        for u, s, y in itertools.product(us, d["state"].split("|"), {sync_class(x) for x in d["sync"].split("|")}):
            (cov if closed(d["verdict"]) else part)[(u, s, y)].append(d["id"])
    return cov, part


def tallies(rs, col):
    c = Counter()
    for d in rs:
        for v in d[col].split("|"):
            c[v] += 1
    return c


def two_slips_inside_both_cribs(n=97, crib1=13, crib2=11):
    """Chance that two slips at random places fall one inside each crib, so that neither crib
    stays whole on one side (the part of two or more slips the per-crib test does not cover)."""
    gaps = n - 1
    return 2 * ((crib1 - 1) / gaps) * ((crib2 - 1) / gaps)
