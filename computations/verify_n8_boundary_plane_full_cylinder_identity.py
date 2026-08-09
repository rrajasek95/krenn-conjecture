#!/usr/bin/env python3
"""Coefficient-complete three-cylinder identity on the 15-variable plane."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product

import verify_n10_five_cross_occupied_modulus_incidence as incidence
import verify_n8_three_cut_exactness_tangent as tangent


Q = Fraction
VARIABLE_COUNT = 15
ZERO_MONOMIAL = (0,) * VARIABLE_COUNT


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def poly_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                answer.pop(monomial)
    return answer


def poly_scale(polynomial, scalar):
    return {
        monomial: Q(scalar) * coefficient
        for monomial, coefficient in polynomial.items()
        if Q(scalar) * coefficient
    }


def poly_multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_exponent + right_exponent
                for left_exponent, right_exponent in zip(left_monomial, right_monomial)
            )
            answer[monomial] = answer.get(monomial, Q(0)) + left_coefficient * right_coefficient
            if not answer[monomial]:
                answer.pop(monomial)
    return answer


def polynomial_matrix_multiply(left, right):
    return tuple(
        tuple(
            poly_add(
                *tuple(
                    poly_multiply(left[row][middle], right[middle][column])
                    for middle in range(len(right))
                )
            )
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def polynomial_matrix_add(left, right, right_scalar=Q(1)):
    return tuple(
        tuple(
            poly_add(left[row][column], poly_scale(right[row][column], right_scalar))
            for column in range(len(left[0]))
        )
        for row in range(len(left))
    )


def zero_polynomial_matrix(size):
    return tuple(tuple({} for _column in range(size)) for _row in range(size))


def identity_polynomial_matrix(size):
    return tuple(
        tuple(
            {ZERO_MONOMIAL: Q(1)} if row == column else {}
            for column in range(size)
        )
        for row in range(size)
    )


def sparse_difference(*terms):
    answer = {}
    for scalar, vector in terms:
        for key, value in vector.items():
            answer[key] = answer.get(key, Q(0)) + Q(scalar) * value
            if not answer[key]:
                answer.pop(key)
    return answer


def row_difference(*terms):
    words = set()
    for _scalar, rows in terms:
        words.update(rows)
    return {
        word: sparse_difference(
            *tuple((scalar, rows.get(word, {})) for scalar, rows in terms)
        )
        for word in words
        if sparse_difference(
            *tuple((scalar, rows.get(word, {})) for scalar, rows in terms)
        )
    }


def monomial_for(indices):
    indices = set(indices)
    return tuple(int(index in indices) for index in range(VARIABLE_COUNT))


def add_sparse_polynomial(target, monomial, vector):
    for row, coefficient in vector.items():
        polynomial = target.setdefault(row, {})
        polynomial[monomial] = polynomial.get(monomial, Q(0)) + coefficient
        if not polynomial[monomial]:
            polynomial.pop(monomial)
        if not polynomial:
            target.pop(row)


def add_row_polynomials(target, monomial, rows):
    for word, vector in rows.items():
        add_sparse_polynomial(target.setdefault(word, {}), monomial, vector)
        if not target[word]:
            target.pop(word)


def build_data():
    boundary_shear = tangent.load_boundary_shear()
    dependence = boundary_shear.load_dependence()
    quotient = dependence.load_quotient()
    cached = quotient.load_cached_blocks()
    matrix_cache = cached.load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    return dependence, bounded.prepare()


def main() -> None:
    dependence, data = build_data()
    module = data["module"]
    one_cell = data["one_cell"]
    unit_gate = one_cell.load_unit_gate()
    left = tuple(
        direction
        for direction in dependence.ADMISSIBLE_DIRECTIONS
        if direction[:2] == (2, 3)
    ) + (incidence.OCCUPIED_MODULUS,)
    right = tuple(
        direction
        for direction in dependence.ADMISSIBLE_DIRECTIONS
        if direction[:2] == (6, 7)
    )
    directions = left + right
    direction_index = {direction: index for index, direction in enumerate(directions)}
    require(len(directions) == VARIABLE_COUNT, "boundary-plane direction count changed")

    base = data["base"]
    single_cells = {
        direction: incidence.add_weighted_old_coordinates(
            module, base, ((direction, Q(1)),)
        )
        for direction in directions
    }
    pair_cells = {
        (left_direction, right_direction): incidence.add_weighted_old_coordinates(
            module,
            base,
            ((left_direction, Q(1)), (right_direction, Q(1))),
        )
        for left_direction in left
        for right_direction in right
    }

    base_tensor = module.matching_tensor(module.B, base)
    single_tensors = {
        direction: module.matching_tensor(module.B, cells)
        for direction, cells in single_cells.items()
    }
    pair_tensors = {
        pair: module.matching_tensor(module.B, cells)
        for pair, cells in pair_cells.items()
    }
    pure_polynomials = []
    for colour in range(3):
        word = (colour,) * 8
        polynomial = {ZERO_MONOMIAL: base_tensor.get(word, Q(0))}
        for direction in directions:
            coefficient = single_tensors[direction].get(word, Q(0)) - base_tensor.get(word, Q(0))
            if coefficient:
                polynomial[monomial_for((direction_index[direction],))] = coefficient
        for pair, tensor in pair_tensors.items():
            coefficient = (
                tensor.get(word, Q(0))
                - single_tensors[pair[0]].get(word, Q(0))
                - single_tensors[pair[1]].get(word, Q(0))
                + base_tensor.get(word, Q(0))
            )
            if coefficient:
                polynomial[monomial_for(tuple(direction_index[d] for d in pair))] = coefficient
        pure_polynomials.append(polynomial)
    require(
        pure_polynomials == [{ZERO_MONOMIAL: Q(1)}] * 3,
        "the boundary plane moved a pure anchor",
    )

    nilpotence_census = Counter()
    coefficient_census = Counter()
    for cut in unit_gate.THREE_CUTS:
        u_set = tuple(vertex for vertex in module.S if vertex != cut)
        c_set = (cut, 6, 7)

        def raw(cells):
            columns = one_cell.insertion_columns(module, u_set, cells)
            combined = module.flatten_rows(
                one_cell.residual_tensor(module, cells), c_set, u_set
            )
            one_rows = module.flatten_rows(
                module.sector(c_set, 1, cells), c_set, u_set
            )
            return columns, combined, one_rows

        base_columns, base_combined, base_one = raw(base)
        selected = tangent.independent_indices(module, base_columns)
        require(len(selected) == 14, f"cut-{cut} base cofactor rank changed")
        base_selected = tuple(base_columns[index] for index in selected)
        pivot_rows = tuple(sorted(module.rational_basis(list(base_selected))))
        require(len(pivot_rows) == 14, f"cut-{cut} pivot count changed")
        single_raw = {direction: raw(cells) for direction, cells in single_cells.items()}
        pair_raw = {pair: raw(cells) for pair, cells in pair_cells.items()}

        column_polynomials = [dict() for _index in selected]
        family_polynomials = ({}, {})
        for local_index, full_index in enumerate(selected):
            add_sparse_polynomial(
                column_polynomials[local_index], ZERO_MONOMIAL, base_columns[full_index]
            )
        add_row_polynomials(family_polynomials[0], ZERO_MONOMIAL, base_combined)
        add_row_polynomials(family_polynomials[1], ZERO_MONOMIAL, base_one)

        for direction in directions:
            monomial = monomial_for((direction_index[direction],))
            columns, combined, one_rows = single_raw[direction]
            for local_index, full_index in enumerate(selected):
                add_sparse_polynomial(
                    column_polynomials[local_index],
                    monomial,
                    sparse_difference((Q(1), columns[full_index]), (-Q(1), base_columns[full_index])),
                )
            add_row_polynomials(
                family_polynomials[0], monomial,
                row_difference((Q(1), combined), (-Q(1), base_combined)),
            )
            add_row_polynomials(
                family_polynomials[1], monomial,
                row_difference((Q(1), one_rows), (-Q(1), base_one)),
            )

        for pair in pair_cells:
            monomial = monomial_for(tuple(direction_index[d] for d in pair))
            columns, combined, one_rows = pair_raw[pair]
            left_columns, left_combined, left_one = single_raw[pair[0]]
            right_columns, right_combined, right_one = single_raw[pair[1]]
            for local_index, full_index in enumerate(selected):
                add_sparse_polynomial(
                    column_polynomials[local_index],
                    monomial,
                    sparse_difference(
                        (Q(1), columns[full_index]),
                        (-Q(1), left_columns[full_index]),
                        (-Q(1), right_columns[full_index]),
                        (Q(1), base_columns[full_index]),
                    ),
                )
            add_row_polynomials(
                family_polynomials[0], monomial,
                row_difference(
                    (Q(1), combined), (-Q(1), left_combined),
                    (-Q(1), right_combined), (Q(1), base_combined),
                ),
            )
            add_row_polynomials(
                family_polynomials[1], monomial,
                row_difference(
                    (Q(1), one_rows), (-Q(1), left_one),
                    (-Q(1), right_one), (Q(1), base_one),
                ),
            )

        matrix = tuple(
            tuple(column_polynomials[column].get(row, {}) for column in range(14))
            for row in pivot_rows
        )
        matrix0 = tuple(
            tuple(matrix[row][column].get(ZERO_MONOMIAL, Q(0)) for column in range(14))
            for row in range(14)
        )
        inverse0 = dependence.matrix_inverse(matrix0)
        difference = tuple(
            tuple(
                poly_add(
                    matrix[row][column],
                    {ZERO_MONOMIAL: -matrix0[row][column]} if matrix0[row][column] else {},
                )
                for column in range(14)
            )
            for row in range(14)
        )
        normalized = tuple(
            tuple(
                poly_add(
                    *tuple(poly_scale(difference[middle][column], inverse0[row][middle]) for middle in range(14))
                )
                for column in range(14)
            )
            for row in range(14)
        )
        power = normalized
        inverse_series = identity_polynomial_matrix(14)
        sign = -1
        nilpotence_index = None
        for exponent in range(1, 15):
            inverse_series = polynomial_matrix_add(
                inverse_series, power, Q(sign)
            )
            power = polynomial_matrix_multiply(power, normalized)
            if power == zero_polynomial_matrix(14):
                nilpotence_index = exponent + 1
                break
            sign = -sign
        require(nilpotence_index is not None, f"cut-{cut} moving frame is not nilpotent")
        nilpotence_census[nilpotence_index] += 1
        inverse0_polynomial = tuple(
            tuple(
                {ZERO_MONOMIAL: inverse0[row][column]} if inverse0[row][column] else {}
                for column in range(14)
            )
            for row in range(14)
        )
        inverse = polynomial_matrix_multiply(inverse_series, inverse0_polynomial)
        require(
            polynomial_matrix_multiply(matrix, inverse) == identity_polynomial_matrix(14),
            f"cut-{cut} polynomial frame inverse failed",
        )

        for family_index, rows in enumerate(family_polynomials):
            for boundary_word in product(range(3), repeat=3):
                row_polynomial = rows.get(boundary_word, {})
                pivot_vector = tuple(row_polynomial.get(row, {}) for row in pivot_rows)
                coefficients = tuple(
                    poly_add(
                        *tuple(
                            poly_multiply(inverse[column][row], pivot_vector[row])
                            for row in range(14)
                        )
                    )
                    for column in range(14)
                )
                ambient_rows = set(row_polynomial)
                for column in column_polynomials:
                    ambient_rows.update(column)
                for ambient_row in ambient_rows:
                    reconstructed = poly_add(
                        *tuple(
                            poly_multiply(
                                column_polynomials[column].get(ambient_row, {}),
                                coefficients[column],
                            )
                            for column in range(14)
                        )
                    )
                    require(
                        reconstructed == row_polynomial.get(ambient_row, {}),
                        f"cut-{cut} family-{family_index} word {boundary_word} left the moving cylinder",
                    )
                coefficient_census[(cut, family_index)] += sum(
                    len(polynomial) for polynomial in coefficients
                )

    require(
        nilpotence_census == Counter({2: 3}),
        "moving-frame nilpotence census changed",
    )
    require(
        coefficient_census
        == Counter(
            {
                (2, 0): 106,
                (2, 1): 108,
                (3, 0): 106,
                (3, 1): 108,
                (4, 0): 29,
                (4, 1): 27,
            }
        ),
        "moving-cylinder coefficient census changed",
    )

    print("N=8 15-variable boundary-plane full cylinder identity: PASS")
    print(f"directions: {len(directions)} = {len(left)} on 23 + {len(right)} on 67")
    print(f"pure anchors: {pure_polynomials}")
    print(f"moving-frame nilpotence census: {dict(sorted(nilpotence_census.items()))}")
    print(f"coefficient-solution term census: {dict(sorted(coefficient_census.items()))}")
    print("verdict: all affine/bilinear coefficients of both cylinder families vanish")


if __name__ == "__main__":
    main()
