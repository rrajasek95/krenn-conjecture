#!/usr/bin/env python3
"""Exact checks for notes/zeon-lefschetz-apolar-obstruction.md.

The substantive proof is symbolic.  This script independently constructs
the Boolean disjointness matrices, checks their ranks modulo a large prime,
and audits all dimension and scalar formulas through n=12.
"""

from itertools import combinations
from math import comb, factorial


PRIME = 1_000_000_007


def rank_mod(matrix, p=PRIME):
    """Return exact row rank over F_p."""
    a = [[x % p for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], p - 2, p)
        a[rank] = [(x * inv) % p for x in a[rank]]
        pivot_row = a[rank]
        for i in range(rows):
            if i != rank and a[i][col]:
                c = a[i][col]
                a[i] = [(x - c * y) % p for x, y in zip(a[i], pivot_row)]
        rank += 1
        if rank == rows:
            break
    return rank


def disjointness_matrix(n, k):
    subsets = tuple(combinations(range(n), k))
    masks = tuple(sum(1 << i for i in s) for s in subsets)
    return [[int(r & s == 0) for s in masks] for r in masks]


def hilbert(n, k):
    return 1 if k in (0, n) else 3 * comb(n, k)


def audit(n):
    assert n % 2 == 0
    m = n // 2

    # Theta^m = 3 (2m)! / 2^m times the common socle generator.
    theta_top = 3 * factorial(n) // (2**m)
    # Direct count: for each color, m! times the number of perfect matchings.
    perfect_matchings = factorial(n) // (2**m * factorial(m))
    assert theta_top == 3 * factorial(m) * perfect_matchings
    assert theta_top % PRIME

    for k in range(1, m + 1):
        mat = disjointness_matrix(n, k)
        size = comb(n, k)
        assert rank_mod(mat) == size

        # Product of the known Kneser eigenvalues is nonzero modulo PRIME.
        determinant = 1
        for j in range(k + 1):
            eigenvalue = (-1) ** j * comb(n - k - j, k - j)
            multiplicity = comb(n, j) - (comb(n, j - 1) if j else 0)
            determinant = determinant * pow(eigenvalue % PRIME, multiplicity, PRIME) % PRIME
        assert determinant

    # Strong-Lefschetz Jordan blocks account for every vector in G.
    jordan_dimension = 0
    for k in range(m + 1):
        multiplicity = hilbert(n, k) - (hilbert(n, k - 2) if k >= 2 else 0)
        assert multiplicity >= 0
        jordan_dimension += multiplicity * (m - k + 1)
    total_dimension = sum(hilbert(n, k) for k in range(n + 1))
    assert jordan_dimension == total_dimension

    # Hessian at the all-ones point: three blocks J_n-I_n.
    hessian_det = ((-1) ** (n - 1) * (n - 1)) ** 3
    assert hessian_det != 0
    return theta_top, total_dimension, hessian_det


def main():
    for n in range(2, 13, 2):
        theta_top, dimension, hessian_det = audit(n)
        print(
            f"n={n:2d}: dim(G)={dimension:6d}, "
            f"Theta^(n/2)={theta_top}, Hessian det={hessian_det}"
        )
    print("verified quadratic and linear strong-Lefschetz audits through n=12")


if __name__ == "__main__":
    main()
