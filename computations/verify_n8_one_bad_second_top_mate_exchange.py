#!/usr/bin/env python3
"""Audit the direct second mate in the sharp one-bad exchange complex.

The first exchange theorem leaves a private mixed top coefficient.  For
each such coefficient, add every alternative endpoint-coloured perfect
matching for the same six-site word.  The 12 representative private words
give 12*14=168 direct second-route charts.

Every chart creates a *new* mixed top word with a unique source matching,
distinct from all private top words present before the second route.  Thus
the first two exchange arrows never close; signed holonomy is not reached
at this depth.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py":
        "2b32c6d50ea1dda5a7b412a0fcd6de2373ab483b5b25eba7352684a5499e8f28",
    "computations/verify_n8_one_bad_first_cross_mate_exchange.py":
        "e1d641d64bf0659d6b28ea64bf8a935e17c4da1c7e2c831f0dfb041fc78eaf0c",
}
EXPECTED_DIGEST = "10d31ddd4aecc9d19883e2eeedc7064a38b0ec098a0c76059fd3760fbffaaa80"


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


def audit_second_routes(base, first):
    all_matchings = tuple(base.perfect_matchings(base.SITES))
    route_counts = Counter()
    new_private_counts = Counter()
    representative_records = []
    first_charts = 0
    private_words = 0

    for orbit_index, packet in enumerate(base.SHARP_REPRESENTATIVES):
        a_matching, b_matching, b_holes, c_matching, c_holes = packet
        sharp = (
            tuple((edge, (base.A, base.A)) for edge in a_matching)
            + tuple((edge, (base.B, base.B)) for edge in b_matching)
            + tuple((edge, (base.C, base.C)) for edge in c_matching)
        )
        channels = (
            ("bc", base.B, base.C, b_holes[0], c_holes[1]),
            ("cb", base.C, base.B, c_holes[0], b_holes[1]),
        )
        for channel, left_colour, right_colour, left_hole, right_hole in channels:
            fixed = ((left_hole, left_colour),
                     (right_hole, right_colour))
            private_response = first.endpoint_tensor(sharp, 2, fixed)
            require(len(private_response) == 1
                    and next(iter(private_response.values())) == 1,
                    "the sharp cross coefficient stopped being private")
            response_word = next(iter(private_response))
            complement = tuple(site for site in base.SITES
                               if site not in (left_hole, right_hole))
            response_matchings = tuple(
                first.decorated_matching(matching, response_word)
                for matching in base.perfect_matchings(complement)
            )
            old_response = tuple(
                matching for matching in response_matchings
                if all(cell in sharp for cell in matching)
            )
            require(len(old_response) == 1,
                    "the sharp private response route changed")
            first_mates = tuple(
                matching for matching in response_matchings
                if frozenset(matching) != frozenset(old_response[0])
            )
            require(len(first_mates) == 2,
                    "the first C4 mate count changed")

            for first_mate_index, first_mate in enumerate(first_mates):
                first_charts += 1
                first_source = sharp + first_mate
                first_top = first.endpoint_tensor(first_source, 3)
                old_private_words = {
                    word for word, coefficient in first_top.items()
                    if word != (base.A,) * 6 and coefficient == 1
                }
                require(old_private_words,
                        "a first mate lost its private mixed top")
                private_words += len(old_private_words)

                for private_word in sorted(old_private_words):
                    decorated_top_matchings = tuple(
                        first.decorated_matching(matching, private_word)
                        for matching in all_matchings
                    )
                    old_top = tuple(
                        matching for matching in decorated_top_matchings
                        if all(cell in first_source for cell in matching)
                    )
                    require(len(old_top) == 1,
                            "a first-arrow top word stopped being private")
                    alternatives = tuple(
                        matching for matching in decorated_top_matchings
                        if frozenset(matching) != frozenset(old_top[0])
                    )
                    require(len(alternatives) == 14,
                            "the six-site alternate matching count changed")

                    for alternative_index, top_mate in enumerate(alternatives):
                        new_cells = tuple(cell for cell in top_mate
                                          if cell not in first_source)
                        require(len(new_cells) in (2, 3),
                                "a direct top mate left the two/three-cell chart")
                        second_source = first_source + new_cells
                        second_top = first.endpoint_tensor(second_source, 3)
                        require(second_top[private_word] == 2,
                                "the direct top mate did not add a second route")

                        new_private = {
                            word: coefficient
                            for word, coefficient in second_top.items()
                            if (word != (base.A,) * 6
                                and word not in old_private_words
                                and coefficient == 1)
                        }
                        require(new_private,
                                "a direct second route closed without a new "
                                "private mixed top")
                        for word in new_private:
                            decompositions = first.top_decompositions(
                                base, second_source, word
                            )
                            require(len(decompositions) == 1,
                                    "a reported new private word is not unique")
                            require(any(cell in new_cells
                                        for cell in decompositions[0]),
                                    "a new private word does not use a new cell")

                        route_counts[orbit_index, len(new_cells)] += 1
                        new_private_counts[
                            orbit_index, len(new_cells), len(new_private)
                        ] += 1
                        if len(representative_records) < 12:
                            representative_records.append({
                                "sharp_orbit": orbit_index,
                                "channel": channel,
                                "first_mate": first_mate_index,
                                "private_word": list(private_word),
                                "top_mate": alternative_index,
                                "new_cells": [
                                    [list(edge), list(colours)]
                                    for edge, colours in new_cells
                                ],
                                "new_private_words": [
                                    list(word) for word in sorted(new_private)
                                ],
                            })

    require((first_charts, private_words) == (8, 12),
            "the first-arrow chart/private-word count changed")
    require(route_counts == Counter({
        (0, 2): 48,
        (0, 3): 64,
        (1, 2): 24,
        (1, 3): 32,
    }), f"the direct second-route count changed: {route_counts}")
    require(sum(route_counts.values()) == 168,
            "the second-route total changed")

    return {
        "first_mate_charts": first_charts,
        "private_top_words": private_words,
        "alternative_top_matchings_per_word": 14,
        "second_route_charts": sum(route_counts.values()),
        "route_counts_by_sharp_orbit_and_new_cells": [
            [orbit, new_cells, count]
            for (orbit, new_cells), count in sorted(route_counts.items())
        ],
        "new_private_count_distribution": [
            [orbit, new_cells, count_private, count]
            for (orbit, new_cells, count_private), count
            in sorted(new_private_counts.items())
        ],
        "sample_records": representative_records,
        "verdict": (
            "every direct top mate creates a new private mixed top word; "
            "the first two exchange arrows do not close"
        ),
    }


def main():
    base = load_pinned("one_bad_binary_base", next(iter(PINS)))
    first_path = tuple(PINS)[1]
    first = load_pinned("one_bad_first_exchange", first_path)
    audit = audit_second_routes(base, first)
    ledger = {
        "pins": PINS,
        "second_top_mate_exchange": audit,
        "scope": (
            "direct alternate perfect matchings for private top words on "
            "the eight first-mate charts only"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"second-mate exchange ledger changed: {digest}")

    print("N=8 one-bad second top-mate exchange: PASS")
    print("first charts / private words / second routes: 8 / 12 / 168")
    print("new cells per second route: 72 need 2; 96 need 3")
    print("all second routes create a new private mixed top word")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
