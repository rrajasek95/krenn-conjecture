#!/usr/bin/env python3
"""One-step Bockstein test for sparse degree-six fixed-tail duals."""

from array import array
from collections import defaultdict
import importlib.util
import pickle
from pathlib import Path


HERE = Path(__file__).resolve().parent
D6M_PATH = HERE / "analyze_n8_full_source_pure_product_degree6_modular.py"
SPEC = importlib.util.spec_from_file_location("n8_degree6_mod", D6M_PATH)
D6M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D6M)
D6 = D6M.D6
D5 = D6M.D5

PRIME = 1009


def previous_columns(state5):
    high = tuple(sorted(state5["coupled_columns"]))
    low = tuple(sorted(state5["low_columns"]))
    return high + low


def invariant_target_coefficient(column, target_row, target_orbit_size):
    count = 0
    for output in D5.iter_column_outputs(column):
        if D5.row_degree(output) == 6 and D5.canonical_row(output) == target_row:
            count += 1
    numerator = len(D5.column_orbit(column)) * count
    if numerator % target_orbit_size:
        raise RuntimeError("target coefficient orbit quotient is not integral")
    return numerator // target_orbit_size


def sparse_tail_functional(target_row, columns, column_index):
    target_orbit_size = len({
        bytes(sorted(transform[value] for value in target_row))
        for transform in D5.VARIABLE_TRANSFORMS
    })
    candidates = {
        D5.canonical_column(column) for column in D6.incident_columns(target_row)
    }
    functional = {}
    for column in candidates:
        if column not in column_index:
            continue
        coefficient = invariant_target_coefficient(
            column, target_row, target_orbit_size
        )
        if coefficient % PRIME:
            functional[column_index[column]] = coefficient % PRIME
    return functional, len(candidates)


def augmented_rank(matrix, frequencies, functional):
    row_count = len(frequencies)
    augmented_frequency = len(functional)
    order = sorted(range(row_count + 1), key=lambda index: (
        augmented_frequency if index == row_count else frequencies[index],
        index,
    ))
    row_order = [0] * (row_count + 1)
    for new_index, old_index in enumerate(order):
        row_order[old_index] = new_index
    column_order = sorted(
        range(len(matrix)),
        key=lambda index: (
            len(matrix[index]) + (index in functional),
            min(
                [row_order[item >> 3] for item in matrix[index]]
                + ([row_order[row_count]] if index in functional else [])
            ),
            index,
        ),
    )
    pivots = [None] * (row_count + 1)
    pivot_origins = [None] * (row_count + 1)
    pivot_inverses = [None] * (row_count + 1)
    pivot_reductions = [None] * (row_count + 1)
    rank = 0
    maximum_basis = 0
    for column_index in column_order:
        vector = {
            row_order[item >> 3]: item & 7 for item in matrix[column_index]
        }
        if column_index in functional:
            vector[row_order[row_count]] = functional[column_index]
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

    target = {row_order[row_count]: 1}
    target_factors = {}
    while target:
        pivot = min(target)
        value = target[pivot]
        basis = pivots[pivot]
        if basis is None:
            raise RuntimeError("augmented kernel target is inconsistent")
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
    beta = dict(target_factors)
    solution = {}
    for pivot in range(row_count, -1, -1):
        coefficient = beta.pop(pivot, 0) % PRIME
        if not coefficient:
            continue
        inverse = pivot_inverses[pivot]
        origin = pivot_origins[pivot]
        origin_coefficient = coefficient * inverse % PRIME
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
        raise RuntimeError("augmented solution propagation failed")
    low_image = defaultdict(int)
    functional_value = 0
    for column_index, coefficient in solution.items():
        for item in matrix[column_index]:
            low_image[item >> 3] = (
                low_image[item >> 3] + coefficient * (item & 7)
            ) % PRIME
        functional_value = (
            functional_value + coefficient * functional.get(column_index, 0)
        ) % PRIME
    if any(low_image.values()) or functional_value != 1:
        raise RuntimeError("augmented kernel direction replay failed")
    return rank, maximum_basis, solution, len(target_factors)


def main():
    with open("/tmp/n8_degree5_compact_state.pkl", "rb") as source:
        state5 = pickle.load(source)
    columns = previous_columns(state5)
    column_index = {column: index for index, column in enumerate(columns)}
    with open("/tmp/n8_degree5_coupled_matrix.pkl", "rb") as source:
        matrix5, frequencies5 = pickle.load(source)
    with open("/tmp/n8_degree6_compact_state.pkl", "rb") as source:
        state6 = pickle.load(source)
    rows6 = tuple(sorted(state6["degree6_rows"]))
    residual6 = state6["degree6_tail"]
    with open("/tmp/n8_degree6_fixed_matrix.pkl", "rb") as source:
        _matrix6, frequencies6, _metadata = pickle.load(source)
    zero_rows = [index for index, frequency in enumerate(frequencies6)
                 if frequency == 0 and residual6.get(rows6[index], 0)]
    if len(zero_rows) != 1466:
        raise RuntimeError("zero-frequency residual-row census changed")
    selected_index = zero_rows[0]
    selected_row = rows6[selected_index]
    functional, candidate_count = sparse_tail_functional(
        selected_row, columns, column_index
    )
    if not functional:
        raise RuntimeError("selected Bockstein functional is zero")
    print("selected row", selected_row.hex(), "residual",
          residual6[selected_row], "incident candidates", candidate_count,
          "earlier support", len(functional), flush=True)
    rank, maximum_basis, solution, target_factors = augmented_rank(
        matrix5, frequencies5, functional
    )
    print("Bockstein augmented rank", rank, "base rank", 72904,
          "rowspace", rank == 72904, "maximum basis", maximum_basis,
          flush=True)
    print("kernel direction support", len(solution), "target factors",
          target_factors, flush=True)
    with open("/tmp/n8_degree6_first_bockstein_direction.pkl", "wb") as output:
        pickle.dump({
            "selected_row": selected_row,
            "selected_residual": residual6[selected_row],
            "tail_functional": functional,
            "kernel_direction": solution,
        }, output, protocol=5)


if __name__ == "__main__":
    main()
