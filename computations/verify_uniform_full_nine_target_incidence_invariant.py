#!/usr/bin/env python3
"""Exact audits for the uniform full-nine target-incidence invariant."""

from itertools import combinations, permutations

import sympy as sp


def audit_divided_power_normalization() -> None:
    # q*q^[m-1] = q^m/(m-1)! = m*q^m/m! = m*q^[m].
    for m in range(3, 13):
        assert sp.factorial(m) == m * sp.factorial(m - 1)


def audit_determinant_expansion() -> None:
    q = sp.symbols("Q")
    x = sp.symbols("x0:3")
    entries = sp.symbols("a00:03 a10:13 a20:23")
    a = sp.Matrix(3, 3, entries)
    d = sp.diag(*x)
    rhs = x[0] * x[1] * x[2]
    rhs -= q * (
        a[0, 0] * x[1] * x[2]
        + a[1, 1] * x[0] * x[2]
        + a[2, 2] * x[0] * x[1]
    )
    rhs += q**2 * sum(a.cofactor(i, i) * x[i] for i in range(3))
    rhs -= q**3 * a.det()
    assert sp.expand((d - q * a).det() - rhs) == 0


def audit_cauchy_binet_site_multiplicity(n: int) -> tuple[int, int]:
    sites = tuple(range(n))
    nonzero_terms = 0
    minimum = 3
    for rows in combinations(sites, 3):
        row_set = set(rows)
        for cols in combinations(sites, 3):
            col_set = set(cols)
            for perm in permutations(range(3)):
                # C_uu=0, so this determinant monomial vanishes.
                if any(rows[a] == cols[perm[a]] for a in range(3)):
                    continue
                nonzero_terms += 1
                for u in sites:
                    literal = sum(
                        u not in (rows[a], cols[perm[a]]) for a in range(3)
                    )
                    formula = 3 - int(u in row_set) - int(u in col_set)
                    assert literal == formula
                    assert literal >= 1
                    minimum = min(minimum, literal)
    return nonzero_terms, minimum


def audit_incidence_counts(n: int) -> int:
    # n=2m and each of three incidence sets has size at least n-2.
    minimum_full = n
    for n0 in range(n + 1):
        for n1 in range(n - n0 + 1):
            for n2 in range(n - n0 - n1 + 1):
                n3 = n - n0 - n1 - n2
                total = n1 + 2 * n2 + 3 * n3
                if n0 != 0 or total < 3 * (n - 2):
                    continue
                assert n3 >= n1 + n - 6
                minimum_full = min(minimum_full, n3)
    assert minimum_full == max(0, n - 6)
    return minimum_full


def audit_directed_pair_count() -> None:
    for n in range(10, 42, 2):
        bound = (6 * (n - 1)) // (n - 2)
        assert bound == 6
        if n >= 14:
            assert n * (n - 1) // 2 > 6 * n
        else:
            assert n * (n - 1) // 2 <= 6 * n


def main() -> None:
    audit_divided_power_normalization()
    audit_determinant_expansion()
    ledgers = {}
    for n in (6, 8, 10, 12):
        terms, minimum = audit_cauchy_binet_site_multiplicity(n)
        assert minimum == 1
        ledgers[n] = terms
        audit_incidence_counts(n)
    audit_directed_pair_count()
    print("Cauchy--Binet nonzero determinant terms:", ledgers)
    print("uniform full-nine target-incidence invariant: PASS")


if __name__ == "__main__":
    main()
