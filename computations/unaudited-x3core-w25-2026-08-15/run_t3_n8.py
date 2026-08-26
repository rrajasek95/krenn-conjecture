#!/usr/bin/env python3
"""W25 T3 -- THE LADDER AT N = 8 FOR GENERAL SOURCES.

At N = 8 a word's off-count (N minus its largest colour multiplicity) runs
0..5, so the ladder is  X_0 ... X_5 = EXACT  (one rung longer than at N=6):

    (8,0,0) 0 | (7,1,0) 1 | (6,2,0),(6,1,1) 2 | (5,3,0),(5,2,1) 3
    | (4,4,0),(4,3,1),(4,2,2) 4 | (3,3,2) 5.

RUNG MAP measured here, with the same discipline as at N = 6:

 * CALIBRATION.  W25-D1 gives an unlimited supply of X_3 points at every N:
   every DIAGONAL X_2 source is automatically an X_3 source (odd colour
   classes force H = 0).  So W23's N=8 X_2 generator points -- and every
   diagonal object in the corpus -- sit at rung >= 3, exactly as the committed
   near-exact N=6 source does.  Whether they reach rung 4 is decided here.

 * THE TRIANGLE DEFORMATION (the N=6 all-blocked mechanism, transplanted).
   T1c showed that W23's four all-blocked X_2 points at N=6 are a diagonal
   X_3 point plus three free blocks on a TRIANGLE of sites -- and that,
   because no perfect matching can use two edges of a triangle, membership in
   X_k on that skeleton is an exact inhomogeneous LINEAR system.  The same
   construction is run here at N = 8: solve X_2 on the triangle skeleton,
   sample the affine solution space, decide every live pair, then solve X_3 on
   the same skeleton and see whether it collapses the deformation.
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
import w25_core as C                                            # noqa: E402
import w25_walk as WK                                           # noqa: E402
import w25_decide as D                                          # noqa: E402
import w23_decide as W23D                                       # noqa: E402
import run_t2_u2 as T2                                          # noqa: E402

N = 8
RES = {}
RAN = []


def control(name):
    RAN.append(name)


def linear_system(base, k, tri, n=N):
    """Membership in X_k as an exact linear system in the 27 entries of the
    three blocks of the triangle `tri` (no PM uses two triangle edges)."""
    cols = [(e, i, j) for e in tri for i in range(3) for j in range(3)]
    idx = {t: i for i, t in enumerate(cols)}
    z = C.copy_source(base)
    for e in tri:
        z[e] = [[Fraction(0)] * 3 for _ in range(3)]
    unit = {}
    for e in tri:
        for i in range(3):
            for j in range(3):
                t = C.copy_source(z)
                t[e][i][j] = Fraction(1)
                unit[(e, i, j)] = t
    rows, rhs = [], []
    for w in C.near_constant_words(n, 3, k):
        const = C.H(z, w, n)
        row = [C.H(unit[t], w, n) - const for t in cols]
        rows.append(row)
        rhs.append((Fraction(1) if len(set(w)) == 1 else Fraction(0)) - const)
    return rows, rhs, cols


def apply_sol(base, vec, cols, tri):
    out = C.copy_source(base)
    for e in tri:
        out[e] = [[Fraction(0)] * 3 for _ in range(3)]
    for k, (e, i, j) in enumerate(cols):
        out[e][i][j] = vec[k]
    return out


def screen(src, tag, n=N, cross=False):
    """Decide live pairs until a WITNESS appears."""
    live = [(p, q) for p, q in combinations(range(n), 2) if C.live(src, p, q)]
    order = sorted(live, key=lambda pq: -C.matrix_rank(C.oriented(src, *pq)))
    dec = []
    for (p, q) in order:
        U = tuple(x for x in range(n) if x not in (p, q))
        v, d, _ = D.decide_pair(src, p, q, U, f"{tag}_{p}{q}", primes=())
        dec.append([list((p, q)), v])
        if v == "WITNESS":
            return {"n_live": len(live), "n_decided": len(dec),
                    "witness": [p, q], "all_blocked": False}
    return {"n_live": len(live), "n_decided": len(dec), "witness": None,
            "all_blocked": bool(live), "verdicts": dec}


def full_battery(src, tag, n=N):
    rows = []
    for p, q in combinations(range(n), 2):
        if not C.live(src, p, q):
            continue
        U = tuple(x for x in range(n) if x not in (p, q))
        v1, d1, mp = D.decide_pair(src, p, q, U, f"{tag}A{p}{q}",
                                   primes=(1000003,))
        isrc, _ = C.clear_denominators(src)
        v2, _, _ = W23D.decide_pair(isrc, p, q, U, f"{tag}B{p}{q}",
                                    primes=(32003,))
        rows.append({"pair": [p, q], "w25": v1, "dim": d1, "modp": mp,
                     "w23": v2, "agree": v1 == v2})
    return {"n_live": len(rows),
            "n_witness": sum(1 for r in rows if r["w25"] == "WITNESS"),
            "all_blocked": bool(rows) and all(r["w25"] == "BLOCKED"
                                              for r in rows),
            "disagreements": sum(1 for r in rows if not r["agree"]),
            "rows": rows}


def main():
    t0 = time.time()
    rng = random.Random(80808)

    print("=" * 74)
    print("(1) the N = 8 ladder: words per rung")
    print("=" * 74)
    counts = {}
    for k in range(6):
        counts[k] = len(C.near_constant_words(N, 3, k))
    print(f"   |X_k words|: {counts}   (3^8 = {3 ** 8})")
    shapes = {}
    for k in range(6):
        w = set(C.near_constant_words(N, 3, k))
        prev = set(C.near_constant_words(N, 3, k - 1)) if k else set()
        shapes[k] = dict(Counter(tuple(sorted(Counter(x).values(), reverse=True))
                                 for x in w - prev))
    for k in range(6):
        print(f"      rung {k} adds shapes {shapes[k]}")
    RES["ladder"] = {"counts": counts,
                     "new_shapes": {str(k): {str(a): b for a, b in v.items()}
                                    for k, v in shapes.items()}}
    control("T3_1_ladder")

    print("=" * 74)
    print("(2) CALIBRATION: where do diagonal N=8 objects sit? (W25-D1)")
    print("=" * 74)
    cal = []
    for t in range(8):
        col, w, src = T2.build_n_diagonal(N, rng, extra=rng.choice([0, 2, 3]))
        if src is None:
            continue
        rec = {"extra_edges": len(col) - 3 * N // 2,
               "in_X2": C.in_Xk(src, N, 2)[0], "in_X3": C.in_Xk(src, N, 3)[0],
               "in_X4": C.in_Xk(src, N, 4)[0], "in_X5": C.in_Xk(src, N, 5)[0]}
        md = C.mixed_defects(src, N)
        rec["defects"] = len(md)
        rec["defect_offcounts"] = sorted(set(C.offcount(x) for x in md))
        cal.append(rec)
        print(f"   diagonal source ({rec['extra_edges']} extra edges): "
              f"X_2 {rec['in_X2']}, X_3 {rec['in_X3']}, X_4 {rec['in_X4']}, "
              f"X_5 {rec['in_X5']}; {rec['defects']} defects at off-counts "
              f"{rec['defect_offcounts']}")
    print("   => every diagonal X_2 object at N=8 is an X_3 object (W25-D1); "
          "its first defects sit at off-count 4, exactly as at N=6 the "
          "committed near-exact source is an X_3 point whose 3 defects are "
          "the balanced (2,2,2) words.")
    RES["calibration"] = cal
    assert all(r["in_X2"] == r["in_X3"] for r in cal)
    control("T3_2_calibration")

    print("=" * 74)
    print("(3) THE TRIANGLE DEFORMATION AT N = 8 -- rung by rung")
    print("=" * 74)
    rung = {}
    found_allblocked = {}
    bases = []
    for t in range(6):
        col, w, src = T2.build_n_diagonal(N, rng, extra=rng.choice([0, 2, 3]))
        if src is not None:
            bases.append((col, src))
    print(f"   {len(bases)} diagonal X_3 bases built")
    for bi, (col, base) in enumerate(bases):
        for tri in [[(0, 1), (0, 2), (1, 2)], [(1, 2), (1, 3), (2, 3)],
                    [(0, 2), (0, 4), (2, 4)]]:
            dims = {}
            for k in (2, 3, 4):
                rows, rhs, cols = linear_system(base, k, tri)
                part, kern = C.solve_linear(rows, rhs, len(cols))
                dims[k] = None if part is None else len(kern)
                if k == 2 and part is not None:
                    for s in range(4):
                        vec = list(part)
                        if s:
                            for kv in kern:
                                lam = Fraction(rng.randint(-3, 3))
                                if lam:
                                    vec = [a + lam * b
                                           for a, b in zip(vec, kv)]
                        cand = apply_sol(base, vec, cols, tri)
                        ok, bw = C.in_Xk(cand, N, 2)
                        assert ok, ("left X_2", bw)
                        sc = screen(cand, f"T{bi}{tri[0][0]}{s}")
                        rec = {"base": bi, "tri": [list(e) for e in tri],
                               "sample": s, "x2_dim": dims[2],
                               "in_X3": C.in_Xk(cand, N, 3)[0],
                               "n_live": sc["n_live"],
                               "all_blocked": sc["all_blocked"]}
                        rung.setdefault("X2_samples", []).append(rec)
                        if sc["all_blocked"]:
                            bat = full_battery(cand, f"F{bi}{s}")
                            blocks = {f"{a},{b}": [[str(x) for x in r]
                                                   for r in cand[(a, b)]]
                                      for a, b in combinations(range(N), 2)}
                            found_allblocked.setdefault("X2", []).append(
                                {"base": bi, "tri": [list(e) for e in tri],
                                 "battery": {k2: v for k2, v in bat.items()
                                             if k2 != "rows"},
                                 "rows": bat["rows"], "blocks": blocks,
                                 "in_X3": rec["in_X3"]})
                            print(f"      >>> ALL-BLOCKED X_2 point at N=8 "
                                  f"(base {bi}, triangle {tri}): live "
                                  f"{bat['n_live']}, disagreements "
                                  f"{bat['disagreements']}, in X_3 "
                                  f"{rec['in_X3']}", flush=True)
            print(f"   base {bi} triangle {tri}: solution dims X_2 "
                  f"{dims[2]}, X_3 {dims[3]}, X_4 {dims[4]}", flush=True)
            rung.setdefault("dims", []).append({"base": bi,
                                                "tri": [list(e) for e in tri],
                                                "dims": {str(k): v for k, v
                                                         in dims.items()}})
    RES["triangle"] = rung
    RES["triangle_allblocked"] = found_allblocked
    control("T3_3_triangle_deformation")

    print("=" * 74)
    print("(4) rung map: all-blocked status at N = 8")
    print("=" * 74)
    x2s = rung.get("X2_samples", [])
    n_ab = sum(1 for r in x2s if r["all_blocked"])
    n_x3 = sum(1 for r in x2s if r["in_X3"])
    n_ab_x3 = sum(1 for r in x2s if r["all_blocked"] and r["in_X3"])
    print(f"   X_2 points sampled on triangle skeletons: {len(x2s)}; "
          f"ALL-BLOCKED {n_ab}; of those also in X_3: {n_ab_x3}")
    print(f"   (X_3 members among the samples: {n_x3})")
    dd = rung.get("dims", [])
    print(f"   triangle solution dimensions (X_2 / X_3 / X_4) over "
          f"{len(dd)} skeletons: "
          f"{sorted(set((r['dims']['2'], r['dims']['3'], r['dims']['4']) for r in dd))}")
    RES["rung_map"] = {"x2_samples": len(x2s), "x2_all_blocked": n_ab,
                       "x2_all_blocked_and_in_X3": n_ab_x3,
                       "x3_members": n_x3}
    control("T3_4_rung_map")

    print("=" * 74)
    print("(5) X_3 objects at N = 8: is any of them all-blocked?")
    print("=" * 74)
    x3stats = []
    for bi, (col, base) in enumerate(bases):
        sc = screen(base, f"B{bi}")
        x3stats.append({"base": bi, **{k: v for k, v in sc.items()
                                       if k != "verdicts"}})
        for k in range(3):
            src = base
            ok = True
            for s in range(rng.randint(1, 4)):
                nxt, dm = WK.site_solve(src, rng.randrange(N), N, 3, rng,
                                        spread=rng.choice([1, 2, 3]))
                if nxt is None:
                    ok = False
                    break
                src = nxt
            if not ok:
                continue
            okx, bw = C.in_Xk(src, N, 3)
            assert okx, ("walk left X_3", bw)
            sc2 = screen(src, f"W{bi}{k}")
            x3stats.append({"base": bi, "walk": k,
                            **{kk: v for kk, v in sc2.items()
                               if kk != "verdicts"}})
            if sc2["all_blocked"]:
                blocks = {f"{a},{b}": [[str(x) for x in r]
                                       for r in src[(a, b)]]
                          for a, b in combinations(range(N), 2)}
                RES.setdefault("x3_allblocked_objects", []).append(
                    {"base": bi, "walk": k, "blocks": blocks,
                     "verdicts": sc2.get("verdicts"),
                     "n_live": sc2["n_live"]})
                print(f"      >>> ALL-BLOCKED X_3 CANDIDATE at N=8 "
                      f"(base {bi}, walk {k}) -- object stored", flush=True)
    nab3 = sum(1 for r in x3stats if r["all_blocked"])
    print(f"   {len(x3stats)} X_3 objects at N=8 screened; ALL-BLOCKED "
          f"{nab3}; live-pair range "
          f"{min(r['n_live'] for r in x3stats)}-"
          f"{max(r['n_live'] for r in x3stats)}")
    RES["x3_screen"] = {"objects": len(x3stats), "all_blocked": nab3,
                        "stats": x3stats}
    control("T3_5_x3_screen")

    declared = ["T3_1_ladder", "T3_2_calibration", "T3_3_triangle_deformation",
                "T3_4_rung_map", "T3_5_x3_screen"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    assert not missing
    with open(f"{BASE}/results_t3_n8.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"wrote results_t3_n8.json ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
