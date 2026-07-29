#!/usr/bin/env python3
"""Verify the two universal relabeling orbits of diagonal toric cuts.

Every seed guard is the union of the six matching terms in an odd three-row
Laurent circuit.  Vertex and colour relabeling preserves that contradiction,
so its full ``S_8 x S_3`` orbit gives target-independent support clauses.
"""

from __future__ import annotations

from itertools import permutations

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as search_toric
import search_parallel_binomial_nonzero_constants_cegar as toric
from verify_n8_toric_orbit40_boundary import boundary_support


def image_guard(guard, vertex_permutation, colour_permutation):
    image = []
    for u, v, a, b in guard:
        image_u, image_v = vertex_permutation[u], vertex_permutation[v]
        image_a, image_b = colour_permutation[a], colour_permutation[b]
        if image_u > image_v:
            image_u, image_v = image_v, image_u
            image_a, image_b = image_b, image_a
        image.append((image_u, image_v, image_a, image_b))
    return frozenset(image)


def full_orbit(guard):
    return {
        image_guard(guard, vertex_permutation, colour_permutation)
        for vertex_permutation in permutations(range(signed.N))
        for colour_permutation in permutations(range(signed.Q))
    }


def main():
    search = signed.LazySearch(
        40, "cadical195", max_cells=34, unique_constants=False
    )
    try:
        fibres = toric.exact_fibres(
            signed.N, boundary_support(), search.matchings
        )
        mixed, rows = search_toric.exponent_rows(search, fibres)
        circuits = search_toric.unit_triangle_circuits(rows)
        guards = {
            frozenset(
                cell
                for index in indices
                for _matching_number, decorated in mixed[index][1]
                for cell in decorated
            )
            for indices in circuits
        }
        assert len(circuits) == len(guards) == 48

        remaining = set(guards)
        orbit_data = []
        while remaining:
            representative = min(remaining, key=lambda item: tuple(sorted(item)))
            orbit = full_orbit(representative)
            members = remaining & orbit
            orbit_data.append((representative, orbit, len(members)))
            remaining -= members

        assert len(orbit_data) == 2
        assert sorted((len(orbit), members) for _rep, orbit, members in orbit_data) == [
            (30240, 16),
            (30240, 32),
        ]
        first_orbit = orbit_data[0][1]
        second_orbit = orbit_data[1][1]
        assert first_orbit.isdisjoint(second_orbit)
        independent_union = first_orbit | second_orbit
        encoder_union = set(search_toric.global_diagonal_triangle_guards())
        assert encoder_union == independent_union
        assert {
            representative for representative, _orbit, _members in orbit_data
        } == set(search_toric.DIAGONAL_TRIANGLE_GUARD_REPRESENTATIVES)
        assert all(
            len(guard) == 10
            and all(a == b for _u, _v, a, b in guard)
            for guard in independent_union
        )
        print(
            "PASS: 48 checked seed circuits generate two disjoint "
            "S8xS3 orbits of 30,240 sound 10-cell guards "
            "(60,480 total)"
        )
        for number, (representative, _orbit, members) in enumerate(orbit_data):
            print(
                f"class {number}: seed_members={members} "
                f"representative={tuple(sorted(representative))}"
            )
    finally:
        search.delete()


if __name__ == "__main__":
    main()
