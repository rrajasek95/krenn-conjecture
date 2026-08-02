#!/usr/bin/env python3
"""Batch the zero-frequency degree-six Bockstein equations modulo 1009."""

from array import array
from collections import Counter, defaultdict
from fractions import Fraction
import importlib.util
import pickle
from pathlib import Path


HERE = Path(__file__).resolve().parent
ONE_PATH = HERE / "analyze_n8_full_source_degree6_bockstein.py"
SPEC = importlib.util.spec_from_file_location("n8_degree6_bockstein", ONE_PATH)
ONE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ONE)
D5 = ONE.D5
D6 = ONE.D6
PRIME = ONE.PRIME


def modular_fraction(value):
    value = Fraction(value)
    return value.numerator * pow(value.denominator, PRIME - 2, PRIME) % PRIME


def zero_frequency_functionals(rows, columns, column_index):
    by_column = defaultdict(list)
    row_frequencies = array("I", [0]) * len(rows)
    support_histogram = Counter()
    candidate_histogram = Counter()
    for index, row in enumerate(rows, 1):
        functional, candidate_count = ONE.sparse_tail_functional(
            row, columns, column_index
        )
        support_histogram[len(functional)] += 1
        candidate_histogram[candidate_count] += 1
        for column, coefficient in functional.items():
            by_column[column].append((index - 1, coefficient))
            row_frequencies[index - 1] += 1
        if index % 100 == 0:
            print("functionals", index, "/", len(rows), "nnz",
                  sum(row_frequencies), flush=True)
    return by_column, row_frequencies, support_histogram, candidate_histogram


def solve_augmented(matrix, frequencies, tails_by_column, tail_frequencies,
                    tail_target):
    base_rows = len(frequencies)
    tail_rows = len(tail_frequencies)
    total_rows = base_rows + tail_rows
    order = sorted(range(total_rows), key=lambda index: (
        frequencies[index] if index < base_rows
        else tail_frequencies[index - base_rows],
        index,
    ))
    row_order = [0] * total_rows
    for new_index, old_index in enumerate(order):
        row_order[old_index] = new_index
    column_order = sorted(range(len(matrix)), key=lambda index: (
        len(matrix[index]) + len(tails_by_column.get(index, ())),
        min(
            [row_order[item >> 3] for item in matrix[index]]
            + [row_order[base_rows + item[0]]
               for item in tails_by_column.get(index, ())]
        ),
        index,
    ))

    pivots = [None] * total_rows
    pivot_origins = [None] * total_rows
    pivot_inverses = [None] * total_rows
    pivot_reductions = [None] * total_rows
    rank = 0
    basis_nonzeros = 0
    maximum_basis = 0
    for processed, column_index in enumerate(column_order, 1):
        vector = {
            row_order[item >> 3]: item & 7 for item in matrix[column_index]
        }
        for tail_row, coefficient in tails_by_column.get(column_index, ()):
            vector[row_order[base_rows + tail_row]] = coefficient
        reductions = []
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            basis = pivots[pivot]
            if basis is None:
                inverse = pow(value, PRIME - 2, PRIME)
                normalized = tuple(sorted(
                    (index, coefficient * inverse % PRIME)
                    for index, coefficient in vector.items()
                ))
                pivots[pivot] = () if len(normalized) == 1 else normalized
                pivot_origins[pivot] = column_index
                pivot_inverses[pivot] = inverse
                pivot_reductions[pivot] = tuple(reductions)
                rank += 1
                basis_nonzeros += len(normalized)
                maximum_basis = max(maximum_basis, len(normalized))
                break
            if not basis:
                vector.pop(pivot)
            else:
                for index, coefficient in basis:
                    new_value = (
                        vector.get(index, 0) - value * coefficient
                    ) % PRIME
                    if new_value:
                        vector[index] = new_value
                    else:
                        vector.pop(index, None)
            reductions.append((pivot, value))
        if processed % 25000 == 0:
            print("elim", processed, "/", len(matrix), "rank", rank,
                  "basisnnz", basis_nonzeros, "max", maximum_basis,
                  flush=True)

    target = {
        row_order[base_rows + index]: value
        for index, value in enumerate(tail_target) if value
    }
    target_factors = {}
    target_residual = {}
    while target:
        pivot = min(target)
        value = target[pivot]
        basis = pivots[pivot]
        if basis is None:
            target_residual[pivot] = value
            target.pop(pivot)
        else:
            target_factors[pivot] = value
            if not basis:
                target.pop(pivot)
            else:
                for index, coefficient in basis:
                    new_value = (
                        target.get(index, 0) - value * coefficient
                    ) % PRIME
                    if new_value:
                        target[index] = new_value
                    else:
                        target.pop(index, None)
    print("RESULT rank", rank, "base", 72904, "added", rank - 72904,
          "rows", total_rows, "leftnull", total_rows - rank,
          "consistent", not target_residual, "targetres",
          len(target_residual), "targetfactors", len(target_factors),
          "basisnnz", basis_nonzeros, "max", maximum_basis, flush=True)
    if target_residual:
        selected = min(target_residual)
        dual_ordered = {selected: 1}
        for pivot in range(total_rows - 1, -1, -1):
            basis = pivots[pivot]
            if basis is None:
                continue
            value = -sum(
                coefficient * dual_ordered.get(index, 0)
                for index, coefficient in basis if index != pivot
            ) % PRIME if basis else 0
            if value:
                dual_ordered[pivot] = value
        dual_base = {
            index: dual_ordered[row_order[index]]
            for index in range(base_rows)
            if dual_ordered.get(row_order[index], 0)
        }
        dual_tail = {
            index: dual_ordered[row_order[base_rows + index]]
            for index in range(tail_rows)
            if dual_ordered.get(row_order[base_rows + index], 0)
        }
        pairing = sum(
            coefficient * tail_target[index]
            for index, coefficient in dual_tail.items()
        ) % PRIME
        if pairing != target_residual[selected]:
            raise RuntimeError("extracted dual has the wrong target pairing")
        for column_index, vector in enumerate(matrix):
            value = sum(
                dual_base.get(item >> 3, 0) * (item & 7)
                for item in vector
            )
            value += sum(
                dual_tail.get(row, 0) * coefficient
                for row, coefficient in tails_by_column.get(column_index, ())
            )
            if value % PRIME:
                raise RuntimeError("extracted dual does not annihilate matrix")
        print("dual support base", len(dual_base), "tail", len(dual_tail),
              "pairing", pairing, flush=True)
        return rank, target_residual, None, (dual_base, dual_tail, pairing)

    beta = dict(target_factors)
    solution = {}
    for pivot in range(total_rows - 1, -1, -1):
        coefficient = beta.pop(pivot, 0) % PRIME
        if not coefficient:
            continue
        origin_coefficient = coefficient * pivot_inverses[pivot] % PRIME
        origin = pivot_origins[pivot]
        solution[origin] = (
            solution.get(origin, 0) + origin_coefficient
        ) % PRIME
        if not solution[origin]:
            solution.pop(origin)
        for earlier_pivot, reduction_coefficient in pivot_reductions[pivot]:
            beta[earlier_pivot] = (
                beta.get(earlier_pivot, 0)
                - origin_coefficient * reduction_coefficient
            ) % PRIME
            if not beta[earlier_pivot]:
                beta.pop(earlier_pivot)
    if beta:
        raise RuntimeError("batch Bockstein propagation left pivot factors")

    base_image = defaultdict(int)
    tail_image = defaultdict(int)
    for column_index, coefficient in solution.items():
        for item in matrix[column_index]:
            row = item >> 3
            base_image[row] = (
                base_image[row] + coefficient * (item & 7)
            ) % PRIME
        for row, value in tails_by_column.get(column_index, ()):
            tail_image[row] = (
                tail_image[row] + coefficient * value
            ) % PRIME
    if any(base_image.values()):
        raise RuntimeError("batch correction left a lower-degree image")
    if any(tail_image[index] != value
           for index, value in enumerate(tail_target)):
        raise RuntimeError("batch correction does not hit zero-row target")
    print("solution support", len(solution), flush=True)
    return rank, target_residual, solution, None


def main():
    with open("/tmp/n8_degree5_compact_state.pkl", "rb") as source:
        state5 = pickle.load(source)
    columns = ONE.previous_columns(state5)
    column_index = {column: index for index, column in enumerate(columns)}
    with open("/tmp/n8_degree5_coupled_matrix.pkl", "rb") as source:
        matrix5, frequencies5 = pickle.load(source)
    with open("/tmp/n8_degree6_compact_state.pkl", "rb") as source:
        state6 = pickle.load(source)
    rows6 = tuple(sorted(state6["degree6_rows"]))
    residual6 = state6["degree6_tail"]
    with open("/tmp/n8_degree6_fixed_matrix.pkl", "rb") as source:
        _matrix6, frequencies6, _metadata = pickle.load(source)
    zero_rows = tuple(
        rows6[index] for index, frequency in enumerate(frequencies6)
        if frequency == 0 and residual6.get(rows6[index], 0)
    )
    if len(zero_rows) != 1466:
        raise RuntimeError("zero-frequency residual-row census changed")
    tails_by_column, tail_frequencies, support_histogram, candidates = (
        zero_frequency_functionals(zero_rows, columns, column_index)
    )
    print("zero-row tails", len(zero_rows), "columns", len(tails_by_column),
          "nnz", sum(tail_frequencies), "support histogram",
          sorted(support_histogram.items()), "candidate histogram",
          sorted(candidates.items()), flush=True)
    tail_target = tuple(
        -modular_fraction(residual6[row]) % PRIME for row in zero_rows
    )
    rank, target_residual, solution, dual = solve_augmented(
        matrix5, frequencies5, tails_by_column, tail_frequencies, tail_target
    )
    with open("/tmp/n8_degree6_zero_bockstein_batch.pkl", "wb") as output:
        pickle.dump({
            "zero_rows": zero_rows,
            "tail_frequencies": tail_frequencies,
            "tail_target": tail_target,
            "rank": rank,
            "target_residual": target_residual,
            "kernel_correction": solution,
            "violating_dual": dual,
        }, output, protocol=5)


if __name__ == "__main__":
    main()
