#!/usr/bin/env python3
"""W25 T1a -- THE THREE-OFF IDENTITY L3, THE DIAGONAL PARITY THEOREM, AND THE
INTER-PROBE CONTROL BATTERY.

Contents
--------
C1  H cross-check: W25's bitmask DP vs W23's PM enumeration (random + exact
    + Q(omega) sources).
C2  cap_error cross-check: W25's W22-M CLOSED FORM vs W23's subset-sum-over-J
    expansion (this simultaneously CHECKS LEMMA W22-M).
C3  L1 / L2 residual cross-check vs W23.
C4  decider agreement W25 vs W23 on every pair of the committed near-exact
    source, over Q and modulo three primes (two of them = 1 mod 3, ledger 19).
C5  MUTATION controls: each identity must FAIL on a perturbed source.

T1a-1  LAW L3 (three-off tensor identity) [PROVED-HERE, verified N=6,8]:
       Psi^(c)_{abe} = A_ab (x) T_e + A_ae (x) T_b + A_be (x) T_a + Xi
       equals the tensor of H-values on 3-off words; exactness pins it to
       e_c (x) e_c (x) e_c.
T1a-2  DEGENERATION: setting any one off-slot back to c reduces L3 to L2
       exactly (so the NEW content of L3 is the 2x2x2 all-off-colour corner:
       8 equations per (triple, colour), 480 instances = the 420 three-off
       words with the 60 (3,3)-words counted twice).
T1a-3  W25-D1 [PROVED-HERE, all even N]: on the DIAGONAL stratum (every block
       monochrome rank <= 1) H_w = 0 whenever some colour class of w has ODD
       size.  Consequently diagonal X_2 = diagonal X_3 (indeed = diagonal
       X_{2k+1} for the odd rungs) -- the whole diagonal stratum of X_2 is a
       supply of X_3 points.
T1a-4  W25-U1+ [PROVED-HERE, all even N]: for Delta^(3)_N, H_w = 1 if every
       colour class w^{-1}(d) is a union of M_d-edges and H_w = 0 otherwise;
       every M-consistent word has all classes even, so the off-count is even;
       hence Delta^(3)_N lies in X_3 (not merely X_2 = W23-U1), and its first
       failures sit at off-count 4 and are exactly the bicoloured 4-cycles of
       the cubic graph M_0 + M_1 + M_2.
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
import w25_decide as D                                          # noqa: E402
import w23_core as W23                                          # noqa: E402
import w23_decide as W23D                                       # noqa: E402

RES = {}
RAN = []


def control(name):
    RAN.append(name)


# ------------------------------------------------------------------ sources

def rand_source(rng, n, lo=-3, hi=3, omega=False):
    src = {}
    for e in combinations(range(n), 2):
        if omega:
            src[e] = [[C.Om(rng.randint(lo, hi), rng.randint(lo, hi))
                       for _ in range(3)] for _ in range(3)]
        else:
            src[e] = [[Fraction(rng.randint(lo, hi)) for _ in range(3)]
                      for _ in range(3)]
    return src


def rand_diagonal(rng, n, omega=False, pspan=True):
    """A DIAGONAL source: every block monochrome rank <= 1.  Colour classes are
    forced to span (each vertex gets at least one edge of each colour) when
    pspan, by first laying down three disjoint perfect matchings."""
    src = C.zero_source(n, 3, C.Om(0) if omega else Fraction(0))
    used = set()
    if pspan:
        for c, M in enumerate(C.default_three_pms(n)):
            for (a, b) in M:
                k = C.ekey(a, b)
                used.add(k)
                src[k][c][c] = (C.Om(rng.randint(1, 4), rng.randint(0, 2))
                                if omega else Fraction(rng.randint(1, 4)))
    for e in combinations(range(n), 2):
        if e in used:
            continue
        if rng.random() < 0.3:
            c = rng.randrange(3)
            src[e][c][c] = (C.Om(rng.randint(1, 4), rng.randint(0, 2))
                            if omega else Fraction(rng.randint(1, 4)))
    return src


# ------------------------------------------------- the L3 identity, verified

def h_three_off_tensor(src, S, c, n):
    """[H_B(A)_{w}] where w = c off S and (d1,d2,d3) on S."""
    a, b, e = S
    out = [[[None] * 3 for _ in range(3)] for _ in range(3)]
    for d1 in range(3):
        for d2 in range(3):
            for d3 in range(3):
                word = [c] * n
                word[a], word[b], word[e] = d1, d2, d3
                out[d1][d2][d3] = C.H(src, tuple(word), n)
    return out


def check_l3(src, n, tag, sample_triples=None, rng=None):
    bad = []
    triples = list(combinations(range(n), 3))
    if sample_triples and len(triples) > sample_triples:
        triples = rng.sample(triples, sample_triples)
    for S in triples:
        for c in range(3):
            P = C.l3_Psi(src, S, c, n)
            Hm = h_three_off_tensor(src, S, c, n)
            for d1 in range(3):
                for d2 in range(3):
                    for d3 in range(3):
                        if P[d1][d2][d3] != Hm[d1][d2][d3]:
                            bad.append([tag, list(S), c, d1, d2, d3,
                                        str(P[d1][d2][d3]),
                                        str(Hm[d1][d2][d3])])
    return bad


def check_l2(src, n, tag):
    """L2 as an identity: C_ab A_ab + Phi = [H_{w(d,e)}]."""
    bad = []
    for a, b in combinations(range(n), 2):
        for c in range(3):
            lhs = W23.l2_lhs(src, a, b, c, n)
            rhs = W23.l2_words(src, a, b, c, n)
            for d in range(3):
                for e in range(3):
                    if lhs[d][e] != rhs[d][e]:
                        bad.append([tag, a, b, c, d, e])
    return bad


# ------------------------------------------------------ the diagonal stratum

def is_diagonal(src, n):
    for a, b in combinations(range(n), 2):
        m = src[(a, b)]
        nz = [(i, j) for i in range(3) for j in range(3) if m[i][j] != 0]
        if not nz:
            continue
        if len(nz) != 1 or nz[0][0] != nz[0][1]:
            return False
    return True


def edge_colour(src, a, b):
    m = C.oriented(src, a, b)
    for c in range(3):
        if m[c][c] != 0:
            return c
    return None


def m_consistent(word, mats):
    """Delta^(3) criterion: every site's M_{w_u}-partner carries w_u."""
    part = {}
    for c, M in enumerate(mats):
        for (a, b) in M:
            part[(c, a)] = b
            part[(c, b)] = a
    for u, d in enumerate(word):
        if word[part[(d, u)]] != d:
            return False
    return True


def main():
    rng = random.Random(250815)
    print("=" * 74)
    print("C1  H cross-check  W25 bitmask DP  vs  W23 PM enumeration")
    print("=" * 74)
    tot = bad = 0
    for n in (4, 6, 8):
        for t in range(8):
            src = rand_source(rng, n)
            for _ in range(30):
                w = tuple(rng.randrange(3) for _ in range(n))
                tot += 1
                if C.H(src, w, n) != W23.H(src, w, n):
                    bad += 1
    for src, n in [(C.delta43(), 4), (C.near_exact_six_site(), 6),
                   (C.delta3_N(6), 6), (C.delta3_N(8), 8)]:
        for w in product(range(3), repeat=n):
            tot += 1
            if C.H(src, w, n) != W23.H(src, w, n):
                bad += 1
    print(f"   {tot - bad}/{tot} agree  (mismatches {bad})")
    RES["C1_H_crosscheck"] = {"total": tot, "mismatch": bad}
    control("C1_H_crosscheck")
    assert bad == 0

    print("=" * 74)
    print("C2  cap_error:  W25 (W22-M closed form)  vs  W23 (subset-sum over J)")
    print("=" * 74)
    tot = bad = 0
    srcs = [C.near_exact_six_site(), C.delta3_N(6)] + \
           [rand_source(rng, 6) for _ in range(4)]
    for src in srcs:
        for _ in range(40):
            p, q = sorted(rng.sample(range(6), 2))
            U = tuple(x for x in range(6) if x not in (p, q))
            K = [[Fraction(rng.randint(-2, 2)) for _ in range(3)]
                 for _ in range(3)]
            tot += 1
            if C.cap_error(src, p, q, K, U) != W23.cap_error(src, p, q, K, U):
                bad += 1
    # N = 8 (h = 3): the closed form must also hold beyond h = 2
    for src in [C.delta3_N(8), rand_source(rng, 8)]:
        for _ in range(6):
            p, q = sorted(rng.sample(range(8), 2))
            U = tuple(x for x in range(8) if x not in (p, q))
            K = [[Fraction(rng.randint(-1, 1)) for _ in range(3)]
                 for _ in range(3)]
            tot += 1
            if C.cap_error(src, p, q, K, U) != W23.cap_error(src, p, q, K, U):
                bad += 1
    print(f"   {tot - bad}/{tot} agree  (mismatches {bad})  "
          f"-- also an independent check of LEMMA W22-M at h = 2 and h = 3")
    RES["C2_caperror_crosscheck"] = {"total": tot, "mismatch": bad}
    control("C2_caperror_crosscheck")
    assert bad == 0

    print("=" * 74)
    print("C3  L1 / L2 residual cross-check vs W23")
    print("=" * 74)
    tot = bad = 0
    for src, n in [(C.near_exact_six_site(), 6), (C.delta3_N(6), 6),
                   (rand_source(rng, 6), 6), (rand_source(rng, 6), 6)]:
        for a in range(n):
            for c in range(3):
                tot += 1
                if C.l1_residual(src, a, c, n) != W23.l1_residual(src, a, c, n):
                    bad += 1
        for a, b in combinations(range(n), 2):
            for c in range(3):
                tot += 1
                if C.l2_residual(src, a, b, c, n) != W23.l2_residual(src, a, b,
                                                                    c, n):
                    bad += 1
    print(f"   {tot - bad}/{tot} agree  (mismatches {bad})")
    RES["C3_L1L2_crosscheck"] = {"total": tot, "mismatch": bad}
    control("C3_L1L2_crosscheck")
    assert bad == 0

    print("=" * 74)
    print("T1a-1  LAW L3: the three-off tensor identity")
    print("=" * 74)
    allbad = []
    for tagn, (src, n) in enumerate([(C.near_exact_six_site(), 6),
                                     (C.delta3_N(6), 6),
                                     (rand_source(rng, 6), 6),
                                     (rand_source(rng, 6), 6),
                                     (rand_diagonal(rng, 6), 6),
                                     (rand_source(rng, 6, omega=True), 6),
                                     (rand_source(rng, 8), 8),
                                     (C.delta3_N(8), 8)]):
        b = check_l3(src, n, f"src{tagn}", sample_triples=10, rng=rng)
        allbad += b
        print(f"   source {tagn} (N={n}): L3 violations {len(b)}")
    print(f"   TOTAL L3 violations over all sources: {len(allbad)}")
    RES["T1a1_L3"] = {"violations": len(allbad), "detail": allbad[:5]}
    assert not allbad
    control("T1a1_L3_identity")

    print("=" * 74)
    print("T1a-2  DEGENERATION: L3 with one slot back at c  ==  L2")
    print("=" * 74)
    tot = bad = 0
    for src, n in [(rand_source(rng, 6), 6), (C.near_exact_six_site(), 6),
                   (rand_source(rng, 8), 8)]:
        for S in list(combinations(range(n), 3))[:8]:
            a, b_, e = S
            for c in range(3):
                P = C.l3_Psi(src, S, c, n)
                # slot 3 (site e) returned to c  ->  L2 at the pair (a,b)
                l2 = W23.l2_lhs(src, a, b_, c, n)
                for d1 in range(3):
                    for d2 in range(3):
                        tot += 1
                        if P[d1][d2][c] != l2[d1][d2]:
                            bad += 1
    print(f"   {tot - bad}/{tot} degenerations agree  (mismatches {bad})")
    print("   => the NEW content of L3 is the 2x2x2 ALL-OFF-COLOUR corner:")
    nwords = {k: len(C.near_constant_words(6, 3, k)) for k in range(5)}
    print(f"      N=6 ladder word counts {nwords}; 3-off words "
          f"{nwords[3] - nwords[2]}; equation instances 3 colours x "
          f"{len(list(combinations(range(6), 3)))} triples x 8 = "
          f"{3 * 20 * 8} (the 60 (3,3)-words appear twice)")
    RES["T1a2_degeneration"] = {"total": tot, "mismatch": bad,
                                "ladder_words": nwords}
    assert bad == 0
    control("T1a2_L3_degenerates_to_L2")

    print("=" * 74)
    print("C5  MUTATION controls (each identity must FAIL on a perturbation)")
    print("=" * 74)
    mut = {}
    src = C.near_exact_six_site()
    bad0 = check_l3(src, 6, "clean")
    m1 = C.copy_source(src)
    m1[(0, 1)][0][0] = m1[(0, 1)][0][0] + 1
    bad1 = check_l3(m1, 6, "mut-block")
    print(f"   L3 on the clean source: {len(bad0)} violations (expected 0)")
    print(f"   L3 with a mutated BLOCK: {len(bad1)} violations "
          f"(expected 0 -- L3 is an IDENTITY, true for every source)")
    # the identity is unconditional; what mutation must break is EXACTNESS
    r0 = sum(1 for S in combinations(range(6), 3) for c in range(3)
             for d1 in range(3) for d2 in range(3) for d3 in range(3)
             if C.l3_residual(src, S, c, 6)[d1][d2][d3] != 0)
    r1 = sum(1 for S in combinations(range(6), 3) for c in range(3)
             for d1 in range(3) for d2 in range(3) for d3 in range(3)
             if C.l3_residual(m1, S, c, 6)[d1][d2][d3] != 0)
    print(f"   L3 RESIDUAL (vs e_c (x) e_c (x) e_c): clean {r0} nonzero, "
          f"mutated {r1} nonzero  -- the mutation control FIRES ({r1} > 0)")
    mut["l3_identity_clean"] = len(bad0)
    mut["l3_identity_mutated"] = len(bad1)
    mut["l3_residual_clean"] = r0
    mut["l3_residual_mutated"] = r1
    assert len(bad0) == 0 and len(bad1) == 0 and r0 == 0 and r1 > 0
    control("C5_mutation_L3")

    print("=" * 74)
    print("T1a-3  W25-D1: the DIAGONAL PARITY THEOREM")
    print("=" * 74)
    print("   claim: on a diagonal source H_w = 0 whenever some colour class")
    print("   of w has ODD size; hence every ODD-off-count word is automatic")
    print("   and diagonal X_2 = diagonal X_3.")
    tot = bad = 0
    oddwords = 0
    for n in (6, 8):
        for t in range(6):
            src = rand_diagonal(rng, n, omega=(t == 5))
            assert is_diagonal(src, n)
            for w in product(range(3), repeat=n):
                cnt = [sum(1 for x in w if x == c) for c in range(3)]
                if any(x % 2 for x in cnt):
                    oddwords += 1
                    tot += 1
                    if C.H(src, w, n) != 0:
                        bad += 1
    print(f"   {tot - bad}/{tot} odd-class words have H = 0 "
          f"(violations {bad})")
    RES["T1a3_diagonal_parity"] = {"tested": tot, "violations": bad}
    assert bad == 0
    control("T1a3_diagonal_parity")

    # the consequence, checked directly: diagonal X_2 => diagonal X_3
    checked = imp = 0
    for n in (6, 8):
        for t in range(40):
            src = rand_diagonal(rng, n)
            if C.in_Xk(src, n, 2)[0]:
                checked += 1
                if C.in_Xk(src, n, 3)[0]:
                    imp += 1
    print(f"   diagonal sources found in X_2: {checked}; of these in X_3: "
          f"{imp}  (W25-D1 predicts equality)")
    RES["T1a3_x2_implies_x3_diag"] = {"in_X2": checked, "also_in_X3": imp}
    assert checked == imp
    control("T1a3_diag_X2_equals_X3")

    print("=" * 74)
    print("T1a-4  W25-U1+: Delta^(3)_N lies in X_3 at every even N")
    print("=" * 74)
    d3res = {}
    for n in (6, 8, 10):
        mats = C.default_three_pms(n)
        src = C.delta3_N(n, mats)
        rec = {"in_X1": C.in_Xk(src, n, 1)[0], "in_X2": C.in_Xk(src, n, 2)[0],
               "in_X3": C.in_Xk(src, n, 3)[0]}
        # the combinatorial formula H_w = [w is M-consistent]
        mism = 0
        if n <= 8:
            for w in product(range(3), repeat=n):
                if C.H(src, w, n) != (1 if m_consistent(w, mats) else 0):
                    mism += 1
            rec["combinatorial_formula_mismatches"] = mism
            defs = C.mixed_defects(src, n)
            rec["defects"] = len(defs)
            rec["defect_offcounts"] = sorted(set(C.offcount(w) for w in defs))
        else:
            rec["combinatorial_formula_mismatches"] = "skipped (3^10)"
            # verify X_3 membership only (the ladder words)
        d3res[str(n)] = rec
        print(f"   N={n}: {rec}")
        assert rec["in_X3"]
        if n <= 8:
            assert mism == 0
            assert all(x % 2 == 0 for x in rec["defect_offcounts"])
    RES["T1a4_delta3_in_X3"] = d3res
    control("T1a4_delta3_in_X3")

    print("=" * 74)
    print("C4  decider agreement W25 vs W23 (near-exact source, every pair)")
    print("=" * 74)
    ne = C.near_exact_six_site()
    rows = []
    dis = mm = 0
    for p, q in combinations(range(6), 2):
        if not C.live(ne, p, q):
            rows.append({"pair": [p, q], "live": False})
            continue
        U = tuple(x for x in range(6) if x not in (p, q))
        v1, d1, mp = D.decide_pair(ne, p, q, U, f"NE{p}{q}")
        v2, d2, mp2 = W23D.decide_pair(ne, p, q, U, f"WNE{p}{q}",
                                       primes=(32003, 1000003))
        agree = (v1 == v2)
        dis += (0 if agree else 1)
        mm += sum(1 for ch, dd in mp.items() if (dd == -1) != (d1 == -1))
        rows.append({"pair": [p, q], "live": True, "w25": v1, "dimQ": d1,
                     "modp": mp, "w23": v2, "agree": agree})
    nw = sum(1 for r in rows if r.get("w25") == "WITNESS")
    print(f"   live {sum(1 for r in rows if r['live'])}; WITNESS {nw}; "
          f"decider disagreements {dis}; mod-p mismatches {mm}")
    print(f"   (W23 reports 9 witnesses on this object -- inter-probe "
          f"agreement: {nw == 9})")
    RES["C4_decider_agreement"] = {"rows": rows, "disagreements": dis,
                                   "modp_mismatch": mm, "n_witness": nw}
    assert dis == 0 and mm == 0 and nw == 9
    control("C4_decider_agreement")

    # ------------------------------------------------------------- manifest
    declared = ["C1_H_crosscheck", "C2_caperror_crosscheck",
                "C3_L1L2_crosscheck", "T1a1_L3_identity",
                "T1a2_L3_degenerates_to_L2", "C5_mutation_L3",
                "T1a3_diagonal_parity", "T1a3_diag_X2_equals_X3",
                "T1a4_delta3_in_X3", "C4_decider_agreement"]
    missing = [x for x in declared if x not in RAN]
    print("=" * 74)
    print(f"CONTROL MANIFEST (ledger 21): declared {len(declared)}, ran "
          f"{len(RAN)}, missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    assert not missing, f"controls declared but never run: {missing}"

    with open(f"{BASE}/results_t1a_identities.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t1a_identities.json")


if __name__ == "__main__":
    main()
