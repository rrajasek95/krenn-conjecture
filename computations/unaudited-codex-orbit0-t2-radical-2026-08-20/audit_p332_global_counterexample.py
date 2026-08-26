#!/usr/bin/env python3
"""Independent exact counterexample to the S3-stable P332 radical route."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
INTERFACE_PATH = HERE / "audit_p332_coordinate_interface.py"
SPEC = importlib.util.spec_from_file_location("p332_interface", INTERFACE_PATH)
P332 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P332)
OUT = HERE / "results_p332_global_counterexample.json"

COUNTS = ((3, 3, 2), (3, 2, 3), (2, 3, 3))
VECTORS = ((1, -1, 0), (1, 0, -1), (0, 1, -1))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def assignments(counts):
    raw = tuple(direction for direction, count in enumerate(counts)
                for _ in range(count))
    return sorted(set(permutations(raw)))


def raw_matrices(second_exception=False):
    matrices = {}
    for edge in P332.EDGES:
        matrix = [[0] * 3 for _ in range(3)]
        matrix[1][1] = 1
        if edge == (0, 1) or (second_exception and edge == (2, 3)):
            matrix[1][2] = 1
        matrices[edge] = matrix
    return matrices


def bilinear(matrix, left, right):
    return sum(left[a] * right[b] * matrix[a][b]
               for a in range(3) for b in range(3))


def coordinates(matrices):
    result = []
    for edge in P332.EDGES:
        matrix = matrices[edge]
        a = bilinear(matrix, VECTORS[0], VECTORS[0])
        b = bilinear(matrix, VECTORS[1], VECTORS[1])
        c = bilinear(matrix, VECTORS[2], VECTORS[2])
        h = (bilinear(matrix, VECTORS[0], VECTORS[1])
             - bilinear(matrix, VECTORS[1], VECTORS[0]))
        result.extend((a, b, c, h))
    return tuple(result)


def word_hafnian(word, matrices):
    total = 0
    for matching in P332.PM8:
        term = 1
        for edge in matching:
            term *= matrices[edge][word[edge[0]]][word[edge[1]]]
        total += term
    return total


def raw_word_values(matrices):
    return {word: word_hafnian(word, matrices)
            for word in product(range(3), repeat=8)}


def source_value(assignment, values):
    return sum(coefficient * values[word]
               for word, coefficient in P332.raw_source_words(assignment).items())


def matching_values(assignment, point):
    values = []
    for matching in P332.PM8:
        value = 1
        for edge in matching:
            form = P332.TWICE_FORM[(assignment[edge[0]], assignment[edge[1]])]
            value *= sum(form[i] * point[4 * P332.EDGE_ID[edge] + i]
                         for i in range(4))
        values.append(value)
    return values


def directional_hafnian(direction, point):
    assignment = (direction,) * 8
    # This is stored 16 times the directional Hafnian.
    return P332.direct_polarized_value(assignment, point) // 16


def main():
    groups = [assignments(counts) for counts in COUNTS]
    all_assignments = [assignment for group in groups for assignment in group]
    require(len(all_assignments) == 1680 and len(set(all_assignments)) == 1680,
            "S3-stable assignment census changed")

    matrices = raw_matrices(False)
    point = coordinates(matrices)
    baseline = (1, 0, 1, 0)
    exceptional = (1, 0, 0, 1)
    require(all(point[4 * i:4 * i + 4]
                == (exceptional if edge == (0, 1) else baseline)
                for i, edge in enumerate(P332.EDGES)),
            "raw lift does not realize the claimed contrast blocks")
    raw_values = raw_word_values(matrices)

    placement_census = []
    total_matching_terms = 0
    for counts, group in zip(COUNTS, groups):
        stored_histogram = Counter()
        raw_histogram = Counter()
        nonzero_matching_terms = 0
        for assignment in group:
            terms = matching_values(assignment, point)
            nonzero_matching_terms += sum(value != 0 for value in terms)
            total_matching_terms += len(terms)
            stored = sum(terms)
            raw = source_value(assignment, raw_values)
            require(stored == 16 * raw,
                    "contrast evaluation differs from raw256 source replay")
            stored_histogram[stored] += 1
            raw_histogram[raw] += 1
        require(stored_histogram == {0: 560}
                and raw_histogram == {0: 560}
                and nonzero_matching_terms == 0,
                "a P332 generator or matching term survives")
        placement_census.append({
            "multiplicities": list(counts),
            "generators": len(group),
            "stored_16P_value_histogram": {"0": 560},
            "literal_P_value_histogram": {"0": 560},
            "nonzero_matching_terms": nonzero_matching_terms,
        })

    A, B, C = (directional_hafnian(direction, point)
               for direction in range(3))
    factors = (A + B - C, A + C - B, B + C - A)
    heron = factors[0] * factors[1] * factors[2]
    require((A, B, C) == (105, 0, 90)
            and factors == (15, 195, -15)
            and heron == -43_875,
            "Heron target changed or vanished")

    # A second exceptional oriented edge can absorb both mandatory q sites;
    # this must break the termwise zero and guards the exceptional-edge count.
    mutated_matrices = raw_matrices(True)
    mutated_point = coordinates(mutated_matrices)
    mutated_raw = raw_word_values(mutated_matrices)
    mutated_nonzero = 0
    for assignment in all_assignments:
        stored = P332.direct_polarized_value(assignment, mutated_point)
        raw = source_value(assignment, mutated_raw)
        require(stored == 16 * raw, "mutation raw256 replay failed")
        mutated_nonzero += stored != 0
    require(mutated_nonzero > 0, "second-edge mutation did not fire")

    result = {
        "status": "UNAUDITED exact S3-stable P332 rational counterexample",
        "interface_sha256": sha256(INTERFACE_PATH.read_bytes()).hexdigest(),
        "raw_assignment": (
            "For every oriented edge u<v set x_uv^(11)=1; additionally set "
            "x_01^(12)=1; all other raw cells are zero."
        ),
        "ordinary_edge_a_b_c_h": list(baseline),
        "exceptional_edge": [0, 1],
        "exceptional_edge_a_b_c_h": list(exceptional),
        "ordinary_difference_matrix": [[1, 0], [0, 0]],
        "exceptional_difference_matrix": [[1, 1], [0, 0]],
        "placement_census": placement_census,
        "generators_checked": len(all_assignments),
        "matching_terms_checked": total_matching_terms,
        "raw_source_rows_checked_per_generator": 256,
        "A_B_C": [A, B, C],
        "Heron_factors": list(factors),
        "Heron_value": heron,
        "termwise_reason": (
            "Every assignment has at least two q-direction sites. Ordinary "
            "blocks support only pXp, and the one exceptional block supports "
            "only one additional right-q slot. Thus every one of the105 "
            "matching products is zero before summation."
        ),
        "second_exception_mutation_nonzero_generators": mutated_nonzero,
        "conclusion": (
            "All1680 contractions in the S3-stable (3,3,2) family vanish at "
            "an integral point where Heron is nonzero. Hence Heron is not in "
            "radical(J332_stable), and no positive power belongs to J332."
        ),
        "global_scope": (
            "This refutes only the contrast subideal. The point is not a "
            "common zero of all6558 original mixed Hafnians, so it does not "
            "refute the N=8 conjecture or the full mixed-ideal radical route."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("S3-stable P332 global counterexample: PASS")
    print("generators / matching terms:", len(all_assignments), total_matching_terms)
    print("A,B,C / Heron:", (A, B, C), heron)
    print("mutation nonzero:", mutated_nonzero)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
