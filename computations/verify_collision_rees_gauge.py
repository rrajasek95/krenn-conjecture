#!/usr/bin/env python3
"""Exact checks for the Rees collision gauges and their K4 limitation."""

from __future__ import annotations

import itertools
from fractions import Fraction


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def polynomial_product(factors):
    answer = (Fraction(1),)
    for factor in factors:
        result = [Fraction(0)] * (len(answer) + len(factor) - 1)
        for i, left in enumerate(answer):
            for j, right in enumerate(factor):
                result[i + j] += left * right
        answer = tuple(result)
    return answer


def target_coefficients(p, q):
    """Coefficient polynomial for every x/z coloring in the sheared target."""
    n = len(p)
    answer = {}
    for z_sites_mask in range(1 << n):
        minus_factors = []
        plus_factors = []
        for site in range(n):
            if z_sites_mask & (1 << site):
                minus_factors.append((Fraction(0), Fraction(-1, 2)))
                plus_factors.append((Fraction(0), Fraction(1, 2)))
            else:
                minus_factors.append((p[site],))
                plus_factors.append((q[site],))
        left = polynomial_product(minus_factors)
        right = polynomial_product(plus_factors)
        degree = max(len(left), len(right))
        answer[z_sites_mask] = tuple(
            (left[i] if i < len(left) else 0)
            + (right[i] if i < len(right) else 0)
            for i in range(degree)
        )
    return answer


def audit_multiparameter_formula():
    a = (Fraction(-6, 5), Fraction(0), Fraction(0), Fraction(0))
    p = tuple(1 - value / 2 for value in a)
    q = tuple(1 + value / 2 for value in a)
    P = polynomial_product(tuple((value,) for value in p))[0]
    R = polynomial_product(tuple((value,) for value in q))[0]
    C = P + R
    assert p == (Fraction(8, 5), 1, 1, 1)
    assert q == (Fraction(2, 5), 1, 1, 1)
    assert (P, R, C) == (Fraction(8, 5), Fraction(2, 5), 2)

    coefficients = target_coefficients(p, q)
    assert coefficients[0] == (2,)
    for site in range(4):
        expected = Fraction(-P, 2 * p[site]) + Fraction(R, 2 * q[site])
        assert coefficients[1 << site][1] == expected
    for i in range(4):
        for j in range(i + 1, 4):
            expected = Fraction(P, 4 * p[i] * p[j]) + Fraction(
                R, 4 * q[i] * q[j]
            )
            assert coefficients[(1 << i) | (1 << j)][2] == expected

    # Formula (9), followed by (12).  Here sqrt(P*R)=4/5 is rational.
    sqrt_PR = Fraction(4, 5)
    centered_minus = []
    centered_plus = []
    for pi, qi in zip(p, q, strict=True):
        c = (P / pi - R / qi) / (2 * C)
        kappa = pi * qi / sqrt_PR  # C=2
        centered_minus.append((c - Fraction(1, 2) / pi) * kappa)
        centered_plus.append((c + Fraction(1, 2) / qi) * kappa)
    assert centered_minus == [Fraction(-1, 4)] * 4
    assert centered_plus == [Fraction(1)] * 4
    for site in range(4):
        assert P * centered_minus[site] + R * centered_plus[site] == 0
    for i in range(4):
        for j in range(i + 1, 4):
            second = (
                P * centered_minus[i] * centered_minus[j]
                + R * centered_plus[i] * centered_plus[j]
            )
            assert second == Fraction(1, 2)


def k4_output(edge_tables):
    answer = {}
    for coloring in itertools.product(range(3), repeat=4):
        total = Fraction(0)
        for matching in perfect_matchings(range(4)):
            term = Fraction(1)
            for i, j in matching:
                term *= edge_tables.get((i, j, coloring[i], coloring[j]), 0)
            total += term
        answer[coloring] = total
    return answer


def audit_k4_source_and_support():
    U, V, Y = range(3)
    source = {}
    for edge in ((0, 1), (2, 3)):
        source[edge + (U, U)] = Fraction(1)
    for edge in ((0, 3), (1, 2)):
        source[edge + (V, V)] = Fraction(1)
    for edge in ((0, 2), (1, 3)):
        source[edge + (Y, Y)] = Fraction(1)
    actual = k4_output(source)
    for coloring, value in actual.items():
        expected = Fraction(1) if len(set(coloring)) == 1 else Fraction(0)
        assert value == expected

    # A nontrivial exact branch-stabilizer point.  Products in each branch
    # are one, and all six collapsed cells remain nonzero.
    lam = (Fraction(2), Fraction(3), Fraction(1, 2), Fraction(1, 3))
    mu = (Fraction(5), Fraction(1, 7), Fraction(7), Fraction(1, 5))
    nu = (Fraction(11), Fraction(1, 13), Fraction(13), Fraction(1, 11))
    assert polynomial_product(tuple((v,) for v in lam))[0] == 1
    assert polynomial_product(tuple((v,) for v in mu))[0] == 1
    assert polynomial_product(tuple((v,) for v in nu))[0] == 1
    cells = (
        lam[0] * lam[1],
        lam[2] * lam[3],
        mu[0] * mu[3],
        mu[1] * mu[2],
        nu[0] * nu[2],
        nu[1] * nu[3],
    )
    assert all(cells)
    assert cells[0] * cells[1] == 1
    assert cells[2] * cells[3] == 1
    assert cells[4] * cells[5] == 1

    # In a valuation degeneration, finiteness says that all six displayed
    # pair valuations are nonnegative.  Their complementary sums are zero,
    # so each valuation is exactly zero.  Exhaust a generous integer box as
    # an independent implementation check of the elementary implication.
    for alpha in itertools.product(range(-3, 4), repeat=3):
        alpha = alpha + (-sum(alpha),)
        uvals = (alpha[0] + alpha[1], alpha[2] + alpha[3])
        if min(uvals) >= 0:
            assert uvals == (0, 0)
    for beta in itertools.product(range(-3, 4), repeat=3):
        beta = beta + (-sum(beta),)
        vvals = (beta[0] + beta[3], beta[1] + beta[2])
        if min(vvals) >= 0:
            assert vvals == (0, 0)
    for gamma in itertools.product(range(-3, 4), repeat=3):
        gamma = gamma + (-sum(gamma),)
        yvals = (gamma[0] + gamma[2], gamma[1] + gamma[3])
        if min(yvals) >= 0:
            assert yvals == (0, 0)


def main():
    audit_multiparameter_formula()
    audit_k4_source_and_support()
    print("verified exact multi-parameter Rees target and centered two-jet")
    print("verified K4 branch-stabilizer support rigidity and discriminant limit")


if __name__ == "__main__":
    main()
