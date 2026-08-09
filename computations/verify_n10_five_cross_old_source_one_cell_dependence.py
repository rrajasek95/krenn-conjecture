#!/usr/bin/env python3
"""Dependence of the 62 constant-row quotient jumps on old-source charts.

This is a localized, bounded old-source audit.  It uses the fourteen absent
one-cell directions already proved to preserve all three anchored N=8 cut
cylinders for every nonzero parameter.  For each direction it reconstructs
the 62 positive-degree quotient witnesses, proves which base matrices remain
support-rank deficient over Q[t], and computes a joint ideal of selected
augmented minors in Q[t].
"""

from __future__ import annotations

import importlib.util
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_quotient():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_constant_row_quotient_blocks_92_105.py"
    )
    spec = importlib.util.spec_from_file_location("quotient", path)
    require(spec is not None and spec.loader is not None, "cannot load quotient")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def trim(polynomial):
    answer = list(polynomial)
    while answer and not answer[-1]:
        answer.pop()
    return tuple(answer)


def poly_add(left, right):
    size = max(len(left), len(right))
    return trim(
        tuple(
            (left[index] if index < len(left) else Q(0))
            + (right[index] if index < len(right) else Q(0))
            for index in range(size)
        )
    )


def poly_scale(polynomial, scalar):
    return trim(tuple(Q(scalar) * coefficient for coefficient in polynomial))


def poly_multiply(left, right):
    if not left or not right:
        return ()
    answer = [Q(0)] * (len(left) + len(right) - 1)
    for left_index, left_coefficient in enumerate(left):
        for right_index, right_coefficient in enumerate(right):
            answer[left_index + right_index] += (
                left_coefficient * right_coefficient
            )
    return trim(answer)


def poly_divmod(dividend, divisor):
    dividend = list(trim(dividend))
    divisor = trim(divisor)
    require(divisor, "polynomial division by zero")
    if len(dividend) < len(divisor):
        return (), tuple(dividend)
    quotient = [Q(0)] * (len(dividend) - len(divisor) + 1)
    while dividend and len(dividend) >= len(divisor):
        shift = len(dividend) - len(divisor)
        coefficient = dividend[-1] / divisor[-1]
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            dividend[index + shift] -= coefficient * value
        dividend = list(trim(dividend))
    return trim(quotient), tuple(dividend)


def monic(polynomial):
    polynomial = trim(polynomial)
    return poly_scale(polynomial, Q(1) / polynomial[-1]) if polynomial else ()


def poly_gcd(left, right):
    left = trim(left)
    right = trim(right)
    while right:
        _quotient, remainder = poly_divmod(left, right)
        left, right = right, remainder
    return monic(left)


def interpolate_at_integers(values):
    """Return coefficients of the unique degree < len(values) polynomial."""
    answer = ()
    for index, value in enumerate(values):
        numerator = (Q(1),)
        denominator = Q(1)
        for other in range(len(values)):
            if other == index:
                continue
            numerator = poly_multiply(numerator, (-Q(other), Q(1)))
            denominator *= Q(index - other)
        answer = poly_add(answer, poly_scale(numerator, value / denominator))
    return trim(answer)


def determinant(matrix):
    size = len(matrix)
    rows = [list(map(Q, row)) for row in matrix]
    answer = Q(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if rows[row][column]), None
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            answer = -answer
        pivot_value = rows[column][column]
        answer *= pivot_value
        for row in range(column + 1, size):
            if not rows[row][column]:
                continue
            factor = rows[row][column] / pivot_value
            for index in range(column + 1, size):
                rows[row][index] -= factor * rows[column][index]
    return answer


def matrix_inverse(matrix):
    size = len(matrix)
    rows = [
        list(map(Q, row))
        + [Q(index == column) for column in range(size)]
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if rows[row][column]), None
        )
        require(pivot is not None, "selected augmented square became singular")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [value / scale for value in rows[column]]
        for row in range(size):
            if row == column or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                rows[row][index] - factor * rows[column][index]
                for index in range(2 * size)
            ]
    return tuple(tuple(row[size:]) for row in rows)


def matrix_multiply(left, right):
    return tuple(
        tuple(
            sum(
                left[row][middle] * right[middle][column]
                for middle in range(len(right))
            )
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def dense_rank(matrix):
    rows = [list(map(Q, row)) for row in matrix]
    row_index = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(row_index, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[row_index], rows[pivot] = rows[pivot], rows[row_index]
        scale = rows[row_index][column]
        rows[row_index] = [value / scale for value in rows[row_index]]
        for row in range(len(rows)):
            if row == row_index or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                rows[row][index] - factor * rows[row_index][index]
                for index in range(len(rows[0]))
            ]
        row_index += 1
    return row_index


def nilpotency_index(matrix):
    size = len(matrix)
    power = matrix
    for exponent in range(1, size + 1):
        if not any(value for row in power for value in row):
            return exponent
        power = matrix_multiply(power, matrix)
    return None


def determinant_polynomial(columns0, columns1, selected):
    size = len(columns0[0])
    require(len(selected) == size, "selected minor is not square")
    values = []
    for parameter in range(size + 1):
        matrix = [
            [
                columns0[column][row]
                + Q(parameter) * (columns1[column][row] - columns0[column][row])
                for column in selected
            ]
            for row in range(size)
        ]
        values.append(determinant(matrix))
    polynomial = interpolate_at_integers(values)
    require(polynomial and polynomial[0], "anchored augmented minor vanished")
    return polynomial


def independent_columns(module, columns):
    selected = []
    basis = {}
    for index, column in enumerate(columns):
        sparse_column = {
            row: value for row, value in enumerate(column) if value
        }
        candidate = module.rational_basis(
            list(basis.values()) + [sparse_column]
        )
        if len(candidate) > len(basis):
            selected.append(index)
            basis = candidate
    return tuple(selected)


def support_rank(columns):
    row_count = len(columns[0])
    adjacency = {
        column: tuple(
            row for row in range(row_count) if columns[column][row]
        )
        for column in range(len(columns))
    }
    matched_column = {}

    def augment(column, seen):
        for row in adjacency[column]:
            if row in seen:
                continue
            seen.add(row)
            if row not in matched_column or augment(matched_column[row], seen):
                matched_column[row] = column
                return True
        return False

    return sum(augment(column, set()) for column in adjacency)


def vector_columns_from_sparse_matrix(quotient, bounded, matrix):
    rows, columns, entries = matrix
    zero_monomial = (0, 0, 0, 0, 0)
    deleted = {
        row
        for row, _column, polynomial in entries
        if zero_monomial in polynomial
    }
    kept = tuple(row for row in range(rows) if row not in deleted)
    row_index = {row: index for index, row in enumerate(kept)}
    weights = tuple(map(bounded.Q, (1, 2, 3, 5, 7)))
    vectors = [[Q(0)] * len(kept) for _column in range(columns)]
    for row, column, polynomial in entries:
        if row not in row_index:
            continue
        vectors[column][row_index[row]] = quotient.evaluate_polynomial(
            bounded, polynomial, weights
        )
    return kept, tuple(tuple(vector) for vector in vectors)


def surviving_cases(
    quotient,
    cached,
    palette,
    five,
    four,
    matrix_cache,
    bounded,
    data,
    pair_survivors,
    right_coordinates,
):
    cases = defaultdict(list)
    for block in cached.ACTIVE_LIBRARY_BLOCKS:
        audit = palette.audit_pair_block(
            five,
            four,
            bounded,
            data,
            pair_survivors[block],
            right_coordinates,
        )
        exception_supports = {case[0] for case, _record in audit["exceptions"]}
        for case, determinant_record in audit["determinants"]:
            support = case[0]
            if support in exception_supports:
                continue
            _rank, bad, _base, augmented = matrix_cache.witness_matrices(
                bounded, data, support
            )
            winning_names = tuple(
                name
                for name, factors in determinant_record[3].items()
                if name.startswith("aug") and palette.torus_monomial(factors)
            )
            for name in winning_names:
                record, matching = quotient.constant_row_quotient_record(
                    bounded, data["module"], augmented[name]
                )
                if record[3] <= record[2]:
                    continue
                number = int(name[3:])
                word, remainder = sorted(bad.items())[number]
                labels, basis = bounded.independent_column_labels(
                    data["module"],
                    bounded.evaluated_columns(
                        data, support, tuple(map(Q, matrix_cache.SAMPLE))
                    ),
                )
                row_coordinates = tuple(sorted(basis)) + (min(remainder),)
                kept, columns0 = vector_columns_from_sparse_matrix(
                    quotient, bounded, augmented[name]
                )
                require(record[1] == len(kept), "kept-row count changed")
                selected = independent_columns(data["module"], columns0)
                require(
                    len(selected) == len(kept) and matching[1] == len(kept),
                    "anchored augmented rank changed",
                )
                cases[support].append(
                    {
                        "name": name,
                        "word": word,
                        "labels": labels,
                        "row_coordinates": row_coordinates,
                        "kept": kept,
                        "columns0": columns0,
                        "selected": selected,
                    }
                )
    require(sum(map(len, cases.values())) == 62, "surviving-witness count changed")
    require(len(cases) == 52, "surviving-case count changed")
    return cases


def add_old_coordinate(module, base, coordinate):
    cells = {edge: list(entries) for edge, entries in base.items()}
    module.add_sources(cells, ((*coordinate, Q(1)),))
    return cells


def changed_columns(data, support, metadata, old_cells, sample):
    module = data["module"]
    lifted = data["forced_pair"].lift_cells(module, old_cells)
    cells = data["provenance"].add_weighted_coordinates(
        module, lifted, tuple(zip(support, sample))
    )
    insertion = data["forced_pair"].insertion_columns(
        module, data["u_set"], cells
    )
    tensor = module.matching_tensor(data["provenance"].B10, cells)
    residual = data["forced_pair"].tensor_difference(
        tensor, data["forced_pair"].delta_tensor(data["provenance"].B10)
    )
    rows = data["forced_pair"].flatten_rows(
        residual,
        data["provenance"].B10,
        (2, 6, 7),
        data["u_set"],
    )
    answer = []
    for label in metadata["labels"]:
        vector = insertion[label]
        answer.append(
            tuple(
                vector.get(metadata["row_coordinates"][local_row], Q(0))
                for local_row in metadata["kept"]
            )
        )
    residual_vector = rows.get(metadata["word"], {})
    answer.append(
        tuple(
            residual_vector.get(metadata["row_coordinates"][local_row], Q(0))
            for local_row in metadata["kept"]
        )
    )
    return tuple(answer)


ADMISSIBLE_DIRECTIONS = (
    (2, 3, 0, 1),
    (2, 3, 0, 2),
    (2, 3, 1, 0),
    (2, 3, 1, 1),
    (2, 3, 1, 2),
    (2, 3, 2, 0),
    (2, 3, 2, 2),
    (6, 7, 0, 1),
    (6, 7, 0, 2),
    (6, 7, 1, 0),
    (6, 7, 1, 1),
    (6, 7, 2, 0),
    (6, 7, 2, 1),
    (6, 7, 2, 2),
)


def main() -> None:
    quotient = load_quotient()
    cached = quotient.load_cached_blocks()
    matrix_cache = cached.load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    module = data["module"]
    sample = tuple(map(Q, matrix_cache.SAMPLE))
    left_coordinates = tuple(
        coordinate for coordinate in data["coordinates"]
        if coordinate[1] == 8
    )
    right_coordinates = tuple(
        coordinate for coordinate in data["coordinates"]
        if coordinate[1] == 9
    )
    pair_survivors = five.universal_pair_survivors(
        data, left_coordinates, right_coordinates
    )
    cases = surviving_cases(
        quotient,
        cached,
        palette,
        five,
        four,
        matrix_cache,
        bounded,
        data,
        pair_survivors,
        right_coordinates,
    )

    one_cell = data["one_cell"]
    unit_gate = one_cell.load_unit_gate()
    independent, dependent = one_cell.classify_characters(module, data["base"])
    require(len(dependent) == 6, "dependent old-source chart count changed")
    observed_admissible = []
    for direction in independent:
        old_cells = add_old_coordinate(module, data["base"], direction)
        if all(
            unit_gate.active_complete(module.cut_record(cut, old_cells))
            for cut in unit_gate.THREE_CUTS
        ):
            observed_admissible.append(direction)
    require(
        tuple(observed_admissible) == ADMISSIBLE_DIRECTIONS,
        "admissible old-source chart list changed",
    )

    chart_records = []
    for direction in ADMISSIBLE_DIRECTIONS:
        old_cells = add_old_coordinate(module, data["base"], direction)
        robust = 0
        dependence_gcd = ()
        maximum_degree = 0
        changed_selected_entries = 0
        changed_quotient_entries = 0
        shear_census = Counter()
        for support, witnesses in cases.items():
            for metadata in witnesses:
                columns0 = metadata["columns0"]
                columns1 = changed_columns(
                    data, support, metadata, old_cells, sample
                )
                affine_support = tuple(
                    tuple(
                        columns0[column][row]
                        or columns1[column][row] - columns0[column][row]
                        for row in range(len(columns0[column]))
                    )
                    for column in range(len(columns0))
                )
                if support_rank(affine_support[:-1]) >= len(columns0[0]):
                    continue
                robust += 1
                changed_quotient_entries += sum(
                    columns0[column][row] != columns1[column][row]
                    for column in range(len(columns0))
                    for row in range(len(columns0[column]))
                )
                changed_selected_entries += sum(
                    columns0[column][row] != columns1[column][row]
                    for column in metadata["selected"]
                    for row in range(len(columns0[column]))
                )
                selected0 = tuple(
                    tuple(columns0[column][row] for column in metadata["selected"])
                    for row in range(len(columns0[0]))
                )
                selected_difference = tuple(
                    tuple(
                        columns1[column][row] - columns0[column][row]
                        for column in metadata["selected"]
                    )
                    for row in range(len(columns0[0]))
                )
                shear = matrix_multiply(
                    matrix_inverse(selected0), selected_difference
                )
                shear_record = (dense_rank(shear), nilpotency_index(shear))
                require(shear_record[1] is not None, "column shear is not nilpotent")
                shear_census[shear_record] += 1
                polynomial = determinant_polynomial(
                    columns0, columns1, metadata["selected"]
                )
                maximum_degree = max(maximum_degree, len(polynomial) - 1)
                dependence_gcd = (
                    polynomial
                    if not dependence_gcd
                    else poly_gcd(dependence_gcd, polynomial)
                )
        require(robust, f"no robust quotient witness on chart {direction}")
        chart_records.append(
            (
                direction,
                robust,
                maximum_degree,
                monic(dependence_gcd),
                changed_selected_entries,
                changed_quotient_entries,
                tuple(sorted(shear_census.items())),
            )
        )

    require(
        all(record[3] == (Q(1),) for record in chart_records),
        "a nonunit joint dependence ideal appeared",
    )
    require(
        tuple((record[4], record[5]) for record in chart_records)
        == (
            (0, 0), (0, 0), (0, 0), (2, 2), (0, 0),
            (0, 0), (0, 0), (8, 8), (0, 0), (0, 0),
            (35, 35), (0, 0), (10, 10), (0, 0),
        ),
        "changed-entry census changed",
    )
    require(
        tuple(record[6] for record in chart_records)
        == (
            (((0, 1), 62),),
            (((0, 1), 62),),
            (((0, 1), 62),),
            (((0, 1), 60), ((1, 2), 2)),
            (((0, 1), 62),),
            (((0, 1), 62),),
            (((0, 1), 62),),
            (((0, 1), 58), ((1, 2), 4)),
            (((0, 1), 62),),
            (((0, 1), 62),),
            (((0, 1), 38), ((1, 2), 24)),
            (((0, 1), 62),),
            (((0, 1), 56), ((1, 2), 6)),
            (((0, 1), 62),),
        ),
        "column-shear palette changed",
    )
    print("N=10 quotient old-source one-cell dependence: exact frontier")
    print("positive-degree quotient witnesses/cases: 62/52")
    print("admissible arbitrary-weight old-source charts: 14")
    print(
        "robust witnesses per chart: "
        + str(tuple(record[1] for record in chart_records))
    )
    print(
        "maximum selected-minor degrees: "
        + str(tuple(record[2] for record in chart_records))
    )
    print(
        "changed selected/full quotient entries: "
        + str(tuple((record[4], record[5]) for record in chart_records))
    )
    print(
        "column-shear rank/nilpotency censuses: "
        + str(tuple(record[6] for record in chart_records))
    )
    print("joint localized dependence ideals: 14/14 unit")
    print("scope: anchored one-cell old-source charts at one exact cross torus point")
    print("arbitrary-old-source identity certified: 0")


if __name__ == "__main__":
    main()
