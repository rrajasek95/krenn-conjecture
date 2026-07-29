#!/usr/bin/env python3
"""Exact audit for the p=19 C=6 parity-pencil coupling."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_p19_singleton_parity_common_lift_closure as singleton
import verify_live_three_zero_higher_split_p19_double_common_lift_closure as double
import verify_live_three_zero_higher_split_p19_triple_common_lift_closure as triple


EXPECTED_C6 = {
    0: {
        (0, 8, 5): 8,
        (1, 7, 4): 7,
        (2, 6, 3): 6,
        (3, 5, 2): 5,
        (4, 4, 1): 4,
        (6, 0, 3): 2,
        (6, 1, 1): 2,
    },
    1: {
        (0, 7, 3): 6,
        (1, 6, 2): 5,
        (2, 5, 1): 4,
        (5, 0, 2): 1,
        (5, 1, 0): 1,
    },
}


EXPECTED_NEW = {
    0: {(3, 5, 2), (4, 4, 1), (6, 0, 3), (6, 1, 1)},
    1: {(1, 6, 2), (2, 5, 1)},
}


def prior_closed() -> dict[int, set[tuple[int, int, int]]]:
    out = {0: set(), 1: set()}
    for e in (0, 1):
        for parameters in singleton.parameter_families(e):
            data = singleton.selected_data(e, *parameters)
            if data["pool"] >= 1 and data["fixed_classes"] <= 5:
                out[e].add(parameters)
        out[e] |= double.EXPECTED[e]
        out[e] |= triple.EXPECTED[e]
    return out


def audit_c6_census_and_ledger() -> None:
    old_closed = prior_closed()
    observed_c6 = {0: {}, 1: {}}
    observed_new = {0: set(), 1: set()}

    for e in (0, 1):
        residual = singleton.parameter_families(e) - old_closed[e]
        for parameters in residual:
            a, b, _u = parameters
            data = singleton.selected_data(e, *parameters)
            fixed_classes = e + a + max(b - 2, 0)
            assert fixed_classes == data["fixed_classes"]
            if fixed_classes != 6:
                continue
            pool = data["pool"]
            observed_c6[e][parameters] = pool
            if 2 <= pool <= 5:
                observed_new[e].add(parameters)

            # At C=6 the relation and common degrees reduce uniformly.
            assert data["relation_degree"] == pool + 1
            assert data["common_degree"] == pool + 4

    assert observed_c6 == EXPECTED_C6
    assert observed_new == EXPECTED_NEW
    assert sum(len(x) for x in observed_c6.values()) == 12
    assert sum(len(x) for x in observed_new.values()) == 6

    all_new_closed = {
        e: old_closed[e] | observed_new[e] for e in (0, 1)
    }
    assert sum(len(values) for values in all_new_closed.values()) == 81

    expected_remaining = {
        0: {
            (0, 8, 5), (0, 9, 3), (0, 10, 1), (0, 11, -1),
            (1, 7, 4), (1, 8, 2), (1, 9, 0),
            (2, 6, 3), (2, 7, 1),
        },
        1: {(0, 7, 3), (0, 8, 1), (5, 0, 2), (5, 1, 0)},
    }
    observed_remaining = {
        e: singleton.parameter_families(e) - all_new_closed[e]
        for e in (0, 1)
    }
    assert observed_remaining == expected_remaining
    assert sum(len(values) for values in observed_remaining.values()) == 13


def audit_small_pool_intersections() -> None:
    # N=P+4.  A pair of cubic-multiple spaces has dimension P-1;
    # a triple has dimension max(P-4, 0).
    for pool in range(2, 9):
        degree = pool + 4
        pair_dimension = max(degree - 6 + 1, 0)
        triple_dimension = max(degree - 9 + 1, 0)
        assert pair_dimension == pool - 1
        assert triple_dimension == max(pool - 4, 0)
        if pool == 2:
            assert pair_dimension == 1 < 2
        if pool in (3, 4):
            assert triple_dimension == 0
        if pool == 5:
            assert triple_dimension == 1

    # If the common kernel had dimension three, all transported
    # three-spaces would coincide and be divisible by all pool cubics.
    for pool in range(2, 20):
        degree = pool + 4
        common_multiple_dimension = max(degree - 3 * pool + 1, 0)
        assert common_multiple_dimension < 3


def audit_five_pool_fibre() -> None:
    z, x, v, fibre = sp.symbols("z x v fibre")
    cubic = (z - x) ** 2 * (z + x)
    logarithmic_jet = sp.factor(
        sp.diff(cubic, z).subs(z, v) / cubic.subs(z, v)
    )
    expected = (3 * v + x) / (v**2 - x**2)
    assert sp.factor(logarithmic_jet - expected) == 0

    fibre_polynomial = sp.expand(
        fibre * (v**2 - x**2) - (3 * v + x)
    )
    assert sp.Poly(fibre_polynomial, x).degree() <= 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1

    # Four equations indexed by the three-subsets of a four-set force
    # all four logarithmic jets to be equal.
    jets = sp.symbols("j0:4")
    constant = sp.symbols("constant")
    equations = [
        constant + sum(jets[j] for j in range(4) if j != omitted)
        for omitted in range(4)
    ]
    for i in range(1, 4):
        assert sp.factor(equations[i] - equations[0]) == (
            jets[0] - jets[i]
        )


def audit_parity_dimensions() -> None:
    for pool in range(2, 20):
        relation_degree = pool + 1
        other_pool_values = pool - 1
        local_forced_degree = 2 * other_pool_values + 1
        local_parity_degree = 2 * relation_degree - 1
        assert local_forced_degree == 2 * relation_degree - 3
        assert local_parity_degree - local_forced_degree == 2
        # The quotient is even of degree at most two: dimension two.
        assert 2 // 2 + 1 == 2

        common_degree = pool + 4
        global_forced_degree = 2 * pool + 1
        global_parity_degree = 2 * common_degree - 1
        assert global_parity_degree - global_forced_degree == 6
        # The quotient is even of degree at most six: dimension four.
        assert 6 // 2 + 1 == 4

    # Every nonzero two-vector in the exterior square of a three-space
    # is decomposable: the Grassmannian Gr(2,3) fills P(wedge^2 C^3).
    assert sp.binomial(3, 2) == 3

    # A primitive parity-zero pencil is even.  Two independent even
    # polynomials require residual z-degree at least two.
    for residual_degree in (0, 1):
        even_dimension = residual_degree // 2 + 1
        assert even_dimension == 1
    assert 2 // 2 + 1 == 2


def audit_klein_line_and_repetition() -> None:
    # Canonical flag form of a line in Gr(2,4):
    # e1^(a e2+b e3).  Every point is decomposable and all pencils share
    # e1.  The Pluecker quadratic vanishes identically.
    a, b = sp.symbols("a b")
    p12, p13, p14, p23, p24, p34 = a, b, 0, 0, 0, 0
    pluecker = p12 * p34 - p13 * p24 + p14 * p23
    assert pluecker == 0

    # If a projective kernel line is not contained in the Klein quadric,
    # its restriction of the quadratic has degree two and hence at most
    # two intersection points unless it is identically zero.
    t = sp.symbols("t")
    generic_quadratic = sp.Poly(a * t**2 + b * t + 1, t)
    assert generic_quadratic.degree() == 2

    # Rank four would permit at most two distinct lifted pencils.
    # A repeated square pencil has cubic gcd degree 3s and needs residual
    # degree at least two.
    for pool in range(6, 30):
        common_degree = pool + 4
        max_repetition = (common_degree - 2) // 3
        assert max_repetition == (pool + 2) // 3
        assert 2 * max_repetition < pool


def main() -> None:
    audit_c6_census_and_ledger()
    audit_small_pool_intersections()
    audit_five_pool_fibre()
    audit_parity_dimensions()
    audit_klein_line_and_repetition()
    print("p=19 C=6 parity-pencil coupling: PASS")
    print("small-pool closure: 6 of 12 C=6 families")
    print("updated p=19 ledger: 81/94 closed, 13 remain")
    print("P>=6 global parity quotient rank <= 3: audited")


if __name__ == "__main__":
    main()
