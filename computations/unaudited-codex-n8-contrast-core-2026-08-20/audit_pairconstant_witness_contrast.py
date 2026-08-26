#!/usr/bin/env python3
"""Evaluate all 560 contrast P_sigma at the rational 78-generator zero."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BRIDGE = (ROOT / "computations" /
          "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20")
PC78 = (ROOT / "computations" /
        "unaudited-codex-n8-orbit0-normalized-78-2026-08-20")
OUT = HERE / "results_pairconstant_witness_contrast.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTRAST = load_module("n8_contrast_witness_base",
                       BRIDGE / "audit_trichromatic_332_contraction.py")
VERIFY = load_module("n8_contrast_witness_pc78",
                     PC78 / "verify_pair_constant_78_counterexample.py")
BASE = CONTRAST.BASE
Q = Fraction


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def assignments_332():
    answer = []
    for sites01 in combinations(range(8), 3):
        remainder = [site for site in range(8) if site not in sites01]
        for sites02 in combinations(remainder, 3):
            labels = ["12"] * 8
            for site in sites01:
                labels[site] = "01"
            for site in sites02:
                labels[site] = "02"
            answer.append(tuple(labels))
    require(len(answer) == 560 and len(set(answer)) == 560,
            "(3,3,2) assignment count changed")
    return tuple(answer)


def direct_polarized_hafnian(labels, values):
    total = Q(0)
    for matching in BASE.PM8:
        term = Q(1)
        for u, v in matching:
            left = CONTRAST.VECTORS[labels[u]]
            right = CONTRAST.VECTORS[labels[v]]
            term *= sum(
                left[a] * right[b] * values[(u, v, a, b)]
                for a in BASE.COLORS for b in BASE.COLORS
            )
        total += term
    return total


def source_expansion(labels, word_values):
    total = Q(0)
    active_words = 0
    for word, value in word_values.items():
        coefficient = 1
        for site, colour in enumerate(word):
            coefficient *= CONTRAST.VECTORS[labels[site]][colour]
        if coefficient:
            active_words += 1
            total += coefficient * value
    require(active_words == 256,
            "contrast tensor active-word count changed")
    return total


def main():
    values = VERIFY.assignment()
    word_values = {
        word: VERIFY.evaluate_word(word, values)[0]
        for word in product(BASE.COLORS, repeat=8)
    }
    assignments = assignments_332()
    amplitudes = Counter()
    for labels in assignments:
        direct = direct_polarized_hafnian(labels, values)
        expanded = source_expansion(labels, word_values)
        require(direct == expanded,
                "literal P_sigma disagrees with its 256-word source expansion")
        amplitudes[direct] += 1
    require(sum(amplitudes.values()) == 560,
            "contrast amplitude mass changed")
    require(len(amplitudes) == 77 and Q(0) not in amplitudes,
            "contrast witness zero/nonzero census changed")

    all_same = {
        label: direct_polarized_hafnian((label,) * 8, values)
        for label in CONTRAST.VECTORS
    }
    require(all_same == {"01": Q(1280, 9), "02": Q(1280, 9),
                         "12": Q(1280, 9)},
            "all-same contrast values changed")
    a, b, c = (all_same[label] for label in ("01", "02", "12"))
    heron = (a + b - c) * (a + c - b) * (b + c - a)
    pure_target = Q(512000, 729)
    require(heron == Q(2097152000, 729) != 8 * pure_target,
            "Heron witness value changed")

    hostile_values = VERIFY.assignment(
        ((Q(1), Q(2, 3)), (Q(0), Q(-1)))
    )
    hostile = direct_polarized_hafnian(assignments[0], hostile_values)
    require(hostile != direct_polarized_hafnian(assignments[0], values),
            "clone-sign mutation did not fire")

    result = {
        "status": "UNAUDITED exact rational contrast evaluation",
        "contrast_assignments": len(assignments),
        "source_words_per_contraction": 256,
        "distinct_amplitudes": len(amplitudes),
        "zero_contrast_polynomials": amplitudes.get(Q(0), 0),
        "nonzero_contrast_polynomials": sum(amplitudes.values()),
        "amplitude_histogram": {
            f"{value.numerator}/{value.denominator}": count
            for value, count in sorted(amplitudes.items())
        },
        "all_same_A_B_C": {
            label: [value.numerator, value.denominator]
            for label, value in all_same.items()
        },
        "heron_target": [heron.numerator, heron.denominator],
        "pure_target": [pure_target.numerator, pure_target.denominator],
        "heron_equals_8_times_pure_target_at_this_partial_zero": False,
        "hostile_first_contrast_value": [hostile.numerator,
                                         hostile.denominator],
        "conclusion": (
            "The rational common zero of the 78 pair-constant mixed "
            "generators is not a zero of J_332: every one of the 560 "
            "contrast polarizations P_sigma is nonzero. Hence this witness "
            "does not obstruct a J_332 radical proof for the Heron target."
        ),
        "logical_note": (
            "Vanishing of the five literal colour-profile-(3,3,2) word "
            "orbits does not imply P_sigma=0. Each P_sigma is a signed "
            "256-word combination involving multiple colour profiles. "
            "Likewise F congruent to 8*T modulo the full mixed ideal does "
            "not imply equality at this point, which kills only 78 mixed "
            "generators."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("pair-constant witness contrast evaluation: PASS")
    print("P_sigma total / zero / amplitudes:",
          560, amplitudes.get(Q(0), 0), len(amplitudes))
    print("A=B=C / Heron:", a, heron)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
