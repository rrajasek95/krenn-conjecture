#!/usr/bin/env python3
"""Exact audit of the p=28 all-quartic pure-fifth-pole frontier.

The audit constructs formal selected-row models for the three residual
all-quartic tuples.  It deliberately does not assert a collision-profile
realization of the original tensor equations.
"""

from __future__ import annotations

import math

import sympy as sp


z = sp.symbols("z")

COMPLEMENT = tuple(range(1, 8))
REPEATED_POLES = (8, 9)
COMMON_POLE = 10
MU = -COMMON_POLE

B = sp.prod(z - a for a in COMPLEMENT)
ELL = tuple(sp.expand(B / (z - a)) for a in COMPLEMENT)
FIFTH_BASIS = tuple(sp.expand(ell**5) for ell in ELL)


def valuation(poly: sp.Expr, point: int) -> int:
    """Exact order of a nonzero polynomial at a rational point."""
    order = 0
    while sp.diff(poly, z, order).subs(z, point) == 0:
        order += 1
    return order


def primitive_integer_vector(vector: sp.Matrix) -> sp.Matrix:
    denominator = sp.ilcm(*(sp.denom(entry) for entry in vector))
    integral = sp.Matrix([sp.expand(denominator * entry) for entry in vector])
    divisor = sp.gcd_list(list(integral))
    return sp.Matrix([entry / divisor for entry in integral])


def jet_conditions(d: int, k: int) -> tuple[tuple[int, int], ...]:
    conditions = [(COMMON_POLE, order) for order in range(k)]
    for point in REPEATED_POLES[:d]:
        conditions.extend(((point, 0), (point, 1)))
    return tuple(conditions)


def jet_matrix(d: int, k: int) -> sp.Matrix:
    return sp.Matrix(
        [
            [sp.diff(section, z, order).subs(z, point)
             for section in FIFTH_BASIS]
            for point, order in jet_conditions(d, k)
        ]
    )


def structural_model(
    d: int, k: int
) -> tuple[sp.Matrix, sp.Expr, sp.Expr, sp.Expr]:
    """Choose a deterministic exact separated member of the jet kernel."""
    matrix = jet_matrix(d, k)
    assert matrix.rank() == k + 2 * d
    nullspace = matrix.nullspace()
    assert len(nullspace) == 7 - k - 2 * d

    dimension = len(nullspace)
    combinations: list[tuple[int, ...]] = [
        tuple(int(i == j) for i in range(dimension))
        for j in range(dimension)
    ]
    combinations.extend(
        [
            (1,) * dimension,
            tuple(range(1, dimension + 1)),
            tuple((-1) ** i for i in range(dimension)),
        ]
    )

    for combination in combinations:
        vector = sum(
            (coefficient * basis_vector
             for coefficient, basis_vector in zip(combination, nullspace)),
            sp.zeros(7, 1),
        )
        vector = primitive_integer_vector(vector)
        if any(entry == 0 for entry in vector):
            continue

        numerator = sp.expand(
            sum(vector[i] * FIFTH_BASIS[i] for i in range(7))
        )
        repeated = sp.prod(z - point for point in REPEATED_POLES[:d])
        quotient = sp.cancel(
            numerator / ((z - COMMON_POLE) ** k * repeated**2)
        )
        if sp.denom(quotient) != 1:
            continue
        singleton = sp.Poly(quotient, z)
        if singleton.degree() != 30 - k - 2 * d:
            continue
        if singleton.eval(COMMON_POLE) == 0:
            continue
        if any(singleton.eval(point) == 0
               for point in REPEATED_POLES[:d]):
            continue
        if sp.gcd(singleton, singleton.diff()).degree() != 0:
            continue
        reflected = sp.Poly(singleton.as_expr().subs(z, -z), z)
        if sp.gcd(singleton, reflected).degree() != 0:
            continue
        forbidden = COMPLEMENT + REPEATED_POLES + (COMMON_POLE,)
        if any(singleton.eval(point) == 0 or singleton.eval(-point) == 0
               for point in forbidden):
            continue
        return vector, numerator, repeated, singleton.as_expr()

    raise AssertionError(f"no deterministic model found for d={d}, k={k}")


def primitive_numerator(
    coefficients: sp.Matrix,
    section: sp.Expr,
    k: int,
) -> sp.Expr:
    """Construct N from the residue-free rational primitive.

    If R=sum_i c_i/(z-a_i)^5, integrate R*section term by term.  The
    primitive is normalized to vanish at COMMON_POLE.  Its zero there has
    order k+1, so division gives the relation numerator N.
    """
    primitive_times_b4 = 0
    for i, a in enumerate(COMPLEMENT):
        for order in range(4):
            jet = sp.diff(section, z, order).subs(z, a)
            coefficient = jet / (math.factorial(order) * (order - 4))
            primitive_times_b4 += (
                coefficients[i]
                * coefficient
                * (z - a) ** order
                * ELL[i] ** 4
            )

    primitive_times_b4 = sp.Poly(sp.expand(primitive_times_b4), z)
    constant = sp.cancel(
        primitive_times_b4.eval(COMMON_POLE) / B.subs(z, COMMON_POLE) ** 4
    )
    normalized = sp.Poly(
        sp.expand(primitive_times_b4.as_expr() - constant * B**4), z
    )
    divisor = sp.Poly((z - COMMON_POLE) ** (k + 1), z)
    return sp.exquo(normalized, divisor).as_expr()


def audit_model(d: int, k: int) -> None:
    coefficients, numerator, repeated, singleton = structural_model(d, k)
    h = 28 - k
    selected_singletons = h + 2 - 2 * d

    # In 4^7 2^d 1^(h+2-2d), every available double is forced into role
    # two: using x doubles would require h+2-2x singletons.
    legal_double_counts = tuple(
        x for x in range(d + 1)
        if h + 2 - 2 * x <= selected_singletons
    )
    assert legal_double_counts == (d,)

    assert sp.degree(B, z) == 7
    assert all(sp.degree(ell, z) == 6 for ell in ELL)
    assert sp.Matrix(
        [[section.subs(z, a) for section in FIFTH_BASIS]
         for a in COMPLEMENT]
    ).rank() == 7
    assert sp.degree(numerator, z) == 30
    assert sp.degree(singleton, z) == selected_singletons
    assert valuation(numerator, COMMON_POLE) == k
    assert all(valuation(numerator, point) == 2
               for point in REPEATED_POLES[:d])
    assert sp.expand(
        numerator
        - (z - COMMON_POLE) ** k * repeated**2 * singleton
    ) == 0

    # F/B^5 has one pure fifth-order partial fraction at each quartic
    # complement node.  Equivalently the local unit is constant through
    # order four.
    for i, a in enumerate(COMPLEMENT):
        remainder = sp.rem(
            sp.Poly(numerator - coefficients[i] * ELL[i] ** 5, z),
            sp.Poly((z - a) ** 5, z),
        )
        assert remainder.is_zero
        assert ELL[i].subs(z, a) != 0

    # The singleton factor has exactly the structural separations needed
    # for its roots to define distinct, pairwise nonopposite selected
    # singleton values, disjoint from all fixed values and the common pole.
    singleton_poly = sp.Poly(singleton, z)
    assert singleton_poly.eval(0) != 0
    assert sp.gcd(singleton_poly, singleton_poly.diff()).degree() == 0
    assert sp.gcd(
        singleton_poly,
        sp.Poly(singleton.subs(z, -z), z),
    ).degree() == 0
    for point in COMPLEMENT + REPEATED_POLES[:d] + (COMMON_POLE,):
        assert singleton_poly.eval(point) != 0
        assert singleton_poly.eval(-point) != 0

    # Four independent cubics give four exact relation numerators.
    relation_numerators = []
    for degree in range(4):
        section = z**degree
        relation = primitive_numerator(coefficients, section, k)
        assert sp.degree(relation, z) <= h - 1
        operator = sp.expand(
            B * ((z - COMMON_POLE) * sp.diff(relation, z)
                 + (k + 1) * relation)
            - 4 * (z - COMMON_POLE) * sp.diff(B, z) * relation
        )
        assert sp.Poly(
            sp.expand(operator - repeated**2 * singleton * section), z
        ).is_zero
        relation_numerators.append(relation)

    # Their images are Q^2 H times 1,z,z^2,z^3, hence independence is
    # immediate from injectivity of the displayed differential operator.
    assert len(relation_numerators) == 4

    # The general selected-row bound gives q<=6, while four row relations
    # give q>=6.  The displayed arithmetic checks the exact dimensions.
    layers = h + 2 - d
    ambient_degree = h + 3 - d
    relation_dimension = 4
    row_rank = layers - relation_dimension
    kernel_dimension = ambient_degree + 1 - row_rank
    assert kernel_dimension == 6
    selected_gap_six = 6 * 6 - 2 * 6 - h - 2 + max(0, 6 - k)
    selected_gap_seven = 7 * 7 - 2 * 7 - h - 2 + max(0, 7 - k)
    assert selected_gap_six == 0
    assert selected_gap_seven == 12


def main() -> None:
    audited: list[tuple[int, int]] = []
    for d in range(3):
        for k in range(1, 7 - 2 * d):
            audit_model(d, k)
            audited.append((d, k))

    assert audited == [
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
        (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 1), (2, 2),
    ]

    # At the same fixed rational nodes, the unmodelled loads already have
    # full column rank.  This is only a generic-osculation frontier, not a
    # nonexistence claim when the nodes themselves are allowed to vary.
    for d, first_unmodelled in ((1, 5), (2, 3)):
        for k in range(first_unmodelled, 7):
            assert jet_matrix(d, k).rank() == 7

    print("p=28 all-quartic pure-fifth-pole frontier: PASS")
    print("exact formal q=6 models:", audited)
    print("four primitive relation numerators per model: exact")
    print("scope: selected-row frontier, not a tensor realization")


if __name__ == "__main__":
    main()
