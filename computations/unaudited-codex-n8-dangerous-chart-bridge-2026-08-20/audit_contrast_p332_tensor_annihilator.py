#!/usr/bin/env python3
"""Exact S8-module audit of the balanced-contrast tensor annihilator.

Use the ordered basis (p,q) of the two-dimensional colour-difference plane,
with r=q-p.  The 1680 site tensors having direction counts (3,3,2), with
all three choices of the doubled direction, span W in (Q^2)^{tensor 8}.
This checker proves rank(W)=229 and gives a compact exact basis of W^perp.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import json
from math import gcd, lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_contrast_p332_tensor_annihilator.json"
Q = Fraction
N = 8
DIRECTIONS = ((1, 0), (0, 1), (-1, 1))  # p, q, r=q-p
WORDS = tuple(product((0, 1), repeat=N))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
ASSIGNMENTS_BY_DOUBLED_KIND = tuple(
    tuple(sorted(set(permutations(tuple(
        kind
        for kind in range(3)
        for _ in range(2 if kind == doubled else 3)
    )))))
    for doubled in range(3)
)
ASSIGNMENTS = tuple(assignment for block in ASSIGNMENTS_BY_DOUBLED_KIND
                    for assignment in block)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def tensor_row(assignment: tuple[int, ...]) -> dict[int, int]:
    row = {0: 1}
    for site, direction in enumerate(assignment):
        updated = Counter()
        for prefix, coefficient in row.items():
            for bit, factor in enumerate(DIRECTIONS[direction]):
                if factor:
                    updated[(prefix << 1) | bit] += coefficient * factor
        row = {index: coefficient for index, coefficient in updated.items()
               if coefficient}
    return row


def dot(row: dict[int, int], vector: tuple[int, ...]) -> int:
    return sum(coefficient * vector[index]
               for index, coefficient in row.items())


def modular_rank(rows, columns: int, prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for source in rows:
        row = {index: int(value) % prime
               for index, value in source.items() if int(value) % prime}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                inverse = pow(row[pivot], -1, prime)
                row = {index: value * inverse % prime
                       for index, value in row.items() if value % prime}
                pivots[pivot] = row
                break
            factor = row[pivot]
            old = pivots[pivot]
            for index, value in old.items():
                new_value = (row.get(index, 0) - factor * value) % prime
                if new_value:
                    row[index] = new_value
                else:
                    row.pop(index, None)
    require(all(0 <= pivot < columns for pivot in pivots),
            "modular pivot outside matrix")
    return len(pivots)


def rref(matrix: list[list[int | Fraction]], columns: int):
    rows = [[Q(value) for value in row] for row in matrix]
    pivot_columns = []
    pivot_row = 0
    for column in range(columns):
        chosen = next((index for index in range(pivot_row, len(rows))
                       if rows[index][column]), None)
        if chosen is None:
            continue
        rows[pivot_row], rows[chosen] = rows[chosen], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [rows[index][j] - factor * rows[pivot_row][j]
                           for j in range(columns)]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows[:pivot_row], tuple(pivot_columns)


def integerize(vector: list[Fraction]) -> tuple[int, ...]:
    denominator = 1
    for value in vector:
        denominator = lcm(denominator, value.denominator)
    answer = [int(value * denominator) for value in vector]
    divisor = 0
    for value in answer:
        divisor = gcd(divisor, abs(value))
    if divisor:
        answer = [value // divisor for value in answer]
    first = next((value for value in answer if value), 1)
    if first < 0:
        answer = [-value for value in answer]
    return tuple(answer)


def nullspace(matrix: list[list[int | Fraction]], columns: int):
    reduced, pivots = rref(matrix, columns)
    free = tuple(column for column in range(columns)
                 if column not in pivots)
    answer = []
    for free_column in free:
        vector = [Q(0)] * columns
        vector[free_column] = Q(1)
        for row_index, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row_index][free_column]
        answer.append(integerize(vector))
    return tuple(answer), pivots


def dense_to_sparse(vector):
    return {index: value for index, value in enumerate(vector) if value}


def symmetric_vector(alpha: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(alpha[sum(word)] for word in WORDS)


def distinguished_vector(y: tuple[int, ...], distinguished: int):
    return tuple(y[8 * word[distinguished]
                   + sum(word) - word[distinguished]]
                 for word in WORDS)


def main() -> None:
    require(tuple(map(len, ASSIGNMENTS_BY_DOUBLED_KIND)) == (560, 560, 560)
            and len(ASSIGNMENTS) == len(set(ASSIGNMENTS)) == 1680,
            "full balanced-assignment census changed")
    rows = tuple(tensor_row(assignment) for assignment in ASSIGNMENTS)
    support_histogram = Counter(map(len, rows))
    require(support_histogram == {4: 560, 8: 1120},
            "raw tensor-row support changed")
    ranks = {prime: modular_rank(rows, 256, prime)
             for prime in (1009, 1013)}
    require(set(ranks.values()) == {229}, "raw tensor rank changed")

    # S8-fixed vectors are constant on the nine Hamming-weight layers.
    c8_rows = []
    for row in rows:
        aggregate = [0] * 9
        for index, coefficient in row.items():
            aggregate[sum(WORDS[index])] += coefficient
        c8_rows.append(aggregate)
    symmetric_basis, c8_pivots = nullspace(c8_rows, 9)
    require(len(c8_pivots) == 3 and len(symmetric_basis) == 6,
            "S8-fixed annihilator dimension changed")
    require(tuple(tuple(c8_rows[560 * doubled])
                  for doubled in range(3)) == (
                      (0, 0, 0, -1, 3, -3, 1, 0, 0),
                      (0, 0, -1, 3, -3, 1, 0, 0, 0),
                      (0, 0, 0, 1, -2, 1, 0, 0, 0),
                  ), "symmetric seed constraints changed")

    # S7 fixes site 0 and permutes sites 1,...,7.  Its fixed vectors have
    # coordinates y[e,k], where e is bit 0 and k is the remaining weight.
    c7_rows = []
    for row in rows:
        aggregate = [0] * 16
        for index, coefficient in row.items():
            word = WORDS[index]
            aggregate[8 * word[0] + sum(word) - word[0]] += coefficient
        c7_rows.append(aggregate)
    s7_basis, c7_pivots = nullspace(c7_rows, 16)
    require(len(c7_pivots) == 7 and len(s7_basis) == 9,
            "S7-fixed annihilator dimension changed")

    # Vanishing S8 Reynolds average cuts out the three standard highest
    # vectors inside the nine-dimensional S7-fixed annihilator.
    reynolds_zero = []
    for weight in range(9):
        equation = [0] * 16
        if weight <= 7:
            equation[weight] = 8 - weight
        if weight >= 1:
            equation[8 + weight - 1] = weight
        reynolds_zero.append(equation)
    standard_seeds, combined_pivots = nullspace(c7_rows + reynolds_zero, 16)
    require(len(combined_pivots) == 13 and len(standard_seeds) == 3,
            "standard highest-vector count changed")

    symmetric_full = tuple(symmetric_vector(alpha)
                           for alpha in symmetric_basis)
    standard_orbits = tuple(
        tuple(distinguished_vector(seed, distinguished)
              for distinguished in range(8))
        for seed in standard_seeds
    )
    require(all(all(sum(orbit[site][coordinate] for site in range(8)) == 0
                        for coordinate in range(256))
                    for orbit in standard_orbits),
            "a standard orbit acquired a trivial summand")
    require(all(modular_rank(map(dense_to_sparse, orbit), 256, 1009) == 7
                for orbit in standard_orbits),
            "a proposed standard copy does not have dimension seven")

    # Seven vectors from each orbit are independent; the eighth is minus
    # their sum.  Together with the six invariants they give all 27 vectors.
    annihilator_basis = (symmetric_full
                          + tuple(vector for orbit in standard_orbits
                                  for vector in orbit[:7]))
    require(len(annihilator_basis) == 27
            and modular_rank(map(dense_to_sparse, annihilator_basis),
                             256, 1009) == 27,
            "compact annihilator basis is not independent")
    require(all(dot(row, vector) == 0
                for row in rows for vector in annihilator_basis),
            "compact basis does not annihilate all 1680 raw tensors")
    # Rank(W)>=229 and dim(W^perp)>=27 force equality over Q.
    require(ranks[1009] + len(annihilator_basis) == 256,
            "rank/nullity closure changed")

    def pure_triple(alpha):
        a_value = alpha[0]
        b_value = alpha[8]
        c_value = sum((-1) ** weight
                      * __import__("math").comb(8, weight) * alpha[weight]
                      for weight in range(9))
        return (a_value, b_value, c_value)

    pure_matrix = tuple(pure_triple(alpha) for alpha in symmetric_basis)
    require(modular_rank((dense_to_sparse(row) for row in pure_matrix),
                         3, 1009) == 3,
            "pure A,B,C are not free on the invariant annihilator")
    require(all(vector[0] == vector[-1] == 0
                and sum((-1) ** sum(WORDS[index]) * value
                        for index, value in enumerate(vector)) == 0
                for orbit in standard_orbits for vector in orbit),
            "a standard component contributes to A, B, or C")

    result = {
        "status": "UNAUDITED exact full-P332 tensor-annihilator decomposition",
        "basis": "p=(1,0), q=(0,1), r=q-p=(-1,1)",
        "ambient_dimension": 256,
        "assignments_by_doubled_direction": [560, 560, 560],
        "row_support_histogram": {str(k): v
                                  for k, v in sorted(support_histogram.items())},
        "row_rank_mod_primes": {str(k): v for k, v in ranks.items()},
        "exact_Q_rank": 229,
        "exact_Q_annihilator_dimension": 27,
        "schur_weyl_ambient": {
            "[8]": {"multiplicity": 9, "dimension": 9},
            "[7,1]": {"multiplicity": 7, "dimension": 49},
            "[6,2]": {"multiplicity": 5, "dimension": 100},
            "[5,3]": {"multiplicity": 3, "dimension": 84},
            "[4,4]": {"multiplicity": 1, "dimension": 14},
        },
        "annihilator_S8_module": "6*[8] direct_sum 3*[7,1]",
        "W_isotypic_ranks": {
            "[8]": "3 of 9", "[7,1]": "28 of 49",
            "[6,2]": "100 of 100", "[5,3]": "84 of 84",
            "[4,4]": "14 of 14",
        },
        "symmetric_constraints_on_alpha_0_through_alpha_8": [
            list(c8_rows[560 * doubled]) for doubled in range(3)
        ],
        "symmetric_annihilator_basis": [list(row)
                                        for row in symmetric_basis],
        "standard_highest_vectors_y_e_k": [list(row)
                                            for row in standard_seeds],
        "standard_orbit_rule": (
            "For seed y and distinguished site d, the tensor coordinate at "
            "binary word epsilon is y[8*epsilon_d + "
            "weight(epsilon)-epsilon_d]. The eight site translates sum to "
            "zero and span one [7,1]; retain d=0,...,6 as a basis."
        ),
        "pure_evaluation_rule": {
            "A": "alpha_0",
            "B": "alpha_8",
            "C": "sum_{k=0}^8 (-1)^k binomial(8,k) alpha_k",
            "standard_components": "contribute zero to A, B, and C",
        },
        "pure_evaluation_matrix_on_symmetric_basis": [list(row)
                                                       for row in pure_matrix],
        "pure_evaluation_rank": 3,
        "scope": (
            "The 1680 balanced contractions alone leave A,B,C linearly "
            "unconstrained: their map from the six invariant annihilator "
            "coordinates has rank three. Any Heron radical theorem must use "
            "the nonlinear Hafnian/matchgate locus (or additional mixed "
            "equations), not linear representation theory alone."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("contrast P332 tensor annihilator: PASS")
    print("raw ranks:", ranks)
    print("annihilator: 6*[8] + 3*[7,1], dimension", 27)
    print("pure evaluation rank:", 3)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
