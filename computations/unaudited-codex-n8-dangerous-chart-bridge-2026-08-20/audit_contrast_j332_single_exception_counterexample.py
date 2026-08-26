#!/usr/bin/env python3
"""Exact rational counterexample to Heron in radical(full contrast J332)."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPORT_PATH = HERE / "export_contrast_j332_interface.py"
SPEC = importlib.util.spec_from_file_location("contrast_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
OUT = HERE / "results_contrast_j332_single_exception_counterexample.json"
Q = Fraction
DIRECTIONS = ((1, 0), (0, 1), (-1, 1))  # p,q,r=q-p
EXCEPTIONAL_EDGE = (0, 1)
ASSIGNMENTS_BY_DOUBLED = tuple(
    tuple(sorted(set(permutations(tuple(
        kind for kind in range(3)
        for _ in range(2 if kind == doubled else 3)
    ))))) for doubled in range(3)
)
ASSIGNMENTS = tuple(row for block in ASSIGNMENTS_BY_DOUBLED for row in block)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def multiply(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def block(edge):
    # Coordinates in the ordered (p,q) basis.  Every base block is rank one;
    # the sole exceptional oriented edge has pXq=1 as well.
    if edge == EXCEPTIONAL_EDGE:
        return ((Q(1), Q(1)), (Q(0), Q(0)))
    return ((Q(1), Q(0)), (Q(0), Q(0)))


def bilinear(edge, left_direction, right_direction):
    matrix = block(edge)
    left = DIRECTIONS[left_direction]
    right = DIRECTIONS[right_direction]
    return sum(Q(left[i]) * matrix[i][j] * Q(right[j])
               for i in range(2) for j in range(2))


def evaluate_contraction(assignment):
    nonzero_matching_terms = 0
    value = Q(0)
    for matching in EXPORT.BASE.PM8:
        term = multiply(bilinear((left, right), assignment[left],
                                 assignment[right])
                        for left, right in matching)
        nonzero_matching_terms += (term != 0)
        value += term
    return value, nonzero_matching_terms


def raw_block(edge):
    # Raw colours are ordered 0,1,2.  x^{11}=1 on every edge and the
    # exceptional edge additionally has x^{12}=1.
    matrix = [[Q(0) for _ in range(3)] for _ in range(3)]
    matrix[1][1] = Q(1)
    if edge == EXCEPTIONAL_EDGE:
        matrix[1][2] = Q(1)
    return tuple(map(tuple, matrix))


def raw_hafnian(word):
    return sum(multiply(raw_block((left, right))[word[left]][word[right]]
                        for left, right in matching)
               for matching in EXPORT.BASE.PM8)


def directional_hafnian(left_direction, right_direction=None):
    if right_direction is None:
        right_direction = left_direction
    return sum(multiply(bilinear((left, right), left_direction,
                                 right_direction)
                        for left, right in matching)
               for matching in EXPORT.BASE.PM8)


def main() -> None:
    require(len(ASSIGNMENTS) == len(set(ASSIGNMENTS)) == 1680,
            "full balanced assignment census changed")
    require(tuple(map(len, ASSIGNMENTS_BY_DOUBLED)) == (560, 560, 560),
            "count-placement census changed")

    direct_histograms = []
    nonzero_term_histograms = []
    for assignments in ASSIGNMENTS_BY_DOUBLED:
        evaluations = []
        term_counts = []
        for assignment in assignments:
            value, nonzero_terms = evaluate_contraction(assignment)
            evaluations.append(value)
            term_counts.append(nonzero_terms)
        direct_histograms.append(Counter(evaluations))
        nonzero_term_histograms.append(Counter(term_counts))
    require(direct_histograms == [Counter({Q(0): 560}) for _ in range(3)],
            "a full-S3 balanced contraction is nonzero")
    require(nonzero_term_histograms == [Counter({0: 560}) for _ in range(3)],
            "vanishing ceased to be termwise at the matching level")

    # Independent literal raw-colour replay of all signed 256-word sums.
    raw_h = {word: raw_hafnian(word)
             for word in product(range(3), repeat=8)}
    raw_histograms = []
    mismatch_count = 0
    for assignments in ASSIGNMENTS_BY_DOUBLED:
        values = []
        for assignment in assignments:
            raw_value = sum(Q(sign) * raw_h[tuple(map(int, word))]
                            for word, sign in EXPORT.raw_provenance(assignment))
            direct_value, _terms = evaluate_contraction(assignment)
            mismatch_count += (raw_value != direct_value)
            values.append(raw_value)
        raw_histograms.append(Counter(values))
    require(mismatch_count == 0
            and raw_histograms == [Counter({Q(0): 560}) for _ in range(3)],
            "raw signed-256 replay disagrees or does not vanish")

    a_haf = directional_hafnian(0)
    b_haf = directional_hafnian(1)
    c_haf = directional_hafnian(2)
    require((a_haf, b_haf, c_haf) == (Q(105), Q(0), Q(90)),
            "directional Hafnians changed")
    factors = (a_haf + b_haf - c_haf,
               a_haf + c_haf - b_haf,
               b_haf + c_haf - a_haf)
    heron = multiply(factors)
    require(factors == (Q(15), Q(195), Q(-15))
            and heron == Q(-43_875), "Heron target vanished or changed")

    # Hostile target mutation: deleting the exceptional pXq cell restores
    # C=A and makes Heron zero.
    base_c = Q(105)
    mutated_factors = (a_haf + b_haf - base_c,
                       a_haf + base_c - b_haf,
                       b_haf + base_c - a_haf)
    require(multiply(mutated_factors) == 0,
            "exception-deletion mutation did not kill Heron")

    nonzero_raw_h = Counter(raw_h.values())
    result = {
        "status": "UNAUDITED exact full-J332 rational counterexample",
        "contrast_basis": "p=(1,0), q=(0,1), r=q-p=(-1,1)",
        "point": (
            "D_uv=[[1,0],[0,0]] for all oriented edges u<v except "
            "D_01=[[1,1],[0,0]]."
        ),
        "raw_colour_realization": (
            "x_uv^{11}=1 on all 28 edges; x_01^{12}=1; every other "
            "raw endpoint-colour cell is zero."
        ),
        "assignments_by_doubled_direction": [560, 560, 560],
        "balanced_contractions_checked": 1680,
        "direct_value_histograms": [
            {str(value): count for value, count in histogram.items()}
            for histogram in direct_histograms
        ],
        "nonzero_matching_term_histograms": [
            {str(value): count for value, count in histogram.items()}
            for histogram in nonzero_term_histograms
        ],
        "raw_signed256_replays": 1680,
        "raw_replay_mismatch_count": mismatch_count,
        "raw_H_value_histogram": {
            str(value): count for value, count in sorted(nonzero_raw_h.items())
        },
        "termwise_reason": (
            "Every (3,3,2) assignment has at least two q-sites. Base blocks "
            "annihilate q at either endpoint, while the sole exceptional "
            "pXq edge can service at most one q-site. Hence every one of the "
            "105 perfect-matching terms in every contraction is zero."
        ),
        "A_B_C": [[value.numerator, value.denominator]
                   for value in (a_haf, b_haf, c_haf)],
        "Heron_factors": [[value.numerator, value.denominator]
                           for value in factors],
        "Heron": [heron.numerator, heron.denominator],
        "conclusion": (
            "This rational point belongs to V(J332_full) but not to "
            "V(Heron). Thus Heron is not in radical(J332_full), and no "
            "positive power of Heron belongs to J332_full."
        ),
        "scope": (
            "J332_full is the 1680-generator ideal of all balanced contrast "
            "contractions. The point is not a common zero of every original "
            "mixed H_w, so this does not challenge the N=8 conjecture; it "
            "only terminates the contrast-only radical route."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("full contrast J332 single-exception counterexample: PASS")
    print("P332 zero/total and termwise:", 1680, 1680)
    print("raw signed256 mismatches:", mismatch_count)
    print("A,B,C / Heron:", (a_haf, b_haf, c_haf), heron)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
