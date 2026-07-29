#!/usr/bin/env python3
"""Independent exact audit of the uniform developable-secant lemma.

This checker deliberately imports none of the proposed lemma's checker or
the earlier census scripts.  It exhausts every attainable four-capped
parameter pattern, every actual Pluecker degree after a homogeneous degree
drop, every cone critical-point budget, every symplectic edge degree, and
the four claimed p=20 selections.  SymPy is used only for two local
polynomial identities.
"""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


def wronskian_weight(sequence: tuple[int, ...]) -> int:
    return sum(order - index for index, order in enumerate(sequence))


def attainable_parameters():
    """Yield all capped patterns satisfying the theorem's hypotheses.

    Writing c_i=min(m_i,4), positivity of each multiplicity gives
    1<=c_i<=4.  The equality M4=19 then determines P exactly, so this is
    a finite and genuinely exhaustive parameter list.
    """

    for fixed_classes in range(4, 8):
        pool_floor = max(1, 2 * fixed_classes - 9)
        for capped in product(range(1, 5), repeat=fixed_classes):
            pool = 20 - sum(capped)
            if pool < pool_floor:
                continue
            assert (pool - 1) + sum(capped) == 19
            yield fixed_classes, pool, capped


def audit_saturated_four_space() -> None:
    seen: dict[int, set[int]] = {fixed_classes: set() for fixed_classes in range(4, 8)}

    for fixed_classes, pool, capped in attainable_parameters():
        seen[fixed_classes].add(pool)
        ambient_degree = pool + fixed_classes - 2

        # A fixed class with four-cap 4 can add at most one unit on passing
        # to the five-cap.  This is the worst possible M5, over every actual
        # multiplicity represented by this capped pattern.
        worst_five_mass = (pool - 1) + sum(
            value + int(value == 4) for value in capped
        )
        assert worst_five_mass <= 19 + fixed_classes <= 26
        assert 29 - worst_five_mass > 0

        # The common three-space branch would consist of multiples of all
        # pairwise-coprime moving cubics.  Three independent residuals need
        # residual degree at least two.
        assert 2 * pool > fixed_classes - 4
        assert 3 * pool > ambient_degree - 2

        forced_four = 3 * pool + sum(4 - value for value in capped)
        cap_four = 4 * (ambient_degree + 1 - 4)
        assert forced_four == cap_four == 4 * pool + 4 * fixed_classes - 20

        # Equality at infinity is possible only for the top four echelon
        # degrees N-3,...,N.  This also checks that all attainable cases
        # have enough ambient degree for a four-space.
        equality_echelons = []
        for degrees in combinations(range(ambient_degree + 1), 4):
            if sum(degrees) - 6 == cap_four:
                equality_echelons.append(degrees)
        assert equality_echelons == [
            tuple(range(ambient_degree - 3, ambient_degree + 1))
        ]

        # The raw parity quotient has x-degree C-3.  A complete homogeneous
        # gcd (including infinity) can only lower the actual map degree.
        raw_secant_degree = fixed_classes - 3
        numerator_z_degree = 2 * ambient_degree - 1
        parity_divisor_degree = 2 * pool + 1
        assert numerator_z_degree - parity_divisor_degree == 2 * raw_secant_degree
        assert raw_secant_degree + 1 == fixed_classes - 2 <= 5

        for actual_degree in range(1, raw_secant_degree + 1):
            # P distinct stationary fibers annihilate det(beta), whose
            # projective degree is 2d-4.
            assert pool > 2 * actual_degree - 4

    assert seen == {
        4: set(range(4, 17)),
        5: set(range(1, 16)),
        6: set(range(3, 15)),
        7: set(range(5, 14)),
    }

    assert wronskian_weight((0, 2, 3, 4)) == 3
    assert wronskian_weight((0, 3, 4, 5)) == 6

    # Directly exercise every gcd-order branch over a range far beyond all
    # p=20 multiplicities.  The audit note supplies the symbolic piecewise
    # proof, so this loop is a regression check rather than a finite proxy
    # for an infinite quantifier.
    for multiplicity in range(1, 65):
        nominal = max(0, 4 - multiplicity)
        for gcd_order in range(1, 65):
            if gcd_order < multiplicity:
                corrected = 4 * gcd_order + max(
                    0, 4 - (multiplicity - gcd_order)
                )
                assert corrected > nominal
            elif gcd_order > multiplicity:
                assert 4 * gcd_order > nominal
            # gcd_order=m is excluded by exactness: the reduced leading
            # coefficient is forced to vanish, enlarging the gcd.


def audit_local_parity_division() -> None:
    t, alpha, mu = sp.symbols("t alpha mu", nonzero=True)

    # A stationary positive branch and a transverse negative branch at a
    # pool pair.  Their wedge has a simple, rather than multiple or common,
    # vector zero.  The choice of higher coefficients is immaterial.
    positive = sp.Matrix([1 + alpha * t, t**2, t**3, t**4])
    negative = sp.Matrix([mu, -t, 0, t**2])
    minors = sp.Matrix(
        [
            sp.expand(positive[i] * negative[j] - positive[j] * negative[i])
            for i in range(4)
            for j in range(i + 1, 4)
        ]
    )
    divided_fiber = sp.simplify(minors.diff(t).subs(t, 0))
    assert divided_fiber == sp.Matrix([-1, 0, 0, 0, 0, 0])

    # Every nonzero alternating form in dimension four has rank two or four:
    # its determinant is the square of its Pfaffian.
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    skew = sp.Matrix(
        [[0, a, b, c], [-a, 0, d, e], [-b, -d, 0, f], [-c, -e, -f, 0]]
    )
    pfaffian = a * f - b * e + c * d
    assert sp.factor(skew.det() - pfaffian**2) == 0


def audit_terminal_branches() -> None:
    symplectic_degree_triples = set()

    for fixed_classes, pool, _ in attainable_parameters():
        ambient_degree = pool + fixed_classes - 2
        raw_secant_degree = fixed_classes - 3

        for secant_degree in range(1, raw_secant_degree + 1):
            assert pool > 2 * secant_degree - 4

            # Cone: exhaust every number c of critical pool squares allowed
            # by the degree-3(d-2) Wronskian of a spanning g^2_d.  For every
            # such c, the signed-zero inequality is strictly impossible.
            if secant_degree >= 2:
                for critical_pool in range(pool + 1):
                    if 2 * critical_pool > 3 * (secant_degree - 2):
                        continue
                    assert 2 * (pool - critical_pool) > (
                        ambient_degree - 2 * secant_degree
                    )

            # Symplectic tangent edge: a nonplanar edge has e>=3 and the
            # quotient form forces k=d-e>=1.  Exhaust every permitted zero
            # count s of that form and check the signed quotient map.
            for edge_degree in range(3, secant_degree):
                k = secant_degree - edge_degree
                form_degree = 2 * k - 2
                symplectic_degree_triples.add(
                    (fixed_classes, secant_degree, edge_degree, k)
                )
                for vanished_pool in range(min(pool, form_degree) + 1):
                    assert 2 * (pool - vanished_pool) > (
                        ambient_degree - 2 * k
                    )

    assert symplectic_degree_triples == {(7, 4, 3, 1)}

    # In the decomposable branch, the Schubert equation is exactly the
    # numerator of the derivative of projection from the fixed line.
    x = sp.symbols("x")
    u = sp.Function("u")(x)
    v = sp.Function("v")(x)
    schubert = sp.diff(u, x) * v - u * sp.diff(v, x)
    assert sp.simplify(sp.diff(u / v, x) * v**2 - schubert) == 0


def profile_for(h: int, triples: int) -> tuple[int, ...]:
    doubles = 7 - triples
    singleton_offset = 3 - triples
    return (
        (5,)
        + (3,) * triples
        + (2,) * doubles
        + (1,) * (h + singleton_offset)
    )


def audit_p20_corollary() -> None:
    expected = [
        (0, 7, 3, 6, 10, (5, 2, 2, 2, 2, 2)),
        (1, 6, 2, 5, 9, (5, 3, 2, 2, 2, 2)),
        (2, 5, 1, 4, 8, (5, 3, 3, 2, 2, 2)),
        (3, 4, 0, 3, 7, (5, 3, 3, 3, 2, 2)),
    ]
    observed = []

    for triples in range(4):
        doubles = 7 - triples
        singleton_offset = 3 - triples
        pool = 6 - triples
        fixed = (5,) + (3,) * triples + (2,) * (5 - triples)
        common_degree = pool + 6 - 2

        assert sum(fixed) + (pool - 1) == 20
        assert (pool - 1) + sum(min(value, 5) for value in fixed) == 20
        assert (pool - 1) + sum(min(value, 4) for value in fixed) == 19
        assert pool >= 3 == 2 * 6 - 9

        complement = tuple(sorted(fixed + (1,) * (pool - 1), reverse=True))
        assert sum(min(value, 3) for value in complement) == 18

        for h in range(13, 20):
            profile = profile_for(h, triples)
            assert sum(profile) == 20 + h + 2
            assert sum(max(0, value - 3) for value in profile) == 2

            # The formal d=2 selection removes two double classes and h-2
            # singleton layers.  Reconstruct its complement from scratch.
            selected_singletons = h - 2
            remaining = list(profile)
            for _ in range(2):
                remaining.remove(2)
            for _ in range(selected_singletons):
                remaining.remove(1)
            assert tuple(sorted(remaining, reverse=True)) == complement

            # The q=6 selected-row Wronskian bound is strict.  Together with
            # pair drops (dimension >=4) and the independently proved
            # low-role exclusion of dimension four, this leaves exactly the
            # five-dimensional selected kernel required by the common lift.
            krenn_k = 20 - h
            q6_gap = 22 - h + max(0, 6 - krenn_k)
            assert q6_gap > 0

        observed.append(
            (triples, doubles, singleton_offset, pool, common_degree, fixed)
        )

    assert observed == expected

    # These are genuine sharp frontiers, not silently claimed closures.
    next_c6_pool = 2
    assert next_c6_pool == 2 * 3 - 4  # det(beta) can use both roots.
    assert 4 < 2 * 7 - 9  # All C=7 one-quintuple pools miss the threshold.


def main() -> None:
    audit_saturated_four_space()
    audit_local_parity_division()
    audit_terminal_branches()
    audit_p20_corollary()
    print("independent uniform developable-secant audit: PASS")
    print("all attainable M4=19 patterns for 4<=C<=7: exhausted")
    print("homogeneous degree drops and all developable branches: exhausted")
    print("p=20 one-quintuple selections and kernel bounds: 4 families")


if __name__ == "__main__":
    main()
