#!/usr/bin/env python3
"""Modular coupled second Bockstein for the seven critical chart sources.

This retains all 201 kernel directions of the 570x741 first-shell map.  The
second-shell correction space is the sum of their literal next tails and the
17,915 new matching columns.  Incidence components are eliminated
independently so unrelated row orbits never enter the same sparse basis.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIRST_PATH = HERE / "audit_seven_critical_first_bockstein.py"
SPEC = importlib.util.spec_from_file_location("first_bockstein", FIRST_PATH)
FIRST = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(FIRST)

SOURCE = FIRST.SOURCE
PRIME = 1009


def add_scaled_mod(target, source, scale):
    for key, coefficient in source.items():
        value = (target.get(key, 0) + scale * coefficient) % PRIME
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def counter_mod(column, allowed):
    return {
        row: coefficient % PRIME
        for row, coefficient in Counter(SOURCE.column_outputs(column)).items()
        if row in allowed and coefficient % PRIME
    }


def leading_packet():
    target_rows = tuple(sorted(SOURCE.target_orbit_rows()))
    target_set = frozenset(target_rows)
    support_columns = tuple(sorted(set().union(*(
        SOURCE.incident_columns(row) for row in target_rows
    ))))
    representatives = FIRST.critical_representatives(target_rows, support_columns)
    tails = tuple(
        FIRST.literal_tail(representative, support_columns, target_set)
        for representative in representatives
    )
    first_rows = tuple(sorted(
        set().union(*(Counter(SOURCE.column_outputs(column)) for column in support_columns))
        - target_set
    ))
    first_set = frozenset(first_rows)
    first_columns = tuple(sorted(
        set().union(*(SOURCE.incident_columns(row) for row in first_rows))
        - set(support_columns)
    ))
    if (len(first_rows), len(first_columns)) != (570, 741):
        raise RuntimeError("first shell changed")
    return (target_rows, target_set, support_columns, representatives, tails,
            first_rows, first_set, first_columns)


def first_modular_solve(first_rows, first_columns, tails):
    row_index = {row: index for index, row in enumerate(first_rows)}
    basis = {}
    provenance = {}
    kernels = []
    for column_number, column in enumerate(first_columns):
        literal = counter_mod(column, set(first_rows))
        vector = {row_index[row]: value for row, value in literal.items()}
        representative = {column_number: 1}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, PRIME)
                basis[pivot] = {
                    row: coefficient * inverse % PRIME
                    for row, coefficient in vector.items()
                }
                provenance[pivot] = {
                    source: coefficient * inverse % PRIME
                    for source, coefficient in representative.items()
                }
                break
            add_scaled_mod(vector, basis[pivot], -value)
            add_scaled_mod(representative, provenance[pivot], -value)
        if not vector:
            kernels.append(representative)
    if len(basis) != 540 or len(kernels) != 201:
        raise RuntimeError("first-shell modular rank/kernel changed")

    solutions = []
    for tail in tails:
        vector = {
            row_index[row]: (
                coefficient.numerator
                * pow(coefficient.denominator, -1, PRIME)
            ) % PRIME
            for row, coefficient in tail.items()
        }
        coordinates = {}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                raise RuntimeError("critical tail left first-shell span")
            add_scaled_mod(vector, basis[pivot], -value)
            add_scaled_mod(coordinates, provenance[pivot], value)
        solutions.append(coordinates)
    return tuple(kernels), tuple(solutions)


class UnionFind:
    def __init__(self):
        self.parent = {}
        self.size = {}

    def add(self, item):
        if item not in self.parent:
            self.parent[item] = item
            self.size[item] = 1

    def find(self, item):
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != item:
            parent = self.parent[item]
            self.parent[item] = root
            item = parent
        return root

    def union(self, first, second):
        self.add(first)
        self.add(second)
        first, second = self.find(first), self.find(second)
        if first == second:
            return
        if self.size[first] < self.size[second]:
            first, second = second, first
        self.parent[second] = first
        self.size[first] += self.size[second]


def _back_substitute_basis_coordinates(
    basis_coordinates,
    basis_order,
    basis_origin,
    basis_scale,
    basis_reductions,
):
    """Expand normalized echelon coordinates into correction-vector coordinates."""
    basis_coordinates = dict(basis_coordinates)
    source_coordinates = {}
    for pivot in reversed(basis_order):
        coefficient = basis_coordinates.pop(pivot, 0)
        if not coefficient:
            continue
        inverse = pow(basis_scale[pivot], -1, PRIME)
        scaled = coefficient * inverse % PRIME
        origin = basis_origin[pivot]
        source_coordinates[origin] = (
            source_coordinates.get(origin, 0) + scaled
        ) % PRIME
        if not source_coordinates[origin]:
            source_coordinates.pop(origin)
        for earlier, value in basis_reductions[pivot]:
            updated = (
                basis_coordinates.get(earlier, 0) - scaled * value
            ) % PRIME
            if updated:
                basis_coordinates[earlier] = updated
            else:
                basis_coordinates.pop(earlier, None)
    if basis_coordinates:
        raise RuntimeError("basis back-substitution left coordinates")
    return source_coordinates


def audit(return_state=False):
    (target_rows, target_set, support_columns, representatives, tails,
     first_rows, first_set, first_columns) = leading_packet()
    kernels, first_solutions = first_modular_solve(first_rows, first_columns, tails)

    earlier_rows = target_set | first_set
    second_rows = tuple(sorted(
        set().union(*(Counter(SOURCE.column_outputs(column)) for column in first_columns))
        - earlier_rows
    ))
    second_set = frozenset(second_rows)
    second_columns = tuple(sorted(
        set().union(*(SOURCE.incident_columns(row) for row in second_rows))
        - set(support_columns) - set(first_columns)
    ))
    if (len(second_rows), len(second_columns)) != (27470, 17915):
        raise RuntimeError("second shell changed")

    kernel_tails = []
    for representative in kernels:
        vector = {}
        for column_number, coefficient in representative.items():
            add_scaled_mod(
                vector,
                counter_mod(first_columns[column_number], second_set),
                coefficient,
            )
        kernel_tails.append(vector)

    critical_second_tails = []
    for leading, solution in zip(representatives, first_solutions):
        vector = {}
        for column_number, coefficient in leading.items():
            add_scaled_mod(
                vector,
                counter_mod(support_columns[column_number], second_set),
                coefficient.numerator
                * pow(coefficient.denominator, -1, PRIME) % PRIME,
            )
        for column_number, coefficient in solution.items():
            add_scaled_mod(
                vector,
                counter_mod(first_columns[column_number], second_set),
                -coefficient,
            )
        critical_second_tails.append(vector)

    correction_vectors = [counter_mod(column, second_set) for column in second_columns]
    correction_vectors.extend(kernel_tails)

    union = UnionFind()
    row_to_vectors = defaultdict(list)
    for number, vector in enumerate(correction_vectors):
        rows = tuple(vector)
        if not rows:
            continue
        first = rows[0]
        union.add(first)
        for row in rows[1:]:
            union.union(first, row)
        for row in rows:
            row_to_vectors[row].append(number)
    for tail in critical_second_tails:
        rows = tuple(tail)
        if rows:
            union.add(rows[0])
            for row in rows[1:]:
                union.union(rows[0], row)

    component_rows = defaultdict(set)
    for row in union.parent:
        component_rows[union.find(row)].add(row)
    component_vectors = defaultdict(set)
    for row, numbers in row_to_vectors.items():
        component_vectors[union.find(row)].update(numbers)
    component_targets = defaultdict(list)
    for target_number, tail in enumerate(critical_second_tails):
        if tail:
            component_targets[union.find(next(iter(tail)))].append(target_number)

    component_records = []
    target_remainders = [None] * len(critical_second_tails)
    target_solution_terms = [None] * len(critical_second_tails)
    target_solutions = [None] * len(critical_second_tails)
    correction_kernels = []
    total_rank = 0
    for root in sorted(component_rows, key=lambda item: min(component_rows[item])):
        rows = tuple(sorted(component_rows[root]))
        row_index = {row: index for index, row in enumerate(rows)}
        numbers = tuple(sorted(component_vectors[root]))
        basis = {}
        basis_origin = {}
        basis_scale = {}
        basis_reductions = {}
        basis_order = []
        dependent_reductions = []
        for number in numbers:
            vector = {
                row_index[row]: coefficient
                for row, coefficient in correction_vectors[number].items()
            }
            reductions = []
            while vector:
                pivot = min(vector)
                value = vector[pivot]
                if pivot not in basis:
                    basis_origin[pivot] = number
                    basis_scale[pivot] = value
                    basis_reductions[pivot] = tuple(reductions)
                    basis_order.append(pivot)
                    inverse = pow(value, -1, PRIME)
                    basis[pivot] = {
                        row: coefficient * inverse % PRIME
                        for row, coefficient in vector.items()
                    }
                    break
                reductions.append((pivot, value))
                add_scaled_mod(vector, basis[pivot], -value)
            if not vector:
                dependent_reductions.append((number, tuple(reductions)))
        total_rank += len(basis)
        for number, reductions in dependent_reductions:
            coordinates = _back_substitute_basis_coordinates(
                dict(reductions), basis_order, basis_origin, basis_scale,
                basis_reductions,
            )
            kernel = {number: 1}
            add_scaled_mod(kernel, coordinates, -1)
            replay = {}
            for source_number, coefficient in kernel.items():
                add_scaled_mod(replay, correction_vectors[source_number], coefficient)
            if replay:
                raise RuntimeError("second-shell kernel failed replay")
            correction_kernels.append(kernel)
        for target_number in component_targets[root]:
            vector = {
                row_index[row]: coefficient
                for row, coefficient in critical_second_tails[target_number].items()
            }
            basis_coordinates = {}
            while vector:
                pivot = min(vector)
                value = vector[pivot]
                if pivot not in basis:
                    break
                basis_coordinates[pivot] = (
                    basis_coordinates.get(pivot, 0) + value
                ) % PRIME
                add_scaled_mod(vector, basis[pivot], -value)
            target_remainders[target_number] = len(vector)
            if not vector:
                source_coordinates = _back_substitute_basis_coordinates(
                    basis_coordinates, basis_order, basis_origin, basis_scale,
                    basis_reductions,
                )
                replay = {}
                for number, coefficient in source_coordinates.items():
                    add_scaled_mod(replay, correction_vectors[number], coefficient)
                if replay != critical_second_tails[target_number]:
                    raise RuntimeError("second-shell source solution failed replay")
                target_solution_terms[target_number] = len(source_coordinates)
                target_solutions[target_number] = source_coordinates
        component_records.append((len(rows), len(numbers), len(basis),
                                  tuple(component_targets[root])))

    if any(solution is None for solution in target_solutions):
        raise RuntimeError("not every second tail acquired source coordinates")
    if len(correction_kernels) != len(correction_vectors) - total_rank:
        raise RuntimeError("second-shell nullity/provenance changed")

    third_rows = frozenset(
        set().union(*(Counter(SOURCE.column_outputs(column)) for column in second_columns))
        - earlier_rows - second_set
    )
    if len(third_rows) != 360818:
        raise RuntimeError("third row shell changed")
    third_tails = []
    for leading, first_solution, second_solution in zip(
        representatives, first_solutions, target_solutions
    ):
        vector = {}
        for column_number, coefficient in leading.items():
            add_scaled_mod(
                vector,
                counter_mod(support_columns[column_number], third_rows),
                coefficient.numerator
                * pow(coefficient.denominator, -1, PRIME) % PRIME,
            )
        for column_number, coefficient in first_solution.items():
            add_scaled_mod(
                vector,
                counter_mod(first_columns[column_number], third_rows),
                -coefficient,
            )
        for correction_number, coefficient in second_solution.items():
            if correction_number < len(second_columns):
                add_scaled_mod(
                    vector,
                    counter_mod(second_columns[correction_number], third_rows),
                    -coefficient,
                )
            else:
                kernel = kernels[correction_number - len(second_columns)]
                for column_number, kernel_coefficient in kernel.items():
                    add_scaled_mod(
                        vector,
                        counter_mod(first_columns[column_number], third_rows),
                        -coefficient * kernel_coefficient,
                    )
        third_tails.append(vector)

    result = {
        "prime": PRIME,
        "first_kernel": len(kernels),
        "second_rows": len(second_rows),
        "second_columns": len(second_columns),
        "kernel_tail_nonzero": sum(bool(vector) for vector in kernel_tails),
        "kernel_tail_terms": sum(map(len, kernel_tails)),
        "critical_second_tail_terms": tuple(map(len, critical_second_tails)),
        "incidence_components": len(component_records),
        "largest_components": tuple(sorted(component_records)[-10:]),
        "correction_rank": total_rank,
        "target_remainders": tuple(target_remainders),
        "target_solution_terms": tuple(target_solution_terms),
        "third_rows": len(third_rows),
        "critical_third_tail_rows": len(set().union(*(tail.keys() for tail in third_tails))),
        "critical_third_tail_terms": tuple(map(len, third_tails)),
        "second_correction_kernel": len(correction_kernels),
    }
    if return_state:
        result["_state"] = {
            "target_set": target_set,
            "support_columns": support_columns,
            "representatives": representatives,
            "first_set": first_set,
            "first_columns": first_columns,
            "first_solutions": first_solutions,
            "first_kernels": kernels,
            "second_set": second_set,
            "second_columns": second_columns,
            "second_solutions": tuple(target_solutions),
            "second_correction_kernels": tuple(correction_kernels),
            "third_rows": third_rows,
            "third_tails": tuple(third_tails),
        }
    return result


def main():
    global PRIME
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009)
    args = parser.parse_args()
    PRIME = args.prime
    result = audit()
    for key, value in result.items():
        if key == "_state":
            continue
        print(f"{key}: {value}", flush=True)


if __name__ == "__main__":
    main()
