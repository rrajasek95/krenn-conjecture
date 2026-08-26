#!/usr/bin/env python3
"""Guard against confusing colour-profile (3,3,2) words with P_(3,3,2)."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
POINT_PATH = (HERE.parent /
              "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
              "verify_pair_constant_78_counterexample.py")
POINT_SPEC = importlib.util.spec_from_file_location("j332_point", POINT_PATH)
POINT = importlib.util.module_from_spec(POINT_SPEC)
POINT_SPEC.loader.exec_module(POINT)
BASE = POINT.BASE
OUT = HERE / "results_contrast_j332_cloned_point_guard.json"

Q = Fraction
VECTORS = ((Q(1), Q(-1), Q(0)),
           (Q(1), Q(0), Q(-1)),
           (Q(0), Q(1), Q(-1)))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def bilinear(values, u: int, v: int, left, right):
    return sum(left[a] * right[b] * values[(u, v, a, b)]
               for a in BASE.COLORS for b in BASE.COLORS)


def polarized_hafnian(values, assignment):
    total = Q(0)
    for matching in BASE.PM8:
        term = Q(1)
        for u, v in matching:
            term *= bilinear(values, u, v,
                             VECTORS[assignment[u]], VECTORS[assignment[v]])
        total += term
    return total


def directional_hafnian(values, vector):
    return polarized_hafnian(values, (vector,) * BASE.N)


def main() -> None:
    values = POINT.assignment()
    assignments = sorted(set(permutations((0, 0, 0, 1, 1, 1, 2, 2))))
    require(len(assignments) == 560, "(3,3,2) assignment orbit changed")
    evaluations = Counter(polarized_hafnian(values, assignment)
                          for assignment in assignments)
    require(sum(evaluations.values()) == 560 and Q(0) not in evaluations,
            "a balanced trichromatic polarization unexpectedly vanished")

    profile_332_words = []
    for word in product(BASE.COLORS, repeat=BASE.N):
        if sorted(Counter(word).values(), reverse=True) == [3, 3, 2]:
            value, _supported = POINT.evaluate_word(word, values)
            profile_332_words.append(value)
    require(len(profile_332_words) == 1680
            and not any(profile_332_words),
            "original colour-profile (3,3,2) zero control changed")

    a, b, c = (directional_hafnian(values, vector) for vector in range(3))
    expected = Q(1280, 9)
    require((a, b, c) == (expected, expected, expected),
            "directional contrast Hafnians changed")
    factors = (a + b - c, a + c - b, b + c - a)
    heron = factors[0] * factors[1] * factors[2]
    require(factors == (expected, expected, expected)
            and heron == Q(2_097_152_000, 729) != 0,
            "Heron target changed or vanished")

    # Independently check the block collapse explaining the evaluation:
    # all colour matrices are scalar diagonal, so the three quadratic
    # directions coincide and the antisymmetric coordinate vanishes.
    block_controls = []
    for u in range(BASE.N):
        for v in range(u + 1, BASE.N):
            av = bilinear(values, u, v, VECTORS[0], VECTORS[0])
            bv = bilinear(values, u, v, VECTORS[1], VECTORS[1])
            cv = bilinear(values, u, v, VECTORS[2], VECTORS[2])
            left_right = bilinear(values, u, v, VECTORS[0], VECTORS[1])
            right_left = bilinear(values, u, v, VECTORS[1], VECTORS[0])
            require(av == bv == cv and left_right == right_left,
                    "cloned block is not scalar on the difference plane")
            block_controls.append({
                "edge": [u, v],
                "a=b=c": [av.numerator, av.denominator],
                "h": [0, 1],
            })

    result = {
        "status": "UNAUDITED exact profile-vs-contrast hostile regression",
        "point_source_sha256": sha256(POINT_PATH.read_bytes()).hexdigest(),
        "assignment_rule": (
            "The frozen normalized cloned-block point has all cross-colour "
            "cells zero, all twelve diagonal anchors one, and every "
            "same-colour cross-supervertex block equal to [[1,-2/3],[0,-1]]."
        ),
        "balanced_assignments_checked": len(assignments),
        "balanced_assignment_histogram": {"01": 3, "02": 3, "12": 2},
        "original_colour_profile_332_words": len(profile_332_words),
        "original_colour_profile_332_nonzero": 0,
        "P332_nonzero": sum(evaluations.values()),
        "P332_value_histogram": {
            str(value): count for value, count in sorted(evaluations.items())
        },
        "block_controls": block_controls,
        "A_B_C": [[value.numerator, value.denominator]
                   for value in (a, b, c)],
        "Heron_factors": [[value.numerator, value.denominator]
                           for value in factors],
        "Heron_value": [heron.numerator, heron.denominator],
        "conclusion": (
            "Although all 1680 original H_w with colour multiplicities "
            "(3,3,2) vanish, every one of the 560 balanced sitewise contrast "
            "polarizations P_sigma is nonzero. A P_sigma is a signed sum of "
            "256 H_w across several colour profiles, so profile vanishing "
            "does not give a J332 common zero."
        ),
        "global_scope": (
            "This point is a hostile regression, not a J332 or N=8 "
            "counterexample. In the unnormalized difference-vector convention "
            "used here A=B=C=1280/9 and Heron is nonzero, but P332 is also "
            "nonzero."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("contrast J332 cloned-point hostile guard: PASS")
    print("profile332 zero / P332 nonzero:", len(profile_332_words),
          sum(evaluations.values()))
    print("A=B=C / Heron:", expected, heron)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
