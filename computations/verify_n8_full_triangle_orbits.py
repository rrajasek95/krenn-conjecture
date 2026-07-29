#!/usr/bin/env python3
"""Independent exact audit of the 60,480 preloaded triangle guards."""

from __future__ import annotations

from itertools import permutations

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as toric_search
import verify_n8_toric_orbit40_boundary as boundary


def main():
    # Re-expand the two representatives here rather than calling the search
    # helper, so its orbit generation and deduplication are checked afresh.
    vertex_permutations = tuple(permutations(range(signed.N)))
    color_permutations = tuple(permutations(range(signed.Q)))
    orbits = []
    for representative in toric_search.DIAGONAL_TRIANGLE_GUARD_REPRESENTATIVES:
        images = set()
        for vertex_permutation in vertex_permutations:
            for color_permutation in color_permutations:
                image = frozenset(
                    signed.image_cell(
                        cell, vertex_permutation, color_permutation
                    )
                    for cell in representative
                )
                assert len(image) == 10
                images.add(image)
        assert len(images) == 30240
        orbits.append(images)
    assert orbits[0].isdisjoint(orbits[1])
    guards = orbits[0] | orbits[1]
    assert len(guards) == 60480
    assert guards == set(toric_search.global_diagonal_triangle_guards())

    targets = signed.core.target_orbits(signed.N)[40]
    matchings = tuple(
        signed.core.perfect_matchings(tuple(range(signed.N)))
    )

    class SearchData:
        cells = tuple(
            (u, v, a, b)
            for u in range(signed.N)
            for v in range(u + 1, signed.N)
            for a in range(signed.Q)
            for b in range(signed.Q)
        )
        cell_index = {cell: index for index, cell in enumerate(cells)}

    selected = boundary.boundary_support()
    fibres = signed.core.exact_fibres(
        signed.N, selected, matchings
    )
    mixed, rows = toric_search.exponent_rows(SearchData, fibres)
    circuits = toric_search.unit_triangle_circuits(rows)
    assert len(circuits) == 48
    boundary_guards = set()
    for indices in circuits:
        selected_rows = [rows[index] for index in indices]
        relation = signed.core.flint_odd_relation(selected_rows)
        assert relation is not None and sum(relation) % 2
        assert all(
            sum(
                relation[i] * selected_rows[i][column]
                for i in range(3)
            ) == 0
            for column in range(len(SearchData.cells))
        )
        guard = frozenset(
            cell
            for index in indices
            for _matching_number, decorated in mixed[index][1]
            for cell in decorated
        )
        assert len(guard) == 10
        boundary_guards.add(guard)

    # Each claimed full orbit contains a directly audited boundary circuit.
    # Relabeling its vertices and colors preserves the odd integer relation,
    # so every one of the 60,480 guards is sound.
    assert boundary_guards <= guards
    assert all(boundary_guards & orbit for orbit in orbits)

    all_guards = set(toric_search.global_triangle_guards())
    additional = set(toric_search.global_additional_triangle_guards())
    assert guards.isdisjoint(additional)
    assert len(additional) == 120960
    assert all_guards == guards | additional
    assert len(all_guards) == 181440

    forced = frozenset(
        (u, v, color, color)
        for color, target in enumerate(targets)
        for u, v in target
    )
    reduced = {frozenset(guard - forced) for guard in all_guards}
    assert frozenset() not in reduced
    assert all(1 <= len(clause) <= 10 for clause in reduced)
    print(
        "PASS full triangle preload: 181440 total guards in five audited "
        f"orbits, {len(reduced)} distinct target-reduced clauses"
    )


if __name__ == "__main__":
    main()
