#!/usr/bin/env python3
"""Independent small-matrix replay for the Rust modular accelerator.

This checker deliberately reads the producer JSONL again, replays a Rust
solution against the original multiplicity-aware columns, and computes the
canonical common-echelon remainder in Python.  It is not an exact-Q replay of
the large anchor-K problem; it only qualifies the modular accelerator.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIME = 1009
MODULUS = PRIME


def clean(vector):
    return {index: value % MODULUS for index, value in vector.items()
            if value % MODULUS}


def add_scaled(left, right, scale):
    for index, value in right.items():
        updated = (left.get(index, 0) + scale * value) % MODULUS
        if updated:
            left[index] = updated
        else:
            left.pop(index, None)


def read_interface(path):
    with path.open() as handle:
        header = json.loads(next(handle))
        columns = []
        for expected, line in enumerate(handle):
            record = json.loads(line)
            assert record["index"] == expected
            # Counter is load-bearing: repeated rows add, rather than forming
            # a set.  The synthetic fixture contains one such duplicate.
            columns.append(clean(Counter(dict()) + Counter(
                index for index, value in record["entries"]
                for _ in range(value)
            )))
    target = clean({index: numerator * pow(denominator, -1, MODULUS)
                    for index, numerator, denominator in header["target"]})
    return header, columns, target


def read_interface_general(path):
    """Same reader without assuming positive entries or expanding values."""
    with path.open() as handle:
        header = json.loads(next(handle))
        columns = []
        for expected, line in enumerate(handle):
            record = json.loads(line)
            assert record["index"] == expected
            vector = Counter()
            for index, value in record["entries"]:
                vector[index] += value
            columns.append(clean(vector))
    target = Counter()
    for index, numerator, denominator in header["target"]:
        target[index] += numerator * pow(denominator, -1, MODULUS)
    return header, columns, clean(target)


def python_echelon(columns, target):
    basis = {}
    provenance = {}
    for number, raw in enumerate(columns):
        vector = dict(raw)
        proof = {number: 1}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, MODULUS)
                basis[pivot] = clean({i: v * inverse
                                      for i, v in vector.items()})
                provenance[pivot] = clean({i: v * inverse
                                           for i, v in proof.items()})
                break
            add_scaled(vector, basis[pivot], -value)
            add_scaled(proof, provenance[pivot], -value)
    residual = dict(target)
    solution = {}
    # Complete common reduction: do not halt at a smaller free coordinate.
    while True:
        pivot = next((index for index in sorted(residual)
                      if index in basis), None)
        if pivot is None:
            break
        value = residual[pivot]
        add_scaled(residual, basis[pivot], -value)
        add_scaled(solution, provenance[pivot], value)
    return basis, residual, solution


def replay(columns, solution, target, remainder):
    actual = {}
    for number, coefficient in solution.items():
        add_scaled(actual, columns[number], coefficient)
    add_scaled(actual, remainder, 1)
    assert actual == target, "Rust solution/remainder does not replay"


def audit_case(interface_path, result_path, expectation):
    global MODULUS
    rust = json.loads(result_path.read_text())
    previous_modulus = MODULUS
    MODULUS = rust["prime"]
    header, columns, target = read_interface_general(interface_path)
    basis, residual, solution = python_echelon(columns, target)
    rust_residual = dict(rust["remainder"])
    rust_solution = dict(rust["solution"])
    assert rust["prime"] == MODULUS
    assert rust["row_count"] == header["row_count"]
    assert rust["column_count"] == header["column_count"] == len(columns)
    assert rust["rank"] == len(basis)
    assert rust_residual == residual
    assert rust_solution == solution
    replay(columns, rust_solution, target, rust_residual)
    assert rust["target_in_image"] == expectation["target_in_image"]
    assert rust_residual == expectation["remainder"]
    if rust_solution:
        mutation = dict(rust_solution)
        first = min(mutation)
        mutation[first] = (mutation[first] + 1) % MODULUS
        try:
            replay(columns, mutation, target, rust_residual)
        except AssertionError:
            mutation_fired = True
        else:
            mutation_fired = False
        assert mutation_fired
    answer = {
        "interface": interface_path.name,
        "interface_sha256": sha256(interface_path.read_bytes()).hexdigest(),
        "rank": len(basis),
        "remainder": sorted(map(list, residual.items())),
        "solution": sorted(map(list, solution.items())),
        "python_rust_byte_equal_vectors": True,
        "literal_modular_replay": True,
        "solution_mutation_fired": True,
    }
    MODULUS = previous_modulus
    return answer


def crt(left, left_prime, right, right_prime):
    return (left + left_prime * (
        (right - left) * pow(left_prime, -1, right_prime) % right_prime
    )) % (left_prime * right_prime)


def rational_reconstruct(residue, modulus):
    """Unique small n/d with n == residue*d (mod modulus), if present."""
    bound = math.isqrt(modulus // 2)
    old_r, r = modulus, residue
    old_s, s = 0, 1
    while r and abs(r) > bound:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    if not r or not s:
        raise AssertionError("rational reconstruction failed")
    numerator, denominator = r, s
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    common = math.gcd(numerator, denominator)
    numerator //= common
    denominator //= common
    assert abs(numerator) <= bound and denominator <= bound
    assert (numerator - residue * denominator) % modulus == 0
    return Fraction(numerator, denominator)


def exact_dual_audit(interface_path, result_paths):
    modular = [json.loads(path.read_text()) for path in result_paths]
    primes = [record["prime"] for record in modular]
    assert primes == [1009, 1013]
    assert all(record["target_in_image"] is False for record in modular)
    assert modular[0]["left_dual_free_row"] == modular[1]["left_dual_free_row"]
    modular_duals = [dict(record["left_dual"]) for record in modular]
    support = sorted(set(modular_duals[0]) | set(modular_duals[1]))
    modulus = primes[0] * primes[1]
    exact_dual = {}
    for row in support:
        residue = crt(
            modular_duals[0].get(row, 0), primes[0],
            modular_duals[1].get(row, 0), primes[1],
        )
        coefficient = rational_reconstruct(residue, modulus)
        if coefficient:
            exact_dual[row] = coefficient

    with interface_path.open() as handle:
        header = json.loads(next(handle))
        rows_hex = header["rows_hex"]
        target = Counter()
        for row, numerator, denominator in header["target"]:
            target[row] += Fraction(numerator, denominator)
        column_count = 0
        max_exact_pairing_numerator = 0
        first_column = None
        for line in handle:
            record = json.loads(line)
            vector = Counter()
            for row, value in record["entries"]:
                vector[row] += value
            pairing = sum(exact_dual.get(row, 0) * value
                          for row, value in vector.items())
            assert pairing == 0, f"exact dual missed column {record['index']}"
            max_exact_pairing_numerator = max(
                max_exact_pairing_numerator, abs(pairing.numerator)
            )
            if first_column is None:
                first_column = vector
            column_count += 1
    exact_target_pairing = sum(exact_dual.get(row, 0) * value
                               for row, value in target.items())
    assert exact_target_pairing
    assert column_count == header["column_count"]
    for record, prime_value in zip(modular, primes):
        reduced = sum(
            (coefficient.numerator
             * pow(coefficient.denominator, -1, prime_value)
             * (target.get(row, 0).numerator % prime_value)
             * pow(target.get(row, 0).denominator, -1, prime_value))
            for row, coefficient in exact_dual.items()
        ) % prime_value
        assert reduced == record["left_dual_target_pairing"]

    # Hostile mutation: insert one unit at the certified free row into a
    # literal column; the exact annihilation check must immediately fail.
    free_row = modular[0]["left_dual_free_row"]
    mutated_pairing = sum(exact_dual.get(row, 0) * value
                          for row, value in first_column.items())
    mutated_pairing += exact_dual[free_row]
    assert mutated_pairing != 0

    result = {
        "status": "EXACT-Q DUAL FOR RESTRICTED DIRECT COMPONENT",
        "scope_guard": (
            "This obstructs only the serialized min-degree-six coupled "
            "columns. It is not a global anchor-K obstruction because "
            "lower-kernel degree-six tails are absent."
        ),
        "interface_sha256": sha256(interface_path.read_bytes()).hexdigest(),
        "rows": header["row_count"],
        "columns": column_count,
        "modular_primes": primes,
        "modular_ranks": [record["rank"] for record in modular],
        "modular_remainder_nonzeros": [
            record["target_remainder_nonzeros"] for record in modular
        ],
        "dual_free_row": free_row,
        "exact_dual_support": [
            {
                "row_index": row,
                "row_hex": rows_hex[row],
                "coefficient": str(coefficient),
            }
            for row, coefficient in sorted(exact_dual.items())
        ],
        "rational_reconstruction_modulus": modulus,
        "all_literal_columns_annihilated_over_Q": True,
        "exact_target_pairing": str(exact_target_pairing),
        "column_entry_mutation_fired": True,
        "maximum_exact_column_pairing_numerator": max_exact_pairing_numerator,
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return result


def projection_regression():
    basis_path = HERE / "fixtures/project_basis.jsonl"
    vectors_path = HERE / "fixtures/membership.jsonl"
    projected_path = HERE / "results_tiny_projected.jsonl"
    solution_path = HERE / "results_tiny_projected_solution.json"
    basis_header, basis_columns, _ = read_interface_general(basis_path)
    vector_header, vector_columns, target = read_interface_general(vectors_path)
    projected_header, projected_columns, projected_target = read_interface_general(projected_path)
    result = json.loads(solution_path.read_text())
    assert basis_header["row_count"] == vector_header["row_count"] == 4
    assert projected_header["source_free_rows"] == [0, 1, 3]
    assert projected_header["row_count"] == 3
    assert projected_target == {0: 2, 2: 1}
    assert projected_columns == [{0: 2}, {}, {2: 1}]
    assert result["target_in_image"] and dict(result["solution"]) == {0: 1, 2: 1}

    actual = {}
    for number, coefficient in dict(result["solution"]).items():
        add_scaled(actual, vector_columns[number], coefficient)
    lower_remainder = dict(target)
    add_scaled(lower_remainder, actual, -1)
    basis, final_remainder, basis_solution = python_echelon(
        basis_columns, lower_remainder
    )
    assert not final_remainder and basis_solution == {0: 1}
    mutation = dict(result["solution"])
    mutation.pop(min(mutation))
    mutated = {}
    for number, coefficient in mutation.items():
        add_scaled(mutated, vector_columns[number], coefficient)
    mutated_remainder = dict(target)
    add_scaled(mutated_remainder, mutated, -1)
    _basis, mutated_final, _solution = python_echelon(
        basis_columns, mutated_remainder
    )
    assert mutated_final
    return {
        "status": "PASS: common-echelon projection regression",
        "basis_rank": len(basis),
        "source_rows": 4,
        "quotient_rows": 3,
        "transfer_columns": 3,
        "projected_nonzero_columns": 2,
        "projected_solution": result["solution"],
        "back_substituted_basis_solution": sorted(map(list, basis_solution.items())),
        "literal_augmented_modular_replay": True,
        "solution_mutation_fired": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--exact-dual", nargs=3, metavar=("INTERFACE", "P1009", "P1013"))
    args = parser.parse_args()
    records = [
        audit_case(
            HERE / "fixtures/membership.jsonl",
            HERE / "results_tiny_membership.json",
            {"target_in_image": True, "remainder": {}},
        ),
        audit_case(
            HERE / "fixtures/early_stop.jsonl",
            HERE / "results_tiny_early_stop.json",
            {"target_in_image": False, "remainder": {1: 1}},
        ),
    ]
    projection = projection_regression()
    core = {
        "status": "PASS: modular accelerator qualification only",
        "prime": PRIME,
        "regressions": records,
        "projection_regression": projection,
        "scope_guard": "Rust modular discovery is not exact-Q membership",
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if args.write_results:
        (HERE / "results_regressions.json").write_text(
            json.dumps(core, indent=2, sort_keys=True) + "\n"
        )
    print("accelerator regressions: PASS")
    print("result sha256:", core["result_sha256"])
    if args.exact_dual:
        dual = exact_dual_audit(
            Path(args.exact_dual[0]),
            tuple(Path(item) for item in args.exact_dual[1:]),
        )
        if args.write_results:
            (HERE / "results_degree6_dual_exact.json").write_text(
                json.dumps(dual, indent=2, sort_keys=True) + "\n"
            )
        print("degree6 restricted exact dual: PASS")
        print("dual result sha256:", dual["result_sha256"])


if __name__ == "__main__":
    main()
