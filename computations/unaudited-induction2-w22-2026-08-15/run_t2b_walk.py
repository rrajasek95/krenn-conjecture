#!/usr/bin/env python3
"""W22 T2b -- an EXACT block-wise linear walk on the mixed-exact variety.

BLOCK LINEARITY (a corollary of the same "every PM covers an edge at most
once" fact that gives site linearity): every mixed equation is LINEAR in the
nine entries of any single block A_uv, with coefficients Haf_{B-u-v}(A)_w.
So, holding all other blocks fixed at a mixed-exact point, the admissible
values of A_uv form a LINEAR SUBSPACE containing the current one.  Sampling
it and iterating is an exact random walk on the mixed-exact variety.

Used to manufacture N = 6 mixed-exact sources with FULL-RANK blocks -- the
regime J.1b-support is about, and the regime the constant-block family
(all blocks rank one) cannot reach.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-induction2-w22-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-slice-dirtiness-w5-2026-08-15")
import w22_core as W                                        # noqa: E402
import w22_n6 as N6                                         # noqa: E402
import w22_sitelin as SL                                    # noqa: E402
import slice_core                                           # noqa: E402

N = 6
PAIRS = list(combinations(range(N), 2))
RES = {}


def block_system(src, e, n, ncol=3, mixed_only=True):
    """Rows of the linear system in the nine entries of block A_e."""
    u, v = e
    rest = tuple(x for x in range(n) if x not in e)
    cols = [(i, j) for i in range(ncol) for j in range(ncol)]
    idx = {c: k for k, c in enumerate(cols)}
    rows, rhs, tags = [], [], []
    for word in product(range(ncol), repeat=n):
        const = len(set(word)) == 1
        if const and mixed_only:
            continue
        tab = {(a, b): W.oriented(src, a, b, ncol)
               for a, b in combinations(rest, 2)}
        wo = {a: word[a] for a in rest}
        cof = W._haf_tensor(tab, rest, wo, ncol)
        row = [Fraction(0)] * len(cols)
        row[idx[(word[u], word[v])]] = Fraction(cof)
        rows.append(row)
        rhs.append(Fraction(1) if const else Fraction(0))
        tags.append(word)
    return rows, rhs, cols, tags


def walk(src, rng, steps=40, lo=-3, hi=3):
    cur = {e: [row[:] for row in m] for e, m in src.items()}
    for _ in range(steps):
        e = rng.choice(PAIRS)
        rows, rhs, cols, _ = block_system(cur, e, N)
        part, kern = SL.solve_linear(rows, rhs)
        if part is None or not kern:
            continue
        vec = [Fraction(0)] * len(cols)
        for k in kern:
            lam = Fraction(rng.randint(lo, hi))
            vec = [a + lam * b for a, b in zip(vec, k)]
        if all(x == 0 for x in vec):
            continue
        newblk = [[Fraction(0)] * 3 for _ in range(3)]
        for k, (i, j) in enumerate(cols):
            newblk[i][j] = part[k] + vec[k]
        # keep integers where possible
        den = 1
        for r in newblk:
            for x in r:
                den = den * x.denominator // __import__("math").gcd(
                    den, x.denominator)
        cur[e] = [[int(x * den) if (x * den).denominator == 1 else x * den
                   for x in r] for r in newblk]
    return cur


def main():
    rng = random.Random(31337)

    def haf_t(tt):
        s = 0
        for M in W.perfect_matchings(tuple(range(N))):
            term = 1
            for a, b in M:
                term *= tt[W.ekey(a, b)]
            s += term
        return s

    def const_block_mixed_exact():
        while True:
            t = {e: rng.randint(-5, 5) for e in PAIRS}
            t[(0, 1)] = 0
            b0 = haf_t(t)
            t[(0, 1)] = 1
            c0 = haf_t(t) - b0
            if c0 == 0:
                continue
            v = Fraction(-b0, c0)
            d = v.denominator
            tt = {e: (int(v * d) if e == (0, 1) else int(val * d))
                  for e, val in t.items()}
            if any(x == 0 for x in tt.values()) or haf_t(tt) != 0:
                continue
            return tt

    # ---- build a fleet of mixed-exact sources with full-rank blocks --------
    fleet = []
    for trial in range(30):
        src = N6.source_P0_constant(const_block_mixed_exact(), N)
        w = walk(src, rng, steps=45)
        if not N6.is_mixed_exact(w, N):
            continue
        ranks = [W.matrix_rank(W.oriented(w, a, b)) for a, b in PAIRS]
        pu = W.pures(w, N)
        fleet.append({"src": w, "ranks": ranks,
                      "n_fullrank": sum(1 for r in ranks if r == 3),
                      "pures": [pu[c] for c in range(3)]})
    print(f"fleet: {len(fleet)} mixed-exact walked sources; "
          f"full-rank pairs total {sum(f['n_fullrank'] for f in fleet)}; "
          f"rank histogram "
          f"{ {r: sum(x.count(r) for x in [f['ranks'] for f in fleet]) for r in (0,1,2,3)} }")
    RES["fleet"] = {"n": len(fleet),
                    "n_fullrank_pairs": sum(f["n_fullrank"] for f in fleet),
                    "pure_profiles": sorted(set(
                        tuple(1 if x != 0 else 0 for x in f["pures"])
                        for f in fleet))}
    print("pure profiles seen:", RES["fleet"]["pure_profiles"])

    # ---- (3) J.1b falsifier: full-rank pair, all three slices dirty --------
    rows = []
    for si, f in enumerate(fleet):
        s = f["src"]
        for p, q in PAIRS:
            if W.matrix_rank(W.oriented(s, p, q)) != 3:
                continue
            U = tuple(x for x in range(N) if x not in (p, q))
            dirt = []
            for c in range(3):
                wc = {W.ekey(a, b): W.oriented(s, a, b)[c][c]
                      for a, b in combinations(range(N), 2)}
                dirt.append(slice_core.slice_error(wc, p, q, U) != 0)
            rows.append({"source": si, "pair": [p, q], "dirty": dirt,
                         "all3": all(dirt),
                         "nzdiag": all(W.oriented(s, p, q)[c][c] != 0
                                       for c in range(3))})
    RES["j1b_rows"] = {"full_rank_pairs": len(rows),
                       "all_three_dirty": sum(1 for r in rows if r["all3"]),
                       "all_three_dirty_and_nzdiag":
                           sum(1 for r in rows if r["all3"] and r["nzdiag"]),
                       "dirty_count_hist": {}}
    hist = {}
    for r in rows:
        k = sum(r["dirty"])
        hist[k] = hist.get(k, 0) + 1
    RES["j1b_rows"]["dirty_count_hist"] = hist
    print(f"[J.1b] full-rank pairs on MIXED-EXACT N=6 sources: {len(rows)}; "
          f"#dirty-colour histogram {hist}; all-three-dirty "
          f"{RES['j1b_rows']['all_three_dirty']}")

    # ---- blocking census on the walked fleet ------------------------------
    cen = []
    for si, f in enumerate(fleet[:8]):
        s = f["src"]
        nl = nb = 0
        for p, q in PAIRS:
            if not N6.live(s, p, q):
                continue
            nl += 1
            U = tuple(x for x in range(N) if x not in (p, q))
            v, _ = N6.decide_pair_general(s, p, q, U, f"W{si}_{p}{q}")
            nb += int(v == "BLOCKED")
        cen.append({"source": si, "n_live": nl, "n_blocked": nb,
                    "all_blocked": nl == nb, "n_fullrank": f["n_fullrank"],
                    "pures": [str(x) for x in f["pures"]]})
        print(f"   walked source {si}: live={nl} blocked={nb} "
              f"ALL_BLOCKED={nl == nb} fullrank={f['n_fullrank']} "
              f"pures={cen[-1]['pures']}")
    RES["walked_blocking"] = cen

    # ---- POSITIVE CONTROL for the pure-forcing test (ledger 13b / 17) -----
    # On Delta_{4,3} (an EXACT ternary source) the same site test MUST report
    # solvable, and the kernel must be nontrivial.
    import importlib
    d43 = {e: [[0] * 3 for _ in range(3)] for e in combinations(range(4), 2)}
    for c, M in enumerate([((0, 1), (2, 3)), ((0, 2), (1, 3)),
                           ((0, 3), (1, 2))]):
        for e in M:
            d43[e][c][c] = 1
    pos = []
    for z in range(4):
        sysd = SL.site_systems(d43, z, 4, include_pures=True)
        sysm = SL.site_systems(d43, z, 4, include_pures=False)
        row = {"site": z}
        for c in range(3):
            part, kern = SL.solve_linear(sysd[c][0], sysd[c][1])
            pm, km = SL.solve_linear(sysm[c][0], sysm[c][1])
            row[f"c{c}_solvable_with_pure"] = part is not None
            row[f"c{c}_ker_mixed"] = len(km) if km is not None else None
        pos.append(row)
    RES["positive_control_delta43"] = pos
    print("[positive control] Delta_{4,3} site systems (must be solvable):")
    for r in pos:
        print("   ", r)

    # ---- NON-VACUITY certificate for the N=6 forcing ----------------------
    src = N6.source_P0_constant(const_block_mixed_exact(), N)
    nv = []
    for z in range(N):
        sysm = SL.site_systems(src, z, N, include_pures=False)
        sysd = SL.site_systems(src, z, N, include_pures=True)
        for c in range(3):
            pm, km = SL.solve_linear(sysm[c][0], sysm[c][1])
            part, _ = SL.solve_linear(sysd[c][0], sysd[c][1])
            nv.append({"site": z, "colour": c, "dim_ker_mixed": len(km),
                       "pure_reachable": part is not None})
    RES["nonvacuity_n6"] = nv
    print("[non-vacuity] N=6 constant-block: dim ker(mixed) per (site,colour) "
          f"= {sorted(set(r['dim_ker_mixed'] for r in nv))}, "
          f"pure reachable in {sum(1 for r in nv if r['pure_reachable'])}"
          f"/{len(nv)}")

    with open(f"{BASE}/results_t2b_walk.json", "w") as fh:
        json.dump({k: v for k, v in RES.items()}, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
