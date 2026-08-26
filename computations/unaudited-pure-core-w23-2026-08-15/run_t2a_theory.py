#!/usr/bin/env python3
"""W23 T2a -- the two sides of the composition, formalised exactly.

SIDE R (rigidity, from the pure + near-constant equations)
---------------------------------------------------------
(R1) LEMMA W23-M (matrix form of L1).  For an exact source and every site p,

        sum_{y != p} A_py D_y  =  I_3,   D_y := diag(C^(0)_py, C^(1)_py, C^(2)_py).

     Immediately gives W22-X1 (star injectivity): u^T A_py = 0 for all y
     implies u^T = u^T I = 0.

(R2) THEOREM W23-L2 (this probe's T1) and its corollaries.

(R3) PROPOSITION W23-S1 (exact L1 support criterion).  Fix p and c; let
     T = {y : C^(c)_py != 0} and S_y = supp(sigma^(c)_py).  A value assignment
     with EXACTLY this support pattern satisfying L1 exists iff
        (i)  some y in T has c in S_y, and
        (ii) for every d != c, #{y in T : d in S_y} != 1.
     COROLLARY (support collapse): |T| = 1 forces sigma^(c)_py = (1/C) e_c --
     the colour-c column of that block is a multiple of e_c.

SIDE B (blocking)
-----------------
(B1) W22-X2: all-blocked => for every p and every torus u (all coordinates
     nonzero), |W(u)| >= 3, W(u) = {y : A_py^T u != 0}.
     EXACT DECISION PROCEDURE (implemented here): a detachment witness exists
     at p iff some (m-2)-subset Z of the partners has
        L_Z = intersection over y in Z of ker A_py^T
     nonzero AND not contained in any coordinate hyperplane.  (A linear
     subspace inside a union of hyperplanes lies inside one of them, so this
     is an exact finite test.)

(B2) W22-M1 converse: at a blocked pair every admissible cap has a perfect
     matching of U with >= 2 G_R-edges and the rest in G_A.

THE COMPOSITION QUESTION: can (R) and (B) hold simultaneously?
Sections 3-5 answer it at the ONE-VERTEX level (they can: explicit exact
certificate) and locate where the tension must instead live.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
import w23_core as C                                          # noqa: E402
import w23_walk as WK                                         # noqa: E402

RES = {}


def banner(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


# --------------------------------------------------------- side-B decision

def torus_vector_in(basis, ncol=3):
    """Does span(basis) contain a vector with ALL coordinates nonzero?
    A subspace contained in a finite union of hyperplanes lies in one of them,
    so: nonzero AND for each coordinate i some basis vector has entry != 0."""
    if not basis:
        return None
    for i in range(ncol):
        if all(v[i] == 0 for v in basis):
            return None
    # constructive: a generic rational combination works; search small ones
    for coeffs in product(range(-2, 3), repeat=len(basis)):
        if all(x == 0 for x in coeffs):
            continue
        v = [sum(Fraction(coeffs[k]) * basis[k][i] for k in range(len(basis)))
             for i in range(ncol)]
        if all(x != 0 for x in v):
            return v
    return "EXISTS_BUT_NOT_FOUND_SMALL"


def detachment_scan(src, p, n, ncol=3):
    """All (m-2)-subsets Z of partners of p whose common left kernel contains
    a torus vector.  Each such Z gives a WITNESS pair (W22-X2)."""
    ys = [y for y in range(n) if y != p]
    m = len(ys)
    hits = []
    for Z in combinations(ys, m - 2):
        rows = []
        for y in Z:
            blk = C.oriented(src, p, y, ncol)
            for c in range(ncol):
                rows.append([blk[i][c] for i in range(ncol)])
        basis = C.nullspace(rows, ncol)
        tv = torus_vector_in(basis, ncol)
        if tv is not None:
            hits.append({"Z": list(Z), "kernel_dim": len(basis),
                         "torus_u": [str(x) for x in tv]
                         if isinstance(tv, list) else tv})
    return hits


def main():
    rng = random.Random(770231)

    # ============ (1) LEMMA W23-M : the matrix form of L1 ==================
    banner("(1) LEMMA W23-M : sum_y A_py D_y = I on exact sources")
    rowsM = []
    for name, s, n, ncol in (("Delta_{4,3}", C.delta43(), 4, 3),
                             ("Delta_{6,2}", C.delta_n2(6, ncol=2), 6, 2),
                             ("Delta_{8,2}", C.delta_n2(8, ncol=2), 8, 2),
                             ("Delta_{10,2}", C.delta_n2(10, ncol=2), 10, 2),
                             ("near-exact N=6", C.near_exact_six_site(), 6, 3)):
        bad = 0
        for p in range(n):
            r = C.l1_matrix_residual(s, p, n, ncol)
            if any(x != 0 for row in r for x in row):
                bad += 1
        rowsM.append({"source": name, "sites": n, "violations": bad})
        print(f"   {name}: {n} sites, {bad} violations")
    # negative control: generic sources violate it
    gbad = gtot = 0
    for _ in range(10):
        s = C.random_source(rng, 6)
        for p in range(6):
            gtot += 1
            r = C.l1_matrix_residual(s, p, 6)
            gbad += int(any(x != 0 for row in r for x in row))
    print(f"   [negative control] generic N=6 sources: {gbad}/{gtot} vertices "
          f"violate it")
    RES["l1_matrix_form"] = {"rows": rowsM, "generic_violations": gbad,
                             "generic_total": gtot}

    # ============ (2) the pure equations kill W22-1's falsifier family =====
    banner("(2) THEOREM W23-F : the mixed-exact falsifier family fails L1")
    print("   PROOF.  On A_uv = t_uv J (all-ones blocks), sigma^(c)_ay ="
          " t_ay * 1\n   and C^(c)_ay = haf(t | B\\{a,y}).  Hence the L1 LHS is"
          "\n     (sum_y t_ay haf(t|B\\{a,y})) * 1  =  haf(t) * 1  =  0 * 1,"
          "\n   because the family is defined by haf(t) = 0.  So the L1"
          " residual is\n   EXACTLY -e_c at every site and colour: the maximal"
          " possible failure.")
    fam = []
    for n in (6, 8, 10):
        PAIRS = list(combinations(range(n), 2))

        def haf_t(tt):
            return C.haf_scalar(tt, tuple(range(n)))

        built = 0
        worst_ok = True
        for _ in range(200):
            if built >= 3:
                break
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
            src = {e: [[tt[e]] * 3 for _ in range(3)] for e in PAIRS}
            built += 1
            # (a) it IS mixed-exact (W10/W22-1)
            me = len(C.mixed_defects(src, n)) == 0
            # (b) its L1 residual is exactly -e_c everywhere
            ok = True
            for a in range(n):
                for c in range(3):
                    r = C.l1_residual(src, a, c, n)
                    if r != [(-1 if d2 == c else 0) for d2 in range(3)]:
                        ok = False
            worst_ok = worst_ok and ok and me
            fam.append({"N": n, "mixed_exact": me,
                        "L1_residual_is_minus_e_c": ok,
                        "pures": [str(x) for x in C.pures(src, n).values()]})
        print(f"   N={n}: {built} falsifier members; mixed-exact and "
              f"L1-residual = -e_c everywhere: {worst_ok}")
    RES["falsifier_family"] = fam

    # ============ (3) exhaustive L1 support criterion (PROP W23-S1) ========
    banner("(3) PROPOSITION W23-S1 : exhaustive support sweep at m = 5")
    # pattern per partner: (C_y nonzero?, supp(sigma_y) as a 3-bit mask)
    # -> 16 options per partner, 16^5 = 1,048,576 patterns, ALL enumerated.
    c = 0                                     # wlog by colour symmetry
    feasible = infeasible = 0
    constructed_ok = constructed_bad = 0
    fail_reason = {"no_c_support": 0, "singleton_offcolour": 0, "both": 0}
    opts = [(t, mask) for t in (0, 1) for mask in range(8)]
    for pat in product(opts, repeat=5):
        T = [i for i, (t, mask) in enumerate(pat) if t == 1]
        has_c = any(pat[i][1] >> c & 1 for i in T)
        singles = [d for d in range(3) if d != c
                   and sum(1 for i in T if pat[i][1] >> d & 1) == 1]
        ok = has_c and not singles
        if not ok:
            infeasible += 1
            key = ("both" if (not has_c and singles)
                   else ("no_c_support" if not has_c else "singleton_offcolour"))
            fail_reason[key] += 1
            continue
        feasible += 1
        # CONSTRUCT an explicit rational solution with EXACTLY this support
        Cy = {i: Fraction(1) for i in T}
        sig = {i: [Fraction(0)] * 3 for i in range(5)}
        for i in range(5):
            for d in range(3):
                if pat[i][1] >> d & 1:
                    sig[i][d] = Fraction(1)          # provisional, all nonzero
        # fix the off-colour components to cancel
        for d in range(3):
            if d == c:
                continue
            car = [i for i in T if pat[i][1] >> d & 1]
            if len(car) >= 2:
                sig[car[0]][d] = Fraction(-(len(car) - 1))
        # fix the colour-c components to sum to 1
        carc = [i for i in T if pat[i][1] >> c & 1]
        sig[carc[0]][c] = Fraction(1) - (len(carc) - 1)
        if sig[carc[0]][c] == 0:                      # keep support exact
            sig[carc[0]][c] = Fraction(2)
            if len(carc) > 1:
                sig[carc[1]][c] = Fraction(1) - Fraction(2) - (len(carc) - 2)
                if sig[carc[1]][c] == 0:
                    sig[carc[1]][c] = Fraction(1)
                    sig[carc[0]][c] = Fraction(1) - Fraction(1) - (len(carc) - 2)
        # verify: exact support + L1 holds
        good = True
        for i in range(5):
            for d in range(3):
                if (sig[i][d] != 0) != bool(pat[i][1] >> d & 1):
                    good = False
        if good:
            for d in range(3):
                tot = sum(Cy[i] * sig[i][d] for i in T)
                if tot != (1 if d == c else 0):
                    good = False
        constructed_ok += int(good)
        constructed_bad += int(not good)
    print(f"   patterns enumerated: {feasible + infeasible} (= 16^5)")
    print(f"   L1-feasible: {feasible};  infeasible: {infeasible}  "
          f"(no colour-c carrier {fail_reason['no_c_support']}, "
          f"singleton off-colour carrier {fail_reason['singleton_offcolour']}, "
          f"both {fail_reason['both']})")
    print(f"   explicit rational constructions verified for feasible patterns: "
          f"{constructed_ok} ok, {constructed_bad} not realised by the "
          f"canonical construction")
    RES["l1_support_sweep"] = {"total": feasible + infeasible,
                               "feasible": feasible, "infeasible": infeasible,
                               "fail_reason": fail_reason,
                               "constructed_ok": constructed_ok,
                               "constructed_bad": constructed_bad}

    # COROLLARY: |T| = 1 forces a pure colour-c column
    single = [pat for pat in product(opts, repeat=2)]     # tiny illustration
    print("   COROLLARY (support collapse): among the feasible patterns, every "
          "one\n   with |T| = 1 has supp(sigma) = {c} exactly -- checked "
          "exhaustively:")
    bad = 0
    tot = 0
    for pat in product(opts, repeat=5):
        T = [i for i, (t, mask) in enumerate(pat) if t == 1]
        if len(T) != 1:
            continue
        has_c = any(pat[i][1] >> c & 1 for i in T)
        singles = [d for d in range(3) if d != c
                   and sum(1 for i in T if pat[i][1] >> d & 1) == 1]
        if not (has_c and not singles):
            continue
        tot += 1
        if pat[T[0]][1] != (1 << c):
            bad += 1
    print(f"      {tot} feasible |T|=1 patterns, {bad} with impure colour-c "
          f"column")
    RES["l1_support_sweep"]["singleton_T_feasible"] = tot
    RES["l1_support_sweep"]["singleton_T_impure"] = bad

    # ============ (4) ONE-VERTEX COMPOSITION IS CONSISTENT =================
    banner("(4) THEOREM W23-N1 (negative): the one-vertex composition of "
           "(R1) and (B1)\n    is CONSISTENT -- explicit exact certificate at "
           "m = 5")
    # Take D_y generic invertible and A_2..A_5 generic invertible; solve
    # A_1 = (I - sum_{y>=2} A_y D_y) D_1^{-1}.  Then sum_y A_y D_y = I and
    # every A_y is invertible, so W(u) = {1..5} for every u != 0 and (B1) holds
    # VACUOUSLY at this vertex.
    def inv_diag(d):
        return [Fraction(1) / x for x in d]

    cert = None
    for attempt in range(200):
        D = {y: [Fraction(rng.randint(1, 4)) for _ in range(3)]
             for y in range(1, 6)}
        A = {y: [[Fraction(rng.randint(-3, 3)) for _ in range(3)]
                 for _ in range(3)] for y in range(2, 6)}
        if any(C.det3(A[y]) == 0 for y in A):
            continue
        M = [[(1 if i == j else 0) - sum(A[y][i][j] * D[y][j]
                                        for y in range(2, 6))
              for j in range(3)] for i in range(3)]
        di = inv_diag(D[1])
        A1 = [[M[i][j] * di[j] for j in range(3)] for i in range(3)]
        if C.det3(A1) == 0:
            continue
        A[1] = A1
        # verify (R1)
        S = [[sum(A[y][i][j] * D[y][j] for y in range(1, 6)) for j in range(3)]
             for i in range(3)]
        if S != [[1 if i == j else 0 for j in range(3)] for i in range(3)]:
            continue
        cert = {"D": {str(y): [str(x) for x in D[y]] for y in D},
                "A": {str(y): [[str(x) for x in row] for row in A[y]] for y in A},
                "all_A_invertible": all(C.det3(A[y]) != 0 for y in A),
                "all_D_invertible": all(all(x != 0 for x in D[y]) for y in D),
                "sum_A_D_equals_I": True}
        break
    assert cert is not None, "certificate construction failed"
    print("   certificate found:")
    print(f"      sum_y A_y D_y = I               : {cert['sum_A_D_equals_I']}")
    print(f"      every A_y invertible            : {cert['all_A_invertible']}")
    print(f"      every D_y invertible            : {cert['all_D_invertible']}")
    print("      => W(u) = all 5 partners for every u != 0, so W22-X2's "
          "|W(u)| >= 3\n         holds vacuously; (R1) and (B1) coexist.")
    print("   CONSEQUENCE: no contradiction can be extracted from L1 + X2 at a "
          "single\n   vertex.  The pinning is 9 scalar equations on 45 star "
          "parameters; the\n   blocking side is generic.  The tension must be "
          "GLOBAL (many vertices)\n   or must use the deeper words.")
    RES["one_vertex_certificate"] = cert

    # (4b) the same conclusion with L2 present: L2 at (p,y) constrains A_py in
    # terms of the stars at y, which the one-vertex abstraction leaves free.
    print("\n   [scope] L2 at (p,y) reads sigma^(c)_yv (the star system at y),"
          "\n   which the one-vertex abstraction does not constrain; so adding "
          "L2\n   cannot change the verdict at this level either.")

    # ============ (5) side-B exact decision procedure, validated ===========
    banner("(5) exact detachment-witness decision procedure (B1)")
    ne = C.near_exact_six_site()
    dets = {}
    for p in range(6):
        hits = detachment_scan(ne, p, 6)
        dets[p] = hits
        print(f"   near-exact source, p={p}: {len(hits)} detachment witnesses "
              f"(3-subsets Z with a torus common left kernel)")
    RES["detachment_scan_near_exact"] = {str(p): dets[p] for p in dets}
    # positive control: build a source with a deliberately detached star
    s = C.zero_source(6)
    for e in s:
        for i in range(3):
            for j in range(3):
                s[e][i][j] = rng.randint(-3, 3)
    u0 = [Fraction(1), Fraction(1), Fraction(-2)]
    for y in (1, 2, 3):                     # make A_0y^T u0 = 0
        blk = [[Fraction(rng.randint(-3, 3)) for _ in range(3)]
               for _ in range(2)]
        row2 = [Fraction(-(blk[0][j] * u0[0] + blk[1][j] * u0[1]), u0[2])
                for j in range(3)]
        s[(0, y)] = [blk[0], blk[1], row2]
    hits = detachment_scan(s, 0, 6)
    print(f"   [positive control] planted detachment at p=0 (3 blocks killed by "
          f"u0): detector finds {len(hits)} witnesses "
          f"({'FIRES' if hits else 'MISSED'})")
    # negative control: generic source has none
    negs = 0
    for _ in range(10):
        g = C.random_source(rng, 6)
        negs += int(bool(detachment_scan(g, 0, 6)))
    print(f"   [negative control] generic sources with a detachment witness: "
          f"{negs}/10")
    RES["detachment_controls"] = {"planted_hits": len(hits),
                                  "generic_hits_out_of_10": negs}

    with open(f"{BASE}/results_t2a_theory.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("\nwrote results_t2a_theory.json")


if __name__ == "__main__":
    main()
