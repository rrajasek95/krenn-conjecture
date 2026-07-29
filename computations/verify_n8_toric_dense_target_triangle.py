#!/usr/bin/env python3
"""Exact audit of the dense-chart twelve-cell target triangle guard."""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
import json
from pathlib import Path

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as toric


TARGETS = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 2), (1, 3), (4, 6), (5, 7)),
    ((0, 4), (1, 5), (2, 6), (3, 7)),
)
COLORINGS = (
    (0, 0, 0, 0, 0, 0, 2, 0),
    (0, 0, 0, 0, 0, 2, 0, 0),
    (0, 1, 0, 1, 0, 0, 2, 0),
)
SIGNS = (-1, 1, 1)


def independent_image_guard(guard, vertex, color):
    image = set()
    for u, v, a, b in guard:
        new_u, new_v = vertex[u], vertex[v]
        new_a, new_b = color[a], color[b]
        if new_u > new_v:
            new_u, new_v = new_v, new_u
            new_a, new_b = new_b, new_a
        image.add((new_u, new_v, new_a, new_b))
    return frozenset(image)


def independent_target_automorphisms():
    target_sets = tuple(map(frozenset, TARGETS))
    answer = []
    for vertex in permutations(range(signed.N)):
        images = tuple(
            frozenset(
                tuple(sorted((vertex[u], vertex[v])))
                for u, v in target
            )
            for target in TARGETS
        )
        for color in permutations(range(signed.Q)):
            if all(
                images[source] == target_sets[color[source]]
                for source in range(signed.Q)
            ):
                answer.append((vertex, color))
    return tuple(answer)


def main():
    guard = toric.DENSE_TARGET_TRIANGLE_GUARD_REPRESENTATIVE
    assert len(guard) == 12
    matchings = tuple(
        signed.core.perfect_matchings(tuple(range(signed.N)))
    )
    cells = tuple(
        (u, v, a, b)
        for u in range(signed.N)
        for v in range(u + 1, signed.N)
        for a, b in product(range(signed.Q), repeat=2)
    )
    cell_index = {cell: index for index, cell in enumerate(cells)}

    terms_by_coloring = []
    for coloring in COLORINGS:
        terms = []
        for matching in matchings:
            decorated = signed.decorated_term(coloring, matching)
            if set(decorated) <= guard:
                terms.append(decorated)
        assert len(terms) == 2
        terms_by_coloring.append(tuple(terms))
    assert frozenset(
        cell for terms in terms_by_coloring for term in terms for cell in term
    ) == guard

    rows = [
        signed.core.exponent_row(
            terms[0], terms[1], cell_index, len(cells)
        )
        for terms in terms_by_coloring
    ]
    assert all(
        sum(SIGNS[index] * rows[index][column] for index in range(3)) == 0
        for column in range(len(cells))
    )
    assert sum(SIGNS) % 2
    assert not signed.core.signed_quotient_lattice(rows, len(cells))[0]

    checkpoint = json.loads(Path(__file__).with_name(
        "n8_orbit40_pre_target9408_round6_structural.json"
    ).read_text())
    selected = frozenset(
        tuple(record["cell"]) for record in checkpoint["selected_cells"]
    )
    assert guard <= selected

    old_guards = set(toric.global_triangle_guards())
    full_orbit = set()
    for vertex in permutations(range(signed.N)):
        for color in permutations(range(signed.Q)):
            image = independent_image_guard(guard, vertex, color)
            assert image not in old_guards
            full_orbit.add(image)
    assert len(full_orbit) == 241920

    automorphisms = independent_target_automorphisms()
    assert len(automorphisms) == 48
    target_orbit = {
        independent_image_guard(guard, vertex, color)
        for vertex, color in automorphisms
    }
    assert len(target_orbit) == 48
    assert target_orbit == set(
        toric.target_dense_triangle_guards(automorphisms)
    )
    forced = frozenset(
        (u, v, color, color)
        for color, target in enumerate(TARGETS)
        for u, v in target
    )
    overlap_histogram = Counter(len(image & forced) for image in full_orbit)
    assert overlap_histogram == {
        0: 55680,
        1: 95616,
        2: 61824,
        3: 23808,
        4: 4608,
        5: 384,
    }
    high_overlap = {
        image for image in full_orbit if len(image & forced) >= 3
    }
    assert len(high_overlap) == 28800
    assert target_orbit <= high_overlap
    assert high_overlap == set(
        toric.target_dense_triangle_high_overlap_guards(TARGETS, 3)
    )
    reduced_high_overlap = {image - forced for image in high_overlap}
    assert len(reduced_high_overlap) == 28800
    assert Counter(map(len, reduced_high_overlap)) == {
        7: 384,
        8: 4608,
        9: 23808,
    }
    reduced = {image - forced for image in target_orbit}
    assert len(reduced) == 48
    assert Counter(map(len, reduced)) == {7: 48}
    print(
        "PASS: dense 12-cell guard has the exact odd three-row relation; "
        "its full orbit has 241,920 guards disjoint from the prior 181,440, "
        "its target orbit has 48 seven-literal guards, and the complete "
        "three-plus forced-cell slice has 28,800 distinct 7--9 literal guards"
    )


if __name__ == "__main__":
    main()
