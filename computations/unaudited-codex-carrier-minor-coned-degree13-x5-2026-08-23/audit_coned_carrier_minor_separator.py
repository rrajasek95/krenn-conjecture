#!/usr/bin/env python3
"""Exact-Z replay of the 23-coordinate separator for M*Delta."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
SEARCH_RESULT = HERE / "results_coned_carrier_minor_cegar_p32003.json"
OUT = HERE / "results_coned_carrier_minor_separator_exact.json"
DEG9 = HERE.parent / "unaudited-codex-carrier-minor-degree9-x5-2026-08-23" / "audit_carrier_minor_degree9_x5.py"
EXPECTED_DEG9_SHA256 = "02760ce5e08848f9930acb873dadd053c16dedebe72cd18e89e3c6789cdc265a"
EXPECTED_TARGET_SHA256 = "757ec6347b959dd4e920d676a84281f273bb33a0ee31b0502c86235515798c82"
EXPECTED_SEPARATOR_SHA256 = "9423469a2fd3280203e99a8ed039c500b21b4f5f73e49c3ebba9fc1a3c5eed77"
CELL_PATTERN = re.compile(r"A([0-7])([0-7])_([0-2])([0-2])")
WORDS = (
    (0, 0, 0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 0, 1, 1),
    (0, 0, 0, 0, 0, 0, 2, 0),
    (0, 0, 0, 0, 0, 0, 2, 1),
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_degree9():
    require(sha256(DEG9.read_bytes()).hexdigest() == EXPECTED_DEG9_SHA256,
            "degree-9 source drift")
    spec = importlib.util.spec_from_file_location("degree9_carrier", DEG9)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "missing loader")
    spec.loader.exec_module(module)
    return module


D9 = load_degree9()


def parse_monomial(text):
    if not text:
        return ()
    cells = []
    for factor in text.split("*"):
        match = CELL_PATTERN.fullmatch(factor)
        require(match is not None, factor)
        cells.append(tuple(map(int, match.groups())))
    return tuple(sorted(cells))


def divides(big, small):
    counts = Counter(big)
    for atom in small:
        if not counts[atom]:
            return None
        counts[atom] -= 1
    return tuple(sorted(counts.elements()))


def coned_target():
    cone = (
        D9.cell(0, 1, 0, 0), D9.cell(2, 3, 0, 0),
        D9.cell(4, 5, 0, 0), D9.cell(6, 7, 0, 0),
    )
    target = Counter()
    for monomial, coefficient in D9.target_minor().items():
        target[tuple(sorted(monomial + cone))] += coefficient
    return target, tuple(sorted(cone))


def polynomial_digest(polynomial):
    record = [
        [D9.monomial_text(monomial), coefficient]
        for monomial, coefficient in sorted(polynomial.items())
    ]
    return sha256(json.dumps(record, separators=(",", ":")).encode()).hexdigest()


def separator_digest(entries):
    return sha256(json.dumps(
        entries, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def compatible_words(weight):
    answer = []
    for word in product(range(3), repeat=8):
        if all(weight[site][word[site]] for site in range(8)):
            answer.append(word)
    return tuple(answer)


def scan_all_touching_rows(functional, generators):
    labels = set()
    quotient_occurrences = 0
    for monomial in functional:
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = divides(monomial, term)
                if quotient is not None:
                    labels.add((word_index, quotient))
                    quotient_occurrences += 1
    nonzero = []
    counts = Counter()
    intersection_histogram = Counter()
    for word_index, quotient in sorted(labels):
        counts[D9.word_text(WORDS[word_index])] += 1
        pairing = 0
        intersections = 0
        for term in generators[word_index]:
            monomial = tuple(sorted(term + quotient))
            if monomial in functional:
                intersections += 1
                pairing += functional[monomial]
        intersection_histogram[intersections] += 1
        if pairing:
            nonzero.append((word_index, quotient, pairing))
    return labels, quotient_occurrences, counts, intersection_histogram, nonzero


def audit(mutate=False):
    discovery = json.loads(SEARCH_RESULT.read_text())
    entries = discovery["centered_integer_replay"]["entries"]
    require(separator_digest(entries) == EXPECTED_SEPARATOR_SHA256,
            "separator record drift")
    functional = {
        parse_monomial(entry["monomial"]): entry["coefficient"]
        for entry in entries
    }
    require(len(functional) == 23 and set(functional.values()) == {-1, 1},
            (len(functional), set(functional.values())))
    if mutate:
        first = min(functional)
        functional[first] += 1

    target, cone = coned_target()
    require(polynomial_digest(target) == EXPECTED_TARGET_SHA256,
            "target drift")
    require(len(target) == 6900 and set(map(len, target)) == {13},
            (len(target), set(map(len, target))))
    weights = {D9.fine_weight_of_monomial(monomial) for monomial in target}
    require(len(weights) == 1, weights)
    weight = next(iter(weights))
    exhaustive = compatible_words(weight)
    require(exhaustive == ((0,) * 8,) + WORDS, exhaustive)

    generators = tuple(tuple(D9.amplitude(word)) for word in WORDS)
    labels, occurrences, by_word, intersection_histogram, nonzero = (
        scan_all_touching_rows(functional, generators)
    )
    target_pairing = sum(coefficient * functional.get(monomial, 0)
                         for monomial, coefficient in target.items())
    require(not nonzero, {
        "first_nonzero": [
            D9.word_text(WORDS[word_index]), D9.monomial_text(quotient), pairing
        ] for word_index, quotient, pairing in nonzero[:3]
    })
    require(target_pairing == 1, target_pairing)
    require(len(labels) == 28, len(labels))

    result = {
        "status": "PASS exact-Z nonmembership of M*Delta in degree-13 mixed X5",
        "target": {
            "carrier_minor": (
                "triangle 012; cofactor columns 01,02,12; residual colour 0; "
                "cap rows 01,11,21"
            ),
            "pure_matching_cone": D9.monomial_text(cone),
            "degree": 13,
            "terms": len(target),
            "sha256": EXPECTED_TARGET_SHA256,
            "fine_weight": [list(row) for row in weight],
        },
        "fine_grade_word_census": {
            "all_compatible_words": [D9.word_text(word) for word in exhaustive],
            "pure_word_excluded_from_mixed_X5": "00000000",
            "mixed_words": [D9.word_text(word) for word in WORDS],
        },
        "separator": {
            "coefficient_ring": "Z",
            "support": len(functional),
            "coefficient_set": sorted(set(functional.values())),
            "sha256": EXPECTED_SEPARATOR_SHA256,
            "target_pairing": target_pairing,
            "quotient_occurrences_touching_support": occurrences,
            "distinct_translates_touching_support": len(labels),
            "translates_by_word": dict(by_word),
            "support_intersection_histogram": {
                str(key): value for key, value in sorted(intersection_histogram.items())
            },
            "nonzero_row_pairings": len(nonzero),
            "entries": entries,
        },
        "theorem": (
            "The displayed integer functional annihilates every degree-9 "
            "monomial translate of every mixed X5 amplitude in the target fine "
            "grade, and pairs with M*Delta as 1.  Hence M*Delta is not in that "
            "degree-13 homogeneous mixed-X5 span over any field."
        ),
        "exhaustiveness_guard": (
            "A translated row can pair nontrivially only if one of its 105 "
            "matching terms divides a separator-support monomial.  The replay "
            "enumerates every such quotient for all five compatible mixed "
            "words; every other translate is support-disjoint."
        ),
        "scope_guard": (
            "This refutes the proposed direct homogeneous membership route.  "
            "It does not test radical membership, higher-degree multipliers, or "
            "consequences that also use the inhomogeneous pure normalization "
            "H_0-1."
        ),
        "source_sha256": {
            "degree9_constructor": EXPECTED_DEG9_SHA256,
            "modular_discovery_result": sha256(SEARCH_RESULT.read_bytes()).hexdigest(),
        },
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-separator", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate_separator)
    if args.check_results:
        require(OUT.exists(), OUT)
        require(json.loads(OUT.read_text()) == result, "stored result drift")
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("touching", result["separator"]["distinct_translates_touching_support"],
          result["separator"]["translates_by_word"])
    print("separator/target", result["separator"]["support"],
          result["separator"]["target_pairing"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
