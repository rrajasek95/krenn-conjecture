#!/usr/bin/env python3
"""Exhaust the complete homogeneous degree-five Buchberger layer in chart 26.

All 6,558 original leading monomials are squarefree of degree four.  Hence
the non-product original-original pairs of LCM degree five are exactly the
pairs whose leads share three variables.  This checker enumerates all of
them, expands their exact S-polynomials, and proves:

* there are 84,005 labeled cells (44,028 Hamming-one star transports and
  39,977 Hamming-two direct-double transports);
* every cell has 180 terms with coefficients +/-1, all squarefree;
* no term is reducible by an original leading monomial;
* all 84,005 new degree-five leading monomials are distinct; and
* no new lead occurs in the support of any other degree-five cell.

The last two facts make the degree-five completion order-independent.  New
degree-five cells cannot create another critical pair of total degree five:
an original degree-four lead would have to divide their reduced lead, or two
distinct degree-five leads would have to coincide.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path
from struct import pack


HERE = Path(__file__).resolve().parent
FIRST_PATH = HERE / "verify_n8_chart26_first_homogeneous_spair.py"
SPEC = importlib.util.spec_from_file_location("n8_first_spair", FIRST_PATH)
FIRST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIRST)
D5 = FIRST.D5

EXPECTED_LEDGER_SHA256 = (
    "d840363e3244b3261cad48aa08d2972be20576dbd53b80c9ea0d398067fcd188"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def build_pairs(code_to_lead):
    by_core = defaultdict(list)
    for code, lead in code_to_lead.items():
        for core in combinations(lead, 3):
            by_core[bytes(core)].append(code)
    pairs = []
    core_size_histogram = Counter()
    for codes in by_core.values():
        core_size_histogram[len(codes)] += 1
        for index, first in enumerate(codes):
            for second in codes[index + 1:]:
                lead_first = code_to_lead[first]
                lead_second = code_to_lead[second]
                lcm = bytes(sorted(set(lead_first) | set(lead_second)))
                require(len(lcm) == 5, "a three-variable overlap lost degree five")
                pairs.append((lcm, min(first, second), max(first, second)))
    pairs.sort()
    require(len(pairs) == len(set(pairs)) == 84005,
            "degree-five labeled-pair census changed")
    return pairs, by_core, core_size_histogram


def s_polynomial(lcm, first_code, second_code, polynomials, code_to_lead):
    first_multiplier = FIRST.quotient(lcm, code_to_lead[first_code])
    second_multiplier = FIRST.quotient(lcm, code_to_lead[second_code])
    answer = Counter()
    for row, value in polynomials[first_code].items():
        answer[FIRST.multiply(first_multiplier, row)] += value
    for row, value in polynomials[second_code].items():
        answer[FIRST.multiply(second_multiplier, row)] -= value
    return {row: value for row, value in answer.items() if value}


def is_original_reducible(row, original_leads):
    if len(row) < 4:
        return False
    return any(
        divisor in original_leads
        for divisor in FIRST.divisors(row, 4)
    )


def hamming_distance(first_code, second_code, decoded_words):
    return sum(
        first != second
        for first, second in zip(
            decoded_words[first_code], decoded_words[second_code]
        )
    )


def source_pair_orbits(pairs):
    pair_set = {(first, second) for _lcm, first, second in pairs}
    representatives = {}
    for pair in pair_set:
        orbit = frozenset(
            tuple(sorted((
                D5.WORD_TRANSFORMS[index][pair[0]],
                D5.WORD_TRANSFORMS[index][pair[1]],
            )))
            for index in range(len(D5.WORD_TRANSFORMS))
        )
        representatives[min(orbit)] = orbit
    return representatives


def audit():
    polynomials, lead_to_code = FIRST.original_basis()
    code_to_lead = {code: lead for lead, code in lead_to_code.items()}
    pairs, by_core, core_size_histogram = build_pairs(code_to_lead)
    decoded_words = {
        code: D5.decode_word(code) for code in polynomials
    }

    leading_owner = {}
    cell_histogram = Counter()
    aggregate_degree_histogram = Counter()
    aggregate_coefficient_histogram = Counter()
    original_reducible_terms = 0
    nonsquarefree_terms = 0
    repeated_leads = 0
    polynomial_digest = sha256()

    for cell_index, (lcm, first_code, second_code) in enumerate(pairs, 1):
        polynomial = s_polynomial(
            lcm, first_code, second_code, polynomials, code_to_lead
        )
        require(len(polynomial) == 180,
                "a degree-five cell changed its term census")
        lead = FIRST.leading_monomial(polynomial)
        if lead in leading_owner:
            repeated_leads += 1
        else:
            leading_owner[lead] = cell_index
        hamming = hamming_distance(
            first_code, second_code, decoded_words
        )
        cell_histogram[(hamming, len(polynomial))] += 1
        aggregate_degree_histogram.update(map(len, polynomial))
        aggregate_coefficient_histogram.update(polynomial.values())

        polynomial_digest.update(pack(">HH", first_code, second_code))
        polynomial_digest.update(lcm)
        for row, value in sorted(polynomial.items()):
            original_reducible_terms += is_original_reducible(
                row, lead_to_code
            )
            nonsquarefree_terms += len(row) != len(set(row))
            require(value in (-1, 1), "a degree-five coefficient left +/-1")
            polynomial_digest.update(bytes((len(row),)))
            polynomial_digest.update(row)
            polynomial_digest.update(b"+" if value == 1 else b"-")

    require(cell_histogram == Counter({(1, 180): 44028, (2, 180): 39977}),
            "one-end/direct-double cell census changed")
    require(len(leading_owner) == 84005 and repeated_leads == 0,
            "degree-five leading monomials collided")
    require(original_reducible_terms == 0,
            "a degree-five cell is reducible by an original lead")
    require(nonsquarefree_terms == 0,
            "a raw degree-five transport monomial is not squarefree")
    require(aggregate_degree_histogram == Counter({
        5: 12458960,
        4: 2456787,
        3: 197492,
        2: 7614,
        1: 47,
    }), "aggregate degree-five support histogram changed")
    require(aggregate_coefficient_histogram
            == Counter({-1: 7560450, 1: 7560450}),
            "aggregate degree-five coefficient histogram changed")

    # Since every new lead has degree five, a new cell can reduce another
    # one only if that exact lead occurs as one of its degree-five terms.
    foreign_lead_occurrences = 0
    for cell_index, (lcm, first_code, second_code) in enumerate(pairs, 1):
        polynomial = s_polynomial(
            lcm, first_code, second_code, polynomials, code_to_lead
        )
        own_lead = FIRST.leading_monomial(polynomial)
        for row in polynomial:
            if row != own_lead and row in leading_owner:
                foreign_lead_occurrences += 1
    require(foreign_lead_occurrences == 0,
            "degree-five cells gained a cross-leading incidence")

    pair_orbits = source_pair_orbits(pairs)
    orbit_size_histogram = Counter(map(len, pair_orbits.values()))
    orbit_hamming_size_histogram = Counter()
    for representative, orbit in pair_orbits.items():
        hamming = hamming_distance(
            representative[0], representative[1], decoded_words
        )
        orbit_hamming_size_histogram[(hamming, len(orbit))] += 1
    require(len(pair_orbits) == 39703,
            "support-stabilizer source-pair orbit census changed")
    require(orbit_size_histogram == Counter({4: 39518, 2: 179, 1: 6}),
            "source-pair orbit-size histogram changed")

    ledger = {
        "original_generators": len(polynomials),
        "distinct_original_degree4_leads": len(lead_to_code),
        "three_variable_cores": len(by_core),
        "core_size_histogram": dict(sorted(core_size_histogram.items())),
        "labeled_degree5_pairs": len(pairs),
        "source_pair_orbit_representatives": len(pair_orbits),
        "source_pair_orbit_size_histogram": dict(sorted(
            orbit_size_histogram.items()
        )),
        "source_pair_orbit_hamming_size_histogram": [
            [[hamming, size], count]
            for (hamming, size), count
            in sorted(orbit_hamming_size_histogram.items())
        ],
        "hamming1_star_transport_cells": cell_histogram[(1, 180)],
        "hamming2_direct_double_cells": cell_histogram[(2, 180)],
        "terms_per_cell": 180,
        "aggregate_term_count": sum(aggregate_degree_histogram.values()),
        "aggregate_degree_histogram": dict(sorted(
            aggregate_degree_histogram.items()
        )),
        "aggregate_coefficient_histogram": dict(sorted(
            aggregate_coefficient_histogram.items()
        )),
        "original_reducible_terms": original_reducible_terms,
        "nonsquarefree_terms": nonsquarefree_terms,
        "distinct_new_degree5_leads": len(leading_owner),
        "new_lead_collisions": repeated_leads,
        "foreign_new_lead_occurrences": foreign_lead_occurrences,
        "complete_cell_stream_sha256": polynomial_digest.hexdigest(),
        "conclusion": (
            "all original-original degree5 S-cells form an independent "
            "squarefree Buchberger layer"
        ),
        "scope_guard": (
            "this completes total degree five, not the higher-degree "
            "Buchberger basis or homogeneous pure-target membership"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen complete degree-five ledger changed")
    print(
        "n=8 chart26 complete degree-five Buchberger layer: PASS; "
        "cells=84005, star/direct=44028/39977, foreign incidences=0"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
