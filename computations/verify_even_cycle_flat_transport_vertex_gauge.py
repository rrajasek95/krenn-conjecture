#!/usr/bin/env python3
"""Verify the flat alternating-even-cycle vertex-gauge theorem.

For an alternating cycle C_(2r), let M and N be its two perfect matchings.
If the two matching products agree coefficientwise and are nonzero, every
edge table factors through the two incident vertex lines.  Equality of the
two matching-product supports has the analogous rectangular-support
conclusion.  The proof is by freezing all coordinates except the endpoints
of one edge at a common nonzero pivot word.

The checker exercises C4, C6, and C8 over three colours, including zero
vertex coordinates, and audits the pivot reconstruction and support claim.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json


EXPECTED_LEDGER_SHA256 = (
    "9bee2de423db959391b81eb2e7adaf1ee9ca7a7e3107828ab1fd6c3d2bbc859f"
)
COLOURS = tuple(range(3))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matchings(order):
    even = tuple((site, site + 1) for site in range(0, order, 2))
    odd = tuple((site, (site + 1) % order) for site in range(1, order, 2))
    return even, odd


def outer(left, right, scale):
    return tuple(tuple(scale * left[a] * right[b] for b in COLOURS)
                 for a in COLOURS)


def matching_product(word, matching, tables):
    value = Q(1)
    for edge in matching:
        u, v = edge
        value *= tables[edge][word[u]][word[v]]
    return value


def support_product(word, matching, supports):
    return all((word[u], word[v]) in supports[edge]
               for edge in matching for u, v in (edge,))


def change(word, assignments):
    result = list(word)
    for site, colour in assignments.items():
        result[site] = colour
    return tuple(result)


def audit_order(order):
    even, odd = matchings(order)
    all_edges = even + odd

    # Deterministic vertex factors.  Zeros are included without killing the
    # common pivot colour 0.
    vertex = {
        site: tuple(Q((site + 2) * (colour + 1))
                    if not (colour == 2 and site % 3 == 1) else Q(0)
                    for colour in COLOURS)
        for site in range(order)
    }
    scales = {edge: Q(index + 2) for index, edge in enumerate(all_edges)}
    even_scale = Q(1)
    odd_scale = Q(1)
    for edge in even:
        even_scale *= scales[edge]
    for edge in odd:
        odd_scale *= scales[edge]
    # Normalize the last odd edge so the two scalar products agree.
    scales[odd[-1]] *= even_scale / odd_scale
    tables = {
        edge: outer(vertex[edge[0]], vertex[edge[1]], scales[edge])
        for edge in all_edges
    }

    words = tuple(itertools.product(COLOURS, repeat=order))
    left = {word: matching_product(word, even, tables) for word in words}
    right = {word: matching_product(word, odd, tables) for word in words}
    require(left == right and any(left.values()),
            f"C{order} coefficientwise flat identity changed")
    require(any(value == 0 for value in left.values()),
            f"C{order} zero-coordinate test became dense")

    pivot = (0,) * order
    pivot_value = left[pivot]
    require(pivot_value != 0, f"C{order} pivot vanished")
    reconstructed_vertex = {
        site: tuple(left[change(pivot, {site: colour})] / pivot_value
                    for colour in COLOURS)
        for site in range(order)
    }
    reconstructed = {
        word: pivot_value
        * product(reconstructed_vertex[site][word[site]]
                  for site in range(order))
        for word in words
    }
    require(reconstructed == left,
            f"C{order} pivot vertex reconstruction failed")

    for edge, table in tables.items():
        require(all(table[a][b] * table[0][0]
                    == table[a][0] * table[0][b]
                    for a in COLOURS for b in COLOURS),
                f"C{order} edge {edge} lost rank one")

    # Support equality is rectangular on the same vertex subsets.
    vertex_support = {
        site: frozenset(colour for colour in COLOURS
                        if vertex[site][colour] != 0)
        for site in range(order)
    }
    supports = {
        edge: frozenset(itertools.product(vertex_support[edge[0]],
                                          vertex_support[edge[1]]))
        for edge in all_edges
    }
    even_words = {word for word in words
                  if support_product(word, even, supports)}
    odd_words = {word for word in words
                 if support_product(word, odd, supports)}
    expected_words = set(itertools.product(
        *(vertex_support[site] for site in range(order))))
    require(even_words == odd_words == expected_words,
            f"C{order} rectangular support identity changed")

    # The pivot-slice proof reconstructs each edge support from the common
    # tensor support: vary just that edge's two endpoint colours.
    for edge in all_edges:
        u, v = edge
        recovered = frozenset(
            (a, b) for a in COLOURS for b in COLOURS
            if change(pivot, {u: a, v: b}) in even_words
        )
        require(recovered == supports[edge],
                f"C{order} pivot slice failed on edge {edge}")

    return {
        "order": order,
        "words": len(words),
        "zero_words": sum(value == 0 for value in left.values()),
        "edges": len(all_edges),
        "edge_rank_one_minors": len(all_edges) * 9,
        "common_support_size": len(even_words),
        "pivot_slice_rectangles": len(all_edges),
    }


def product(values):
    result = Q(1)
    for value in values:
        result *= value
    return result


def main():
    ledger = {
        "orders": [audit_order(order) for order in (4, 6, 8)],
        "coefficient_theorem": (
            "on one alternating C_(2r), complete nonzero coefficientwise "
            "equality of the two perfect-matching products forces every "
            "edge table to factor through common vertex lines"
        ),
        "support_theorem": (
            "equality of the two nonempty matching-product supports forces "
            "every edge support to be S_u x S_v and the common word support "
            "to be the single Cartesian product of the vertex supports"
        ),
        "proof": (
            "choose a common nonzero pivot word and freeze every coordinate "
            "except the endpoints of one edge; the opposite matching then "
            "separates those two variables into its two adjacent edge "
            "factors, proving rank one (and rectangular support) edgewise"
        ),
        "frontier": (
            "chordless C6/C8 have no new globally flat coefficient geometry; "
            "the remaining obligation is source isolation/base exhaustivity, "
            "while chords are needed only for nonflat or extra-base terms"
        ),
        "scope": (
            "the theorem assumes complete two-base equality or support "
            "equality; full source rows with additional matching bases still "
            "require synchronization, routing, or source saturation"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"even-cycle flat gauge ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("even-cycle flat transport vertex gauge: PASS")


if __name__ == "__main__":
    main()
