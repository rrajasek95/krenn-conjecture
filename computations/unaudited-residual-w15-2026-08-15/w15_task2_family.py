#!/usr/bin/env python3
"""W15 TASK 2/3 -- apply the Phi-forcing mechanism to the whole (R) family.

For each instance m = 20..28 find a target point (x*,y*) at which Phi is
REQUIRED to be nonzero (a constant word with no extras, or a mixed word
with exactly one extra monomial) and decide, exactly over Q via Singular,
whether the clean equations FORCE Phi(x*,y*) = 0.  Forced => the template
is dead.
"""

import json
import os
import sys
import time
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import W8_IMMUNE, single_cell_activity, MATCHINGS, CONST_WORDS
from w15_forcing import (full_matchings, extras, y_free, x_ok, forcing_test)

HERE = os.path.dirname(os.path.abspath(__file__))
L4 = tuple(product(range(3), repeat=4))
res = {}
only = sys.argv[1:] and [int(a) for a in sys.argv[1:]]

for m in sorted(W8_IMMUNE):
    if only and m not in only:
        continue
    T = W8_IMMUNE[m]
    act = single_cell_activity(T)
    fullm = full_matchings(T)
    YF = y_free(T, act)
    # candidate targets, best first: constants with 0 extras, then mixed
    # words with exactly one extra
    cands = []
    for c in range(3):
        x = y = (c,) * 4
        if not extras(T, x, y, fullm):
            cands.append(((x, y), "constant", 0))
    ones = [(x, y) for x in L4 for y in L4
            if len(set(tuple(x) + tuple(y))) > 1
            and len(extras(T, x, y, fullm)) == 1]
    ones.sort(key=lambda t: -len(x_ok(T, act, t[1])))
    cands += [(t, "mixed", 1) for t in ones[:4]]
    entry = {"n_full_matchings": len(fullm), "n_y_free": len(YF),
             "n_one_extra_mixed": len(ones), "trials": [], "verdict": "open"}
    print(f"=== m={m}  |F|={len(fullm)}  Yfree={len(YF)}  "
          f"one-extra mixed words={len(ones)}", flush=True)
    for (tgt, kind, k) in cands:
        XO = [x for x in x_ok(T, act, tgt[1]) if x != tgt[0]]
        hit = False
        for nx, ny in ((2, 2), (3, 2), (3, 3), (4, 3), (5, 4), (8, 4)):
            if nx > len(XO) or ny > len(YF):
                continue
            t0 = time.time()
            try:
                v, nv, ne, raw = forcing_test(T, tgt, XO[:nx], YF[:ny],
                                              timeout=1500)
            except Exception as exc:
                print(f"   ERROR {exc}", flush=True)
                v, nv, ne = None, -1, -1
            dt = time.time() - t0
            print(f"   target={kind} x*={tgt[0]} y*={tgt[1]} extras={k} "
                  f"|X'|={nx} |Y'|={ny}: FORCED={v} vars={nv} eqs={ne} "
                  f"{dt:.1f}s", flush=True)
            entry["trials"].append({"kind": kind, "xstar": list(tgt[0]),
                                    "ystar": list(tgt[1]), "extras": k,
                                    "nx": nx, "ny": ny, "forced": v,
                                    "vars": nv, "eqs": ne,
                                    "seconds": round(dt, 1)})
            if v:
                hit = True
                break
        if hit:
            entry["verdict"] = ("killed:constant-word-vanishes" if kind ==
                                "constant" else
                                "killed:single-extra-monomial-vanishes")
            entry["killing_target"] = {"x": list(tgt[0]), "y": list(tgt[1]),
                                       "kind": kind, "extras": k}
            break
    print(f"   VERDICT m={m}: {entry['verdict']}", flush=True)
    res[m] = entry
    json.dump(res, open(os.path.join(HERE, "results_task2_family.json"), "w"),
              indent=1)
print("DONE")
