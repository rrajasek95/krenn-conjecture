#!/usr/bin/env python3
"""W23 T2g -- THE COMPLETE LADDER AT N = 6.

At N = 6 a word's "off-count" relative to its best constant background is
determined by its colour multiset:

    (6,0,0) 0-off | (5,1,0) 1-off | (4,2,0),(4,1,1) 2-off
    (3,3,0),(3,2,1) 3-off | (2,2,2) 4-off

so the ladder is  X_0 subset X_1 subset X_2 subset X_3 subset X_4 = EXACT,
and X_3 is the LAST nonempty rung (X_4 is empty by the six-site theorem).
X_3 imposes every equation except the BALANCED (2,2,2) words -- and the
committed near-exact source is exactly an X_3 point.

T2f established that ALL-BLOCKED points of X_2 EXIST among general sources.
This runner asks the same question one rung up: is there an ALL-BLOCKED point
of X_3?  Every candidate gets the full control battery (raw-word membership,
both deciders, two primes).
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-induction2-w22-2026-08-15")
import w23_core as C                                          # noqa: E402
import w23_walk as WK                                         # noqa: E402
import w23_decide as DEC                                      # noqa: E402
import w22_n6 as N6                                           # noqa: E402
import run_t2f_x2_allblocked as T2F                           # noqa: E402

N = 6
PAIRS = list(combinations(range(N), 2))
RES = {}


def main():
    rng = random.Random(606060)
    ne = C.near_exact_six_site()
    for k in (0, 1, 2, 3, 4):
        w = WK.near_constant_words(N, 3, k)
        shapes = Counter(tuple(sorted(Counter(x).values())) for x in w)
        print(f"   X_{k}: {len(w)} words; colour-multiset shapes "
              f"{dict(shapes)}", flush=True)
    words3 = WK.near_constant_words(N, 3, 3)
    words4 = WK.near_constant_words(N, 3, 4)
    print(f"   X_4 has {len(words4)} words = all 3^6 = 729? "
          f"{len(words4) == 729}", flush=True)
    print(f"   near-exact source in X_3: "
          f"{WK.in_Xk(ne, N, words3)[0]}", flush=True)
    RES["ladder_words"] = {str(k): len(WK.near_constant_words(N, 3, k))
                           for k in range(5)}

    # site-system dimensions on X_3
    dims = []
    for z in range(N):
        sysd = WK.site_systems(ne, z, N, words3)
        row = []
        for c in range(3):
            rows, rhs, tags, cols = sysd[c]
            part, kern = WK.solve_linear(rows, rhs)
            row.append(None if part is None else len(kern))
        dims.append(row)
    print(f"   X_3 site-system kernel dims at the near-exact source: {dims}",
          flush=True)
    RES["x3_site_dims"] = dims

    # walk X_3 and hunt for all-blocked points
    found = []
    examined = 0
    stats = []
    while examined < 40 and len(found) < 3:
        src = ne
        steps = rng.randint(2, 8)
        ok = True
        for t in range(steps):
            new, d = WK.walk_step(src, t % N, N, words3, rng, spread=2)
            if new is None:
                ok = False
                break
            src = new
        if not ok:
            continue
        examined += 1
        bat = T2F.full_battery(src, f"X3{examined}")
        # re-verify membership at the X_3 level explicitly
        inx3 = WK.in_Xk(src, N, words3)[0]
        md = C.mixed_defects(src, N)
        shapes = Counter(tuple(sorted(Counter(w).values())) for w in md)
        stats.append({"obj": examined, "in_X3": inx3, "n_live": bat["n_live"],
                      "n_witness": bat["n_witness"],
                      "all_blocked": bat["all_blocked"],
                      "ranks": bat["ranks"], "defects": len(md),
                      "defect_shapes": {str(k): v for k, v in shapes.items()}})
        print(f"   X_3 object {examined}: in X_3 {inx3}; live {bat['n_live']}; "
              f"witness {bat['n_witness']}; defects {len(md)} "
              f"{dict(shapes)}; ranks {bat['ranks']}", flush=True)
        if bat["all_blocked"]:
            blocks = {f"{a},{b}": [[str(x) for x in row]
                                   for row in src[(a, b)]] for a, b in PAIRS}
            found.append({"battery": {k: v for k, v in bat.items()
                                      if k != "rows"},
                          "rows": bat["rows"], "blocks": blocks})
            print(f"   >>> ALL-BLOCKED X_3 OBJECT (decider disagreements "
                  f"{bat['decider_disagreements']}, mod-p mismatches "
                  f"{bat['modp_mismatch']})", flush=True)
    print(f"\n{examined} walked X_3 objects; ALL-BLOCKED: {len(found)}")
    wc = [s["n_witness"] for s in stats]
    if wc:
        print(f"witness counts: min {min(wc)} max {max(wc)}")
    RES["x3_walk"] = {"examined": examined, "all_blocked": len(found),
                      "stats": stats, "found": found}

    with open(f"{BASE}/results_t2g_x3.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t2g_x3.json")


if __name__ == "__main__":
    main()
