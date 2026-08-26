#!/usr/bin/env python3
"""W25 T1c -- THE ALL-BLOCKED LOCUS OF X_2 AT N=6, AND HOW X_3 MEETS IT.

W23 exhibited four all-blocked points of X_2 among general N=6 sources; all
four have the same rank profile (one dead pair, twelve rank-one blocks, two
rank-THREE blocks).  This runner identifies the locus exactly.

STRUCTURE FOUND.  Every one of the four is

    (a DIAGONAL X_2 = X_3 source of skeleton class (4,4,4))
    +  two extra FULL-RANK blocks at (0,2) and (1,2),  with (0,1) dead,

i.e. a deformation of a diagonal point supported on the three blocks of the
triangle {0,1,2} -- three blocks NO perfect matching can use twice (they
pairwise share a vertex), so H_B(A)_w is LINEAR in the 27 unknown entries
jointly.  Membership in X_k restricted to that skeleton is therefore an exact
inhomogeneous LINEAR system, solved here in closed form.

RESULT.  On this skeleton, X_2 is an affine space of positive dimension whose
GENERIC point is all-blocked; adding the three-off (X_3) equations collapses it
to the single point where the two extra blocks VANISH -- the diagonal X_3 point
itself, which carries 9 witnesses.  So X_3 kills exactly the deformation that
made X_2 all-blocked.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, product

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

N = 6
RES = {}
RAN = []
TRI = [(0, 1), (0, 2), (1, 2)]


def control(name):
    RAN.append(name)


def unknown_cols():
    return [(e, i, j) for e in TRI for i in range(3) for j in range(3)]


def linear_system(base, k):
    """H_w is linear in the 27 triangle entries (no PM uses two of the three
    triangle edges).  Build rows/rhs for membership in X_k."""
    cols = unknown_cols()
    idx = {t: i for i, t in enumerate(cols)}
    words = C.near_constant_words(N, 3, k)
    rows, rhs, tags = [], [], []
    for w in words:
        row = [Fraction(0)] * len(cols)
        # constant term: H with all three triangle blocks zeroed
        z = C.copy_source(base)
        for e in TRI:
            z[e] = [[Fraction(0)] * 3 for _ in range(3)]
        const = C.H(z, w, N)
        for e in TRI:
            for i in range(3):
                for j in range(3):
                    t = C.copy_source(z)
                    t[e][i][j] = Fraction(1)
                    row[idx[(e, i, j)]] = C.H(t, w, N) - const
        tgt = Fraction(1) if len(set(w)) == 1 else Fraction(0)
        rows.append(row)
        rhs.append(tgt - const)
        tags.append(w)
    return rows, rhs, cols, tags


def apply_sol(base, vec, cols):
    out = C.copy_source(base)
    for e in TRI:
        out[e] = [[Fraction(0)] * 3 for _ in range(3)]
    for k, (e, i, j) in enumerate(cols):
        out[e][i][j] = vec[k]
    return out


def battery(src, tag, cross=True):
    rows = []
    for p, q in combinations(range(N), 2):
        lv = C.live(src, p, q)
        row = {"pair": [p, q], "live": lv,
               "rank": C.matrix_rank(C.oriented(src, p, q))}
        if lv:
            U = tuple(x for x in range(N) if x not in (p, q))
            v1, d1, mp = D.decide_pair(src, p, q, U, f"{tag}A{p}{q}")
            row.update({"w25": v1, "dimQ": d1, "modp": mp})
            if cross:
                isrc, _ = C.clear_denominators(src)
                v2, _, _ = W23D.decide_pair(isrc, p, q, U, f"{tag}B{p}{q}",
                                            primes=(32003,))
                row["w23"] = v2
                row["agree"] = v1 == v2
        rows.append(row)
    lv = [r for r in rows if r["live"]]
    return {"in_X2": C.in_Xk(src, N, 2)[0], "in_X3": C.in_Xk(src, N, 3)[0],
            "n_live": len(lv),
            "n_witness": sum(1 for r in lv if r["w25"] == "WITNESS"),
            "all_blocked": bool(lv) and all(r["w25"] == "BLOCKED" for r in lv),
            "disagreements": sum(1 for r in lv if not r.get("agree", True)),
            "modp_mismatch": sum(1 for r in lv for ch, dd in r["modp"].items()
                                 if (dd == -1) != (r["dimQ"] == -1)),
            "ranks": sorted(r["rank"] for r in rows), "rows": rows}


def main():
    rng = random.Random(606)
    objs = C.w23_allblocked_x2()
    print("=" * 74)
    print("(1) reproduction control: W23's four all-blocked X_2 objects, "
          "re-decided by W25's INDEPENDENT decider")
    print("=" * 74)
    repro = []
    for i, src in enumerate(objs):
        bat = battery(src, f"AB{i}")
        print(f"   object {i}: in X_2 {bat['in_X2']}, in X_3 {bat['in_X3']}, "
              f"live {bat['n_live']}, witness {bat['n_witness']}, "
              f"ALL-BLOCKED {bat['all_blocked']}, disagreements "
              f"{bat['disagreements']}, mod-p {bat['modp_mismatch']}, "
              f"ranks {bat['ranks']}")
        repro.append({k: v for k, v in bat.items() if k != "rows"})
        assert bat["all_blocked"] and bat["in_X2"] and not bat["in_X3"]
        assert bat["disagreements"] == 0 and bat["modp_mismatch"] == 0
    RES["reproduction"] = repro
    control("T1c1_reproduction")

    print("=" * 74)
    print("(2) the skeleton: DIAGONAL core + the triangle {0,1,2}")
    print("=" * 74)
    base = C.copy_source(objs[0])
    core = {f"{e[0]},{e[1]}": [[str(x) for x in row] for row in base[e]]
            for e in base if e not in TRI}
    diagcore = all(len([(i, j) for i in range(3) for j in range(3)
                        if base[e][i][j] != 0]) <= 1
                   for e in base if e not in TRI)
    print(f"   the 12 non-triangle blocks are monochrome rank <= 1: "
          f"{diagcore}")
    for e in TRI:
        print(f"   triangle block {e}: "
              f"{[[str(x) for x in row] for row in base[e]]} "
              f"(rank {C.matrix_rank(base[e])})")
    RES["skeleton"] = {"diagonal_core": diagcore, "core": core}
    assert diagcore
    control("T1c2_skeleton")

    print("=" * 74)
    print("(3) X_2 and X_3 on the skeleton, in closed form (LINEAR: no PM "
          "uses two triangle edges)")
    print("=" * 74)
    out = {}
    sols = {}
    for k in (2, 3):
        rows, rhs, cols, tags = linear_system(base, k)
        part, kern = C.solve_linear(rows, rhs, len(cols))
        assert part is not None, f"X_{k} infeasible on the skeleton"
        out[k] = {"equations": len(rows), "unknowns": len(cols),
                  "solution_dim": len(kern)}
        sols[k] = (part, kern, cols)
        print(f"   X_{k}: {len(rows)} equations, {len(cols)} unknowns -> "
              f"affine solution space of dimension {len(kern)}")
    part3, kern3, cols3 = sols[3]
    zero3 = all(x == 0 for x in part3) and not kern3
    print(f"   X_3 solution is the SINGLE point with all three triangle "
          f"blocks ZERO: {zero3}")
    RES["linear_systems"] = out
    RES["x3_forces_zero"] = zero3
    assert zero3
    control("T1c3_linear_closed_form")

    print("=" * 74)
    print("(4) is the whole X_2 solution space all-blocked?")
    print("=" * 74)
    part2, kern2, cols2 = sols[2]
    recs = []
    nab = 0
    for t in range(10):
        vec = list(part2)
        if t:
            for kv in kern2:
                lam = Fraction(rng.randint(-3, 3))
                if lam:
                    vec = [a + lam * b for a, b in zip(vec, kv)]
        src = apply_sol(base, vec, cols2)
        ok, bw = C.in_Xk(src, N, 2)
        assert ok, ("point left X_2", bw)
        bat = battery(src, f"L{t}", cross=(t < 3))
        nab += int(bat["all_blocked"])
        recs.append({"t": t, "in_X3": bat["in_X3"], "n_live": bat["n_live"],
                     "n_witness": bat["n_witness"],
                     "all_blocked": bat["all_blocked"],
                     "ranks": bat["ranks"],
                     "disagreements": bat["disagreements"],
                     "modp_mismatch": bat["modp_mismatch"]})
        print(f"   point {t}: live {bat['n_live']}, witness "
              f"{bat['n_witness']}, ALL-BLOCKED {bat['all_blocked']}, "
              f"in X_3 {bat['in_X3']}, ranks {bat['ranks']}")
    print(f"   all-blocked at {nab}/10 sampled points of the "
          f"{len(kern2)}-dimensional X_2 solution space")
    RES["x2_locus_points"] = recs
    RES["x2_locus_allblocked"] = nab
    control("T1c4_x2_locus_sampling")

    print("=" * 74)
    print("(5) EXPLICIT-POINT CONTROL OUTSIDE the asserted locus (ledger 18)")
    print("=" * 74)
    src0 = apply_sol(base, [Fraction(0)] * len(cols2), cols2)
    b0 = battery(src0, "Z0", cross=False)
    print(f"   the triangle-zero point (= the diagonal X_3 source): in X_2 "
          f"{b0['in_X2']}, in X_3 {b0['in_X3']}, live {b0['n_live']}, "
          f"witness {b0['n_witness']}, ALL-BLOCKED {b0['all_blocked']}")
    RES["control_zero_point"] = {k: v for k, v in b0.items() if k != "rows"}
    assert b0["in_X3"] and b0["n_witness"] > 0 and not b0["all_blocked"]
    control("T1c5_explicit_point_control")

    print("=" * 74)
    print("(6) the same analysis on the other three W23 objects")
    print("=" * 74)
    same = []
    for i, o in enumerate(objs):
        rows, rhs, cols, tags = linear_system(o, 3)
        p3, k3 = C.solve_linear(rows, rhs, len(cols))
        rows2, rhs2, cols2b, _ = linear_system(o, 2)
        p2, k2 = C.solve_linear(rows2, rhs2, len(cols2b))
        same.append({"obj": i, "x2_dim": None if p2 is None else len(k2),
                     "x3_dim": None if p3 is None else len(k3),
                     "x3_is_zero": p3 is not None and not k3
                                   and all(x == 0 for x in p3)})
        print(f"   object {i}: X_2 solution dim "
              f"{same[-1]['x2_dim']}, X_3 solution dim {same[-1]['x3_dim']}, "
              f"X_3 forces the triangle to zero: {same[-1]['x3_is_zero']}")
    RES["all_four"] = same
    assert all(s["x3_is_zero"] for s in same)
    control("T1c6_all_four_objects")

    declared = ["T1c1_reproduction", "T1c2_skeleton",
                "T1c3_linear_closed_form", "T1c4_x2_locus_sampling",
                "T1c5_explicit_point_control", "T1c6_all_four_objects"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    assert not missing
    with open(f"{BASE}/results_t1c_x2locus.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t1c_x2locus.json")


if __name__ == "__main__":
    main()
