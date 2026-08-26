#!/usr/bin/env python3
"""Exact-Q/Z replay for F_(0^8) times the canonical carrier minor."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import reduce
from hashlib import sha256
import importlib.util
from itertools import product
import json
from math import gcd, lcm
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
SEARCH = HERE / "search_pure_amplitude_carrier_minor_cegar.py"
MODULAR = HERE / "results_pure_amplitude_carrier_minor_cegar_p32003.json"
OUT = HERE / "results_pure_amplitude_carrier_minor_separator_exact.json"
EXPECTED_SEARCH_SHA256 = "2369cd3feca71448b39f9ace70fa3c2480da8cd41e14345d1efdc6f651dbedee"
EXPECTED_COMMON_SHA256 = "519bbabc971396d086b3454d9f2ea28ec49a3316597f399a8e969944b265c093"
EXPECTED_DEG9_SHA256 = "02760ce5e08848f9930acb873dadd053c16dedebe72cd18e89e3c6789cdc265a"
EXPECTED_MODULAR_SHA256 = "474b2e5775b99f0c54d58dec911b1903449e92398938e2eff6738ae4a0024920"
EXPECTED_TARGET_SHA256 = "90397081d79e8172c1b0af67f41b96b31d5c9ef37c155c0888976b2908caaf8e"
CELL_PATTERN = re.compile(r"A([0-7])([0-7])_([0-2])([0-2])")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_search():
    require(sha256(SEARCH.read_bytes()).hexdigest() == EXPECTED_SEARCH_SHA256,
            "search source drift")
    spec = importlib.util.spec_from_file_location("pure_search", SEARCH)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "missing loader")
    spec.loader.exec_module(module)
    require(sha256(module.COMMON_PATH.read_bytes()).hexdigest()
            == EXPECTED_COMMON_SHA256, "common source drift")
    require(sha256(module.C.DEG9.read_bytes()).hexdigest()
            == EXPECTED_DEG9_SHA256, "degree9 source drift")
    return module


S = load_search()
C = S.C
D9 = S.D9
P = S.P


def parse_monomial(text):
    factors = []
    for factor in text.split("*"):
        match = CELL_PATTERN.fullmatch(factor)
        require(match is not None, factor)
        factors.append(tuple(map(int, match.groups())))
    return tuple(sorted(factors))


def rational_reconstruct(residue, numerator_bound=32, denominator_bound=16):
    candidates = []
    for denominator in range(1, denominator_bound + 1):
        inverse = pow(denominator, P - 2, P)
        for numerator in range(-numerator_bound, numerator_bound + 1):
            if gcd(abs(numerator), denominator) != 1:
                continue
            if numerator * inverse % P == residue % P:
                candidates.append(Fraction(numerator, denominator))
    require(candidates, residue)
    candidates.sort(key=lambda value: (
        abs(value.numerator) + value.denominator,
        value.denominator, abs(value.numerator), value.numerator,
    ))
    best = candidates[0]
    require(sum(
        abs(value.numerator) + value.denominator
        == abs(best.numerator) + best.denominator
        for value in candidates
    ) == 1, (residue, candidates[:3]))
    return best


def primitive_integer_lift(entries):
    rational = {
        parse_monomial(entry["monomial"]):
        rational_reconstruct(entry["coefficient"] % P)
        for entry in entries
    }
    denominator = reduce(lcm, (value.denominator for value in rational.values()), 1)
    integer = {
        monomial: int(value * denominator)
        for monomial, value in rational.items()
    }
    common = reduce(gcd, (abs(value) for value in integer.values()))
    integer = {monomial: value // common for monomial, value in integer.items()}
    return rational, integer, denominator, common


def scan_all_touching_rows(functional, generators):
    labels = set()
    occurrences = 0
    for monomial in functional:
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = C.divides(monomial, term)
                if quotient is not None:
                    labels.add((word_index, quotient))
                    occurrences += 1
    nonzero = []
    by_word = Counter()
    for label in sorted(labels):
        by_word[D9.word_text(C.WORDS[label[0]])] += 1
        pairing = sum(functional.get(monomial, 0)
                      for monomial in C.row_monomials(label, generators))
        if pairing:
            nonzero.append((label, pairing))
    return labels, occurrences, by_word, nonzero


def exact_entries(functional):
    return [
        {
            "monomial": D9.monomial_text(monomial),
            "coefficient": coefficient,
        }
        for monomial, coefficient in sorted(functional.items())
    ]


def audit(mutate=False):
    require(sha256(MODULAR.read_bytes()).hexdigest() == EXPECTED_MODULAR_SHA256,
            "modular result drift")
    modular = json.loads(MODULAR.read_text())
    require(modular["status"] == "SEPARATOR_MOD_P", modular["status"])
    require(len(modular["rounds"]) == 191 and modular["final_rank"] == 1405,
            (len(modular["rounds"]), modular["final_rank"]))
    stored = modular["centered_integer_replay"]["entries"]
    rational, functional, common_denominator, primitive_gcd = (
        primitive_integer_lift(stored)
    )
    require(len(functional) == 44, len(functional))
    require(set(functional.values()) == {-2, -1, 1, 2, 3},
            set(functional.values()))
    require({value.denominator for value in rational.values()} == {1, 2},
            {value.denominator for value in rational.values()})
    if mutate:
        functional[min(functional)] += 1

    target = S.target_polynomial()
    require(S.target_digest(target) == EXPECTED_TARGET_SHA256, "target drift")
    require(len(target) == 664_776 and set(map(len, target)) == {13},
            (len(target), set(map(len, target))))
    weight_set = {D9.fine_weight_of_monomial(monomial) for monomial in target}
    require(len(weight_set) == 1, len(weight_set))
    weight = next(iter(weight_set))
    compatible = tuple(
        word for word in product(range(3), repeat=8)
        if all(weight[site][word[site]] for site in range(8))
    )
    require(compatible == ((0,) * 8,) + C.WORDS, compatible)

    generators = tuple(tuple(D9.amplitude(word)) for word in C.WORDS)
    labels, occurrences, by_word, nonzero = scan_all_touching_rows(
        functional, generators
    )
    target_pairing = sum(coefficient * functional.get(monomial, 0)
                         for monomial, coefficient in target.items())
    require(not nonzero, [
        [D9.word_text(C.WORDS[label[0]]),
         D9.monomial_text(label[1]), pairing]
        for label, pairing in nonzero[:3]
    ])
    require(target_pairing == 2, target_pairing)
    require(len(labels) == 52, len(labels))

    entries = exact_entries(functional)
    separator_sha = sha256(json.dumps(
        entries, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    result = {
        "status": (
            "PASS exact-Z nonmembership of F_00000000*Delta in degree-13 mixed X5"
        ),
        "target": {
            "formula": "F_00000000 * canonical Delta",
            "degree": 13,
            "terms": len(target),
            "sha256": EXPECTED_TARGET_SHA256,
            "fine_weight": [list(row) for row in weight],
            "coefficient_histogram": modular["target"]["coefficient_histogram"],
        },
        "fine_grade_word_census": {
            "all_compatible_words": [D9.word_text(word) for word in compatible],
            "pure_word_excluded_from_mixed_X5": "00000000",
            "mixed_words": [D9.word_text(word) for word in C.WORDS],
        },
        "modular_discovery": {
            "prime": P,
            "empty_seed": True,
            "rounds_including_terminal_scan": len(modular["rounds"]),
            "final_rank": modular["final_rank"],
            "final_columns": modular["final_columns"],
            "final_basis_fill": modular["final_basis_fill"],
            "terminal_dual_support": modular["final_dual_support"],
        },
        "exact_separator": {
            "coefficient_ring": "Z",
            "rational_reconstruction_denominators": [1, 2],
            "clearing_denominator": common_denominator,
            "primitive_gcd_removed": primitive_gcd,
            "support": len(functional),
            "coefficient_set": sorted(set(functional.values())),
            "target_pairing": target_pairing,
            "quotient_occurrences_touching_support": occurrences,
            "distinct_translates_touching_support": len(labels),
            "translates_by_word": dict(by_word),
            "nonzero_row_pairings": len(nonzero),
            "sha256": separator_sha,
            "entries": entries,
        },
        "theorem": (
            "The displayed primitive integer functional annihilates every "
            "degree-9 monomial translate of every mixed X5 amplitude in the "
            "target fine grade and pairs with F_00000000*Delta as 2. Hence "
            "the normalized degree-13 target is not in the homogeneous mixed-X5 "
            "span over Q (indeed over every field of characteristic other than 2)."
        ),
        "exhaustiveness_guard": (
            "A row outside the 52 enumerated translates is disjoint from the "
            "44-coordinate separator support. The five mixed words are exhaustive "
            "in the target fine grade."
        ),
        "scope_guard": (
            "This refutes direct degree-13 homogeneous membership. It does not "
            "decide radical membership, higher-degree multiplication, or use of "
            "the inhomogeneous pure normalization row F_00000000-1 itself."
        ),
        "source_sha256": {
            "search": EXPECTED_SEARCH_SHA256,
            "common": EXPECTED_COMMON_SHA256,
            "degree9": EXPECTED_DEG9_SHA256,
            "modular_result": EXPECTED_MODULAR_SHA256,
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
        require(OUT.exists() and json.loads(OUT.read_text()) == result,
                "stored exact result drift")
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    exact = result["exact_separator"]
    print(result["status"])
    print("support/touching", exact["support"],
          exact["distinct_translates_touching_support"],
          exact["translates_by_word"])
    print("target pairing", exact["target_pairing"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
