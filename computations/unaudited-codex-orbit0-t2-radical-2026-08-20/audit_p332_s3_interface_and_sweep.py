#!/usr/bin/env python3
"""Exact S3-stable P332 census and two hostile uniform-point sweeps.

The fixed (3,3,2) orbit is not colour-permutation stable.  This audit uses
all three placements of the multiplicity two, computes the exact Q-rank of
their literal 256-word coefficient tensors, and evaluates every contraction
both in 112 contrast coordinates and after a concrete 252-cell lift.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
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
OUT = HERE / "results_p332_s3_interface_and_sweep.json"

COUNTS = ((3, 3, 2), (3, 2, 3), (2, 3, 3))
POINTS = {
    "oriented_rank_one": (1, 0, 0, 1),
    "symmetric_fixed_placement": (-12, 8, -10, 0),
}
VECTORS = ((1, -1, 0), (1, 0, -1), (0, 1, -1))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def assignments(counts):
    raw = tuple(direction for direction, count in enumerate(counts)
                for _ in range(count))
    return sorted(set(permutations(raw)))


def tensor_row(assignment):
    """Expand directions p,q,q-p in the p/q tensor-word basis."""
    row = {0: 1}
    for site, direction in enumerate(assignment):
        if direction == 0:
            continue
        if direction == 1:
            row = {mask | (1 << site): coefficient
                   for mask, coefficient in row.items()}
            continue
        updated = Counter()
        for mask, coefficient in row.items():
            updated[mask] -= coefficient
            updated[mask | (1 << site)] += coefficient
        row = {mask: coefficient for mask, coefficient in updated.items()
               if coefficient}
    return row


def rational_rank(rows):
    pivots = {}
    for original in rows:
        row = {column: Fraction(coefficient)
               for column, coefficient in original.items()}
        while row:
            pivot = min(row)
            coefficient = row[pivot]
            if pivot not in pivots:
                row = {column: value / coefficient
                       for column, value in row.items()}
                pivots[pivot] = row
                break
            basis = pivots[pivot]
            for column, value in basis.items():
                updated = row.get(column, Fraction(0)) - coefficient * value
                if updated:
                    row[column] = updated
                else:
                    row.pop(column, None)
    return pivots


def raw_cell_matrix(point):
    # A right inverse of the difference-plane coordinate map.  In the dual
    # basis to p,q the lower-right block is [[a,pXq],[qXp,b]].
    a, b, c, h = map(Fraction, point)
    pq = (a + b - c + h) / 2
    qp = (a + b - c - h) / 2
    matrix = [[Fraction(0)] * 3 for _ in range(3)]
    matrix[1][1] = a
    matrix[1][2] = pq
    matrix[2][1] = qp
    matrix[2][2] = b
    return matrix


def bilinear(matrix, left, right):
    return sum(left[a] * right[b] * matrix[a][b]
               for a in range(3) for b in range(3))


def contrast_coordinates(matrix):
    a = bilinear(matrix, VECTORS[0], VECTORS[0])
    b = bilinear(matrix, VECTORS[1], VECTORS[1])
    c = bilinear(matrix, VECTORS[2], VECTORS[2])
    h = (bilinear(matrix, VECTORS[0], VECTORS[1])
         - bilinear(matrix, VECTORS[1], VECTORS[0]))
    return a, b, c, h


def word_hafnian(word, matrices):
    total = 0
    for matching in P332.PM8:
        term = 1
        for edge in matching:
            term *= matrices[edge][word[edge[0]]][word[edge[1]]]
        total += term
    return total


def raw_word_values(point):
    matrix = raw_cell_matrix(point)
    matrices = {edge: matrix for edge in P332.EDGES}
    return {word: word_hafnian(word, matrices)
            for word in product(range(3), repeat=8)}


def source_evaluation(assignment, values):
    return sum(coefficient * values[word]
               for word, coefficient in
               P332.raw_source_words(assignment).items())


def main() -> None:
    groups = [assignments(counts) for counts in COUNTS]
    require([len(group) for group in groups] == [560, 560, 560],
            "one multiplicity-placement orbit changed")
    all_assignments = [assignment for group in groups for assignment in group]
    require(len(set(all_assignments)) == 1680,
            "multiplicity placements overlap")

    tensor_rows = [tensor_row(assignment) for assignment in all_assignments]
    fixed_ranks = [len(rational_rank(tensor_row(assignment)
                                     for assignment in group))
                   for group in groups]
    pivots = rational_rank(tensor_rows)
    require(fixed_ranks == [173, 173, 173] and len(pivots) == 229,
            "exact contraction rank changed")

    support_histogram = Counter()
    coefficient_histogram = Counter()
    polynomial_digests = []
    for assignment in all_assignments:
        poly = P332.quartic(assignment)
        support_histogram[len(poly)] += 1
        coefficient_histogram.update(poly.values())
        polynomial_digests.append(
            sha256(repr(sorted(poly.items())).encode()).hexdigest()
        )
    require(len(set(polynomial_digests)) == 1680,
            "S3-stable generator list has duplicates")
    require(support_histogram == {12_228: 1680},
            "generator support changed")

    sweeps = {}
    for name, candidate in POINTS.items():
        point = tuple(candidate) * 28
        raw_values = raw_word_values(candidate)
        by_placement = []
        for group_number, group in enumerate(groups):
            values = Counter()
            raw = Counter()
            for assignment in group:
                stored = P332.direct_polarized_value(assignment, point)
                literal = source_evaluation(assignment, raw_values)
                require(stored == 16 * literal,
                        "contrast point differs from literal 256-row source")
                values[stored] += 1
                raw[literal] += 1
            by_placement.append({
                "multiplicities": list(COUNTS[group_number]),
                "zero": values[0],
                "nonzero": 560 - values[0],
                "distinct_values": len(values),
                "minimum_stored_16P": min(values),
                "maximum_stored_16P": max(values),
                "literal_zero": raw[0],
            })
        matrix = raw_cell_matrix(candidate)
        require(contrast_coordinates(matrix) == tuple(map(Fraction, candidate)),
                "raw 3x3 lift does not realize a candidate")
        A, B, C = (105 * candidate[i] ** 4 for i in range(3))
        factors = (A + B - C, A + C - B, B + C - A)
        heron = factors[0] * factors[1] * factors[2]
        require(heron != 0, "hostile candidate lost its nonzero Heron value")
        sweeps[name] = {
            "point_per_edge_a_b_c_h": list(candidate),
            "raw_3x3_cell_matrix_per_edge": [
                [[value.numerator, value.denominator] for value in row]
                for row in matrix
            ],
            "placement_census": by_placement,
            "all_1680_zero": all(item["zero"] == 560
                                 for item in by_placement),
            "A_B_C": [A, B, C],
            "Heron_factors": list(factors),
            "Heron_value": heron,
        }
    require(not sweeps["oriented_rank_one"]["all_1680_zero"]
            and not sweeps["symmetric_fixed_placement"]["all_1680_zero"],
            "a hostile candidate unexpectedly became a counterexample")
    require(sweeps["oriented_rank_one"]["placement_census"][0]["nonzero"] == 219
            and sweeps["symmetric_fixed_placement"]["placement_census"][0]["zero"] == 560,
            "orientation/fixed-placement hostile regressions did not fire")

    result = {
        "status": "UNAUDITED exact S3-stable P332 interface and hostile sweep",
        "interface_sha256": sha256(INTERFACE_PATH.read_bytes()).hexdigest(),
        "multiplicity_placements": [list(counts) for counts in COUNTS],
        "generators_per_placement": [len(group) for group in groups],
        "generator_count_before_dedupe": len(all_assignments),
        "generator_count_after_dedupe": len(set(polynomial_digests)),
        "generator_support_histogram": {
            str(k): v for k, v in sorted(support_histogram.items())
        },
        "fixed_placement_exact_Q_ranks": fixed_ranks,
        "S3_stable_exact_Q_rank": len(pivots),
        "rank_coordinate_space": 256,
        "rank_argument": (
            "Expand p,q,q-p at each site in the p/q tensor-word basis and "
            "perform exact Fraction common-echelon reduction. Literal H_w "
            "supports are disjoint, while the 112 contrast coordinates are "
            "a surjective linear image of the raw edge cells, so this is "
            "also the exact rank of the quartic contractions."
        ),
        "candidate_sweeps": sweeps,
        "raw_rows_checked_per_generator": 256,
        "literal_source_checks": len(all_assignments),
        "generator_digest": sha256("".join(polynomial_digests).encode()).hexdigest(),
        "conclusion": (
            "Neither uniform candidate annihilates the complete S3-stable "
            "1680-generator family. The oriented point fails because h "
            "changes sign under endpoint reversal; the symmetric point "
            "annihilates only one placement of the multiplicity two. These "
            "are hostile regressions, not radical counterexamples."
        ),
        "scope": (
            "The counterexample sweep is not a proof that Heron lies in the "
            "radical. A negative Macaulay computation is likewise restricted "
            "unless the full homogeneous component is closed."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("S3-stable P332 interface/sweep: PASS")
    print("fixed/all ranks:", fixed_ranks, len(pivots))
    print("candidate all-zero:", {name: item["all_1680_zero"]
                                   for name, item in sweeps.items()})
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
