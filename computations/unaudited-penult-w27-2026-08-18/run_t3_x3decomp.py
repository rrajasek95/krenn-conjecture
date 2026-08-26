#!/usr/bin/env python3
"""W27 T3 -- DECOMPOSE THE X_3 VARIETY AT N = 6.

W27-R1 applied at N = 6: A lies in X_3 iff, at any site z, the three colour
systems (15 unknowns each, 213 equations each) are consistent, and consistency
is exactly

    r_const^{(c)}  NOT in the row span of the mixed rows,

which in particular forces  rank(mixed rows) <= 14  --  a NON-generic
condition on the K_5 background.  So X_3 fibres over the space of K_5
backgrounds, with an affine fibre of dimension  sum_c (15 - rank_c)  over each
feasible background.  This runner uses that fibration as the stratification:

  * builds a large family of exact X_3 points at N = 6 from four independent
    seed families;
  * records, for every point, the full 6 x 3 table of site/colour kernel
    dimensions (the STRATUM SIGNATURE) plus support data;
  * decides EVERY live pair exactly (Singular, Rabinowitsch) and reports the
    witness count per stratum -- looking for any all-blocked point;
  * isolates the rigid stratum (kernel [0,0,0] at a site: the star there is
    determined by the background) and measures it.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
W25BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-x3core-w25-2026-08-15")
W23BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W25BASE)
sys.path.insert(0, W23BASE)
import w27_core as W                                              # noqa: E402
import w27_x4 as X                                                # noqa: E402
import w25_walk as WK                                             # noqa: E402
import w25_decide as D                                            # noqa: E402
import run_t1d_diagonal as T1D                                    # noqa: E402
import run_t1e_diagonal_uniform as T1E                            # noqa: E402
C = W.C

N = 6
RES = {"points": []}
RAN = []
OUT = f"{BASE}/results_t3_x3decomp.json"
WORDS3 = None


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def signature(src):
    """The 6 x 3 table of (rank_mixed, kernel) for the X_3 systems, plus the
    exact kernel dimensions of the FULL systems (W25's site_dims)."""
    sm = X.src_mod(src, X.P1, n=N)
    tabs = X.cof_tables(sm, X.P1, n=N)
    tab = []
    for z in range(N):
        row = []
        for c in range(3):
            rows, rhs, tags, cols = X.build_rows(tabs, WORDS3, z, c, n=N)
            ok, rmix, rall = X.feasible_mod(rows, rhs, len(cols), X.P1)
            row.append({"feasible": ok, "rank_mixed": rmix,
                        "kernel": len(cols) - rall})
        tab.append(row)
    return tab


def decide_all(src, tag):
    rows = []
    for p, q in combinations(range(N), 2):
        if not C.live(src, p, q):
            continue
        U = tuple(x for x in range(N) if x not in (p, q))
        v, d, mp = D.decide_pair(src, p, q, U, f"{tag}_{p}{q}", primes=())
        rows.append({"pair": [p, q], "verdict": v, "dim": d,
                     "rank": C.matrix_rank(C.oriented(src, p, q))})
    return rows


def seeds(rng):
    out = []
    # (a) the committed near-exact six-site source
    out.append(("near_exact", C.near_exact_six_site()))
    # (b) Delta^3_6
    out.append(("delta3_6", C.delta3_N(6)))
    # (c) the 24 diagonal classes, one exact point each
    surv = T1E._survivors()
    classes = sorted(set(T1D.canonical(Ls) for Ls in surv))
    for i, cn in enumerate(classes):
        pts = T1E.sample_points(cn, rng, k=1)
        if pts:
            out.append((f"diag_class{i}", T1D.build_source(cn, pts[0])))
    # (d) W23's all-blocked X_2 objects (they are NOT in X_3; project them)
    try:
        for j, s in enumerate(C.w23_allblocked_x2()):
            out.append((f"w23_allblockedX2_{j}", s))
    except Exception as ex:                                       # noqa: BLE001
        print(f"   (w23 objects unavailable: {ex})")
    return out


def main():
    global WORDS3
    t0 = time.time()
    rng = random.Random(1234567)
    WORDS3 = list(C.near_constant_words(N, 3, 3))
    print(f"X_3 words at N=6: {len(WORDS3)} (of 729; the 90 (2,2,2) words are "
          f"exactly what separates X_3 from EXACT)")
    RES["n_words"] = len(WORDS3)

    print("=" * 74)
    print("(0) CONTROL: at N=6 the only profile of off-count > 3 is (2,2,2)")
    print("=" * 74)
    profs = [p for p in W.profiles(N, 3) if max(p) != N]
    hi = sorted(set(tuple(sorted(p, reverse=True)) for p in profs
                    if N - max(p) > 3))
    print(f"   profiles with off-count > 3: {hi}")
    assert hi == [(2, 2, 2)], hi
    n222 = sum(1 for w in __import__("itertools").product(range(3), repeat=N)
               if sorted([sum(1 for x in w if x == c) for c in range(3)])
               == [2, 2, 2])
    print(f"   number of (2,2,2) words: {n222} => EXACT = X_3 + {n222} "
          f"equations at N=6")
    RES["gap_to_exact"] = n222
    control("T3_0_profiles")
    ck("profiles")

    print("=" * 74)
    print("(1) BUILD X_3 points at N=6 (four independent seed families + "
          "site-linear walks)")
    print("=" * 74)
    pts = []
    for name, s in seeds(rng):
        ok3 = C.in_Xk(s, N, 3)[0]
        if ok3:
            pts.append((name, s))
        else:
            # project into X_3 by one site solve
            for z in range(N):
                cur, dims = WK.site_solve(s, z, N, 3, keep_particular=True)
                if cur is not None and C.in_Xk(cur, N, 3)[0]:
                    pts.append((f"{name}_proj{z}", cur))
                    break
    print(f"   direct seeds landing in X_3: {len(pts)}")
    walked = []
    for name, s in list(pts):
        for k in range(3):
            cur = s
            good = True
            for st in range(rng.randint(1, 3)):
                nxt, dm = WK.site_solve(cur, rng.randrange(N), N, 3, rng,
                                        spread=rng.choice([1, 2, 3]))
                if nxt is None:
                    good = False
                    break
                cur = nxt
            if good and C.in_Xk(cur, N, 3)[0]:
                walked.append((f"{name}_w{k}", cur))
    pts += walked
    print(f"   after site-linear walks: {len(pts)} exact X_3 points")
    RES["n_points"] = len(pts)
    control("T3_1_build")
    ck("build")

    print("=" * 74)
    print("(2) STRATIFY and DECIDE")
    print("=" * 74)
    strata = {}
    allblocked = []
    recs = []
    for i, (name, s) in enumerate(pts):
        assert C.in_Xk(s, N, 3)[0]
        sig = signature(s)
        kers = [[sig[z][c]["kernel"] for c in range(3)] for z in range(N)]
        rks = [[sig[z][c]["rank_mixed"] for c in range(3)] for z in range(N)]
        key = str(sorted(tuple(x) for x in kers))
        live = [(p, q) for p, q in combinations(range(N), 2) if C.live(s, p, q)]
        rows = decide_all(s, f"T3_{i}")
        nw = sum(1 for r in rows if r["verdict"] == "WITNESS")
        rec = {"name": name, "kernels": kers, "rank_mixed": rks,
               "n_live": len(live), "n_witness": nw,
               "all_blocked": bool(live) and nw == 0,
               "stratum": key,
               "n_frozen_sites": sum(1 for k in kers if k == [0, 0, 0]),
               "n_zero_blocks": 15 - len(live),
               "verdicts": [[r["pair"], r["verdict"]] for r in rows]}
        recs.append(rec)
        strata.setdefault(key, []).append(nw)
        if rec["all_blocked"]:
            allblocked.append({**rec,
                               "blocks": {f"{a},{b}": [[str(x) for x in row]
                                                       for row in s[(a, b)]]
                                          for a, b in combinations(range(N), 2)}})
        RES["points"] = recs
        RES["all_blocked"] = allblocked
        if i % 5 == 0:
            print(f"   [{i:3d}/{len(pts)}] {name:26s} live {len(live):2d} "
                  f"witnesses {nw:2d} frozen sites {rec['n_frozen_sites']}",
                  flush=True)
            ck(f"pt{i}")
    print(f"   points decided: {len(recs)}; ALL-BLOCKED found: "
          f"{len(allblocked)}")
    control("T3_2_stratify")
    ck("stratify")

    print("=" * 74)
    print("(3) THE STRATA")
    print("=" * 74)
    lines = []
    for k in sorted(strata, key=lambda x: (-len(strata[x]), x)):
        v = strata[k]
        line = (f"   n={len(v):3d}  min witnesses {min(v):2d}  max {max(v):2d} "
                f" signature {k[:88]}")
        print(line)
        lines.append(line)
    RES["strata"] = {k: {"n": len(v), "min_witness": min(v), "max": max(v)}
                     for k, v in strata.items()}
    RES["strata_lines"] = lines
    mins = min(min(v) for v in strata.values())
    print(f"   MINIMUM witness count over every X_3 point built: {mins}")
    RES["global_min_witness"] = mins
    control("T3_3_strata")

    print("=" * 74)
    print("(4) THE RIGID STRATUM (frozen sites)")
    print("=" * 74)
    byfrozen = {}
    for r in recs:
        byfrozen.setdefault(r["n_frozen_sites"], []).append(r["n_witness"])
    for k in sorted(byfrozen):
        v = byfrozen[k]
        print(f"   {k} frozen sites: {len(v)} points; witnesses min {min(v)} "
              f"max {max(v)}")
    RES["by_frozen"] = {str(k): {"n": len(v), "min": min(v), "max": max(v)}
                        for k, v in byfrozen.items()}
    control("T3_4_rigid")

    declared = ["T3_0_profiles", "T3_1_build", "T3_2_stratify", "T3_3_strata",
                "T3_4_rigid"]
    missing = [x for x in declared if x not in RAN]
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
