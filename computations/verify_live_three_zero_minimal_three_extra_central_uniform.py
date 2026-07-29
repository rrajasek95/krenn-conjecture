#!/usr/bin/env python3
"""Exact uniform-rank certificate for the central minimal three-extra chart.

Together with the Q=0 certificate imported below, this proves that the full
19-column response has rank 19 for every value of the six chart parameters.
Every selected row has source pair different from 01, so the arbitrary direct
B_01 term is absent identically.
"""

from __future__ import annotations

import sympy as sp

import verify_live_three_zero_minimal_three_extra_q0 as q0
from explore_live_three_zero_minimal_three_extra_response import (
    flint_determinant,
    symbolic_response_matrix,
)


CHARTS = q0.CHARTS
rows = q0.rows


N99_ROWS = rows(
    """
    2011210;11 0012110;11 0221012;11 0200112;11
    2000020;12 0001012;11 0010110;11 1110010;00
    2111010;00 1011010;02 1101010;00 0201012;11
    2201012;11 2200120;11 2100012;11 2200022;11
    0000012;00 0000020;00 0000110;00
    """
)

N98_ROWS = rows(
    """
    2020010;22 1012010;22 2201220;11 1000020;11
    1101010;22 0100020;11 1100010;02 0111010;22
    0001012;11 0010110;11 1211010;22 1110010;22
    2201012;11 2010012;11 0201012;11 0210110;11
    0000012;00 0000020;00 0000110;00
    """
)

A_PLANE_ROWS = rows(
    """
    0000210;00 0002010;00 0020010;00 0001110;11
    0010110;11 0011010;11 0100110;11 0111010;02
    1000110;11 1011010;02 1101010;02 1110010;02
    0011010;00 0201110;11 2001110;11 2200112;11
    0000110;00 0001012;00 0001020;00
    """
)

C_PLANE_ROWS = rows(
    """
    0001210;00 0002010;00 0020010;00 0001020;11
    0010020;11 0011010;11 0100020;11 0111010;02
    1000020;11 1011010;02 1101010;02 1110010;02
    0011010;00 0201020;11 2001020;11 2200022;11
    0000020;00 0001012;00 0001110;00
    """
)

E_PLANE_ROWS = rows(
    """
    0001210;00 0002010;00 0020010;00 0001012;11
    0010012;11 0011010;11 0100012;11 0111010;02
    1000012;11 1011010;02 1101010;02 1110010;02
    0011010;00 0201012;11 2001012;11 2200022;11
    0000012;00 0001020;00 0001110;00
    """
)

A_QUADRATIC_ROWS = rows(
    """
    0101210;11 2221010;12 0212110;11 1211010;00
    2200022;11 2010020;11 2001010;12 0200112;11
    0110010;11 1110010;00 2111010;22 1101010;22
    0101010;02 2110010;02 1210010;11 2110010;11
    0000110;00 0001012;00 0001020;00
    """
)

AXIS_A_ROWS = rows(
    """
    2221010;12 2210212;11 2202112;00 0211010;11
    0210012;11 1211010;00 2210010;12 2100020;11
    1101010;00 2201010;22 2001012;11 0111010;00
    1110010;02 2200022;11 2110010;02 2201010;00
    0001012;00 0001020;00 0011110;00
    """
)

AXIS_C_ROWS = rows(
    """
    0201210;02 1221010;11 2112010;00 2010012;11
    2210010;22 2200022;11 2201020;11 1211010;02
    1101010;00 2111010;00 2200110;12 0210012;11
    1110010;00 2201110;11 0201010;00 1210010;00
    0001012;00 0001110;00 0011020;00
    """
)

AXIS_E_ROWS = rows(
    """
    0201210;02 1221010;11 2112010;00 2010020;11
    2210010;22 2200022;11 1211010;02 1101010;00
    2111010;00 2200110;12 0210020;11 1201010;11
    1110010;00 2201020;11 0201010;00 1210010;00
    0001020;00 0001110;00 0011012;00
    """
)

ORIGIN_ROWS = rows(
    """
    1202010;00 2221010;02 1200210;00 2210110;11
    2211010;11 1211010;02 2210012;11 1110010;00
    2201012;11 2200120;11 0111010;00 1101010;00
    2011010;02 0211010;02 2211010;00 1210010;00
    0011012;00 0011020;00 0011110;00
    """
)

DOUBLE_CE_ROWS = rows(
    """
    2112010;12 1020110;02 1210210;12 0101010;12
    2200012;12 1001010;12 0210012;11 1110010;00
    1011010;02 0200120;11 1111010;11 0111010;22
    1101010;02 2100010;02 0201010;02 2201012;11
    0000110;00 0001012;00 0001020;00
    """
)

DOUBLE_AE_ROWS = rows(
    """
    2202010;00 1110210;11 2021020;11 2001012;11
    1101010;00 1000020;11 2200012;12 2010110;11
    1211010;22 0201010;22 0111010;02 1111010;11
    1110010;00 1200010;02 2010010;02 2200120;11
    0000020;00 0001012;00 0001110;00
    """
)

DOUBLE_AC_ROWS = rows(
    """
    2202010;00 1110210;11 2021020;11 1101010;00
    2200020;12 1000012;11 2010110;11 1211010;22
    0201010;22 1001010;11 0111010;02 1111010;11
    1110010;00 1200010;02 2010010;02 2201110;11
    0000012;00 0001020;00 0001110;00
    """
)


_DETERMINANTS = {}


def determinant(labels):
    if labels not in _DETERMINANTS:
        _DETERMINANTS[labels] = flint_determinant(CHARTS, labels)
    return _DETERMINANTS[labels]


def assert_parameter_only(value):
    degrees = value.degrees()
    assert degrees[1] == degrees[3] == degrees[5] == 0


def certify_new_parameter_only_minors():
    n99 = determinant(N99_ROWS)
    a, b, c, d, e, f = n99.context().gens()
    s, g, p, q, j, ell, k, xminor, fpoly, w, delta, pair_product = (
        q0.invariant_polynomials(a, c, e)
    )
    u = 6*p + 3*g + s
    v = (
        4*a**2*c*e + a**2*c + 4*a**2*e - a*c**2
        + 3*a*c*e - c**2*e
    )
    assert n99 == (
        2**39 * 3**7 * a**6 * c**8 * e**5
        * (c + e) * (a + c) * (s + 3) * k * q**2
    )
    assert_parameter_only(n99)

    n98 = determinant(N98_ROWS)
    assert n98 == 2**41 * 3**7 * a**7 * c**7 * e**6 * j**4 * u * v
    assert_parameter_only(n98)

    yplane = a*c - 2*a*e - 2*a + c*e + 4*c - 2*e
    plane_certificates = (
        (
            A_PLANE_ROWS,
            2**38 * 3**9 * c**9 * e**8 * g**2 * k**4
            * (a*e + 2*a + 2*e) * (a*c + 2*a + 2*c) * yplane,
        ),
        (
            C_PLANE_ROWS,
            2**37 * 3**9 * a**8 * e**7 * g**2 * k**4
            * (a*c + 2*a + 2*c) * xminor * (c*e + 2*c + 2*e)**2,
        ),
        (
            E_PLANE_ROWS,
            2**37 * 3**9 * a**8 * c**7 * g**2 * k**4
            * (a*e + 2*a + 2*e) * xminor * (c*e + 2*c + 2*e)**2,
        ),
    )
    for labels, expected in plane_certificates:
        actual = determinant(labels)
        assert actual == expected
        assert_parameter_only(actual)


def assert_localized_unit(name, equations, localizers, variables):
    tau = sp.Symbol("tau_" + name)
    ideal = [sp.expand(polynomial) for polynomial in equations]
    ideal.append(1 - tau*sp.prod(localizers))
    basis = sp.groebner(
        ideal, *variables, tau, order="grevlex", domain=sp.QQ
    )
    assert basis.reduce(sp.S.One)[1] == 0, name


def certify_noncoordinate_saturation():
    a, c, e, x, y = sp.symbols("a c e x y")
    s, g, p, q, j, ell, k, xminor, fpoly, w, delta, pair_product = (
        q0.invariant_polynomials(a, c, e)
    )
    u = 6*p + 3*g + s
    v = (
        4*a**2*c*e + a**2*c + 4*a**2*e - a*c**2
        + 3*a*c*e - c**2*e
    )

    # On ace*Q != 0 these are precisely the squarefree supports of N99
    # and N98 after deleting invertible factors.
    n99_open = (c + e) * (a + c) * (s + 3) * k
    n98_open = j * u * v
    assert sp.expand(pair_product - (s*g - p)) == 0

    pair_substitutions = {
        "ac": {a: x, c: x, e: y},
        "ae": {a: x, e: x, c: y},
        "ce": {c: x, e: x, a: y},
    }
    repeated_branches = (
        ("GL", (g, ell), False),
        ("GK", (g, k), False),
        ("KJ", (k, j), True),
        ("KF", (k, fpoly), True),
        ("JX", (j, xminor), True),
        ("LXF", (ell, xminor, fpoly), True),
    )
    checked = 0
    for branch_name, equations, invert_g in repeated_branches:
        for pair_name, substitution in pair_substitutions.items():
            localized = [(a*c*e*q).subs(substitution)]
            if invert_g:
                localized.append(g.subs(substitution))
            assert_localized_unit(
                branch_name + pair_name,
                [polynomial.subs(substitution) for polynomial in equations]
                + [n99_open.subs(substitution), n98_open.subs(substitution)],
                localized,
                (x, y),
            )
            checked += 1

    nonrepeated_branches = (
        ("GLW", (g, ell, w), False),
        ("GKW", (g, k, w), False),
        ("KJW", (k, j, w), True),
    )
    for branch_name, equations, invert_g in nonrepeated_branches:
        localized = [a*c*e*q]
        if invert_g:
            localized.append(g)
        assert_localized_unit(
            branch_name,
            list(equations) + [n99_open, n98_open],
            localized,
            (a, c, e),
        )
        checked += 1
    assert checked == 21


def squarefree_restricted_support(labels, substitutions, variables, symbols):
    value = determinant(labels)
    assert_parameter_only(value)
    local_map = {str(symbol): symbol for symbol in symbols}
    product = sp.S.One
    for factor, _multiplicity in value.factor()[1]:
        expression = sp.sympify(
            str(factor).replace("^", "**"), locals=local_map
        )
        restricted = sp.factor(expression.subs(substitutions))
        assert restricted != 0
        if not restricted.is_number:
            product *= restricted
    return sp.Poly(product, *variables, domain=sp.QQ).sqf_part().monic().as_expr()


def groebner_expressions(polynomials, variables):
    basis = sp.groebner(polynomials, *variables, order="lex", domain=sp.QQ)
    return tuple(sp.expand(polynomial.as_expr()) for polynomial in basis.polys)


def monic_expression(polynomial, variables):
    return sp.Poly(polynomial, *variables, domain=sp.QQ).monic().as_expr()


def certify_coordinate_planes():
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    symbols = (a, b, c, d, e, f)
    plane_data = (
        (
            "a",
            {a: 0},
            (c, e),
            (
                A_PLANE_ROWS,
                *q0.COORD_A_CURVE_ROWS,
                AXIS_E_ROWS,
                AXIS_C_ROWS,
                ORIGIN_ROWS,
                q0.COORD_C_ENDPOINT_ROWS,
                q0.COORD_E_ENDPOINT_ROWS,
            ),
            (
                c + sp.Rational(16, 13)*e**2
                + sp.Rational(283, 91)*e + sp.Rational(300, 91),
                e**3 + sp.Rational(26, 7)*e**2
                + sp.Rational(33, 7)*e + sp.Rational(18, 7),
            ),
        ),
        (
            "c",
            {c: 0},
            (a, e),
            (
                C_PLANE_ROWS,
                *q0.COORD_C_CURVE_ROWS,
                AXIS_A_ROWS,
                AXIS_E_ROWS,
                ORIGIN_ROWS,
                q0.COORD_A_ENDPOINT_ROWS,
                q0.COORD_E_ENDPOINT_ROWS,
            ),
            (a + 2, e + 2),
        ),
        (
            "e",
            {e: 0},
            (a, c),
            (
                E_PLANE_ROWS,
                *q0.COORD_E_CURVE_ROWS,
                AXIS_A_ROWS,
                AXIS_C_ROWS,
                ORIGIN_ROWS,
                q0.COORD_A_ENDPOINT_ROWS,
                q0.COORD_C_ENDPOINT_ROWS,
            ),
            (a + 2, c + 2),
        ),
    )

    for plane_name, substitutions, variables, witnesses, expected in plane_data:
        supports = [
            squarefree_restricted_support(
                labels, substitutions, variables, symbols
            )
            for labels in witnesses
        ]
        assert groebner_expressions(supports, variables) == tuple(expected), plane_name

        if plane_name == "a":
            quadratic_support = squarefree_restricted_support(
                A_QUADRATIC_ROWS, substitutions, variables, symbols
            )
            expected_support = (
                c*e*(c - e)*(c + e)*(c + e + 3)
                * (3*c*e + c + e)*(c*e + 3*c + 3*e + 6)
            )
            assert quadratic_support == monic_expression(
                expected_support, variables
            )
            assert groebner_expressions(
                supports + [quadratic_support], variables
            ) == (c + 2, e + 2)


def certify_double_coordinate_points():
    cases = (
        (DOUBLE_CE_ROWS, (0, -2, -2), 2**68 * 3**9),
        (DOUBLE_AE_ROWS, (-2, 0, -2), 2**66 * 3**12),
        (DOUBLE_AC_ROWS, (-2, -2, 0), 2**66 * 3**12),
    )
    for labels, (avalue, cvalue, evalue), expected in cases:
        parameters, matrix = symbolic_response_matrix(CHARTS, labels)
        a, b, c, d, e, f = parameters
        restricted = matrix.subs({a: avalue, c: cvalue, e: evalue})
        # Equality to a scalar proves independence of all three nuisance
        # parameters b,d,f at the point, not merely nonvanishing at b=d=f=0.
        assert sp.factor(restricted.det(method="domain-ge")) == expected


def main():
    # Re-run the companion Q=0 audit so this script is an end-to-end central
    # chart certificate rather than merely an audit of its complement.
    q0.certify_parameter_only_minors()
    q0.certify_fixed_points()
    q0.certify_branch_algebra()
    certify_new_parameter_only_minors()
    certify_noncoordinate_saturation()
    certify_coordinate_planes()
    certify_double_coordinate_points()
    print("minimal three-extra central 01^3 chart: UNIFORM RANK 19")
    print("Q=0 closure and 21 Q-nonzero noncoordinate branch ideals: exact")
    print("three coordinate-plane ideals and three endpoint minors: exact")
    print("all selected rows direct-free; arbitrary B_01 scale allowed")


if __name__ == "__main__":
    main()
