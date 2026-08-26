#!/usr/bin/env python3
"""Deterministic finite-field referee for the one-colour Q-support lemma.

Search points with all six block permanents -1 and all four complementary
triangle contractions 2.  Record the minimum number of nonzero self products
Q_s Q_sbar among points whose pure Hafnian (equivalently their sum) is
nonzero.  A <=2 point would be a modular warning/counterexample candidate;
absence in this bounded sample is only discovery evidence.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_one_colour_self_support_search.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
ORIENTATIONS = tuple(bits for bits in product((0, 1), repeat=4)
                     if bits[0] == 0)
PAIRINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        result.extend(((first, second),) + tail
                      for tail in perfect_matchings(rest))
    return tuple(result)


PM8 = perfect_matchings(tuple(range(8)))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
MATCHING_VARIABLES = tuple(tuple(
    4 * EDGE_INDEX[(u // 2, v // 2)] + 2 * (u % 2) + (v % 2)
    for u, v in matching if u // 2 != v // 2
) for matching in PM8)


def permanent(matrix, prime):
    a, b, c, d = matrix
    return (a * d + b * c) % prime


def entry(matrix, left_bit, right_bit):
    return matrix[2 * left_bit + right_bit]


def triangle(left, middle, right, prime):
    # Blocks M_ij=left, M_ik=middle, M_jk=right for i<j<k.
    return sum(entry(left, x, y) * entry(middle, 1 - x, z)
               * entry(right, 1 - y, 1 - z)
               for x, y, z in product((0, 1), repeat=3)) % prime


def q_value(blocks, bits, prime):
    result = 0
    for (i, j), (k, l) in PAIRINGS:
        result += entry(blocks[(i, j)], bits[i], bits[j]) * entry(
            blocks[(k, l)], bits[k], bits[l])
    return result % prime


def self_values(blocks, prime):
    values = []
    for bits in ORIENTATIONS:
        complement = tuple(1 - bit for bit in bits)
        values.append(q_value(blocks, bits, prime)
                      * q_value(blocks, complement, prime) % prime)
    return tuple(values)


def q_vector(blocks, prime):
    return tuple(q_value(blocks, tuple((index >> (3 - site)) & 1
                                       for site in range(4)), prime)
                 for index in range(16))


def h_gradient_mask(blocks, prime):
    values = tuple(value for edge in EDGES for value in blocks[edge])
    h = 0
    gradient = [0] * 24
    for variables in MATCHING_VARIABLES:
        zeros = [variable for variable in variables if not values[variable]]
        product_nonzero = 1
        for variable in variables:
            if values[variable]:
                product_nonzero = product_nonzero * values[variable] % prime
        if not zeros:
            h = (h + product_nonzero) % prime
            for variable in variables:
                gradient[variable] = (gradient[variable]
                                      + product_nonzero
                                      * pow(values[variable], -1, prime)) % prime
        elif len(zeros) == 1:
            gradient[zeros[0]] = (gradient[zeros[0]] + product_nonzero) % prime
    mask = sum((value != 0) << index for index, value in enumerate(gradient))
    return h, mask


def cofactor_zero_supports_permanents(cofactor_mask):
    orientations = []
    for block in range(6):
        allowed = (~(cofactor_mask >> (4 * block))) & 15
        choices = []
        if allowed & 9 == 9:
            choices.append(0)
        if allowed & 6 == 6:
            choices.append(1)
        if not choices:
            return ()
        orientations.append(tuple(choices))
    return tuple(orientations)


def search(prime, trials, seed):
    rng = random.Random(seed)
    matrices = tuple(matrix for matrix in product(range(prime), repeat=4)
                     if permanent(matrix, prime) == prime - 1)
    candidate_cache = {}

    def candidates(left, middle):
        key = (left, middle)
        if key not in candidate_cache:
            candidate_cache[key] = tuple(
                right for right in matrices
                if triangle(left, middle, right, prime) == 2 % prime
            )
        return candidate_cache[key]

    minimum = 9
    minimum_q_support = 17
    support_histogram = Counter()
    valid_points = 0
    nonzero_hafnian_points = 0
    witness = None
    q_support_witness = None
    low_q_points = 0
    cofactor_viable_low_q_points = 0
    cofactor_viable_low_q_witness = None
    cofactor_viable_class_histogram = Counter()
    cofactor_viable_witness_by_class = {}
    for _ in range(trials):
        m01 = rng.choice(matrices)
        m02 = rng.choice(matrices)
        c12 = candidates(m01, m02)
        if not c12:
            continue
        m12 = rng.choice(c12)
        m03 = rng.choice(matrices)
        c13 = candidates(m01, m03)
        if not c13:
            continue
        # Trying all M13 is important: the two final triangle equations can
        # be correlated even though each separately has many solutions.
        order13 = list(c13)
        rng.shuffle(order13)
        found_this_trial = False
        for m13 in order13:
            final_left = set(candidates(m02, m03))
            final_right = set(candidates(m12, m13))
            possible23 = sorted(final_left & final_right)
            if not possible23:
                continue
            # Inspect every compatible final block; these are usually few.
            for m23 in possible23:
                blocks = {(0, 1): m01, (0, 2): m02, (0, 3): m03,
                          (1, 2): m12, (1, 3): m13, (2, 3): m23}
                values = self_values(blocks, prime)
                q_values = q_vector(blocks, prime)
                active = sum(value != 0 for value in values)
                hafnian = sum(values) % prime
                valid_points += 1
                support_histogram[active] += 1
                if hafnian:
                    nonzero_hafnian_points += 1
                    coordinate_support = sum(value != 0 for value in q_values)
                    if coordinate_support <= 8:
                        low_q_points += 1
                        direct_h, cofactor_mask = h_gradient_mask(blocks, prime)
                        if direct_h != hafnian:
                            raise RuntimeError("direct Hafnian/identity mismatch")
                        orientations = cofactor_zero_supports_permanents(cofactor_mask)
                        if orientations:
                            cofactor_viable_low_q_points += 1
                            for bits in product(*orientations):
                                b01, b02, b03, b12, b13, b23 = bits
                                tail = (b12 ^ b01 ^ b02,
                                        b13 ^ b01 ^ b03,
                                        b23 ^ b02 ^ b03)
                                identifier = 4 * tail[0] + 2 * tail[1] + tail[2]
                                cofactor_viable_class_histogram[identifier] += 1
                                cofactor_viable_witness_by_class.setdefault(
                                    identifier, {
                                        "blocks": {f"{i}{j}": list(blocks[(i, j)])
                                                   for i, j in EDGES},
                                        "Q_0000_through_1111": list(q_values),
                                        "H": hafnian,
                                        "cofactor24": cofactor_mask,
                                        "orientation_bits": list(bits),
                                    }
                                )
                            if cofactor_viable_low_q_witness is None:
                                cofactor_viable_low_q_witness = {
                                    "blocks": {f"{i}{j}": list(blocks[(i, j)])
                                               for i, j in EDGES},
                                    "Q_0000_through_1111": list(q_values),
                                    "H": hafnian,
                                    "cofactor24": cofactor_mask,
                                    "cofactor_orientation_options": [list(row)
                                                                      for row in orientations],
                                }
                    if coordinate_support < minimum_q_support:
                        minimum_q_support = coordinate_support
                        q_support_witness = {
                            "blocks": {f"{i}{j}": list(blocks[(i, j)])
                                       for i, j in EDGES},
                            "Q_0000_through_1111": list(q_values),
                            "self_values": list(values),
                            "H": hafnian,
                        }
                    if active < minimum:
                        minimum = active
                        witness = {
                            "blocks": {f"{i}{j}": list(blocks[(i, j)])
                                       for i, j in EDGES},
                            "self_values": list(values),
                            "H": hafnian,
                        }
                    # Do not stop at the first two-active point: the refined
                    # candidate lemma concerns all 16 individual Q supports.

    return {
        "prime": prime,
        "matrix_count_permanent_minus_one": len(matrices),
        "random_outer_trials": trials,
        "valid_completed_points_inspected": valid_points,
        "nonzero_H_points": nonzero_hafnian_points,
        "active_self_pair_histogram": dict(sorted(support_histogram.items())),
        "minimum_active_with_H_nonzero": minimum if minimum <= 8 else None,
        "minimum_witness": witness,
        "found_active_at_most_two": minimum <= 2,
        "minimum_Q_coordinate_support_with_H_nonzero": (
            minimum_q_support if minimum_q_support <= 16 else None
        ),
        "minimum_Q_support_witness": q_support_witness,
        "H_nonzero_Q_support_at_most_8_points": low_q_points,
        "cofactor_viable_Q_support_at_most_8_points": (
            cofactor_viable_low_q_points
        ),
        "cofactor_viable_low_Q_witness": cofactor_viable_low_q_witness,
        "cofactor_viable_low_Q_switching_class_memberships": dict(
            sorted(cofactor_viable_class_histogram.items())
        ),
        "cofactor_viable_low_Q_witness_by_switching_class": dict(
            sorted(cofactor_viable_witness_by_class.items())
        ),
    }


def main():
    records = [search(3, 2000, 0x8503),
               search(5, 6000, 0x8505),
               search(7, 2500, 0x8507)]
    result = {
        "status": "UNAUDITED bounded finite-field referee",
        "constraints": (
            "perm(M_ij)=-1 for six blocks; C_ijk=2 for four triples"
        ),
        "identity_used": "under these constraints H=sum_s Q_s Q_sbar",
        "records": records,
        "scope": (
            "A <=2 witness is a modular warning; a negative bounded search "
            "is not a characteristic-zero proof."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for record in records:
        print("p", record["prime"], "valid", record["valid_completed_points_inspected"],
              "min active", record["minimum_active_with_H_nonzero"],
              "min Q support", record["minimum_Q_coordinate_support_with_H_nonzero"],
              "counterexample", record["found_active_at_most_two"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
