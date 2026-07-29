#!/usr/bin/env python3
"""Construct exact algebraic weights from a toric-binomial survivor.

The search's quotient-product test proves existence.  This module turns that
existence into explicit weights.  Smith coordinates split the mixed Laurent
solution set into finitely many torsion components and a free torus.  On each
component, an injective mixed-radix substitution sends all free variables to
integer powers of one positive integer.  Exact cyclotomic reduction finds a
component and specialization where all three pure sums are nonzero.

Each returned aggregate-cell weight has the form ``zeta**r * base**p``.
Dividing every selected cell incident with vertex zero and endpoint colour
``a`` by the corresponding pure sum ``C_a`` then normalizes all three pure
coefficients to one.  Every mixed coefficient retains its common factor and
remains zero.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import lcm, prod

from sympy import Poly, Symbol, cyclotomic_poly
from sympy.polys.domains import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp


X = Symbol("X")


def integer_entries(matrix):
    return [
        [int(matrix[i, j].element) for j in range(matrix.shape[1])]
        for i in range(matrix.shape[0])
    ]


def smith_coordinates(rows, number_variables):
    """Return diagonal data for ``U D V=S`` and the transformed half-RHS."""

    if not rows:
        return (), (), [
            [int(i == j) for j in range(number_variables)]
            for i in range(number_variables)
        ], 0
    matrix = DomainMatrix.from_list([list(row) for row in rows], ZZ)
    diagonal, left, right = smith_normal_decomp(matrix)
    s = integer_entries(diagonal)
    u = integer_entries(left)
    v = integer_entries(right)
    rank = 0
    for i in range(min(len(rows), number_variables)):
        if s[i][i]:
            rank += 1
    assert all(
        not s[i][i]
        for i in range(rank, min(len(rows), number_variables))
    )
    twice_rhs = tuple(sum(u_row) for u_row in u)
    for i in range(rank, len(rows)):
        assert twice_rhs[i] % 2 == 0
    return tuple(s[i][i] for i in range(rank)), twice_rhs, v, rank


def transform_exponent(exponent, right):
    """Transform ``x``-monomial exponents after ``x_j=prod z_i^V[j,i]``."""

    return tuple(
        sum(exponent[row] * right[row][column]
            for row in range(len(exponent)))
        for column in range(len(exponent))
    )


def mixed_radices(transformed_families, rank, number_variables):
    """Choose an injective univariate encoding of all free exponent vectors."""

    free = number_variables - rank
    if not free:
        return ()
    vectors = [
        exponent[rank:]
        for family in transformed_families
        for exponent in family
    ]
    minima = [min(vector[i] for vector in vectors) for i in range(free)]
    maxima = [max(vector[i] for vector in vectors) for i in range(free)]
    radices = []
    multiplier = 1
    for low, high in zip(minima, maxima):
        radices.append(multiplier)
        multiplier *= high - low + 1

    # The offset contributed by the minima is common, so standard mixed-radix
    # uniqueness applies even though the original exponents may be negative.
    for family in transformed_families:
        encodings = [
            sum(exponent[rank + i] * radices[i] for i in range(free))
            for exponent in family
        ]
        assert len(set(encodings)) == len({exponent[rank:] for exponent in family})
    return tuple(radices)


def cyclotomic_sum_is_zero(order, coefficients, cyclotomic):
    """Decide ``sum coefficients[r] zeta^r == 0`` exactly."""

    polynomial = Poly.from_dict(
        {
            (exponent % order,): coefficient
            for exponent, coefficient in coefficients.items()
            if coefficient
        },
        (X,),
        domain=ZZ,
    )
    return polynomial.rem(cyclotomic).is_zero


def exact_toric_specialization(
    rows,
    monomial_families,
    *,
    max_torsion_components=1_000_000,
):
    """Find ``zeta**r * base**p`` variables satisfying rows and nonzero sums.

    ``monomial_families`` is a sequence of Laurent polynomials, each given as
    a sequence of exponent vectors with coefficient one.  The return value is
    ``(root_order, base, root_exponents, integer_powers, family_terms)``.
    The last item lists ``(root exponent, integer power)`` for every monomial.
    """

    number_variables = len(rows[0]) if rows else len(monomial_families[0][0])
    diagonal, twice_rhs, right, rank = smith_coordinates(rows, number_variables)
    transformed_families = tuple(
        tuple(transform_exponent(exponent, right) for exponent in family)
        for family in monomial_families
    )
    radices = mixed_radices(
        transformed_families, rank, number_variables
    )

    moduli = tuple(abs(value) for value in diagonal)
    component_count = prod(moduli)
    if component_count > max_torsion_components:
        raise RuntimeError(
            f"torsion component count {component_count} exceeds exact limit "
            f"{max_torsion_components}"
        )
    root_order = 2
    for modulus in moduli:
        root_order = lcm(root_order, 2 * modulus)
    cyclotomic = Poly(cyclotomic_poly(root_order, X), X, domain=ZZ)

    chosen_internal = None
    chosen_transformed_terms = None
    for branch in product(*(range(modulus) for modulus in moduli)):
        internal = [0] * number_variables
        for i, (diagonal_entry, branch_value) in enumerate(
            zip(diagonal, branch)
        ):
            phase = (
                Fraction(twice_rhs[i], 2) + branch_value
            ) / diagonal_entry
            internal[i] = int(phase * root_order) % root_order

        transformed_terms = []
        all_nonzero_as_polynomials = True
        for family in transformed_families:
            terms = []
            coefficients_by_power = defaultdict(lambda: defaultdict(int))
            for exponent in family:
                root_exponent = sum(
                    exponent[i] * internal[i] for i in range(rank)
                ) % root_order
                integer_power = sum(
                    exponent[rank + i] * radices[i]
                    for i in range(number_variables - rank)
                )
                terms.append((root_exponent, integer_power))
                coefficients_by_power[integer_power][root_exponent] += 1
            if all(
                cyclotomic_sum_is_zero(
                    root_order, coefficients, cyclotomic
                )
                for coefficients in coefficients_by_power.values()
            ):
                all_nonzero_as_polynomials = False
                break
            transformed_terms.append(tuple(terms))
        if all_nonzero_as_polynomials:
            chosen_internal = tuple(internal)
            chosen_transformed_terms = tuple(transformed_terms)
            break

    if chosen_internal is None:
        raise AssertionError(
            "every torsion component kills a family; quotient product is zero"
        )

    base = 2
    while True:
        all_nonzero = True
        for terms in chosen_transformed_terms:
            minimum = min(power for _root, power in terms)
            coefficients = defaultdict(int)
            for root_exponent, integer_power in terms:
                coefficients[root_exponent] += base ** (integer_power - minimum)
            if cyclotomic_sum_is_zero(
                root_order, coefficients, cyclotomic
            ):
                all_nonzero = False
                break
        if all_nonzero:
            break
        base += 1

    internal_powers = [0] * rank + list(radices)
    root_exponents = tuple(
        sum(right[row][i] * chosen_internal[i] for i in range(rank))
        % root_order
        for row in range(number_variables)
    )
    integer_powers = tuple(
        sum(right[row][i] * internal_powers[i]
            for i in range(number_variables))
        for row in range(number_variables)
    )

    for row in rows:
        assert sum(a * b for a, b in zip(row, integer_powers)) == 0
        assert (
            sum(a * b for a, b in zip(row, root_exponents)) % root_order
            == root_order // 2
        )

    family_terms = tuple(
        tuple(
            (
                sum(a * b for a, b in zip(exponent, root_exponents))
                % root_order,
                sum(a * b for a, b in zip(exponent, integer_powers)),
            )
            for exponent in family
        )
        for family in monomial_families
    )
    assert family_terms == chosen_transformed_terms
    return (
        root_order,
        base,
        root_exponents,
        integer_powers,
        family_terms,
    )


def n8_exact_witness(search, selected, fibres, rows):
    """Project an n=8 survivor and return a fully checked exact witness."""

    active = tuple(sorted(selected))
    active_index = {cell: index for index, cell in enumerate(active)}
    projected_rows = [
        [row[search.cell_index[cell]] for cell in active]
        for row in rows
    ]

    pure_decorated = tuple(
        tuple(decorated for _matching_number, decorated in fibres[(colour,) * 8])
        for colour in range(3)
    )
    monomial_families = []
    for family in pure_decorated:
        exponents = []
        for decorated in family:
            exponent = [0] * len(active)
            for cell in decorated:
                exponent[active_index[cell]] += 1
            exponents.append(tuple(exponent))
        monomial_families.append(tuple(exponents))

    result = exact_toric_specialization(projected_rows, monomial_families)
    order, base, root_exponents, integer_powers, pure_terms = result
    cell_roots = dict(zip(active, root_exponents))
    cell_powers = dict(zip(active, integer_powers))

    # Exhaustively audit every one of the 3^8 coefficient fibres.  Mixed
    # pairs must agree in the integer part and differ by exactly -1 in the
    # root-of-unity part.
    for colouring in product(range(3), repeat=8):
        terms = fibres.get(colouring, ())
        for _matching_number, decorated in terms:
            vertex_zero_colors = []
            for u, v, a, b in decorated:
                if u == 0:
                    vertex_zero_colors.append(a)
                elif v == 0:
                    vertex_zero_colors.append(b)
            # Every perfect matching has exactly one edge at vertex zero.
            # Dividing its cell by C_{coloring[0]} therefore multiplies every
            # term in this coefficient by the same normalization factor.
            assert vertex_zero_colors == [colouring[0]]
        values = [
            (
                sum(cell_roots[cell] for cell in decorated) % order,
                sum(cell_powers[cell] for cell in decorated),
            )
            for _matching_number, decorated in terms
        ]
        if len(set(colouring)) == 1:
            assert values == list(pure_terms[colouring[0]])
        else:
            assert len(values) in (0, 2)
            if values:
                assert values[0][1] == values[1][1]
                assert (values[0][0] - values[1][0]) % order == order // 2

    return {
        "root_order": order,
        "integer_base": base,
        "cell_root_exponents": cell_roots,
        "cell_integer_powers": cell_powers,
        "pure_terms": pure_terms,
    }
