#!/usr/bin/env python3
"""Constant-row quotient and pair-block closure through block 105."""

from __future__ import annotations

import importlib.util
import math
from collections import Counter
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_cached_blocks():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_cached_blocks_78_91.py"
    )
    spec = importlib.util.spec_from_file_location("cached_blocks", path)
    require(spec is not None and spec.loader is not None, "cannot load cache")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate_polynomial(bounded, polynomial, weights):
    return sum(
        coefficient
        * math.prod(
            weight ** exponent
            for weight, exponent in zip(weights, monomial)
        )
        for monomial, coefficient in polynomial.items()
    )


def support_rank(rows, columns, entries, kept_rows, column_limit):
    """Maximum matching rank of a sparse polynomial matrix support."""
    adjacency = {
        column: tuple(
            row
            for row in kept_rows
            if any(
                candidate_row == row
                and candidate_column == column
                and polynomial
                for candidate_row, candidate_column, polynomial in entries
            )
        )
        for column in range(min(columns, column_limit))
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

    rank = 0
    for column in adjacency:
        if augment(column, set()):
            rank += 1
    return rank


def constant_row_quotient_record(bounded, module, matrix):
    rows, columns, entries = matrix
    zero_monomial = (0, 0, 0, 0, 0)
    deleted_rows = {
        row
        for row, _column, polynomial in entries
        if zero_monomial in polynomial
    }
    kept_rows = tuple(row for row in range(rows) if row not in deleted_rows)
    row_index = {row: index for index, row in enumerate(kept_rows)}
    weights = tuple(map(bounded.Q, (1, 2, 3, 5, 7)))
    evaluated_columns = []
    for column in range(columns):
        vector = {}
        for row, candidate_column, polynomial in entries:
            if candidate_column != column or row not in row_index:
                continue
            value = evaluate_polynomial(bounded, polynomial, weights)
            if value:
                vector[row_index[row]] = value
        evaluated_columns.append(vector)
    base_rank = len(module.rational_basis(evaluated_columns[:-1]))
    augmented_rank = len(module.rational_basis(evaluated_columns))
    matching_ranks = (
        support_rank(rows, columns, entries, kept_rows, columns - 1),
        support_rank(rows, columns, entries, kept_rows, columns),
    )
    return (
        len(deleted_rows), len(kept_rows), base_rank, augmented_rank
    ), matching_ranks


def main() -> None:
    cached_blocks = load_cached_blocks()
    matrix_cache = cached_blocks.load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    left_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 8
    )
    right_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 9
    )
    pair_survivors = five.universal_pair_survivors(
        data, left_coordinates, right_coordinates
    )
    require(len(pair_survivors) == 196, "pair-survivor count changed")

    quotient_census = Counter()
    library_cases = 0
    surviving_cases = 0
    surviving_witnesses = 0
    support_saturated_witnesses = 0
    matching_jump_witnesses = 0
    first_survivor = None
    for block in cached_blocks.ACTIVE_LIBRARY_BLOCKS:
        audit = palette.audit_pair_block(
            five,
            four,
            bounded,
            data,
            pair_survivors[block],
            right_coordinates,
        )
        exception_supports = {case[0] for case, _record in audit["exceptions"]}
        for case, determinant in audit["determinants"]:
            if case[0] in exception_supports:
                continue
            rank, bad, _base, augmented = matrix_cache.witness_matrices(
                bounded, data, case[0]
            )
            require(
                rank == determinant[0] and bad == determinant[2],
                "reconstructed quotient witness changed",
            )
            winning_names = tuple(
                name
                for name, factors in determinant[3].items()
                if name.startswith("aug") and palette.torus_monomial(factors)
            )
            require(winning_names, "monomial augmented witness disappeared")
            case_survives = False
            for name in winning_names:
                record, matching_ranks = constant_row_quotient_record(
                    bounded, data["module"], augmented[name]
                )
                quotient_census[record] += 1
                if record[2:] == matching_ranks:
                    support_saturated_witnesses += 1
                if matching_ranks[1] > matching_ranks[0]:
                    matching_jump_witnesses += 1
                if record[3] > record[2]:
                    case_survives = True
                    surviving_witnesses += 1
                    if first_survivor is None:
                        first_survivor = (
                            block,
                            case[0],
                            name,
                            record,
                            matching_ranks,
                            case[1],
                            case[2],
                        )
            if case_survives:
                surviving_cases += 1
            library_cases += 1

    target_records = Counter()
    frontiers = []
    expected_pairs = (
        ((2, 8, 1, 2), (6, 8, 1, 0)),
        ((2, 8, 1, 2), (6, 8, 2, 0)),
        ((2, 8, 1, 2), (7, 8, 0, 0)),
        ((2, 8, 1, 2), (7, 8, 1, 0)),
        ((2, 8, 1, 2), (7, 8, 2, 0)),
        ((2, 8, 2, 0), (2, 8, 2, 2)),
        ((2, 8, 2, 0), (3, 8, 1, 2)),
        ((2, 8, 2, 0), (4, 8, 1, 2)),
        ((2, 8, 2, 0), (5, 8, 1, 2)),
        ((2, 8, 2, 0), (6, 8, 0, 2)),
        ((2, 8, 2, 0), (6, 8, 1, 2)),
        ((2, 8, 2, 0), (6, 8, 2, 2)),
        ((2, 8, 2, 0), (7, 8, 0, 2)),
        ((2, 8, 2, 0), (7, 8, 1, 2)),
    )
    require(pair_survivors[91:105] == expected_pairs, "pair-block order changed")
    for block in range(91, 105):
        record, affine_cases, torus_cases = matrix_cache.torus_pair_block(
            palette,
            five,
            four,
            bounded,
            data,
            pair_survivors[block],
            right_coordinates,
        )
        target_records.update(record)
        frontiers.append((len(affine_cases), len(torus_cases)))

    rank_jump_census = Counter(
        {
            record: count
            for record, count in quotient_census.items()
            if record[3] > record[2]
        }
    )
    require(
        (library_cases, sum(quotient_census.values()), len(quotient_census))
        == (1_909, 5_359, 30),
        "constant-row quotient census changed",
    )
    require(
        rank_jump_census
        == Counter(
            {
                (16, 6, 5, 6): 22,
                (15, 7, 6, 7): 10,
                (17, 5, 4, 5): 10,
                (10, 11, 10, 11): 4,
                (8, 13, 12, 13): 4,
                (12, 9, 8, 9): 4,
                (10, 12, 11, 12): 4,
                (9, 13, 12, 13): 4,
            }
        ),
        "constant-row quotient rank-jump census changed",
    )
    require(
        (
            support_saturated_witnesses,
            matching_jump_witnesses,
            surviving_witnesses,
            surviving_cases,
        )
        == (5_359, 62, 62, 52),
        "support-rank certification changed",
    )
    require(
        first_survivor
        == (
            0,
            (
                (0, 8, 1, 0),
                (0, 8, 1, 2),
                (2, 9, 0, 0),
                (3, 9, 1, 0),
                (3, 9, 1, 2),
            ),
            "aug1",
            (10, 11, 10, 11),
            (10, 11),
            (198, 210, 212, 324, 336, 338),
            (True, (), (), 24),
        ),
        "first constant-row quotient survivor changed",
    )
    require(
        tuple(frontiers)
        == (
            (70, 0), (0, 0), (0, 0), (70, 0), (0, 0),
            (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
            (0, 0), (0, 0), (0, 0), (0, 0),
        ),
        "target affine/torus frontier changed",
    )
    audited_supports = 14 * 59_640
    new_supports = sum(
        count
        for (grade_count, _status), count in target_records.items()
        if grade_count >= 3
    )
    closed_cumulative = 5_403_720 + new_supports
    remaining = 11_614_176 - closed_cumulative
    require(
        (audited_supports, new_supports, closed_cumulative, remaining)
        == (834_960, 832_608, 6_236_328, 5_377_848),
        "target support arithmetic changed",
    )

    print("N=10 five-cross constant-row quotient blocks 92-105: frontier")
    print(f"library monomial cases: {library_cases}")
    print(f"constant-row quotient signatures: {len(quotient_census)}")
    print(f"quotient rank-jump witnesses: {surviving_witnesses}")
    print(f"quotient rank-jump cases: {surviving_cases}")
    print(f"matching-rank-certified witnesses: {support_saturated_witnesses}")
    print(f"matching-rank-certified jumps: {matching_jump_witnesses}")
    print(f"first quotient jump: {first_survivor}")
    print(f"target supports: {audited_supports}; new supports: {new_supports}")
    print(f"target affine/torus candidates: "
          f"{sum(x for x, _ in frontiers)}/{sum(y for _, y in frontiers)}")
    print("target literal survivors: 0")
    print(f"cumulative closed new grade-3-to-6 supports: {closed_cumulative}")
    print(f"remaining unaudited grade-3-to-6 supports: {remaining}")
    print("arbitrary-old-source identity certified: 0")


if __name__ == "__main__":
    main()
