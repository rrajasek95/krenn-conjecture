#!/usr/bin/env python3
"""W9 Task A2 -- how high does Sigma go on the MIXED-EXACT stratum?

The STAGE_A family is a 12-parameter closed-form family of eight-site
sources whose ENTIRE MIXED SYSTEM IS EXACT (only the pure words 0^8, 1^8
fail).  Every ceiling argument derived from the mixed equations -- (STAR)
pinning, W5's L1/L2 laws, the attachment criterion, W6's support criterion
-- applies to these sources VERBATIM.  So

        max { Sigma(A) : A in the mixed-exact stratum, support m }

is a LOWER BOUND for any mixed-system-derived ceiling C(m).
H4 needs C(m) < Sigma_min(m).  We measure the gap.

Exact arithmetic throughout (Fraction).  Parameter choice is a search
(labelled), every verdict is exact.
"""
from __future__ import annotations
import importlib, json, random, sys
from fractions import Fraction as F
from itertools import combinations
import w9_core as w9
from w9_core import COLORS, cells

mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")

def build(params):
    blocks = mod.build_stage_a(params)
    out = {}
    for u, v in combinations(range(8), 2):
        t = mod.C.oriented(blocks, u, v)
        out[(u, v)] = [[F(t[a][b]) for b in COLORS] for a in COLORS]
    return out

def mk_params(rng, big=False):
    def r():
        while True:
            n = rng.randint(-9, 9) if not big else rng.randint(-40, 40)
            if n: return F(n)
    def r3():  # allow denominators too
        return F(rng.randint(-9, 9) or 1, rng.randint(1, 5))
    return ((r(), r()), (r(), r()), r3(), r3(), r3(), r3(),
            (r3(), r3(), r3()), (r3(), r3(), r3()),
            (r3(), r3(), r3()), (r3(), r3(), r3()),
            r(), r())

OUT = {"note": "search over STAGE_A parameter space; all verdicts exact"}
rng = random.Random(20260815)
best = None
records = []
seen_sigma = {}
TRIALS = 400
for trial in range(TRIALS):
    params = mk_params(rng)
    try:
        src = build(params)
    except ZeroDivisionError:
        continue
    c = w9.full_census(src)
    key = (c["m"], c["Sigma"])
    seen_sigma[key] = seen_sigma.get(key, 0) + 1
    if best is None or (c["Sigma"], -c["m"]) > (best[1]["Sigma"], -best[1]["m"]):
        best = (params, c, src)

print("=" * 74)
print("A2  Sigma over the STAGE_A (mixed-exact) family:", TRIALS, "random exact points")
print("=" * 74)
for (m, S), n in sorted(seen_sigma.items(), key=lambda kv: (-kv[0][1], kv[0][0])):
    print(f"   m = {m:3d}   Sigma = {S:4d}   count = {n:4d}"
          f"   Sigma_min({m}) = {w9.SIGMA_MIN.get(m)}")
OUT["sigma_histogram"] = [{"m": m, "Sigma": S, "count": n} for (m, S), n in
                          sorted(seen_sigma.items())]

params, c, src = best
print(f"\nBEST point: m = {c['m']}, Sigma = {c['Sigma']}")
print(f"   params = {params}")

# ---- EXACT VERIFICATION of the best point ---------------------------------
print("\n-- exact verification of the maximal point --")
defects = w9.defect_words(src)
print(f"   GHZ defect words   : {len(defects)} -> "
      f"{sorted(''.join(map(str,w)) for w in defects)}")
mixed_bad = sum(1 for w in defects if len(set(w)) > 1)
print(f"   MIXED defects      : {mixed_bad}   (0 == mixed system fully exact)")
print(f"   m = {c['m']}  Sigma = {c['Sigma']}  beta = {c['beta']}  |H| = {c['H']}")
print(f"   Sigma/m            = {c['Sigma_over_m']} ~ {float(c['Sigma_over_m']):.4f}")
sm = w9.SIGMA_MIN[c['m']]
print(f"   Sigma_min({c['m']})       = {sm}")
print(f"   GAP  Sigma_min - Sigma = {sm - c['Sigma']}")
print(f"   => any MIXED-SYSTEM-DERIVED ceiling must satisfy C({c['m']}) >= {c['Sigma']};")
print(f"      H4 needs C({c['m']}) <= {sm-1}.  Surviving window: "
      f"[{c['Sigma']}, {sm-1}]  (width {sm - c['Sigma']}).")

print("\n-- per-block cell profile of the maximal point --")
for (u, v), d in sorted(c["per_block"].items()):
    if d["cells"]:
        print(f"   edge {u}{v}: cells = {d['cells']}  rank = {d['rank']}  {d['kind']}")

OUT["best"] = {"m": c["m"], "Sigma": c["Sigma"], "beta": c["beta"], "H": c["H"],
               "sigma_min": sm, "gap": sm - c["Sigma"],
               "mixed_defects": mixed_bad,
               "defects": sorted("".join(map(str, w)) for w in defects),
               "params": str(params), "kinds": c["kinds"],
               "cell_histogram": {str(k): v for k, v in c["cell_histogram"].items()},
               "per_block": {f"{u},{v}": {"cells": d["cells"], "rank": d["rank"],
                                          "kind": d["kind"]}
                             for (u, v), d in c["per_block"].items()}}

# ---- CONTROL: symbolic max support of the family ---------------------------
# Union of cells that are nonzero at SOME sampled parameter point == the
# family's generic cell pattern.  Sigma_generic is then the family maximum.
union = {k: [[0]*3 for _ in range(3)] for k in src}
rng2 = random.Random(777)
for _ in range(300):
    try:
        s2 = build(mk_params(rng2))
    except ZeroDivisionError:
        continue
    for k in s2:
        for i in COLORS:
            for j in COLORS:
                if s2[k][i][j]:
                    union[k][i][j] = 1
gen_sigma = sum(sum(row) for k in union for row in union[k])
gen_m = sum(1 for k in union if any(any(r) for r in union[k]))
print(f"\nCONTROL (generic cell pattern of the family, union over 300 points):")
print(f"   generic m = {gen_m}   generic Sigma = {gen_sigma}"
      f"   {'== best found' if gen_sigma == c['Sigma'] else '!! best found is not generic'}")
OUT["generic_pattern"] = {"m": gen_m, "Sigma": gen_sigma}

with open("results_a2_generic_stage_a.json", "w") as fh:
    json.dump(OUT, fh, indent=1, sort_keys=True)
print("\nwrote results_a2_generic_stage_a.json")
