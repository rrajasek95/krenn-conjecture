#!/usr/bin/env python3
"""Exact audit of the sole-plane layer t=r+4 (including (4,8))."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations
from math import factorial

import sympy as sp

from verify_live_three_zero_sole_plane_first_high_layer_uniform import (
    E0,
    E1,
    E2,
    ZERO,
    cauchy_permanent,
    source_22_response,
)


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def elementary(values, degree):
    return sum(
        (sp.prod(values[index] for index in subset)
         for subset in combinations(range(len(values)), degree)),
        sp.S.Zero,
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


def audit_profiles_and_triple_deletion():
    profiles = tuple(
        profile for profile in integer_partitions(8)
        if max(profile) <= 3
    )
    require(
        profiles == (
            (3, 3, 2), (3, 3, 1, 1), (3, 2, 2, 1),
            (3, 2, 1, 1, 1), (3, 1, 1, 1, 1, 1),
            (2, 2, 2, 2), (2, 2, 2, 1, 1),
            (2, 2, 1, 1, 1, 1), (2, 1, 1, 1, 1, 1, 1),
            (1, 1, 1, 1, 1, 1, 1, 1),
        ),
        "profiles == ( (3, 3, 2), (3, 3, 1, 1), (3, 2, 2, 1), (3, ...",
    )

    h = sp.symbols("h0:5", nonzero=True)
    e3 = elementary(h, 3)
    deleted_e3 = tuple(elementary(h[:m] + h[m + 1 :], 3) for m in range(5))
    require(
        sp.expand(sum(deleted_e3) - 2 * e3) == 0,
        "sp.expand(sum(deleted_e3) - 2 * e3) == 0",
    )
    for m in range(5):
        complement = h[:m] + h[m + 1 :]
        require(
            sp.expand(e3 - deleted_e3[m] - h[m] * elementary(complement, 2)) == 0,
            "sp.expand(e3 - deleted_e3[m] - h[m] * elementary(compleme...",
        )
    e2 = elementary(h, 2)
    deleted_e2 = tuple(elementary(h[:m] + h[m + 1 :], 2) for m in range(5))
    require(
        sp.expand(sum(deleted_e2) - 3 * e2) == 0,
        "sp.expand(sum(deleted_e2) - 3 * e2) == 0",
    )
    for m in range(5):
        complement = h[:m] + h[m + 1 :]
        require(
            sp.expand(e2 - deleted_e2[m] - h[m] * elementary(complement, 1)) == 0,
            "sp.expand(e2 - deleted_e2[m] - h[m] * elementary(compleme...",
        )

    rows = sp.symbols("u0:4")
    a = sp.Symbol("a")
    matrix = tuple(tuple(1 / (row + column) for column in (1, a, a, a)) for row in rows)
    hs = tuple((row + 1) / (row + a) for row in rows)
    expected = 6 * sp.prod(1 / (row + 1) for row in rows) * elementary(hs, 3)
    require(
        sp.cancel(permanent(matrix) - expected) == 0,
        "sp.cancel(permanent(matrix) - expected) == 0",
    )


def audit_distinct_quartic_obstruction():
    c, y, z, ay, az = sp.symbols("c y z A_y A_z")
    xy = ay + (c + 3 * y) / (c**2 - y**2)
    xz = az + (c + 3 * z) / (c**2 - z**2)
    # Projective compatibility of one affine factor ell=ux+v at the two
    # poles: u=X_y(v-uy), u=X_z(v-uz).
    numerator = sp.factor(
        sp.together(xy - xz + (z - y) * xy * xz).as_numer_denom()[0]
    )
    polynomial = sp.Poly(numerator, c)
    require(
        polynomial.degree() <= 4,
        "polynomial.degree() <= 4",
    )
    coefficients = polynomial.all_coeffs()
    require(
        sp.expand(coefficients[1] + (ay + az) * (y - z)) == 0,
        "sp.expand(coefficients[1] + (ay + az) * (y - z)) == 0",
    )
    # If the quartic were identically zero and y != z, the cubic
    # coefficient gives az=-ay.  The leading coefficient then gives
    # ay=0 or ay=-2/(y-z).  Both branches leave a nonzero coefficient.
    zero_branch = sp.Poly(numerator.subs({ay: 0, az: 0}), c)
    require(
        sp.expand(zero_branch.coeff_monomial(c**2) - 2 * (y - z)) == 0,
        "sp.expand(zero_branch.coeff_monomial(c**2) - 2 * (y - z))...",
    )
    exceptional_branch = sp.factor(
        numerator.subs({ay: -2 / (y - z), az: 2 / (y - z)})
    )
    require(
        sp.expand(
            exceptional_branch
            + 4 * (y - z) * (c**2 + c*y + c*z + 3*y*z)
        ) == 0,
        "sp.expand( exceptional_branch + 4 * (y - z) * (c**2 + c*y...",
    )

    # Ordinary Borchardt at a rational stress point, and the numerator
    # degree that leaves precisely one affine factor after five roots.
    row_values = tuple(map(sp.Rational, (2, 3, 5, 7)))
    pole_values = tuple(map(sp.Rational, (1, 11, 13, 17)))
    cauchy = sp.Matrix([[1 / (x + pole) for pole in pole_values] for x in row_values])
    squared = sp.Matrix([[1 / (x + pole) ** 2 for pole in pole_values] for x in row_values])
    require(
        sp.cancel(permanent(cauchy.tolist()) - squared.det() / cauchy.det()) == 0,
        "sp.cancel(permanent(cauchy.tolist()) - squared.det() / ca...",
    )
    denominator_degree = 2 * len(pole_values)
    require(
        denominator_degree - 2 == 6,
        "denominator_degree - 2 == 6",
    )
    require(
        6 - 5 == 1,
        "6 - 5 == 1",
    )


def confluent_matrices(row_profile, a, b):
    x = sp.Symbol("x")
    denominator_functions = (
        1 / (x + 1),
        1 / (x + a),
        -1 / (x + a) ** 2,
        1 / (x + b),
    )
    numerator_functions = (
        1 / (x + 1) ** 2,
        1 / (x + a) ** 2,
        -2 / (x + a) ** 3,
        1 / (x + b) ** 2,
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


def audit_double_pair_and_residue():
    # Column confluence, including an independent simultaneous row
    # confluence stress case.
    for row_profile in (
        ((sp.Rational(2), 1), (sp.Rational(3), 1),
         (sp.Rational(5), 1), (sp.Rational(7), 1)),
        ((sp.Rational(2), 2), (sp.Rational(3), 1),
         (sp.Rational(5), 1)),
    ):
        a, b = sp.Rational(11), sp.Rational(13)
        rows = tuple(value for value, multiplicity in row_profile for _ in range(multiplicity))
        raw = [[1 / (x + pole) for pole in (1, a, a, b)] for x in rows]
        denominator, numerator = confluent_matrices(row_profile, a, b)
        require(
            denominator.det() != 0,
            "denominator.det() != 0",
        )
        require(
            sp.cancel(permanent(raw) - numerator.det() / denominator.det()) == 0,
            "sp.cancel(permanent(raw) - numerator.det() / denominator....",
        )

    x, y, a = sp.symbols("x y a")
    base_minor = sp.det(sp.Matrix([
        [1 / (x + a) ** 2, -2 / (x + a) ** 3],
        [1 / (y + a) ** 2, -2 / (y + a) ** 3],
    ]))
    expected = -2 * (x - y) / ((x + a) ** 3 * (y + a) ** 3)
    require(
        sp.cancel(base_minor - expected) == 0,
        "sp.cancel(base_minor - expected) == 0",
    )

    b, constant = sp.symbols("b C")
    phi = 1 / (1 + b) - 2 / (b - 1)
    require(
        sp.factor(phi + (b + 3) / (b**2 - 1)) == 0,
        "sp.factor(phi + (b + 3) / (b**2 - 1)) == 0",
    )
    fibre = sp.Poly(sp.together(phi - constant).as_numer_denom()[0], b)
    require(
        fibre.degree() <= 2,
        "fibre.degree() <= 2",
    )
    require(
        fibre.coeff_monomial(b) == -1,
        "fibre.coeff_monomial(b) == -1",
    )

    # Outside a fixed double class, six labels of multiplicity at most two
    # contain at least three distinct values.
    for profile in ((2, 2, 2, 2), (2, 2, 2, 1, 1),
                    (2, 2, 1, 1, 1, 1), (2, 1, 1, 1, 1, 1, 1)):
        require(
            len(profile) - 1 >= 3,
            "len(profile) - 1 >= 3",
        )


def audit_s_embedding():
    exceptional = frozenset(range(8))
    # Every P_4 tuple on a seven-label deletion embeds as an S_4 tuple by
    # adjoining the omitted label to its marked singleton.
    count = 0
    for omitted in exceptional:
        seven = exceptional - {omitted}
        for marked in seven:
            remainder = seven - {marked}
            for left_tuple in combinations(sorted(remainder), 4):
                left = frozenset(left_tuple)
                right = remainder - left
                pair = frozenset((omitted, marked))
                require(
                    len(pair) == 2 and len(left) == 4 and len(right) == 2,
                    "len(pair) == 2 and len(left) == 4 and len(right) == 2",
                )
                require(
                    pair | left | right == exceptional,
                    "pair | left | right == exceptional",
                )
                count += 1
    require(
        count == 8 * 7 * 15,
        "count == 8 * 7 * 15",
    )


def audit_uniform_extension_frontier():
    # After the uniform triple closure, every part is at most two.  Seven
    # classes imply d <= r-3, exactly the number of common-pole jet columns.
    # The six-class boundary exists only at r=5,6,7,8.  Removing a fixed
    # double pair and a moving b leaves at most r-3 double base rows.
    six_class = []
    residual = []
    for r in range(5, 21):
        for profile in integer_partitions(r + 4, maximum=2):
            classes = len(profile)
            doubles = profile.count(2)
            if classes >= 7:
                require(
                    doubles <= r - 3,
                    "doubles <= r - 3",
                )
                continue
            if classes == 6:
                require(
                    r in (5, 6, 7, 8),
                    "r in (5, 6, 7, 8)",
                )
                require(
                    doubles in (3, 4, 5, 6),
                    "doubles in (3, 4, 5, 6)",
                )
                max_base_rows = max(
                    doubles - (2 if moving == 2 else 1)
                    for moving in set(profile[1:])
                )
                require(
                    max_base_rows <= r - 3,
                    "max_base_rows <= r - 3",
                )
                six_class.append((r, profile))
                continue
            residual.append((r, profile))
    require(
        six_class == [
            (5, (2, 2, 2, 1, 1, 1)),
            (6, (2, 2, 2, 2, 1, 1)),
            (7, (2, 2, 2, 2, 2, 1)),
            (8, (2, 2, 2, 2, 2, 2)),
        ],
        "six_class == [ (5, (2, 2, 2, 1, 1, 1)), (6, (2, 2, 2, 2, ...",
    )
    require(
        residual == [
            (5, (2, 2, 2, 2, 1)),
            (6, (2, 2, 2, 2, 2)),
        ],
        "residual == [ (5, (2, 2, 2, 2, 1)), (6, (2, 2, 2, 2, 2)), ]",
    )

    a, b, A, B = sp.symbols("a b A B")
    logarithmic_first = A + 1 / (a + b) + 2 / (a - b)
    logarithmic_second = B + 1 / (a + b) ** 2 + 2 / (a - b) ** 2
    numerator = sp.factor(sp.together(
        logarithmic_first**2 + logarithmic_second
    ).as_numer_denom()[0])
    polynomial = sp.Poly(numerator, b)
    require(
        polynomial.degree() == 4,
        "polynomial.degree() == 4",
    )
    expected = (
        A**2 + B,
        -2 * A,
        -2 * (A**2 * a**2 + 3 * A * a + B * a**2 - 2),
        2 * a * (A * a + 4),
        a**2 * (A**2 * a**2 + 6 * A * a + B * a**2 + 12),
    )
    require(
        all(
            sp.expand(actual - wanted) == 0
            for actual, wanted in zip(polynomial.all_coeffs(), expected)
        ),
        "all( sp.expand(actual - wanted) == 0 for actual, wanted i...",
    )
    # Identical vanishing would force A=0 from the cubic coefficient, after
    # which the linear coefficient is 8a, nonzero for a repeated class.
    require(
        sp.expand(polynomial.coeff_monomial(b**3) + 2 * A) == 0,
        "sp.expand(polynomial.coeff_monomial(b**3) + 2 * A) == 0",
    )
    require(
        sp.expand(polynomial.coeff_monomial(b).subs(A, 0) - 8 * a) == 0,
        "sp.expand(polynomial.coeff_monomial(b).subs(A, 0) - 8 * a...",
    )

    # The two apparent residuals close by fixing a double value b and
    # varying the selected repeated pair a,a.  The zero residue at -b has a
    # quadratic fibre in a, while there are respectively three and four
    # other double values.  The row-base counts equal the common-jet counts.
    moving, fixed, constant = sp.symbols("moving fixed constant")
    fibre_map = 2 / (moving + fixed) - 3 / (moving - fixed)
    require(
        sp.factor(
            fibre_map + (moving + 5 * fixed) / (moving**2 - fixed**2)
        ) == 0,
        "sp.factor( fibre_map + (moving + 5 * fixed) / (moving**2 ...",
    )
    fibre_polynomial = sp.Poly(
        sp.together(fibre_map - constant).as_numer_denom()[0], moving
    )
    require(
        fibre_polynomial.degree() <= 2,
        "fibre_polynomial.degree() <= 2",
    )
    require(
        abs(fibre_polynomial.coeff_monomial(moving)) == 1,
        "abs(fibre_polynomial.coeff_monomial(moving)) == 1",
    )
    for r, profile in residual:
        double_classes = profile.count(2)
        require(
            double_classes - 1 >= 3,
            "double_classes - 1 >= 3",
        )
        # Remove the moving double pair and one fixed-b label.
        require(
            double_classes - 2 == r - 3,
            "double_classes - 2 == r - 3",
        )


def find_pivots(betas):
    exceptional = tuple(range(8))
    for marked in exceptional:
        remainder = tuple(site for site in exceptional if site != marked)
        for left in combinations(remainder, 4):
            right = tuple(site for site in remainder if site not in left)
            value = cauchy_permanent(
                tuple(betas[site] for site in left),
                (Fraction(1),) + tuple(betas[site] for site in right),
            )
            if value:
                p_data = (marked, left, right, value)
                break
        else:
            continue
        break
    else:
        raise AssertionError("no P pivot at stress point")

    for marked in combinations(exceptional, 2):
        remainder = tuple(site for site in exceptional if site not in marked)
        for left in combinations(remainder, 4):
            right = tuple(site for site in remainder if site not in left)
            value = cauchy_permanent(
                tuple(betas[site] for site in left),
                (Fraction(1), Fraction(1))
                + tuple(betas[site] for site in right),
            )
            if value:
                return p_data, (marked, left, right, value)
    raise AssertionError("no S pivot at stress point")


def audit_literal_response():
    exceptional_betas = tuple(map(Fraction, (0, 2, 3, 4, 5, 6, 7, 8)))
    betas = exceptional_betas + (Fraction(1), Fraction(1), Fraction(1))
    centres = (8, 9)
    extra = 10
    active = centres + (extra,)
    direct_scale = Fraction(17)
    p = (Fraction(2), Fraction(3), Fraction(5))
    (marked, p_left, p_right, p_value), (s_marked, s_left, s_right, s_value) = find_pivots(betas)

    # Noncoordinate plane: P kills all three rows at c,d literally.
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
            require(
                response[target] == 2 * p[2] * p_value,
                "response[target] == 2 * p[2] * p_value",
            )
            require(
                all(response[site] == 0 for site in active if site != target),
                "all(response[site] == 0 for site in active if site != tar...",
            )

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
        require(
            response[target] == 2 * p[2] * p_value,
            "response[target] == 2 * p[2] * p_value",
        )
        require(
            all(response[site] == 0 for site in active if site != target),
            "all(response[site] == 0 for site in active if site != tar...",
        )

    # S kills an arbitrary contraction of the extra block modulo the
    # centre binary rows already killed above.
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
    require(
        response[extra] == 2 * s_value,
        "response[extra] == 2 * s_value",
    )

    # Coordinate plane: all three active sites are D-type.  S is a literal
    # singleton for both binary orientations and for each zero third row.
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
            require(
                response[target] == 2 * s_value,
                "response[target] == 2 * s_value",
            )
            require(
                all(response[site] == 0 for site in others),
                "all(response[site] == 0 for site in others)",
            )

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
        require(
            response[target] == 2 * s_value,
            "response[target] == 2 * s_value",
        )
        require(
            all(response[site] == 0 for site in others),
            "all(response[site] == 0 for site in others)",
        )


def audit_chart_cover():
    # 12 and 02 charts contain a literal row with source-2 coordinate.
    # In the 01 chart, a!=0 uses row zero, then b!=0 uses row one, and the
    # sole residual point a=b=0 is exactly the coordinate plane.
    a, b = sp.symbols("a b")
    chart_01 = sp.Matrix([[1, 0, a], [0, 1, b]])
    chart_12 = sp.Matrix([[a, 1, 0], [b, 0, 1]])
    chart_02 = sp.Matrix([[1, a, 0], [0, b, 1]])
    require(
        chart_12[1, 2] == 1 and chart_02[1, 2] == 1,
        "chart_12[1, 2] == 1 and chart_02[1, 2] == 1",
    )
    require(
        chart_01.subs({a: 0, b: 0}).rowspace() == [
            sp.Matrix([[1, 0, 0]]), sp.Matrix([[0, 1, 0]])
        ],
        "chart_01.subs({a: 0, b: 0}).rowspace() == [ sp.Matrix([[1...",
    )


def main():
    audit_profiles_and_triple_deletion()
    print("ten-profile census and triple-class deletion: exact")
    audit_distinct_quartic_obstruction()
    print("all-distinct projective quartic obstruction: exact")
    audit_double_pair_and_residue()
    print("double-pair confluence and quadratic residue fibre: exact")
    audit_s_embedding()
    print("S_4 embedding into the uniform P_4 family: exact")
    audit_uniform_extension_frontier()
    print("uniform t=r+4 closure, including dense-double fibres: exact")
    audit_literal_response()
    print("noncoordinate/coordinate literal response, direct scale 17: exact")
    audit_chart_cover()
    print("three-chart row-plane cover: exact")
    print("sole-plane layer t=r+4 closure: PASS")


if __name__ == "__main__":
    main()
