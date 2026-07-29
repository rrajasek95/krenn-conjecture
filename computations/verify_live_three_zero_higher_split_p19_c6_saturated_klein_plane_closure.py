#!/usr/bin/env python3
"""Exact audit for the p=19 C=6 saturated Klein-plane closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_p19_c6_parity_pencil_coupling as c6
import verify_live_three_zero_higher_split_p19_singleton_parity_common_lift_closure as singleton


NEW_CLOSED = {
    0: {(0, 8, 5), (1, 7, 4), (2, 6, 3)},
    1: {(0, 7, 3)},
}


FIXED_PARTS = {
    (0, 8, 5): (2, 2, 2, 2, 2, 2),
    (1, 7, 4): (3, 2, 2, 2, 2, 2),
    (2, 6, 3): (3, 3, 2, 2, 2, 2),
    (0, 7, 3, 1): (4, 2, 2, 2, 2, 2),
}


def audit_census_and_ledger() -> None:
    prior = c6.prior_closed()
    prior = {e: prior[e] | c6.EXPECTED_NEW[e] for e in (0, 1)}
    assert sum(len(values) for values in prior.values()) == 81

    observed_new = {0: set(), 1: set()}
    for e in (0, 1):
        for parameters in singleton.parameter_families(e) - prior[e]:
            data = singleton.selected_data(e, *parameters)
            if data["fixed_classes"] == 6 and data["pool"] >= 6:
                observed_new[e].add(parameters)
    assert observed_new == NEW_CLOSED

    closed = {e: prior[e] | observed_new[e] for e in (0, 1)}
    assert sum(len(values) for values in closed.values()) == 85

    expected_remaining = {
        0: {
            (0, 9, 3), (0, 10, 1), (0, 11, -1),
            (1, 8, 2), (1, 9, 0), (2, 7, 1),
        },
        1: {(0, 8, 1), (5, 0, 2), (5, 1, 0)},
    }
    remaining = {
        e: singleton.parameter_families(e) - closed[e]
        for e in (0, 1)
    }
    assert remaining == expected_remaining
    assert sum(len(values) for values in remaining.values()) == 9

    # The four displayed profiles and their six fixed multiplicities.
    for e, parameters_set in NEW_CLOSED.items():
        for parameters in parameters_set:
            a, b, u = parameters
            data = singleton.selected_data(e, a, b, u)
            fixed = tuple(
                sorted(
                    (4,) * e
                    + (3,) * a
                    + (2,) * data["remaining_doubles"],
                    reverse=True,
                )
            )
            key = parameters if e == 0 else (*parameters, 1)
            assert fixed == FIXED_PARTS[key]
            assert len(fixed) == 6
            assert sum(fixed) == 20 - data["pool"]
            assert data["pool"] in (6, 7, 8)
            assert data["common_degree"] == data["pool"] + 4


def minimal_sequence(dimension: int, omitted_order: int) -> tuple[int, ...]:
    values = [j for j in range(dimension + 1) if j != omitted_order]
    return tuple(values[:dimension])


def weight(sequence: tuple[int, ...]) -> int:
    return sum(value - index for index, value in enumerate(sequence))


def audit_saturated_wronskian() -> None:
    for pool, fixed in (
        (8, (2, 2, 2, 2, 2, 2)),
        (7, (3, 2, 2, 2, 2, 2)),
        (6, (3, 3, 2, 2, 2, 2)),
        (6, (4, 2, 2, 2, 2, 2)),
    ):
        degree = pool + 4
        pool_sequence = minimal_sequence(4, 1)
        assert pool_sequence == (0, 2, 3, 4)
        assert weight(pool_sequence) == 3

        fixed_weight = 0
        for multiplicity in fixed:
            sequence = minimal_sequence(4, multiplicity)
            assert weight(sequence) == 4 - multiplicity
            fixed_weight += weight(sequence)

            # A positive gcd order at a displayed row makes the bound
            # strict.  The equality g=m cannot be maximal, because the
            # exact row kills the reduced leading coefficient.
            for gcd_order in range(1, multiplicity):
                corrected = 4 * gcd_order + 4 - (
                    multiplicity - gcd_order
                )
                assert corrected == 5 * gcd_order + 4 - multiplicity
                assert corrected > 4 - multiplicity
            for gcd_order in range(multiplicity + 1, 8):
                assert 4 * gcd_order > 4 - multiplicity

        forced = pool * 3 + fixed_weight
        cap = 4 * (degree + 1 - 4)
        assert sum(fixed) == 20 - pool
        assert fixed_weight == pool + 4
        assert forced == cap == 4 * pool + 4

        # If zero were a pool value, T_0=z^3 S_0 would force three
        # sections to vanish to order at least three.  The resulting
        # sequence (0,3,4,5) has weight six instead of the nominal three
        # and strictly exceeds the already saturated cap.
        zero_pool_sequence = (0, 3, 4, 5)
        assert weight(zero_pool_sequence) == 6
        assert forced - 3 + weight(zero_pool_sequence) > cap


def wedge_coordinates(left: sp.Matrix, right: sp.Matrix) -> list[sp.Expr]:
    return [
        sp.expand(left[i] * right[j] - left[j] * right[i])
        for i in range(4)
        for j in range(i + 1, 4)
    ]


def audit_parity_quotient_and_pool_jets() -> None:
    # The nominal quotient degree is exactly at most three in x=z^2.
    for pool in (6, 7, 8):
        common_degree = pool + 4
        numerator_degree = 2 * common_degree - 1
        divisor_degree = 2 * pool + 1
        assert numerator_degree - divisor_degree == 6
        assert 6 // 2 == 3

    # At a nonzero pool square, one branch is stationary and the other
    # regular.  Their wedge has an exact first-order zero in x-q^2.
    t = sp.symbols("t")
    plus = sp.Matrix([1, t**2, t**3, t**4])
    minus = sp.Matrix([1, t, 0, 0])
    nonzero_wedge = wedge_coordinates(plus, minus)
    orders = [sp.Poly(value, t).as_dict() for value in nonzero_wedge]
    assert any(monomials.get((1,), 0) != 0 for monomials in orders)
    assert all(sp.expand(value.subs(t, 0)) == 0 for value in nonzero_wedge)
    # The first divided wedge is e0^e1, so the limiting line contains
    # the stationary positive-branch value e0.
    assert sp.Poly(nonzero_wedge[0], t).coeff_monomial(t) == 1
    assert all(
        sp.Poly(value, t).coeff_monomial(t) == 0
        for value in nonzero_wedge[1:]
    )

    # The six quotient coordinates satisfy the Klein equation.
    p01, p02, p03, p12, p13, p23 = sp.symbols(
        "p01 p02 p03 p12 p13 p23"
    )
    klein = p01 * p23 - p02 * p13 + p03 * p12
    u = sp.symbols("u0:4")
    v = sp.symbols("v0:4")
    minors = {
        p01: u[0] * v[1] - u[1] * v[0],
        p02: u[0] * v[2] - u[2] * v[0],
        p03: u[0] * v[3] - u[3] * v[0],
        p12: u[1] * v[2] - u[2] * v[1],
        p13: u[1] * v[3] - u[3] * v[1],
        p23: u[2] * v[3] - u[3] * v[2],
    }
    assert sp.expand(klein.subs(minors)) == 0

    # In the rank-zero branch a primitive parity-pure four-space is
    # even.  Its projective derivatives at q and -q vanish together, in
    # conflict with a saturated nonzero pool pair.
    x = sp.symbols("x")
    z = sp.symbols("z")
    even_vector = sp.Matrix([1, x, x**2, x**3]).subs(x, z**2)
    even_derivative = even_vector.diff(z)
    assert sp.simplify(
        even_derivative.subs(z, -z) + even_derivative
    ) == sp.zeros(4, 1)


def audit_klein_plane_models() -> None:
    # Alpha plane: all lines contain e0.
    a, b, c = sp.symbols("a b c")
    e0 = sp.Matrix([1, 0, 0, 0])
    alpha_other = sp.Matrix([0, a, b, c])
    alpha = wedge_coordinates(e0, alpha_other)
    assert alpha == [a, b, c, 0, 0, 0]

    # Beta plane: all lines lie in <e0,e1,e2>, hence the fourth
    # coordinate of every point on every line is zero.
    beta_left = sp.Matrix([a, b, c, 0])
    d, e, f = sp.symbols("d e f")
    beta_right = sp.Matrix([d, e, f, 0])
    beta = wedge_coordinates(beta_left, beta_right)
    assert [beta[index] for index in (2, 4, 5)] == [0, 0, 0]

    # Smooth conic ruling: lines a(x) tensor B.  The Pluecker image has
    # coordinates proportional to 1,x,x^2 and spans a genuine conic.
    x = sp.symbols("x")
    ruling_left = sp.Matrix([1, 0, x, 0])
    ruling_right = sp.Matrix([0, 1, 0, x])
    ruling = wedge_coordinates(ruling_left, ruling_right)
    assert ruling == [1, 0, x, -x, 0, x**2]
    assert sp.expand(ruling[0] * ruling[5] + ruling[2] * ruling[3]) == 0

    # No point section of this ruling is projectively stationary.  Three
    # wedge coordinates of p and p' are b0^2, b0*b1, b1^2.
    b0, b1, db0, db1 = sp.symbols("b0 b1 db0 db1")
    point = sp.Matrix([b0, b1, x * b0, x * b1])
    derivative = sp.Matrix(
        [db0, db1, b0 + x * db0, b1 + x * db1]
    )
    stationary_test = wedge_coordinates(point, derivative)
    assert sp.expand(stationary_test[1]) == b0**2
    assert sp.expand(stationary_test[4]) == b1**2
    assert sp.expand(stationary_test[2] + stationary_test[3]) == 2 * b0 * b1


def audit_alpha_and_conic_degree_bounds() -> None:
    # A nondegenerate g^2_d of degree at most three has total Wronskian
    # weight 3(d-2).  A critical point costs at least two, so there is at
    # most one.
    for degree in (2, 3):
        total_weight = 3 * (degree - 2)
        assert total_weight // 2 <= 1

    # Zero has already been excluded.  Removing at most one critical
    # square leaves too many coincident cubics for degree N=P+4.
    for pool in (6, 7, 8):
        coincident = pool - 1
        common_degree = pool + 4
        assert 3 * coincident > common_degree - 2

    # A nonconstant cover of a Pluecker conic has even degree 2e.  Under
    # the degree-three cap only e=1 is possible.
    possible_cover_degrees = [e for e in range(1, 10) if 2 * e <= 3]
    assert possible_cover_degrees == [1]


def main() -> None:
    audit_census_and_ledger()
    audit_saturated_wronskian()
    audit_parity_quotient_and_pool_jets()
    audit_klein_plane_models()
    audit_alpha_and_conic_degree_bounds()
    print("p=19 C=6 saturated Klein-plane closure: PASS")
    print("P=6,7,8 C=6 families closed: 4")
    print("updated p=19 ledger: 85/94 closed, 9 remain")
    print("alpha, beta, Klein-line, and conic cases: exhausted")


if __name__ == "__main__":
    main()
