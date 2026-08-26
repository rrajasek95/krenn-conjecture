#!/usr/bin/env python3
"""Exact rational counterexample to the 78 pair-constant generator subideal."""

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
BASE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
             "audit_dangerous_charts.py")
SPEC = importlib.util.spec_from_file_location("n8_pc78_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
OUT = HERE / "results_pair_constant_78_counterexample.json"

Q = Fraction
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
CLONE_MATRIX = ((Q(1), Q(-2, 3)), (Q(0), Q(-1)))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def pair_constant_word(colours):
    return tuple(colour for colour in colours for _ in range(2))


def assignment(matrix=CLONE_MATRIX):
    values = {cell: Q(0) for cell in BASE.CELLS}
    for left, right in M0:
        for colour in BASE.COLORS:
            values[(left, right, colour, colour)] = Q(1)
    for first_pair in range(4):
        for second_pair in range(first_pair + 1, 4):
            for first_clone in range(2):
                for second_clone in range(2):
                    u = 2 * first_pair + first_clone
                    v = 2 * second_pair + second_clone
                    for colour in BASE.COLORS:
                        values[(u, v, colour, colour)] = (
                            matrix[first_clone][second_clone]
                        )
    return values


def evaluate_word(word, values):
    total = Q(0)
    supported = 0
    for matching in BASE.PM8:
        term = Q(1)
        for u, v in matching:
            term *= values[(u, v, word[u], word[v])]
        total += term
        supported += bool(term)
    return total, supported


def permanent(matrix):
    return matrix[0][0] * matrix[1][1] + matrix[0][1] * matrix[1][0]


def triangle_weight(matrix):
    total = Q(0)
    for ri, rj, rk in product(range(2), repeat=3):
        total += (matrix[ri][rj]
                  * matrix[1 - ri][rk]
                  * matrix[1 - rj][1 - rk])
    return total


def no_internal_four_weight(matrix):
    total = Q(0)
    terms = 0
    for matching in BASE.PM8:
        if any(u // 2 == v // 2 for u, v in matching):
            continue
        value = Q(1)
        for u, v in matching:
            first_pair, first_clone = divmod(u, 2)
            second_pair, second_clone = divmod(v, 2)
            require(first_pair < second_pair,
                    "canonical physical edge reversed supervertices")
            value *= matrix[first_clone][second_clone]
        total += value
        terms += 1
    require(terms == 60, "four-supervertex no-internal count changed")
    return total, terms


def partition_profile(colours):
    return tuple(sorted(Counter(colours).values(), reverse=True))


def main() -> None:
    require(len(BASE.PM8) == 105, "PM(8) count changed")
    values = assignment()
    p = permanent(CLONE_MATRIX)
    c = triangle_weight(CLONE_MATRIX)
    d, d_terms = no_internal_four_weight(CLONE_MATRIX)
    require((p, c, d) == (Q(-1), Q(2), Q(53, 9)),
            "four-supervertex weights changed")
    z = {
        0: Q(1),
        1: Q(1),
        2: Q(1) + p,
        3: Q(1) + 3 * p + c,
        4: Q(1) + 6 * p + 4 * c + d,
    }
    require(z == {0: Q(1), 1: Q(1), 2: Q(0),
                  3: Q(0), 4: Q(80, 9)},
            "block partition functions changed")

    evaluations = {}
    supported_histogram = Counter()
    profile_histogram = Counter()
    for colours in product(BASE.COLORS, repeat=4):
        word = pair_constant_word(colours)
        actual, supported = evaluate_word(word, values)
        expected = Q(1)
        for size in Counter(colours).values():
            expected *= z[size]
        require(actual == expected,
                "literal hafnian disagrees with colour-block factorization")
        evaluations[colours] = actual
        supported_histogram[supported] += 1
        profile_histogram[partition_profile(colours)] += 1

    pure = {colours[0]: value for colours, value in evaluations.items()
            if len(set(colours)) == 1}
    mixed = {colours: value for colours, value in evaluations.items()
             if len(set(colours)) > 1}
    require(len(mixed) == 78 and all(value == 0 for value in mixed.values()),
            "a pair-constant mixed generator does not vanish")
    require(pure == {0: Q(80, 9), 1: Q(80, 9), 2: Q(80, 9)},
            "pure tuple changed")

    # A sign mutation of the upper-right clone entry must destroy the mixed
    # zero.  This guards the cancellation P=-1, C=2.
    hostile_matrix = ((Q(1), Q(2, 3)), (Q(0), Q(-1)))
    hostile_values = assignment(hostile_matrix)
    hostile_word = pair_constant_word((0, 0, 0, 1))
    hostile_value, _ = evaluate_word(hostile_word, hostile_values)
    require(hostile_value != 0, "hostile clone-matrix mutation did not fire")

    target = pure[0] * pure[1] * pure[2]
    require(target == Q(512000, 729) != 0,
            "pure target product changed")
    nonzero_coordinates = sum(value != 0 for value in values.values())
    result = {
        "status": "UNAUDITED exact rational pair-constant counterexample",
        "normalized_anchor_values": 12,
        "clone_matrix": [[[value.numerator, value.denominator]
                          for value in row] for row in CLONE_MATRIX],
        "assignment_rule": (
            "All cross-colour cells and all unlisted cells are zero. Every "
            "same-colour cross-supervertex 2x2 clone block equals the frozen "
            "matrix; all twelve orbit0 diagonal anchors equal one."
        ),
        "nonzero_coordinates": nonzero_coordinates,
        "perfect_matchings_per_word": len(BASE.PM8),
        "pair_constant_words_checked": len(evaluations),
        "mixed_generators_checked": len(mixed),
        "four_supervertex_expansion": {
            "two_block_permanent_P": [p.numerator, p.denominator],
            "three_block_triangle_C": [c.numerator, c.denominator],
            "four_block_no_internal_D": [d.numerator, d.denominator],
            "no_internal_matching_terms": d_terms,
            "Z0_through_Z4": {
                str(size): [value.numerator, value.denominator]
                for size, value in z.items()
            },
        },
        "colour_partition_profile_histogram": {
            "+".join(map(str, profile)): count
            for profile, count in sorted(profile_histogram.items())
        },
        "supported_term_histogram": {
            str(count): words for count, words in sorted(supported_histogram.items())
        },
        "mixed_values": [0, 1],
        "pure_values": {
            str(colour): [value.numerator, value.denominator]
            for colour, value in pure.items()
        },
        "pure_target_product": [target.numerator, target.denominator],
        "hostile_mutation_value": [hostile_value.numerator,
                                   hostile_value.denominator],
        "conclusion": (
            "The 78 pair-constant mixed generators do not force "
            "H_0*H_1*H_2=0, even set-theoretically over Q. Any normalized "
            "orbit0 proof must use at least one non-pair-constant mixed word."
        ),
        "scope": (
            "This point is only a common zero of the 78-generator subideal; "
            "it is not asserted to annihilate the other 6,480 mixed words."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 normalized 78-generator counterexample: PASS")
    print("pair-constant words / mixed zero:", len(evaluations), len(mixed))
    print("P,C,D / pure:", p, c, d, pure[0])
    print("target product:", target)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
