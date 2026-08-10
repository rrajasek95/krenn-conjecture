#!/usr/bin/env python3
"""Freeze the first cycle gate for source-labelled matching exchange.

This does not enumerate a third one-bad support layer.  It combines:

* the pinned two-arrow one-bad audit (no return through 168 routes);
* the primitive C4/C6 matching count on six sites;
* the first commuting exchange square, supported on two disjoint C4s; and
* the pinned exact N=12 feedback model showing that even matching feedback
  can close without odd Laurent holonomy, while exporting singleton debt.

Thus an odd exponent cycle is a unit, but a local matching potential cannot
be globally well-founded unless it also records all boundary fibres.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py":
        "2b32c6d50ea1dda5a7b412a0fcd6de2373ab483b5b25eba7352684a5499e8f28",
    "computations/verify_n8_one_bad_first_cross_mate_exchange.py":
        "e1d641d64bf0659d6b28ea64bf8a935e17c4da1c7e2c831f0dfb041fc78eaf0c",
    "computations/verify_n8_one_bad_second_top_mate_exchange.py":
        "1df9d9eb63220782d672dd89ce56759c6fb515c923cd9124d162ff0a40862ea5",
    "computations/verify_rankone_feedback_recombination_countermodel.py":
        "8abb693488fade9faa1b03a702f8b1205ca8dbe04aad751b525bb94142d56444",
}
EXPECTED_DIGEST = "b0d95b63ad15a6fccae9114bd7a552d481c08c32b2bfdfcf1193c456c84982f0"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def occurrence(matching):
    return Counter(matching)


def signed_row(positive, negative):
    answer = Counter(occurrence(positive))
    answer.subtract(occurrence(negative))
    return answer


def audit_primitive_six_site_exchanges(base):
    matchings = tuple(base.perfect_matchings(base.SITES))
    require(len(matchings) == 15, "the K6 perfect-matching count changed")
    pair_types = Counter()
    for left, right in itertools.combinations(matchings, 2):
        common = len(set(left) & set(right))
        require(common in (0, 1), "two distinct K6 matchings share too much")
        symmetric_cycle = 6 if common == 0 else 4
        pair_types[symmetric_cycle] += 1
    require(pair_types == Counter({4: 45, 6: 60}),
            f"the primitive K6 exchange count changed: {pair_types}")

    local = Counter()
    fixed = set(matchings[0])
    for other in matchings[1:]:
        local[6 if not (fixed & set(other)) else 4] += 1
    require(local == Counter({4: 6, 6: 8}),
            "the six/eight C4/C6 alternatives changed")
    return {
        "perfect_matchings": 15,
        "unordered_pairs": 105,
        "pair_types": {"C4": 45, "C6": 60},
        "alternatives_from_one_matching": {"C4": 6, "C6": 8},
        "meaning": (
            "a binomial mate is one primitive alternating component; two "
            "components would expose four same-word matchings"
        ),
    }


def audit_first_commuting_square():
    # Two independent C4 switches on 0,1,2,3 and 4,5,6,7.
    m00 = ((0, 1), (2, 3), (4, 5), (6, 7))
    m10 = ((0, 3), (1, 2), (4, 5), (6, 7))
    m01 = ((0, 1), (2, 3), (4, 7), (5, 6))
    m11 = ((0, 3), (1, 2), (4, 7), (5, 6))
    require(occurrence(m00) + occurrence(m11)
            == occurrence(m10) + occurrence(m01),
            "the commuting matching square lost its occurrence identity")

    rows = (
        signed_row(m10, m00),
        signed_row(m11, m10),
        signed_row(m01, m11),
        signed_row(m00, m01),
    )
    total = Counter()
    for row in rows:
        total.update(row)
    require(not +total and not -total,
            "the four exchange rows stopped telescoping")
    require(len(rows) % 2 == 0,
            "the commuting square stopped being sign-even")

    # A closed relation of three plus-binomials has product sign -1.
    odd_rows = ((1, 0), (0, 1), (-1, -1))
    require(tuple(sum(row[index] for row in odd_rows)
                  for index in range(2)) == (0, 0),
            "the abstract odd exponent circuit stopped closing")
    require((-1) ** len(odd_rows) == -1 and (-1) ** len(rows) == 1,
            "the signed cycle parity changed")
    return {
        "minimum_vertices_for_two_disjoint_C4s": 8,
        "square": [list(map(list, matching))
                   for matching in (m00, m10, m11, m01)],
        "occurrence_identity": "chi00+chi11=chi10+chi01",
        "four_binomial_holonomy": 1,
        "odd_closed_binomial_holonomy": -1,
        "verdict": (
            "odd exponent cycles are Laurent units; the first independent "
            "physical diamond is even and sign-consistent"
        ),
    }


def audit_feedback_counterguard(feedback):
    cells = feedback.build_cells()
    fibres = feedback.fibres(cells)
    pure = {}
    for colour in range(3):
        fibre = fibres[(colour,) * feedback.ORDER]
        pure[colour] = [
            len(fibre),
            sum(feedback.matching_weight(matching, cells)
                for matching in fibre),
        ]
    require(pure == {0: [1, 1], 1: [5, 1], 2: [1, 1]},
            "the feedback model lost its normalized pure fibres")

    mixed = {word: fibre for word, fibre in fibres.items()
             if len(set(word)) > 1}
    histogram = Counter(len(fibre) for fibre in mixed.values())
    require(histogram == Counter({1: 100, 2: 11}),
            "the feedback boundary histogram changed")
    binomials = [fibre for fibre in mixed.values() if len(fibre) == 2]
    require(all(sum(feedback.matching_weight(matching, cells)
                    for matching in fibre) == 0
                for fibre in binomials),
            "a feedback binomial stopped cancelling")
    differences = {feedback.signed_difference(fibre, cells)
                   for fibre in binomials}
    require(len(differences) == 1,
            "the feedback Laurent rows stopped being identical")
    nonzero_row = next(iter(differences))
    require(nonzero_row[0] and nonzero_row[1],
            "the feedback Laurent row became zero")
    return {
        "order": feedback.ORDER,
        "pure_fibres_size_and_coefficient": pure,
        "mixed_fibre_histogram": {"singleton": 100, "binomial": 11},
        "distinct_signed_laurent_rows": 1,
        "odd_dependency": False,
        "verdict": (
            "even feedback can close with exact pure anchors and no odd "
            "holonomy, but exports 100 singleton boundary fibres"
        ),
    }


def main():
    paths = tuple(PINS)
    base = load_pinned("one_bad_binary", paths[0])
    first = load_pinned("one_bad_first", paths[1])
    second = load_pinned("one_bad_second", paths[2])
    feedback = load_pinned("feedback_counterguard", paths[3])

    # Re-run the bounded one-bad two-arrow theorem, not a third layer.
    second_audit = second.audit_second_routes(base, first)
    require(second_audit["second_route_charts"] == 168,
            "the bounded second-arrow theorem changed")
    require("new private mixed top" in second_audit["verdict"],
            "the second-arrow no-return verdict changed")

    ledger = {
        "pins": PINS,
        "bounded_one_bad_gate": {
            "first_mate_charts": second_audit["first_mate_charts"],
            "private_top_words": second_audit["private_top_words"],
            "second_route_charts": second_audit["second_route_charts"],
            "cycles_through_two_arrows": 0,
        },
        "primitive_six_site_exchanges":
            audit_primitive_six_site_exchanges(base),
        "first_commuting_square": audit_first_commuting_square(),
        "even_feedback_counterguard": audit_feedback_counterguard(feedback),
        "conclusion": (
            "there is no source-labelled cycle through two one-bad arrows; "
            "an odd exponent cycle would be a unit, but even feedback is a "
            "real escape unless a global boundary-fibre potential descends"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"one-bad exchange-cycle ledger changed: {digest}")

    print("N=8 one-bad source-labelled exchange cycle gate: PASS")
    print("one-bad cycles through two arrows: 0")
    print("first independent-component diamond: even commuting C4 x C4 square")
    print("even feedback counterguard: 11 binomials, 100 boundary singletons")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
