#!/usr/bin/env python3
"""Audit the orbit0 anchors=1 normalization and specialized polynomials."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import importlib.util
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = (HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
             / "audit_dangerous_charts.py")
SPEC = importlib.util.spec_from_file_location("orbit0_normalized_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
OUT = HERE / "results_orbit0_normalized_chart.json"
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
PRIME = 1009


def specialize(row, anchors):
    return bytes(sorted(cell for cell in row if cell not in anchors))


def polynomial_for_word(word, anchors):
    return Counter(specialize(row, anchors) for row in BASE.word_terms(word))


def convolve(left, right):
    answer = Counter()
    for left_row, left_coefficient in left.items():
        for right_row, right_coefficient in right.items():
            answer[bytes(sorted(left_row + right_row))] += (
                left_coefficient * right_coefficient
            )
    return +answer


def evaluate_word(word, values):
    total = 0
    for row in BASE.word_terms(word):
        term = 1
        for cell in row:
            term = term * values[cell] % PRIME
        total = (total + term) % PRIME
    return total


def main():
    anchors = frozenset(
        BASE.CELL_ID[(u, v, colour, colour)]
        for colour in BASE.COLORS for u, v in M0
    )
    assert len(anchors) == 12

    # Literal gauge covariance over a finite-field control point.  The proof
    # is termwise because every perfect matching uses every site exactly once.
    rng = random.Random(820031)
    values = [rng.randrange(1, PRIME) for _ in BASE.CELLS]
    lambdas = [[rng.randrange(1, PRIME) for _ in BASE.COLORS]
               for _ in range(BASE.N)]
    transformed = []
    for cell, value in zip(BASE.CELLS, values):
        u, v, a, b = cell
        transformed.append(value * lambdas[u][a] * lambdas[v][b] % PRIME)
    for word in product(BASE.COLORS, repeat=BASE.N):
        scale = 1
        for site, colour in enumerate(word):
            scale = scale * lambdas[site][colour] % PRIME
        assert evaluate_word(word, transformed) == evaluate_word(word, values) * scale % PRIME

    generator_histogram = Counter()
    constant_generators = 0
    collected_term_histogram = Counter()
    raw_degree_histogram = Counter()
    for word in product(BASE.COLORS, repeat=BASE.N):
        if len(set(word)) == 1:
            continue
        polynomial = polynomial_for_word(word, anchors)
        degrees = tuple(sorted({len(row) for row in polynomial}))
        generator_histogram[degrees] += 1
        collected_term_histogram[len(polynomial)] += 1
        for row, coefficient in polynomial.items():
            raw_degree_histogram[len(row)] += coefficient
        if polynomial.get(b"", 0):
            constant_generators += 1
            assert polynomial[b""] == 1
    assert constant_generators == 3**4 - 3 == 78

    pure = [polynomial_for_word((colour,) * BASE.N, anchors)
            for colour in BASE.COLORS]
    target = convolve(convolve(pure[0], pure[1]), pure[2])
    target_degree_histogram = Counter()
    target_mass_by_degree = Counter()
    for row, coefficient in target.items():
        target_degree_histogram[len(row)] += 1
        target_mass_by_degree[len(row)] += coefficient
    assert sum(target.values()) == 105**3
    assert target[b""] == 1 and max(map(len, target)) == 12

    result = {
        "status": "UNAUDITED exact orbit0 normalized-chart audit",
        "anchors": bytes(sorted(anchors)).hex(),
        "gauge_covariance_words_checked_mod_1009": 3**8,
        "gauge_statement": (
            "x_uv[a,b] -> lambda[u,a]lambda[v,b]x_uv[a,b] scales H_w by "
            "product_v lambda[v,w_v]. The four disjoint selected edges per "
            "colour let one set all twelve nonzero anchors to 1 without "
            "changing mixed vanishing or pure nonvanishing."
        ),
        "specialized_variables": 252 - len(anchors),
        "mixed_generators": 3**8 - 3,
        "mixed_generators_with_constant_term_one": constant_generators,
        "generator_degree_support_histogram": {
            ",".join(map(str, degrees)): count
            for degrees, count in sorted(generator_histogram.items())
        },
        "generator_collected_term_count_histogram": {
            str(count): multiplicity
            for count, multiplicity in sorted(collected_term_histogram.items())
        },
        "generator_raw_term_mass_by_degree": {
            str(degree): mass for degree, mass in sorted(raw_degree_histogram.items())
        },
        "target": "specialization of T=H0*H1*H2 after setting anchors to 1",
        "target_collected_rows": len(target),
        "target_total_mass": sum(target.values()),
        "target_row_count_by_degree": {
            str(degree): count for degree, count in sorted(target_degree_histogram.items())
        },
        "target_mass_by_degree": {
            str(degree): mass for degree, mass in sorted(target_mass_by_degree.items())
        },
        "membership_scope": (
            "Chart exclusion is T in sqrt(J_A), not 1 in J_A. A positive "
            "Macaulay certificate is exact; failure at a bounded multiplier "
            "degree is not a radical nonmembership theorem."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 normalized-chart audit: PASS")
    print("constant generators:", constant_generators)
    print("target rows/mass:", len(target), sum(target.values()))
    print("target rows by degree:", dict(sorted(target_degree_histogram.items())))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
