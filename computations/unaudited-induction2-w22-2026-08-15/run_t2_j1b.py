#!/usr/bin/env python3
"""W22 T2 -- J.1b-support (Gap A') via site linearity.

(1) Verify the STAR IDENTITY (Lemma W22-S) and its CONTRACTION (*) on genuine
    EXACT sources: Delta_{4,3} (the K_4 ternary exception) and Delta_{N,2}
    (two colours, every even N).  Mutation controls.
(2) Use W22-L (site linearity) to build RICH mixed-exact N=6 sources with
    FULL-RANK blocks by exact linear solves through the constant-block family.
(3) Search those for the J.1b falsifier shape: a FULL-RANK pair at which all
    three colour slices are DIRTY.
(4) Decide, exactly, which PURE PROFILES a site-z modification can reach --
    a mechanised instance of the six-site theorem, and the shape of the
    argument at general N.
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

RES = {}


def delta43():
    """Delta_{4,3}: the three perfect matchings of K_4, matching c carrying
    colour c at both endpoints."""
    src = {e: [[0] * 3 for _ in range(3)] for e in combinations(range(4), 2)}
    pms = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    for c, M in enumerate(pms):
        for e in M:
            src[e][c][c] = 1
    return src


def delta_n2(n):
    """Delta_{N,2} as a genuine TWO-colour source (2x2 blocks)."""
    M0, M1 = N6.delta_n2_cycle(n)
    src = {e: [[0, 0], [0, 0]] for e in combinations(range(n), 2)}
    for e in M0:
        src[W.ekey(*e)][0][0] = 1
    for e in M1:
        src[W.ekey(*e)][1][1] = 1
    return src


def main():
    rng = random.Random(9091)

    # ================= (1) the star identity on EXACT sources ==============
    checks = []
    src = delta43()
    assert W.ghz_defects(src, 4) == [], "Delta_{4,3} is not exact"
    for z in range(4):
        for c in range(3):
            r = SL.star_identity_residual(src, z, c, 4)
            checks.append(("delta43", z, c, r))
    for n in (6, 8, 10):
        s2 = delta_n2(n)
        assert W.ghz_defects(s2, n, ncol=2) == [], f"Delta_{n},2 not exact"
        for z in range(n):
            for c in range(2):
                r = SL.star_identity_residual(s2, z, c, n, ncol=2)
                checks.append((f"delta{n}2", z, c, r))
    bad = [c for c in checks if any(x != 0 for x in c[3])]
    RES["star_identity"] = {"checked": len(checks), "violations": len(bad)}
    print(f"[W22-S] star identity: {len(checks)} (site,colour) instances, "
          f"{len(bad)} violations")

    # contraction identity (*) at random u
    cbad = ctot = 0
    for _ in range(60):
        s = delta43()
        p = rng.randrange(4)
        u = [rng.randint(-5, 5) for _ in range(3)]
        for c in range(3):
            ctot += 1
            if SL.contraction_identity_residual(s, p, u, c, 4) != 0:
                cbad += 1
    for n in (6, 8):
        s2 = delta_n2(n)
        for _ in range(30):
            p = rng.randrange(n)
            u = [rng.randint(-5, 5) for _ in range(2)]
            for c in range(2):
                ctot += 1
                if SL.contraction_identity_residual(s2, p, u, c, n, ncol=2) != 0:
                    cbad += 1
    RES["contraction_identity"] = {"checked": ctot, "violations": cbad}
    print(f"[W22-S*] contraction identity: {ctot} instances, {cbad} violations")

    # MUTATION control: perturb one cell of an exact source -> identity must
    # break somewhere
    fired = trials = 0
    for _ in range(40):
        s = delta43()
        e = rng.choice(list(s))
        i, j = rng.randrange(3), rng.randrange(3)
        s[e][i][j] += rng.choice([1, -1, 2])
        trials += 1
        if any(any(x != 0 for x in SL.star_identity_residual(s, z, c, 4))
               for z in range(4) for c in range(3)):
            fired += 1
    RES["star_identity_mutation"] = {"trials": trials, "fired": fired}
    print(f"[control] mutation of an exact source breaks the star identity: "
          f"{fired}/{trials}")

    # ================= (2) site-linear deformation at N = 6 ================
    N = 6
    PAIRS = list(combinations(range(N), 2))

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
            if any(x == 0 for x in tt.values()):
                continue
            if haf_t(tt) != 0:
                continue
            return tt

    deform = []
    fullrank_sources = []
    for trial in range(8):
        t = const_block_mixed_exact()
        src = N6.source_P0_constant(t, N)
        z = rng.randrange(N)
        sysd = SL.site_systems(src, z, N, include_pures=False)   # mixed only
        sol = {}
        dims = []
        okall = True
        for c in range(3):
            rows, rhs, tags, cols = sysd[c]
            part, kern = SL.solve_linear(rows, rhs)
            if part is None:
                okall = False
                break
            dims.append(len(kern))
            vec = [Fraction(0)] * len(cols)
            for k in kern:
                lam = Fraction(rng.randint(-4, 4))
                vec = [a + lam * b for a, b in zip(vec, k)]
            sol[c] = [a + b for a, b in zip(part, vec)]
        if not okall:
            continue
        cols = sysd[0][3]
        new = SL.apply_site_solution(src, z, sol, cols, N)
        ok = N6.is_mixed_exact(new, N)
        ranks = [W.matrix_rank(W.oriented(new, a, b)) for a, b in PAIRS]
        pu = W.pures(new, N)
        deform.append({"trial": trial, "site": z, "kernel_dims": dims,
                       "mixed_exact": ok, "ranks": ranks,
                       "n_fullrank_pairs": sum(1 for r in ranks if r == 3),
                       "pures": [str(pu[c]) for c in range(3)]})
        if ok and any(r == 3 for r in ranks):
            fullrank_sources.append(new)
    RES["site_deformation"] = deform
    print(f"[W22-L] site-linear deformations: {len(deform)} built, "
          f"{sum(1 for d in deform if d['mixed_exact'])} mixed-exact, "
          f"{sum(d['n_fullrank_pairs'] for d in deform)} full-rank pairs total")

    # ================= (3) the J.1b falsifier shape ========================
    # a FULL-RANK pair at which all three colour slices are DIRTY,
    # on a MIXED-EXACT source.
    fals = []
    for si, s in enumerate(fullrank_sources):
        for p, q in PAIRS:
            if W.matrix_rank(W.oriented(s, p, q)) != 3:
                continue
            U = tuple(x for x in range(N) if x not in (p, q))
            dirt = []
            for c in range(3):
                w = {W.ekey(a, b): W.oriented(s, a, b)[c][c]
                     for a, b in combinations(range(N), 2)}
                dirt.append(slice_core.slice_error(w, p, q, U) != 0)
            fals.append({"source": si, "pair": [p, q],
                         "dirty": dirt, "all_three_dirty": all(dirt)})
    n_fr = len(fals)
    n_all3 = sum(1 for f in fals if f["all_three_dirty"])
    RES["j1b_falsifier_n6"] = {"full_rank_pairs_examined": n_fr,
                               "all_three_dirty": n_all3,
                               "rows": fals[:80]}
    print(f"[J.1b] N=6 mixed-exact, full-rank pairs examined {n_fr}, "
          f"all-three-dirty {n_all3}")

    # blocking status of those sources (does all-blocked survive full rank?)
    blk = []
    for si, s in enumerate(fullrank_sources[:4]):
        nl = nb = 0
        for p, q in PAIRS:
            if not N6.live(s, p, q):
                continue
            nl += 1
            U = tuple(x for x in range(N) if x not in (p, q))
            v, _ = N6.decide_pair_general(s, p, q, U, f"D{si}_{p}{q}")
            nb += int(v == "BLOCKED")
        pu = W.pures(s, N)
        blk.append({"source": si, "n_live": nl, "n_blocked": nb,
                    "all_blocked": nl == nb,
                    "n_fullrank": sum(1 for e in PAIRS
                                      if W.matrix_rank(W.oriented(s, *e)) == 3),
                    "pures": [str(pu[c]) for c in range(3)]})
        print(f"   deformed source {si}: live={nl} blocked={nb} "
              f"ALL_BLOCKED={nl == nb} fullrank={blk[-1]['n_fullrank']}")
    RES["deformed_blocking"] = blk

    # ================= (4) reachable pure profiles from one site ===========
    reach = []
    for trial in range(6):
        t = const_block_mixed_exact()
        src = N6.source_P0_constant(t, N)
        for z in range(N):
            sysd = SL.site_systems(src, z, N, include_pures=True)
            per_colour = {}
            for c in range(3):
                rows, rhs, tags, cols = sysd[c]
                # split: mixed rows (RHS 0) + the single pure row (RHS 1)
                part, kern = SL.solve_linear(rows, rhs)
                per_colour[c] = (part is not None)
            reach.append({"trial": trial, "site": z,
                          "colour_solvable": per_colour,
                          "all_three_solvable": all(per_colour.values())})
    n_all = sum(1 for r in reach if r["all_three_solvable"])
    RES["pure_reachability"] = {"instances": len(reach),
                                "all_three_solvable": n_all,
                                "rows": reach}
    print(f"[six-site, mechanised] site-z solves reaching pures (1,1,1): "
          f"{n_all}/{len(reach)}")

    with open(f"{BASE}/results_t2_j1b.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
