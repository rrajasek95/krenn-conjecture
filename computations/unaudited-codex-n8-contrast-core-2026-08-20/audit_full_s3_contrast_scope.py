#!/usr/bin/env python3
"""Referee the full S3-stable contrast family and two proposed zeros."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BRIDGE = (ROOT / "computations" /
          "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20")
INTERFACE_PATH = (ROOT / "computations" /
                  "unaudited-codex-orbit0-t2-radical-2026-08-20" /
                  "audit_p332_coordinate_interface.py")
UNIFORM_PATH = BRIDGE / "audit_contrast_j332_uniform_counterexample.py"
OUT = HERE / "results_full_s3_contrast_scope.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


INTERFACE = load_module("n8_full_s3_interface", INTERFACE_PATH)
UNIFORM = load_module("n8_full_s3_uniform", UNIFORM_PATH)
Q = Fraction
VECTORS = ((1, -1, 0), (1, 0, -1), (0, 1, -1))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def full_assignments():
    answer = []
    for counts in ((2, 3, 3), (3, 2, 3), (3, 3, 2)):
        answer.extend(word for word in product(range(3), repeat=8)
                      if tuple(word.count(kind) for kind in range(3)) == counts)
    require(len(answer) == len(set(answer)) == 1680,
            "full S3 assignment count changed")
    return tuple(answer)


def raw_source_signature(assignment):
    # The zero colour of the assigned difference vector at every site
    # recovers the assignment, proving literal contraction deduplication.
    zero_colour = {kind: VECTORS[kind].index(0) for kind in range(3)}
    return tuple(zero_colour[kind] for kind in assignment)


def pure_word_coefficient(assignment, colour):
    value = 1
    for kind in assignment:
        value *= VECTORS[kind][colour]
    return value


def evaluate_family(point, assignments):
    matrix = UNIFORM.type_matrix(point)
    histograms = {}
    for counts in ((2, 3, 3), (3, 2, 3), (3, 3, 2)):
        values = Counter(
            UNIFORM.evaluate_p(assignment, matrix)
            for assignment in assignments
            if tuple(assignment.count(kind) for kind in range(3)) == counts
        )
        histograms["".join(map(str, counts))] = values
    return matrix, histograms


def raw_lift_matrix():
    # In raw endpoint-colour coordinates this is alpha beta^T with
    # alpha=(0,-1,0), beta=(0,-1,-1).  It realizes [[1,1],[0,0]] in the
    # ordered (p,q) difference basis.
    return ((Q(0), Q(0), Q(0)),
            (Q(0), Q(1), Q(1)),
            (Q(0), Q(0), Q(0)))


def bilinear(left, matrix, right):
    return sum(left[a] * matrix[a][b] * right[b]
               for a in range(3) for b in range(3))


def main():
    assignments = full_assignments()
    signatures = {raw_source_signature(assignment)
                  for assignment in assignments}
    require(len(signatures) == 1680,
            "two full-S3 contractions have the same raw tensor signature")
    require(all(pure_word_coefficient(assignment, colour) == 0
                for assignment in assignments for colour in range(3)),
            "a full-S3 contraction retains a pure source word")

    proposed = {"a": Q(1), "b": Q(0), "c": Q(0), "h": Q(1)}
    proposed_matrix, proposed_hist = evaluate_family(proposed, assignments)
    require(proposed_matrix == ((Q(1), Q(1), Q(0)),
                                (Q(0), Q(0), Q(0)),
                                (Q(-1), Q(-1), Q(0))),
            "proposed point type matrix changed")
    explicit = (0, 0, 0, 1, 2, 1, 2, 1)
    require(UNIFORM.evaluate_p(explicit, proposed_matrix) == 3,
            "explicit must-fire P_sigma changed")
    require(any(value for histogram in proposed_hist.values()
                for value in histogram),
            "false proposed point unexpectedly became a common zero")

    # Freeze the earlier genuine fixed-560 point explicitly; the shared
    # discovery script may be edited by another lane while this referee runs.
    old_point = {"a": Q(-12), "b": Q(8), "c": Q(-10), "h": Q(0)}
    old_matrix, old_hist = evaluate_family(old_point, assignments)
    require(old_hist["332"] == {Q(0): 560},
            "symmetric fixed-560 zero changed")
    require(old_hist["323"] == {Q(340200): 560}
            and old_hist["233"] == {Q(163800): 560},
            "S3 translates of fixed-560 zero changed")

    raw = raw_lift_matrix()
    p, q, r = VECTORS
    a = bilinear(p, raw, p)
    b = bilinear(q, raw, q)
    c = bilinear(r, raw, r)
    h = bilinear(p, raw, q) - bilinear(q, raw, p)
    require((a, b, c, h) == (Q(1), Q(0), Q(0), Q(1)),
            "raw 3x3 lift does not realize proposed contrast coordinates")

    result = {
        "status": "UNAUDITED exact full-S3 contrast scope referee",
        "fixed_count_assignments": 560,
        "count_placements": 3,
        "full_s3_contractions": len(assignments),
        "distinct_raw_tensor_signatures": len(signatures),
        "pure_coefficients_all_zero": True,
        "inclusion": (
            "All 1,680 contractions are distinct signed combinations of "
            "mixed H_w only, hence their ideal is contained in I_mix."
        ),
        "proposed_point": {name: [value.numerator, value.denominator]
                           for name, value in proposed.items()},
        "proposed_type_matrix": [
            [[value.numerator, value.denominator] for value in row]
            for row in proposed_matrix
        ],
        "proposed_nonzero_example": {
            "assignment": "".join(map(str, explicit)),
            "P_sigma": [3, 1],
        },
        "proposed_histograms": {
            placement: {str(value): count
                        for value, count in sorted(histogram.items())}
            for placement, histogram in proposed_hist.items()
        },
        "raw_3x3_lift": [
            [[value.numerator, value.denominator] for value in row]
            for row in raw
        ],
        "old_symmetric_point": {
            name: [value.numerator, value.denominator]
            for name, value in old_point.items()
        },
        "old_symmetric_S3_histograms": {
            placement: {str(value): count
                        for value, count in sorted(histogram.items())}
            for placement, histogram in old_hist.items()
        },
        "conclusion": (
            "Neither proposed uniform point is a common zero of the full "
            "S3-stable 1,680-contraction family. The h=1 point already "
            "fails inside the original fixed 560 because endpoint reversal "
            "changes the sign of h; the symmetric h=0 point kills fixed332 "
            "but not the other two multiplicity placements."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("full S3 contrast scope referee: PASS")
    print("contractions / signatures:", len(assignments), len(signatures))
    print("false h=1 explicit:", "".join(map(str, explicit)), 3)
    print("old point translated values:",
          old_hist["332"], old_hist["323"], old_hist["233"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
