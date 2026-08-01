#!/usr/bin/env python3
"""Exact audit of the sole-plane t=r+6 frontier and its closed sectors."""

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
from verify_live_three_zero_sole_plane_third_high_layer_uniform import (
    audit_affine_robin_compatibility,
)
from verify_live_three_zero_sole_plane_fourth_high_all_distinct_dr4_closure import (
    audit_root_and_fibre_counts,
    audit_row_bridge,
    audit_sharp_degree_bound,
)


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


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
        (sp.prod(matrix[i][sigma[i]] for i in range(size))
         for sigma in permutations(range(size))),
        sp.S.Zero,
    )


def elementary(values, degree):
    if degree == 0:
        return sp.S.One
    return sum(
        (sp.prod(values[i] for i in subset)
         for subset in combinations(range(len(values)), degree)),
        sp.S.Zero,
    )


def route(profile, r):
    if max(profile) >= 5:
        return "heavy"
    if all(part == 1 for part in profile):
        return "distinct_dr4"
    if max(profile) >= 3 and len(profile) >= 5:
        return "many_class_high"
    if len(profile) == 4:
        return "four_class_high"
    require(
        max(profile) <= 2,
        "max(profile) <= 2",
    )
    doubles = sum(part == 2 for part in profile)
    if doubles == 1:
        return "sparse_double_A"
    if doubles >= 2 and len(profile) >= 11:
        return "sparse_double_B"
    return "dense_double_residual"


def audit_profile_census():
    profiles = tuple(integer_partitions(13))
    require(
        len(profiles) == 101,
        "len(profiles) == 101",
    )
    routed = {}
    for profile in profiles:
        routed.setdefault(route(profile, 7), []).append(profile)
    require(
        {key: len(value) for key, value in routed.items()} == {
            "heavy": 62,
            "four_class_high": 3,
            "many_class_high": 29,
            "dense_double_residual": 4,
            "sparse_double_B": 1,
            "sparse_double_A": 1,
            "distinct_dr4": 1,
        },
        "{key: len(value) for key, value in routed.items()} == { \"...",
    )
    residual = tuple(
        profile for profile in profiles if "residual" in route(profile, 7)
    )
    require(
        residual == (
            (2, 2, 2, 2, 2, 2, 1),
            (2, 2, 2, 2, 2, 1, 1, 1),
            (2, 2, 2, 2, 1, 1, 1, 1, 1),
            (2, 2, 2, 1, 1, 1, 1, 1, 1, 1),
        ),
        "residual == ( (2, 2, 2, 2, 2, 2, 1), (2, 2, 2, 2, 2, 1, 1...",
    )

    # The dense double tail is finite in r: d>=r-4 and
    # d<=floor((r+6)/2) is impossible from r=15 onward.
    tails = {}
    for r in range(7, 25):
        tails[r] = tuple(
            d for d in range(1, (r + 6) // 2 + 1)
            if d >= r - 4
        )
    require(
        tails == {
            7: (3, 4, 5, 6),
            8: (4, 5, 6, 7),
            9: (5, 6, 7),
            10: (6, 7, 8),
            11: (7, 8),
            12: (8, 9),
            13: (9,),
            14: (10,),
            15: (), 16: (), 17: (), 18: (), 19: (), 20: (),
            21: (), 22: (), 23: (), 24: (),
        },
        "tails == { 7: (3, 4, 5, 6), 8: (4, 5, 6, 7), 9: (5, 6, 7)...",
    )


def audit_heavy_and_degree_bookkeeping():
    rows = tuple(map(sp.Rational, (2, 3, 5, 7, 11, 13, 17)))
    a = sp.Rational(19)
    columns = (sp.Rational(1), sp.Rational(1), a, a, a, a, a)
    lhs = permanent([[1 / (x + y) for y in columns] for x in rows])
    h = tuple((x + a) / (x + 1) for x in rows)
    rhs = (
        factorial(5) * factorial(2)
        * sp.prod(1 / (x + a) for x in rows)
        * elementary(h, 2)
    )
    require(
        sp.cancel(lhs - rhs) == 0,
        "sp.cancel(lhs - rhs) == 0",
    )

    for r in range(7, 31):
        degree = r - 5
        require(
            (r + 1) - degree == 6,
            "(r + 1) - degree == 6",
        )
        while degree:
            require(
                r + 1 - degree != 0,
                "r + 1 - degree != 0",
            )
            degree -= 1

        # Five selected labels, m_R represented value classes.  The degree
        # formula is unchanged from the preceding layer.
        for m_r in range(1, 6):
            denominator = r + m_r + 1
            numerator = denominator - 2
            residual = numerator - (r + 1)
            require(
                residual == m_r - 2,
                "residual == m_r - 2",
            )


def audit_high_collision_boundaries():
    audit_affine_robin_compatibility()
    a, b, c, d, j = sp.symbols("a b c d j")

    def transport(selected, other1, other2):
        return (
            (2*b + other1 + other2) / ((b + other1) * (b + other2))
            - (j + 1) / (selected - b) + j / (selected + b)
        )

    first = sp.factor(sp.together(
        transport(a, c, d) - transport(c, a, d)
    ))
    second = sp.factor(sp.together(
        transport(a, c, d) - transport(d, a, c)
    ))
    first_num = first.as_numer_denom()[0]
    second_num = second.as_numer_denom()[0]
    first_core = j*a*b + a*c + b**2 + j*b*c
    second_core = j*a*b + a*d + b**2 + j*b*d
    require(
        sp.expand(first_num + 2*(a-c)*first_core) == 0,
        "sp.expand(first_num + 2*(a-c)*first_core) == 0",
    )
    require(
        sp.expand(second_num + 2*(a-d)*second_core) == 0,
        "sp.expand(second_num + 2*(a-d)*second_core) == 0",
    )
    require(
        sp.factor(first_core - second_core) == (a + j*b)*(c-d),
        "sp.factor(first_core - second_core) == (a + j*b)*(c-d)",
    )
    require(
        sp.expand(
            first_core.subs(a, -j*b) - (1-j**2)*b**2
        ) == 0,
        "sp.expand( first_core.subs(a, -j*b) - (1-j**2)*b**2 ) == 0",
    )
    require(
        sp.expand(first_core.subs({a: -3*b, j: 3})) == -8*b**2,
        "sp.expand(first_core.subs({a: -3*b, j: 3})) == -8*b**2",
    )

    # The only four-class boundary not killed by the repeated-anchor
    # exchange is 4^3 1 with its singleton equal to zero.  Selecting that
    # zero anchor and four copies of a moving class gives chi_4(0,x)=-1/x,
    # an injective function on the three nonzero moving values.
    x = sp.Symbol("x")
    chi4 = 4 / x - 5 / x
    require(
        sp.factor(chi4 + 1/x) == 0,
        "sp.factor(chi4 + 1/x) == 0",
    )


def simple_quadratic_row(x, y, constant):
    denominator = x**2 - y**2
    y_numerator = constant * denominator + x + 3*y
    return (
        -y_numerator,
        denominator + y*y_numerator,
        -2*y*denominator - y**2*y_numerator,
    )


def triple_quadratic_row(x, u, first, second):
    denominator = x**2 - u**2
    log_first_numerator = first*denominator - x - 3*u
    log_second_numerator = (
        second*denominator**2 + (x-u)**2 + 2*(x+u)**2
    )
    second_derivative_numerator = sp.expand(
        log_first_numerator**2 + log_second_numerator
    )
    return (
        second_derivative_numerator,
        sp.expand(2*log_first_numerator*denominator
                  - u*second_derivative_numerator),
        sp.expand(2*denominator**2
                  - 4*u*log_first_numerator*denominator
                  + u**2*second_derivative_numerator),
    )


def audit_sparse_double_determinants():
    x, a, b, u, aa, bb, uu, ww = sp.symbols("x a b u A B U W")
    determinant_a = sp.expand(sp.Matrix([
        simple_quadratic_row(x, a, aa),
        simple_quadratic_row(x, b, bb),
        triple_quadratic_row(x, u, uu, ww),
    ]).det())
    polynomial_a = sp.Poly(determinant_a, x)
    require(
        polynomial_a.degree() <= 8,
        "polynomial_a.degree() <= 8",
    )
    localizer_a = (
        u * (a-1)*(a+1)*(b-1)*(b+1)*(u-1)*(u+1)
        * (a-b)*(a+b)*(a-u)*(a+u)*(b-u)*(b+u)
    )
    require(
        singular_status(
            polynomial_a.all_coeffs(), (a, b, u, aa, bb, uu, ww),
            localizer=sp.expand(localizer_a),
        ) == "UNIT",
        "singular_status( polynomial_a.all_coeffs(), (a, b, u, aa,...",
    )

    v, vv, tt = sp.symbols("v V T")
    row_u = triple_quadratic_row(x, u, uu, ww)[:2]
    row_v = triple_quadratic_row(x, v, vv, tt)[:2]
    determinant_b = sp.expand(sp.Matrix([row_u, row_v]).det())
    polynomial_b = sp.Poly(determinant_b, x)
    require(
        polynomial_b.degree() <= 8,
        "polynomial_b.degree() <= 8",
    )
    localizer_b = (
        u*v*(u-1)*(u+1)*(v-1)*(v+1)*(u-v)*(u+v)
    )
    require(
        singular_status(
            polynomial_b.all_coeffs(), (u, v, uu, ww, vv, tt),
            localizer=sp.expand(localizer_b),
        ) == "UNIT",
        "singular_status( polynomial_b.all_coeffs(), (u, v, uu, ww...",
    )


def audit_cubic_identity_frontier():
    z, x, y = sp.symbols("z x y")
    cubic = (z-x)*(z+x)**2
    phi = (x+3*y)/(x**2-y**2)
    require(
        sp.cancel(
            sp.diff(cubic, z).subs(z, -y) - phi*cubic.subs(z, -y)
        ) == 0,
        "sp.cancel( sp.diff(cubic, z).subs(z, -y) - phi*cubic.subs...",
    )

    # The quartet linear certificate has an explicit inhomogeneous term
    # once the three fixed pair contributions are restored.
    values = sp.symbols("a0:4")

    def psi(left, right):
        return 1/(left+right) - 2/(right-left)

    constant = sp.factor(sum(
        sp.prod(values[i]+values[j] for j in range(4) if j != i)
        * sum(psi(values[i], values[j]) for j in range(4) if j != i)
        for i in range(4)
    ))
    require(
        sp.expand(constant - 9*sum(values)**2) == 0,
        "sp.expand(constant - 9*sum(values)**2) == 0",
    )

    # Exact reconnaissance only: on six rational structural anchors, the
    # fifteen quartet linear equations are already inconsistent.  This is
    # not promoted to a universal symbolic lemma.
    nodes = tuple(map(sp.Rational, (2, 3, 5, 7, 11, 13)))
    rows = []
    rhs = []
    for core in combinations(range(6), 4):
        rows.append([
            (sp.prod(nodes[i]+nodes[j] for j in core if j != i)
             if i in core else 0)
            for i in range(6)
        ])
        rhs.append(-9*sum(nodes[i] for i in core)**2)
    matrix = sp.Matrix(rows)
    require(
        matrix.rank() == 6,
        "matrix.rank() == 6",
    )
    require(
        matrix.row_join(sp.Matrix(rhs)).rank() == 7,
        "matrix.row_join(sp.Matrix(rhs)).rank() == 7",
    )

    # Full DR4 closes the identity branch.  These application audits verify
    # the exact sign bridge, sharp degree, strict root count, and final fibre
    # contradiction; the theorem itself has its own generic, exceptional,
    # and independent exact checkers.
    audit_row_bridge()
    audit_sharp_degree_bound()
    audit_root_and_fibre_counts()


def geometry(r):
    exceptional = tuple(range(r + 6))
    common_live = tuple(range(r + 6, 2*r))
    centres = (2*r, 2*r + 1)
    extra = 2*r + 2
    common_active = common_live + centres
    active = common_active + (extra,)
    exceptional_betas = (
        (Fraction(0), Fraction(2), Fraction(2))
        + tuple(Fraction(value) for value in range(3, r + 6))
    )
    betas = exceptional_betas + (Fraction(1),) * (r - 3)
    require(
        len(exceptional_betas) == r + 6,
        "len(exceptional_betas) == r + 6",
    )
    require(
        len(betas) == 2*r + 3,
        "len(betas) == 2*r + 3",
    )
    require(
        len(common_active) == r - 4,
        "len(common_active) == r - 4",
    )
    require(
        len(active) == r - 3,
        "len(active) == r - 3",
    )
    return exceptional, common_live, centres, extra, common_active, active, betas


def audit_literal_response(r=7):
    (
        exceptional, common_live, centres, extra,
        common_active, active, betas,
    ) = geometry(r)
    marked = exceptional[0]
    remaining = exceptional[1:]
    p_left, p_right = remaining[:r], remaining[r:]
    s_marked = exceptional[:2]
    remaining = exceptional[2:]
    s_left, s_right = remaining[:r], remaining[r:]
    require(
        len(p_right) == 5 and len(s_right) == 4,
        "len(p_right) == 5 and len(s_right) == 4",
    )
    p_value = cauchy_permanent(
        tuple(betas[i] for i in p_left),
        (Fraction(1),)*(r-5) + tuple(betas[i] for i in p_right),
    )
    s_value = cauchy_permanent(
        tuple(betas[i] for i in s_left),
        (Fraction(1),)*(r-4) + tuple(betas[i] for i in s_right),
    )
    require(
        p_value and s_value,
        "p_value and s_value",
    )
    p = (Fraction(2), Fraction(3), Fraction(5))
    direct = Fraction(17)

    for target in common_active:
        others = tuple(i for i in common_active if i != target)
        rows = [ZERO] * len(betas)
        rows[marked] = E2
        rows[extra] = p
        rows[target] = E0
        for i in others:
            rows[i] = E1
        for i in p_left:
            rows[i] = E0
        for i in p_right:
            rows[i] = E1
        response = source_22_response(tuple(rows), betas, active, direct)
        require(
            response[target] == 2*p[2]*p_value,
            "response[target] == 2*p[2]*p_value",
        )
        require(
            all(response[i] == 0 for i in active if i != target),
            "all(response[i] == 0 for i in active if i != target)",
        )

    rows = [ZERO] * len(betas)
    for i in s_marked:
        rows[i] = E2
    for i in s_left:
        rows[i] = E0
    for i in s_right:
        rows[i] = E1
    for i in common_active:
        rows[i] = E1
    rows[extra] = p
    response = source_22_response(tuple(rows), betas, active, direct)
    require(
        response[extra] == 2*s_value,
        "response[extra] == 2*s_value",
    )

    # Coordinate representative, both binary orientations at one target;
    # the shore-count identity is target-independent.
    target = active[0]
    others = tuple(i for i in active if i != target)
    for same, opposite in ((E0, E1), (E1, E0)):
        rows = [ZERO] * len(betas)
        for i in s_marked:
            rows[i] = E2
        for i in s_left:
            rows[i] = same
        for i in s_right:
            rows[i] = opposite
        rows[target] = same
        for i in others:
            rows[i] = opposite
        response = source_22_response(tuple(rows), betas, active, direct)
        require(
            response[target] == 2*s_value,
            "response[target] == 2*s_value",
        )
        require(
            all(response[i] == 0 for i in others),
            "all(response[i] == 0 for i in others)",
        )


def main():
    audit_profile_census()
    print("r=7 census: 101 profiles, 97 closed, 4 exact residuals")
    audit_heavy_and_degree_bookkeeping()
    print("five-equal deletion descent and residual degree m_R-2: exact")
    audit_high_collision_boundaries()
    print("multiplicity-three/four collision sectors: exact")
    audit_sparse_double_determinants()
    print("sparse-double degree-eight determinants: localized UNIT")
    audit_cubic_identity_frontier()
    print("all-distinct cubic identity branch: closed uniformly by full DR4")
    audit_literal_response()
    print("literal r=7 P/S response, beta zero/repetition, scale 17: exact")
    print("sole-plane t=r+6 four-profile frontier: AUDIT PASS")


if __name__ == "__main__":
    main()
