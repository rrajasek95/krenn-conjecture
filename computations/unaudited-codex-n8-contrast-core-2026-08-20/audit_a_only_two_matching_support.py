#!/usr/bin/env python3
"""Exclude a-only contrast zeros on unions of at most two matchings."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
             "audit_dangerous_charts.py")
OUT = HERE / "results_a_only_two_matching_support.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_module("n8_a_only_base", BASE_PATH)
Q = Fraction
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
RELATIVE_TYPES = {
    "1+1+1+1": M0,
    "2+1+1": ((0, 2), (1, 3), (4, 5), (6, 7)),
    "2+2": ((0, 2), (1, 3), (4, 6), (5, 7)),
    "3+1": ((0, 2), (1, 4), (3, 5), (6, 7)),
    "4": ((0, 2), (1, 4), (3, 6), (5, 7)),
}
# Twice the coefficient of a_uv in D(direction_left,direction_right) on the
# slice b=c=h=0.  A common factor 2^-4 is irrelevant to every P_sigma=0.
K = ((2, 1, -1), (1, 0, -1), (-1, -1, 0))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def full_assignments():
    answer = []
    for counts in ((2, 3, 3), (3, 2, 3), (3, 3, 2)):
        answer.extend(word for word in product(range(3), repeat=8)
                      if tuple(word.count(kind) for kind in range(3)) == counts)
    require(len(answer) == len(set(answer)) == 1680,
            "full S3 assignment count changed")
    return tuple(answer)


def matching_coefficient(assignment, matching):
    answer = 1
    for u, v in matching:
        answer *= K[assignment[u]][assignment[v]]
    return answer


def rank(rows, modulus=None):
    basis = {}
    for input_row in rows:
        row = list(input_row)
        if modulus:
            row = [value % modulus for value in row]
        else:
            row = list(map(Q, row))
        while True:
            pivot = next((index for index, value in enumerate(row) if value),
                         None)
            if pivot is None:
                break
            if pivot not in basis:
                if modulus:
                    inverse = pow(row[pivot], -1, modulus)
                    row = [(value * inverse) % modulus for value in row]
                else:
                    value = row[pivot]
                    row = [entry / value for entry in row]
                basis[pivot] = row
                break
            factor = row[pivot]
            if modulus:
                row = [(entry - factor * other) % modulus
                       for entry, other in zip(row, basis[pivot])]
            else:
                row = [entry - factor * other
                       for entry, other in zip(row, basis[pivot])]
    return len(basis)


def independent_rows(rows, target_rank):
    selected = []
    current_rank = 0
    for index, row in enumerate(rows):
        trial = selected + [row]
        new_rank = rank(trial)
        if new_rank > current_rank:
            selected.append(row)
            current_rank = new_rank
            if current_rank == target_rank:
                return selected, index
    raise RuntimeError("coefficient matrix did not reach full column rank")


def determinant(matrix):
    matrix = [list(map(int, row)) for row in matrix]
    n = len(matrix)
    sign = 1
    denominator = 1
    for pivot in range(n - 1):
        swap = next((row for row in range(pivot, n)
                     if matrix[row][pivot]), None)
        if swap is None:
            return 0
        if swap != pivot:
            matrix[pivot], matrix[swap] = matrix[swap], matrix[pivot]
            sign *= -1
        value = matrix[pivot][pivot]
        for row in range(pivot + 1, n):
            for column in range(pivot + 1, n):
                numerator = (matrix[row][column] * value
                             - matrix[row][pivot] * matrix[pivot][column])
                require(numerator % denominator == 0,
                        "Bareiss division ceased to be exact")
                matrix[row][column] = numerator // denominator
        denominator = value
    return sign * matrix[n - 1][n - 1] if n else 1


def main():
    assignments = full_assignments()
    records = []
    for relative_type, second in RELATIVE_TYPES.items():
        edges = frozenset(M0) | frozenset(second)
        supported_matchings = tuple(
            matching for matching in BASE.PM8
            if frozenset(matching) <= edges
        )
        rows = [tuple(matching_coefficient(assignment, matching)
                      for matching in supported_matchings)
                for assignment in assignments]
        column_count = len(supported_matchings)
        exact_rank = rank(rows)
        require(exact_rank == column_count,
                ("matching coefficient columns became dependent",
                 relative_type, exact_rank, column_count))
        require(rank(rows, 1009) == rank(rows, 1013) == exact_rank,
                "modular rank control disagrees with exact rank")
        selected_rows, terminal_index = independent_rows(rows, column_count)
        det = determinant(selected_rows)
        require(det != 0, "selected exact minor vanished")
        selected_assignments = []
        scan = []
        current_rank = 0
        for index, row in enumerate(rows[:terminal_index + 1]):
            new_rank = rank(scan + [row])
            if new_rank > current_rank:
                scan.append(row)
                selected_assignments.append(assignments[index])
                current_rank = new_rank
        require(scan == selected_rows and len(scan) == column_count,
                "selected row provenance replay failed")
        records.append({
            "relative_cycle_partition": relative_type,
            "union_edges": len(edges),
            "supported_perfect_matchings": column_count,
            "exact_rank": exact_rank,
            "rank_mod_1009": rank(rows, 1009),
            "rank_mod_1013": rank(rows, 1013),
            "minor_determinant": det,
            "minor_assignments": ["".join(map(str, assignment))
                                  for assignment in selected_assignments],
            "minor_rows": [list(row) for row in selected_rows],
            "matchings": [[list(edge) for edge in matching]
                          for matching in supported_matchings],
        })

    # Deleting edges only deletes matching columns, and a subset of an
    # independent column family remains independent.  Thus the census also
    # covers every graph contained in one of these five union types.
    hostile = list(records[-1]["minor_rows"])
    hostile[0] = [0] * len(hostile[0])
    require(determinant(hostile) == 0,
            "zero-row mutation did not kill the exact minor")

    result = {
        "status": "UNAUDITED exact a-only two-matching support obstruction",
        "contrast_slice": "b_uv=c_uv=h_uv=0 for all 28 edges",
        "coefficient_matrix": [list(row) for row in K],
        "full_s3_contractions": len(assignments),
        "relative_union_types": len(records),
        "records": records,
        "conclusion": (
            "On the a-only slice, no point whose occupied physical graph is "
            "contained in the union of at most two perfect matchings can "
            "annihilate all 1,680 contrast contractions while Haf(a) is "
            "nonzero. For every union type the contraction coefficients of "
            "its supported perfect matchings are linearly independent; all "
            "P_sigma=0 therefore force every matching weight to zero."
        ),
        "target_scope": (
            "Here B=C=0 and Heron=-Haf(a)^3. Hence this excludes a Heron-"
            "nonzero common zero on these support strata, but not on denser "
            "a-only graphs or in the full 112-variable contrast space."
        ),
        "covariance": (
            "The five relative cycle partitions exhaust S8-orbits of an "
            "ordered pair of perfect matchings. The full 1,680-contraction "
            "family and a-coordinate slice are S8-stable."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("a-only two-matching support obstruction: PASS")
    for record in records:
        print(record["relative_cycle_partition"],
              record["supported_perfect_matchings"],
              record["minor_determinant"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
