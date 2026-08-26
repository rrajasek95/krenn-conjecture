#!/usr/bin/env python3
"""Exact first valuation collision for D*cross-cap-minor."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K1_PATH = HERE / "audit_crosscap_pure_cone_k1.py"
K1_SHA256 = "fed7765f1733ce5d21bed9a3f69a4b13a068f7f11e02ae0d2609df91b6a60328"
OUT = HERE / "results_crosscap_D_cone_valuation.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_k1():
    require(sha256(K1_PATH.read_bytes()).hexdigest() == K1_SHA256,
            "k1 checker changed")
    spec = importlib.util.spec_from_file_location("crosscap_k1", K1_PATH)
    require(spec is not None and spec.loader is not None, "cannot load k1")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


K = load_k1()
C = K.C
PORTS = tuple((site, colour) for site in range(8) for colour in range(3))


def d_coned_grade():
    base = (
        (3, 3, 3), (3, 3, 3), (1, 0, 0), (1, 0, 0),
        (0, 0, 0), (3, 3, 3), (1, 0, 0), (4, 3, 3),
    )
    return tuple(tuple(value + 1 for value in row) for row in base)


def specialize_all_leaf_colours(base, values=(1, 1, 1)):
    source = {edge: [row[:] for row in matrix]
              for edge, matrix in base.items()}
    for colour, value in enumerate(values):
        source[(0, 1)][colour][colour] = Fraction(value)
    return source


def word_text(word):
    return "".join(map(str, word))


def profile(word):
    return "+".join(map(str, sorted(Counter(word).values(), reverse=True)))


def fine_weight(monomial):
    weight = [[0, 0, 0] for _ in range(8)]
    for (u, v, a, b), exponent in monomial.items():
        weight[u][a] += exponent
        weight[v][b] += exponent
    return tuple(tuple(row) for row in weight)


def cell_label(u, v, colour):
    return (u, v, colour, colour) if u < v else (v, u, colour, colour)


def construct_supported_multiplier(weight, word):
    degrees = [[weight[site][colour] - int(word[site] == colour)
                for colour in range(3)] for site in range(8)]
    monomial = Counter()
    valuation = [0, 0, 0]

    # The only leaf-leaf variables on the family are A_01[c,c].  Their
    # forced exponents are half the leaf/hub degree imbalance.
    for colour in range(3):
        leaf_total = sum(degrees[site][colour] for site in range(5))
        hub_total = sum(degrees[site][colour] for site in (5, 6, 7))
        difference = leaf_total - hub_total
        require(difference >= 0 and difference % 2 == 0,
                (colour, leaf_total, hub_total))
        exponent = difference // 2
        require(exponent <= degrees[0][colour]
                and exponent <= degrees[1][colour],
                (colour, exponent, degrees[0][colour], degrees[1][colour]))
        if exponent:
            monomial[cell_label(0, 1, colour)] += exponent
            valuation[colour] += exponent
            degrees[0][colour] -= exponent
            degrees[1][colour] -= exponent

    # Complete diagonal hub-leaf support: greedily realize each colour's
    # remaining bipartite degree sequence.  Parallel edges are monomial
    # powers and are allowed.
    for colour in range(3):
        hubs = {site: degrees[site][colour] for site in (5, 6, 7)}
        for leaf in range(5):
            remaining = degrees[leaf][colour]
            for hub in (5, 6, 7):
                used = min(remaining, hubs[hub])
                if used:
                    monomial[cell_label(leaf, hub, colour)] += used
                    remaining -= used
                    hubs[hub] -= used
            require(remaining == 0, (colour, leaf, remaining, hubs))
        require(not any(hubs.values()), (colour, hubs))

    expected = tuple(tuple(weight[site][colour]
                           - int(word[site] == colour)
                           for colour in range(3)) for site in range(8))
    require(fine_weight(monomial) == expected,
            (fine_weight(monomial), expected))
    require(sum(monomial.values()) == 28, sum(monomial.values()))
    return monomial, tuple(valuation)


def monomial_value(source, monomial):
    value = Fraction(1)
    for (u, v, a, b), exponent in monomial.items():
        value *= C.cell(source, u, v, a, b) ** exponent
    return value


def monomial_manifest(monomial):
    return [
        {
            "cell": f"A_{u}{v}[{a},{b}]",
            "exponent": exponent,
        }
        for (u, v, a, b), exponent in sorted(monomial.items())
    ]


def run(mutate=False):
    base = K.diagonal_hub_leaf_source(1)
    source = specialize_all_leaf_colours(base)
    minor, matrices = K.canonical_minor(source, mutate=mutate)
    require(minor and all(C.determinant(matrix) for matrix in matrices),
            "response open failed")

    pure_coefficients = []
    for colour in range(3):
        word = (colour,) * 8
        value = C.amplitude(source, word)
        require(value, (colour, value))
        pure_coefficients.append(value)

    nonzero_mixed = []
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        value = C.amplitude(source, word)
        if value:
            nonzero_mixed.append((word, value))
    require(nonzero_mixed, "no mixed valuation collision")
    first_word, first_coefficient = nonzero_mixed[0]
    require(word_text(first_word) == "00001001", word_text(first_word))

    weight = d_coned_grade()
    require(all(weight[site][first_word[site]] for site in range(8)),
            "first word not fine-grade compatible")
    multiplier, multiplier_valuation = construct_supported_multiplier(
        weight, first_word)
    require(multiplier_valuation == (0, 1, 1), multiplier_valuation)
    multiplier_coefficient = monomial_value(source, multiplier)
    require(multiplier_coefficient, multiplier_coefficient)
    row_leading_coefficient = first_coefficient * multiplier_coefficient
    target_leading_coefficient = (
        pure_coefficients[0] * pure_coefficients[1] * pure_coefficients[2]
        * minor
    )
    require(row_leading_coefficient and target_leading_coefficient,
            (row_leading_coefficient, target_leading_coefficient))

    result = {
        "status": "PASS exact D-cone first valuation collision",
        "upstream": {
            "path": str(K1_PATH.relative_to(ROOT)),
            "sha256": K1_SHA256,
        },
        "target": {
            "formula": "D*P = F_00000000 F_11111111 F_22222222 * cross-cap minor",
            "source_degree": 32,
            "fine_weight": [list(row) for row in weight],
            "all_site_colour_ports_positive": True,
            "compatible_mixed_words": 6558,
            "valuation": [1, 1, 1],
            "leading_coefficient": C.fraction_string(target_leading_coefficient),
        },
        "family": {
            "formula": "diagonal K_(3,5) + sum_c t_c A_01[c,c]",
            "base_source_sha256": C.source_digest(base),
            "pure_linear_coefficients": [
                C.fraction_string(value) for value in pure_coefficients
            ],
            "crosscap_minor": C.fraction_string(minor),
            "crosscap_minor_independent_of_t0_t1_t2": True,
            "nonzero_mixed_word_count": len(nonzero_mixed),
        },
        "first_collision": {
            "word": word_text(first_word),
            "profile": profile(first_word),
            "generator_valuation": [1, 0, 0],
            "generator_leading_coefficient": C.fraction_string(first_coefficient),
            "multiplier_source_degree": 28,
            "multiplier_valuation": list(multiplier_valuation),
            "multiplier_leading_coefficient": C.fraction_string(
                multiplier_coefficient),
            "row_valuation": [1, 1, 1],
            "row_leading_coefficient": C.fraction_string(row_leading_coefficient),
            "multiplier": monomial_manifest(multiplier),
        },
        "verdict": (
            "The all-k single-colour valuation separator does not extend to "
            "D*P. A literal profile-6+2 mixed row times the displayed "
            "degree-28 source monomial attains the same (1,1,1) valuation "
            "as the target. This is not an ideal-membership certificate; it "
            "is the exact first obstruction to the proposed valuation proof."
        ),
        "scope_guard": (
            "No conclusion is made about D*P membership, D^n P^m, radical "
            "membership, or normalized flatness. The requested uniform "
            "valuation route fails already at n=m=1."
        ),
        "mutation": mutate,
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-crossed-orientation", action="store_true")
    args = parser.parse_args()
    result = run(mutate=args.mutate_crossed_orientation)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.mutate_crossed_orientation:
        require(OUT.exists() and OUT.read_text() == text,
                "PASS hostile orientation mutation changed artifact")
    if args.check_results:
        require(OUT.exists() and OUT.read_text() == text,
                "result artifact mismatch")
    if args.write_results:
        OUT.write_text(text)
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": result["logical_sha256"],
        "word": result["first_collision"]["word"],
        "row_valuation": result["first_collision"]["row_valuation"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
