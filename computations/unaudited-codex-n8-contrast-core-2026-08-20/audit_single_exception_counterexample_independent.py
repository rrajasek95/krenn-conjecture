#!/usr/bin/env python3
"""Independent exact replay of the full-contrast single-edge counterexample.

This deliberately imports no discovery code.  It checks the 1,680 balanced
contractions in the two-dimensional contrast basis and again by expanding
them as signed sums of the 3^8 raw-colour Hafnians.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_single_exception_counterexample_independent.json"
Q = Fraction
P = (Q(1), Q(0))
QDIR = (Q(0), Q(1))
R = (Q(-1), Q(1))
DIRECTIONS = (P, QDIR, R)
RAW_DIRECTIONS = ((1, -1, 0), (1, 0, -1), (0, 1, -1))
EXCEPTIONAL_EDGE = (0, 1)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        result.extend(((first, second),) + tail
                      for tail in perfect_matchings(remainder))
    return tuple(result)


PM8 = perfect_matchings(tuple(range(8)))


def assignments_with_counts(counts: tuple[int, int, int]):
    word = tuple(kind for kind, count in enumerate(counts)
                 for _ in range(count))
    return tuple(sorted(set(permutations(word))))


ASSIGNMENT_BLOCKS = tuple(assignments_with_counts(counts)
                          for counts in ((2, 3, 3), (3, 2, 3), (3, 3, 2)))


def contrast_block(edge: tuple[int, int]):
    return (((Q(1), Q(1)), (Q(0), Q(0)))
            if edge == EXCEPTIONAL_EDGE
            else ((Q(1), Q(0)), (Q(0), Q(0))))


def raw_block(edge: tuple[int, int]):
    matrix = [[Q(0) for _ in range(3)] for _ in range(3)]
    matrix[1][1] = Q(1)
    if edge == EXCEPTIONAL_EDGE:
        matrix[1][2] = Q(1)
    return tuple(map(tuple, matrix))


def product_of(values):
    result = Q(1)
    for value in values:
        result *= value
    return result


def bilinear(left, matrix, right):
    return sum(left[i] * matrix[i][j] * right[j]
               for i in range(len(left)) for j in range(len(right)))


def matching_term(assignment, matching):
    return product_of(
        bilinear(DIRECTIONS[assignment[u]], contrast_block((u, v)),
                 DIRECTIONS[assignment[v]])
        for u, v in matching
    )


def contraction(assignment):
    terms = tuple(matching_term(assignment, matching) for matching in PM8)
    return sum(terms, Q(0)), sum(value != 0 for value in terms)


def raw_hafnian(word):
    return sum((product_of(raw_block((u, v))[word[u]][word[v]]
                           for u, v in matching)
                for matching in PM8), Q(0))


def expanded_contraction(assignment, raw_hafnians):
    result = Q(0)
    site_terms = tuple(tuple((raw_colour, Q(coefficient))
                             for raw_colour, coefficient
                             in enumerate(RAW_DIRECTIONS[kind]) if coefficient)
                       for kind in assignment)
    for choices in product(*site_terms):
        word = tuple(raw_colour for raw_colour, _ in choices)
        coefficient = product_of(value for _, value in choices)
        result += coefficient * raw_hafnians[word]
    return result


def directional_hafnian(direction):
    return sum((product_of(
        bilinear(direction, contrast_block((u, v)), direction)
        for u, v in matching) for matching in PM8), Q(0))


def main() -> None:
    require(len(PM8) == 105, "perfect-matching count changed")
    require(tuple(map(len, ASSIGNMENT_BLOCKS)) == (560, 560, 560),
            "balanced-assignment count changed")

    direct_histograms = []
    term_histograms = []
    for block in ASSIGNMENT_BLOCKS:
        evaluations = tuple(contraction(assignment) for assignment in block)
        direct_histograms.append(Counter(value for value, _ in evaluations))
        term_histograms.append(Counter(count for _, count in evaluations))
    require(direct_histograms == [Counter({Q(0): 560})] * 3,
            "a balanced contraction did not vanish")
    require(term_histograms == [Counter({0: 560})] * 3,
            "vanishing was not termwise")

    raw_hafnians = {word: raw_hafnian(word)
                    for word in product(range(3), repeat=8)}
    raw_mismatches = 0
    for block in ASSIGNMENT_BLOCKS:
        for assignment in block:
            raw_mismatches += (expanded_contraction(assignment, raw_hafnians)
                               != contraction(assignment)[0])
    require(raw_mismatches == 0, "raw-colour signed expansion disagreed")

    # Also check directly that the raw 3x3 blocks restrict to the advertised
    # contrast blocks in the ordered basis (p,q).
    for edge in ((u, v) for u in range(8) for v in range(u + 1, 8)):
        restricted = tuple(tuple(bilinear(RAW_DIRECTIONS[i], raw_block(edge),
                                           RAW_DIRECTIONS[j])
                                 for j in range(2)) for i in range(2))
        require(restricted == contrast_block(edge),
                f"raw block restriction failed at {edge}")

    a, b, c = tuple(directional_hafnian(direction)
                    for direction in DIRECTIONS)
    factors = (a + b - c, a + c - b, b + c - a)
    heron = product_of(factors)
    require((a, b, c) == (Q(105), Q(0), Q(90)),
            "directional Hafnians changed")
    require(factors == (Q(15), Q(195), Q(-15))
            and heron == Q(-43_875), "Heron control changed")

    result = {
        "status": "UNAUDITED independent exact contrast counterexample replay",
        "imports_discovery_code": False,
        "perfect_matchings": len(PM8),
        "balanced_assignments_by_count_placement": list(map(len, ASSIGNMENT_BLOCKS)),
        "direct_value_histograms": [dict(map(lambda item: (str(item[0]), item[1]),
                                                histogram.items()))
                                    for histogram in direct_histograms],
        "nonzero_matching_term_histograms": [dict(histogram)
                                               for histogram in term_histograms],
        "raw_signed_expansion_mismatches": raw_mismatches,
        "raw_colour_nonzero_cells": (
            "x_uv^(1,1)=1 on every u<v; x_01^(1,2)=1; all others zero"
        ),
        "contrast_blocks": (
            "D_uv=[[1,0],[0,0]], except D_01=[[1,1],[0,0]]"
        ),
        "A_B_C": [int(a), int(b), int(c)],
        "Heron_factors": list(map(int, factors)),
        "Heron": int(heron),
        "termwise_reason": (
            "Every balanced assignment has at least two q-sites. All base "
            "blocks kill q at both endpoints and the exceptional oriented "
            "edge can absorb at most one q-site."
        ),
        "conclusion": (
            "The full 1680-generator contrast ideal has a rational zero with "
            "Heron nonzero, so its radical cannot prove N=8."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("independent single-exception contrast replay: PASS")
    print("balanced rows / raw mismatches:", 1680, raw_mismatches)
    print("A,B,C / Heron:", (a, b, c), heron)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
