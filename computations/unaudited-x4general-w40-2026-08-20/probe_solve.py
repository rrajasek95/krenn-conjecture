#!/usr/bin/env python3
"""W40 probe: the D5 level-4 variety in its 6 surviving coordinates; find an
explicit rational point and audit it with the INHERITED engines."""
from __future__ import annotations

import itertools
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, N, Sym, build_variables, cell_forms, completion_generators,
    d5_point, haf, haf_pm, install_d3, kernel_bases, no_shadow_guard, off,
    run_singular, words3,
)

bg = d5_point()
kb = kernel_bases(bg)
names, lamidx, qidx = build_variables(kb)
cf = cell_forms(bg, kb, lamidx, qidx)
g4, _ = completion_generators(cf, 4)

KEEP = [lamidx[(2, 1)], lamidx[(6, 5)], qidx[(0, 4)], qidx[(1, 3)],
        qidx[(2, 6)], qidx[(5, 7)]]
KEEPNAME = ["L2", "L6", "q04", "q13", "q26", "q57"]
ZERO = [i for i in range(len(names)) if i not in KEEP]

# substitute the forced zeros, keep only the 6 survivors
sub = {}
for pos, i in enumerate(KEEP):
    sub[i] = pos
red = []
for g in g4:
    t = {}
    for m, c in g.t.items():
        if any(x in ZERO for x in m):
            continue
        mm = tuple(sorted(sub[x] for x in m))
        t[mm] = t.get(mm, Fraction(0)) + c
    t = {m: c for m, c in t.items() if c}
    if t:
        red.append(Sym(t))
uniq = {}
for g in red:
    uniq[tuple(sorted(g.t.items()))] = g
red = list(uniq.values())
nn = [f"zzv({i + 1})" for i in range(6)]
print("reduced generators:", len(red))
for g in sorted(red, key=lambda x: (x.ndeg(), len(x.t)))[:14]:
    print("   ", g.to_singular(nn))

body = ",\n ".join(g.to_singular(nn) for g in red)
script = ("ring R = 0, (zzv(1..6)), dp;\n"
          f"ideal zzI = {body};\n"
          "ideal zzG = std(zzI);\n"
          '"UNIT:", (size(zzG)==1 && zzG[1]==1);\n'
          '"DIM:", dim(zzG);\n'
          '"GB:", string(zzG);\n')
no_shadow_guard(script, set(nn))
txt = run_singular(script, timeout=900)
print(txt.strip()[:1500])

# --- explicit point search over small rationals -------------------------
print("\n--- explicit points ---")
vals_full = [Fraction(0)] * len(names)


def test(pt6):
    v = [Fraction(0)] * len(names)
    for pos, i in enumerate(KEEP):
        v[i] = pt6[pos]
    src = install_d3(cf, v)
    bad4 = [w for w in itertools.product(range(3), repeat=N)
            if off(w) <= 4 and haf(src, w, n=N, sample=Fraction(0))
            != (1 if len(set(w)) == 1 else 0)]
    bad5 = [w for w in itertools.product(range(3), repeat=N)
            if off(w) == 5 and haf(src, w, n=N, sample=Fraction(0))
            != (1 if len(set(w)) == 1 else 0)]
    return v, src, bad4, bad5


C = [Fraction(x) for x in (-2, -1, 1, 2)] + [Fraction(1, 2), Fraction(-1, 2)]
found = []
for L2 in C:
    for L6 in C:
        for q04 in C:
            for q13 in C:
                for q26 in C:
                    for q57 in C:
                        pt = [L2, L6, q04, q13, q26, q57]
                        ok = all(g.evaluate(
                            {i: pt[i] for i in range(6)}
                            if False else pt) == 0 for g in red)
                        if ok:
                            found.append(pt)
    if found:
        break
print("small-rational hits:", len(found))
for pt in found[:3]:
    v, src, b4, b5 = test(pt)
    print("  pt", [str(x) for x in pt], "k4 violations", len(b4),
          "off5 violations", len(b5))
    if not b4:
        out = {"point6": [str(x) for x in pt],
               "keep": KEEPNAME,
               "off5_violating_words": [list(w) for w in b5][:8],
               "n_off5_violations": len(b5),
               "source": {str(e): [[str(src[e][a][b]) for b in range(3)]
                                   for a in range(3)] for e in EDG}}
        json.dump(out, open(os.path.join(HERE, "probe_x4point.json"), "w"),
                  indent=1, sort_keys=True)
        print("  STORED probe_x4point.json")
        break
