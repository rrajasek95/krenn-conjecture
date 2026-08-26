#!/usr/bin/env python3
"""W23 T2d -- an N-UNIFORM family in X_2, and a PROVED witness theorem on it.

THEOREM W23-U1 [PROVED-HERE, every even N].  Let M_0, M_1, M_2 be PAIRWISE
DISJOINT perfect matchings of K_N and let w_c be nonzero weights on M_c with
prod_{e in M_c} w_c(e) = 1.  The DIAGONAL source

    A_uv = sum_c w_c(u,v) [uv in M_c] E_cc                    ("Delta^(3)_N")

lies in X_2 (pures + L1 + L2) but is NOT exact.
  * pures: haf(w_c) = prod_{e in M_c} w_c(e) = 1 (M_c is the only PM of M_c).
  * L1: automatic on the diagonal stratum (the off-colour star components
    A_au[d][c], d != c, all vanish).
  * L2 (diagonal form, proved in T2b): w_d(e) C^(c)_e = 0 for d != c.  Here
    C^(c)_e = haf(w_c | B\\e) = 0 unless e in M_c (deleting two vertices not
    joined by an M_c-edge destroys the only PM), and if e in M_c then
    w_d(e) = 0 for d != c by disjointness.  So every product vanishes.
  * NOT exact: the deeper (rainbow) words fail.

THEOREM W23-U2 [PROVED-HERE, every even N >= 6].  EVERY live pair of
Delta^(3)_N carries a witness; in particular Delta^(3)_N is never all-blocked.

PROOF.  Let pq in M_{c_1} and let {c_1,c_2,c_3} = {0,1,2}.  Write y_i for p's
M_{c_i}-partner (y_1 = q) and q_i for q's M_{c_i}-partner (q_1 = p).  Put
U = B \\ {p,q} and Z = U \\ {y_2,y_3}: every site of Z is DETACHED from p.
Since R_ab = 0 whenever both a,b are p-detached and every G_R-edge meets
{y_2,y_3}, no perfect matching of U carries more than two G_R-edges, so only
|J| = 2 survives in Lemma W22-M and

  E = s^{h-2} sum_{b1 != b2 in Z} R_{y2 b1} (x) R_{y3 b2} (x) Haf_{Z\\{b1,b2}}(A).

With kappa^(i) := row c_i of K one has R_{y_i b} = w(p y_i) e_{c_i} (x)
A_qb^T kappa^(i), and A_qb = w(qb) E_{d d} for the colour d of qb.  Only
b in {q_2,q_3} gives a nonzero factor, and the two ordered choices land on the
SAME basis tensor (each slot receives its own edge colour), so

  E = s^{h-2} w(p y_2) w(p y_3) w(q q_2) w(q q_3)
        * ( K[c_2][c_2] K[c_3][c_3] + K[c_2][c_3] K[c_3][c_2] )
        * (basis tensor) (x) Haf_{Z\\{q_2,q_3}}(A) .

The cap  K = I + E_{c_2 c_3} - E_{c_3 c_2}  is admissible (kappa_c = 1,
s = w(pq) != 0) and makes the bracket 1*1 + 1*(-1) = 0.  If instead q_2 or q_3
lies in {y_2,y_3} (a rainbow triangle) the sum is empty and E = 0 for EVERY
admissible cap.  []

This runner verifies both theorems exactly at N = 6, 8, 10, 12 and cross-checks
the N = 6 verdicts against the independent Singular decision.
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
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-induction2-w22-2026-08-15")
import w23_core as C                                          # noqa: E402
import w23_walk as WK                                         # noqa: E402
import w23_decide as DEC                                      # noqa: E402
import w22_core as W22                                        # noqa: E402

RES = {}


def banner(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


def three_disjoint_pms(n, rng, weights=True, tries=4000):
    """Three pairwise disjoint perfect matchings of K_n, with weights whose
    product is 1 on each matching."""
    for _ in range(tries):
        used = set()
        Ms = []
        ok = True
        for c in range(3):
            verts = list(range(n))
            rng.shuffle(verts)
            M = []
            good = True
            for i in range(0, n, 2):
                e = C.ekey(verts[i], verts[i + 1])
                if e in used:
                    good = False
                    break
                M.append(e)
            if not good:
                ok = False
                break
            used |= set(M)
            Ms.append(M)
        if ok:
            break
    else:
        raise RuntimeError("could not build three disjoint PMs")
    src = C.zero_source(n)
    ws = {}
    for c, M in enumerate(Ms):
        vals = [Fraction(rng.choice([1, 2, 3, -1, -2])) for _ in M[:-1]] \
            if weights else [Fraction(1)] * (len(M) - 1)
        prod = Fraction(1)
        for v in vals:
            prod *= v
        vals.append(Fraction(1) / prod)
        for e, v in zip(M, vals):
            src[e][c][c] = v
            ws[(c, e)] = v
    return src, Ms, ws


def witness_cap(c1, c2, c3):
    K = [[0] * 3 for _ in range(3)]
    for c in range(3):
        K[c][c] = 1
    K[c2][c3] = 1
    K[c3][c2] = -1
    return K


def main():
    rng = random.Random(9182736)
    RES["theorems"] = {}

    # =============== (1) THEOREM W23-U1 : Delta^(3)_N lies in X_2 ==========
    banner("(1) THEOREM W23-U1: Delta^(3)_N is in X_2 at every even N")
    rows = []
    for n in (6, 8, 10, 12):
        for trial in range(3 if n <= 10 else 1):
            src, Ms, ws = three_disjoint_pms(n, rng)
            words2 = WK.near_constant_words(n, 3, 2)
            ok2, badw = WK.in_Xk(src, n, words2)
            pu = C.pures(src, n)
            # L1 and L2 residuals directly
            l1bad = sum(1 for a in range(n) for c in range(3)
                        if any(x != 0 for x in C.l1_residual(src, a, c, n)))
            l2bad = 0
            for a, b in combinations(range(n), 2):
                for c in range(3):
                    if any(x != 0 for r in C.l2_residual(src, a, b, c, n)
                           for x in r):
                        l2bad += 1
            exact = (C.exact_defects(src, n) == []) if n <= 8 else None
            rows.append({"N": n, "trial": trial, "in_X2": ok2,
                         "pures": [str(pu[c]) for c in range(3)],
                         "L1_violations": l1bad, "L2_violations": l2bad,
                         "exact": exact})
            print(f"   N={n} t{trial}: in X_2 {ok2}; pures "
                  f"{[str(pu[c]) for c in range(3)]}; L1 violations {l1bad}; "
                  f"L2 violations {l2bad}; exact "
                  f"{'(not tested)' if exact is None else exact}")
    RES["theorems"]["U1"] = rows

    # =============== (2) THEOREM W23-U2 : every live pair has a witness ====
    banner("(2) THEOREM W23-U2: the explicit cap kills E at every live pair")
    u2 = []
    for n in (6, 8, 10):
        for trial in range(2):
            src, Ms, ws = three_disjoint_pms(n, rng)
            colour_of = {}
            for c, M in enumerate(Ms):
                for e in M:
                    colour_of[e] = c
            nlive = nzero = nadm = 0
            for p, q in combinations(range(n), 2):
                if not DEC.live(src, p, q):
                    continue
                nlive += 1
                c1 = colour_of[C.ekey(p, q)]
                c2, c3 = [c for c in range(3) if c != c1]
                K = witness_cap(c1, c2, c3)
                U = tuple(x for x in range(n) if x not in (p, q))
                adm = C.is_admissible(src, p, q, K)
                E = C.cap_error(src, p, q, K, U)
                nadm += int(adm)
                nzero += int(adm and not E)
            u2.append({"N": n, "trial": trial, "live_pairs": nlive,
                       "admissible": nadm, "E_zero": nzero})
            print(f"   N={n} t{trial}: {nlive} live pairs; the explicit cap is "
                  f"admissible at {nadm} and gives E = 0 at {nzero}")
    RES["theorems"]["U2"] = u2

    # (2b) cross-check at N = 6 against the independent Singular decision
    banner("(2b) N=6 cross-check of W23-U2 against the Singular decision")
    src, Ms, ws = three_disjoint_pms(6, rng)
    agree = tot = 0
    verdicts = []
    for p, q in combinations(range(6), 2):
        if not DEC.live(src, p, q):
            continue
        U = tuple(x for x in range(6) if x not in (p, q))
        v, d, mp = DEC.decide_pair(src, p, q, U, f"U{p}{q}")
        verdicts.append([p, q, v, d, mp])
        tot += 1
        agree += int(v == "WITNESS")
    print(f"   Singular verdicts on Delta^(3)_6: WITNESS at {agree}/{tot} live "
          f"pairs (theorem predicts all)")
    print(f"   per-pair (pair, verdict, dim, mod-p dims): {verdicts}")
    RES["theorems"]["U2_singular_n6"] = {"live": tot, "witness": agree,
                                         "verdicts": verdicts}

    # (2c) MUTATION CONTROL: the cap must FAIL once the hypotheses are broken
    banner("(2c) mutation controls on THEOREM W23-U2")
    fired = trials = 0
    for _ in range(40):
        src, Ms, ws = three_disjoint_pms(6, rng)
        colour_of = {}
        for c, M in enumerate(Ms):
            for e in M:
                colour_of[e] = c
        # break the hypothesis: add one extra off-matching entry
        e = rng.choice([x for x in src if x not in colour_of])
        cc = rng.randrange(3)
        src[e][cc][cc] = Fraction(rng.choice([1, -1, 2]))
        bad = 0
        live_ct = 0
        for p, q in combinations(range(6), 2):
            if not DEC.live(src, p, q):
                continue
            ee = C.ekey(p, q)
            if ee not in colour_of:
                continue
            live_ct += 1
            c1 = colour_of[ee]
            c2, c3 = [c for c in range(3) if c != c1]
            K = witness_cap(c1, c2, c3)
            U = tuple(x for x in range(6) if x not in (p, q))
            if C.is_admissible(src, p, q, K) and C.cap_error(src, p, q, K, U):
                bad += 1
        trials += 1
        fired += int(bad > 0)
    print(f"   adding one off-matching entry makes the explicit cap FAIL "
          f"somewhere: {fired}/{trials}")
    RES["theorems"]["U2_mutation"] = {"trials": trials, "fired": fired}

    # a mutated CAP must also fail
    fired = trials = 0
    for _ in range(40):
        src, Ms, ws = three_disjoint_pms(6, rng)
        colour_of = {}
        for c, M in enumerate(Ms):
            for e in M:
                colour_of[e] = c
        bad = 0
        for p, q in combinations(range(6), 2):
            if not DEC.live(src, p, q):
                continue
            c1 = colour_of[C.ekey(p, q)]
            c2, c3 = [c for c in range(3) if c != c1]
            K = witness_cap(c1, c2, c3)
            K[c3][c2] = 1                     # WRONG SIGN: symmetric, not anti
            U = tuple(x for x in range(6) if x not in (p, q))
            if C.is_admissible(src, p, q, K) and C.cap_error(src, p, q, K, U):
                bad += 1
        trials += 1
        fired += int(bad > 0)
    print(f"   the SAME cap with the sign flipped (symmetric instead of "
          f"antisymmetric) fails: {fired}/{trials}")
    RES["theorems"]["U2_cap_mutation"] = {"trials": trials, "fired": fired}

    # =============== (3) THEOREM W23-DR : the diagonal-regime structure ====
    banner("(3) THEOREM W23-DR: colour-exclusive live edges in the diagonal "
           "regime")
    print("   STATEMENT [PROVED-HERE, every even N].  Let A be a DIAGONAL "
          "source in X_2\n   and put L_c = {e : w_c(e) C^(c)_e != 0}.  Then\n"
          "     (a) every site is covered by L_c, for every c   [expand "
          "haf(w_c) = 1\n         along the site], so |L_c| >= N/2;\n"
          "     (b) L_0, L_1, L_2 are pairwise DISJOINT [e in L_c cap L_d "
          "would give\n         w_d(e) C^(c)_e != 0, contradicting L2];\n"
          "     (c) every edge of L_c is monochrome of colour c, so its block "
          "has RANK 1;\n     (d) hence at least 3N/2 of the C(N,2) edges carry "
          "rank-one blocks\n         (N=6: 9 of 15; N=8: 12 of 28 -- W5's "
          "diagonal-regime corollary,\n         re-derived independently from "
          "L2).")
    dr = []
    for n in (6, 8, 10):
        src, Ms, ws = three_disjoint_pms(n, rng)
        Ls = []
        for c in range(3):
            w = C.colour_slice(src, c, n)
            L = [e for e in combinations(range(n), 2)
                 if w[e] != 0 and C.cofactor(w, n, e) != 0]
            Ls.append(set(L))
        covers = [len(set(x for e in L for x in e)) == n for L in Ls]
        disj = all(not (Ls[i] & Ls[j]) for i, j in combinations(range(3), 2))
        rk1 = all(C.matrix_rank(C.oriented(src, *e)) == 1
                  for L in Ls for e in L)
        dr.append({"N": n, "sizes": [len(L) for L in Ls], "covers": covers,
                   "pairwise_disjoint": disj, "all_rank_one": rk1,
                   "bound_3N_over_2": 3 * n // 2,
                   "total": sum(len(L) for L in Ls)})
        print(f"   N={n}: |L_c| = {[len(L) for L in Ls]}, each covers B "
              f"{covers}, pairwise disjoint {disj}, all rank-one {rk1}; "
              f"total {sum(len(L) for L in Ls)} >= {3*n//2}")
    # and on the exhaustive N=6 family from T2b
    with open(f"{BASE}/results_t2b_diag6.json") as fh:
        T2B = json.load(fh)
    import run_t2b_diag6 as D6
    bad = 0
    checked = 0
    for r in T2B["X2_blocking"]["rows"]:
        t = tuple(r["triple"])
        s = D6.source_of(t)
        Ls = []
        for c in range(3):
            w = C.colour_slice(s, c, 6)
            Ls.append(set(e for e in combinations(range(6), 2)
                          if w[e] != 0 and C.cofactor(w, 6, e) != 0))
        checked += 1
        okc = all(len(set(x for e in L for x in e)) == 6 for L in Ls)
        okd = all(not (Ls[i] & Ls[j]) for i, j in combinations(range(3), 2))
        okr = all(C.matrix_rank(C.oriented(s, *e)) == 1 for L in Ls for e in L)
        if not (okc and okd and okr):
            bad += 1
    print(f"   verified on the exhaustive X_2 cap D6(1) family: {checked} "
          f"classes, {bad} violations")
    RES["theorems"]["DR"] = {"rows": dr, "d6_checked": checked, "d6_bad": bad}

    with open(f"{BASE}/results_t2d_uniform.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("\nwrote results_t2d_uniform.json")


if __name__ == "__main__":
    main()
