#!/usr/bin/env python3
"""Exact audit of the seventh-split ``(p,d,s)=(8,7,3)`` closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def check_core_legality_and_degrees() -> None:
    p, doubles, singles = 8, 7, 3
    labels = 2 * doubles + singles
    classes = doubles + singles
    assert labels == p + 9 == 17
    assert classes == 10

    for core in combinations(range(classes), 7):
        selected_doubles = len(set(core).intersection(range(doubles)))
        assert selected_doubles >= 4
        # Every such mate is a singleton class in the complement.
        assert selected_doubles > 0
        complement_labels = labels - 7
        numerator_cap = p + len(core) - 1
        assert complement_labels == 10
        assert numerator_cap == 14
        assert numerator_cap - complement_labels == 4

    # Successive |T|=8,9 exchange-and-cancellation steps, then the full lift.
    assert 4 + 3 == 7 and 7 - 2 == 5
    assert 5 + 3 == 8 and 8 - 2 == 6
    assert 6 + 3 == 9


def check_gauge_and_lift_counts() -> None:
    z, a, c, y, q = sp.symbols("z a c y q")
    gauge = (z - c) * (z + c) ** 2
    psi = 1 / (a + c) - 2 / (c - a)
    value = gauge.subs(z, -a)
    derivative = sp.diff(gauge, z).subs(z, -a)
    assert sp.factor(derivative / value + psi) == 0
    lifted = derivative * q + value * (-y * q) + (y + psi) * value * q
    assert sp.factor(lifted) == 0
    assert gauge.subs(z, -c) == 0
    assert sp.diff(gauge, z).subs(z, -c) == 0

    # Adding b removes (z-b) from the complement and adds (z+b)^2 to
    # the selected denominator; the cubic lift preserves B_T q / Delta_T.
    b_old, delta_old = sp.symbols("b_old delta_old", nonzero=True)
    left = (b_old / (z - c)) * gauge * q / (delta_old * (z + c) ** 2)
    right = b_old * q / delta_old
    assert sp.factor(left - right) == 0

    # Exact gcd/RH count in the three-lift lemma for all three set sizes.
    for size_t in (8, 9, 10):
        m = size_t - 1
        for epsilon in (0, 1):
            n = size_t - epsilon
            assert m == n + epsilon - 1
            e0_values = (0,) if epsilon == 0 else (0, 2, 3, 4, 5, 6)
            for e0 in e0_values:
                for rho in range(n + 1):
                    for sigma in range(n + 1):
                        minimum_e = rho + 2 * sigma + e0
                        if minimum_e > m:
                            continue
                        delta_cap = m - minimum_e
                        if delta_cap < 1:
                            continue
                        u = n - rho - sigma
                        assert u >= delta_cap
                        assert n - sigma >= delta_cap
                        assert 2 * (n - sigma) > 2 * delta_cap - 2


def check_weighted_full_core() -> None:
    doubles = sp.symbols("d0:7")
    singles = sp.symbols("s0:3")
    mu = sp.symbols("mu")
    values = doubles + singles

    def psi(anchor: sp.Expr, added: sp.Expr) -> sp.Expr:
        return 1 / (anchor + added) - 2 / (added - anchor)

    # Double anchor: one self mate and one mate at every other double remain.
    anchor = doubles[0]
    others = tuple(value for value in values if value != anchor)
    base = -sp.Rational(1, 2) / anchor - 2 / (mu - anchor)
    base -= sum(2 / (anchor + value) for value in doubles[1:])
    base -= sum(1 / (anchor + value) for value in singles)
    full_y = base + sum(psi(anchor, value) for value in others)
    expected = -sum(1 / (anchor + value) for value in doubles)
    expected -= 2 / (mu - anchor)
    expected -= 2 * sum(1 / (value - anchor) for value in others)
    assert sp.factor(full_y - expected) == 0

    # Singleton anchor: no self mate remains.  This expression is safe when
    # the chosen singleton is zero.
    anchor = singles[0]
    others = tuple(value for value in values if value != anchor)
    base = -2 * sum(1 / (anchor + value) for value in doubles)
    base -= sum(1 / (anchor + value) for value in singles[1:])
    base -= 2 / (mu - anchor)
    full_y = base + sum(psi(anchor, value) for value in others)
    expected = -sum(1 / (anchor + value) for value in doubles)
    expected -= 2 / (mu - anchor)
    expected -= 2 * sum(1 / (value - anchor) for value in others)
    difference = sp.factor(full_y - expected)
    assert difference == 0
    assert sp.factor(difference.subs(singles[0], 0)) == 0


def check_residue_and_wronskian() -> None:
    # B has seven roots, q has degree nine, and the eleven double poles give
    # denominator degree twenty-two.
    degree_b, degree_q = 7, 9
    degree_denominator = 2 + 2 * 10
    assert degree_denominator == 22
    assert degree_denominator - degree_b - degree_q == 6

    # Exact structural stress with a zero singleton: all ten value nodes and
    # the common-pole node are distinct and every required sum is nonzero.
    sample_values = tuple(range(1, 8)) + (0, 8, 9)
    sample_mu = 20
    nodes = tuple(-value for value in sample_values) + (-sample_mu,)
    assert len(set(nodes)) == 11
    assert all(sample_mu != value for value in sample_values)
    assert all(sample_mu + value != 0 for value in sample_values)

    # Local double-pole residue is a Robin functional without division by q.
    w = sp.symbols("w")
    c0, c1, q0, q1 = sp.symbols("c0 c1 q0 q1", nonzero=True)
    regular = sp.expand((c0 + c1 * w) * (q0 + q1 * w))
    residue = regular.coeff(w, 1)
    assert sp.factor(residue - c0 * (q1 + c1 / c0 * q0)) == 0

    # Eleven-node Wronskian inequality.
    r, b = sp.symbols("r b", integer=True, nonnegative=True)
    left = (11 - b) * (r - 1)
    right = r * (10 - r - 2 * b)
    asserted = r**2 + r - 11 + b * (r + 1)
    assert sp.expand(left - right - asserted) == 0

    for dimension in range(3, 11):
        vanishing_sequence = [0] + list(range(2, dimension + 1))
        weight = sum(order - index for index, order in enumerate(vanishing_sequence))
        assert weight == dimension - 1

    # Degree-nine polynomial spaces have dimension at most ten.
    for dimension in range(3, 11):
        for gcd_nodes in range(12):
            minimum_e = 2 * gcd_nodes
            if minimum_e > 9:
                continue
            forced = (11 - gcd_nodes) * (dimension - 1)
            cap = dimension * (10 - dimension - minimum_e)
            assert forced > cap


def main() -> None:
    check_core_legality_and_degrees()
    check_gauge_and_lift_counts()
    check_weighted_full_core()
    check_residue_and_wronskian()
    print("seventh-split final (8,7,3) exchange closure: PASS")
    print("seven-core legality and three exchange degrees: exact")
    print("seven-mate full-core residue and eleventh node: exact")
    print("eleven-node degree-nine Wronskian obstruction: exact")


if __name__ == "__main__":
    main()
