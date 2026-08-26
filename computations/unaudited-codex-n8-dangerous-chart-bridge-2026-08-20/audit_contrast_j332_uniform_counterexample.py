#!/usr/bin/env python3
"""Exact scope guard for proposed uniform-block J332 counterexamples.

The full ideal contains all three choices for which of p,q,r occurs twice,
not merely the original 560 assignments of count profile (3,3,2).
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations, product as cartesian_product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPORT_PATH = HERE / "export_contrast_j332_interface.py"
SPEC = importlib.util.spec_from_file_location("j332_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
OUT = HERE / "results_contrast_j332_uniform_scope_guard.json"
Q = Fraction
POINT = {"a": Q(1), "b": Q(0), "c": Q(0), "h": Q(1)}
OLD_SLICE_ONLY_POINT = {"a": Q(-12), "b": Q(8), "c": Q(-10), "h": Q(0)}
ASSIGNMENTS_BY_DOUBLED_KIND = tuple(
    tuple(sorted(set(permutations(tuple(
        kind
        for kind in range(3)
        for _ in range(2 if kind == doubled else 3)
    )))))
    for doubled in range(3)
)
ALL_ASSIGNMENTS = tuple(
    assignment
    for assignments in ASSIGNMENTS_BY_DOUBLED_KIND
    for assignment in assignments
)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def type_matrix(point=POINT):
    a, b, c, h = (point[name] for name in ("a", "b", "c", "h"))
    return (
        (a, (a + b - c + h) / 2, (-a + b - c + h) / 2),
        ((a + b - c - h) / 2, b, (-a + b + c + h) / 2),
        ((-a + b - c - h) / 2, (-a + b + c - h) / 2, c),
    )


def evaluate_p(assignment, matrix):
    return sum(product(matrix[assignment[u]][assignment[v]]
                       for u, v in matching)
               for matching in EXPORT.BASE.PM8)


def product(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def uniform_symbolic_polynomial():
    # Sparse polynomial in a,b,c, derived independently from the 105 PMs.
    same = {
        (0, 0): {(1, 0, 0): Q(1)},
        (1, 1): {(0, 1, 0): Q(1)},
        (2, 2): {(0, 0, 1): Q(1)},
    }
    cross = {
        (0, 1): {(1, 0, 0): Q(1, 2), (0, 1, 0): Q(1, 2),
                 (0, 0, 1): Q(-1, 2)},
        (0, 2): {(1, 0, 0): Q(-1, 2), (0, 1, 0): Q(1, 2),
                 (0, 0, 1): Q(-1, 2)},
        (1, 2): {(1, 0, 0): Q(-1, 2), (0, 1, 0): Q(1, 2),
                 (0, 0, 1): Q(1, 2)},
    }
    forms = dict(same)
    for (left, right), form in cross.items():
        forms[(left, right)] = forms[(right, left)] = form

    def multiply(left, right):
        answer = Counter()
        for le, lc in left.items():
            for re, rc in right.items():
                answer[tuple(le[i] + re[i] for i in range(3))] += lc * rc
        return answer

    assignment = EXPORT.ASSIGNMENTS[0]
    answer = Counter()
    for matching in EXPORT.BASE.PM8:
        term = Counter({(0, 0, 0): Q(1)})
        for u, v in matching:
            term = multiply(term, forms[(assignment[u], assignment[v])])
        answer.update(term)
    return Counter({exponent: coefficient for exponent, coefficient
                    in answer.items() if coefficient})


def evaluate_symbolic(polynomial, point):
    a, b, c = point["a"], point["b"], point["c"]
    return sum(coefficient * a ** exponent[0] * b ** exponent[1]
               * c ** exponent[2]
               for exponent, coefficient in polynomial.items())


def main() -> None:
    require(tuple(map(len, ASSIGNMENTS_BY_DOUBLED_KIND)) == (560, 560, 560)
            and len(ALL_ASSIGNMENTS) == len(set(ALL_ASSIGNMENTS)) == 1680,
            "full (3,3,2) assignment census changed")
    matrix = type_matrix()
    require(matrix == ((Q(1), Q(1), Q(0)),
                       (Q(0), Q(0), Q(0)),
                       (Q(-1), Q(-1), Q(0))),
            "uniform type bilinear matrix changed")

    # Independent raw-colour realization, identical on all 28 oriented edges:
    # x^{11}=x^{12}=1 and the other seven entries vanish.
    raw_x = ((Q(0), Q(0), Q(0)),
             (Q(0), Q(1), Q(1)),
             (Q(0), Q(0), Q(0)))
    raw_type_matrix = tuple(tuple(sum(
        Q(EXPORT.VECTORS[left][i]) * raw_x[i][j]
        * Q(EXPORT.VECTORS[right][j])
        for i in range(3) for j in range(3)
    ) for right in range(3)) for left in range(3))
    require(raw_type_matrix == matrix,
            "raw-colour realization does not induce the contrast point")

    raw_h = {}
    for word in cartesian_product(range(3), repeat=8):
        raw_h[word] = sum(product(raw_x[word[u]][word[v]]
                                 for u, v in matching)
                          for matching in EXPORT.BASE.PM8)

    by_doubled = []
    raw_mismatch_count = 0
    for assignments in ASSIGNMENTS_BY_DOUBLED_KIND:
        evaluations = Counter()
        for assignment in assignments:
            direct_value = evaluate_p(assignment, matrix)
            raw_value = sum(Q(sign) * raw_h[tuple(map(int, word))]
                            for word, sign in EXPORT.raw_provenance(assignment))
            raw_mismatch_count += (direct_value != raw_value)
            evaluations[direct_value] += 1
        by_doubled.append(evaluations)
    require(raw_mismatch_count == 0,
            "raw signed-256 contraction disagrees with contrast evaluation")
    nonzero_by_doubled = tuple(560 - histogram[Q(0)]
                               for histogram in by_doubled)
    require(nonzero_by_doubled == (177, 219, 219),
            "oriented-h hostile regression no longer rejects the candidate")

    # Hostile scope regression: the earlier h=0 point kills only one of the
    # three count placements, so a 560-generator check is insufficient.
    old_matrix = type_matrix(OLD_SLICE_ONLY_POINT)
    old_by_doubled = [Counter(evaluate_p(assignment, old_matrix)
                              for assignment in assignments)
                      for assignments in ASSIGNMENTS_BY_DOUBLED_KIND]
    require(sum(histogram == Counter({Q(0): 560})
                for histogram in old_by_doubled) == 1
            and all(len(histogram) == 1 for histogram in old_by_doubled),
            "slice-only hostile regression no longer detects the scope error")

    a_haf = 105 * POINT["a"] ** 4
    b_haf = 105 * POINT["b"] ** 4
    c_haf = 105 * POINT["c"] ** 4
    factors = (a_haf + b_haf - c_haf,
               a_haf + c_haf - b_haf,
               b_haf + c_haf - a_haf)
    heron = product(factors)
    require((a_haf, b_haf, c_haf) == (Q(105), Q(0), Q(0)),
            "directional Hafnians changed")
    require(factors == (Q(105), Q(105), Q(-105))
            and heron == Q(-1_157_625) != 0,
            "Heron evaluation changed or vanished")

    result = {
        "status": "UNAUDITED exact full-S3 J332 uniform-candidate scope guard",
        "interface_exporter_sha256": sha256(EXPORT_PATH.read_bytes()).hexdigest(),
        "point": {name: [value.numerator, value.denominator]
                  for name, value in POINT.items()},
        "point_rule": (
            "Every one of the 28 endpoint-ordered contrast blocks has the "
            "same coordinates (a,b,c,h)=(1,0,0,1). Equivalently, in raw "
            "colours x_uv^{11}=x_uv^{12}=1 and all other entries are zero."
        ),
        "type_bilinear_matrix": [
            [[value.numerator, value.denominator] for value in row]
            for row in matrix
        ],
        "count_placements": [
            {"doubled_kind": doubled,
             "assignment_count": len(ASSIGNMENTS_BY_DOUBLED_KIND[doubled]),
             "P332_value_histogram": {
                 str(value): count
                 for value, count in by_doubled[doubled].items()
             }}
            for doubled in range(3)
        ],
        "P332_generators_checked": len(ALL_ASSIGNMENTS),
        "raw256_replays_checked": len(ALL_ASSIGNMENTS),
        "raw256_mismatch_count": raw_mismatch_count,
        "nonzero_generator_count_by_doubled_kind": list(nonzero_by_doubled),
        "raw_colour_matrix": [
            [[value.numerator, value.denominator] for value in row]
            for row in raw_x
        ],
        "A_B_C": [[value.numerator, value.denominator]
                   for value in (a_haf, b_haf, c_haf)],
        "Heron_factors": [[value.numerator, value.denominator]
                           for value in factors],
        "Heron": [heron.numerator, heron.denominator],
        "hostile_slice_only_point": {
            "point": {name: [value.numerator, value.denominator]
                      for name, value in OLD_SLICE_ONLY_POINT.items()},
            "count_placement_histograms": [
                {str(value): count for value, count in histogram.items()}
                for histogram in old_by_doubled
            ],
            "purpose": (
                "Exactly one 560-generator slice vanishes. This mutation "
                "fails if the checker accidentally drops either of the "
                "other two choices of doubled contrast direction."
            ),
        },
        "conclusion": (
            "Neither proposed uniform point is a counterexample to the full "
            "1680-generator ideal. The h=1 point has Heron nonzero but fails "
            "177/219/219 generators according to the doubled direction. The "
            "h=0 point kills only one 560-generator slice. A full-S3, signed-"
            "orientation check is mandatory before any radical conclusion."
        ),
        "scope": (
            "This is a negative hostile regression only: it disproves two "
            "candidate points, not Heron radical containment or failure."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("uniform contrast J332 scope guard: PASS")
    print("nonzero P332 by doubled kind:", nonzero_by_doubled)
    print("raw signed-256 mismatches:", raw_mismatch_count)
    print("A,B,C:", a_haf, b_haf, c_haf)
    print("Heron:", heron)
    print("hostile old-point histograms:", old_by_doubled)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
