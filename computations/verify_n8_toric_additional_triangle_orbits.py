#!/usr/bin/env python3
"""Independently certify three additional global toric guard orbits."""

from __future__ import annotations

from collections import Counter
from itertools import permutations

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as search_toric
import search_parallel_binomial_nonzero_constants_cegar as toric


REPRESENTATIVES = (
    frozenset({
        (0, 1, 0, 0), (0, 3, 0, 0), (0, 6, 1, 2),
        (1, 2, 0, 0), (1, 4, 0, 0), (2, 3, 0, 0),
        (2, 6, 1, 1), (3, 4, 0, 0), (4, 6, 1, 1),
        (5, 7, 1, 1),
    }),
    frozenset({
        (0, 1, 0, 0), (0, 3, 0, 0), (0, 4, 2, 2),
        (1, 2, 0, 0), (1, 6, 0, 0), (2, 3, 0, 0),
        (2, 4, 0, 0), (3, 6, 0, 0), (4, 6, 1, 1),
        (5, 7, 1, 1),
    }),
    frozenset({
        (0, 1, 0, 0), (0, 3, 0, 0), (0, 6, 0, 0),
        (1, 2, 0, 0), (1, 4, 0, 0), (2, 3, 0, 0),
        (2, 6, 1, 1), (3, 4, 0, 0), (4, 6, 1, 1),
        (5, 7, 1, 1),
    }),
)


def independent_image(guard, vertex_permutation, colour_permutation):
    answer = []
    for u, v, a, b in guard:
        u, v = vertex_permutation[u], vertex_permutation[v]
        a, b = colour_permutation[a], colour_permutation[b]
        if u > v:
            u, v, a, b = v, u, b, a
        answer.append((u, v, a, b))
    return frozenset(answer)


def independent_orbit(guard):
    return {
        independent_image(guard, vertex, colour)
        for vertex in permutations(range(signed.N))
        for colour in permutations(range(signed.Q))
    }


def certify_representative(search, guard):
    """Recover the three binomials from the ten cells and check their circuit."""

    fibres = toric.exact_fibres(signed.N, guard, search.matchings)
    assert Counter(map(len, fibres.values())) == {2: 3}
    pairs = [
        (colouring, terms)
        for colouring, terms in sorted(fibres.items())
        if len(set(colouring)) > 1
    ]
    assert len(pairs) == 3
    rows = [
        toric.exponent_row(
            terms[0][1], terms[1][1], search.cell_index, len(search.cells)
        )
        for _colouring, terms in pairs
    ]
    circuits = search_toric.unit_triangle_circuits(rows)
    assert circuits == ((0, 1, 2),)
    assert not toric.signed_quotient_lattice(rows, len(search.cells))[0]
    recovered_guard = frozenset(
        cell
        for _colouring, terms in pairs
        for _matching_number, decorated in terms
        for cell in decorated
    )
    assert recovered_guard == guard


def main():
    search = signed.LazySearch(
        40, "cadical195", max_cells=40, unique_constants=False
    )
    try:
        for representative in REPRESENTATIVES:
            certify_representative(search, representative)

        orbits = tuple(independent_orbit(rep) for rep in REPRESENTATIVES)
        assert tuple(map(len, orbits)) == (30240, 60480, 30240)
        assert all(
            orbits[i].isdisjoint(orbits[j])
            for i in range(3)
            for j in range(i + 1, 3)
        )
        old = set(search_toric.global_diagonal_triangle_guards())
        additional = set().union(*orbits)
        assert old.isdisjoint(additional)
        assert len(additional) == 120960
        assert additional == set(
            search_toric.global_additional_triangle_guards()
        )
        assert old | additional == set(search_toric.global_triangle_guards())
        assert set(REPRESENTATIVES) == set(
            search_toric.ADDITIONAL_TRIANGLE_GUARD_REPRESENTATIVES
        )
        print(
            "PASS: three self-contained odd circuits generate disjoint "
            "orbits 30,240 + 60,480 + 30,240; production preload is "
            "exactly 181,440 guards including the prior 60,480"
        )
    finally:
        search.delete()


if __name__ == "__main__":
    main()
