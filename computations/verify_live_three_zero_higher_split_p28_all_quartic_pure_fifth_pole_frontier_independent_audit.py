#!/usr/bin/env python3
"""Independent audit of the p=28 all-quartic pure-fifth-pole frontier.

This checker does not import the primary checker.  It reconstructs the
confluent jet systems, builds independently chosen exact sections of the
seven-dimensional fifth-power system, audits the selected-row relation
criterion (including its local principal-part content), and checks all
role and dimension bookkeeping.
"""

from __future__ import annotations

import math

import sympy as sp


z = sp.symbols("z")

QUARTIC_NODES = tuple(range(1, 8))
REPEATED_POLES = (8, 9)
COMMON_POLE = 10

B = sp.prod(z - a for a in QUARTIC_NODES)
COFACTORS = tuple(sp.cancel(B / (z - a)) for a in QUARTIC_NODES)
FIFTH_SECTIONS = tuple(sp.expand(cofactor**5) for cofactor in COFACTORS)
B4 = sp.expand(B**4)

MODELED_PAIRS = (
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 2),
)


def order_at(poly: sp.Expr, point: int) -> int:
    """Return the exact order of a nonzero polynomial at ``point``."""
    polynomial = sp.Poly(poly, z)
    order = 0
    while polynomial.eval(point) == 0:
        polynomial = sp.Poly(polynomial.diff(), z)
        order += 1
    return order


def conditions(d: int, k: int) -> tuple[tuple[int, int], ...]:
    rows = [(COMMON_POLE, derivative) for derivative in range(k)]
    for point in REPEATED_POLES[:d]:
        rows.extend(((point, 0), (point, 1)))
    return tuple(rows)


def confluent_matrix(d: int, k: int) -> sp.Matrix:
    return sp.Matrix([
        [sp.diff(section, z, derivative).subs(z, point)
         for section in FIFTH_SECTIONS]
        for point, derivative in conditions(d, k)
    ])


def candidate_vectors(nullspace: list[sp.Matrix]):
    """Yield a generic deterministic sequence, different from the source audit."""
    dimension = len(nullspace)
    for parameter in range(1, 25):
        patterns = (
            tuple(parameter ** index for index in range(dimension)),
            tuple(parameter + index + 1 for index in range(dimension)),
            tuple((-parameter) ** index for index in range(dimension)),
        )
        for pattern in patterns:
            yield sum(
                (coefficient * vector
                 for coefficient, vector in zip(pattern, nullspace)),
                sp.zeros(7, 1),
            )


def exact_section(d: int, k: int) -> tuple[sp.Matrix, sp.Expr, sp.Expr, sp.Expr]:
    """Build a monic structurally separated section of the jet kernel."""
    matrix = confluent_matrix(d, k)
    nullspace = matrix.nullspace()
    assert len(nullspace) == 7 - k - 2 * d

    repeated = sp.prod(z - point for point in REPEATED_POLES[:d])
    forced = (z - COMMON_POLE) ** k * repeated**2

    for raw_vector in candidate_vectors(nullspace):
        if any(entry == 0 for entry in raw_vector):
            continue
        raw_section = sp.expand(sum(
            raw_vector[index] * FIFTH_SECTIONS[index]
            for index in range(7)
        ))
        leading = sp.LC(sp.Poly(raw_section, z))
        if leading == 0:
            continue
        coefficients = sp.Matrix([sp.cancel(entry / leading)
                                  for entry in raw_vector])
        section = sp.Poly(sp.expand(raw_section / leading), z)
        quotient = sp.cancel(section.as_expr() / forced)
        if sp.denom(quotient) != 1:
            continue
        singleton = sp.Poly(quotient, z)
        expected_degree = 30 - k - 2 * d
        if section.degree() != 30 or singleton.degree() != expected_degree:
            continue
        if sp.LC(singleton) != 1:
            continue
        if order_at(section.as_expr(), COMMON_POLE) != k:
            continue
        if any(order_at(section.as_expr(), point) != 2
               for point in REPEATED_POLES[:d]):
            continue
        if sp.gcd(singleton, singleton.diff()).degree() != 0:
            continue
        reflected = sp.Poly(singleton.as_expr().subs(z, -z), z)
        if sp.gcd(singleton, reflected).degree() != 0:
            continue
        forbidden = QUARTIC_NODES + REPEATED_POLES[:d] + (COMMON_POLE,)
        if any(singleton.eval(sign * point) == 0
               for point in forbidden for sign in (-1, 1)):
            continue
        return coefficients, section.as_expr(), repeated, singleton.as_expr()

    raise AssertionError(f"no independent exact model for d={d}, k={k}")


def relation_numerator(
    coefficients: sp.Matrix,
    section: sp.Expr,
    k: int,
) -> sp.Expr:
    """Integrate the pure fifth-pole expansion and normalize at z=10."""
    numerator_before_normalization = 0
    for index, a in enumerate(QUARTIC_NODES):
        for derivative in range(4):
            jet = sp.diff(section, z, derivative).subs(z, a)
            antiderivative_coefficient = sp.cancel(
                jet / (math.factorial(derivative) * (derivative - 4))
            )
            numerator_before_normalization += (
                coefficients[index]
                * antiderivative_coefficient
                * (z - a) ** derivative
                * COFACTORS[index] ** 4
            )

    raw = sp.Poly(sp.expand(numerator_before_normalization), z)
    value = sp.cancel(raw.eval(COMMON_POLE) / B4.subs(z, COMMON_POLE))
    normalized = sp.Poly(sp.expand(raw.as_expr() - value * B4), z)
    divisor = sp.Poly((z - COMMON_POLE) ** (k + 1), z)
    return sp.exquo(normalized, divisor).as_expr()


def operator(numerator: sp.Expr, k: int) -> sp.Expr:
    return sp.expand(
        B * ((z - COMMON_POLE) * sp.diff(numerator, z)
             + (k + 1) * numerator)
        - 4 * (z - COMMON_POLE) * sp.diff(B, z) * numerator
    )


def audit_local_pure_poles(coefficients: sp.Matrix, section: sp.Expr) -> None:
    """Check the four missing lower Laurent coefficients independently."""
    reconstructed = sp.expand(sum(
        coefficients[index] * FIFTH_SECTIONS[index]
        for index in range(7)
    ))
    assert sp.Poly(section - reconstructed, z).is_zero

    for index, a in enumerate(QUARTIC_NODES):
        cofactor = COFACTORS[index]
        local_coefficient = sp.cancel(
            section.subs(z, a) / cofactor.subs(z, a) ** 5
        )
        assert local_coefficient == coefficients[index]
        assert local_coefficient != 0

        # Congruence modulo (z-a)^5 is exactly the assertion that the
        # Laurent expansion of F/B^5 has no orders -4,-3,-2,-1.
        remainder = sp.rem(
            sp.Poly(section - local_coefficient * cofactor**5, z),
            sp.Poly((z - a) ** 5, z),
        )
        assert remainder.is_zero


def audit_row_relation_reconstruction(
    d: int,
    k: int,
    coefficients: sp.Matrix,
    section: sp.Expr,
    repeated: sp.Expr,
    singleton: sp.Expr,
) -> None:
    """Check polynomial primitives, local templates, moments, and q=6."""
    h = 28 - k
    selected_singletons = h + 2 - 2 * d
    selected_rows = h + 2 - d
    ambient_degree = h + 3 - d
    Q = sp.Poly(repeated, z)
    H = sp.Poly(singleton, z)
    selected_denominator = sp.Poly(Q.as_expr() ** 3 * H.as_expr() ** 2, z)
    contact_factor = sp.Poly(Q.as_expr() ** 2 * H.as_expr(), z)

    assert H.degree() == selected_singletons
    assert selected_denominator.degree() == 2 * h + 4 - d
    assert contact_factor.degree() == h + 2

    numerators: list[sp.Expr] = []
    image_sections: list[sp.Expr] = []
    for degree in range(4):
        target = z**degree
        numerator = relation_numerator(coefficients, target, k)
        image = operator(numerator, k)
        expected = sp.expand(contact_factor.as_expr() * target)
        assert sp.Poly(image - expected, z).is_zero
        assert sp.degree(numerator, z) <= h - 1

        # Moment cancellation: N/(Q^3 H^2)=O(z^(-D-2)).  These are exactly
        # the D+1 vanishing Laurent moments defining a selected-row
        # relation, rather than merely a solution of a differential ODE.
        infinity_gap = selected_denominator.degree() - sp.degree(numerator, z)
        assert infinity_gap >= ambient_degree + 2

        # The quotient G=(z-10)^(k+1)N/B^4 is locally constant through
        # order three at a repeated pole.  Hence multiplying Omega by G
        # only rescales its entire order-three principal part there.
        g_numerator = sp.expand((z - COMMON_POLE) ** (k + 1) * numerator)
        for point in REPEATED_POLES[:d]:
            scalar = sp.cancel(
                g_numerator.subs(z, point) / B4.subs(z, point)
            )
            local_difference_numerator = sp.Poly(
                sp.expand(g_numerator - scalar * B4), z
            )
            assert sp.rem(
                local_difference_numerator,
                sp.Poly((z - point) ** 3, z),
            ).is_zero

        # At every (possibly algebraic) singleton pole alpha, G' has an H
        # factor.  Since H is squarefree and disjoint from B(z)(z-10),
        # G-G(alpha)=O((z-alpha)^2), which rescales the complete order-two
        # principal part.  This collective remainder test covers all roots.
        assert sp.rem(sp.Poly(image, z), H).is_zero
        assert sp.rem(sp.Poly(image, z), sp.Poly(Q.as_expr() ** 2, z)).is_zero

        numerators.append(numerator)
        image_sections.append(sp.exquo(sp.Poly(image, z), contact_factor).as_expr())

    numerator_matrix = sp.Matrix([
        [sp.Poly(numerator, z).coeff_monomial(z**power)
         for power in range(h)]
        for numerator in numerators
    ])
    image_matrix = sp.Matrix([
        [sp.Poly(image, z).coeff_monomial(z**power)
         for power in range(4)]
        for image in image_sections
    ])
    assert numerator_matrix.rank() == image_matrix.rank() == 4

    # The relation map has target P_3 and zero kernel: E(N)=0 would make
    # (z-10)^(k+1)N/B^4 constant, and evaluation at z=10 kills it.  Thus
    # the four displayed relations are the complete relation space.
    relation_dimension = 4
    row_rank = selected_rows - relation_dimension
    selected_kernel_dimension = ambient_degree + 1 - row_rank
    assert selected_kernel_dimension == 6

    q6_gap = 6 * 6 - 2 * 6 - h - 2 + max(0, 6 - k)
    q7_gap = 7 * 7 - 2 * 7 - h - 2 + max(0, 7 - k)
    assert q6_gap == 0
    assert q7_gap == 12


def audit_bookkeeping_and_fixed_node_ranks() -> None:
    residual_tuples = {
        0: (7, 0, 0, 2),
        1: (7, 0, 1, 0),
        2: (7, 0, 2, -2),
    }
    recovered_models: list[tuple[int, int]] = []

    for d in range(3):
        e, triples, doubles, u = residual_tuples[d]
        assert (e, triples, doubles, u) == (7, 0, d, 2 - 2 * d)
        assert 4 * e + 3 * triples + 2 * doubles + u == 30

        for k in range(1, 7):
            h = 28 - k
            available_singletons = h + u
            required_singletons = h + 2 - 2 * d
            assert available_singletons == required_singletons
            assert 4 * e + 2 * doubles + available_singletons == h + 30

            legal_double_counts = tuple(
                chosen for chosen in range(d + 1)
                if h + 2 - 2 * chosen <= available_singletons
            )
            assert legal_double_counts == (d,)

            matrix = confluent_matrix(d, k)
            expected_rank = min(7, k + 2 * d)
            assert matrix.rank() == expected_rank
            if matrix.rank() < 7:
                recovered_models.append((d, k))

    assert tuple(recovered_models) == MODELED_PAIRS


def main() -> None:
    audit_bookkeeping_and_fixed_node_ranks()

    audited: list[tuple[int, int]] = []
    for d, k in MODELED_PAIRS:
        coefficients, section, repeated, singleton = exact_section(d, k)
        audit_local_pure_poles(coefficients, section)
        audit_row_relation_reconstruction(
            d, k, coefficients, section, repeated, singleton
        )
        audited.append((d, k))

    assert tuple(audited) == MODELED_PAIRS
    print("p=28 all-quartic pure-fifth-pole independent audit: PASS")
    print("exact separated selected-row q=6 models:", audited)
    print("principal-part reconstruction and moment cancellation: exact")
    print("scope guard: formal selected rows only; no tensor realization")


if __name__ == "__main__":
    main()
