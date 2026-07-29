#!/usr/bin/env python3
"""Exact audits for the uniform dense cyclic cofactor-plane obstruction.

The cubic Bianchi tensor on a cyclic character line has four orbit
equations.  Their radical is a three-line scheme with offset profiles
(r,1,0,-1,-r), where r(2r^2+3r+3)=0.  A diagonal cyclic action is then
killed by one quartic (or the terminal equation at r=0).  If cyclic
rotation swaps the two contact axes, diagonalizing that action gives two
character profiles; one mixed cubic forces their r parameters to agree,
collapsing the local cofactor plane to a line.
"""

from __future__ import annotations

from itertools import product

import sympy as sp

from verify_uniform_dense_cyclic_contact_obstruction import (
    EDGES,
    MATCHINGS,
    REPRESENTATIVES,
    VERTICES,
    cyclic_binary_equations,
)


def audit_cyclic_cubic_radical():
    variables, equations, _ = cyclic_binary_equations()
    x1, x2, x3, x4 = variables
    cubics = [
        equation
        for equation in equations
        if sp.Poly(equation, *variables).total_degree() == 3
    ]
    assert [REPRESENTATIVES[index] for index in (0, 1, 2, 4)] == [
        representative
        for representative, equation in zip(REPRESENTATIVES, equations)
        if sp.Poly(equation, *variables).total_degree() == 3
    ]

    profile_polynomial = x1 * (
        2 * x1**2 + 3 * x1 * x2 + 3 * x2**2
    )
    radical_generators = (x3, x2 + x4, profile_polynomial)

    # I is contained in J: all four cubic equations vanish on the claimed
    # three projective character directions.
    radical_basis = sp.groebner(
        radical_generators, *variables, order="grevlex", domain=sp.QQ
    )
    assert all(radical_basis.reduce(equation)[1] == 0 for equation in cubics)

    # Conversely, powers of every generator of J lie in I.  Since the last
    # generator is squarefree in Q[x1,x2], J itself is radical.
    cubic_basis = sp.groebner(
        cubics, *variables, order="grevlex", domain=sp.QQ
    )
    power_certificate = (x3**7, (x2 + x4) ** 7, profile_polynomial**3)
    assert all(cubic_basis.reduce(value)[1] == 0 for value in power_certificate)

    r = sp.symbols("r")
    quadratic = 2 * r**2 + 3 * r + 3
    assert sp.discriminant(quadratic, r) == -15
    assert sp.gcd(sp.Poly(r, r), sp.Poly(quadratic, r)) == 1

    # A nonzero point of J must have x2 != 0 and hence normalizes to
    # (r,1,0,-1), with fifth offset -r.
    origin_with_x2_zero = sp.groebner(
        radical_generators + (x2,), *variables, order="grevlex", domain=sp.QQ
    )
    for variable in variables:
        assert origin_with_x2_zero.reduce(variable**3)[1] == 0

    return variables, equations


def audit_diagonal_character_exit(variables, equations) -> None:
    r = sp.symbols("r")
    substitution = dict(zip(variables, (r, 1, 0, -1)))
    restricted = [sp.factor(equation.subs(substitution)) for equation in equations]
    profile_equation = r * (2 * r**2 + 3 * r + 3)
    assert restricted[1] == profile_equation / 3
    assert restricted[5] == 4 * r**3 * (r + 6) / 9

    # The nonzero cubic roots cannot pass the quartic equation.
    assert sp.gcd(
        sp.Poly(2 * r**2 + 3 * r + 3, r), sp.Poly(r + 6, r)
    ) == 1

    # At the remaining cubic root r=0, the unshifted terminal coefficient is
    # zero (the stored equation is coefficient minus 15).
    assert restricted[-1].subs(r, 0) == -15


def audit_swapped_character_mixed_cubic() -> None:
    r, t, amplitude_u, amplitude_v, character = sp.symbols("r t A B lambda")
    offsets_u = (None, r, 1, 0, -1, -r)
    offsets_v = (None, t, 1, 0, -1, -t)

    first = {1: {}, 2: {}}
    for i in VERTICES:
        for j in VERTICES:
            if i == j:
                continue
            offset = (j - i) % 6
            first[1][i, j] = amplitude_u * character**i * offsets_u[offset]
            first[2][i, j] = (
                amplitude_v * (-character) ** i * offsets_v[offset]
            )
    assert all(
        sp.expand(sum(first[color][i, j] for j in VERTICES if j != i)) == 0
        for color in (1, 2)
        for i in VERTICES
    )

    second = {}
    for left, right in product((1, 2), repeat=2):
        for i, k in EDGES:
            second[left, right, i, k] = sp.expand(
                -sum(
                    first[left][i, j] * first[right][k, ell]
                    for j in VERTICES
                    if j not in (i, k)
                    for ell in VERTICES
                    if ell not in (i, k, j)
                )
                / 3
            )

    cells = {}
    for i, j in EDGES:
        cells[i, j, 0, 0] = sp.Integer(1)
        for color in (1, 2):
            cells[i, j, color, 0] = first[color][i, j]
            cells[i, j, 0, color] = first[color][j, i]
        for left, right in product((1, 2), repeat=2):
            cells[i, j, left, right] = second[left, right, i, j]

    coloring = (1, 1, 2, 0, 0, 0)
    coefficient = sp.factor(
        sum(
            sp.prod(cells[i, j, coloring[i], coloring[j]] for i, j in matching)
            for matching in MATCHINGS
        )
    )
    assert coefficient == (
        -sp.Rational(2, 3)
        * amplitude_u**2
        * amplitude_v
        * character**3
        * (r - t)
    )


def main() -> None:
    variables, equations = audit_cyclic_cubic_radical()
    audit_diagonal_character_exit(variables, equations)
    audit_swapped_character_mixed_cubic()
    print(
        "cyclic cubic radical: three antisymmetric projective profiles "
        "(power certificates 7,7,3)"
    )
    print("diagonal cyclic action: quartic/terminal obstruction: PASS")
    print("swapped cyclic action: one mixed cubic forces plane rank one: PASS")


if __name__ == "__main__":
    main()
