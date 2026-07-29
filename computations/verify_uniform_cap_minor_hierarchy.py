#!/usr/bin/env python3
"""Exact symbolic audit of the uniform cap-minor hierarchy."""

import math

import sympy as sp


def check(d: int, m: int) -> None:
    x = sp.symbols("x")
    aa = sp.Matrix(d, d, lambda i, j: sp.symbols(f"a{i}{j}"))
    ell = sp.Matrix(d, 1, lambda i, _: sp.symbols(f"l{i}"))
    row = sp.Matrix(1, d, lambda _, j: sp.symbols(f"r{j}"))
    rank_one = ell * row

    lhs = sp.Rational(d, math.factorial(m)) * x ** (m - d) * (
        x * aa + sp.Rational(m, d) * rank_one
    ).det()

    h = x**m / math.factorial(m)
    q = x ** (m - 1) / math.factorial(m - 1)
    rhs = 0
    for i in range(d):
        for j in range(d):
            cof = (-1) ** (i + j) * aa.minor_submatrix(i, j).det() if d > 1 else 1
            rhs += cof * (aa[i, j] * h + rank_one[i, j] * q)

    assert sp.expand(lhs - rhs) == 0, (d, m, sp.factor(lhs - rhs))


def check_invertible_factorization(m: int) -> None:
    x = sp.symbols("x")
    aa = sp.Matrix(3, 3, lambda i, j: sp.symbols(f"a{i}{j}"))
    ell = sp.Matrix(3, 1, lambda i, _: sp.symbols(f"l{i}"))
    row = sp.Matrix(1, 3, lambda _, j: sp.symbols(f"r{j}"))
    adj_scalar = (row * aa.adjugate() * ell)[0]

    direct = (x * aa + sp.Rational(m, 3) * ell * row).det()
    expected = x**3 * aa.det() + sp.Rational(m, 3) * x**2 * adj_scalar
    assert sp.expand(direct - expected) == 0, m


def main() -> None:
    checked = []
    for m in range(3, 9):
        for d in range(1, 4):
            check(d, m)
            checked.append((d, m))
        check_invertible_factorization(m)
    print(f"PASS uniform cap-minor hierarchy: {len(checked)} minor/order cases")
    print("PASS rank-one determinant factorization for m=3,...,8")


if __name__ == "__main__":
    main()
