#!/usr/bin/env python3
"""Verify the first minimized three-row pure-zero certificate at n=8."""

from __future__ import annotations

from collections import Counter
from itertools import permutations

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as search_toric
import search_parallel_binomial_nonzero_constants_cegar as toric


SELECTED = frozenset({
    (0, 1, 0, 0), (0, 2, 1, 1), (0, 3, 0, 0), (0, 4, 2, 2),
    (0, 5, 0, 0), (0, 7, 0, 0), (1, 2, 0, 0), (1, 3, 1, 1),
    (1, 3, 1, 2), (1, 3, 2, 1), (1, 3, 2, 2), (1, 4, 0, 0),
    (1, 5, 1, 1), (1, 5, 1, 2), (1, 5, 2, 1), (1, 5, 2, 2),
    (1, 6, 0, 0), (2, 3, 0, 0), (2, 5, 0, 0), (2, 6, 2, 2),
    (2, 7, 0, 0), (3, 4, 0, 0), (3, 6, 0, 0), (3, 7, 1, 1),
    (3, 7, 1, 2), (3, 7, 2, 1), (3, 7, 2, 2), (4, 5, 0, 0),
    (4, 6, 1, 1), (4, 7, 0, 0), (5, 6, 0, 0), (5, 7, 1, 1),
    (5, 7, 1, 2), (5, 7, 2, 1), (5, 7, 2, 2), (6, 7, 0, 0),
})

PURE_COLOUR = 1
PURE_MATCHINGS = frozenset({
    frozenset({(0, 2), (1, 3), (4, 6), (5, 7)}),
    frozenset({(0, 2), (1, 5), (3, 7), (4, 6)}),
})


def independent_image_guard(guard, vertex, colour):
    answer = []
    for u, v, a, b in guard:
        u, v = vertex[u], vertex[v]
        a, b = colour[a], colour[b]
        if u > v:
            u, v, a, b = v, u, b, a
        answer.append((u, v, a, b))
    return frozenset(answer)


def main():
    search = signed.LazySearch(
        40, "cadical195", max_cells=40, unique_constants=False
    )
    try:
        fibres = toric.exact_fibres(
            signed.N, SELECTED, search.matchings
        )
        assert Counter(map(len, fibres.values())) == {2: 96, 24: 1}
        assert tuple(len(fibres[(colour,) * signed.N]) for colour in range(3)) == (
            24, 2, 2
        )
        mixed, rows = search_toric.exponent_rows(search, fibres)
        assert len(mixed) == len(rows) == 94
        consistent, lattice = toric.signed_quotient_lattice(
            rows, len(search.cells)
        )
        assert consistent
        remainder, classes = toric.reduced_constant_product(
            signed.N,
            fibres,
            lattice,
            search.cells,
            search.cell_index,
        )
        assert not remainder and len(classes) == 1

        used, colours = toric.minimize_zero_product_certificate(
            signed.N,
            fibres,
            rows,
            search.cells,
            search.cell_index,
        )
        assert used == (75,) and colours == (1,)
        minimal_rows = [rows[index] for index in used]
        minimal_consistent, minimal_lattice = toric.signed_quotient_lattice(
            minimal_rows, len(search.cells)
        )
        assert minimal_consistent
        minimal_remainder, minimal_classes = toric.reduced_constant_product(
            signed.N,
            fibres,
            minimal_lattice,
            search.cells,
            search.cell_index,
            colours,
        )
        assert not minimal_remainder
        assert list(minimal_classes.values()) == [[1, 1]]

        # The originally discovered three-row certificate remains a valid
        # independently checked schema, but it is subsumed by row 75.
        three_used = (77, 79, 81)
        reduced_rows = [rows[index] for index in three_used]
        reduced_consistent, reduced_lattice = toric.signed_quotient_lattice(
            reduced_rows, len(search.cells)
        )
        assert reduced_consistent
        reduced_remainder, reduced_classes = toric.reduced_constant_product(
            signed.N,
            fibres,
            reduced_lattice,
            search.cells,
            search.cell_index,
            colours,
        )
        assert not reduced_remainder
        assert list(reduced_classes.values()) == [[1, 1]]
        assert {
            tuple(terms[index][0] for index in range(2))
            for _colouring, terms in (mixed[row] for row in three_used)
        } == {(49, 52)}
        guard = {
            cell
            for index in three_used
            for _matching_number, decorated in mixed[index][1]
            for cell in decorated
        }
        assert len(guard) == 10
        assert frozenset(guard) == search_toric.THREE_ROW_PURE_ZERO_MIXED_GUARD
        schemas = set()
        for vertex in permutations(range(signed.N)):
            image_matchings = frozenset(
                frozenset(
                    tuple(sorted((vertex[u], vertex[v])))
                    for u, v in matching
                )
                for matching in PURE_MATCHINGS
            )
            for colour in permutations(range(signed.Q)):
                schemas.add((
                    independent_image_guard(guard, vertex, colour),
                    colour[PURE_COLOUR],
                    image_matchings,
                ))
        assert len(schemas) == 15120
        assert schemas == set(
            search_toric.global_three_row_pure_zero_schemas()
        )
        print(
            "PASS: 36-cell chart has a one-row pure-zero witness; the "
            "alternative three-row 10-cell certificate is exact but "
            "subsumed, and its S8xS3 orbit has 15,120 schemas"
        )
    finally:
        search.delete()


if __name__ == "__main__":
    main()
