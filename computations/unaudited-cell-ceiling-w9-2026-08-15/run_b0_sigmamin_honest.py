#!/usr/bin/env python3
"""W9 Task B0 -- honest Sigma_min(m) at N=8, beta FREE (>= floor), warm-started
from W6's own certificates so the result can only improve on W6's numbers.
Every certificate re-verified by the independent exact pure-Python counter."""
from __future__ import annotations
import json, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'unaudited-bridge-w6-2026-08-15'))
import w9_anneal as A
import w9_template as wt
from w6_task2_collision8 import geometry
from itertools import combinations

BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 60.0
BANDS = [19, 20, 21, 22, 23, 24, 25, 26, 27]
EDGES = tuple(combinations(range(8), 2))
W6BLOB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "unaudited-bridge-w6-2026-08-15",
                        "results_sigmamin_N8.json")))
W6 = {r["m"]: r for r in W6BLOB["rows"]}

geo = geometry(8)
rng = random.Random(20260815)
rows = []
print(f"W9/B0  honest Sigma_min at N=8 (beta free >= floor), warm-started from "
      f"W6.  budget {BUDGET}s/support.", flush=True)
print("   m  floor   W6(beta=floor)   W9(beta free)  delta  beta  reverified", flush=True)
for m in BANDS:
    floor = max(0, 24 - m)
    w6row = W6[m]
    warm = None
    if w6row["template"] is not None:
        warm = [frozenset(tuple(c) for c in s) for s in w6row["template"]]
    best = A.anneal(geo, rng, m, floor, BUDGET, warm=warm)
    if best is None:
        print(f"  {m:2d}    {floor:2d}       {w6row['sigma_min_upper_bound']:4d}"
              f"            --", flush=True)
        rows.append({"m": m, "w6": w6row["sigma_min_upper_bound"], "w9": None})
        continue
    sigma, tpl, rec = best
    T = {EDGES[n]: frozenset(map(tuple, s)) for n, s in enumerate(tpl)}
    aud = wt.audit(T)
    ok = (aud["Sigma"] == sigma and aud["m"] == m and aud["S_singleton_free"]
          and not aud["T4_missing_pures"] and aud["T5_min_degree_ok"]
          and aud["T6_slots_ok"] and aud["beta"] >= floor)
    w6s = w6row["sigma_min_upper_bound"]
    print(f"  {m:2d}    {floor:2d}       {w6s:4d}          {sigma:4d}"
          f"   {sigma - w6s:+4d}   {rec['beta']:3d}   {'OK' if ok else 'FAIL'}",
          flush=True)
    rows.append({"m": m, "floor": floor, "w6_beta_pinned": w6s,
                 "w9_beta_free": sigma, "delta": sigma - w6s,
                 "beta": rec["beta"], "reverified": bool(ok),
                 "template": [sorted(map(list, s)) for s in tpl],
                 "audit": {k: v for k, v in aud.items()
                           if k != "mixed_fibre_histogram"}})
with open("results_b0_sigmamin_honest.json", "w") as fh:
    json.dump({"budget": BUDGET, "rows": rows}, fh, indent=1, default=str)
print("wrote results_b0_sigmamin_honest.json", flush=True)
