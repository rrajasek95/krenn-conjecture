#!/usr/bin/env python3
"""Independent exact audit of the complete DR4 endpoint package.

This file does not import any of the DR4 author checkers.  It reconstructs
the product-pairing endpoint matrix over QQ(a,b), keeps a homogeneous
cofactor kernel (so a chosen pivot is allowed to vanish), and isolates the
zero-dimensional residue left after removing the H divisor.  It also checks
the endpoint signs, scaling law, structural charts, and several direct
determinant stress instances.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, combinations_with_replacement

import sympy as sp
from sympy.polys.domains import QQ


A_SYMBOL, B_SYMBOL = sp.symbols("a b")
FIELD = QQ.frac_field("a", "b")
A, B = FIELD.gens
ANCHORS = (FIELD.one, A, B, A * B)
SUBSETS = tuple(
    subset
    for size in range(1, 5)
    for subset in combinations(range(4), size)
)
INDEX = {subset: position for position, subset in enumerate(SUBSETS)}


def endpoint_matrix() -> list[list]:
    """Sixteen linearized endpoint rows on the 15 monomial coordinates."""
    output = []
    for omitted, anchor_i in enumerate(ANCHORS):
        complement = tuple(index for index in range(4) if index != omitted)
        for sign in (1, -1):
            diagonal = {}
            for index in complement:
                node = ANCHORS[index]
                derivative_diagonal = sum(
                    (
                        1 / (node - ANCHORS[other])
                        for other in complement
                        if other != index
                    ),
                    FIELD.zero,
                )
                if sign == 1:
                    endpoint_shift = -2 / (node + anchor_i)
                else:
                    endpoint_shift = (
                        -1 / (node + anchor_i) - 1 / (node - anchor_i)
                    )
                diagonal[index] = derivative_diagonal + endpoint_shift

            coefficients = {tuple(complement): FIELD.one}
            for pair in combinations(complement, 2):
                remaining = next(index for index in complement if index not in pair)
                coefficients[pair] = diagonal[remaining]
            for index in complement:
                other_one, other_two = (
                    other for other in complement if other != index
                )
                coefficients[(index,)] = (
                    diagonal[other_one] * diagonal[other_two]
                    + 1 / (ANCHORS[other_one] - ANCHORS[other_two]) ** 2
                )
            output.append(
                [coefficients.get(subset, FIELD.zero) for subset in SUBSETS]
            )
            multiplied = {
                tuple(sorted((omitted,) + subset)): value
                for subset, value in coefficients.items()
            }
            output.append(
                [multiplied.get(subset, FIELD.zero) for subset in SUBSETS]
            )
    return output


def cofactor_kernel(rows: list[list], omitted_rows: tuple[int, int]):
    """Return Delta*k, the homogeneous cofactor vector of fourteen rows."""
    matrix = [
        row[:]
        for index, row in enumerate(rows)
        if index not in omitted_rows
    ]
    assert len(matrix) == 14 and len(matrix[0]) == 15
    pivot_row = 0
    pivots = []
    pivot_minor = FIELD.one
    sign = 1
    for column in range(15):
        selected = next(
            (
                row
                for row in range(pivot_row, 14)
                if matrix[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        if selected != pivot_row:
            matrix[pivot_row], matrix[selected] = (
                matrix[selected], matrix[pivot_row]
            )
            sign = -sign
        pivot = matrix[pivot_row][column]
        pivot_minor *= pivot
        matrix[pivot_row] = [entry / pivot for entry in matrix[pivot_row]]
        for row in range(14):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == 14:
            break
    assert pivots == list(range(14))
    normalized = [FIELD.zero] * 15
    normalized[14] = FIELD.one
    for row, column in reversed(tuple(enumerate(pivots))):
        normalized[column] = -sum(
            (
                matrix[row][later] * normalized[later]
                for later in range(column + 1, 15)
            ),
            FIELD.zero,
        )
    cofactor = [sign * pivot_minor * entry for entry in normalized]
    selected_rows = [
        row for index, row in enumerate(rows) if index not in omitted_rows
    ]
    for row in selected_rows:
        assert not sum(
            (entry * value for entry, value in zip(row, cofactor, strict=True)),
            FIELD.zero,
        )
    return cofactor


def toric_quadratic(vector: list, left: tuple[tuple[int, ...], tuple[int, ...]],
                    right: tuple[tuple[int, ...], tuple[int, ...]]):
    return (
        vector[INDEX[left[0]]] * vector[INDEX[left[1]]]
        - vector[INDEX[right[0]]] * vector[INDEX[right[1]]]
    )


def numerator_and_denominator(value):
    numerator, denominator = sp.together(value.as_expr()).as_numer_denom()
    return sp.factor(numerator), sp.factor(denominator)


def check_endpoint_reduction_and_scaling() -> None:
    """Derive both endpoint shifts directly from the original cubic row."""
    x, ti, tj, ui, z = sp.symbols("x ti tj U z", nonzero=True)
    r0, r1 = sp.symbols("r0 r1")
    # Only the value and derivative of r at tj are needed.
    q_value = (tj - ti) * r0
    q_derivative = r0 + (tj - ti) * r1
    original = (
        (x**2 - tj**2) * (q_derivative + ui * q_value)
        - (x - 3 * tj) * q_value
    )
    plus = sp.factor(original.subs(x, ti))
    minus = sp.factor(original.subs(x, -ti))
    expected_plus = -(
        (tj - ti) ** 2
        * (ti + tj)
        * (r1 + (ui - 2 / (ti + tj)) * r0)
    )
    expected_minus = -(
        (tj - ti) ** 2
        * (ti + tj)
        * (
            r1
            + (
                ui - 1 / (ti + tj) - 1 / (tj - ti)
            )
            * r0
        )
    )
    assert sp.factor(plus - expected_plus) == 0
    assert sp.factor(minus - expected_minus) == 0

    # Under t -> lambda*t and x -> lambda*x, q_tilde(z)=q(z/lambda)
    # and U_tilde=U/lambda make every cleared row scale by lambda.
    lam, qv, qd = sp.symbols("lambda qv qd", nonzero=True)
    old = (x**2 - ti**2) * (qd + ui * qv) - (x - 3 * ti) * qv
    scaled = (
        ((lam * x) ** 2 - (lam * ti) ** 2)
        * (qd / lam + ui / lam * qv)
        - (lam * x - 3 * lam * ti) * qv
    )
    assert sp.expand(scaled - lam * old) == 0

    # The normalized product-pairing chart has precisely these structural
    # factors: no anchor is zero, equal, or opposite.
    structural = (
        A_SYMBOL
        * B_SYMBOL
        * (A_SYMBOL**2 - 1)
        * (B_SYMBOL**2 - 1)
        * (A_SYMBOL**2 - B_SYMBOL**2)
        * (A_SYMBOL**2 * B_SYMBOL**2 - 1)
    )
    samples = [(2, 3), (2, 5), (3, -2)]
    for a_value, b_value in samples:
        anchors = (1, a_value, b_value, a_value * b_value)
        admissible = (
            all(value != 0 for value in anchors)
            and len(set(anchors)) == 4
            and all(
                anchors[i] + anchors[j] != 0
                for i in range(4)
                for j in range(i + 1, 4)
            )
        )
        assert bool(structural.subs({A_SYMBOL: a_value, B_SYMBOL: b_value})) == admissible


def check_h_nonzero_homogeneous_certificate() -> None:
    """Close the product chart away from H, including isolated points."""
    rows = endpoint_matrix()
    vector = cofactor_kernel(rows, (0, 2))
    # The raw fourteen-row cofactors have a common chart scale.  Remove it
    # before specializing; otherwise its zero divisor would make every raw
    # cofactor vanish even though the saturated kernel line persists.
    common_one = (
        A_SYMBOL**2 * B_SYMBOL
        + A_SYMBOL * B_SYMBOL**2
        + 2 * A_SYMBOL * B_SYMBOL
        + A_SYMBOL
        + B_SYMBOL
    )
    common_two = (
        A_SYMBOL**2 * B_SYMBOL
        - 3 * A_SYMBOL**2
        + A_SYMBOL * B_SYMBOL**2
        + 2 * A_SYMBOL * B_SYMBOL
        + A_SYMBOL
        - 3 * B_SYMBOL**2
        + B_SYMBOL
    )
    common_scale = FIELD.convert(common_one * common_two)
    vector = [entry / common_scale for entry in vector]

    # These are genuine homogeneous toric relations: both products have
    # the same total exponent vector in U_0,...,U_3.
    first = toric_quadratic(
        vector,
        ((1,), (2, 3)),
        ((2,), (1, 3)),
    )
    second = toric_quadratic(
        vector,
        ((0,), (1, 3)),
        ((3,), (0, 1)),
    )
    first_num, first_den = numerator_and_denominator(first)
    second_num, second_den = numerator_and_denominator(second)

    h = (A_SYMBOL + 1) ** 2 * (B_SYMBOL + 1) ** 2 - 16 * A_SYMBOL * B_SYMBOL
    structural = (
        A_SYMBOL
        * B_SYMBOL
        * (A_SYMBOL - 1)
        * (A_SYMBOL + 1)
        * (B_SYMBOL - 1)
        * (B_SYMBOL + 1)
        * (A_SYMBOL - B_SYMBOL)
        * (A_SYMBOL + B_SYMBOL)
        * (A_SYMBOL * B_SYMBOL - 1)
        * (A_SYMBOL * B_SYMBOL + 1)
    )
    # After saturation, every coordinate is regular throughout the
    # admissible product chart, and the fourteen selected rows still
    # annihilate it identically.
    for entry in vector:
        _, coordinate_denominator = numerator_and_denominator(entry)
        for factor, _ in sp.factor_list(coordinate_denominator)[1]:
            assert sp.rem(
                sp.Poly(structural, A_SYMBOL, B_SYMBOL),
                sp.Poly(factor, A_SYMBOL, B_SYMBOL),
            ).is_zero
    for index, row in enumerate(rows):
        if index in (0, 2):
            continue
        assert not sum(
            (entry * value for entry, value in zip(row, vector, strict=True)),
            FIELD.zero,
        )
    # The cofactor construction removes the nonstructural pivot divisor.
    # Its remaining denominators may only vanish on the structural chart
    # boundary.  The exact factor assertions below are filled with the
    # independently obtained quotients, rather than trusting a stored PASS.
    for denominator in (first_den, second_den):
        denominator_factors = sp.factor_list(denominator)[1]
        for factor, _ in denominator_factors:
            assert sp.rem(
                sp.Poly(structural, A_SYMBOL, B_SYMBOL),
                sp.Poly(factor, A_SYMBOL, B_SYMBOL),
            ).is_zero

    first_quotient = sp.factor(first_num / h)
    second_quotient = sp.factor(second_num / h)
    assert sp.denom(first_quotient) == 1
    assert sp.denom(second_quotient) == 1

    # Remove all explicitly structural factors.  Constants and powers are
    # immaterial; the two residual equations are recorded canonically.
    structural_irreducibles = {
        sp.factor(value)
        for value in (
            A_SYMBOL,
            B_SYMBOL,
            A_SYMBOL - 1,
            A_SYMBOL + 1,
            B_SYMBOL - 1,
            B_SYMBOL + 1,
            A_SYMBOL - B_SYMBOL,
            A_SYMBOL + B_SYMBOL,
            A_SYMBOL * B_SYMBOL - 1,
            A_SYMBOL * B_SYMBOL + 1,
        )
    }

    def nonstructural_part(expression):
        constant, factors = sp.factor_list(expression)
        answer = sp.Integer(constant)
        for factor, exponent in factors:
            if sp.factor(factor) not in structural_irreducibles:
                answer *= factor**exponent
        return sp.factor(answer)

    residual_one = nonstructural_part(first_quotient)
    residual_two = nonstructural_part(second_quotient)
    expected_one = -(
        A_SYMBOL**3 * B_SYMBOL**2
        + A_SYMBOL**3
        + A_SYMBOL**2 * B_SYMBOL**3
        + 12 * A_SYMBOL**2 * B_SYMBOL**2
        - 15 * A_SYMBOL**2 * B_SYMBOL
        - 15 * A_SYMBOL * B_SYMBOL**2
        + 12 * A_SYMBOL * B_SYMBOL
        + A_SYMBOL
        + B_SYMBOL**3
        + B_SYMBOL
    )
    expected_two = -(
        A_SYMBOL**3 * B_SYMBOL**3
        + A_SYMBOL**3 * B_SYMBOL
        - 15 * A_SYMBOL**2 * B_SYMBOL**2
        + 12 * A_SYMBOL**2 * B_SYMBOL
        + A_SYMBOL**2
        + A_SYMBOL * B_SYMBOL**3
        + 12 * A_SYMBOL * B_SYMBOL**2
        - 15 * A_SYMBOL * B_SYMBOL
        + B_SYMBOL**2
        + 1
    )
    assert sp.factor(residual_one / expected_one).is_number
    assert sp.factor(residual_two / expected_two).is_number
    residual_one = expected_one
    residual_two = expected_two

    resultant = sp.factor(
        sp.resultant(residual_one, residual_two, B_SYMBOL)
    )
    expected_resultant = (
        -576
        * A_SYMBOL**2
        * (A_SYMBOL - 1) ** 5
        * (A_SYMBOL + 1) ** 3
        * (A_SYMBOL**2 + 1) ** 2
        * (A_SYMBOL**2 + 14 * A_SYMBOL + 1)
    )
    assert sp.factor(resultant - expected_resultant) == 0

    # The only two nonstructural projected factors give b=0 and b=-1,
    # respectively.  Hence they are not admissible isolated exceptions.
    groebner_one = sp.groebner(
        [residual_one, residual_two, A_SYMBOL**2 + 1],
        B_SYMBOL,
        A_SYMBOL,
        order="lex",
    )
    groebner_two = sp.groebner(
        [residual_one, residual_two, A_SYMBOL**2 + 14 * A_SYMBOL + 1],
        B_SYMBOL,
        A_SYMBOL,
        order="lex",
    )
    assert [poly.as_expr() for poly in groebner_one.polys] == [
        B_SYMBOL,
        A_SYMBOL**2 + 1,
    ]
    assert [poly.as_expr() for poly in groebner_two.polys] == [
        B_SYMBOL + 1,
        A_SYMBOL**2 + 14 * A_SYMBOL + 1,
    ]


def direct_determinant(nodes, translations):
    x, z = sp.symbols("x z")
    basis = (sp.Integer(1), z, z**2, z**3)
    matrix = []
    for node, translation in zip(nodes, translations, strict=True):
        matrix.append(
            [
                sp.expand(
                    (x**2 - node**2)
                    * (sp.diff(q, z).subs(z, node) + translation * q.subs(z, node))
                    - (x - 3 * node) * q.subs(z, node)
                )
                for q in basis
            ]
        )
    return sp.Poly(sp.expand(sp.Matrix(matrix).det(method="domain-ge")), x)


def check_direct_stress() -> None:
    """Directly test the determinant and canonical U=0 kernel."""
    x, z = sp.symbols("x z")
    instances = [
        ((1, 2, 3, 6), (0, 0, 0, 0)),
        ((1, 2, 5, 10), (1, -2, 3, 4)),
        ((2, 3, 5, 7), (0, 0, 0, 0)),
    ]
    for nodes, translations in instances:
        determinant = direct_determinant(nodes, translations)
        if all(value == 0 for value in translations):
            assert determinant.as_expr() == 0
            gauge = (z - x) * (z + x) ** 2
            for node in nodes:
                row_value = (
                    (x**2 - node**2) * sp.diff(gauge, z).subs(z, node)
                    - (x - 3 * node) * gauge.subs(z, node)
                )
                assert sp.expand(row_value) == 0
        else:
            assert determinant.as_expr() != 0

    def numeric_endpoint_rows(nodes):
        output = []
        for omitted, anchor_i in enumerate(nodes):
            complement = tuple(index for index in range(4) if index != omitted)
            for sign in (1, -1):
                diagonal = {}
                for index in complement:
                    node = nodes[index]
                    derivative_diagonal = sum(
                        sp.Rational(1, node - nodes[other])
                        for other in complement
                        if other != index
                    )
                    shift = (
                        -sp.Rational(2, node + anchor_i)
                        if sign == 1
                        else -sp.Rational(1, node + anchor_i)
                        - sp.Rational(1, node - anchor_i)
                    )
                    diagonal[index] = derivative_diagonal + shift
                coefficients = {tuple(complement): sp.Integer(1)}
                for pair in combinations(complement, 2):
                    remaining = next(i for i in complement if i not in pair)
                    coefficients[pair] = diagonal[remaining]
                for index in complement:
                    one, two = (i for i in complement if i != index)
                    coefficients[(index,)] = (
                        diagonal[one] * diagonal[two]
                        + sp.Rational(1, (nodes[one] - nodes[two]) ** 2)
                    )
                output.append(
                    [coefficients.get(subset, sp.Integer(0)) for subset in SUBSETS]
                )
                multiplied = {
                    tuple(sorted((omitted,) + subset)): value
                    for subset, value in coefficients.items()
                }
                output.append(
                    [multiplied.get(subset, sp.Integer(0)) for subset in SUBSETS]
                )
        return sp.Matrix(output)

    generic_nodes = tuple(map(sp.Integer, (1, 2, 3, 5)))
    assert numeric_endpoint_rows(generic_nodes).rank() == 15

    symbolic_rows = endpoint_matrix()
    rank_instances = [
        # Product-pairing, H != 0.
        (sp.Rational(2), sp.Rational(3), 14),
        (sp.Rational(2), sp.Rational(5), 14),
        # Both conjugate points on H=0 at a=-4.
        (sp.Rational(-4), sp.Rational(-1, 9), 14),
        (sp.Rational(-4), sp.Rational(-9), 14),
    ]
    grouped_pairs = defaultdict(list)
    for first, second in combinations_with_replacement(range(15), 2):
        exponent = tuple(
            int(vertex in SUBSETS[first]) + int(vertex in SUBSETS[second])
            for vertex in range(4)
        )
        grouped_pairs[exponent].append((first, second))
    for a_value, b_value, expected_rank in rank_instances:
        matrix = sp.Matrix(
            [
                [
                    sp.cancel(
                        entry.as_expr().subs(
                            {A_SYMBOL: a_value, B_SYMBOL: b_value}
                        )
                    )
                    for entry in row
                ]
                for row in symbolic_rows
            ]
        )
        assert matrix.rank() == expected_rank
        if expected_rank == 14:
            kernel = matrix.nullspace()
            assert len(kernel) == 1
            vector = kernel[0]
            incompatible = False
            for pairs in grouped_pairs.values():
                if len(pairs) < 2:
                    continue
                baseline = pairs[0]
                for other in pairs[1:]:
                    relation = (
                        vector[baseline[0]] * vector[baseline[1]]
                        - vector[other[0]] * vector[other[1]]
                    )
                    if relation != 0:
                        incompatible = True
                        break
                if incompatible:
                    break
            assert incompatible


def main() -> None:
    check_endpoint_reduction_and_scaling()
    check_h_nonzero_homogeneous_certificate()
    check_direct_stress()
    print("independent full DR4 endpoint audit: PASS")
    print("H!=0 cofactor relations and isolated points: exact")
    print("endpoint signs, scaling, and product chart boundary: exact")


if __name__ == "__main__":
    main()
