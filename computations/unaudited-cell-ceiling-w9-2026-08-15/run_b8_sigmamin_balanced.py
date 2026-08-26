#!/usr/bin/env python3
"""W9 Task B8 -- THE HONEST H4 TARGET:  Sigma_min^P(m).

Two corrections to W6's Sigma_min are needed, and they pull opposite ways.

 (i)  beta must be FREE (>= floor), not pinned at the floor.  Pinning
      inflates Sigma_min.                                   [lowers it]
 (ii) by W3 Corollary A.2 the MINIMUM-CELL-SUPPORT counterexample is
      BALANCED, so only case-(P) (balanceable) templates may be counted.
      W6's certificates at m = 19,20,21,22,23,25 are all case (D).
                                                            [raises it]

Sigma_min^P(m) := min { Sigma(T) : T has m nonempty blocks, beta >= max(0,24-m),
                        all three pure fibres >= 1, all 24 slots covered,
                        min degree >= 3, NO mixed singleton, AND T is in
                        W3 case (P) }.

H4 must beat THIS number: it needs a proved ceiling C(m) < Sigma_min^P(m).
Balance is decided by W3's own exactly-certified LP (w3_balance).
Fibre counts exact; every reported certificate re-audited in pure Python.
"""
from __future__ import annotations
import json, os, random, sys, time
from fractions import Fraction as F
from itertools import combinations
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'unaudited-bridge-w6-2026-08-15'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'unaudited-git-moment-w3-2026-08-15'))
import w9_anneal as A
import w9_template as wt
import w3_core as w3c
import w3_balance as w3b
from w6_task2_collision8 import geometry

N = 8
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: k for k, e in enumerate(EDGES)}
CI = w3c.cell_index(N)


def to_S(template):
    return sorted(CI[(EIDX[e], i, j)] for e in template for (i, j) in template[e])


def is_P(template):
    S = to_S(template)
    bal = w3b.find_balance(N, S)
    if bal is None:
        return False, None
    ok = w3b.verify_balance(N, S, bal["y"], bal["mu"])
    return bool(ok), bal


def collect(geo, rng, m, floor, seconds, warm):
    """Anneal, collecting EVERY cheap-feasible template seen, keyed by Sigma."""
    import math
    start = time.time()
    pool = {}
    tpl = warm
    while time.time() - start < seconds:
        if tpl is None:
            tpl = A._random_seed(geo, rng, m, floor)
            if tpl is None:
                break
        cur, rec = A.cost(geo, tpl, m, floor)
        if cur is None:
            tpl = None
            continue
        T = 8.0
        while time.time() - start < seconds:
            T = max(T * 0.9997, 0.15)
            cand = A.move(geo, rng, tpl)
            if cand is None:
                continue
            val, r2 = A.cost(geo, cand, m, floor)
            if val is None:
                continue
            if val <= cur or rng.random() < math.exp(-(val - cur) / T):
                tpl, cur = cand, val
            if r2["feasible"]:
                s = r2["sigma"]
                pool.setdefault(s, []).append([frozenset(x) for x in cand])
                if len(pool[s]) > 12:
                    pool[s] = pool[s][:12]
        tpl = None
    return pool


if __name__ == "__main__":
    BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 120.0
    BANDS = [19, 20, 21, 22, 23, 24, 25, 26, 27]
    geo = geometry(N)
    rng = random.Random(20260815)
    W6BLOB = json.load(open(os.path.join("..", "unaudited-bridge-w6-2026-08-15",
                                         "results_sigmamin_N8.json")))
    W6 = {r["m"]: r for r in W6BLOB["rows"]}
    try:
        W9B0 = {r["m"]: r for r in
                json.load(open("results_b0_sigmamin_honest.json"))["rows"]}
    except FileNotFoundError:
        W9B0 = {}

    print("=" * 100)
    print("B8  Sigma_min^P(m): the honest H4 target (beta free AND W3 case (P))")
    print("=" * 100)
    print(f"{'m':>3} {'W6(beta pin)':>13} {'W9(beta free)':>14} "
          f"{'Sigma_min^P':>12} {'#(D)-rejected below it':>23}", flush=True)
    rows = []
    for m in BANDS:
        floor = max(0, 24 - m)
        w6row = W6[m]
        warm = ([frozenset(tuple(c) for c in s) for s in w6row["template"]]
                if w6row["template"] else None)
        pool = collect(geo, rng, m, floor, BUDGET, warm)
        best_P, rejected = None, 0
        for s in sorted(pool):
            hit = False
            for cand in pool[s]:
                T = {EDGES[n]: frozenset(map(tuple, x)) for n, x in enumerate(cand)}
                ok, bal = is_P(T)
                if ok:
                    aud = wt.audit(T)
                    good = (aud["Sigma"] == s and aud["m"] == m
                            and aud["S_singleton_free"]
                            and not aud["T4_missing_pures"]
                            and aud["T5_min_degree_ok"] and aud["T6_slots_ok"]
                            and aud["beta"] >= floor)
                    if good:
                        best_P = (s, cand, aud, bal)
                        hit = True
                        break
            if hit:
                break
            rejected += len(pool[s])
        w9f = W9B0.get(m, {}).get("w9_beta_free")
        print(f"{m:3d} {w6row['sigma_min_upper_bound']:13d} "
              f"{(w9f if w9f is not None else -1):14d} "
              f"{(best_P[0] if best_P else -1):12d} {rejected:23d}", flush=True)
        rows.append({"m": m,
                     "w6_beta_pinned": w6row["sigma_min_upper_bound"],
                     "w9_beta_free": w9f,
                     "sigma_min_P": best_P[0] if best_P else None,
                     "D_rejected_below": rejected,
                     "template": ([sorted(map(list, x)) for x in best_P[1]]
                                  if best_P else None),
                     "audit": ({k: v for k, v in best_P[2].items()
                                if k != "mixed_fibre_histogram"} if best_P else None)})
    with open("results_b8_sigmamin_balanced.json", "w") as fh:
        json.dump({"budget": BUDGET, "rows": rows}, fh, indent=1, default=str)
    print("\nwrote results_b8_sigmamin_balanced.json")
