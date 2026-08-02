#!/usr/bin/env python3
"""Source-faithful degree-two/three Bockstein test for chart 25."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import base64
import importlib.util
import json
import math
import os
from pathlib import Path
import zlib


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load("n8_chart25_degree2", "analyze_n8_chart25_degree2_lift.py")
DEG3 = load("n8_chart25_degree3", "analyze_n8_chart25_degree3_lift.py")
QQ = Fraction
PRIMES = tuple(int(value) for value in
               os.environ.get("CHART25_PRIMES", "1009").split(","))


def degree3_seed_rows(old_columns, initial_residual):
    rows = set(initial_residual)
    for position, column in enumerate(old_columns, 1):
        for actual_column in BASE.column_orbit(column):
            for row in BASE.column_rows(actual_column):
                if BASE.row_degree(row) == 3:
                    rows.add(BASE.canonical_row(row))
        if position % 500 == 0:
            print("old tails", position, "/", len(old_columns),
                  "degree3 seed rows", len(rows), flush=True)
    return rows


def block_entries(old, column, degree2_index, degree3_index):
    entries = {}
    if old:
        entries.update(BASE.invariant_entries(column, degree2_index))
    offset = len(degree2_index)
    for index, value in DEG3.invariant_entries(column, degree3_index).items():
        entries[offset + index] = value
    return entries


def eliminate(columns, degree2_rows, degree3_rows,
              degree2_residual, degree3_residual, prime):
    degree2_index = {row: index for index, row in enumerate(degree2_rows)}
    degree3_index = {row: index for index, row in enumerate(degree3_rows)}
    pivots = {}
    pivot_metadata = {}
    pivot_origin = Counter()
    total = len(columns[0]) + len(columns[1])
    position = 0
    for old, family in ((True, columns[0]), (False, columns[1])):
        for column in family:
            position += 1
            reductions = []
            vector = {
                index: value % prime
                for index, value in block_entries(
                    old, column, degree2_index, degree3_index
                ).items() if value % prime
            }
            while vector:
                pivot = min(vector)
                value = vector[pivot]
                if pivot not in pivots:
                    inverse = pow(value, -1, prime)
                    pivots[pivot] = {
                        index: coefficient * inverse % prime
                        for index, coefficient in vector.items()
                    }
                    pivot_origin["old" if old else "new"] += 1
                    pivot_metadata[pivot] = (
                        position - 1, value, tuple(reductions)
                    )
                    break
                reductions.append((pivot, value))
                for index, coefficient in pivots[pivot].items():
                    new = (vector.get(index, 0) - value * coefficient) % prime
                    if new:
                        vector[index] = new
                    else:
                        vector.pop(index, None)
            if position % 1000 == 0:
                print("block eliminate", position, "/", total,
                      "rank", len(pivots), "origins", dict(pivot_origin),
                      flush=True)
    target = {
        degree2_index[row]: (-value.numerator
                             * pow(value.denominator, -1, prime)) % prime
        for row, value in degree2_residual.items()
    }
    offset = len(degree2_rows)
    target.update({
        offset + degree3_index[row]: (-value.numerator
                                      * pow(value.denominator, -1, prime))
                                     % prime
        for row, value in degree3_residual.items()
    })
    target_factors = {}
    while target:
        pivot = min(target)
        if pivot not in pivots:
            break
        value = target[pivot]
        target_factors[pivot] = value
        for index, coefficient in pivots[pivot].items():
            new = (target.get(index, 0) - value * coefficient) % prime
            if new:
                target[index] = new
            else:
                target.pop(index, None)
    remainder_layers = Counter(
        2 if index < offset else 3 for index in target
    )
    solution = {}
    pivot_coefficients = dict(target_factors)
    for pivot in sorted(pivot_metadata, reverse=True):
        coefficient = pivot_coefficients.pop(pivot, 0) % prime
        if not coefficient:
            continue
        column_index, leading_value, reductions = pivot_metadata[pivot]
        scalar = coefficient * pow(leading_value, -1, prime) % prime
        solution[column_index] = scalar
        for earlier_pivot, factor in reductions:
            value = (pivot_coefficients.get(earlier_pivot, 0)
                     - scalar * factor) % prime
            if value:
                pivot_coefficients[earlier_pivot] = value
            else:
                pivot_coefficients.pop(earlier_pivot, None)
    if pivot_coefficients:
        raise RuntimeError("unresolved pivot coefficients in modular solve")
    signature = sha256(json.dumps([
        (pivot, metadata[0])
        for pivot, metadata in sorted(pivot_metadata.items())
    ], separators=(",", ":")).encode("ascii")).hexdigest()
    return (len(pivots), pivot_origin, target, remainder_layers,
            solution, signature)


def crt(residues, primes):
    value = 0
    modulus = 1
    for residue, prime in zip(residues, primes):
        correction = (residue - value) * pow(modulus, -1, prime) % prime
        value += correction * modulus
        modulus *= prime
    return value % modulus, modulus


def rational_reconstruct(residue, modulus):
    if not residue:
        return QQ(0)
    bound = math.isqrt(modulus // 2)
    old_remainder, remainder = modulus, residue
    old_denominator, denominator = 0, 1
    while remainder > bound:
        quotient = old_remainder // remainder
        old_remainder, remainder = (
            remainder, old_remainder - quotient * remainder
        )
        old_denominator, denominator = (
            denominator, old_denominator - quotient * denominator
        )
    numerator = remainder
    if denominator < 0:
        numerator = -numerator
        denominator = -denominator
    if (not denominator or denominator > bound or abs(numerator) > bound
            or math.gcd(numerator, denominator) != 1
            or (residue * denominator - numerator) % modulus):
        raise RuntimeError("rational reconstruction bound exhausted")
    return QQ(numerator, denominator)


def reconstruct_solutions(solutions):
    support = set().union(*map(set, solutions))
    reconstructed = {}
    modulus = math.prod(PRIMES)
    for index in support:
        residue, checked_modulus = crt(
            [solution.get(index, 0) for solution in solutions], PRIMES
        )
        if checked_modulus != modulus:
            raise RuntimeError("CRT modulus mismatch")
        value = rational_reconstruct(residue, modulus)
        if value:
            reconstructed[index] = value
    for index, value in reconstructed.items():
        for prime, solution in zip(PRIMES, solutions):
            expected = (value.numerator
                        * pow(value.denominator, -1, prime)) % prime
            if solution.get(index, 0) != expected:
                raise RuntimeError("rational reconstruction replay failed")
    return reconstructed, modulus


def exact_actual_replay(columns, solution):
    actual2, _ = BASE.averaged_degree2_residual()
    actual3, _ = BASE.corrected_residual_at_degree(3, {})
    residuals = {2: dict(actual2), 3: dict(actual3)}
    combined = columns[0] + columns[1]
    for position, (index, scalar) in enumerate(solution.items(), 1):
        for actual_column in BASE.column_orbit(combined[index]):
            for row in BASE.column_rows(actual_column):
                degree = BASE.row_degree(row)
                if degree not in residuals:
                    continue
                value = residuals[degree].get(row, QQ(0)) + scalar
                if value:
                    residuals[degree][row] = value
                else:
                    residuals[degree].pop(row, None)
        if position % 1000 == 0:
            print("exact actual replay", position, "/", len(solution),
                  "remaining", {degree: len(rows)
                                 for degree, rows in residuals.items()},
                  flush=True)
    if any(residuals.values()):
        raise RuntimeError("exact actual degree-two/three replay failed")


def encoded_certificate(columns, solution):
    combined = columns[0] + columns[1]
    payload = [
        ["".join(map(str, combined[index][0])),
         list(combined[index][1]), value.numerator, value.denominator]
        for index, value in sorted(solution.items())
    ]
    raw = json.dumps(payload, separators=(",", ":")).encode("ascii")
    compressed = zlib.compress(raw, 9)
    return (base64.b85encode(compressed).decode("ascii"),
            sha256(raw).hexdigest(), len(raw), len(compressed))


def main():
    _, residual2 = BASE.averaged_degree2_residual()
    rows2, columns2, layers2 = BASE.close_leading(residual2)
    _, residual3 = BASE.corrected_residual_at_degree(3, {})
    seeds3 = degree3_seed_rows(columns2, residual3)
    print("degree3 Bockstein seeds", len(seeds3),
          "initial residual", len(residual3), flush=True)
    rows3, columns3, layers3 = DEG3.close_leading(seeds3)
    solutions = []
    signatures = []
    for prime in PRIMES:
        print("start prime", prime, flush=True)
        (rank, origins, remainder, remainder_layers,
         solution, signature) = eliminate(
            (columns2, columns3), rows2, rows3, residual2, residual3, prime
        )
        solutions.append(solution)
        signatures.append(signature)
        print({
            "prime": prime,
            "degree2_rows": len(rows2),
            "degree2_columns": len(columns2),
            "degree2_layers": layers2,
            "degree3_rows": len(rows3),
            "degree3_columns": len(columns3),
            "degree3_layers": layers3,
            "block_rank": rank,
            "pivot_origins": dict(origins),
            "source_faithful_consistent": not remainder,
            "remainder_support": len(remainder),
            "remainder_layers": dict(remainder_layers),
            "solution_support": len(solution),
            "pivot_signature": signature,
        }, flush=True)
    if len(set(signatures)) != 1:
        raise RuntimeError("pivot structure changed across primes")
    if all(not remainder for remainder in (remainder,)):
        rational_solution, modulus = reconstruct_solutions(solutions)
        values = Counter(rational_solution.values())
        denominator_lcm = math.lcm(*(
            value.denominator for value in rational_solution.values()
        ))
        print("rational reconstruction modulus", modulus,
              "support", len(rational_solution),
              "denominator lcm", denominator_lcm,
              "distinct values", len(values), flush=True)
        print("most common rational values", values.most_common(20), flush=True)
        exact_actual_replay((columns2, columns3), rational_solution)
        print("chart25 degree-three exact actual replay: PASS", flush=True)
        certificate, digest, raw_size, compressed_size = encoded_certificate(
            (columns2, columns3), rational_solution
        )
        print("certificate sha256", digest, "raw/compressed",
              raw_size, compressed_size, flush=True)
        print("CERTIFICATE_B85=" + certificate, flush=True)


if __name__ == "__main__":
    main()
