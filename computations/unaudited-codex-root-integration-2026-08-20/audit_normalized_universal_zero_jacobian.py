#!/usr/bin/env python3
"""Jacobian audit at the universal all-Hafnians-zero normalized point."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = (HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
             / "audit_dangerous_charts.py")
SPEC = importlib.util.spec_from_file_location("universal_zero_jacobian_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
OUT = HERE / "results_normalized_universal_zero_jacobian.json"
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
EXCEPTIONAL_EDGE = (0, 2)
PRIMES = (1009, 1013)


def reduce_row(row, basis, prime):
    row = {column: value % prime for column, value in row.items() if value % prime}
    while row:
        pivot = min(row)
        if pivot not in basis:
            inverse = pow(row[pivot], -1, prime)
            normalized = {column: value * inverse % prime
                          for column, value in row.items()}
            basis[pivot] = normalized
            return True
        factor = row[pivot]
        for column, value in basis[pivot].items():
            updated = (row.get(column, 0) - factor * value) % prime
            if updated:
                row[column] = updated
            else:
                row.pop(column, None)
    return False


def word_value_and_gradient(word, values, variable_index, prime):
    total = 0
    gradient = Counter()
    for matching_term in BASE.word_terms(word):
        term = 1
        for cell in matching_term:
            term = term * values[cell] % prime
        total = (total + term) % prime
        for cell in matching_term:
            index = variable_index.get(cell)
            if index is not None:
                gradient[index] = (gradient[index]
                                   + term * pow(values[cell], -1, prime)) % prime
    return total, dict(gradient)


def run_prime(prime):
    anchors = frozenset(
        BASE.CELL_ID[(u, v, colour, colour)]
        for colour in BASE.COLORS for u, v in M0
    )
    variables = tuple(cell for cell in range(len(BASE.CELLS)) if cell not in anchors)
    variable_index = {cell: index for index, cell in enumerate(variables)}
    values = []
    for u, v, _a, _b in BASE.CELLS:
        values.append((-6 if (u, v) == EXCEPTIONAL_EDGE else 1) % prime)
    assert all(values[cell] == 1 for cell in anchors)

    mixed_basis = {}
    pure_gradients = []
    zero_values = 0
    for word in product(BASE.COLORS, repeat=BASE.N):
        value, gradient = word_value_and_gradient(
            word, values, variable_index, prime
        )
        assert value == 0
        zero_values += 1
        if len(set(word)) == 1:
            pure_gradients.append(gradient)
        else:
            reduce_row(gradient, mixed_basis, prime)
    mixed_rank = len(mixed_basis)
    augmented = {pivot: row.copy() for pivot, row in mixed_basis.items()}
    pure_rank_increase = sum(
        reduce_row(gradient, augmented, prime) for gradient in pure_gradients
    )
    return {
        "prime": prime,
        "normalized_variables": len(variables),
        "all_hafnian_values_zero": zero_values,
        "mixed_jacobian_rank": mixed_rank,
        "tangent_dimension_upper_linear": len(variables) - mixed_rank,
        "pure_gradient_rank_increase": pure_rank_increase,
        "mixed_plus_pure_jacobian_rank": len(augmented),
        "pivot_columns": sorted(mixed_basis),
    }


def main():
    runs = [run_prime(prime) for prime in PRIMES]
    assert runs[0]["mixed_jacobian_rank"] == runs[1]["mixed_jacobian_rank"]
    assert runs[0]["pure_gradient_rank_increase"] == runs[1]["pure_gradient_rank_increase"]
    result = {
        "status": "UNAUDITED exact modular Jacobian audit at universal zero",
        "point": (
            "anchors are 1; every endpoint-colour cell on uv equals z_uv; "
            "z_02=-6 and all other z_uv=1"
        ),
        "runs": runs,
        "scope_guard": (
            "Jacobian ranks describe only the Zariski tangent space at this "
            "one exact T=0 point. They are not a global radical certificate."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("normalized universal-zero Jacobian audit: PASS")
    for run in runs:
        print(run["prime"], run["mixed_jacobian_rank"],
              run["pure_gradient_rank_increase"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
