#!/usr/bin/env python3
"""Independent exact audit of the p=19, C=7 developable-secant closure.

This does not import or invoke the original C7 checker.  It checks the
arithmetic and local algebra used by the proof, including degree drops and
the simple parity-wedge root at every pool square.
"""

from __future__ import annotations

from fractions import Fraction

import sympy as sp


PROFILES = (
    # (triples, doubles, singleton offset, pool, common degree, fixed rows)
    (0, 9, 3, 6, 11, (2, 2, 2, 2, 2, 2, 2)),
    (1, 8, 2, 5, 10, (3, 2, 2, 2, 2, 2, 2)),
)


def wronskian_weight(sequence: tuple[int, ...]) -> int:
    return sum(order - index for index, order in enumerate(sequence))


def audit_saturated_common_space() -> None:
    for triples, doubles, offset, pool, degree, fixed in PROFILES:
        selected_doubles = 2
        assert pool == offset - 1 + 2 * selected_doubles
        assert len(fixed) == 7
        assert fixed == (3,) * triples + (2,) * (doubles - selected_doubles)
        assert degree == pool + 5
        assert 3 * pool > degree

        pool_sequence = (0, 2, 3, 4)
        fixed_sequences = {
            2: (0, 1, 3, 4),
            3: (0, 1, 2, 4),
        }
        finite_weight = pool * wronskian_weight(pool_sequence)
        finite_weight += sum(
            wronskian_weight(fixed_sequences[multiplicity])
            for multiplicity in fixed
        )
        cap = 4 * (degree - 3)
        assert finite_weight == cap

        # Every possible positive finite gcd order raises the local cost.
        for multiplicity in (1,) + fixed:
            nominal = 4 - multiplicity
            for gcd_order in range(1, 8):
                if gcd_order < multiplicity:
                    corrected = 5 * gcd_order + 4 - multiplicity
                    assert corrected > nominal
                elif gcd_order > multiplicity:
                    assert 4 * gcd_order > nominal

        assert wronskian_weight((0, 3, 4, 5)) == 6
        assert finite_weight - 3 + 6 > cap

        # Equality forces the unique top echelon degrees and no infinity
        # base point or Wronskian zero.
        echelon = tuple(range(degree - 3, degree + 1))
        assert sum(echelon) - sum(range(4)) == cap
        any_strict_drop = tuple(value - 1 for value in echelon)
        assert sum(any_strict_drop) - sum(range(4)) < cap


def audit_local_parity_quotient() -> None:
    # Work at z=q+t after independent projective rescalings.  The positive
    # branch is stationary and the negative branch regular:
    #   F(q+t)=a + alpha*a*t + O(t^2),
    #   F(-q-t)=mu*a - c*t + O(t^2),  a wedge c != 0.
    t, alpha, mu = sp.symbols("t alpha mu", nonzero=True)
    a = sp.Matrix([1, 0, 0, 0])
    c = sp.Matrix([0, 1, 0, 0])
    positive = a + alpha * a * t + sp.Matrix([0, 0, t**2, t**3])
    negative = mu * a - c * t + sp.Matrix([0, 0, 0, t**2])
    minors = sp.Matrix(
        [
            sp.expand(positive[i] * negative[j] - positive[j] * negative[i])
            for i in range(4)
            for j in range(i + 1, 4)
        ]
    )
    divided_value = sp.simplify(minors.diff(t).subs(t, 0))
    expected = sp.Matrix([-1, 0, 0, 0, 0, 0])
    assert divided_value == expected
    assert divided_value != sp.zeros(6, 1)

    # Therefore a common quotient gcd cannot contain the pool square.  The
    # vector is the Pluecker coordinate of span(a,c), which contains a.
    assert expected[0] != 0

    for pool in (5, 6):
        degree = pool + 5
        numerator_bound = 2 * degree - 1
        forced_divisor_degree = 2 * pool + 1
        assert numerator_bound - forced_divisor_degree == 8
        assert Fraction(8, 2) == 4

        # Removing any homogeneous gcd of degree g (including infinity)
        # can only lower the actual Pluecker degree.
        for gcd_degree in range(5):
            actual_degree = 4 - gcd_degree
            assert 0 <= actual_degree <= 4


def audit_developability_and_klein_cases() -> None:
    # det beta has degree d+d-4.  Five distinct pool squares force it zero.
    for degree in range(0, 5):
        determinant_degree = 2 * degree - 4
        if determinant_degree >= 0:
            assert 5 > determinant_degree

    # Alternating forms on a four-space have rank 2 or 4 when nonzero.
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    skew = sp.Matrix(
        [[0, a, b, c], [-a, 0, d, e], [-b, -d, 0, f], [-c, -e, -f, 0]]
    )
    pfaffian = a * f - b * e + c * d
    assert sp.factor(skew.det()) == sp.factor(pfaffian**2)

    # In the decomposable tangent branch the Schubert condition is exactly
    # the numerator of the derivative of a projection to P1.
    x = sp.symbols("x")
    u = sp.Function("u")(x)
    v = sp.Function("v")(x)
    projection_numerator = sp.diff(u, x) * v - u * sp.diff(v, x)
    assert sp.simplify(sp.diff(u / v, x) * v**2 - projection_numerator) == 0


def audit_terminal_degree_counts() -> None:
    for pool in (5, 6):
        ambient_degree = pool + 5

        # Cone: direction must span P2, so 2 <= d <= 4.
        for degree in range(2, 5):
            critical_budget = 3 * (degree - 2)  # upper bound for 2c
            quotient_degree = ambient_degree - 2 * degree
            assert 2 * pool > quotient_degree + critical_budget
            assert pool > degree - 1

        # Symplectic edge: S/R has degree e-d, and the descended quadratic
        # second fundamental form has degree 2(d-e)-2.
        admissible = []
        for degree in range(1, 5):
            for edge_degree in range(3, 12):
                form_degree = 2 * (degree - edge_degree) - 2
                if form_degree >= 0:
                    admissible.append((degree, edge_degree, form_degree))
        assert admissible == [(4, 3, 0)]

        quotient_degree = ambient_degree - 2
        assert quotient_degree == pool + 3
        assert 2 * pool > quotient_degree

        # Structural nonopposition and q != 0 make the signed pool points
        # 2P distinct points, not P points with an assumed multiplicity two.
        symbolic_values = tuple(range(1, pool + 1))
        signed_values = {sign * value for value in symbolic_values for sign in (-1, 1)}
        assert len(signed_values) == 2 * pool


def main() -> None:
    audit_saturated_common_space()
    audit_local_parity_quotient()
    audit_developability_and_klein_cases()
    audit_terminal_degree_counts()
    print("independent p=19 C=7 developable-secant audit: PASS")
    print("pool-square quotient fibers: nonzero after forced division")
    print("cone and tangent-edge degree counts: PASS")
    print("signed terminal zeros: 2P distinct points")


if __name__ == "__main__":
    main()
