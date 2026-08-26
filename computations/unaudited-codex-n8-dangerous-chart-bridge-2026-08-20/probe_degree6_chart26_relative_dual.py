#!/usr/bin/env python3
"""Pull back the two-row d6 dual over a discovery prime.

This constructs a functional on every row through degree five in the frozen
target-incident component, together with lambda=e(r_plus)-e(r_minus) in
degree six, and verifies it against all 4,513 lower and 53,228 minimum-d5
source columns.  Equal small lifts at several primes are only an exact-Q
candidate until the integer replay is run.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LK_PATH = HERE / "probe_degree6_chart26_lower_kernel.py"
SPEC = importlib.util.spec_from_file_location("lower_kernel", LK_PATH)
LK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LK)
PROBE = LK.PROBE
BASE = LK.BASE
R_MINUS = bytes.fromhex("00041962759496bcc6dbe0ee")
R_PLUS = bytes.fromhex("00042374757c94bcc6dbe7ee")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def lambda_tail(tail, prime):
    return (tail.get(R_PLUS, 0) - tail.get(R_MINUS, 0)) % prime


def solve_augmented_transpose(vectors, tails, prime):
    """Solve mu*A_j = -lambda*T_j, with four free mu coordinates zero."""
    basis = {}
    for raw, tail in zip(vectors, tails):
        vector = LK.clean(raw, prime)
        rhs = (-lambda_tail(tail, prime)) % prime
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, prime)
                vector = LK.clean(Counter({i: x * inverse
                                           for i, x in vector.items()}), prime)
                rhs = rhs * inverse % prime
                basis[pivot] = (vector, rhs)
                break
            base_vector, base_rhs = basis[pivot]
            LK.add_scaled(vector, base_vector, -value, prime)
            rhs = (rhs - value * base_rhs) % prime
        else:
            require(rhs == 0, "lambda does not annihilate the lower kernel")
    require(len(basis) == 1239, "augmented transpose rank changed")
    solution = Counter()
    for pivot in sorted(basis, reverse=True):
        vector, rhs = basis[pivot]
        value = (rhs - sum(coefficient * solution.get(index, 0)
                           for index, coefficient in vector.items()
                           if index != pivot)) % prime
        if value:
            solution[pivot] = value
    for vector, tail in zip(vectors, tails):
        require(sum(value * solution.get(index, 0)
                    for index, value in vector.items()) % prime
                == (-lambda_tail(tail, prime)) % prime,
                "augmented transpose solution failed replay")
    return basis, solution


def lift_to_literal_rows(component, augmented_mu, prime):
    lower_count = len(component["lower_rows"])
    non_singleton = component["non_singleton"]
    quotient_position = component["quotient_position"]
    triple_columns = component["triple_columns"]
    triple_basis = component["triple_basis"]
    singleton = component["singleton"]

    mu_lower = Counter({component["lower_rows"][index]: value
                        for index, value in augmented_mu.items()
                        if index < lower_count})
    mu5 = Counter()

    # Singleton minimum-d5 columns directly pin their leading row values.
    for row, column in singleton.items():
        value = (-lambda_tail(LK.degree_tail(column, 6), prime)) % prime
        if value:
            mu5[row] = value
    for column in component["columns5"]:
        outputs = LK.degree_tail(column, 5)
        if sum(outputs.values()) == 1:
            row = next(iter(outputs))
            require((sum(count * mu5.get(candidate, 0)
                         for candidate, count in outputs.items())
                     + lambda_tail(LK.degree_tail(column, 6), prime)) % prime
                    == 0, "duplicate singleton d5 equation disagrees")

    # The 42 quotient/non-pivot row values are exactly the augmented free
    # coordinates.  The 215 pivot values follow from normalized triple-basis
    # equations, descending in pivot order.
    for non_index, position in quotient_position.items():
        value = augmented_mu.get(lower_count + position, 0)
        if value:
            mu5[non_singleton[non_index]] = value

    triple_rhs = []
    for column in triple_columns:
        rhs = (-lambda_tail(LK.degree_tail(column, 6), prime)) % prime
        for row, count in LK.degree_tail(column, 5).items():
            if row in singleton:
                rhs = (rhs - count * mu5.get(row, 0)) % prime
        triple_rhs.append(rhs)
    for pivot in sorted(triple_basis, reverse=True):
        vector, combination = triple_basis[pivot]
        rhs = sum(value * triple_rhs[index]
                  for index, value in combination.items()) % prime
        value = (rhs - sum(coefficient * mu5.get(
            non_singleton[index], 0
        ) for index, coefficient in vector.items() if index != pivot)) % prime
        if value:
            mu5[non_singleton[pivot]] = value
        else:
            mu5.pop(non_singleton[pivot], None)

    # Literal modular checks on every source column in the frozen component.
    for column in component["columns5"]:
        pairing = lambda_tail(LK.degree_tail(column, 6), prime)
        pairing += sum(count * mu5.get(row, 0)
                       for row, count in LK.degree_tail(column, 5).items())
        require(pairing % prime == 0,
                "literal minimum-d5 dual replay failed")
    for column in component["lower_columns"]:
        pairing = lambda_tail(LK.degree_tail(column, 6), prime)
        for output in BASE.column_rows(column):
            degree = BASE.row_degree(output, PROBE.ANCHORS)
            row = PROBE.canonical_row(output)
            if degree in (0, 2, 3, 4):
                pairing += mu_lower.get(row, 0)
            elif degree == 5:
                pairing += mu5.get(row, 0)
        require(pairing % prime == 0, "literal lower dual replay failed")
    return mu_lower, mu5


def audit(prime, write_results):
    component = LK.build_frozen_degree5_component(prime)
    augmented, tails, _corrections, definition_sha = (
        LK.corrected_lower_columns(component, prime)
    )
    basis, augmented_mu = solve_augmented_transpose(
        augmented, tails, prime
    )
    mu_lower, mu5 = lift_to_literal_rows(component, augmented_mu, prime)
    centered = lambda value: value if value <= prime // 2 else value - prime
    lower_ledger = [[row.hex(), centered(value)]
                    for row, value in sorted(mu_lower.items())]
    d5_ledger = [[row.hex(), centered(value)]
                 for row, value in sorted(mu5.items())]
    core = {
        "status": "UNAUDITED modular component-relative dual",
        "chart": 26,
        "legacy_one_based_chart": 29,
        "prime": prime,
        "d6_lambda": [[R_MINUS.hex(), -1], [R_PLUS.hex(), 1]],
        "target_pairing": -8,
        "augmented_rank_free_dimension": [len(basis), 1243 - len(basis)],
        "mu_lower": lower_ledger,
        "mu_degree5": d5_ledger,
        "mu_support": [len(lower_ledger), len(d5_ledger)],
        "corrected_lower_definition_sha256": definition_sha,
        "literal_source_columns_checked": [
            len(component["lower_columns"]), len(component["columns5"]), 9835
        ],
        "component_relative_only": True,
        "exact_integer_replay_proved": False,
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if write_results:
        out = HERE / f"results_degree6_chart26_relative_dual_p{prime}.json"
        out.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
    print("relative dual modular replay: PASS", flush=True)
    print("support lower/d5:", len(lower_ledger), len(d5_ledger), flush=True)
    print("result sha256:", core["result_sha256"], flush=True)
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    audit(args.prime, args.write_results)


if __name__ == "__main__":
    main()
