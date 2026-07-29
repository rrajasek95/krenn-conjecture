#!/usr/bin/env python3
"""Exact audit of the uniform stationary/developable-secant lemma.

The script checks the parameter identities, local parity division, all
terminal bundle inequalities, and the four p=20 one-quintuple selections.
It does not use floating-point arithmetic.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_q5_boundary_census as q5


def weight(sequence: tuple[int, ...]) -> int:
    return sum(value - index for index, value in enumerate(sequence))


def audit_capped_mass_and_saturation() -> None:
    # M4=19 means sum min(mi,4)=20-P.  Check the symbolic four-space
    # equality and the uniform five-space gap for every theorem parameter.
    for fixed_classes in range(4, 8):
        minimum_pool = max(1, 2 * fixed_classes - 9)
        for pool in range(minimum_pool, 30):
            common_degree = pool + fixed_classes - 2
            fixed_four_mass = 20 - pool
            if fixed_four_mass < 0:
                continue

            forced_four = 3 * pool + 4 * fixed_classes - fixed_four_mass
            cap_four = 4 * (common_degree + 1 - 4)
            assert forced_four == cap_four == 4 * pool + 4 * fixed_classes - 20

            # The fifth cap adds at most one for every fixed class.
            capped_five_mass_upper = 19 + fixed_classes
            assert capped_five_mass_upper <= 26 < 29
            assert 29 - capped_five_mass_upper > 0

            # A common three-space of multiples of all P cubics would
            # require 3P <= N-2.  The theorem range gives the opposite.
            assert 2 * pool > fixed_classes - 4
            assert 3 * pool > common_degree - 2

    assert weight((0, 2, 3, 4)) == 3
    assert weight((0, 3, 4, 5)) == 6

    # Every genuine gcd order increases the nominal local cost.  The
    # case g=m is handled separately by exactness/maximality in the proof.
    for multiplicity in range(1, 13):
        nominal = max(0, 4 - multiplicity)
        for gcd_order in range(1, 15):
            if gcd_order < multiplicity:
                corrected = 4 * gcd_order + max(
                    0, 4 - (multiplicity - gcd_order)
                )
                assert corrected > nominal
            elif gcd_order > multiplicity:
                assert 4 * gcd_order > nominal

    # Equality at infinity forces the four top echelon degrees.
    for common_degree in range(5, 30):
        echelon = tuple(range(common_degree - 3, common_degree + 1))
        cap = 4 * (common_degree - 3)
        assert sum(echelon) - 6 == cap
        for index in range(4):
            dropped = list(echelon)
            dropped[index] -= 1
            if all(dropped[i] < dropped[i + 1] for i in range(3)):
                assert sum(dropped) - 6 < cap


def audit_parity_quotient_and_degree_drops() -> None:
    # Stationary positive branch and regular negative branch.  The first
    # divided Pluecker vector is nonzero, so no quotient gcd has a pool root.
    t, alpha, mu = sp.symbols("t alpha mu", nonzero=True)
    positive = sp.Matrix([1 + alpha * t, t**2, t**3, t**4])
    # This is F(-q-t); differentiating F(-z) contributes the displayed
    # local sign, but only nonvanishing of the transverse vector matters.
    negative = sp.Matrix([mu, -t, 0, t**2])
    minors = sp.Matrix(
        [
            sp.expand(
                positive[i] * negative[j]
                - positive[j] * negative[i]
            )
            for i in range(4)
            for j in range(i + 1, 4)
        ]
    )
    divided_value = sp.simplify(minors.diff(t).subs(t, 0))
    assert divided_value == sp.Matrix([-1, 0, 0, 0, 0, 0])

    for fixed_classes in range(4, 8):
        for pool in range(1, 12):
            common_degree = pool + fixed_classes - 2
            numerator_degree = 2 * common_degree - 1
            forced_divisor_degree = 2 * pool + 1
            quotient_z_degree = numerator_degree - forced_divisor_degree
            assert quotient_z_degree == 2 * fixed_classes - 6
            assert quotient_z_degree // 2 == fixed_classes - 3

            raw_degree = fixed_classes - 3
            # Removing a homogeneous gcd, including infinity, only lowers d.
            for gcd_degree in range(raw_degree + 1):
                actual_degree = raw_degree - gcd_degree
                assert 0 <= actual_degree <= raw_degree

    # A nonzero alternating form in dimension four has rank two or four.
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    skew = sp.Matrix(
        [[0, a, b, c], [-a, 0, d, e], [-b, -d, 0, f], [-c, -e, -f, 0]]
    )
    pfaffian = a * f - b * e + c * d
    assert sp.factor(skew.det()) == sp.factor(pfaffian**2)


def audit_developability_and_terminal_inequalities() -> None:
    for fixed_classes in range(4, 8):
        minimum_pool = max(1, 2 * fixed_classes - 9)
        for pool in range(minimum_pool, 30):
            common_degree = pool + fixed_classes - 2
            for secant_degree in range(1, fixed_classes - 2):
                determinant_degree = 2 * secant_degree - 4
                assert pool > determinant_degree

                # Cone directions must span P2, hence d>=2.  Combining
                # 2c<=3(d-2) with the signed quotient zeros yields this.
                if secant_degree >= 2:
                    cone_upper = fixed_classes + secant_degree - 8
                    assert cone_upper <= 2 * fixed_classes - 11
                    assert pool > cone_upper

                    critical_budget = 3 * (secant_degree - 2)
                    quotient_degree = common_degree - 2 * secant_degree
                    assert 2 * pool > quotient_degree + critical_budget

    # Enumerate every nonplanar symplectic pair allowed by C<=7,
    # d<=C-3, e>=3, and the nonzero quotient form O(2(d-e)-2).
    admissible = []
    for fixed_classes in range(4, 8):
        for secant_degree in range(1, fixed_classes - 2):
            for edge_degree in range(3, 15):
                k = secant_degree - edge_degree
                form_degree = 2 * k - 2
                if form_degree >= 0:
                    admissible.append(
                        (fixed_classes, secant_degree, edge_degree, k, form_degree)
                    )
    assert admissible == [(7, 4, 3, 1, 0)]

    fixed_classes, secant_degree, edge_degree, k, form_degree = admissible[0]
    assert form_degree == 0
    minimum_pool = 2 * fixed_classes - 9
    for pool in range(minimum_pool, 20):
        common_degree = pool + fixed_classes - 2
        quotient_zero_degree = common_degree - 2 * k
        assert quotient_zero_degree == pool + fixed_classes - 4
        assert 2 * pool > quotient_zero_degree
        assert pool > fixed_classes - 4

    # General exact symplectic relaxation:
    # s<=2k-2 and 2(P-s)<=N-2k imply P<=C+2k-6.
    for fixed_classes in range(4, 15):
        for k in range(1, 8):
            for pool in range(1, 30):
                common_degree = pool + fixed_classes - 2
                maximal_s = 2 * k - 2
                relaxed_rhs = common_degree - 2 * k + 2 * maximal_s
                if 2 * pool <= relaxed_rhs:
                    assert pool <= fixed_classes + 2 * k - 6

    # The decomposable Schubert condition is the derivative numerator
    # of projection from the fixed line.
    x = sp.symbols("x")
    u = sp.Function("u")(x)
    v = sp.Function("v")(x)
    numerator = sp.diff(u, x) * v - u * sp.diff(v, x)
    assert sp.simplify(sp.diff(u / v, x) * v**2 - numerator) == 0


def p20_profile(h: int, triples: int) -> tuple[int, ...]:
    doubles = 7 - triples
    singleton_offset = 3 - triples
    return (
        (5,)
        + (3,) * triples
        + (2,) * doubles
        + (1,) * (h + singleton_offset)
    )


def audit_p20_application() -> None:
    observed = []
    for triples in range(4):
        doubles = 7 - triples
        singleton_offset = 3 - triples
        pool = 6 - triples
        fixed_classes = 6
        common_degree = pool + fixed_classes - 2
        fixed = (5,) + (3,) * triples + (2,) * (5 - triples)
        complement = tuple(sorted(fixed + (1,) * (pool - 1), reverse=True))

        assert sum(complement) == 20
        assert (pool - 1) + sum(min(value, 5) for value in fixed) == 20
        assert (pool - 1) + sum(min(value, 4) for value in fixed) == 19
        assert common_degree == 10 - triples
        assert pool >= 2 * fixed_classes - 9 == 3
        assert 3 * pool > common_degree - 2

        forced = 3 * pool + sum(max(0, 4 - value) for value in fixed)
        cap = 4 * (common_degree + 1 - 4)
        assert forced == cap

        for h in range(13, 20):
            krenn_k = 20 - h
            q6_gap = 22 - h + max(0, 6 - krenn_k)
            assert q6_gap > 0

            profile = p20_profile(h, triples)
            assert sum(profile) == 20 + h + 2
            assert q5.applicability_formula(profile, h)
            assert q5.high_excess(profile) == 2
            assert q5.capped_mass(complement) == 18

            selection = q5.Selection(2, 0, complement)
            assert selection in q5.formal_selections(profile, h, 20)

            selected_singletons = h - 2
            assert profile.count(1) - selected_singletons == pool - 1

        observed.append(
            (triples, doubles, singleton_offset, pool, common_degree, fixed)
        )

    assert observed == [
        (0, 7, 3, 6, 10, (5, 2, 2, 2, 2, 2)),
        (1, 6, 2, 5, 9, (5, 3, 2, 2, 2, 2)),
        (2, 5, 1, 4, 8, (5, 3, 3, 2, 2, 2)),
        (3, 4, 0, 3, 7, (5, 3, 3, 3, 2, 2)),
    ]

    # Record the first exact gaps rather than silently extending the claim.
    c6_next_pool = 2
    assert c6_next_pool <= 2 * 6 - 10  # O(2) may use both stationary roots.
    assert max(4, 3, 2, 1) < 2 * 7 - 9  # Every C=7 quintuple pool is too small.


def main() -> None:
    audit_capped_mass_and_saturation()
    audit_parity_quotient_and_degree_drops()
    audit_developability_and_terminal_inequalities()
    audit_p20_application()
    print("uniform stationary/developable-secant lemma: PASS")
    print("four-capped mass 19, 4<=C<=7, P>=2C-9: audited")
    print("cone, decomposable-edge, symplectic-edge branches: exhausted")
    print("p=20 one-quintuple C=6 application: 4 families")


if __name__ == "__main__":
    main()
