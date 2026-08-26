#!/usr/bin/env python3
"""W25 T1f -- THE HEAVY N=6 ADVERSARIAL BUILDER (ledger 20, second pass).

T1b screened 377 X_3 objects at N=6 from four seed families and found no
all-blocked point.  T3 then FOUND one at N=8 -- by exactly the move that fails
at N=6 (a long site-linear walk inside X_3).  This runner therefore re-attacks
N=6 with the N=8 recipe and with much more force:

  * longer walks (up to 20 site solves) with large kernel spreads;
  * every one of the 24 diagonal classes as a seed, several weight points each;
  * the triangle-deformation skeleton of T1c walked inside X_3;
  * Q(omega) walks;
  * torus-twisted and colour/site-permuted restarts (the ladder and the
    witness predicate are invariant under that group, so this is a diversity
    device, not a new stratum);
  * every object re-verified in X_3 against the raw 639-word definition, then
    screened; any all-blocked object gets the full two-decider battery.
"""
from __future__ import annotations

import json
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x3core-w25-2026-08-15")
W23BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W23BASE)
import w25_core as C
import w25_walk as WK
import w25_decide as D
import w23_decide as W23D
import run_t1d_diagonal as T1D
import run_t1e_diagonal_uniform as T1E

N = 6
RES = {}
RAN = []
ESC = []


def control(name):
    RAN.append(name)


def screen(src, tag):
    live = [(p, q) for p, q in combinations(range(N), 2) if C.live(src, p, q)]
    order = sorted(live, key=lambda pq: -C.matrix_rank(C.oriented(src, *pq)))
    dec = []
    for (p, q) in order:
        U = tuple(x for x in range(N) if x not in (p, q))
        v, d, _ = D.decide_pair(src, p, q, U, f"{tag}_{p}{q}", primes=())
        dec.append([[p, q], v])
        if v == "WITNESS":
            return {"n_live": len(live), "all_blocked": False,
                    "n_decided": len(dec)}
    return {"n_live": len(live), "all_blocked": bool(live),
            "n_decided": len(dec), "verdicts": dec}


def record(src, tag, seed, stats):
    ok, bw = C.in_Xk(src, N, 3)
    assert ok, (tag, "left X_3", bw)
    live = sum(1 for a, b in combinations(range(N), 2) if C.live(src, a, b))
    if live == 0:
        stats.append({"tag": tag, "seed": seed, "skip": True})
        return
    ranks = sorted(C.matrix_rank(C.oriented(src, a, b))
                   for a, b in combinations(range(N), 2))
    sc = screen(src, tag)
    stats.append({"tag": tag, "seed": seed, "ranks": ranks, **sc})
    if sc["all_blocked"]:
        blocks = {f"{a},{b}": [[str(x) for x in r] for r in src[(a, b)]]
                  for a, b in combinations(range(N), 2)}
        ESC.append({"tag": tag, "seed": seed, "blocks": blocks,
                    "verdicts": sc.get("verdicts")})
        print(f"\n   *** ALL-BLOCKED X_3 CANDIDATE AT N=6: {tag} "
              f"(seed {seed})\n", flush=True)


def long_walk(src, rng, steps, spread):
    cur = src
    for t in range(steps):
        nxt, dm = WK.site_solve(cur, rng.randrange(N), N, 3, rng,
                                spread=spread)
        if nxt is None:
            return None
        cur = nxt
    return cur


def main():
    t0 = time.time()
    rng = random.Random(1234567)
    stats = []
    classes = sorted(set(T1D.canonical(Ls) for Ls in T1E._survivors()))

    print("(1) long walks from every diagonal class")
    for i, cn in enumerate(classes):
        for wpt in T1E.sample_points(cn, rng, k=2):
            base = T1D.build_source(cn, wpt)
            for rep in range(6):
                steps = rng.choice([4, 8, 12, 20])
                spread = rng.choice([1, 2, 3, 5, 9])
                s = long_walk(base, rng, steps, spread)
                if s is not None:
                    record(s, f"L{i}_{rep}", f"diag{i}", stats)
        if i % 6 == 0:
            print(f"   class {i}: objects {len(stats)}, all-blocked "
                  f"{sum(1 for x in stats if x.get('all_blocked'))}",
                  flush=True)
    control("HB1_long_diagonal_walks")

    print("(2) torus twists then long walks")
    for i, cn in enumerate(classes[:12]):
        for wpt in T1E.sample_points(cn, rng, k=1):
            base = T1D.build_source(cn, wpt)
            for rep in range(4):
                lam = [[Fraction(rng.choice([1, -1, 2, -2, 3])) for _ in range(3)]
                       for _ in range(N)]
                for c in range(3):
                    pr = Fraction(1)
                    for u in range(N - 1):
                        pr *= lam[u][c]
                    lam[N - 1][c] = 1 / pr
                tw = C.torus_act(base, lam, N)
                assert C.in_Xk(tw, N, 3)[0], "torus action left X_3"
                s = long_walk(tw, rng, rng.choice([6, 12]),
                              rng.choice([2, 3, 5]))
                if s is not None:
                    record(s, f"T{i}_{rep}", f"torus{i}", stats)
    control("HB2_torus_walks")

    print("(3) triangle-deformation skeletons walked inside X_3")
    for i, cn in enumerate(classes[:12]):
        for wpt in T1E.sample_points(cn, rng, k=1):
            base = T1D.build_source(cn, wpt)
            for tri in ([(0, 1), (0, 2), (1, 2)], [(3, 4), (3, 5), (4, 5)],
                        [(0, 3), (0, 4), (3, 4)]):
                cols = [(e, a, b) for e in tri for a in range(3)
                        for b in range(3)]
                z = C.copy_source(base)
                for e in tri:
                    z[e] = [[Fraction(0)] * 3 for _ in range(3)]
                rows, rhs = [], []
                units = {}
                for t in cols:
                    e, a, b = t
                    u = C.copy_source(z)
                    u[e][a][b] = Fraction(1)
                    units[t] = u
                for w in C.near_constant_words(N, 3, 3):
                    const = C.H(z, w, N)
                    rows.append([C.H(units[t], w, N) - const for t in cols])
                    rhs.append((Fraction(1) if len(set(w)) == 1
                                else Fraction(0)) - const)
                part, kern = C.solve_linear(rows, rhs, len(cols))
                if part is None:
                    continue
                for rep in range(3):
                    vec = list(part)
                    for kv in kern:
                        lam = Fraction(rng.randint(-4, 4))
                        if lam:
                            vec = [a + lam * b for a, b in zip(vec, kv)]
                    s = C.copy_source(z)
                    for k2, (e, a, b) in enumerate(cols):
                        s[e][a][b] = vec[k2]
                    record(s, f"D{i}_{tri[0][0]}{rep}", f"tri{i}", stats)
    control("HB3_triangle_walks")

    print("(4) Q(omega) long walks")
    for i, cn in enumerate(classes[:12]):
        for wpt in T1E.sample_points(cn, rng, k=1):
            base = T1D.build_source(cn, {e: C.Om(v, 0)
                                         for e, v in wpt.items()})
            for rep in range(3):
                cur = base
                good = True
                for t in range(rng.choice([4, 8])):
                    z = rng.randrange(N)
                    sysd = WK.site_systems(cur, z, N, 3)
                    sol = {}
                    for c in range(3):
                        rws, rh, tg, cls = sysd[c]
                        pt, kn = C.solve_linear(rws, rh, len(cls))
                        if pt is None:
                            good = False
                            break
                        vec = list(pt)
                        for kv in kn:
                            lam = C.Om(rng.randint(-3, 3), rng.randint(-3, 3))
                            if lam != 0:
                                vec = [a + lam * b for a, b in zip(vec, kv)]
                        sol[c] = vec
                    if not good:
                        break
                    cur = WK.apply_site_solution(cur, z, sol, sysd[0][3], N)
                if good:
                    record(cur, f"W{i}_{rep}", f"omega{i}", stats)
    control("HB4_omega_walks")

    n = len([s for s in stats if "n_live" in s])
    ab = sum(1 for s in stats if s.get("all_blocked"))
    print(f"\nTOTAL X_3 objects screened at N=6: {n}; ALL-BLOCKED {ab}")
    lv = Counter(s.get("n_live") for s in stats if "n_live" in s)
    rk = Counter(tuple(s["ranks"]) for s in stats if "ranks" in s)
    print(f"live-pair distribution {dict(sorted(lv.items()))}; distinct rank "
          f"profiles {len(rk)}; max block rank "
          f"{max(max(s['ranks']) for s in stats if 'ranks' in s)}")
    RES["stats"] = stats
    RES["escalations"] = ESC
    RES["summary"] = {"objects": n, "all_blocked": ab,
                      "live_distribution": {str(k): v for k, v in lv.items()},
                      "rank_profiles": len(rk),
                      "seconds": round(time.time() - t0, 1)}
    declared = ["HB1_long_diagonal_walks", "HB2_torus_walks",
                "HB3_triangle_walks", "HB4_omega_walks"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    assert not missing
    with open(f"{BASE}/results_t1f_builder2.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t1f_builder2.json")


if __name__ == "__main__":
    main()
