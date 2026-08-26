#!/usr/bin/env python3
"""A3 Task 4 -- the descent interface: is P1's minor law N-uniform?

Two separate questions, answered separately.

(A) THE MINOR LAW ITSELF.  D is the canonical projection of a CUBIC form on
    the 9-dimensional cap space onto the determinant line Lambda^3 (x)
    Lambda^3:
        D(f) = sum_sigma sgn(sigma) * coeff_f( K_{0,s0} K_{1,s1} K_{2,s2} ).
    The claim is
        D( s^{3-j} kappa_{c_1} .. kappa_{c_j} ) = (3-j)! * (minor of A_pq
        obtained by deleting rows and columns c_1..c_j),      distinct c's,
        D = 0 whenever a colour repeats.
    s(K) = <K, A_pq> and kappa_c(K) = K_cc depend on NOTHING but the 3x3
    pair block, so the identity cannot depend on N.  Verified here exactly
    over Q on (i) random integer A_pq, (ii) the A_pq of an explicit N = 10
    source, (iii) singular / rank-1 / zero A_pq edge cases.
    Mutation control: perturb one entry of A_pq and the two sides must move
    together; perturb the CLAIMED right-hand side and they must disagree.

(B) THE TAXONOMY AROUND IT.  P1's FACT 1 ("every error component lies in
    ker D") is a statement about CUBIC error components, i.e. h = 3, N = 8.
    At half-order h the cap error is
        E = sum_{k=2}^{h} s^{h-k} r^k x^{h-k} / (k!(h-k)!),
    and s, r are LINEAR in K while x is constant, so every component of E is
    homogeneous of K-degree exactly h.  Hence
        h = 3 (N = 8): cubic  -> D applies, FACT 1 is meaningful;
        h = 4 (N = 10): quartic -> the ideal has NOTHING in degree 3, so no
        degree-3 L-monomial can block, and the determinantal obstruction has
        no analogue because Lambda^4 of a 3-space is ZERO.
    This script verifies the degree fact exactly on sample words of an
    explicit N = 10 source (and re-checks h = 3 at N = 8).
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, permutations

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a3_core import perfect_matchings

NVAR = 9                      # K_{ij}, index 3i + j


# ------------------------------------------------------------- tiny polynomials

def poly_mul(p, q):
    out = {}
    for a, ca in p.items():
        for b, cb in q.items():
            k = tuple(x + y for x, y in zip(a, b))
            out[k] = out.get(k, Fraction(0)) + ca * cb
    return {k: v for k, v in out.items() if v}


def poly_add(p, q):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, Fraction(0)) + v
        if out[k] == 0:
            del out[k]
    return out


def poly_scale(p, c):
    if c == 0:
        return {}
    return {k: v * c for k, v in p.items()}


def linear(coeffs):
    """coeffs is a length-9 list -> the linear form sum coeffs[t] K_t."""
    out = {}
    for t, c in enumerate(coeffs):
        if c:
            e = [0] * NVAR
            e[t] = 1
            out[tuple(e)] = Fraction(c)
    return out


ONE = {tuple([0] * NVAR): Fraction(1)}


def det_pairing(cubic):
    """D(f) = sum_sigma sgn(sigma) coeff_f(K_{0,s0} K_{1,s1} K_{2,s2})."""
    total = Fraction(0)
    for sigma in permutations(range(3)):
        sgn = 1
        pairs = [(i, sigma[i]) for i in range(3)]
        inv = sum(1 for a, b in combinations(range(3), 2)
                  if sigma[a] > sigma[b])
        sgn = (-1) ** inv
        e = [0] * NVAR
        for i, j in pairs:
            e[3 * i + j] += 1
        total += sgn * cubic.get(tuple(e), Fraction(0))
    return total


def minor_complement(A, deleted):
    """Minor of the 3x3 A obtained by deleting rows AND columns `deleted`."""
    keep = [i for i in range(3) if i not in deleted]
    if not keep:
        return Fraction(1)
    if len(keep) == 1:
        i = keep[0]
        return Fraction(A[i][i])
    if len(keep) == 2:
        (i, j) = keep
        return Fraction(A[i][i] * A[j][j] - A[i][j] * A[j][i])
    a, b, c = keep
    return Fraction(
        A[a][a] * (A[b][b] * A[c][c] - A[b][c] * A[c][b])
        - A[a][b] * (A[b][a] * A[c][c] - A[b][c] * A[c][a])
        + A[a][c] * (A[b][a] * A[c][b] - A[b][b] * A[c][a]))


def forms(A):
    s = linear([A[i][j] for i in range(3) for j in range(3)])
    kap = [linear([1 if t == 3 * c + c else 0 for t in range(NVAR)])
           for c in range(3)]
    return s, kap


def check_minor_law(A):
    """All 20 degree-3 monomials in L = {s, k0, k1, k2}; exact verdicts."""
    s, kap = forms(A)
    rows = []
    ok = True
    for multiset in sorted(set(tuple(sorted(c)) for c in
                               __import__("itertools").combinations_with_replacement(
                                   ["s", "k0", "k1", "k2"], 3))):
        p = ONE
        cs = []
        for tok in multiset:
            if tok == "s":
                p = poly_mul(p, s)
            else:
                c = int(tok[1])
                cs.append(c)
                p = poly_mul(p, kap[c])
        D = det_pairing(p)
        if len(set(cs)) != len(cs):
            pred = Fraction(0)
            law = "repeated colour -> 0"
        else:
            j = len(cs)
            fact = 1
            for t in range(2, 3 - j + 1):
                fact *= t
            pred = fact * minor_complement(A, set(cs))
            law = f"({3-j})! * complementary minor"
        rows.append(dict(monomial="".join(multiset), D=str(D),
                         predicted=str(pred), agree=(D == pred), law=law))
        ok = ok and (D == pred)
    return ok, rows


# ------------------------------------------------------- the h-degree statement

def cap_error_degrees(N, source, p, q, words):
    """K-degrees of the full-support cap-error components at half-order
    h = N/2 - 1, computed exactly on the given sample words."""
    U = [v for v in range(N) if v not in (p, q)]
    h = len(U) // 2
    A = {e: source[e] for e in source}

    def blk(u, v):
        return A[(u, v)] if (u, v) in A else [[A[(v, u)][j][i] for j in range(3)]
                                             for i in range(3)]

    s = linear([blk(p, q)[i][j] for i in range(3) for j in range(3)])

    def R(a, b, ca, cb):
        """R_ab(K)[ca][cb] as a linear form in K (see wsplit_core form_R)."""
        coeffs = [0] * NVAR
        Apa, Aqb = blk(min(p, a), max(p, a)), blk(min(q, b), max(q, b))
        Apb, Aqa = blk(min(p, b), max(p, b)), blk(min(q, a), max(q, a))
        pa = Apa if p < a else [[Apa[y][x] for y in range(3)] for x in range(3)]
        qb = Aqb if q < b else [[Aqb[y][x] for y in range(3)] for x in range(3)]
        pb = Apb if p < b else [[Apb[y][x] for y in range(3)] for x in range(3)]
        qa = Aqa if q < a else [[Aqa[y][x] for y in range(3)] for x in range(3)]
        for i in range(3):
            for j in range(3):
                coeffs[3 * i + j] += pa[i][ca] * qb[j][cb] + pb[i][cb] * qa[j][ca]
        return linear(coeffs)

    out = {}
    for w in words:
        col = dict(zip(U, w))
        acc = {}
        for M in perfect_matchings(tuple(U)):
            Rs = {e: R(e[0], e[1], col[e[0]], col[e[1]]) for e in M}
            As = {e: Fraction(blk(e[0], e[1])[col[e[0]]][col[e[1]]]) for e in M}
            for k in range(2, h + 1):
                for S in combinations(M, k):
                    term = ONE
                    for e in S:
                        term = poly_mul(term, Rs[e])
                    for e in M:
                        if e not in S:
                            term = poly_scale(term, As[e])
                    for _ in range(h - k):
                        term = poly_mul(term, s)
                    denom = 1
                    for t in range(2, k + 1):
                        denom *= t
                    for t in range(2, h - k + 1):
                        denom *= t
                    acc = poly_add(acc, poly_scale(term, Fraction(1, denom)))
        degs = sorted({sum(e) for e in acc})
        out["".join(map(str, w))] = dict(h=h, monomials=len(acc), degrees=degs,
                                         homogeneous_of_degree_h=(degs == [h])
                                         or (not degs))
    return out


def random_source(N, rng, lo=-4, hi=4):
    return {(u, v): [[rng.randint(lo, hi) for _ in range(3)] for _ in range(3)]
            for u, v in combinations(range(N), 2)}


def main():
    rng = random.Random(20260815)
    out = {}

    # (A1) random integer A_pq
    fails = []
    for t in range(200):
        A = [[rng.randint(-6, 6) for _ in range(3)] for _ in range(3)]
        ok, rows = check_minor_law(A)
        if not ok:
            fails.append(A)
    out["random_Apq"] = dict(tested=200, all_agree=(not fails), failures=fails)
    print("minor law on 200 random integer A_pq: all agree =", not fails)

    # (A2) A_pq drawn from an explicit N = 10 source
    src10 = random_source(10, rng)
    A10 = src10[(0, 1)]
    ok, rows = check_minor_law(A10)
    out["N10_source_Apq"] = dict(A_pq=A10, all_agree=ok, table=rows)
    print("minor law on the A_pq of an N=10 source: all agree =", ok)
    for r in rows:
        if r["monomial"] in ("sss", "k0ss", "k0k1s", "k0k1k2",
                             "k0k0s", "k0k0k0"):
            print("   ", r["monomial"], "D =", r["D"], "pred =", r["predicted"],
                  "|", r["law"])

    # (A3) edge cases
    edge = {}
    for name, A in (("zero", [[0] * 3 for _ in range(3)]),
                    ("identity", [[1 if i == j else 0 for j in range(3)]
                                  for i in range(3)]),
                    ("rank1", [[i * j for j in range(1, 4)]
                               for i in range(1, 4)]),
                    ("singular", [[1, 2, 3], [2, 4, 6], [1, 1, 1]])):
        ok, rows = check_minor_law(A)
        edge[name] = ok
    out["edge_cases"] = edge
    print("edge cases (zero/identity/rank1/singular) all agree:", edge)

    # (A4) MUTATION CONTROL: falsify the law on purpose
    A = [[rng.randint(1, 5) for _ in range(3)] for _ in range(3)]
    s, kap = forms(A)
    p = poly_mul(poly_mul(s, s), kap[0])
    D = det_pairing(p)
    good = 2 * minor_complement(A, {0})
    bad1 = 6 * minor_complement(A, {0})            # wrong factorial
    bad2 = 2 * minor_complement(A, {1})            # wrong deleted index
    out["mutation_control"] = dict(D=str(D), correct=str(good),
                                   wrong_factorial=str(bad1),
                                   wrong_index=str(bad2),
                                   correct_matches=(D == good),
                                   mutants_rejected=(D != bad1 and D != bad2))
    print("mutation control: D matches correct law =", D == good,
          "; mutants rejected =", (D != bad1 and D != bad2))

    # (B) K-degree of the cap error at h = 3 (N=8) and h = 4 (N=10)
    deg = {}
    src8 = random_source(8, rng)
    deg["N=8"] = cap_error_degrees(8, src8, 0, 1,
                                   [(0, 0, 0, 0, 0, 0), (0, 1, 2, 0, 1, 2)])
    print("N=8 (h=3) cap-error component degrees:",
          {k: v["degrees"] for k, v in deg["N=8"].items()})
    deg["N=10"] = cap_error_degrees(10, src10, 0, 1,
                                    [(0,) * 8, (0, 1, 2, 0, 1, 2, 0, 1)])
    print("N=10 (h=4) cap-error component degrees:",
          {k: v["degrees"] for k, v in deg["N=10"].items()})
    out["cap_error_degrees"] = deg

    with open(__file__.rsplit("/", 1)[0] + "/results_task4_minorlaw.json",
              "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote results_task4_minorlaw.json")


if __name__ == "__main__":
    main()
