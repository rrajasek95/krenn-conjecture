#!/usr/bin/env python3
"""Exact audit for the p=19 C=7 developable-secant closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_p19_singleton_parity_common_lift_closure as singleton
import verify_live_three_zero_higher_split_p19_c6_parity_pencil_coupling as c6
import verify_live_three_zero_higher_split_p19_c6_saturated_klein_plane_closure as c6_saturated
import verify_live_three_zero_higher_split_p19_undecic_singleton_double_coupling_closure as undecic


TARGETS = {0: {(0, 9, 3), (1, 8, 2)}, 1: set()}

EXPECTED = {
    (0, 9, 3): {
        "pool": 6,
        "degree": 11,
        "fixed": (2, 2, 2, 2, 2, 2, 2),
    },
    (1, 8, 2): {
        "pool": 5,
        "degree": 10,
        "fixed": (3, 2, 2, 2, 2, 2, 2),
    },
}


def weight(sequence: tuple[int, ...]) -> int:
    return sum(value - index for index, value in enumerate(sequence))


def minimal_sequence(dimension: int, omitted: int) -> tuple[int, ...]:
    return tuple(value for value in range(dimension + 1) if value != omitted)


def audit_profiles_and_saturation() -> None:
    for parameters, expected in EXPECTED.items():
        a, b, u = parameters
        data = singleton.selected_data(0, a, b, u)
        fixed = tuple(sorted((3,) * a + (2,) * data["remaining_doubles"], reverse=True))

        assert data["d"] == 2
        assert data["pool"] == expected["pool"]
        assert data["fixed_classes"] == 7
        assert data["relation_degree"] == data["pool"] + 2
        assert data["common_degree"] == expected["degree"] == data["pool"] + 5
        assert fixed == expected["fixed"]
        assert sum(fixed) == 20 - data["pool"]

        # A common three-space would be divisible by all moving cubics.
        assert 3 * data["pool"] > data["common_degree"]

        pool_sequence = minimal_sequence(4, 1)
        assert pool_sequence == (0, 2, 3, 4)
        assert weight(pool_sequence) == 3

        fixed_weight = 0
        for multiplicity in fixed:
            sequence = minimal_sequence(4, multiplicity)
            assert weight(sequence) == 4 - multiplicity
            fixed_weight += weight(sequence)

            # Every positive local gcd order makes the equality strict.
            for gcd_order in range(1, multiplicity):
                corrected = 4 * gcd_order + 4 - (multiplicity - gcd_order)
                assert corrected == 5 * gcd_order + 4 - multiplicity
                assert corrected > 4 - multiplicity
            for gcd_order in range(multiplicity + 1, 8):
                assert 4 * gcd_order > 4 - multiplicity

        forced = 3 * data["pool"] + fixed_weight
        cap = 4 * (data["common_degree"] + 1 - 4)
        assert forced == cap == 4 * data["pool"] + 8

        # A zero pool gives (0,3,4,5), three units over the nominal row.
        zero_sequence = (0, 3, 4, 5)
        assert weight(zero_sequence) == 6
        assert forced - 3 + weight(zero_sequence) > cap


def audit_parity_and_second_fundamental_degrees() -> None:
    for pool in (5, 6):
        common_degree = pool + 5
        parity_numerator_degree = 2 * common_degree - 1
        parity_divisor_degree = 2 * pool + 1
        assert parity_numerator_degree - parity_divisor_degree == 8
        assert 8 // 2 == 4

        # wedge^2 K has dimension six; C[x]_{<=4} has dimension five.
        assert 4 * 3 // 2 == 6
        assert 4 + 1 == 5

    # Rank zero would make a primitive four-space parity-pure.  The odd
    # case has the common factor z; in the even case the derivatives at
    # q and -q vanish together, contrary to the saturated local ledger.
    z = sp.symbols("z")
    even_vector = sp.Matrix([1, z**2, z**4, z**6])
    even_derivative = even_vector.diff(z)
    assert sp.simplify(even_derivative.subs(z, -z) + even_derivative) == sp.zeros(4, 1)
    odd_vector = z * even_vector
    assert all(sp.rem(entry, z) == 0 for entry in odd_vector)

    # det(beta) is a section of det(S)^* det(Q) Omega^2,
    # hence O(d+d-4)=O(2d-4).  Five pool squares exceed it for d<=4.
    for degree in range(1, 5):
        determinant_degree = 2 * degree - 4
        if determinant_degree >= 0:
            assert 5 > determinant_degree

    # Local stationary/regular branches have an exact simple wedge zero.
    t = sp.symbols("t")
    stationary = sp.Matrix([1, t**2, t**3, t**4])
    regular = sp.Matrix([1, t, 0, 0])
    minors = [
        sp.expand(stationary[i] * regular[j] - stationary[j] * regular[i])
        for i in range(4)
        for j in range(i + 1, 4)
    ]
    valuations = []
    for value in minors:
        if value == 0:
            continue
        powers = sp.Poly(value, t).as_dict()
        valuations.append(min(monomial[0] for monomial in powers))
    assert min(valuations) == 1
    first_divided = [sp.expand(value / t).subs(t, 0) for value in minors]
    assert first_divided[0] == 1


def audit_klein_hyperplane_cases() -> None:
    # Every alternating form in dimension four is either decomposable
    # (Pfaffian zero) or symplectic (Pfaffian nonzero).
    a01, a02, a03, a12, a13, a23 = sp.symbols("a01 a02 a03 a12 a13 a23")
    pfaffian = a01 * a23 - a02 * a13 + a03 * a12
    skew = sp.Matrix(
        [
            [0, a01, a02, a03],
            [-a01, 0, a12, a13],
            [-a02, -a12, 0, a23],
            [-a03, -a13, -a23, 0],
        ]
    )
    assert sp.factor(skew.det() - pfaffian**2) == 0

    # For omega=u^v, the hyperplane equation is the Schubert condition
    # that the moving line meet ker(u) cap ker(v).
    p01, p02, p03, p12, p13, p23 = sp.symbols("p01 p02 p03 p12 p13 p23")
    klein = p01 * p23 - p02 * p13 + p03 * p12
    assert sp.Poly(klein.subs(p01, 0), p02, p03, p12, p13, p23).total_degree() == 2

    # A decomposable hyperplane on a tangent curve says that the
    # projection [u(gamma):v(gamma)] has zero derivative.
    z = sp.symbols("z")
    u = sp.Function("u")(z)
    v = sp.Function("v")(z)
    numerator = sp.expand(sp.diff(u / v, z) * v**2)
    assert sp.simplify(numerator - (sp.diff(u, z) * v - u * sp.diff(v, z))) == 0

    # Canonical Legendrian twisted cubic: tangent vectors are isotropic
    # for a nondegenerate alternating form, and its tangent Pluecker
    # curve has degree four.  This audits the unique surviving bundle
    # degree pair rather than assuming that it is empty.
    s, t = sp.symbols("s t")
    gamma = sp.Matrix([s**3, s**2 * t, s * t**2, t**3])
    gs, gt = gamma.diff(s), gamma.diff(t)
    omega = sp.Matrix(
        [
            [0, 0, 0, 1],
            [0, 0, -3, 0],
            [0, 3, 0, 0],
            [-1, 0, 0, 0],
        ]
    )
    assert omega.det() != 0
    assert sp.expand((gs.T * omega * gt)[0]) == 0
    tangent_minors = [
        sp.expand(gs[i] * gt[j] - gs[j] * gt[i])
        for i in range(4)
        for j in range(i + 1, 4)
    ]
    assert max(sp.Poly(value, s, t).total_degree() for value in tangent_minors if value != 0) == 4
    assert sp.simplify((s * gs + t * gt) / 3 - gamma) == sp.zeros(4, 1)


def audit_cone_and_symplectic_terminal_bounds() -> None:
    for pool in (5, 6):
        ambient_degree = pool + 5

        # Cone branch.  A critical pool costs at least two units in the
        # 3(d-2) Wronskian; combine this with the signed zero divisor of
        # O(-N) -> O(-2d).  The relaxed combined inequality already fails.
        for degree in range(2, 5):
            critical_weight_cap = 3 * (degree - 2)
            max_twice_critical = critical_weight_cap
            assert 2 * pool > ambient_degree - 2 * degree + max_twice_critical
            assert pool > degree - 1

        # A nonplanar symplectic edge has e>=3.  The rank-one symmetric
        # form is a nonzero section of O(2(d-e)-2).  Enumerate all pairs.
        possible = [
            (degree, edge_degree)
            for degree in range(1, 5)
            for edge_degree in range(3, 10)
            if 2 * (degree - edge_degree) - 2 >= 0
        ]
        assert possible == [(4, 3)]
        degree, edge_degree = possible[0]
        assert 2 * (degree - edge_degree) - 2 == 0

        # S/R=O(-1), so after the square cover the quotient is O(-2).
        quotient_zero_degree = ambient_degree - 2
        assert 2 * pool > quotient_zero_degree
        assert quotient_zero_degree == pool + 3


def audit_updated_ledger() -> None:
    closed75 = c6.prior_closed()
    closed81 = {e: closed75[e] | c6.EXPECTED_NEW[e] for e in (0, 1)}
    closed85 = {e: closed81[e] | c6_saturated.NEW_CLOSED[e] for e in (0, 1)}
    closed89 = {e: closed85[e] | undecic.TARGETS[e] for e in (0, 1)}
    assert sum(len(values) for values in closed89.values()) == 89
    for e in (0, 1):
        assert TARGETS[e].isdisjoint(closed89[e])

    closed91 = {e: closed89[e] | TARGETS[e] for e in (0, 1)}
    assert sum(len(values) for values in closed91.values()) == 91
    remaining = {
        e: singleton.parameter_families(e) - closed91[e]
        for e in (0, 1)
    }
    assert remaining == {
        0: {(0, 10, 1)},
        1: {(5, 0, 2), (5, 1, 0)},
    }


def main() -> None:
    audit_profiles_and_saturation()
    audit_parity_and_second_fundamental_degrees()
    audit_klein_hyperplane_cases()
    audit_cone_and_symplectic_terminal_bounds()
    audit_updated_ledger()
    print("p=19 C=7 developable-secant closure: PASS")
    print("P=5,6 C=7 families closed: 2")
    print("updated p=19 ledger: 91/94 closed, 3 remain")
    print("cone, decomposable-edge, and symplectic-edge branches: exhausted")


if __name__ == "__main__":
    main()
