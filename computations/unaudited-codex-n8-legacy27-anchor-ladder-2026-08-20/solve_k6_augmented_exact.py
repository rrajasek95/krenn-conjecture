#!/usr/bin/env python3
"""Exact-Q solve of the frozen legacy27 K^6 augmented orbit matrix."""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
import argparse
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
MATRIX = HERE / "k6_augmented_matrix.json"
OUT = HERE / "k6_augmented_solution_exact.json"
EXPECTED_MATRIX_SHA256 = (
    "78a62528fc5dce57f5c20f4000b3b35bfe0b2f6679ebd1285f7de97fb9d0fb92"
)
PRIMES = (1009, 1013)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_scaled(target, source, scale):
    for index, value in source.items():
        updated = target.get(index, Fraction(0)) + scale * value
        if updated:
            target[index] = updated
        else:
            target.pop(index, None)


def peel(rows, columns):
    incident = [[] for _ in range(rows)]
    for number, vector in enumerate(columns):
        for row in vector:
            incident[row].append(number)
    active = [True] * rows
    counts = [len(vector) for vector in columns]
    queue = deque(number for number, count in enumerate(counts) if count == 1)
    order = []
    while queue:
        column = queue.popleft()
        if counts[column] != 1:
            continue
        row = next((row for row in columns[column] if active[row]), None)
        require(row is not None, "unit peel active-count drifted")
        active[row] = False
        order.append((row, column))
        for other in incident[row]:
            counts[other] -= 1
            require(counts[other] >= 0, "unit peel count became negative")
            if counts[other] == 1:
                queue.append(other)
    return tuple(order), tuple(row for row, value in enumerate(active) if value)


def modular_basis(columns, core_rows, prime):
    core_index = {row: number for number, row in enumerate(core_rows)}
    candidates = []
    for column, raw in enumerate(columns):
        vector = Counter({core_index[row]: value for row, value in raw.items()
                          if row in core_index})
        if vector:
            candidates.append((len(vector), len(raw), column, vector))
    candidates.sort()
    basis = {}
    selected = []
    for _core_weight, _full_weight, column, raw in candidates:
        vector = {
            row: value.numerator * pow(value.denominator, -1, prime) % prime
            for row, value in raw.items()
            if value.numerator % prime
        }
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, prime)
                basis[pivot] = {
                    row: entry * inverse % prime
                    for row, entry in vector.items()
                }
                selected.append(column)
                break
            for row, entry in basis[pivot].items():
                updated = (vector.get(row, 0) - value * entry) % prime
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
    return basis, tuple(selected)


def reduce_target_mod(target, core_rows, basis, prime):
    core_index = {row: number for number, row in enumerate(core_rows)}
    residual = {core_index[row]: value.numerator
                * pow(value.denominator, -1, prime) % prime
                for row, value in target.items()
                if row in core_index and value % prime}
    while residual:
        pivot = min(residual)
        if pivot not in basis:
            break
        value = residual[pivot]
        for row, entry in basis[pivot].items():
            updated = (residual.get(row, 0) - value * entry) % prime
            if updated:
                residual[row] = updated
            else:
                residual.pop(row, None)
    return residual


def exact_core_solution(columns, target, core_rows, selected, pivot_numbers):
    pivot_rows = tuple(core_rows[number] for number in pivot_numbers)
    size = len(selected)
    require(len(pivot_rows) == size, "core minor is not square")
    augmented = []
    for row in pivot_rows:
        augmented.append([
            Fraction(columns[column].get(row, 0)) for column in selected
        ] + [Fraction(target.get(row, 0))])
    determinant = Fraction(1)
    sign = 1
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if augmented[row][column]), None)
        require(pivot is not None, "modular core minor vanished over Q")
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
            sign *= -1
        pivot_value = augmented[column][column]
        determinant *= pivot_value
        augmented[column] = [value / pivot_value
                             for value in augmented[column]]
        # Complete common-echelon reduction, not a triangular early stop.
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [left - scale * right
                              for left, right in
                              zip(augmented[row], augmented[column])]
        if (column + 1) % 50 == 0:
            print(f"exact core pivots {column + 1}/{size}", flush=True)
    determinant *= sign
    solution = Counter({selected[index]: augmented[index][-1]
                        for index in range(size) if augmented[index][-1]})
    return solution, determinant


def audit():
    payload = json.loads(MATRIX.read_text())
    require(payload["matrix_sha256"] == EXPECTED_MATRIX_SHA256,
            "frozen matrix digest changed")
    rows = payload["total_rows"]
    columns = tuple(Counter({row: Fraction(value) for row, value in
                             column["entries"]})
                    for column in payload["columns"])
    target = Counter({row: Fraction(value) for row, value in payload["target"]})
    peel_order, core_rows = peel(rows, columns)
    require((len(peel_order), len(core_rows)) == (3533, 372),
            "augmented unit-peel census changed")

    modular = {}
    selected_1009 = None
    pivot_1009 = None
    for prime in PRIMES:
        basis, selected = modular_basis(columns, core_rows, prime)
        residual = reduce_target_mod(target, core_rows, basis, prime)
        modular[str(prime)] = {
            "core_rank": len(basis),
            "core_left_nullity": len(core_rows) - len(basis),
            "target_remainder_nonzeros": len(residual),
            "target_in_image": not residual,
        }
        require(len(basis) == 331 and not residual,
                f"mod-{prime} calibration changed")
        if prime == 1009:
            selected_1009 = selected
            pivot_1009 = tuple(sorted(basis))

    solution, determinant = exact_core_solution(
        columns, target, core_rows, selected_1009, pivot_1009
    )
    replay = Counter()
    for column, coefficient in solution.items():
        add_scaled(replay, columns[column], coefficient)
    residual = Counter(target)
    add_scaled(residual, replay, Fraction(-1))
    core_set = set(core_rows)
    require(not any(row in core_set for row in residual),
            "exact core solution left an active row")
    for row, column in reversed(peel_order):
        coefficient = residual.get(row, Fraction(0))
        if not coefficient:
            continue
        pivot_value = columns[column][row]
        require(pivot_value, "reverse peel lost its pivot coefficient")
        coefficient /= pivot_value
        solution[column] += coefficient
        add_scaled(residual, columns[column], -coefficient)
    require(not residual, "exact reverse peeling left a residual")

    exact_replay = Counter()
    for column, coefficient in solution.items():
        add_scaled(exact_replay, columns[column], coefficient)
    require(exact_replay == target, "full augmented exact replay failed")
    first = min(solution)
    mutation = Counter(exact_replay)
    add_scaled(mutation, columns[first], -solution[first])
    require(mutation != target, "exact solution deletion mutation did not fire")

    denominator_lcm = 1
    for coefficient in solution.values():
        denominator_lcm = (denominator_lcm * coefficient.denominator
                           // math.gcd(denominator_lcm,
                                       coefficient.denominator))
    core = {
        "status": "UNAUDITED exact-Q augmented solve; labelled replay pending",
        "matrix_sha256": EXPECTED_MATRIX_SHA256,
        "matrix_dimensions": [rows, len(columns)],
        "unit_peeled_rows": len(peel_order),
        "irreducible_core_rows": len(core_rows),
        "modular_crosschecks": modular,
        "exact_core_rank": len(selected_1009),
        "exact_core_left_nullity": len(core_rows) - len(selected_1009),
        "exact_core_minor_determinant": str(determinant),
        "exact_solution_terms": len(solution),
        "exact_solution_denominator_lcm": denominator_lcm,
        "exact_augmented_replay": True,
        "term_deletion_mutation_fired": True,
        "solution": [[column, str(coefficient)]
                     for column, coefficient in sorted(solution.items())
                     if coefficient],
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("legacy27 K6 augmented exact solve: PASS")
    print("terms:", result["exact_solution_terms"])
    print("determinant:", result["exact_core_minor_determinant"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
