#!/usr/bin/env python3
"""W32 / T4 -- the CLUSTER (base-colour) EXPANSION and the DETERMINATION lemma,
plus tangent-space measurements of the 2-colour exact variety.

A. THE EXPANSION.  Put xi_i = e_0 + eta_i with eta_i in span(e_1,e_2).  Then
   Phi(e_0+eta) = sum_k Phi_k(eta), Phi_k = the part with exactly k sites
   off colour 0, and X_4 at N = 8 says

     Phi_0 = 1,  Phi_1 = Phi_2 = Phi_3 = Phi_4 = Phi_7 = 0,
     Phi_5, Phi_6 vanish except on the (3,3,2)-profile monomials,
     Phi_8 = prod_i eta_i[1] + prod_i eta_i[2].

   The k = 1 and k = 2 terms, written out (kappa_0(S) := haf(A^{00}|S),
   beta^b_p[r] := A_pr[b][0]):

     (deg 1)  sum_r beta^b_p[r] kappa_0(V-p-r) = 0                for all p, b
     (deg 2)  A_pq[b][b'] kappa_0(V-p-q)
              + sum_{r != s, r,s not in {p,q}} beta^b_p[r] beta^{b'}_q[s]
                kappa_0(V-p-q-r-s) = 0                      for all p<q, b, b'

B. W32-DET.  Writing K_pq := kappa_0(V-p-q): on the stratum where K_pq != 0
   for every pair, (deg 2) DETERMINES all 112 mixed cells A_pq[b][b']
   (b,b' in {1,2}) from the 140 parameters (a, beta).  The pure cells
   A[1][1] and A[2][2] are determined twice (base colour 0 and base colour 2,
   resp. 0 and 1) -- an explicit consistency system.

C. TANGENT MEASUREMENTS of the d = 2 exact variety at n = 8 (the object
   W32-2COL forces on every pair restriction).

Checkpoint: results_t4.json.
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w32_core import (Manifest, ekey, haf_word, offcount, perfect_matchings,
                      profile, require, zero_source)  # noqa: E402

OUT = os.path.join(HERE, "results_t4.json")
N = 8
V = tuple(range(N))
R = {}
MAN = Manifest(["deg1_identity", "deg2_identity", "deg3_identity",
                "det_wellposed", "d2_tangent", "d2_tangent_mutation"])
PRIMES = (1000003, 1000033)      # both = 1 mod 3 (checked below, ledger 19)


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def kappa(src, S, c=0):
    """haf of the pure-c part over S."""
    w = {s: c for s in S}
    return haf_word(src, w, sites=S)


def rnd_source(rng, dom="Q"):
    src = zero_source(N)
    for e in src:
        for a in range(3):
            for b in range(3):
                src[e][a][b] = Fraction(rng.randint(-5, 5))
    return src


def cellv(src, u, v, a, b):
    return src[(u, v)][a][b] if u < v else src[(v, u)][b][a]


# ------------------------------------------------------------------- A / deg 1
def task_deg1():
    rng = random.Random(1001)
    checks = 0
    for _ in range(6):
        src = rnd_source(rng)
        for p in V:
            for b in (1, 2):
                w = tuple(b if i == p else 0 for i in range(N))
                lhs = haf_word(src, w)
                rhs = sum((cellv(src, p, r, b, 0)
                           * kappa(src, tuple(x for x in V if x not in (p, r))))
                          for r in V if r != p)
                require(lhs == rhs, f"deg1 identity failed at p={p},b={b}")
                checks += 1
    MAN.mark("deg1_identity")
    R["deg1"] = {"checks": checks, "mismatches": 0,
                 "n_conditions": N * 2}
    print("deg-1 cluster identity verified,", checks, "checks;",
          N * 2, "conditions (the (7,1,0) words)")


def task_deg2():
    rng = random.Random(1002)
    checks = 0
    for _ in range(4):
        src = rnd_source(rng)
        for p, q in itertools.combinations(V, 2):
            for b in (1, 2):
                for b2 in (1, 2):
                    w = tuple(b if i == p else (b2 if i == q else 0)
                              for i in range(N))
                    lhs = haf_word(src, w)
                    rest = [x for x in V if x not in (p, q)]
                    tot = cellv(src, p, q, b, b2) * kappa(
                        src, tuple(rest))
                    for r in rest:
                        for s in rest:
                            if r == s:
                                continue
                            U = tuple(x for x in rest if x not in (r, s))
                            tot += (cellv(src, p, r, b, 0)
                                    * cellv(src, q, s, b2, 0)
                                    * kappa(src, U))
                    require(lhs == tot,
                            f"deg2 identity failed at {p},{q},{b},{b2}")
                    checks += 1
    MAN.mark("deg2_identity")
    R["deg2"] = {"checks": checks, "mismatches": 0,
                 "n_conditions": len(list(itertools.combinations(V, 2))) * 4}
    print("deg-2 cluster identity verified,", checks, "checks;",
          28 * 4, "conditions (the (6,2,0)+(6,1,1) words)")


def task_deg3():
    rng = random.Random(1003)
    checks = 0
    for _ in range(2):
        src = rnd_source(rng)
        trip = list(itertools.combinations(V, 3))
        rng.shuffle(trip)
        for (p, q, r) in trip[:6]:
            for bs in itertools.product((1, 2), repeat=3):
                T = {p: bs[0], q: bs[1], r: bs[2]}
                w = tuple(T.get(i, 0) for i in range(N))
                lhs = haf_word(src, w)
                rest = [x for x in V if x not in T]
                tot = Fraction(0)
                # one internal pair + one site matched outside
                for (x, y) in itertools.combinations(list(T), 2):
                    z = [t for t in T if t not in (x, y)][0]
                    for s in rest:
                        U = tuple(t for t in rest if t != s)
                        tot += (cellv(src, x, y, T[x], T[y])
                                * cellv(src, z, s, T[z], 0)
                                * kappa(src, U))
                # all three matched outside
                for (s1, s2, s3) in itertools.permutations(rest, 3):
                    U = tuple(t for t in rest if t not in (s1, s2, s3))
                    tot += (cellv(src, p, s1, T[p], 0)
                            * cellv(src, q, s2, T[q], 0)
                            * cellv(src, r, s3, T[r], 0)
                            * kappa(src, U)) / 1
                require(lhs == tot, f"deg3 identity failed at {p},{q},{r},{bs}")
                checks += 1
    MAN.mark("deg3_identity")
    R["deg3"] = {"checks": checks, "mismatches": 0}
    print("deg-3 cluster identity verified,", checks, "checks")


def task_det():
    """W32-DET well-posedness: on which stratum is the determination valid?
    Measure how often K_pq = kappa_0(V-p-q) can vanish, given that
    sum_r a_pr K_pr = kappa_0(V) = 1 forces each row of K to be nonzero."""
    rng = random.Random(1004)
    zero_counts = {}
    for _ in range(200):
        src = zero_source(N)
        dens = rng.choice([0.2, 0.35, 0.5, 0.8, 1.0])
        for e in src:
            if rng.random() < dens:
                src[e][0][0] = Fraction(rng.randint(1, 9))
        if kappa(src, V) == 0:
            continue
        z = sum(1 for (p, q) in itertools.combinations(V, 2)
                if kappa(src, tuple(x for x in V if x not in (p, q))) == 0)
        zero_counts[z] = zero_counts.get(z, 0) + 1
    # the row condition
    rowok = True
    for _ in range(30):
        src = zero_source(N)
        for e in src:
            src[e][0][0] = Fraction(rng.randint(-4, 4))
        k = kappa(src, V)
        if k == 0:
            continue
        for p in V:
            tot = sum(cellv(src, p, r, 0, 0)
                      * kappa(src, tuple(x for x in V if x not in (p, r)))
                      for r in V if r != p)
            if tot != k:
                rowok = False
    require(rowok, "the row identity sum_r a_pr K_pr = kappa_0(V) failed")
    MAN.mark("det_wellposed")
    R["det"] = {
        "n_params_total": 252,
        "n_params_a_beta": 28 + 112,
        "n_determined_cells": 112,
        "gauge_dim": 21,
        "deg1_linear_conditions": 16,
        "K_zero_count_histogram": {str(k): v for k, v
                                   in sorted(zero_counts.items())},
        "row_identity": "sum_r a_pr K_pr = kappa_0(V) = 1, so no row of K "
                        "is identically zero on the X_4 locus",
    }
    print("W32-DET: 252 cells = 140 (a,beta) + 112 determined; gauge 21; "
          "16 linear deg-1 conditions.  K-zero histogram:", zero_counts)


# ---------------------------------------------------------- C. d=2 tangent
def ham_pair(m_a, m_b):
    src = {}
    for a, b in itertools.combinations(range(N), 2):
        src[(a, b)] = [[Fraction(0)] * 2 for _ in range(2)]
    for e in m_a:
        src[ekey(*e)][0][0] = Fraction(1)
    for e in m_b:
        src[ekey(*e)][1][1] = Fraction(1)
    return src


def haf2(src, w, sites):
    tot = Fraction(0)
    for M in perfect_matchings(tuple(sorted(sites))):
        pr = Fraction(1)
        for (u, v) in M:
            c = src[(u, v)][w[u]][w[v]] if u < v else src[(v, u)][w[v]][w[u]]
            if c == 0:
                pr = Fraction(0)
                break
            pr *= c
        tot += pr
    return tot


def d2_jacobian_rank(src, p):
    """Rank mod p of the Jacobian of the 2^8 exactness equations in the 112
    cells, at the point `src` (2-colour source)."""
    cols = [(e, a, b) for e in sorted(src) for a in range(2)
            for b in range(2)]
    cidx = {c: i for i, c in enumerate(cols)}
    basis = [None] * len(cols)
    rank = 0
    for w in itertools.product(range(2), repeat=N):
        row = [0] * len(cols)
        for (u, v) in src:
            S = tuple(x for x in V if x not in (u, v))
            val = haf2(src, w, S)
            j = cidx[((u, v), w[u], w[v])]
            row[j] = (row[j] + val.numerator
                      * pow(val.denominator, p - 2, p)) % p
        v = row
        for j in range(len(cols)):
            if v[j]:
                if basis[j] is None:
                    inv = pow(v[j], p - 2, p)
                    basis[j] = [x * inv % p for x in v]
                    rank += 1
                    break
                f = v[j]
                v = [(x - f * y) % p for x, y in zip(v, basis[j])]
    return rank


def task_d2_tangent():
    for p in PRIMES:
        require(is_prime(p) and p % 3 == 1, f"prime discipline: {p}")
    m0 = [ekey(i, i + 1) for i in range(0, N, 2)]
    m1 = [ekey(i, (i + 1) % N) for i in range(1, N, 2)]
    pts = {}
    base = ham_pair(m0, m1)
    pts["Delta2_hamiltonian"] = base
    aug = {e: [r[:] for r in m] for e, m in base.items()}
    aug[(0, 4)][0][0] = Fraction(1)
    pts["Delta2_plus_chord04"] = aug
    aug2 = {e: [r[:] for r in m] for e, m in aug.items()}
    aug2[(1, 5)][1][1] = Fraction(1)
    pts["Delta2_plus_two_chords"] = aug2
    # a weighted point in the same family
    rng = random.Random(77)
    wt = {e: [r[:] for r in m] for e, m in base.items()}
    scal = [Fraction(rng.randint(1, 5)) for _ in range(N)]
    for (u, v) in wt:
        for a in range(2):
            for b in range(2):
                wt[(u, v)][a][b] *= scal[u] * scal[v]
    # renormalise the two constant words to 1
    for c in range(2):
        h = haf2(wt, (c,) * N, V)
        if h != 0:
            f = Fraction(1)
            # scale the whole colour-c pure part by h^{-1/4} is not rational;
            # instead rescale one site's cells
            for (u, v) in wt:
                if u == 0 or v == 0:
                    wt[(u, v)][c][c] /= h
    pts["Delta2_gauged"] = wt
    out = {}
    for name, s in pts.items():
        exact = all(haf2(s, w, V) == (1 if len(set(w)) == 1 else 0)
                    for w in itertools.product(range(2), repeat=N))
        ranks = {str(p): d2_jacobian_rank(s, p) for p in PRIMES}
        out[name] = {"exact": exact, "jacobian_rank": ranks,
                     "n_params": 112,
                     "local_dim_upper": {k: 112 - v for k, v in ranks.items()},
                     "gauge_dim": 2 * N - 2}
        print(f"  {name}: exact={exact} rank={ranks} "
              f"=> tangent dim <= {112 - list(ranks.values())[0]} "
              f"(gauge dim {2*N-2})")
    MAN.mark("d2_tangent")
    R["d2_tangent"] = out
    # mutation control: a NON-exact point must be flagged
    bad = {e: [r[:] for r in m] for e, m in base.items()}
    bad[(0, 1)][0][1] = Fraction(1)
    ex = all(haf2(bad, w, V) == (1 if len(set(w)) == 1 else 0)
             for w in itertools.product(range(2), repeat=N))
    require(not ex, "d2 mutation control did not fire")
    MAN.mark("d2_tangent_mutation")
    R["d2_tangent_mutation"] = {"fired": True}
    print("  d2 mutation control fires")


def main():
    task_deg1()
    task_deg2()
    task_deg3()
    task_det()
    print("d=2 exact variety, tangent measurements:")
    task_d2_tangent()
    R["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
