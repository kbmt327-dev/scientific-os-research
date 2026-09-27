"""Write results/classical-20260927.json (the author's recorded run for this package)."""
import json

import k4_classical as C

settings = {}
for a, al in C.ALPHABETS.items():
    for f in C.FORMS:
        k = C.keystream(al, f)
        settings[f"{a} {f}"] = {"keystream": list(C.keystream_text(al, f)),
                                "periodic_survivors": C.periodic_survivors(k),
                                "difference_survivors": C.difference_survivors(k),
                                "english_running_key_share": C.english_running_key_p(k, al, 20000)}
rec = {
    "source": "rechecked 2026-09-27 for the Note; internal records EP-0032 (2026-09-20), EP-0018-0020, EP-0051-0056",
    "testable_periods": C.testable_periods(), "settings": settings,
    "transposition_share_as_flat_as_k4": C.transposition_p(20000), "k4_distinct_letters": len(set(C.K4)),
    "recorded_not_rerun": {
        "EP-0053 periodic key with a free alphabet per residue, p <= 24 (with column letter statistics)":
            "rejected by the cribs or the column statistics",
        "EP-0020 free transposition then English running key (9,442 settings)": "rejected",
        "EP-0051 keyed columnar transposition and K3-style rotation, each with a periodic key":
            "no candidate (177 cells unfinished)",
        "EP-0052 Hill n = 2-4 with transposition; Trifid with word cubes": "no candidate",
        "EP-0052 ciphers with 25 or fewer output symbols; Porta": "impossible (K4 uses 26 letters; S->S and K->K)",
        "EP-0054 two stacked keyword layers (1.4e10 settings)": "no candidate",
        "EP-0053 row transposition with a periodic key": "not distinguishable from shuffled controls",
        "EP-0059 periodic key followed by two 7x7 turning grilles (2.09e10)": "no candidate",
        "devices with no fixed points (Enigma with reflector, M-94, M-138-A, HC-9)":
            "impossible if positions coincide: S->S at 32, K->K at 73"}}
with open("results/classical-20260927.json", "w", encoding="utf-8") as fh:
    json.dump(rec, fh, indent=1)
