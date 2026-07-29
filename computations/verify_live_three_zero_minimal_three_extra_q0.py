#!/usr/bin/env python3
"""Exact certificate that the central minimal three-extra response has no Q=0 survivor.

All response rows used below have source pair different from 01.  Consequently
the arbitrary direct B_01 term is identically absent from every certified
minor.  Determinants are taken after clearing the common 1/4 row factor, as in
the generic-frontier certificate.
"""

from __future__ import annotations

import sympy as sp

from explore_live_three_zero_minimal_three_extra_response import flint_determinant


CHARTS = ("01", "01", "01")


def rows(specification: str):
    answer = []
    for token in specification.split():
        word, source = token.split(";")
        answer.append((tuple(map(int, word)), int(source[0]), int(source[1])))
    assert len(answer) == 19
    assert all((source_left, source_right) != (0, 1)
               for _, source_left, source_right in answer)
    return tuple(answer)


STANDARD_EXTRA = "0000012;00 0000020;00 0000110;00"

M0_ROWS = rows(
    """
    0020010;00 2212022;11 2200222;00 1011010;02
    0200120;11 2000112;11 1110010;22 2111010;02
    0001012;11 0010110;11 1101010;22 0201020;11
    0201012;11 1001010;11 2001012;11 2201012;11
    """ + STANDARD_EXTRA
)

MG_ROWS = rows(
    """
    1220012;11 0212020;11 2201210;12 2000010;22
    0010110;11 0200110;12 2111010;02 1101010;02
    1011010;22 1110010;02 0001012;11 2001110;11
    0210110;11 1200012;11 2210110;11 1010010;11
    """ + STANDARD_EXTRA
)

ML_ROWS = rows(
    """
    0000210;00 0002010;00 0020010;00 0001010;12
    0010010;12 0100010;12 0111010;02 1000010;12
    1011010;02 1101010;02 1110010;02 1111010;11
    0211010;02 2011010;02 0011010;00 0011010;11
    """ + STANDARD_EXTRA
)

MK_ROWS = rows(
    """
    0000210;00 0002010;00 0020010;00 0001010;12
    0010010;12 0100010;12 0111010;22 1000010;12
    1011010;22 1101010;22 1110010;22 0011010;00
    0011010;02 0011010;11 0201012;11 2001012;11
    """ + STANDARD_EXTRA
)

MJ_ROWS = rows(
    """
    0000210;00 0002010;00 0020010;00 0001010;12
    0010010;12 0100010;12 0111010;02 1000010;12
    1011010;02 1101010;02 1110010;02 0011010;00
    0011010;11 0201012;11 0201020;11 2001012;11
    """ + STANDARD_EXTRA
)

MP_ROWS = rows(
    """
    0000210;00 0002010;00 0020010;00 0001010;12
    0010010;12 0100010;12 0111010;22 1000010;12
    1011010;22 1101010;22 1110010;22 0011010;00
    0011010;02 0201012;11 0201020;11 2001012;11
    """ + STANDARD_EXTRA
)

MACE_ROWS = rows(
    """
    0000010;00 0000010;02 0000210;00 0001010;00
    0001010;02 0001010;12 0002010;02 0010010;00
    0010010;02 0011010;00 0020010;02 0100010;00
    0100010;02 0200010;02 1000010;02 2000010;02
    """ + STANDARD_EXTRA
)

ALL_ONE_ROWS = rows(
    """
    0000210;00 0002010;00 0020010;00 0001010;12
    0010010;12 0100010;12 0111010;12 0211010;02
    1000010;12 1011010;12 1101010;12 1110010;12
    0201010;00 2001010;00 0201012;11 0201020;11
    """ + STANDARD_EXTRA
)

COORD_A_ENDPOINT_ROWS = rows(
    """
    0011210;00 0012010;00 0021010;00 0011010;00
    0101010;00 0110010;00 0111010;02 0111010;11
    0200022;11 0201010;00 0201012;11 0201020;11
    1001010;00 1011010;11 1101010;11 2001010;00
    0001012;00 0001020;00 0011110;00
    """
)

COORD_C_ENDPOINT_ROWS = rows(
    """
    0001210;00 0012010;00 0021010;00 0011010;00
    0101010;00 0110010;00 0111010;02 0111010;11
    0200112;11 0201010;00 0201012;11 0201110;11
    1001010;00 1011010;11 1101010;11 2001010;00
    0001012;00 0001110;00 0011020;00
    """
)

COORD_E_ENDPOINT_ROWS = rows(
    """
    0001210;00 0012010;00 0021010;00 0011010;00
    0101010;00 0110010;00 0111010;02 0111010;11
    0200120;11 0201010;00 0201020;11 0201110;11
    1001010;00 1011010;11 1101010;11 2001010;00
    0001020;00 0001110;00 0011012;00
    """
)

# Three direct-free witnesses on a=0, Q=0.  Their restricted squarefree
# supports have gcd c(c+2).
COORD_A_CURVE_ROWS = (
    rows(
        """
        2120010;02 0101210;11 1212010;02 1100010;22
        2010010;22 1000110;11 0200112;11 0011010;11
        1110010;02 1011010;02 1101010;02 2111010;22
        0110010;00 0211010;11 2201012;11 2211010;11
        0000110;00 0001012;00 0001020;00
        """
    ),
    rows(
        """
        1202010;12 2221022;11 2200210;00 1100010;11
        2010010;22 1000110;11 0200112;11 0101010;12
        0111010;02 1011010;22 1101010;02 1110010;02
        1001010;00 1201010;11 2201110;11 2101010;11
        0000110;00 0001012;00 0001020;00
        """
    ),
    rows(
        """
        2212012;00 1110210;11 0221110;11 0110010;22
        1010010;11 2100012;11 0011010;11 1000110;11
        1101010;22 2111010;02 1110010;22 1211010;02
        0101010;00 2210110;11 1210010;11 2011010;11
        0000110;00 0001012;00 0001020;00
        """
    ),
)

# Three witnesses on c=0, Q=0.  Their restricted squarefree supports have
# gcd a(a+2).
COORD_C_CURVE_ROWS = (
    rows(
        """
        2201210;22 1112010;11 2021010;12 0110010;11
        1000020;11 2010110;11 1001010;11 2200010;22
        2111010;02 1101010;02 1211010;02 1110010;02
        1010010;00 2001020;11 1200020;11 2210020;11
        0000020;00 0001012;00 0001110;00
        """
    ),
    rows(
        """
        2212112;11 0210210;02 2220010;00 0011010;12
        2000020;12 2100110;11 1010010;22 0100020;11
        1011010;02 1110010;02 1101010;02 2111010;22
        0101010;00 2010020;11 1210010;11 2201020;11
        0000020;00 0001012;00 0001110;00
        """
    ),
    rows(
        """
        1202012;11 1220010;12 0011210;02 0100020;11
        0111010;22 1200010;12 1010010;22 1110010;22
        0201010;12 0110010;12 1211010;22 1101010;22
        1100010;00 1201010;11 2201012;11 2201110;11
        0000020;00 0001012;00 0001110;00
        """
    ),
)

# Three witnesses on e=0, Q=0.  Their restricted squarefree supports also
# have gcd a(a+2).
COORD_E_CURVE_ROWS = (
    rows(
        """
        2201210;22 1112010;11 2021010;12 0110010;11
        2001020;11 1000012;11 1200020;11 2010110;11
        2111010;02 1101010;02 1211010;02 1110010;02
        1010010;00 2210020;11 1210010;11 2210012;11
        0000012;00 0001020;00 0001110;00
        """
    ),
    rows(
        """
        2212112;11 0210210;02 2220010;00 0011010;12
        2010020;11 2000012;12 2100110;11 0100012;11
        1011010;02 1110010;02 1101010;02 2111010;22
        0101010;00 2010012;11 0201012;11 2201020;11
        0000012;00 0001020;00 0001110;00
        """
    ),
    rows(
        """
        1202012;11 1220010;12 0011210;02 0100012;11
        0111010;22 1200010;12 1010010;22 1110010;22
        0201010;12 0110010;12 1211010;22 1101010;22
        1100010;00 1201010;11 2201012;11 2201110;11
        0000012;00 0001020;00 0001110;00
        """
    ),
)


def invariant_polynomials(a, c, e):
    s = a + c + e
    g = a * c + a * e + c * e
    p = a * c * e
    q = g + 3 * s + 6
    j = 3 * p + g
    ell = 3 * g + 4 * s + 3
    k = 3 * p + 4 * g + 3 * s
    x = a * c + a * e + 4 * a - 2 * c * e - 2 * c - 2 * e
    fpoly = (
        3 * a * c**2 * e + 3 * a * c * e**2 + 16 * a * c * e
        + 6 * a * c + 6 * a * e - 6 * c**2 * e**2
        - 8 * c**2 * e - 6 * c**2 - 8 * c * e**2 - 6 * e**2
    )
    w = (
        a**2 * c**2 * e + 4 * a**2 * c**2 + a**2 * c * e**2
        + 2 * a**2 * c * e + 4 * a**2 * e**2 + a * c**2 * e**2
        + 2 * a * c**2 * e + 2 * a * c * e**2 + 4 * c**2 * e**2
    )
    delta = (a - c) * (a - e) * (c - e)
    pair_product = (a + c) * (a + e) * (c + e)
    return s, g, p, q, j, ell, k, x, fpoly, w, delta, pair_product


def certify_parameter_only_minors():
    certificates = (
        ("M0", M0_ROWS, lambda a, c, e, z:
         -(2**40) * 3**8 * a**6 * c**8 * e**5
         * z[1] * z[5] * z[6] * z[4]**2),
        ("MG", MG_ROWS, lambda a, c, e, z:
         -(2**37) * 3**9 * a**5 * c**9 * e**8
         * z[11] * z[5] * z[4] * z[6]**2),
        ("ML", ML_ROWS, lambda a, c, e, z:
         2**35 * 3**14 * a**6 * c**7 * e**7
         * z[10] * z[1]**2 * z[6]**6),
        ("MK", MK_ROWS, lambda a, c, e, z:
         -(2**40) * 3**14 * a**8 * c**9 * e**7
         * z[10] * z[1]**2 * z[4]**4),
        ("MJ", MJ_ROWS, lambda a, c, e, z:
         2**36 * 3**13 * a**9 * c**9 * e**8
         * z[1]**2 * z[6]**4 * z[7]),
        ("MP", MP_ROWS, lambda a, c, e, z:
         2**39 * 3**13 * a**9 * c**8 * e**7
         * z[1]**2 * z[4]**4 * z[8]),
        ("Mace", MACE_ROWS, lambda a, c, e, z:
         -(2**35) * 3**26 * a**10 * c**11 * e**11
         * z[10] * z[9]**2),
    )
    determinants = {}
    for name, labels, expected in certificates:
        determinant = flint_determinant(CHARTS, labels)
        a, b, c, d, e, f = determinant.context().gens()
        invariants = invariant_polynomials(a, c, e)
        assert determinant == expected(a, c, e, invariants), name
        assert determinant.degrees()[1] == 0
        assert determinant.degrees()[3] == 0
        assert determinant.degrees()[5] == 0
        determinants[name] = determinant
    return determinants


def certify_fixed_points():
    cases = (
        (COORD_A_ENDPOINT_ROWS, (-2, 0, 0), -(2**65) * 3**18),
        (COORD_C_ENDPOINT_ROWS, (0, -2, 0), 2**66 * 3**18),
        (COORD_E_ENDPOINT_ROWS, (0, 0, -2), 2**66 * 3**18),
        (ALL_ONE_ROWS, (-1, -1, -1), -(2**40) * 3**22),
    )
    for labels, (avalue, cvalue, evalue), expected in cases:
        determinant = flint_determinant(CHARTS, labels)
        assert determinant.degrees()[1] == 0
        assert determinant.degrees()[3] == 0
        assert determinant.degrees()[5] == 0
        assert determinant(avalue, 0, cvalue, 0, evalue, 0) == expected


def monic_squarefree_support(determinant, substitutions, variable, symbols):
    """Squarefree numerator support after restriction, ignoring multiplicities."""
    _, factors = determinant.factor()
    numerator = sp.S.One
    locals_map = {str(symbol): symbol for symbol in symbols}
    for factor, _multiplicity in factors:
        expression = sp.sympify(str(factor).replace("^", "**"), locals=locals_map)
        restricted = sp.cancel(expression.subs(substitutions))
        factor_numerator = restricted.as_numer_denom()[0]
        assert factor_numerator != 0
        numerator *= factor_numerator
    return sp.Poly(numerator, variable, domain=sp.QQ).sqf_part().monic()


def certify_coordinate_curves(a, b, c, d, e, f):
    symbols = (a, b, c, d, e, f)
    expected_a = (
        c * (c + 2) * (c**2 + 3*c + 3)
        * (3*c**2 + 8*c + 6) * (4*c**2 + 9*c + 3),
        -c * (c + 2) * (c**2 - 6*c - 24)
        * (c**2 + 6*c + 6) * (3*c**2 + 8*c + 6),
        c * (c + 2) * (c**2 - 6) * (c**2 - 6*c - 24)
        * (c**2 + 3*c + 3) * (c**2 + 6*c + 6),
    )
    supports_a = []
    for labels, expected in zip(COORD_A_CURVE_ROWS, expected_a):
        determinant = flint_determinant(CHARTS, labels)
        support = monic_squarefree_support(
            determinant,
            {a: 0, e: -(3*c + 6) / (c + 3)},
            c,
            symbols,
        )
        assert support == sp.Poly(expected, c, domain=sp.QQ).monic()
        supports_a.append(support)
    gcd_a = sp.gcd(sp.gcd(supports_a[0], supports_a[1]), supports_a[2])
    assert gcd_a == sp.Poly(c * (c + 2), c).monic()

    expected_c = (
        a * (a + 2) * (a**2 - 6*a - 24) * (a**2 + 3*a + 3)
        * (a**2 + 6*a + 6) * (3*a**2 + 8*a + 6),
        a * (a + 2) * (a**2 - 6*a - 24) * (a**2 + 6*a + 6)
        * (3*a**2 + 8*a + 6) * (4*a**2 + 9*a + 3),
        a * (a + 2) * (a**2 + 3*a + 3) * (4*a**2 + 9*a + 3),
    )
    expected_e = (
        a * (a + 2) * (a**2 + 3*a + 3) * (3*a**2 + 8*a + 6),
        a * (a + 2) * (a**2 + 12*a + 12)
        * (3*a**2 + 8*a + 6) * (4*a**2 + 9*a + 3),
        a * (a + 2) * (a**2 - 6)
        * (a**2 + 3*a + 3) * (4*a**2 + 9*a + 3),
    )
    curve_data = (
        (COORD_C_CURVE_ROWS, expected_c,
         {c: 0, e: -(3*a + 6) / (a + 3)}),
        (COORD_E_CURVE_ROWS, expected_e,
         {e: 0, c: -(3*a + 6) / (a + 3)}),
    )
    for labels_list, expected_list, substitutions in curve_data:
        supports = []
        for labels, expected in zip(labels_list, expected_list):
            determinant = flint_determinant(CHARTS, labels)
            support = monic_squarefree_support(
                determinant, substitutions, a, symbols
            )
            assert support == sp.Poly(expected, a, domain=sp.QQ).monic()
            supports.append(support)
        curve_gcd = sp.gcd(sp.gcd(supports[0], supports[1]), supports[2])
        assert curve_gcd == sp.Poly(a * (a + 2), a).monic()


def same_ideal(left, right, variables):
    left_basis = sp.groebner(left, *variables, order="lex", domain=sp.QQ)
    right_basis = sp.groebner(right, *variables, order="lex", domain=sp.QQ)
    assert all(right_basis.reduce(polynomial)[1] == 0 for polynomial in left)
    assert all(left_basis.reduce(polynomial)[1] == 0 for polynomial in right)


def certify_branch_algebra():
    a, b, c, d, e, f, x, y, z = sp.symbols("a b c d e f x y z")
    s, g, p, q, j, ell, k, xminor, fpoly, w, delta, pair_product = (
        invariant_polynomials(a, c, e)
    )

    # The four exact ideal identities defining the Q=0 branch table.
    same_ideal((q, g), (g, s + 2), (a, c, e))
    same_ideal((q, ell), (g - 3, s + 3), (a, c, e))
    same_ideal((q, k), (g + 3*s + 6, p - 3*s - 8), (a, c, e))
    same_ideal((q, j), (g + 3*s + 6, p - s - 2), (a, c, e))
    same_ideal((q, k, j), (s + 3, g - 3, p + 1), (a, c, e))
    same_ideal((q, ell, k), (s + 3, g - 3, p + 1), (a, c, e))

    # Symmetric identities used on G=0.
    assert sp.expand(pair_product - (s*g - p)) == 0
    cubic = sp.expand((z-a) * (z-c) * (z-e))
    assert sp.expand(cubic - (z**3 - s*z**2 + g*z - p)) == 0
    g_ace_two = sp.groebner((s + 2, g, p - 2), a, c, e,
                            order="lex", domain=sp.QQ)
    assert g_ace_two.reduce(w - 24)[1] == 0
    assert g_ace_two.reduce(delta**2 + 44)[1] == 0
    assert sp.discriminant(z**3 + 2*z**2 - 2, z) == -44
    assert sp.factor((z**3 + 2*z**2).subs(z, z)) == z**2 * (z + 2)

    def pair_substitution(which):
        if which == "ac":
            return {a: x, c: x, e: y}
        if which == "ae":
            return {a: x, e: x, c: y}
        if which == "ce":
            return {c: x, e: x, a: y}
        raise ValueError(which)

    # L=0: a repeated coordinate gives only the all-one point.
    lsub = pair_substitution("ac")
    l_resultant = sp.factor(sp.resultant(q.subs(lsub), ell.subs(lsub), y))
    assert sp.expand(l_resultant + 15*(x + 1)**2) == 0

    # K=0: apart from all-one, a repeated value satisfies h=0 and has
    # third value -(2x+8)/3.  The MP factor F is coprime to h in all
    # three orientations.
    h = x**2 + 4*x + 6
    ksub = pair_substitution("ac")
    k_resultant = sp.factor(sp.resultant(q.subs(ksub), k.subs(ksub), y))
    assert sp.expand(k_resultant + 3*(x + 1)**2*h) == 0
    y_k = -(2*x + 8) / 3
    assert sp.rem(sp.together(q.subs(ksub).subs(y, y_k)).as_numer_denom()[0],
                  h, domain=sp.QQ) == 0
    assert sp.rem(sp.together(k.subs(ksub).subs(y, y_k)).as_numer_denom()[0],
                  h, domain=sp.QQ) == 0
    expected_f_remainders = {
        "ac": -48*(x + 7),
        "ae": -48*(x + 7),
        "ce": -144*(x + 1),
    }
    for which, expected in expected_f_remainders.items():
        restricted = sp.together(
            fpoly.subs(pair_substitution(which)).subs(y, y_k)
        )
        numerator = restricted.as_numer_denom()[0]
        remainder = sp.rem(numerator, h, domain=sp.QQ)
        assert sp.expand(remainder - expected) == 0
        assert sp.gcd(sp.Poly(remainder, x), sp.Poly(h, x)) == 1

    # J=0: a repeated value is x=0,-1,-4.  The first is coordinate,
    # the second is all-one, and at x=-4 the third value is -2/5 while
    # X is nonzero in every orientation.
    jsub = pair_substitution("ac")
    j_resultant = sp.factor(sp.resultant(q.subs(jsub), j.subs(jsub), y))
    assert sp.expand(j_resultant + 3*x*(x + 1)**2*(x + 4)) == 0
    for xv, yv in ((0, -2), (-1, -1), (-4, sp.Rational(-2, 5))):
        assert q.subs(jsub).subs({x: xv, y: yv}) == 0
        assert j.subs(jsub).subs({x: xv, y: yv}) == 0
    expected_x_forms = {
        "ac": (x + 2)*(x - y),
        "ae": (x + 2)*(x - y),
        "ce": -2*(x + 2)*(x - y),
    }
    for which, expected in expected_x_forms.items():
        actual = sp.expand(xminor.subs(pair_substitution(which)))
        assert sp.expand(actual - expected) == 0
        assert actual.subs({x: -4, y: sp.Rational(-2, 5)}) != 0

    # None of the rational coordinate parametrizations loses a point:
    # its proposed denominator cannot vanish on the corresponding curve.
    assert sp.expand(q.subs({a: 0, c: -3})) == -3
    assert sp.expand(q.subs({c: 0, a: -3})) == -3
    assert sp.expand(q.subs({e: 0, a: -3})) == -3

    certify_coordinate_curves(a, b, c, d, e, f)


def main():
    certify_parameter_only_minors()
    certify_fixed_points()
    certify_branch_algebra()
    print("minimal three-extra Q=0 closure: PASS")
    print("seven direct-free parameter-only maximal minors: exact")
    print("four fixed-point determinants: exact")
    print("three coordinate-curve gcds and all branch ideals: exact")


if __name__ == "__main__":
    main()
