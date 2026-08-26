#!/usr/bin/env python3
"""W32 / T2 -- calibrating the new decomposition against the proved diagonal
theorem, and settling the AVERAGING question (attack line 1).

A. DIAGONAL CALIBRATION.  For a diagonal source given by three pairwise
   disjoint perfect matchings of K_8:
     * "the 2-colour restriction A^{ab} is exact"  <=>  M_a u M_b is a
       Hamiltonian 8-cycle;
     * hence W32-2COL  <=>  W27's condition (C);
     * the residual trichromatic conditions collapse to the (4,2,2) words
       <=>  W27's condition (D)  (no (2,1,1)-signature perfect matching).
   Reproduces the 32,970 / 16,800 / 8,610 / 0 census through a completely
   different route (pair restrictions, not W27's word shortcuts).
   => W32-2COL is the general form of (C); the residual gap is the general
   form of (D).  In particular W32-2COL CANNOT kill on its own.

B. AVERAGING.  Answers "does averaging a hypothetical general X_4 point over
   sigma land in X_4?"  NO, and structurally so:
     * every X_k condition is homogeneous of degree N/2 = 4 in the source,
       so X_4 is a cone but not a linear space;
     * explicit counterexample: two exact 2-colour sources whose average is
       not exact (and two sigma-related ones, so the sigma-average itself
       fails);
     * X_4 IS invariant under S_8 x S_3 and under the 21-dimensional gauge
       torus {lambda_u^c : prod_u lambda_u^c = 1}, and it is Zariski closed,
       so torus DEGENERATIONS stay inside (Lemma W32-DEG) -- but the
       degeneration cone is trivial on the full-support stratum (proved in
       the report), so no free sparsification.

Checkpoint: results_t2.json.  Control manifest asserted (ledger 21).
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w32_core import (NCOL, Manifest, all_words, cell, copy_source, ekey,
                      haf_word, offcount, perfect_matchings, profile, require,
                      restrict_pair, zero_source)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_t2.json")
N = 8
R = {}
MAN = Manifest(["pairexact_eq_hamiltonian", "census_matches_W27D3",
                "avg_counterexample", "orbit_invariance", "torus_invariance",
                "degree4_homogeneity"])


def two_colour_diag(m_a, m_b, n=N):
    src = {}
    for a, b in itertools.combinations(range(n), 2):
        src[(a, b)] = [[Fraction(0)] * 2 for _ in range(2)]
    for e in m_a:
        src[ekey(*e)][0][0] = Fraction(1)
    for e in m_b:
        src[ekey(*e)][1][1] = Fraction(1)
    return src


def exact_2col(src, n=N):
    for w in itertools.product(range(2), repeat=n):
        if haf_word(src, w) != (1 if len(set(w)) == 1 else 0):
            return False
    return True


def is_hamiltonian_union(m_a, m_b, n=N):
    adj = {i: [] for i in range(n)}
    for e in list(m_a) + list(m_b):
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    seen, cur, prev = {0}, 0, None
    for _ in range(n - 1):
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            return False
        prev, cur = cur, nxt[0]
        if cur in seen:
            return False
        seen.add(cur)
    return len(seen) == n


# ------------------------------------------------------ A. diagonal calibration
def task_pairexact():
    """On disjoint PM pairs: 2-colour exactness <=> Hamiltonian union."""
    PMs = perfect_matchings(tuple(range(N)))
    rng = random.Random(11)
    sample = rng.sample(range(len(PMs)), 40)
    checked, agree = 0, 0
    for i in sample:
        for j in sample:
            A, B = PMs[i], PMs[j]
            if set(A) & set(B):
                continue
            e1 = exact_2col(two_colour_diag(A, B))
            e2 = is_hamiltonian_union(A, B)
            require(e1 == e2, f"pair-exact != Hamiltonian on {A} {B}")
            checked += 1
            agree += 1
    MAN.mark("pairexact_eq_hamiltonian")
    R["pairexact"] = {"checks": checked, "disagreements": 0}
    print("2-colour exactness <=> Hamiltonian union:", checked,
          "disjoint pairs, 0 disagreements")


def task_census():
    """Reproduce W27-D3's census through the pair-restriction route."""
    PMs = perfect_matchings(tuple(range(N)))
    ham = {}
    for i in range(len(PMs)):
        for j in range(i + 1, len(PMs)):
            if set(PMs[i]) & set(PMs[j]):
                continue
            ham[(i, j)] = is_hamiltonian_union(PMs[i], PMs[j])
    # (D): no perfect matching with 2 edges from one M and 1 from each other
    total = 0
    nh_hist = {}
    passC = passD = both = 0
    idx = range(len(PMs))
    for i, j, k in itertools.combinations(idx, 3):
        if set(PMs[i]) & set(PMs[j]) or set(PMs[i]) & set(PMs[k]) \
                or set(PMs[j]) & set(PMs[k]):
            continue
        total += 1
        nh = sum(ham[(min(a, b), max(a, b))]
                 for a, b in ((i, j), (i, k), (j, k)))
        nh_hist[nh] = nh_hist.get(nh, 0) + 1
        C = (nh == 3)
        # (D) holds  <=>  NO (2,1,1) matching exists
        sets = [set(PMs[i]), set(PMs[j]), set(PMs[k])]
        D = True
        for M in PMs:
            cnt = [sum(1 for e in M if e in S) for S in sets]
            if len(M) == sum(cnt) and sorted(cnt) == [1, 1, 2]:
                D = False
                break
        passC += C
        passD += D
        both += (C and D)
    require((total, passC, passD, both) == (32970, 16800, 8610, 0),
            f"census mismatch: {(total, passC, passD, both)}")
    MAN.mark("census_matches_W27D3")
    R["census"] = {"triples": total, "passC": passC, "passD": passD,
                   "both": both, "nh_histogram": {str(k): v for k, v
                                                  in sorted(nh_hist.items())}}
    print("census via pair restrictions:", total, passC, passD, both,
          "-- matches W27-D3 exactly; nh histogram", nh_hist)


# ---------------------------------------------------------------- B. averaging
def task_avg():
    """X_4 is a degree-4 cone, not convex: two exact 2-colour sources whose
    average is not exact.  Also the sigma-average of a sigma-orbit."""
    PMs = perfect_matchings(tuple(range(N)))
    good = []
    for i in range(len(PMs)):
        for j in range(len(PMs)):
            if i == j or (set(PMs[i]) & set(PMs[j])):
                continue
            if is_hamiltonian_union(PMs[i], PMs[j]):
                good.append((PMs[i], PMs[j]))
            if len(good) >= 40:
                break
        if len(good) >= 40:
            break
    require(len(good) >= 2, "no exact 2-colour objects found")
    A = two_colour_diag(*good[0])
    B = two_colour_diag(*good[1])
    require(exact_2col(A) and exact_2col(B), "seeds not exact")
    avg = {e: [[(A[e][a][b] + B[e][a][b]) / 2 for b in range(2)]
               for a in range(2)] for e in A}
    bad = [w for w in itertools.product(range(2), repeat=N)
           if haf_word(avg, w) != (1 if len(set(w)) == 1 else 0)]
    require(bad, "AVERAGE of two exact sources is exact -- unexpected")
    # sigma-average: sigma = the 3-cycle (0 1 2)(3 4 5)(6)(7) on sites
    sig = {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6, 7: 7}

    def act(src):
        out = {e: [[Fraction(0)] * 2 for _ in range(2)] for e in src}
        for (u, v) in src:
            su, sv = sig[u], sig[v]
            for a in range(2):
                for b in range(2):
                    val = src[(u, v)][a][b]
                    if su < sv:
                        out[(su, sv)][a][b] += val
                    else:
                        out[(sv, su)][b][a] += val
        return out
    orb = [A, act(A), act(act(A))]
    require(exact_2col(orb[1]) and exact_2col(orb[2]),
            "site action does not preserve exactness -- engine bug")
    savg = {e: [[sum(o[e][a][b] for o in orb) / 3 for b in range(2)]
                for a in range(2)] for e in A}
    sbad = [w for w in itertools.product(range(2), repeat=N)
            if haf_word(savg, w) != (1 if len(set(w)) == 1 else 0)]
    require(sbad, "sigma-average of an exact orbit is exact -- unexpected")
    MAN.mark("avg_counterexample")
    R["averaging"] = {
        "pair_average_fails": True, "pair_avg_violations": len(bad),
        "sigma_average_fails": True, "sigma_avg_violations": len(sbad),
        "example_violating_word": list(bad[0]),
        "note": "X_4 conditions are homogeneous of degree 4 in the source; "
                "the locus is a cone, closed under the group action, NOT "
                "closed under averaging.  W28-SYM averages the SOLUTION SET "
                "OF A LINEAR SYSTEM at a symmetric background, never sources."
    }
    print("averaging: pair average fails on", len(bad), "words; sigma average"
          " fails on", len(sbad), "words => no transfer from the symmetric"
          " theorem")


def task_orbit_and_torus():
    """X_k invariance under S_8 x S_3 and under the gauge torus; and degree-4
    homogeneity (which is what forbids averaging)."""
    rng = random.Random(2718)
    src = zero_source(N)
    for e in src:
        for a in range(3):
            for b in range(3):
                src[e][a][b] = Fraction(rng.randint(-5, 5))
    words = [tuple(rng.randrange(3) for _ in range(N)) for _ in range(20)]
    # site permutation
    perm = list(range(N))
    rng.shuffle(perm)
    psrc = zero_source(N)
    for (u, v) in src:
        pu, pv = perm[u], perm[v]
        for a in range(3):
            for b in range(3):
                if pu < pv:
                    psrc[(pu, pv)][a][b] = src[(u, v)][a][b]
                else:
                    psrc[(pv, pu)][b][a] = src[(u, v)][a][b]
    for w in words:
        pw = [0] * N
        for i in range(N):
            pw[perm[i]] = w[i]
        require(haf_word(src, w) == haf_word(psrc, tuple(pw)),
                "site equivariance failed")
    # colour permutation
    cp = [1, 2, 0]
    csrc = zero_source(N)
    for e in src:
        for a in range(3):
            for b in range(3):
                csrc[e][cp[a]][cp[b]] = src[e][a][b]
    for w in words:
        require(haf_word(src, w) == haf_word(csrc, tuple(cp[x] for x in w)),
                "colour equivariance failed")
    MAN.mark("orbit_invariance")
    # gauge torus: lambda_u^c with prod_u lambda_u^c = 1
    lam = [[Fraction(rng.randint(1, 4)) for _ in range(3)] for _ in range(N)]
    for c in range(3):
        pr = Fraction(1)
        for u in range(N - 1):
            pr *= lam[u][c]
        lam[N - 1][c] = 1 / pr
    gsrc = zero_source(N)
    for (u, v) in src:
        for a in range(3):
            for b in range(3):
                gsrc[(u, v)][a][b] = src[(u, v)][a][b] * lam[u][a] * lam[v][b]
    for w in words:
        f = Fraction(1)
        for i in range(N):
            f *= lam[i][w[i]]
        require(haf_word(gsrc, w) == f * haf_word(src, w), "torus action bad")
    for c in range(3):
        cw = (c,) * N
        require(haf_word(gsrc, cw) == haf_word(src, cw),
                "torus does not fix the constant words")
    MAN.mark("torus_invariance")
    # degree-4 homogeneity
    t = Fraction(3)
    tsrc = {e: [[t * src[e][a][b] for b in range(3)] for a in range(3)]
            for e in src}
    for w in words[:6]:
        require(haf_word(tsrc, w) == t ** 4 * haf_word(src, w),
                "not degree-4 homogeneous")
    MAN.mark("degree4_homogeneity")
    R["invariance"] = {"site_perm": True, "colour_perm": True,
                       "gauge_torus_dim": 3 * N - 3,
                       "degree_in_source": N // 2}
    print("invariance controls: S_8 x S_3 equivariance OK; gauge torus (dim",
          3 * N - 3, ") fixes every constant word; H is degree", N // 2,
          "homogeneous")


def main():
    task_pairexact()
    task_census()
    task_avg()
    task_orbit_and_torus()
    R["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
