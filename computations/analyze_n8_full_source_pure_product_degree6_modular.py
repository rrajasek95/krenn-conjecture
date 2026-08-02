#!/usr/bin/env python3
"""Sparse modular fixed-tail B6 solve at the n=8 degree-six frontier."""

from array import array
from collections import Counter, defaultdict
import importlib.util
import os
import pickle
from pathlib import Path
import resource


HERE = Path(__file__).resolve().parent
D6_PATH = HERE / "analyze_n8_full_source_pure_product_degree6_lift.py"
SPEC = importlib.util.spec_from_file_location("n8_degree6", D6_PATH)
D6 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D6)
D5 = D6.D5

PRIME = 1009
STATE_PATH = "/tmp/n8_degree6_compact_state.pkl"
MATRIX_PATH = "/tmp/n8_degree6_fixed_matrix.pkl"


def memory_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)


def canonical_row_and_orbit_size(row):
    orbit = {
        bytes(sorted(transform[value] for value in row))
        for transform in D5.VARIABLE_TRANSFORMS
    }
    return min(orbit), len(orbit)


def invariant_entries(column, row_index):
    counts = defaultdict(int)
    row_sizes = {}
    for output in D5.iter_column_outputs(column):
        if D5.row_degree(output) != 6:
            continue
        representative, row_size = canonical_row_and_orbit_size(output)
        counts[representative] += 1
        row_sizes[representative] = row_size
    column_size = len(D5.column_orbit(column))
    answer = []
    for row, count in counts.items():
        numerator = column_size * count
        if numerator % row_sizes[row]:
            raise RuntimeError("orbit-stabilizer invariant entry is not integral")
        coefficient = numerator // row_sizes[row]
        if not 0 < coefficient < 256:
            raise RuntimeError("invariant coefficient exceeds byte packing")
        answer.append((row_index[row] << 8) | coefficient)
    return array("I", sorted(answer))


def build_matrix(rows, columns):
    row_index = {row: index for index, row in enumerate(rows)}
    frequencies = array("I", [0]) * len(rows)
    matrix = []
    histogram = Counter()
    nonzeros = 0
    coefficient_maximum = 0
    for position, column in enumerate(columns, 1):
        vector = invariant_entries(column, row_index)
        if not vector:
            raise RuntimeError("minimum-degree-six column has no invariant entry")
        matrix.append(vector)
        histogram[len(vector)] += 1
        nonzeros += len(vector)
        for item in vector:
            frequencies[item >> 8] += 1
            coefficient_maximum = max(coefficient_maximum, item & 255)
        if position % 25000 == 0:
            print("matrix", position, "/", len(columns), "nnz", nonzeros,
                  "memMB", round(memory_mb()), flush=True)
    return matrix, frequencies, nonzeros, histogram, coefficient_maximum


def modular_rank_and_target(matrix, frequencies, residual, rows):
    order = sorted(range(len(rows)), key=lambda index: (frequencies[index], index))
    row_order = [0] * len(rows)
    for new_index, old_index in enumerate(order):
        row_order[old_index] = new_index
    column_order = sorted(
        range(len(matrix)),
        key=lambda index: (
            len(matrix[index]),
            min(row_order[item >> 8] for item in matrix[index]),
            index,
        ),
    )
    pivots = [None] * len(rows)
    rank = 0
    basis_nonzeros = 0
    maximum_basis = 0
    for processed, column_index in enumerate(column_order, 1):
        vector = {
            row_order[item >> 8]: item & 255 for item in matrix[column_index]
        }
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
                rank += 1
                basis_nonzeros += len(normalized)
                maximum_basis = max(maximum_basis, len(normalized))
                break
            if not basis:
                vector.pop(pivot)
                continue
            for index, coefficient in basis:
                new_value = (vector.get(index, 0) - value * coefficient) % PRIME
                if new_value:
                    vector[index] = new_value
                else:
                    vector.pop(index, None)
        if processed % 25000 == 0:
            print("elim", processed, "/", len(matrix), "rank", rank,
                  "basisnnz", basis_nonzeros, "max", maximum_basis,
                  "memMB", round(memory_mb()), flush=True)

    target = {}
    for old_index, row in enumerate(rows):
        if row not in residual:
            continue
        value = residual[row]
        modular_value = (
            -value.numerator * pow(value.denominator, PRIME - 2, PRIME)
        ) % PRIME
        if modular_value:
            target[row_order[old_index]] = modular_value
    target_residual = {}
    while target:
        pivot = min(target)
        value = target[pivot]
        basis = pivots[pivot]
        if basis is None:
            target_residual[pivot] = value
            target.pop(pivot)
        elif not basis:
            target.pop(pivot)
        else:
            for index, coefficient in basis:
                new_value = (target.get(index, 0) - value * coefficient) % PRIME
                if new_value:
                    target[index] = new_value
                else:
                    target.pop(index, None)
    print("RESULT rank", rank, "rows", len(rows), "leftnull", len(rows)-rank,
          "consistent", not target_residual, "targetres", len(target_residual),
          "basisnnz", basis_nonzeros, "max", maximum_basis, flush=True)
    return rank, target_residual


def main():
    with open(STATE_PATH, "rb") as source:
        state = pickle.load(source)
    rows = tuple(sorted(state["degree6_rows"]))
    columns = tuple(sorted(state["degree6_columns"]))
    residual = state["degree6_tail"]
    print("loaded", len(rows), len(columns), "tail", len(residual),
          "memMB", round(memory_mb()), flush=True)
    if os.path.exists(MATRIX_PATH):
        with open(MATRIX_PATH, "rb") as source:
            matrix, frequencies, metadata = pickle.load(source)
        nonzeros, histogram, coefficient_maximum = metadata
        print("loaded matrix checkpoint", nonzeros, flush=True)
    else:
        matrix, frequencies, nonzeros, histogram, coefficient_maximum = (
            build_matrix(rows, columns)
        )
        with open(MATRIX_PATH, "wb") as output:
            pickle.dump((matrix, frequencies,
                         (nonzeros, histogram, coefficient_maximum)),
                        output, protocol=5)
    print("matrix census", nonzeros, sorted(histogram.items()),
          "coefmax", coefficient_maximum, "freq", min(frequencies),
          max(frequencies), "memMB", round(memory_mb()), flush=True)
    modular_rank_and_target(matrix, frequencies, residual, rows)


if __name__ == "__main__":
    main()
