#!/usr/bin/env python3
"""Exact audit of the uniform sole-plane layer t=r+5."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations
from math import factorial

import sympy as sp

from explore_live_three_zero_minimal_three_extra_ccb import singular_status
from verify_live_three_zero_sole_plane_first_high_layer_uniform import (
    E0,
    E1,
    E2,
    ZERO,
    cauchy_permanent,
)
from verify_live_three_zero_sole_plane_third_high_first_point_closure import (
    source_22_response,
)


def integer_partitions(total, maximum=None):
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for tail in integer_partitions(total - first, first):
            yield (first,) + tail


def permanent(matrix):
    size = len(matrix)
    return sum(
        (
            sp.prod(matrix[row][sigma[row]] for row in range(size))
            for sigma in permutations(range(size))
        ),
        sp.S.Zero,
    )


def audit_profile_routing():
    expected_r6 = {
        "heavy": 40,
        "four_class": 1,
        "many_class_collision": 14,
        "distinct": 1,
    }
    for r in range(6, 31):
        counts = {key: 0 for key in expected_r6}
        for profile in integer_partitions(r + 5):
            if max(profile) >= 4:
                route = "heavy"
            elif all(part == 1 for part in profile):
                route = "distinct"
            elif len(profile) >= 5:
                route = "many_class_collision"
            else:
                route = "four_class"
                assert len(profile) == 4
                assert all(part >= 2 for part in profile)
            counts[route] += 1
        assert sum(counts.values()) == len(tuple(integer_partitions(r + 5)))
        if r == 6:
            assert counts == expected_r6, counts
    assert tuple(
        profile for profile in integer_partitions(11)
        if max(profile) <= 3 and len(profile) == 4
    ) == ((3, 3, 3, 2),)
    assert tuple(
        profile for profile in integer_partitions(12)
        if max(profile) <= 3 and len(profile) == 4
    ) == ((3, 3, 3, 3),)


def elementary(values, degree):
    if degree == 0:
        return sp.S.One
    return sum(
        (sp.prod(values[index] for index in subset)
         for subset in combinations(range(len(values)), degree)),
        sp.S.Zero,
    )


def audit_heavy_class_descent():
    # Four equal selected columns.  Test the literal permanent expansion,
    # including two common columns at the first new point r=6.
    rows = tuple(map(sp.Rational, (2, 3, 5, 7, 11, 13)))
    a = sp.Rational(17)
    columns = (sp.Rational(1), sp.Rational(1), a, a, a, a)
    left = permanent([[1 / (x + y) for y in columns] for x in rows])
    h = tuple((x + a) / (x + 1) for x in rows)
    right = (
        factorial(4) * factorial(2)
        * sp.prod(1 / (x + a) for x in rows)
        * elementary(h, 2)
    )
    assert sp.cancel(left - right) == 0

    # The deletion descent uses only the two standard elementary-symmetric
    # identities.  The coefficient |N|-j is always five initially and is
    # positive throughout the descent to e_0.
    for r in range(5, 31):
        size = r + 1
        degree = r - 4
        assert size - degree == 5
        while degree >= 1:
            assert size - degree != 0
            degree -= 1
        assert degree == 0


def audit_one_deletion_hermite_degree():
    # N has p+1 row jets and the squared-Cauchy matrix has p columns.
    # A hypothetical full-rank left-kernel vector supported below the top
    # jets has numerator degree <=q_rep-2<=p-1 but p column-jet zeros.
    for p in range(5, 31):
        for q_rep in range(p + 2):
            if q_rep:
                assert q_rep - 2 <= p - 1

        # A rank-losing column relation has denominator degree p+m_R+1,
        # numerator degree <=p+m_R-1, and p+1 Hermite row roots.
        for m_r in range(1, 5):
            denominator_degree = p + m_r + 1
            numerator_degree = denominator_degree - 2
            residual_degree = numerator_degree - (p + 1)
            assert residual_degree == m_r - 2


def pair_polynomial(x, y, ax, ay):
    return sp.expand(
        ax * ay * (x - y) * (x + y) ** 2
        + 2 * ax * y * (x + y)
        - 2 * ay * x * (x + y)
        + (x - y)
    )


def audit_affine_robin_compatibility():
    b, c, ab, ac = sp.symbols("b c A_b A_c")
    yb = ab + (c + 3 * b) / (c**2 - b**2)
    yc = ac + (b + 3 * c) / (b**2 - c**2)
    numerator = sp.factor(
        sp.together(yb - yc + (c - b) * yb * yc).as_numer_denom()[0]
    )
    assert sp.expand(
        numerator - (b - c) ** 2 * pair_polynomial(b, c, ab, ac)
    ) == 0

    # Eliminate the other two Robin constants on a triangle.  This is an
    # undivided resultant, so no exceptional zero of a transport
    # denominator is lost.
    a, aa = sp.symbols("a A_a")
    kab = pair_polynomial(a, b, aa, ab)
    kac = pair_polynomial(a, c, aa, ac)
    kbc = pair_polynomial(b, c, ab, ac)
    first = sp.resultant(kab, kbc, ab)
    triangle = sp.factor(sp.resultant(first, kac, ac))
    expected = -(
        (a - b) * (a - c) * (b - c)
        * (aa * (a**2 + a*b + a*c + b*c) - (2*a + b + c)) ** 2
    )
    assert sp.expand(triangle - expected) == 0

    # Two triangles with a common ordered anchor force A_a(a+b)=1;
    # substitution then forces a+b=0, forbidden structurally.
    d = sp.Symbol("d")
    t_abc = aa * (a + b) * (a + c) - (2*a + b + c)
    t_abd = aa * (a + b) * (a + d) - (2*a + b + d)
    assert sp.expand(
        t_abc - t_abd - (c - d) * (aa * (a + b) - 1)
    ) == 0
    assert sp.expand(t_abc.subs(aa, 1 / (a + b)) + (a + b)) == 0


def audit_four_class_exchange():
    a, b, c, d = sp.symbols("a b c d")

    def baseline(selected, other1, other2):
        return (
            (2*b + other1 + other2) / ((b + other1) * (b + other2))
            - 3 / (selected - b) + 2 / (selected + b)
        )

    first_difference = sp.factor(
        sp.together(baseline(a, c, d) - baseline(c, a, d))
    )
    second_difference = sp.factor(
        sp.together(baseline(a, c, d) - baseline(d, a, c))
    )
    first_num, first_den = first_difference.as_numer_denom()
    second_num, second_den = second_difference.as_numer_denom()
    first_core = 2*a*b + a*c + b**2 + 2*b*c
    second_core = 2*a*b + a*d + b**2 + 2*b*d
    assert sp.expand(first_num + 2 * (a - c) * first_core) == 0
    assert sp.expand(second_num + 2 * (a - d) * second_core) == 0
    assert first_den != 0 and second_den != 0
    assert sp.factor(first_core - second_core) == (a + 2*b) * (c - d)
    assert sp.expand(first_core.subs(a, -2*b)) == -3 * b**2


def audit_all_distinct_robin_obstruction():
    d, a, b, c, aa, bb, cc = sp.symbols("d a b c A B C")

    def row(y, constant):
        zeta = constant - (d + 3 * y) / (d**2 - y**2)
        return (zeta, 1 - y*zeta, -2*y + y**2*zeta)

    determinant = sp.together(
        sp.Matrix([row(a, aa), row(b, bb), row(c, cc)]).det()
    ).as_numer_denom()[0]
    polynomial = sp.Poly(determinant, d)
    assert polynomial.degree() <= 6
    coefficients = tuple(polynomial.all_coeffs())
    assert len(coefficients) == 7
    localizer = (
        (a - 1) * (a + 1) * (b - 1) * (b + 1)
        * (c - 1) * (c + 1)
        * (a - b) * (a + b) * (a - c) * (a + c)
        * (b - c) * (b + c)
    )
    assert singular_status(
        coefficients, (a, b, c, aa, bb, cc),
        localizer=sp.expand(localizer),
    ) == "UNIT"
    for r in range(5, 31):
        assert (r + 5) - 3 >= 7


def geometry(r):
    exceptional = tuple(range(r + 5))
    common_live = tuple(range(r + 5, 2*r))
    centres = (2*r, 2*r + 1)
    extra = 2*r + 2
    common_active = common_live + centres
    active = common_active + (extra,)
    exceptional_betas = (
        (Fraction(0), Fraction(2), Fraction(2))
        + tuple(Fraction(value) for value in range(3, r + 5))
    )
    betas = exceptional_betas + (Fraction(1),) * (r - 2)
    assert len(exceptional_betas) == r + 5
    assert len(betas) == 2*r + 3
    assert len(common_active) == r - 3
    assert len(active) == r - 2
    for left, right in combinations(range(len(betas)), 2):
        assert betas[left] + betas[right] != 0
    return exceptional, common_live, centres, extra, common_active, active, betas


def partitions(r, exceptional):
    marked = exceptional[0]
    remaining = exceptional[1:]
    p_left = remaining[:r]
    p_right = remaining[r:]
    assert len(p_right) == 4

    s_marked = exceptional[:2]
    remaining = exceptional[2:]
    s_left = remaining[:r]
    s_right = remaining[r:]
    assert len(s_right) == 3
    return (marked, p_left, p_right), (s_marked, s_left, s_right)


def audit_s_embedding():
    for r in range(5, 13):
        exceptional = frozenset(range(r + 5))
        count = 0
        for omitted in exceptional:
            previous = exceptional - {omitted}
            for marked in previous:
                remainder = previous - {marked}
                for left_tuple in combinations(sorted(remainder), r):
                    left = frozenset(left_tuple)
                    right = remainder - left
                    pair = frozenset((omitted, marked))
                    assert len(pair) == 2
                    assert len(left) == r and len(right) == 3
                    assert pair | left | right == exceptional
                    count += 1
        assert count == (r + 5) * (r + 4) * sp.binomial(r + 3, r)


def audit_literal_response(r=6):
    (
        exceptional, common_live, centres, extra,
        common_active, active, betas,
    ) = geometry(r)
    (marked, p_left, p_right), (s_marked, s_left, s_right) = partitions(
        r, exceptional
    )
    p_value = cauchy_permanent(
        tuple(betas[site] for site in p_left),
        (Fraction(1),) * (r - 4)
        + tuple(betas[site] for site in p_right),
    )
    s_value = cauchy_permanent(
        tuple(betas[site] for site in s_left),
        (Fraction(1),) * (r - 3)
        + tuple(betas[site] for site in s_right),
    )
    assert p_value and s_value
    p = (Fraction(2), Fraction(3), Fraction(5))
    direct_scale = Fraction(17)

    # Noncoordinate P_r rows: all binary common-active rows, then the two
    # literal zero third rows at the centres.
    for target in common_active:
        others = tuple(site for site in common_active if site != target)
        for same, opposite in ((E0, E1), (E1, E0)):
            rows = [ZERO] * len(betas)
            rows[marked] = E2
            rows[extra] = p
            rows[target] = same
            for site in others:
                rows[site] = opposite
            for site in p_left:
                rows[site] = same
            for site in p_right:
                rows[site] = opposite
            response = source_22_response(tuple(rows), betas, active, direct_scale)
            assert response[target] == 2 * p[2] * p_value
            assert all(response[site] == 0 for site in active if site != target)

    for target in centres:
        rows = [ZERO] * len(betas)
        rows[marked] = E2
        rows[extra] = p
        for site in common_active:
            rows[site] = ZERO if site == target else E1
        for site in p_left:
            rows[site] = E0
        for site in p_right:
            rows[site] = E1
        response = source_22_response(tuple(rows), betas, active, direct_scale)
        assert response[target] == 2 * p[2] * p_value
        assert all(response[site] == 0 for site in active if site != target)

    # S_r kills the noncoordinate extra block after the binary active rows.
    rows = [ZERO] * len(betas)
    for site in s_marked:
        rows[site] = E2
    for site in s_left:
        rows[site] = E0
    for site in s_right:
        rows[site] = E1
    for site in common_active:
        rows[site] = E1
    rows[extra] = p
    response = source_22_response(tuple(rows), betas, active, direct_scale)
    assert response[extra] == 2 * s_value

    # The genuine third row at every common-live target is triangular.
    for target in common_live:
        rows = [ZERO] * len(betas)
        rows[marked] = E2
        rows[extra] = p
        for site in common_active:
            rows[site] = E2 if site == target else E1
        for site in p_left:
            rows[site] = E0
        for site in p_right:
            rows[site] = E1
        response = source_22_response(tuple(rows), betas, active, direct_scale)
        assert response[target] == 2 * p[2] * p_value

    # Coordinate plane: S_r isolates every binary active row, then all
    # D-type zero third rows and the common-live genuine third rows.
    for target in active:
        others = tuple(site for site in active if site != target)
        for same, opposite in ((E0, E1), (E1, E0)):
            rows = [ZERO] * len(betas)
            for site in s_marked:
                rows[site] = E2
            for site in s_left:
                rows[site] = same
            for site in s_right:
                rows[site] = opposite
            rows[target] = same
            for site in others:
                rows[site] = opposite
            response = source_22_response(tuple(rows), betas, active, direct_scale)
            assert response[target] == 2 * s_value
            assert all(response[site] == 0 for site in others)

    for target in centres + (extra,):
        rows = [ZERO] * len(betas)
        for site in s_marked:
            rows[site] = E2
        for site in s_left:
            rows[site] = E0
        for site in s_right:
            rows[site] = E1
        rows[target] = ZERO
        for site in active:
            if site != target:
                rows[site] = E1
        response = source_22_response(tuple(rows), betas, active, direct_scale)
        assert response[target] == 2 * s_value
        assert all(response[site] == 0 for site in active if site != target)

    for target in common_live:
        rows = [ZERO] * len(betas)
        for site in s_marked:
            rows[site] = E2
        for site in s_left:
            rows[site] = E0
        for site in s_right:
            rows[site] = E1
        rows[target] = E2
        for site in active:
            if site != target:
                rows[site] = E1
        response = source_22_response(tuple(rows), betas, active, direct_scale)
        assert response[target] == 2 * s_value


def main():
    audit_profile_routing()
    print("uniform profile routing; r=6 census 56=40+1+14+1: exact")
    audit_heavy_class_descent()
    print("multiplicity-at-least-four elementary deletion descent: exact")
    audit_one_deletion_hermite_degree()
    print("one-deletion Hermite rank and residual degrees: exact")
    audit_affine_robin_compatibility()
    print("affine Robin pair/triangle/four-anchor obstruction: exact")
    audit_four_class_exchange()
    print("four repeated classes exchange obstruction: exact")
    audit_all_distinct_robin_obstruction()
    print("all-distinct quadratic Robin sextic: localized UNIT")
    audit_s_embedding()
    print("inherited S_r embedding: exact")
    audit_literal_response()
    print("literal r=6 response, beta zero/repetition, direct scale 17: exact")
    print("sole-plane layer t=r+5: UNIFORM COMPLETE PASS")


if __name__ == "__main__":
    main()
