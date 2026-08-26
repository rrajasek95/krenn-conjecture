#!/usr/bin/env python3
"""AUDIT A4 / CHECK 04 -- CLAIM 2 (Theorem W12-B) and CLAIM 6 (the sweep).

Independent extractor a4_cut.py.  Targets: the m=20 survivor, W8's nine
immunity templates, >= 10 W11 witnesses, >= 5 W8 m=17 classes.
"""
from __future__ import annotations

import glob
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")
W11 = os.path.join(ROOT, "computations", "unaudited-sat-pair-w11-2026-08-15")
import a4_engine as E    # noqa: E402
import a4_cut as CUT     # noqa: E402

N = 8
out = {}


def load_w11():
    res = []
    for path in sorted(glob.glob(os.path.join(W11, "witnesses", "*.json"))):
        if os.path.basename(path) == "summary.json":
            continue
        with open(path) as fh:
            d = json.load(fh)
        occ = set()
        tmpl = E.Template(N, ())
        for e, cells in zip(d["edges"], d["blocks"]):
            k = tmpl.eidx[tuple(sorted(e))]
            for (i, j) in cells:
                occ.add((k, i, j))
        res.append((os.path.basename(path)[:-5], E.Template(N, occ)))
    return res


def load_m17():
    with open(os.path.join(W8, "results_enumerate_m17.json")) as fh:
        d = json.load(fh)
    return [(f"m17_class{k}", E.Template.from_masks(c["template"]))
            for k, c in enumerate(d["classes"])]


with open(os.path.join(W8, "results_close_m20.json")) as fh:
    SURV = E.Template.from_masks(json.load(fh)["survivors"][0])
with open(os.path.join(W8, "results_immunity.json")) as fh:
    IMM = [(f"immunity_m{e['m']}", E.Template.from_masks(e["template"]))
           for e in json.load(fh)["results"]]
W11T = load_w11()
M17T = load_m17()
print(f"targets loaded: survivor + {len(IMM)} immunity + {len(W11T)} W11 "
      f"+ {len(M17T)} m17 classes = {2 + len(IMM) + len(W11T) + len(M17T) - 1}")
out["target_counts"] = {"immunity": len(IMM), "w11": len(W11T),
                        "m17": len(M17T)}

rng = random.Random(1234)
SPOT_W11 = sorted(rng.sample(range(len(W11T)), 12))
SPOT_M17 = sorted(rng.sample(range(len(M17T)), 7))
out["spot_w11_indices"] = SPOT_W11
out["spot_m17_indices"] = SPOT_M17

TARGETS = ([("survivor_m20", SURV)] + IMM
           + [W11T[k] for k in SPOT_W11] + [M17T[k] for k in SPOT_M17])

rows = []
for name, T in TARGETS:
    t0 = time.time()
    verdict, recs = CUT.cut_kill(T, timeout=120)
    dt = time.time() - t0
    hit = next((r for r in recs if r["verdict"] == "killed"), None)
    rows.append({"name": name, "m": T.m(), "sigma": T.sigma(),
                 "verdict": verdict, "seconds": round(dt, 2),
                 "kill": hit, "n_records": len(recs)})
    print(f"{name:22s} m={T.m():2d} S={T.sigma():3d} -> {verdict:9s} "
          f"({dt:5.1f}s)"
          + (f"  L={hit['L']} side={hit['side']} :: {hit['reason']}"
             if hit else ""))
out["targets"] = rows
out["n_killed"] = sum(1 for r in rows if r["verdict"] == "killed")
print(f"\nKILLED {out['n_killed']} / {len(rows)}")

with open(os.path.join(HERE, "results_chk04.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote results_chk04.json")
