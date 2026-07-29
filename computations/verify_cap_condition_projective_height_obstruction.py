#!/usr/bin/env python3
"""Exact audit for cap-condition-projective-height-obstruction.md."""

from __future__ import annotations

import sympy as sp


def main():
    s, k0, k1, k2, localization = sp.symbols(
        "s kappa_0 kappa_1 kappa_2 localization"
    )
    c2, c4, c6, x, target = sp.symbols("C2 C4 C6 x target")

    normalized_c2 = c2 / s
    normalized_c4 = c4 / s
    normalized_c6 = c6 / s
    l2 = normalized_c2
    l4 = normalized_c4 - normalized_c2**2 / 2
    l6 = (
        normalized_c6
        - normalized_c2 * normalized_c4
        + normalized_c2**3 / 3
    )
    unnormalized = 6 * s**3 * (l6 + l4 * (x + l2))
    d_general = 6 * s**2 * (c6 + c4 * x)
    d_general -= 3 * s * c2**2 * x + c2**3
    assert sp.factor(unnormalized - d_general) == 0

    ghz_c6_plus_c4x = target - c2 * x**2 / 2 - s * x**3 / 6
    d_under_ghz = d_general.subs(c6, ghz_c6_plus_c4x - c4 * x)
    cube_form = 6 * s**2 * target - (s * x + c2) ** 3
    assert sp.expand(d_under_ghz - cube_form) == 0

    # Track only the independent pure tensors X_i and the common x^3
    # direction Z.  For C2=-s*x, the required square-free products are
    # C2*x^2=-s*Z, C2^2*x=s^2*Z, and C2^3=-s^3*Z.
    top_z_coefficient = sp.Rational(1, 3) - sp.Rational(1, 2)
    top_z_coefficient += sp.Rational(1, 6)
    assert top_z_coefficient == 0

    d_z_coefficient = 6 * s**2 * (s * sp.Rational(1, 3))
    d_z_coefficient -= 3 * s * (s**2)
    d_z_coefficient -= -s**3
    assert sp.expand(d_z_coefficient) == 0

    d_coordinates = (6 * s**2 * k0, 6 * s**2 * k1, 6 * s**2 * k2)
    h = s * k0 * k1 * k2

    # The explicit radical certificate h^2 in I_D.
    quotient = k0 * k1**2 * k2**2 / 6
    assert sp.expand(h**2 - quotient * d_coordinates[0]) == 0

    # Rabinowitsch localization: I_D + (1-t*h) is the unit ideal.
    basis = sp.groebner(
        (*d_coordinates, 1 - localization * h),
        localization,
        s,
        k0,
        k1,
        k2,
        order="lex",
        domain=sp.QQ,
    )
    assert basis.contains(sp.Integer(1))
    assert tuple(
        coordinate.subs({s: 1, k0: 1, k1: 1, k2: 1})
        for coordinate in d_coordinates
    ) == (6, 6, 6)

    # Dimension ledgers.  C2 has 15 physical pairs and 9 ordered cells.
    degree_two_coordinates = sp.binomial(6, 2) * 3**2
    assert degree_two_coordinates == 135
    bad_locus_codimension_bound = 1 + degree_two_coordinates
    assert bad_locus_codimension_bound == 136

    cap_dimension = 3**8
    bad_projective_dimension = cap_dimension - bad_locus_codimension_bound - 1
    krull_projective_dimension = cap_dimension - 1 - 729
    assert bad_projective_dimension == 6424
    assert krull_projective_dimension == 5831
    assert bad_projective_dimension > krull_projective_dimension

    print("top GHZ x^3 coefficient:", top_z_coefficient)
    print("D x^3 coefficient:", sp.expand(d_z_coefficient))
    print("D coordinate ideal:", d_coordinates)
    print("radical certificate h^2 multiplier:", quotient)
    print("localized Groebner basis contains 1:", basis.contains(sp.Integer(1)))
    print("degree-two boundary coordinates:", degree_two_coordinates)
    print("bad / Krull projective dimensions at |W|=8:",
          bad_projective_dimension, krull_projective_dimension)
    print("cap-condition projective-height obstruction: PASS")


if __name__ == "__main__":
    main()
