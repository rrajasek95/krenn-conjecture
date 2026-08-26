#!/usr/bin/env python3
"""W9 Task A -- CALIBRATION.  Exact cell census of every near-exact object
we can lay hands on.  Exact arithmetic (Fraction); no floats anywhere.

A1  STAGE_A base + second: defect verification, census, degree profile.
A2  Comparison against Sigma_min(m) -- the H4 kill test.
A3  Mutation controls.
"""
from __future__ import annotations
import json, sys
from fractions import Fraction
from itertools import combinations
import w9_core as w9
from w9_core import COLORS, cells, matrix_rank

OUT = {}

def show_census(name, src):
    c = w9.full_census(src)
    dlive, dR = w9.degree_profile(src)
    print(f"-- {name}")
    print(f"   m = {c['m']}   Sigma = {c['Sigma']}   beta(1-cell) = {c['beta']}"
          f"   |H|(rank>=2) = {c['H']}   Sigma/m = {c['Sigma_over_m']}"
          f" ~ {float(c['Sigma_over_m']):.3f}" if c['m'] else "   empty")
    print(f"   kinds        = {c['kinds']}")
    print(f"   cell hist    = {dict(sorted(c['cell_histogram'].items()))}")
    print(f"   live degrees = {dlive}")
    print(f"   rank1 degrees= {dR}")
    sm = w9.SIGMA_MIN.get(c['m'])
    if sm is not None:
        print(f"   Sigma_min({c['m']}) = {sm}   ->  Sigma {'>=' if c['Sigma']>=sm else '<'} Sigma_min"
              f"   (Sigma - Sigma_min = {c['Sigma']-sm})")
    rec = {k: v for k, v in c.items() if k != "per_block"}
    rec["Sigma_over_m"] = str(c["Sigma_over_m"])
    rec["live_degrees"] = dlive
    rec["rank1_degrees"] = dR
    rec["sigma_min_at_m"] = sm
    rec["per_block"] = {f"{u},{v}": {"cells": d["cells"], "rank": d["rank"],
                                     "kind": d["kind"],
                                     "support": [list(x) for x in d["support"]]}
                        for (u, v), d in c["per_block"].items()}
    return rec


print("=" * 72)
print("A1  STAGE_A (the committed near-exact eight-site source)")
print("=" * 72)
for label, second in (("STAGE_A_BASE", False), ("STAGE_A_SECOND", True)):
    src = w9.load_stage_a(second=second)
    defects = w9.defect_words(src)
    print(f"\n[{label}]  GHZ defect words: {len(defects)}"
          f"  -> {sorted(''.join(map(str,w)) for w in defects)}")
    mixed_bad = sum(1 for w in defects if len(set(w)) > 1)
    print(f"   mixed-word defects: {mixed_bad}  (0 == mixed system FULLY EXACT)")
    rec = show_census(label, src)
    rec["defect_words"] = sorted("".join(map(str, w)) for w in defects)
    rec["mixed_defects"] = mixed_bad
    OUT[label] = rec

print()
print("=" * 72)
print("A3  Mutation controls on the census machinery")
print("=" * 72)
src = w9.load_stage_a()
# M1: zero out one live cell -> Sigma must drop by exactly 1
import copy
mut = {k: [list(r) for r in v] for k, v in src.items()}
tgt = next((k, i, j) for k in mut for i in COLORS for j in COLORS if mut[k][i][j])
mut[tgt[0]][tgt[1]][tgt[2]] = Fraction(0)
c0, c1 = w9.full_census(src), w9.full_census(mut)
print(f"M1 zero one cell {tgt}: Sigma {c0['Sigma']} -> {c1['Sigma']}"
      f"  (delta = {c1['Sigma']-c0['Sigma']}, want -1) "
      f"{'PASS' if c1['Sigma']-c0['Sigma'] == -1 else 'FAIL'}")
# M2: add a cell to a dead block -> m must rise by 1 if any dead block exists
dead = [k for k in src if not cells(src[k])]
if dead:
    mut2 = {k: [list(r) for r in v] for k, v in src.items()}
    mut2[dead[0]][0][0] = Fraction(7)
    c2 = w9.full_census(mut2)
    print(f"M2 wake dead block {dead[0]}: m {c0['m']} -> {c2['m']},"
          f" Sigma {c0['Sigma']} -> {c2['Sigma']} "
          f"{'PASS' if c2['m']==c0['m']+1 and c2['Sigma']==c0['Sigma']+1 else 'FAIL'}")
else:
    print("M2 skipped: no dead blocks (full support)")
# M3: perturbing a live cell must break exactness (defect sweep must SEE it)
mut3 = {k: [list(r) for r in v] for k, v in src.items()}
mut3[tgt[0]][tgt[1]][tgt[2]] += Fraction(1)
d3 = len(w9.defect_words(mut3))
print(f"M3 perturb one live cell: defect count {len(w9.defect_words(src))} -> {d3} "
      f"{'PASS' if d3 > 2 else 'FAIL'}")
# M4: rank census sanity -- a manifestly rank-2 block must classify as rank2
probe = [[Fraction(1),Fraction(0),Fraction(0)],[Fraction(0),Fraction(1),Fraction(0)],[Fraction(0)]*3]
print(f"M4 rank census on explicit rank-2 matrix: {w9.classify_block(probe)} "
      f"{'PASS' if w9.classify_block(probe)=='rank2' else 'FAIL'}")

OUT["controls"] = {"M1_zero_cell_delta": c1['Sigma']-c0['Sigma'],
                   "M3_perturb_defects": d3,
                   "M4_rank2_kind": w9.classify_block(probe)}

with open("results_a_calibration.json", "w") as fh:
    json.dump(OUT, fh, indent=1, sort_keys=True)
print("\nwrote results_a_calibration.json")
