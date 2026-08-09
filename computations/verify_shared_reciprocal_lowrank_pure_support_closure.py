#!/usr/bin/env python3
"""Close every shared-reciprocal low-rank packet by pure/mixed support.

For each of the 477 omission/head-label packets, build the maximal literal
endpoint-cell support allowed by its two coordinate-plane charts.  A missing
pure row is an immediate -1 unit.  The only 15 packets supporting all three
pure rows have counts (3,1,1); branching on the three pure-0 anchors, every
one of the 45 branches has a unique mixed matching made only of mandatory
anchor cells.  Hence the full low-rank branch is empty over every field.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import verify_shared_reciprocal_fourcover_overlap as overlap
import verify_shared_reciprocal_lowrank_headlabel_refinement as refinement


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(8))
P, Q, R = 0, 1, 2
COMMON = tuple(range(3, 8))
COLORS = (0, 1, 2)
PINS = {
    "computations/verify_shared_reciprocal_lowrank_headlabel_refinement.py":
        "2ef59ab46c14b0ea7452430061096cd6a004a22abb118cdc2ade936f702624a0",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency drift: {relative}")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(SITES))
WORDS = tuple(product(COLORS, repeat=8))
require(len(MATCHINGS) == 105, "eight-site perfect-matching count changed")
require(len(WORDS) == 6561, "ternary word count changed")


def omission_representatives():
    representatives = {}
    maps = overlap.balanced_omission_maps()
    for alpha in maps:
        for beta in maps:
            state = overlap.state_from_maps(alpha, beta)
            representatives.setdefault(state, (alpha, beta))
    require(len(representatives) == 99,
            "omission contingency representatives changed")
    return representatives


def maximal_support(packet, representatives):
    """Return the maximal cell predicate allowed by both low-rank charts."""

    state, a, c, b, d = packet
    alpha_tuple, beta_tuple = representatives[state]
    alpha = {site: alpha_tuple[site - 3] for site in COMMON}
    beta = {site: beta_tuple[site - 3] for site in COMMON}
    alpha[R] = alpha_tuple[5]
    beta[Q] = beta_tuple[5]

    def allowed(left, right, left_color, right_color):
        require(left < right, "edge endpoints are not canonical")
        if (left, right) == (P, Q):
            return (left_color, right_color) == (b, a)
        if (left, right) == (P, R):
            return (left_color, right_color) == (d, c)
        # The p-C endpoint stars and the opposite chord are unconstrained by
        # the two internal incident-space planes, so retain all their cells.
        if left == P or (left, right) == (Q, R):
            return True
        if left == Q:
            return (left_color != beta[Q]
                    and right_color != beta[right])
        if left == R:
            return (left_color != alpha[R]
                    and right_color != alpha[right])
        # A common-core block is internal in both deletions; each endpoint
        # lies in the intersection of its alpha- and beta-omission planes.
        return (left_color not in (alpha[left], beta[left])
                and right_color not in (alpha[right], beta[right]))

    return allowed


def supported(matching, word, allowed):
    return all(allowed(left, right, word[left], word[right])
               for left, right in matching)


def matching_cells(matching, word):
    return frozenset(
        (left, right, word[left], word[right])
        for left, right in matching
    )


def pure_matching_census(packets, representatives):
    signatures = Counter()
    survivors = []
    for packet in packets:
        allowed = maximal_support(packet, representatives)
        pure = tuple(
            tuple(matching for matching in MATCHINGS
                  if supported(matching, (color,) * 8, allowed))
            for color in COLORS
        )
        counts = tuple(len(row) for row in pure)
        signatures[counts] += 1
        if all(counts):
            survivors.append((packet, allowed, pure))

    expected = {
        (0, 0, 0): 204,
        (0, 0, 1): 171,
        (0, 1, 0): 27,
        (0, 1, 1): 30,
        (3, 0, 0): 30,
        (3, 1, 1): 15,
    }
    require(signatures == expected,
            f"maximal pure-support signature census changed: {signatures}")
    require(len(survivors) == 15,
            "all-pure maximal-support survivor count changed")
    surviving_states = {packet[0] for packet, _allowed, _pure in survivors}
    expected_state = (0, 0, (1, 0, 0, 0, 1, 1, 0, 1, 1))
    require(surviving_states == {expected_state},
            "all-pure packets stopped sharing one omission state")
    return signatures, survivors


def unique_mixed_anchor_closure(survivors):
    witnesses = []
    word_histogram = Counter()
    matching_histogram = Counter()
    for packet, allowed, pure in survivors:
        require(tuple(len(row) for row in pure) == (3, 1, 1),
                "surviving pure signature changed")
        mandatory_12 = (
            matching_cells(pure[1][0], (1,) * 8)
            | matching_cells(pure[2][0], (2,) * 8)
        )
        for pure_zero_matching in pure[0]:
            mandatory = (
                mandatory_12
                | matching_cells(pure_zero_matching, (0,) * 8)
            )
            witness = None
            for word in WORDS:
                if len(set(word)) == 1:
                    continue
                supported_matchings = tuple(
                    matching for matching in MATCHINGS
                    if supported(matching, word, allowed)
                )
                if len(supported_matchings) != 1:
                    continue
                unique = supported_matchings[0]
                if matching_cells(unique, word) <= mandatory:
                    witness = (word, unique)
                    break
            require(witness is not None,
                    "a pure-anchor branch lost its unique mixed matching")
            word, unique = witness
            witnesses.append((packet, pure_zero_matching, word, unique))
            word_histogram[word] += 1
            matching_histogram[unique] += 1

    require(len(witnesses) == 45,
            "pure-zero anchor branch count changed")
    expected_words = {
        (0, 1, 1, 0, 0, 1, 1, 0): 15,
        (1, 2, 2, 1, 1, 2, 2, 1): 30,
    }
    expected_matchings = {
        ((0, 3), (1, 5), (2, 6), (4, 7)): 15,
        ((0, 4), (1, 6), (2, 5), (3, 7)): 30,
    }
    require(word_histogram == expected_words,
            f"unique mixed-word witnesses changed: {word_histogram}")
    require(matching_histogram == expected_matchings,
            f"unique mixed-match witnesses changed: {matching_histogram}")
    return witnesses, word_histogram, matching_histogram


def main():
    pin_dependencies()
    packets = refinement.combined_packets()
    require(len(packets) == 477, "head-labelled packet count changed")
    representatives = omission_representatives()
    signatures, survivors = pure_matching_census(packets, representatives)
    witnesses, word_histogram, matching_histogram = (
        unique_mixed_anchor_closure(survivors)
    )
    ledger = {
        "packets": len(packets),
        "pure_signatures": {
            ",".join(map(str, signature)): count
            for signature, count in sorted(signatures.items())
        },
        "missing_pure_packets": len(packets) - len(survivors),
        "all_pure_packets": len(survivors),
        "pure_anchor_branches": len(witnesses),
        "mixed_word_histogram": {
            "".join(map(str, word)): count
            for word, count in sorted(word_histogram.items())
        },
        "mixed_matching_histogram": {
            "|".join(f"{left}{right}" for left, right in matching): count
            for matching, count in sorted(matching_histogram.items())
        },
        "coefficient_survivors": 0,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    expected = "d5933de9fc29fd53321a3004ccdb87ff87ff933dbec940d1d70ad89003c88935"
    require(digest == expected,
            f"shared reciprocal pure-support ledger changed: {digest}")
    print("shared reciprocal low-rank pure-support closure: PASS")
    print("maximal pure-support signatures:", dict(sorted(signatures.items())))
    print("missing-pure units:", len(packets) - len(survivors))
    print("all-pure packets / anchor branches:",
          len(survivors), "/", len(witnesses))
    print("unique mixed witness words:", dict(sorted(word_histogram.items())))
    print("coefficient-feasible packets: 0")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
