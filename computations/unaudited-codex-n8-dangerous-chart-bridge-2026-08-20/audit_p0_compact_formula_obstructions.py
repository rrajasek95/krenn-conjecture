#!/usr/bin/env python3
"""Referee compact determinant/Hafnian-product formulae proposed for P0."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, permutations, product
import importlib.util
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
T2_PATH = HERE / "audit_orbit0_t2_pivot_setup.py"
SPEC = importlib.util.spec_from_file_location("orbit0_p0_compact", T2_PATH)
T2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(T2)
INPUT = HERE / "results_orbit0_cutoff9_sparse_r8.json"
OUT = HERE / "results_p0_compact_formula_obstructions.json"
PRIME = 1009


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def build_p0():
    raw = json.loads(INPUT.read_text())
    p0 = {}
    for row_hex, numerator, denominator in raw["residual"]:
        representative = bytes.fromhex(row_hex)
        orbit = T2.row_orbit(representative)
        coefficient = Fraction(numerator, denominator) / len(orbit)
        for row in orbit:
            anchors = [cell for cell in row if cell in T2.ANCHORS]
            if T2.BASE.CELLS[anchors[0]][2] != 0:
                continue
            residual = list(row)
            for cell in anchors:
                residual.remove(cell)
            p0[bytes(residual)] = int(coefficient)
    require(len(p0) == 49392, "P0 support changed")
    return tuple(sorted(p0.items()))


BITS = tuple(product(range(2), repeat=4))
WORDS = tuple(tuple(colour for bit in bits for colour in (1 + bit, 2 - bit))
              for bits in BITS)
BALANCED = tuple(indices for indices in combinations_with_replacement(range(16), 4)
                 if all(sum(BITS[index][pair] for index in indices) == 2
                        for pair in range(4)))
require(len(BALANCED) == 60, "balanced quartic census changed")


def evaluate(p0, seed, prime=PRIME, zero_physical=False):
    rng = random.Random(seed)
    values = [rng.randrange(1, prime) for _ in T2.BASE.CELLS]
    if zero_physical:
        for cell_id, (u, v, _a, _b) in enumerate(T2.BASE.CELLS):
            if (u, v) in T2.M0:
                values[cell_id] = 0

    hafnians = []
    for word in WORDS:
        total = 0
        for row in T2.BASE.word_terms(word):
            term = 1
            for cell in row:
                term = term * values[cell] % prime
            total = (total + term) % prime
        hafnians.append(total)
    p0_value = 0
    for row, coefficient in p0:
        term = coefficient
        for cell in row:
            term = term * values[cell] % prime
        p0_value = (p0_value + term) % prime
    quartics = []
    for indices in BALANCED:
        term = 1
        for index in indices:
            term = term * hafnians[index] % prime
        quartics.append(term)
    return hafnians, quartics, p0_value * p0_value % prime


def determinant_mod(matrix, prime):
    matrix = [row[:] for row in matrix]
    determinant = 1
    sign = 1
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column] % prime), None)
        if pivot is None:
            continue
        if pivot != rank:
            matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
            sign *= -1
        pivot_value = matrix[rank][column] % prime
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        matrix[rank] = [value * inverse % prime for value in matrix[rank]]
        for row in range(rank + 1, len(matrix)):
            if matrix[row][column] % prime:
                factor = matrix[row][column] % prime
                matrix[row] = [(left - factor * right) % prime
                               for left, right in zip(matrix[row], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    if len(matrix) != len(matrix[0]) or rank != len(matrix):
        return rank, 0
    return rank, determinant * sign % prime


def det4(matrix, prime):
    value = 0
    for permutation in permutations(range(4)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(4) for j in range(i + 1, 4))
        term = 1
        for row, column in enumerate(permutation):
            term = term * matrix[row][column] % prime
        value = (value + (-term if inversions % 2 else term)) % prime
    return value


def flattening_determinants(hafnians):
    answers = []
    for left_pairs, right_pairs in (((0, 1), (2, 3)),
                                    ((0, 2), (1, 3)),
                                    ((0, 3), (1, 2))):
        matrix = []
        for left_bits in product(range(2), repeat=2):
            row = []
            for right_bits in product(range(2), repeat=2):
                bits = [0] * 4
                for pair, bit in zip(left_pairs, left_bits):
                    bits[pair] = bit
                for pair, bit in zip(right_pairs, right_bits):
                    bits[pair] = bit
                row.append(hafnians[BITS.index(tuple(bits))])
            matrix.append(row)
        answers.append(det4(matrix, PRIME))
    return answers


def main():
    p0 = build_p0()
    evaluations = [evaluate(p0, 41000 + sample) for sample in range(61)]
    source_matrix = [quartics for _hafnians, quartics, _target in evaluations]
    augmented = [quartics + [target]
                 for _hafnians, quartics, target in evaluations]
    # A 60x60 nonzero source minor and a 61x61 nonzero augmented determinant
    # are integer rank witnesses because all evaluation points are integer
    # lifts of their residues.
    source_rank, source_det = determinant_mod([row[:] for row in source_matrix[:60]],
                                              PRIME)
    augmented_rank, augmented_det = determinant_mod(augmented, PRIME)
    require(source_rank == 60 and source_det
            and augmented_rank == 61 and augmented_det,
            "balanced quartic rank witness changed")

    flattening_controls = []
    for zero_physical in (False, True):
        hafnians, _quartics, target = evaluate(
            p0, 93000 + int(zero_physical), zero_physical=zero_physical
        )
        determinants = flattening_determinants(hafnians)
        require(all(value != target for value in determinants),
                "a flattening determinant unexpectedly equals P0^2")
        flattening_controls.append({
            "physical_pair_cells_zero": zero_physical,
            "P0_square": target,
            "three_flattening_determinants": determinants,
        })

    result = {
        "status": "UNAUDITED exact rank/counterevaluation compact-formula obstruction",
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "prime": PRIME,
        "alternating_words": len(WORDS),
        "balanced_quartic_H_monomials": len(BALANCED),
        "source_evaluation_minor_rank": source_rank,
        "source_evaluation_minor_determinant_mod_prime": source_det,
        "augmented_evaluation_minor_rank": augmented_rank,
        "augmented_evaluation_minor_determinant_mod_prime": augmented_det,
        "quartic_H_span_conclusion": (
            "P0^2 is not a quartic polynomial in the sixteen alternating "
            "hafnians. Port multigrading restricts every possible quartic to "
            "the 60 balanced word multisets; the frozen 61-point integer "
            "evaluation matrix has source rank 60 and augmented rank 61, as "
            "witnessed by nonzero determinants modulo 1009."
        ),
        "flattening_controls": flattening_controls,
        "determinant_conclusion": (
            "In particular P0^2 is not any of the three natural 4x4 "
            "flattening determinants of the 2x2x2x2 alternating-H tensor, "
            "and no 4x4 determinant of linear combinations of those H entries "
            "can follow merely by invertible row/column basis changes."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("P0 compact-formula obstruction referee: PASS")
    print("balanced source/augmented ranks:", source_rank, augmented_rank)
    print("determinants mod 1009:", source_det, augmented_det)
    print("flattening controls:", flattening_controls)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
