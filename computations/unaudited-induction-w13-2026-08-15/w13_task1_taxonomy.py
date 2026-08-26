#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 1(c): the degree-h blocking taxonomy.

For each monomial m in L = {s, kappa_0, kappa_1, kappa_2} of degree h we decide,
EXACTLY over Q, whether m lies in

    L_h(A) = Sigma_h + s Sigma_{h-1} + ... + s^{h-2} Sigma_2 ,   s = <K, A_pq>.

Because span{E_w} is contained in L_h(A) for every source (Theorem W13.2) and
EQUALS it for generic sources (verified in w13_task1_law.py), this is exactly
the degree-h blocking taxonomy:

    m not in L_h(A)  =>  m is NOT in the degree-h error span of ANY source
                         with that A_pq  ->  m can never be a degree-h
                         blocking certificate  [universal exclusion]
    m in L_h(A)      =>  m IS in the degree-h error span of a generic source
                         with that A_pq.

h = 2 reproduces P2/W4's four laws, h = 3 reproduces AND SHARPENS P1's F2
(minor law), h = 4 is new.

Exact arithmetic: one Fraction RREF of the generator matrix per A_pq, then
exact reduction of each target.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations_with_replacement

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_core import (COLORS, NCAP, iota, kidx, monomial_index, monomials,
                      poly_mul, poly_pow, require, rref_exact, sigma_basis)
from w13_task1_law import L_generators, poly_to_row, rank_mod_p_np, P1, P2

LNAMES = ["s", "k0", "k1", "k2"]


def det3(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def cof(A, i, j):
    """The (i,j) cofactor: signed 2x2 minor complementary to row i, column j."""
    rows = [r for r in range(3) if r != i]
    cols = [c for c in range(3) if c != j]
    val = (A[rows[0]][cols[0]] * A[rows[1]][cols[1]]
           - A[rows[0]][cols[1]] * A[rows[1]][cols[0]])
    return val if (i + j) % 2 == 0 else -val


def rank3(A):
    rows = [[Fraction(x) for x in r] for r in A]
    r = 0
    for c in range(3):
        piv = None
        for i in range(r, 3):
            if rows[i][c]:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = 1 / rows[r][c]
        rows[r] = [x * inv for x in rows[r]]
        for i in range(3):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def l_monomials(h):
    """All degree-h monomials in L, as (a, b0, b1, b2) with a + sum b = h."""
    out = []
    for combo in combinations_with_replacement(range(4), h):
        a = sum(1 for x in combo if x == 0)
        b = [sum(1 for x in combo if x == c + 1) for c in range(3)]
        out.append((a, tuple(b)))
    return sorted(set(out))


def mono_name(a, b):
    parts = []
    if a:
        parts.append("s" if a == 1 else f"s^{a}")
    for c in range(3):
        if b[c] == 1:
            parts.append(f"k{c}")
        elif b[c] > 1:
            parts.append(f"k{c}^{b[c]}")
    return "".join(parts) if parts else "1"


def mono_poly(a, b, A_flat):
    sp = {(k,): A_flat[k] for k in range(NCAP) if A_flat[k]}
    poly = poly_pow(sp, a)
    for c in range(3):
        for _ in range(b[c]):
            poly = poly_mul(poly, {(kidx(c, c),): 1})
    return poly


def flat(A):
    return [A[i][j] for i in COLORS for j in COLORS]


def battery(rng):
    def rnd(lo=-6, hi=6):
        return [[rng.randint(lo, hi) for _ in range(3)] for _ in range(3)]

    def rank_r(r):
        M = [[0] * 3 for _ in range(3)]
        for _ in range(r):
            u = [rng.randint(-5, 5) for _ in range(3)]
            v = [rng.randint(-5, 5) for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    M[i][j] += u[i] * v[j]
        return M

    out = []
    while True:
        A = rnd()
        if det3(A) and all(cof(A, i, j) for i in range(3) for j in range(3)) \
                and all(A[i][j] for i in range(3) for j in range(3)):
            out.append(("generic (rank 3, all minors & entries nonzero)", A))
            break
    while True:
        A = rank_r(2)
        if rank3(A) == 2 and all(A[i][j] for i in range(3) for j in range(3)):
            out.append(("rank 2 (det=0), dense", A))
            break
    while True:
        A = rank_r(1)
        if rank3(A) == 1 and all(A[i][j] for i in range(3) for j in range(3)):
            out.append(("rank 1, dense", A))
            break
    out.append(("rank 0 (A_pq = 0)", [[0] * 3 for _ in range(3)]))
    out.append(("identity", [[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
    out.append(("permutation (0 1 2 -> 1 2 0)",
                [[0, 1, 0], [0, 0, 1], [1, 0, 0]]))
    # cofactor (0,0) = 0 but det != 0 and every entry nonzero
    while True:
        A = rnd(1, 6)
        A[1][1] = A[1][2] * A[2][1]
        A[2][2] = 1
        if det3(A) and cof(A, 0, 0) == 0 and all(A[i][j] for i in range(3)
                                                 for j in range(3)):
            out.append(("cof_00 = 0, det != 0", A))
            break
    while True:
        A = rnd(1, 6)
        A[0][0] = 0
        if det3(A) and all(cof(A, i, j) for i in range(3) for j in range(3)):
            out.append(("A_00 = 0 (diagonal entry), det != 0", A))
            break
    while True:
        A = rnd(1, 6)
        for i in (1, 2):
            for j in (1, 2):
                A[i][j] = 0
        if any(A[0][j] for j in range(3)) and any(A[i][0] for i in range(3)):
            out.append(("complementary 2x2 block to (0,0) is zero", A))
            break
    return out


def analyse(h, rng, out):
    print(f"\n===== h = {h}   (N = {2 * h + 2}) =====")
    ambient = len(monomials(NCAP, h))
    monos = l_monomials(h)
    print(f"  ambient dim S^{h} = {ambient}; {len(monos)} L-monomials")
    table = {}
    for label, A in battery(rng):
        t0 = time.time()
        Af = flat(A)
        rows, _ = L_generators(h, Af)
        basis, pivots = rref_exact(rows)
        dimL = len(pivots)
        rk_p = rank_mod_p_np(rows, P1)
        require(rk_p == dimL, ("rank mismatch mod p vs Q", rk_p, dimL))
        members, excluded = [], []
        for a, b in monos:
            vec = [Fraction(x) for x in poly_to_row(mono_poly(a, b, Af), h)]
            for r, col in enumerate(pivots):
                if vec[col]:
                    f = vec[col]
                    vec = [x - f * y for x, y in zip(vec, basis[r])]
            (members if all(x == 0 for x in vec) else excluded).append(
                mono_name(a, b))
        table[label] = {"A": A, "det": det3(A), "rank": rank3(A),
                        "dim_L": dimL, "codim": ambient - dimL,
                        "in_L (blocking possible)": members,
                        "excluded (blocking impossible)": excluded}
        print(f"\n  A_pq: {label}   rank {rank3(A)}, det {det3(A)}, "
              f"dim L_h(A) = {dimL} (codim {ambient - dimL})   "
              f"[{time.time() - t0:.0f}s]")
        print(f"     IN  L_h(A) (degree-{h} blocking possible): "
              f"{', '.join(members) if members else '(none)'}")
        print(f"     OUT of L_h(A) (blocking IMPOSSIBLE): "
              f"{', '.join(excluded) if excluded else '(none)'}")
    out[f"h{h}"] = table
    return table


def main():
    rng = random.Random(90210)
    out = {}
    analyse(2, rng, out)
    analyse(3, rng, out)
    analyse(4, rng, out)
    with open(__file__.rsplit("/", 1)[0] + "/results_taxonomy.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("\nwrote results_taxonomy.json")


if __name__ == "__main__":
    main()
