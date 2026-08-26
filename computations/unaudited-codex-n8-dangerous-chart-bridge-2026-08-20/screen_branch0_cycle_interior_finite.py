#!/usr/bin/env python3
"""Exact finite-field screen of the gauge-fixed k4-cycle interior.

This is discovery only.  It solves the four upper cofactor rows linearly in
a1..a4 for each choice of six live b/d parameters, then solves three rows in
a0 and two rows in a5 before checking all sixteen literal rows and H.
"""

from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
from itertools import product
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


INTERIOR = load("n8_cycle_interior_finite_source",
                HERE / "probe_branch0_cycle_interior.py")


def evaluate(poly, values, prime):
    answer = 0
    for exponent, coefficient in poly.items():
        coefficient = int(coefficient.numerator) * pow(
            int(coefficient.denominator), -1, prime)
        term = coefficient % prime
        for value, power in zip(values, exponent):
            if power:
                term = term * pow(value, power, prime) % prime
        answer += term
    return answer % prime


def affine_solutions(rows, targets, fixed, prime):
    """Enumerate an affine linear solution set in the target coordinates."""
    zeroed = list(fixed)
    for target in targets:
        zeroed[target] = 0
    matrix = []
    for poly in rows:
        constant = evaluate(poly, zeroed, prime)
        line = []
        for target in targets:
            test = list(zeroed)
            test[target] = 1
            line.append((evaluate(poly, test, prime) - constant) % prime)
        matrix.append(line + [(-constant) % prime])

    rank = 0
    pivots = []
    for column in range(len(targets)):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(value * inverse) % prime
                        for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scalar = matrix[row][column]
            matrix[row] = [(left - scalar * right) % prime
                           for left, right in zip(matrix[row], matrix[rank])]
        pivots.append(column)
        rank += 1
    if any(not any(row[:-1]) and row[-1] for row in matrix):
        return ()
    free = tuple(column for column in range(len(targets))
                 if column not in pivots)
    answers = []
    for free_values in product(range(prime), repeat=len(free)):
        solution = [0] * len(targets)
        for column, value in zip(free, free_values):
            solution[column] = value
        for row_index in range(rank - 1, -1, -1):
            pivot = pivots[row_index]
            solution[pivot] = (matrix[row_index][-1]
                               - sum(matrix[row_index][column]
                                     * solution[column]
                                     for column in free)) % prime
        answer = list(fixed)
        for target, value in zip(targets, solution):
            answer[target] = value
        answers.append(tuple(answer))
    return tuple(answers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prime", type=int, nargs="?", default=7)
    parser.add_argument("--stop-first", action="store_true")
    parser.add_argument("--zero-edges", nargs="*", type=int,
                        choices=(1, 2, 3, 4), default=())
    args = parser.parse_args()
    prime = args.prime
    rows, hafnian = INTERIOR.data()
    row_map = {label: poly for label, poly, _ in rows}
    upper = tuple(row_map[f"cofactor_{edge}_0"] for edge in (1, 2, 3, 4))
    solve_a0 = tuple(row_map[label] for label in
                     ("t_012", "t_013", "cofactor_5_0"))
    solve_a5 = tuple(row_map[label] for label in ("t_023", "t_123"))
    all_rows = tuple(poly for _, poly, _ in rows)

    base_indices = (6, 7, 8, 9, 10, 11)  # b0,b1,b3,d1,d3,d4
    counts = {"base": 0, "delta_zero": 0, "upper": 0,
              "interior_upper": 0, "a0": 0, "a5": 0,
              "full_zero": 0, "H_live": 0}
    witnesses = []
    failure_histogram = Counter()
    failure_sets = []
    required_zero = frozenset(args.zero_edges)
    for base in product(range(1, prime), repeat=6):
        counts["base"] += 1
        values = [0] * 12
        for index, value in zip(base_indices, base):
            values[index] = value
        b0, b1, b3, d1, d3, d4 = base
        if (b1 * d3 + b3 * d1 * d4) % prime == 0:
            counts["delta_zero"] += 1
        for with_upper in affine_solutions(upper, (1, 2, 3, 4),
                                           values, prime):
            counts["upper"] += 1
            if any(with_upper[index] == 0 for index in (1, 2, 3, 4)):
                continue
            c_factors = {
                1: (1 + with_upper[1] * with_upper[9]) % prime,
                2: (1 + with_upper[2]) % prime,
                3: (1 + with_upper[3] * with_upper[10]) % prime,
                4: (1 + with_upper[4] * with_upper[11]) % prime,
            }
            if frozenset(edge for edge, factor in c_factors.items()
                         if not factor) != required_zero:
                continue
            counts["interior_upper"] += 1
            for with_a0 in affine_solutions(solve_a0, (0,), with_upper, prime):
                counts["a0"] += 1
                for candidate in affine_solutions(solve_a5, (5,), with_a0,
                                                  prime):
                    counts["a5"] += 1
                    failed = tuple(label for label, poly, _ in rows
                                   if evaluate(poly, candidate, prime))
                    if failed:
                        failure_histogram.update(failed)
                        failure_sets.append(frozenset(failed))
                        continue
                    counts["full_zero"] += 1
                    h_value = evaluate(hafnian, candidate, prime)
                    if not h_value:
                        continue
                    counts["H_live"] += 1
                    witnesses.append({"values": list(candidate), "H": h_value})
                    if args.stop_first:
                        print("prime / counts / witness:", prime, counts,
                              witnesses[-1])
                        return
    print("prime / counts / witnesses:", prime, counts, witnesses[:10])
    print("failure histogram:", dict(failure_histogram.most_common()))
    failure_labels = sorted(set().union(*failure_sets)) if failure_sets else []
    for size in range(1, len(failure_labels) + 1):
        covers = [choice for choice in __import__("itertools").combinations(
            failure_labels, size)
            if all(failure & set(choice) for failure in failure_sets)]
        if covers:
            print("minimum failure-row covers:", size, covers[:20])
            break


if __name__ == "__main__":
    main()
