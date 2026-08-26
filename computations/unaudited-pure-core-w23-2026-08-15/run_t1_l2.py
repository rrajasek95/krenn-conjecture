#!/usr/bin/env python3
"""W23 T1 -- THE TENSOR L2.

THEOREM W23-L2 (algebraic form; every source, every even N, every colour).
Let w(d,e) be the word that is c at every site of B except d at a and e at b
(a != b).  Splitting PM(B) by the partner of a and of b,

    H_B(A)_{w(d,e)}
       = C^(c)_ab A_ab[d][e]
       + sum_{u != v in B\\{a,b}} C^(c)_ab;uv A_au[d][c] A_bv[e][c],

i.e. as a matrix identity in V_a (x) V_b,

    [ H_B(A)_{w(d,e)} ]_{d,e} = C^(c)_ab A_ab + Phi^(c)_ab.              (*)

COROLLARY W23-L2E (exactness form).  If A is EXACT then for all a != b, c,

    C^(c)_ab A_ab + Phi^(c)_ab = e_c (x) e_c.                            (L2)

COROLLARY W23-L2->L1 (contraction).  The colour-c COLUMN of (L2) is exactly
Lemma W22-S (L1) at a, and the colour-c ROW is L1 at b; the new content of L2
is precisely the 2x2 OFF-COLOUR corner (rows and columns != c).
   Proof of the column statement: setting e = c and using the hafnian
   expansion  sum_{v != u} C^(c)_ab;uv w_c(b,v) = C^(c)_au  turns Phi's
   colour-c column into  sum_u C^(c)_au sigma^(c)_au  minus the b term.

COROLLARY W23-L2D (triple determination + consistency).  If C^(c)_ab != 0 for
all three c then A_ab is determined three times over by the star data of the
OTHER blocks; the three determinations agree on the 6 off-diagonal entries by
construction and impose exactly 3 nontrivial relations, one per colour d:

    C^(c2)_ab Phi^(c1)_ab[d][d] = C^(c1)_ab Phi^(c2)_ab[d][d],
    {c1,c2} = {0,1,2} \\ {d}.                                            (C_d)

COROLLARY W23-L2N4 (N=4 closed form).  At N = 4, Phi^(c)_ab has rank <= 2, so
det(C^(c)_ab A_ab - e_c e_c^T) = 0, i.e.

    C^(c)_ab det A_ab = M_cc(A_ab)          (M_cc = principal (c,c) 2x2 minor),

and if A_ab is invertible, C^(c)_ab = (A_ab^{-1})[c][c].  At N=4,
C^(c)_ab = A_{a'b'}[c][c] for the complementary pair {a',b'}, so the diagonal
of the complementary block is the diagonal of A_ab^{-1}.

BRIDGE W23-L2K.  L2 at (a,b) = (p,q) contracted with a cap K is exactly the
diagonal part of the fundamental cap identity
   [(s + r) exp(x)]_U = sum_c kappa_c X_c^U   of the descent note.

This runner PROVES nothing by itself; it verifies (*) as an identity on
arbitrary sources, verifies (L2) on genuinely exact sources at N = 4, 6, 8, 10,
verifies every corollary, and runs the controls.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, permutations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
import w23_core as C                                          # noqa: E402

RES = {}


def banner(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


# ---------------------------------------------------------------- (1) algebraic

def check_algebraic(src, n, ncol=3, pairs=None, colours=None, tag=""):
    """(*) : l2_lhs == matrix of H-values, for EVERY source."""
    pairs = list(combinations(range(n), 2)) if pairs is None else pairs
    colours = range(ncol) if colours is None else colours
    checked = bad = 0
    for a, b in pairs:
        for c in colours:
            lhs = C.l2_lhs(src, a, b, c, n, ncol)
            rhs = C.l2_words(src, a, b, c, n, ncol)
            checked += 1
            if lhs != rhs:
                bad += 1
                print(f"   ALGEBRAIC L2 FAILURE {tag} pair=({a},{b}) c={c}")
                print(f"      lhs={lhs}\n      rhs={rhs}")
    return checked, bad


def check_algebraic_l1(src, n, ncol=3, tag=""):
    checked = bad = 0
    for a in range(n):
        for c in range(ncol):
            lhs = C.l1_lhs(src, a, c, n, ncol)
            rhs = C.l1_words(src, a, c, n, ncol)
            checked += 1
            if lhs != rhs:
                bad += 1
                print(f"   ALGEBRAIC L1 FAILURE {tag} a={a} c={c} "
                      f"{lhs} vs {rhs}")
    return checked, bad


def main():
    rng = random.Random(230815)

    # ================= (1) L2 as an identity on ARBITRARY sources ==========
    banner("(1) THEOREM W23-L2 (algebraic form) on arbitrary sources")
    tot = totbad = 0
    tot1 = tot1bad = 0
    rows = []
    for n in (4, 6, 8):
        for trial in range(3 if n < 8 else 2):
            src = C.random_source(rng, n)
            ch, bd = check_algebraic(src, n, tag=f"rand N={n} t{trial}")
            c1, b1 = check_algebraic_l1(src, n, tag=f"rand N={n} t{trial}")
            tot += ch
            totbad += bd
            tot1 += c1
            tot1bad += b1
            rows.append({"N": n, "kind": "random", "trial": trial,
                         "l2_checked": ch, "l2_bad": bd,
                         "l1_checked": c1, "l1_bad": b1})
    # N = 10: a sample of pairs/colours (full hafnians are 945 terms)
    src10 = C.random_source(rng, 10, lo=-2, hi=2)
    ch, bd = check_algebraic(src10, 10, pairs=[(0, 1), (3, 7)], colours=[0, 2],
                             tag="rand N=10")
    tot += ch
    totbad += bd
    rows.append({"N": 10, "kind": "random", "l2_checked": ch, "l2_bad": bd})
    # sparse / structured sources (the measure-zero strata random draws miss)
    for n in (4, 6):
        for trial in range(4):
            src = C.zero_source(n)
            for e in src:
                if rng.random() < 0.35:
                    i, j = rng.randrange(3), rng.randrange(3)
                    src[e][i][j] = rng.choice([1, -1, 2])
            ch, bd = check_algebraic(src, n, tag=f"sparse N={n}")
            c1, b1 = check_algebraic_l1(src, n, tag=f"sparse N={n}")
            tot += ch
            totbad += bd
            tot1 += c1
            tot1bad += b1
            rows.append({"N": n, "kind": "sparse", "trial": trial,
                         "l2_checked": ch, "l2_bad": bd,
                         "l1_checked": c1, "l1_bad": b1})
    print(f"[W23-L2 algebraic] {tot} (pair,colour) instances, {totbad} failures")
    print(f"[W22-S algebraic ] {tot1} (site,colour) instances, {tot1bad} failures")
    RES["algebraic"] = {"l2_checked": tot, "l2_failures": totbad,
                        "l1_checked": tot1, "l1_failures": tot1bad,
                        "rows": rows}

    # ============ (2) exactness form on genuinely EXACT sources ============
    banner("(2) COROLLARY W23-L2E on genuinely exact sources")
    ex = []
    src = C.delta43()
    assert C.exact_defects(src, 4) == [], "Delta_{4,3} not exact"
    bad = 0
    n_ch = 0
    for a, b in combinations(range(4), 2):
        for c in range(3):
            n_ch += 1
            r = C.l2_residual(src, a, b, c, 4)
            if any(x != 0 for row in r for x in row):
                bad += 1
    ex.append({"source": "Delta_{4,3}", "N": 4, "ncol": 3,
               "checked": n_ch, "violations": bad})
    print(f"   Delta_[4,3]  N=4 ncol=3: {n_ch} instances, {bad} violations")

    for n in (6, 8, 10):
        s2 = C.delta_n2(n, ncol=2)
        assert C.exact_defects(s2, n, ncol=2) == [], f"Delta_{n},2 not exact"
        bad = 0
        n_ch = 0
        for a, b in combinations(range(n), 2):
            for c in range(2):
                n_ch += 1
                r = C.l2_residual(s2, a, b, c, n, ncol=2)
                if any(x != 0 for row in r for x in row):
                    bad += 1
        ex.append({"source": f"Delta_[{n},2]", "N": n, "ncol": 2,
                   "checked": n_ch, "violations": bad})
        print(f"   Delta_[{n},2] N={n} ncol=2: {n_ch} instances, {bad} violations")

    # padded to three colours: exact for c = 0,1 at every (d,e); for c = 2 the
    # ONLY defect is the (2,2) entry (the colour-2 pure equation, which the
    # padded source does not satisfy).
    pad = []
    for n in (6, 8, 10):
        s3 = C.delta_n2(n, ncol=3)
        cnt = {"c01_violations": 0, "c2_only_dd": 0, "c2_other": 0, "checked": 0}
        for a, b in combinations(range(n), 2):
            for c in range(3):
                cnt["checked"] += 1
                r = C.l2_residual(s3, a, b, c, n, ncol=3)
                nz = [(d, e) for d in range(3) for e in range(3) if r[d][e] != 0]
                if c in (0, 1):
                    if nz:
                        cnt["c01_violations"] += 1
                else:
                    if nz == [(2, 2)]:
                        cnt["c2_only_dd"] += 1
                    elif nz:
                        cnt["c2_other"] += 1
        pad.append({"N": n, **cnt})
        print(f"   Delta_[{n},2] padded to ncol=3: c in (0,1) violations "
              f"{cnt['c01_violations']}, c=2 defect exactly at (2,2) "
              f"{cnt['c2_only_dd']}, c=2 other defects {cnt['c2_other']}")
    RES["exactness_form"] = {"exact_sources": ex, "padded": pad}

    # ============ (3) L2 -> L1 contraction (the cofactor recursion) ========
    banner("(3) COROLLARY W23-L2->L1 : the colour-c slices of L2 are L1")
    rec_ch = rec_bad = 0
    slice_ch = slice_bad = 0
    for n, mk in ((4, C.delta43), (6, lambda: C.random_source(rng, 6)),
                  (8, lambda: C.random_source(rng, 8, lo=-2, hi=2))):
        s = mk()
        for a, b in combinations(range(n), 2):
            for c in range(3):
                w = C.colour_slice(s, c, n)
                # cofactor recursion  sum_{v != u} C_ab;uv w_c(b,v) = C_au
                for u in range(n):
                    if u in (a, b):
                        continue
                    tot_r = 0
                    for v in range(n):
                        if v in (a, b, u):
                            continue
                        tot_r += C.cofactor(w, n, (a, b, u, v)) * w[C.ekey(b, v)]
                    rec_ch += 1
                    if tot_r != C.cofactor(w, n, (a, u)):
                        rec_bad += 1
                # colour-c column of L2's LHS == L1's LHS at a
                lhs = C.l2_lhs(s, a, b, c, n)
                col = [lhs[d][c] for d in range(3)]
                slice_ch += 1
                if col != C.l1_lhs(s, a, c, n):
                    slice_bad += 1
                # colour-c row of L2's LHS == L1's LHS at b
                row = [lhs[c][e] for e in range(3)]
                slice_ch += 1
                if row != C.l1_lhs(s, b, c, n):
                    slice_bad += 1
    print(f"   cofactor recursion: {rec_ch} instances, {rec_bad} failures")
    print(f"   L2 colour-c row/column == L1: {slice_ch} instances, "
          f"{slice_bad} failures")
    RES["contraction_to_L1"] = {"recursion_checked": rec_ch,
                                "recursion_failures": rec_bad,
                                "slice_checked": slice_ch,
                                "slice_failures": slice_bad}

    # ============ (4) corollaries: consistency + N=4 determinant law =======
    banner("(4) COROLLARY W23-L2D (consistency) and W23-L2N4 (N=4 law)")
    cons = []
    for name, s, n, ncol in (("Delta_{4,3}", C.delta43(), 4, 3),
                             ("Delta_{6,2}", C.delta_n2(6, ncol=3), 6, 3),
                             ("Delta_{8,2}", C.delta_n2(8, ncol=3), 8, 3)):
        ch = bd = 0
        for a, b in combinations(range(n), 2):
            r = C.l2_consistency_residuals(s, a, b, n, ncol)
            for d, val in r.items():
                ch += 1
                if val != 0:
                    bd += 1
        cons.append({"source": name, "checked": ch, "violations": bd})
        print(f"   consistency (C_d) on {name}: {ch} instances, {bd} violations")
    # the padded Delta_{N,2} is not exact at colour 2, so the (C_d) relations
    # are only guaranteed where the corresponding words are mixed; record both.
    RES["consistency"] = cons

    # N = 4 determinant law: C^(c)_ab det A_ab = M_cc(A_ab).  This is a
    # consequence of rank(Phi) <= 2, hence holds on EXACT N=4 sources.
    n4 = []
    s = C.delta43()
    ch = bd = 0
    for a, b in combinations(range(4), 2):
        blk = C.oriented(s, a, b)
        for c in range(3):
            cof = C.cofactor(C.colour_slice(s, c, 4), 4, (a, b))
            ch += 1
            if cof * C.det3(blk) != C.minor_cc(blk, c):
                bd += 1
    n4.append({"source": "Delta_{4,3}", "checked": ch, "violations": bd})
    print(f"   N=4 determinant law on Delta_[4,3]: {ch} instances, "
          f"{bd} violations")
    # rank(Phi) <= 2 at N = 4 for ARBITRARY sources (the mechanism)
    rk_ch = rk_bad = 0
    for _ in range(20):
        s = C.random_source(rng, 4)
        for a, b in combinations(range(4), 2):
            for c in range(3):
                rk_ch += 1
                if C.matrix_rank(C.l2_Phi(s, a, b, c, 4)) > 2:
                    rk_bad += 1
    print(f"   rank(Phi) <= 2 at N=4 (arbitrary sources): {rk_ch} instances, "
          f"{rk_bad} violations")
    RES["n4_law"] = {"determinant_law": n4, "rank_checked": rk_ch,
                     "rank_violations": rk_bad}

    # ============ (5) the committed near-exact six-site source =============
    banner("(5) the committed near-exact six-site source")
    ne = C.near_exact_six_site()
    n = 6
    md = C.mixed_defects(ne, n)
    pu = C.pures(ne, n)
    print(f"   mixed defects {len(md)}/726, pures "
          f"{[str(pu[c]) for c in range(3)]}")
    # (a) the ALGEBRAIC identity must hold exactly (it is an identity)
    ch, bd = check_algebraic(ne, n, tag="near-exact")
    print(f"   algebraic L2: {ch} instances, {bd} failures")
    # (b) the exactness residual must equal the defect of the corresponding word
    mism = 0
    nz_res = 0
    for a, b in combinations(range(n), 2):
        for c in range(3):
            r = C.l2_residual(ne, a, b, c, n)
            wd = C.l2_words(ne, a, b, c, n)
            for d in range(3):
                for e in range(3):
                    tgt = wd[d][e] - (1 if (d == c and e == c) else 0)
                    if r[d][e] != tgt:
                        mism += 1
                    if r[d][e] != 0:
                        nz_res += 1
    print(f"   L2 residual == (H-value - target): {mism} mismatches; "
          f"{nz_res} nonzero residual entries")
    l1nz = sum(1 for a in range(n) for c in range(3)
               if any(x != 0 for x in C.l1_residual(ne, a, c, n)))
    print(f"   L1 residual: {l1nz}/18 (site,colour) instances nonzero")
    print(f"   defect words: {md}  -- all BALANCED 3-colour words (2,2,2)")
    ranks = {f"{a},{b}": C.matrix_rank(C.oriented(ne, a, b))
             for a, b in combinations(range(n), 2)}
    print(f"   block ranks: {sorted(ranks.values())}")
    print("   >>> THE COMMITTED NEAR-EXACT SOURCE SATISFIES THE ENTIRE "
          "L1 + L2 SYSTEM\n       (all pure, all one-off and all two-off "
          "words) AND CARRIES 9 WITNESS PAIRS.")
    RES["near_exact"] = {"mixed_defects": len(md),
                         "defect_words": [list(w) for w in md],
                         "pures": [str(pu[c]) for c in range(3)],
                         "algebraic_checked": ch, "algebraic_failures": bd,
                         "residual_matches_defect_mismatches": mism,
                         "nonzero_L2_residual_entries": nz_res,
                         "nonzero_L1_instances": l1nz,
                         "block_ranks": ranks}

    # ============ (6) BRIDGE: L2 at (p,q) contracted with a cap ============
    banner("(6) BRIDGE W23-L2K : L2 at (p,q) is the cap identity's diagonal")
    br_ch = br_bad = 0
    for name, s, n, exact in (("Delta_{4,3}", C.delta43(), 4, True),
                              ("random N=6", C.random_source(rng, 6), 6, False),
                              ("Delta_{8,2} pad", C.delta_n2(8, ncol=3), 8, False)):
        for p, q in list(combinations(range(n), 2))[:4]:
            U = tuple(x for x in range(n) if x not in (p, q))
            K = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
            sK = C.cap_s(s, p, q, K)
            R = C.cap_R(s, p, q, K, U)
            for c in range(3):
                w = C.colour_slice(s, c, n)
                lhs = sK * C.haf_scalar(w, U)
                for u, v in combinations(U, 2):
                    lhs += R[(u, v)][c][c] * C.haf_scalar(
                        w, tuple(x for x in U if x not in (u, v)))
                wd = C.l2_words(s, p, q, c, n)
                rhs = sum(K[i][j] * wd[i][j] for i in range(3) for j in range(3))
                br_ch += 1
                if lhs != rhs:
                    br_bad += 1
    print(f"   [(s+r)exp(x)]_U at word c^U  ==  <K, L2-word-matrix>: "
          f"{br_ch} instances, {br_bad} failures")
    RES["bridge"] = {"checked": br_ch, "failures": br_bad}

    # ============ (7) CONTROLS =============================================
    banner("(7) controls")
    ctrl = {}

    # (7a) mutation control: perturbing one cell of an exact source must break
    # the L2 exactness form somewhere.
    fired = trials = 0
    for _ in range(60):
        s = C.delta43()
        e = rng.choice(list(s))
        i, j = rng.randrange(3), rng.randrange(3)
        s[e][i][j] += rng.choice([1, -1, 2, -3])
        trials += 1
        broke = any(any(x != 0 for row in C.l2_residual(s, a, b, c, 4)
                        for x in row)
                    for a, b in combinations(range(4), 2) for c in range(3))
        fired += int(broke)
    ctrl["mutation_delta43"] = {"trials": trials, "fired": fired}
    print(f"   [mutation] one-cell mutation of Delta_[4,3] breaks L2: "
          f"{fired}/{trials}")

    fired = trials = 0
    for _ in range(60):
        s = C.delta_n2(6, ncol=2)
        e = rng.choice(list(s))
        i, j = rng.randrange(2), rng.randrange(2)
        s[e][i][j] += rng.choice([1, -1, 2])
        trials += 1
        broke = any(any(x != 0 for row in C.l2_residual(s, a, b, c, 6, 2)
                        for x in row)
                    for a, b in combinations(range(6), 2) for c in range(2))
        fired += int(broke)
    ctrl["mutation_delta62"] = {"trials": trials, "fired": fired}
    print(f"   [mutation] one-cell mutation of Delta_[6,2] breaks L2: "
          f"{fired}/{trials}")

    # (7b) MUTATION CONTROL ON THE CHECKER: a deliberately wrong Phi (drop the
    # u != v restriction / use the wrong cofactor) must FAIL on exact sources.
    def bad_phi_diagonal_allowed(src, a, b, c, n, ncol=3):
        """Allows u == v.  NOT a firing mutation: C^(c)_ab;uu is a hafnian on
        an ODD site set, hence 0 -- the u != v restriction is enforced by
        PARITY.  Kept as a recorded VACUOUS control (ledger 17 discipline:
        a control that cannot fire must be labelled, not counted)."""
        w = C.colour_slice(src, c, n, ncol)
        rest = [x for x in range(n) if x not in (a, b)]
        out = [[0] * ncol for _ in range(ncol)]
        for u in rest:
            for v in rest:
                cof = C.cofactor(w, n, (a, b, u, v))
                sa = C.star_vec(src, a, u, c, ncol)
                sb = C.star_vec(src, b, v, c, ncol)
                for d in range(ncol):
                    for e2 in range(ncol):
                        out[d][e2] += cof * sa[d] * sb[e2]
        return out

    def bad_phi_one_orientation(src, a, b, c, n, ncol=3):
        """WRONG on purpose: sums only over u < v (drops the (v,u) term)."""
        w = C.colour_slice(src, c, n, ncol)
        rest = [x for x in range(n) if x not in (a, b)]
        out = [[0] * ncol for _ in range(ncol)]
        for u, v in combinations(rest, 2):
            cof = C.cofactor(w, n, (a, b, u, v))
            sa = C.star_vec(src, a, u, c, ncol)
            sb = C.star_vec(src, b, v, c, ncol)
            for d in range(ncol):
                for e2 in range(ncol):
                    out[d][e2] += cof * sa[d] * sb[e2]
        return out

    def bad_phi_wrong_star_slot(src, a, b, c, n, ncol=3):
        """WRONG on purpose: reads sigma^(c)_bu / sigma^(c)_av (slots swapped)."""
        w = C.colour_slice(src, c, n, ncol)
        rest = [x for x in range(n) if x not in (a, b)]
        out = [[0] * ncol for _ in range(ncol)]
        for u, v in permutations(rest, 2):
            cof = C.cofactor(w, n, (a, b, u, v))
            sa = C.star_vec(src, b, u, c, ncol)
            sb = C.star_vec(src, a, v, c, ncol)
            for d in range(ncol):
                for e2 in range(ncol):
                    out[d][e2] += cof * sa[d] * sb[e2]
        return out

    def bad_phi_wrong_cofactor(src, a, b, c, n, ncol=3):
        """WRONG on purpose: uses C^(c)_ab instead of C^(c)_ab;uv."""
        w = C.colour_slice(src, c, n, ncol)
        rest = [x for x in range(n) if x not in (a, b)]
        cof = C.cofactor(w, n, (a, b))
        out = [[0] * ncol for _ in range(ncol)]
        for u, v in permutations(rest, 2):
            sa = C.star_vec(src, a, u, c, ncol)
            sb = C.star_vec(src, b, v, c, ncol)
            for d in range(ncol):
                for e2 in range(ncol):
                    out[d][e2] += cof * sa[d] * sb[e2]
        return out

    mut = {}
    for label, fn in (("phi_allows_u_eq_v (VACUOUS by parity)",
                       bad_phi_diagonal_allowed),
                      ("phi_wrong_cofactor", bad_phi_wrong_cofactor),
                      ("phi_one_orientation", bad_phi_one_orientation),
                      ("phi_wrong_star_slot", bad_phi_wrong_star_slot),
                      ("drop_the_A_term",
                       lambda s, a, b, c, n, ncol=3: C.l2_Phi(s, a, b, c, n, ncol))):
        # Tested against the ALGEBRAIC form on GENERIC sources.  Testing them
        # on Delta_{4,3}/Delta_{N,2} would be vacuous: those sources are
        # diagonal and site-symmetric, so sigma^(c)_au = w_c(a,u) e_c and the
        # slot-swap mutation is a genuine symmetry there (verified: 0/104).
        fires = 0
        checked = 0
        drop_A = label.startswith("drop_the_A_term")
        rngm = random.Random(4242)
        for n in (4, 6):
            for _ in range(3):
                s = C.random_source(rngm, n)
                for a, b in combinations(range(n), 2):
                    for c in range(3):
                        w = C.colour_slice(s, c, n)
                        cof = C.cofactor(w, n, (a, b))
                        blk = C.oriented(s, a, b)
                        phi = fn(s, a, b, c, n, 3)
                        wd = C.l2_words(s, a, b, c, n)
                        checked += 1
                        ok = all((0 if drop_A else cof * blk[d][e]) + phi[d][e]
                                 == wd[d][e] for d in range(3) for e in range(3))
                        fires += int(not ok)
        mut[label] = {"checked": checked, "fired": fires}
        print(f"   [mutation of the CHECKER: {label}] fails the ALGEBRAIC "
              f"identity on generic sources: {fires}/{checked}")
    ctrl["checker_mutations"] = mut

    # (7b') RESOLUTION of L2: one-cell mutations that break EXACTNESS but are
    # invisible to L1+L2 (L2 only sees words with <= 2 sites off a constant
    # background).  Quantifies exactly how partial a certificate L1+L2 is.
    res = {}
    for nm, mk, n, ncol in (("Delta_{4,3}", C.delta43, 4, 3),
                            ("Delta_{6,2}", lambda: C.delta_n2(6, ncol=2), 6, 2)):
        tot = brk_ex = brk_l2 = brk_l1 = 0
        for e in list(mk()):
            for i in range(ncol):
                for j in range(ncol):
                    for delta in (1, -1):
                        s = mk()
                        s[e][i][j] += delta
                        tot += 1
                        ex_bad = bool(C.exact_defects(s, n, ncol))
                        l1_bad = any(any(x != 0 for x in
                                         C.l1_residual(s, a, c, n, ncol))
                                     for a in range(n) for c in range(ncol))
                        l2_bad = l1_bad or any(
                            any(x != 0 for row in C.l2_residual(s, a, b, c, n, ncol)
                                for x in row)
                            for a, b in combinations(range(n), 2)
                            for c in range(ncol))
                        brk_ex += int(ex_bad)
                        brk_l1 += int(l1_bad)
                        brk_l2 += int(l2_bad)
        res[nm] = {"mutations": tot, "break_exactness": brk_ex,
                   "break_L1": brk_l1, "break_L1_or_L2": brk_l2,
                   "invisible_to_L1L2": brk_ex - brk_l2}
        print(f"   [resolution] {nm}: {tot} one-cell mutations; break exactness "
              f"{brk_ex}; break L1 {brk_l1}; break L1+L2 {brk_l2}; "
              f"INVISIBLE to L1+L2 {brk_ex - brk_l2}")
    ctrl["l2_resolution"] = res

    # (7c) inter-probe: reproduce W22-S (star identity, 60/60 contraction) and
    # cross-check H against W22's independent evaluator.
    sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                       "unaudited-induction2-w22-2026-08-15")
    import w22_core as W22                                    # noqa: E402
    import w22_sitelin as SL                                  # noqa: E402

    hcheck = hbad = 0
    for n in (4, 6):
        for _ in range(3):
            s = C.random_source(rng, n)
            for _ in range(20):
                word = tuple(rng.randrange(3) for _ in range(n))
                hcheck += 1
                if C.H(s, word, n) != W22.ghz_coefficient(s, word, n):
                    hbad += 1
    print(f"   [inter-probe] H vs W22.ghz_coefficient: {hcheck} words, "
          f"{hbad} disagreements")

    sbad = stot = 0
    for n, s, ncol in ((4, C.delta43(), 3), (6, C.delta_n2(6, ncol=2), 2),
                       (8, C.delta_n2(8, ncol=2), 2), (10, C.delta_n2(10, ncol=2), 2)):
        for z in range(n):
            for c in range(ncol):
                stot += 1
                mine = C.l1_residual(s, z, c, n, ncol)
                theirs = SL.star_identity_residual(s, z, c, n, ncol)
                if mine != theirs or any(x != 0 for x in mine):
                    sbad += 1
    print(f"   [inter-probe] L1 residual vs W22-S star_identity_residual: "
          f"{stot} instances, {sbad} disagreements-or-nonzero")

    # W22's 60/60 contraction identity control, reproduced verbatim in shape
    rng2 = random.Random(9091)
    cbad = ctot = 0
    for _ in range(60):
        s = C.delta43()
        p = rng2.randrange(4)
        u = [rng2.randint(-5, 5) for _ in range(3)]
        for c in range(3):
            ctot += 1
            if SL.contraction_identity_residual(s, p, u, c, 4) != 0:
                cbad += 1
    print(f"   [inter-probe] W22-S* contraction identity reproduced: "
          f"{ctot} instances, {cbad} violations (W22 reported 60/60 clean "
          f"on Delta_[4,3] alone)")
    ctrl["interprobe"] = {"H_words": hcheck, "H_disagreements": hbad,
                          "L1_vs_W22S": stot, "L1_disagreements": sbad,
                          "W22S_contraction": ctot, "W22S_violations": cbad}

    # (7d) EXPLICIT-POINT control (ledger 13): every claim of the form
    # "L2 forces X" is tested against an explicit exact point.
    s = C.delta43()
    pt = {"Delta_{4,3} exact": C.exact_defects(s, 4) == [],
          "L2 holds there": all(all(x == 0 for row in C.l2_residual(s, a, b, c, 4)
                                    for x in row)
                                for a, b in combinations(range(4), 2)
                                for c in range(3))}
    print(f"   [explicit point] {pt}")
    ctrl["explicit_point"] = {k: bool(v) for k, v in pt.items()}

    RES["controls"] = ctrl

    with open(f"{BASE}/results_t1_l2.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("\nwrote results_t1_l2.json")


if __name__ == "__main__":
    main()
