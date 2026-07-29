#!/usr/bin/env python3
"""Verify the 7,560-clause one-row forced-pure-zero orbit."""

from __future__ import annotations

from itertools import permutations

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as search_toric
import search_parallel_binomial_nonzero_constants_cegar as toric


MIXED_GUARD = frozenset({
    (0, 2, 1, 1), (0, 4, 1, 1), (1, 5, 2, 2),
    (2, 6, 1, 1), (3, 7, 2, 2), (4, 6, 1, 1),
})
PURE_COLOUR = 1
PURE_MATCHINGS = frozenset({
    frozenset({(0, 2), (1, 3), (4, 6), (5, 7)}),
    frozenset({(0, 4), (1, 3), (2, 6), (5, 7)}),
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


def independent_schemas():
    answer = set()
    for vertex in permutations(range(signed.N)):
        matchings = frozenset(
            frozenset(
                tuple(sorted((vertex[u], vertex[v]))) for u, v in matching
            )
            for matching in PURE_MATCHINGS
        )
        for colour in permutations(range(signed.Q)):
            answer.add((
                independent_image_guard(MIXED_GUARD, vertex, colour),
                colour[PURE_COLOUR],
                matchings,
            ))
    return answer


def main():
    search = signed.LazySearch(
        40, "cadical195", max_cells=40, unique_constants=False
    )
    try:
        matching_index = {
            frozenset(matching): number
            for number, matching in enumerate(search.matchings)
        }
        pure_numbers = tuple(sorted(
            matching_index[matching] for matching in PURE_MATCHINGS
        ))
        assert pure_numbers == (16, 49)
        pure_colouring = (PURE_COLOUR,) * signed.N
        pure_terms = tuple(
            search.terms(pure_colouring)[number] for number in pure_numbers
        )

        mixed_colouring = (1, 2, 1, 2, 1, 2, 1, 2)
        mixed_numbers = (23, 52)
        mixed_terms = tuple(
            search.terms(mixed_colouring)[number]
            for number in mixed_numbers
        )
        assert frozenset(cell for term in mixed_terms for cell in term) == MIXED_GUARD

        mixed_row = toric.exponent_row(
            mixed_terms[0], mixed_terms[1], search.cell_index, len(search.cells)
        )
        pure_row = toric.exponent_row(
            pure_terms[0], pure_terms[1], search.cell_index, len(search.cells)
        )
        # Common factors differ, but the two matching ratios are identical.
        assert mixed_row == pure_row
        consistent, lattice = toric.signed_quotient_lattice(
            [mixed_row], len(search.cells)
        )
        assert consistent
        fibres = {pure_colouring: tuple(
            (number, search.terms(pure_colouring)[number])
            for number in pure_numbers
        )}
        remainder, classes = toric.reduced_constant_product(
            signed.N,
            fibres,
            lattice,
            search.cells,
            search.cell_index,
            colors=(PURE_COLOUR,),
        )
        assert not remainder and list(classes.values()) == [[1, 1]]

        schemas = independent_schemas()
        assert len(schemas) == 7560
        assert schemas == set(
            search_toric.global_one_row_pure_zero_schemas()
        )
        assert all(
            len(guard) == 6 and len(matchings) == 2
            for guard, _colour, matchings in schemas
        )
        print(
            "PASS: one mixed binomial has exactly the pure-term exponent "
            "difference; its S8xS3 orbit has 7,560 distinct exact "
            "111-literal pure-zero clauses"
        )
    finally:
        search.delete()


if __name__ == "__main__":
    main()
