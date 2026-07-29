#!/usr/bin/env python3
"""Exact audit of the 28-cell orbit-40 monomial boundary.

The support is one diagonal cell on every edge of K8.  It has the requested
orbit-40 pure matchings and every mixed fibre has exactly two terms, but its
Laurent phase equations contain many three-row odd circuits.  Consequently
no assignment of arbitrary nonzero complex weights (not merely signs) can
make all of those binomials vanish.
"""

from __future__ import annotations

from collections import Counter

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as toric_search
import search_parallel_binomial_nonzero_constants_cegar as toric


def boundary_support():
    colour_one = {(0, 2), (1, 3), (4, 6), (5, 7)}
    colour_two = {
        (0, 4), (0, 6), (1, 5), (1, 7),
        (2, 4), (2, 6), (3, 5), (3, 7),
    }
    return frozenset(
        (
            u,
            v,
            1 if (u, v) in colour_one else 2 if (u, v) in colour_two else 0,
            1 if (u, v) in colour_one else 2 if (u, v) in colour_two else 0,
        )
        for u in range(signed.N)
        for v in range(u + 1, signed.N)
    )


def main():
    search = signed.LazySearch(
        40, "cadical195", max_cells=34, unique_constants=False
    )
    try:
        selected = boundary_support()
        assert len(selected) == 28
        assert search.forced_support <= selected
        fibres = toric.exact_fibres(
            signed.N, selected, search.matchings
        )
        distribution = Counter(map(len, fibres.values()))
        assert distribution == {1: 1, 2: 38, 4: 1, 24: 1}
        assert all(
            len(terms) == 2
            for colouring, terms in fibres.items()
            if len(set(colouring)) > 1
        )

        mixed, rows = toric_search.exponent_rows(search, fibres)
        assert len(mixed) == 38
        assert not toric.signed_quotient_lattice(
            rows, len(search.cells)
        )[0]

        circuits = toric_search.unit_triangle_circuits(rows)
        assert len(circuits) == 48
        guard_sizes = []
        for indices in circuits:
            assert len(indices) == 3
            selected_rows = [rows[index] for index in indices]
            assert not toric.signed_quotient_lattice(
                selected_rows, len(search.cells)
            )[0]
            relation = toric.flint_odd_relation(selected_rows)
            assert relation is not None
            assert sum(relation) % 2
            assert all(
                sum(
                    relation[i] * selected_rows[i][column]
                    for i in range(3)
                ) == 0
                for column in range(len(search.cells))
            )
            guarded = {
                cell
                for index in indices
                for _matching_number, decorated in mixed[index][1]
                for cell in decorated
            }
            guard_sizes.append(len(guarded))
        assert Counter(guard_sizes) == {10: 48}
        print(
            "PASS: orbit40 boundary has 28 cells, 38 mixed binomials, "
            "and 48 exact odd three-row circuits (all 10-cell guards)"
        )
    finally:
        search.delete()


if __name__ == "__main__":
    main()
