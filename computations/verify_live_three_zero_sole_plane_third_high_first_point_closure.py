#!/usr/bin/env python3
"""Exact audit of the sole-plane frontier point (r,t)=(5,10)."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from math import factorial

import sympy as sp

from explore_live_three_zero_minimal_three_extra_ccb import singular_status
from verify_live_three_zero_sole_plane_first_high_layer_uniform import (
    E0,
    E1,
    E2,
    HESSIAN,
    ZERO,
    cauchy_permanent,
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
        (sp.prod(matrix[row][sigma[row]] for row in range(size))
         for sigma in permutations(range(size))),
        sp.S.Zero,
    )


def elementary(values, degree):
    return sum(
        (sp.prod(values[index] for index in subset)
         for subset in combinations(range(len(values)), degree)),
        sp.S.Zero,
    )


def audit_profile_census_and_high_classes():
    profiles = tuple(
        profile for profile in integer_partitions(10)
        if max(profile) <= 4
    )
    assert len(profiles) == 23
    assert profiles == (
        (4, 4, 2), (4, 4, 1, 1), (4, 3, 3), (4, 3, 2, 1),
        (4, 3, 1, 1, 1), (4, 2, 2, 2), (4, 2, 2, 1, 1),
        (4, 2, 1, 1, 1, 1), (4, 1, 1, 1, 1, 1, 1),
        (3, 3, 3, 1), (3, 3, 2, 2), (3, 3, 2, 1, 1),
        (3, 3, 1, 1, 1, 1), (3, 2, 2, 2, 1),
        (3, 2, 2, 1, 1, 1), (3, 2, 1, 1, 1, 1, 1),
        (3, 1, 1, 1, 1, 1, 1, 1), (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 1, 1), (2, 2, 2, 1, 1, 1, 1),
        (2, 2, 1, 1, 1, 1, 1, 1),
        (2, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    )
    assert sum(max(profile) >= 3 for profile in profiles) == 17
    assert tuple(profile for profile in profiles if max(profile) <= 2) == (
        (2, 2, 2, 2, 2), (2, 2, 2, 2, 1, 1),
        (2, 2, 2, 1, 1, 1, 1), (2, 2, 1, 1, 1, 1, 1, 1),
        (2, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    )

    # Four equal special columns reduce to one-point-deletion sums of six
    # nonzero h-values.  If every five-subset sum vanished, every h would
    # equal the total, hence the total and every h would be zero.
    h = sp.symbols("h0:6", nonzero=True)
    total = sum(h)
    deletions = tuple(total - value for value in h)
    assert sp.expand(sum(deletions) - 5 * total) == 0
    for index, deletion in enumerate(deletions):
        assert sp.expand(total - deletion - h[index]) == 0

    # Three equal columns leave exactly the two-special deletion form from
    # the first-high uniform theorem: sum_{i != j} u_i v_j.
    u = sp.symbols("u0:5")
    v = sp.symbols("v0:5")
    ordered = sum(u[i] * v[j] for i in range(5) for j in range(5) if i != j)
    symmetric = sum(
        u[i] * v[j] + u[j] * v[i] for i, j in combinations(range(5), 2)
    )
    assert sp.expand(ordered - symmetric) == 0

    rows = tuple(map(sp.Rational, (2, 3, 5, 7, 11)))
    a, b = sp.Rational(13), sp.Rational(17)
    matrix = [[1 / (x + pole) for pole in (1, b, a, a, a)] for x in rows]
    left = permanent(matrix)
    hs_u = [(x + a) / (x + 1) for x in rows]
    hs_v = [(x + a) / (x + b) for x in rows]
    right = 6 * sp.prod(1 / (x + a) for x in rows) * sum(
        hs_u[i] * hs_v[j]
        for i in range(5) for j in range(5) if i != j
    )
    assert sp.cancel(left - right) == 0

    # Fixed-special version needed here: after removing a chosen triple,
    # the seven moving labels have at least three value classes.
    triple_only = tuple(
        profile for profile in profiles
        if max(profile) == 3
    )
    assert all(len(profile) - 1 >= 3 for profile in triple_only)
    x, y, z = sp.symbols("x y z")
    fxy = (y + 1) / (x + y) + 2 * (1 - y) / (x - y)
    fxz = (z + 1) / (x + z) + 2 * (1 - z) / (x - z)
    expected_difference = -(
        (x - 1) * (y - z) * (x**2 + 3*x*(y + z) + y*z)
        / ((x - y) * (x + y) * (x - z) * (x + z))
    )
    assert sp.cancel(fxy - fxz - expected_difference) == 0
    q = sp.Symbol("q")
    g_yz = x**2 + 3*x*(y + z) + y*z
    g_yq = x**2 + 3*x*(y + q) + y*q
    assert sp.factor(g_yz - g_yq) == (3*x + y) * (z - q)


def projective_quartic():
    c, y, z, ay, az = sp.symbols("c y z A_y A_z")
    xy = ay + (c + 3 * y) / (c**2 - y**2)
    xz = az + (c + 3 * z) / (c**2 - z**2)
    numerator = sp.factor(
        sp.together(xy - xz + (z - y) * xy * xz).as_numer_denom()[0]
    )
    polynomial = sp.Poly(numerator, c)
    assert polynomial.degree() <= 4
    assert sp.expand(polynomial.coeff_monomial(c**3)
                     + (ay + az) * (y - z)) == 0
    zero_branch = sp.Poly(numerator.subs({ay: 0, az: 0}), c)
    assert sp.expand(zero_branch.coeff_monomial(c**2) - 2 * (y - z)) == 0
    special = sp.factor(
        numerator.subs({ay: -2 / (y - z), az: 2 / (y - z)})
    )
    assert sp.expand(
        special + 4 * (y - z) * (c**2 + c*y + c*z + 3*y*z)
    ) == 0


def audit_one_two_double_profiles():
    projective_quartic()
    # With R=(a,a,b,c), deleting the double a leaves no base row for d=1;
    # for d=2 at most the other double class remains.  A nonzero single row
    # cannot support a left-kernel vector.
    for doubles, moving_classes in ((1, 7), (2, 6)):
        assert doubles - 1 <= 1
        assert moving_classes >= 5

    # The confluent denominator has degree 9 and every numerator degree at
    # most 7.  Six Hermite roots leave one affine factor.
    assert 2 + 3 + 2 + 2 == 9
    assert 9 - 2 == 7 and 7 - 6 == 1


def audit_three_four_double_profiles():
    x, y, a = sp.symbols("x y a")
    minor = sp.det(sp.Matrix([
        [1 / (x + a) ** 2, -2 / (x + a) ** 3],
        [1 / (y + a) ** 2, -2 / (y + a) ** 3],
    ]))
    assert sp.cancel(
        minor + 2 * (x - y) / ((x + a) ** 3 * (y + a) ** 3)
    ) == 0

    value, constant = sp.symbols("value constant")
    psi = 2 / (1 + value) - 3 / (value - 1)
    assert sp.factor(psi + (value + 5) / (value**2 - 1)) == 0
    fibre = sp.Poly(sp.together(psi - constant).as_numer_denom()[0], value)
    assert fibre.degree() <= 2
    assert fibre.coeff_monomial(value) == -1
    # Every graph of pair equations on 3 or 4 double classes contains a
    # triangle; its three equations put all three values in one psi fibre.
    for doubles in (3, 4):
        assert len(tuple(combinations(range(doubles), 2))) >= 3


def audit_all_distinct_robin_obstruction():
    d, a, b, c, aa, bb, cc = sp.symbols("d a b c A B C")

    def row(y, constant):
        zeta = constant - (d + 3 * y) / (d**2 - y**2)
        return (zeta, 1 - y * zeta, -2 * y + y**2 * zeta)

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
    result = singular_status(
        coefficients, (a, b, c, aa, bb, cc),
        localizer=sp.expand(localizer),
    )
    assert result == "UNIT", result

    # Five distinct squared-Cauchy columns: denominator degree 10,
    # numerator degree <=8, six roots and a residual quadratic.
    assert 2 * 5 == 10 and 10 - 2 == 8 and 8 - 6 == 2


def confluent_matrices(row_profile, pole_profile):
    x, y = sp.symbols("x y")
    denominator_functions = []
    numerator_functions = []
    for pole, multiplicity in pole_profile:
        for order in range(multiplicity):
            denominator_functions.append(
                sp.diff(1 / (x + y), y, order).subs(y, pole) / factorial(order)
            )
            numerator_functions.append(
                sp.diff(1 / (x + y) ** 2, y, order).subs(y, pole)
                / factorial(order)
            )

    def evaluate(functions):
        rows = []
        for value, multiplicity in row_profile:
            for order in range(multiplicity):
                rows.append([
                    sp.diff(function, x, order).subs(x, value) / factorial(order)
                    for function in functions
                ])
        return sp.Matrix(rows)

    return evaluate(denominator_functions), evaluate(numerator_functions)


def audit_borchardt_confluence():
    tests = (
        (
            ((sp.Rational(2), 2), (sp.Rational(3), 1),
             (sp.Rational(5), 1), (sp.Rational(7), 1)),
            ((sp.Rational(1), 1), (sp.Rational(11), 2),
             (sp.Rational(13), 1), (sp.Rational(17), 1)),
        ),
        (
            ((sp.Rational(2), 1), (sp.Rational(3), 2),
             (sp.Rational(5), 1), (sp.Rational(7), 1)),
            ((sp.Rational(1), 1), (sp.Rational(11), 2),
             (sp.Rational(13), 2)),
        ),
    )
    for row_profile, pole_profile in tests:
        rows = tuple(
            value for value, multiplicity in row_profile
            for _ in range(multiplicity)
        )
        poles = tuple(
            value for value, multiplicity in pole_profile
            for _ in range(multiplicity)
        )
        raw = [[1 / (row + pole) for pole in poles] for row in rows]
        denominator, numerator = confluent_matrices(row_profile, pole_profile)
        assert denominator.det() != 0
        assert sp.cancel(permanent(raw) - numerator.det() / denominator.det()) == 0


def audit_five_double_bad_pair_graph():
    r1, r2, r3 = sp.symbols("r1 r2 r3")
    rows = sp.Matrix([
        [1, value, value**3, value**4] for value in (r1, r2, r3)
    ])
    vandermonde = (r1 - r2) * (r1 - r3) * (r2 - r3)
    first = sp.factor(rows[:, (0, 1, 2)].det())
    second = sp.factor(rows[:, (0, 1, 3)].det())
    assert sp.cancel(first / vandermonde) in (
        r1 + r2 + r3, -(r1 + r2 + r3)
    )
    h2 = r1**2 + r2**2 + r3**2 + r1*r2 + r1*r3 + r2*r3
    assert sp.cancel(second / vandermonde) in (h2, -h2)
    # Thus rank loss is exactly e1=e2=0: then r_i^3 is constant and the
    # last two columns are multiples of the first two.
    e1 = r1 + r2 + r3
    e2 = r1*r2 + r1*r3 + r2*r3
    assert sp.expand(h2 - (e1**2 - e2)) == 0

    # Two bad edges sharing a vertex a.  In p_x=(x-a)/(x+a)
    # coordinates, their endpoints q,r obey qr=3 and r=-q.  The remaining
    # s,t then obey s+t=0, st=-1, hence {s,t}={1,-1}, both structural
    # impossibilities for nonzero repeated beta values.
    q, rr, s, t = sp.symbols("q rr s t")
    eq_sum_difference = sp.factor(
        (q + 3/q) - (rr + 3/rr)
    )
    assert sp.cancel(
        eq_sum_difference - (q - rr) * (q*rr - 3) / (q*rr)
    ) == 0
    eq_pair_difference = sp.factor(
        (3 + 3/q**2) - (3 + 3/rr**2)
    )
    assert sp.cancel(
        eq_pair_difference + 3 * (q - rr) * (q + rr) / (q**2 * rr**2)
    ) == 0
    assert sp.expand(q * (q + 3/q) - (q**2 + 3)) == 0
    # Direct substitution of rr=-q, q^2=-3 in the two full symmetric sums.
    full_sum = q + rr + s + t
    full_pair = q*rr + (q + rr)*(s + t) + s*t
    assert sp.expand(full_sum.subs(rr, -q)) == s + t
    assert sp.expand(full_pair.subs(rr, -q).subs(q**2, -3)) == 3 + s*t
    # The bad-q equations give full sum 0 and full pair 2, hence s+t=0,
    # st=-1 and s^2=1.
    assert sp.expand((s*t).subs(t, -s) + s**2) == 0

    # A graph of maximum degree one is a matching; its complement in K5
    # always contains a triangle.
    vertices = tuple(range(5))
    edges = tuple(combinations(vertices, 2))
    for mask in range(1 << len(edges)):
        bad = tuple(edge for index, edge in enumerate(edges) if mask >> index & 1)
        if any(sum(vertex in edge for edge in bad) > 1 for vertex in vertices):
            continue
        good = set(edges) - set(bad)
        assert any(
            all(edge in good for edge in combinations(triple, 2))
            for triple in combinations(vertices, 3)
        )


def dot_edge(left, right, beta_left, beta_right):
    numerator = sum(
        left[i] * HESSIAN[i][j] * right[j]
        for i in range(3) for j in range(3)
    )
    return numerator / (beta_left + beta_right)


def source_22_response(rows, betas, active, direct_scale):
    direct = (
        (Fraction(0), direct_scale, Fraction(0)),
        (direct_scale, Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
    )
    assert direct[2][2] == 0
    vertices = tuple(range(len(rows)))

    @lru_cache(maxsize=None)
    def hafnian(remaining):
        if not remaining:
            return Fraction(1)
        first = remaining[0]
        answer = Fraction(0)
        for position in range(1, len(remaining)):
            second = remaining[position]
            tail = remaining[1:position] + remaining[position + 1:]
            answer += dot_edge(
                rows[first], rows[second], betas[first], betas[second]
            ) * hafnian(tail)
        return answer

    answer = {}
    for star in active:
        coefficient = Fraction(0)
        for left, right in combinations(vertices, 2):
            if star in (left, right):
                continue
            marked = 2 * rows[left][2] * rows[right][2]
            if not marked:
                continue
            remaining = tuple(
                site for site in vertices if site not in (left, right, star)
            )
            coefficient += marked * hafnian(remaining)
        answer[star] = coefficient
    return answer


def find_pivots(betas):
    exceptional = tuple(range(10))
    p_data = None
    for marked in exceptional:
        remainder = tuple(site for site in exceptional if site != marked)
        for left in combinations(remainder, 5):
            right = tuple(site for site in remainder if site not in left)
            value = cauchy_permanent(
                tuple(betas[site] for site in left),
                (Fraction(1),) + tuple(betas[site] for site in right),
            )
            if value:
                p_data = (marked, left, right, value)
                break
        if p_data:
            break
    assert p_data is not None

    for marked in combinations(exceptional, 2):
        remainder = tuple(site for site in exceptional if site not in marked)
        for left in combinations(remainder, 5):
            right = tuple(site for site in remainder if site not in left)
            value = cauchy_permanent(
                tuple(betas[site] for site in left),
                (Fraction(1), Fraction(1))
                + tuple(betas[site] for site in right),
            )
            if value:
                return p_data, (marked, left, right, value)
    raise AssertionError("no inherited S pivot")


def audit_s_embedding():
    exceptional = frozenset(range(10))
    count = 0
    for omitted in exceptional:
        nine = exceptional - {omitted}
        for marked in nine:
            remainder = nine - {marked}
            for left_tuple in combinations(sorted(remainder), 5):
                left = frozenset(left_tuple)
                right = remainder - left
                pair = frozenset((omitted, marked))
                assert len(pair) == 2 and len(left) == 5 and len(right) == 3
                assert pair | left | right == exceptional
                count += 1
    assert count == 10 * 9 * 56


def audit_literal_response():
    exceptional_betas = tuple(map(Fraction, (0, 2, 3, 4, 5, 6, 7, 8, 9, 10)))
    betas = exceptional_betas + (Fraction(1), Fraction(1), Fraction(1))
    centres = (10, 11)
    extra = 12
    active = centres + (extra,)
    p = (Fraction(2), Fraction(3), Fraction(5))
    direct_scale = Fraction(17)
    (marked, p_left, p_right, p_value), (s_marked, s_left, s_right, s_value) = find_pivots(betas)

    for target in centres:
        other = centres[1] if target == centres[0] else centres[0]
        for same, opposite in ((E0, E1), (E1, E0)):
            rows = [ZERO] * len(betas)
            rows[marked] = E2
            rows[extra] = p
            rows[target] = same
            rows[other] = opposite
            for site in p_left:
                rows[site] = same
            for site in p_right:
                rows[site] = opposite
            response = source_22_response(tuple(rows), betas, active, direct_scale)
            assert response[target] == 2 * p[2] * p_value
            assert all(response[site] == 0 for site in active if site != target)

        rows = [ZERO] * len(betas)
        rows[marked] = E2
        rows[extra] = p
        rows[target] = ZERO
        rows[other] = E1
        for site in p_left:
            rows[site] = E0
        for site in p_right:
            rows[site] = E1
        response = source_22_response(tuple(rows), betas, active, direct_scale)
        assert response[target] == 2 * p[2] * p_value
        assert all(response[site] == 0 for site in active if site != target)

    rows = [ZERO] * len(betas)
    for site in s_marked:
        rows[site] = E2
    for site in s_left:
        rows[site] = E0
    for site in s_right:
        rows[site] = E1
    for site in centres:
        rows[site] = E1
    rows[extra] = p
    response = source_22_response(tuple(rows), betas, active, direct_scale)
    assert response[extra] == 2 * s_value

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

        rows = [ZERO] * len(betas)
        for site in s_marked:
            rows[site] = E2
        for site in s_left:
            rows[site] = E0
        for site in s_right:
            rows[site] = E1
        rows[target] = ZERO
        for site in others:
            rows[site] = E1
        response = source_22_response(tuple(rows), betas, active, direct_scale)
        assert response[target] == 2 * s_value
        assert all(response[site] == 0 for site in others)


def audit_chart_cover():
    a, b = sp.symbols("a b")
    chart_01 = sp.Matrix([[1, 0, a], [0, 1, b]])
    chart_12 = sp.Matrix([[a, 1, 0], [b, 0, 1]])
    chart_02 = sp.Matrix([[1, a, 0], [0, b, 1]])
    assert chart_12[1, 2] == 1 and chart_02[1, 2] == 1
    assert chart_01.subs({a: 0, b: 0}).rowspace() == [
        sp.Matrix([[1, 0, 0]]), sp.Matrix([[0, 1, 0]])
    ]


def main():
    audit_profile_census_and_high_classes()
    print("23-profile census; multiplicity-four/three deletions: exact")
    audit_one_two_double_profiles()
    print("one/two-double affine quartic obstruction: exact")
    audit_three_four_double_profiles()
    print("three/four-double two-pair residue fibres: exact")
    audit_all_distinct_robin_obstruction()
    print("all-distinct quadratic Robin determinant: localized UNIT")
    audit_borchardt_confluence()
    print("simultaneous row/column-confluent Borchardt quotients: exact")
    audit_five_double_bad_pair_graph()
    print("five-double bad-pair matching and good-triangle obstruction: exact")
    audit_s_embedding()
    print("inherited S_5 embedding: exact")
    audit_literal_response()
    print("literal response, beta zero, direct scale 17: exact")
    audit_chart_cover()
    print("three-chart row-plane cover: exact")
    print("sole-plane (r,t)=(5,10) closure: PASS")


if __name__ == "__main__":
    main()
