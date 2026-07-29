#!/usr/bin/env python3
"""Exact obstruction to a cyclic binary contact at the uniform n=6 point.

Work dimensionlessly with C_ij = 1.  Its hafnian is 15, every pair
cofactor is 3, and every four-deletion cofactor is 1.  A cyclic directed
first jet fixed by translation is therefore determined by offsets
x_1,...,x_5 with sum zero.  The pair equations determine the second lift.
This script enumerates the resulting binary matching tensor and proves that
its nine remaining orbit equations generate the unit ideal over Q.  It also
checks every one-dimensional cyclic character, including the nontrivial
sixth roots of unity, by exact cyclotomic Groebner reduction.

Besides asking SymPy for the reduced Groebner basis, the script runs a
small extended Buchberger calculation and checks the resulting explicit
identity 1 = sum_i q_i f_i exactly.  It also audits two hand-readable
reflection subcharts quoted in the accompanying note.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations, product

import sympy as sp


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
REPRESENTATIVES = (
    (0, 0, 0, 1, 1, 1),
    (0, 0, 1, 0, 1, 1),
    (0, 0, 1, 1, 0, 1),
    (0, 0, 1, 1, 1, 1),
    (0, 1, 0, 1, 0, 1),
    (0, 1, 0, 1, 1, 1),
    (0, 1, 1, 0, 1, 1),
    (0, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1),
)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, partner),) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))


def character_binary_coefficients(character):
    """Build all coefficients for b_(i,i+d) = character**i x_d."""

    variables = sp.symbols("x1 x2 x3 x4")
    x1, x2, x3, x4 = variables
    offsets = (None, x1, x2, x3, x4, -x1 - x2 - x3 - x4)

    first = {
        (i, j): character**i * offsets[(j - i) % 6]
        for i in VERTICES
        for j in VERTICES
        if i != j
    }
    assert all(sp.expand(sum(first[i, j] for j in VERTICES if j != i)) == 0
               for i in VERTICES)

    # h_ik=3 and h_ikjl=1 at the uniform dimensionless point.
    second = {}
    for i, k in EDGES:
        numerator = sum(
            first[i, j] * first[k, ell]
            for j in VERTICES
            if j not in (i, k)
            for ell in VERTICES
            if ell not in (i, k, j)
        )
        second[i, k] = sp.expand(-numerator / 3)

    cells = {}
    for i, j in EDGES:
        cells[i, j, 0, 0] = sp.Integer(1)
        cells[i, j, 1, 0] = first[i, j]
        cells[i, j, 0, 1] = first[j, i]
        cells[i, j, 1, 1] = second[i, j]

    def coefficient(coloring):
        return sp.expand(
            sum(
                sp.prod(cells[i, j, coloring[i], coloring[j]] for i, j in matching)
                for matching in MATCHINGS
            )
        )

    coefficients = {
        coloring: coefficient(coloring)
        for coloring in product((0, 1), repeat=6)
    }

    # The leading, tangent, and pair equations are automatic by construction.
    assert coefficients[(0,) * 6] == 15
    assert all(
        value == 0
        for coloring, value in coefficients.items()
        if sum(coloring) in (1, 2)
    )
    return variables, coefficients


def cyclic_binary_equations():
    """Return the fixed-character nine orbit equations and coefficients."""

    variables, coefficients = character_binary_coefficients(sp.Integer(1))

    equations = []
    for coloring in REPRESENTATIVES:
        target = 15 if coloring == (1,) * 6 else 0
        equations.append(sp.expand(coefficients[coloring] - target))

    # Rotation gives exactly the displayed nine nontrivial coefficient orbits.
    def rotations(word):
        return {word[shift:] + word[:shift] for shift in range(6)}

    covered = set()
    for representative, equation in zip(REPRESENTATIVES, equations):
        for coloring in rotations(representative):
            target = 15 if coloring == (1,) * 6 else 0
            assert sp.expand(coefficients[coloring] - target - equation) == 0
            covered.add(coloring)
    assert covered == {
        coloring for coloring in product((0, 1), repeat=6) if sum(coloring) >= 3
    }
    assert tuple(sp.Poly(f, *variables).total_degree() for f in equations) == (
        3, 3, 3, 4, 3, 4, 4, 5, 6
    )
    return variables, equations, coefficients


def monomial_expression(monomial, variables):
    return sp.prod(variable**exponent for variable, exponent in zip(variables, monomial))


def divides(left, right):
    """Whether monomial ``left`` divides monomial ``right``."""

    return all(a <= b for a, b in zip(left, right))


def quotient_monomial(numerator, denominator):
    return tuple(a - b for a, b in zip(numerator, denominator))


def lcm_monomial(left, right):
    return tuple(max(a, b) for a, b in zip(left, right))


def leading_term(poly):
    return poly.terms(order="grevlex")[0]


def extended_unit_certificate(equations, variables):
    """Run deterministic extended Buchberger and return a unit certificate.

    Each basis element is carried together with its expression in the nine
    input equations.  Reduction scans terms in descending grevlex order and
    uses the first available basis divisor.  The routine stops as soon as it
    creates a nonzero constant.
    """

    zero = sp.Poly(0, *variables, domain=sp.QQ)
    one = sp.Poly(1, *variables, domain=sp.QQ)

    basis = [sp.Poly(f, *variables, domain=sp.QQ) for f in equations]
    representations = []
    for index in range(len(equations)):
        row = [zero for _ in equations]
        row[index] = one
        representations.append(row)

    pairs = deque(combinations(range(len(basis)), 2))
    pair_steps = 0
    while pairs:
        i, j = pairs.popleft()
        pair_steps += 1
        lm_i, lc_i = leading_term(basis[i])
        lm_j, lc_j = leading_term(basis[j])
        common = lcm_monomial(lm_i, lm_j)
        multiplier_i = sp.Poly(
            monomial_expression(quotient_monomial(common, lm_i), variables) / lc_i,
            *variables,
            domain=sp.QQ,
        )
        multiplier_j = sp.Poly(
            monomial_expression(quotient_monomial(common, lm_j), variables) / lc_j,
            *variables,
            domain=sp.QQ,
        )
        remainder = multiplier_i * basis[i] - multiplier_j * basis[j]
        representation = [
            multiplier_i * representations[i][index]
            - multiplier_j * representations[j][index]
            for index in range(len(equations))
        ]

        # Fully reduce every divisible term, even if an unreducible leading
        # term is already present.  The tracked identity is preserved exactly.
        while remainder:
            reduction = None
            for monomial, coefficient in remainder.terms(order="grevlex"):
                for basis_index, divisor in enumerate(basis):
                    divisor_monomial, divisor_coefficient = leading_term(divisor)
                    if divides(divisor_monomial, monomial):
                        multiplier = sp.Poly(
                            coefficient
                            * monomial_expression(
                                quotient_monomial(monomial, divisor_monomial), variables
                            )
                            / divisor_coefficient,
                            *variables,
                            domain=sp.QQ,
                        )
                        reduction = (basis_index, multiplier)
                        break
                if reduction is not None:
                    break
            if reduction is None:
                break
            basis_index, multiplier = reduction
            remainder -= multiplier * basis[basis_index]
            representation = [
                value - multiplier * source
                for value, source in zip(
                    representation, representations[basis_index]
                )
            ]

        if not remainder:
            continue

        _, leading_coefficient = leading_term(remainder)
        inverse_leading_coefficient = sp.QQ(1) / leading_coefficient
        remainder = remainder.mul_ground(inverse_leading_coefficient)
        representation = [
            value.mul_ground(inverse_leading_coefficient)
            for value in representation
        ]

        # Directly verify the invariant before extending the basis.
        reconstructed = sum(
            (multiplier * source for multiplier, source in zip(representation, equations)),
            zero,
        )
        assert reconstructed == remainder

        if remainder.total_degree() == 0:
            assert remainder == one
            return representation, pair_steps

        new_index = len(basis)
        pairs.extend((old_index, new_index) for old_index in range(new_index))
        basis.append(remainder)
        representations.append(representation)

    raise AssertionError("Buchberger calculation did not produce a unit")


def audit_all_cyclic_characters() -> None:
    """Exclude b_(i+1,j+1)=zeta b_(i,j) for every zeta**6=1."""

    character = sp.symbols("z")
    variables, coefficients = character_binary_coefficients(character)
    equations = [
        value - (15 if coloring == (1,) * 6 else 0)
        for coloring, value in coefficients.items()
        if sum(coloring) >= 3
    ]

    # Phi_2.  Phi_1 is the fixed-character calculation in main().
    minus_one_equations = [sp.expand(f.subs(character, -1)) for f in equations]
    minus_one_basis = sp.groebner(
        minus_one_equations, *variables, order="grevlex", domain=sp.QQ
    )
    assert list(minus_one_basis.polys) == [
        sp.Poly(1, *variables, domain=sp.QQ)
    ]

    # Phi_3 and Phi_6 cover the two conjugate primitive roots in each case.
    for cyclotomic in (
        character**2 + character + 1,
        character**2 - character + 1,
    ):
        reduced_equations = [
            sp.rem(
                sp.Poly(f, character), sp.Poly(cyclotomic, character)
            ).as_expr()
            for f in equations
        ]
        basis = sp.groebner(
            reduced_equations + [cyclotomic],
            *variables,
            character,
            order="grevlex",
            domain=sp.QQ,
        )
        assert list(basis.polys) == [
            sp.Poly(1, *variables, character, domain=sp.QQ)
        ]


def audit_reflection_subcharts(equations, variables) -> None:
    x1, x2, x3, x4 = variables
    a, b = sp.symbols("a b")

    # Antisymmetric offsets (a,b,0,-b,-a).
    antisymmetric = {x1: a, x2: b, x3: 0, x4: -b}
    restricted = [sp.factor(f.subs(antisymmetric)) for f in equations]
    expected_cubic = a * (2 * a**2 + 3 * a * b + 3 * b**2) / 3
    expected_quartic = 4 * a**3 * (a + 6 * b) / 9
    expected_terminal = (8 * a**6 - 24 * a**4 * b**2 - 96 * a**3 * b**3 - 405) / 27
    assert any(sp.expand(f - expected_cubic) == 0 for f in restricted)
    assert any(sp.expand(f - expected_quartic) == 0 for f in restricted)
    assert sp.expand(restricted[-1] - expected_terminal) == 0

    # Reflection-symmetric offsets (a,b,-2a-2b,b,a).  Two cubics already
    # have resultant -750 b^9; their only common affine zero is the origin.
    symmetric = {x1: a, x2: b, x3: -2 * a - 2 * b, x4: b}
    restricted = [sp.factor(f.subs(symmetric)) for f in equations]
    f = 4 * a**3 + 13 * a**2 * b + 7 * a * b**2 + 6 * b**3
    g = 3 * a**3 + 6 * a**2 * b + 4 * a * b**2 + 2 * b**3
    selected = []
    for candidate in restricted:
        for expected in (f, g):
            quotient = sp.cancel(candidate / expected)
            if quotient.is_Rational and quotient:
                selected.append(expected)
    assert set(selected) == {f, g}
    assert sp.factor(sp.resultant(f, g, a)) == -750 * b**9


def main() -> None:
    variables, equations, _ = cyclic_binary_equations()

    reduced = sp.groebner(equations, *variables, order="grevlex", domain=sp.QQ)
    assert list(reduced.polys) == [sp.Poly(1, *variables, domain=sp.QQ)]

    certificate, pair_steps = extended_unit_certificate(equations, variables)
    zero = sp.Poly(0, *variables, domain=sp.QQ)
    one = sp.Poly(1, *variables, domain=sp.QQ)
    reconstructed = sum(
        (multiplier * source for multiplier, source in zip(certificate, equations)),
        zero,
    )
    assert reconstructed == one
    term_counts = tuple(len(multiplier.terms()) for multiplier in certificate)
    degrees = tuple(multiplier.total_degree() for multiplier in certificate)

    audit_reflection_subcharts(equations, variables)
    audit_all_cyclic_characters()

    print("uniform n=6 cyclic binary-contact ideal: <1> over Q")
    print(
        f"extended certificate: {pair_steps} S-pairs, "
        f"{sum(term_counts)} multiplier terms"
    )
    print(f"multiplier term counts: {term_counts}")
    print(f"multiplier degrees: {degrees}")
    print("all four cyclotomic character cases zeta^6=1: unit ideals")
    print("antisymmetric and reflection-symmetric hand subcharts: PASS")


if __name__ == "__main__":
    main()
