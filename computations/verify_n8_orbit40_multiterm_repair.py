#!/usr/bin/env python3
"""Independent exact checks for the orbit-40 multi-term repair note."""

from __future__ import annotations

from collections import Counter

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import search_n8_orbit40_multiterm_completion as repair
import search_n8_toric_binomial_lazy_cegar as toric_search
import search_parallel_binomial_nonzero_constants_cegar as toric


SEVEN_COVER = frozenset({
    (1, 3, 2, 0), (4, 5, 0, 2), (4, 6, 0, 0),
    (4, 7, 0, 2), (5, 6, 2, 0), (5, 7, 0, 0),
    (6, 7, 0, 2),
})


def fibre_histogram(fibres):
    return Counter(
        len(terms)
        for colouring, terms in fibres.items()
        if len(set(colouring)) > 1
    )


def focused_seed_circuit_cover(search, base, seed_mixed, triangles):
    """Prove the minimum cell cover of the 136 original triangles is seven."""

    optional = tuple(sorted(set(search.cells) - base))
    support = {cell: index + 1 for index, cell in enumerate(optional)}
    top = len(optional)
    clauses = []
    events = {}
    used_rows = {index for triangle in triangles for index in triangle}

    for index in used_rows:
        colouring, pair = seed_mixed[index]
        pair_numbers = {number for number, _decorated in pair}
        row_events = []
        for number, decorated in enumerate(search.terms(colouring)):
            if number in pair_numbers:
                continue
            missing = frozenset(decorated) - base
            assert missing
            top += 1
            selector = top
            row_events.append(selector)
            for cell in missing:
                clauses.append([-selector, support[cell]])
        events[index] = row_events

    for triangle in triangles:
        clauses.append([
            selector
            for index in triangle
            for selector in events[index]
        ])

    first_model = None
    for cap in range(1, 8):
        cardinality = CardEnc.atmost(
            lits=list(support.values()),
            bound=cap,
            top_id=top,
            encoding=EncType.kmtotalizer,
        )
        with Solver(
            name="cadical195",
            bootstrap_with=clauses + cardinality.clauses,
        ) as solver:
            satisfiable = solver.solve()
            assert satisfiable == (cap == 7)
            if satisfiable:
                positive = {literal for literal in solver.get_model() if literal > 0}
                first_model = frozenset(
                    cell for cell, variable in support.items()
                    if variable in positive
                )
                assert len(first_model) == 7
    return first_model


def main():
    search = repair.CompletionSearch(None, symmetry=False)
    try:
        seed = search.seed
        seed_fibres = repair.exact_fibres(search, seed)
        assert len(seed) == 30
        assert fibre_histogram(seed_fibres) == {1: 2, 2: 51, 3: 1}

        seed_mixed, seed_rows = repair.binomial_system(search, seed_fibres)
        consistent, _lattice = toric.signed_quotient_lattice(
            seed_rows, len(search.cells)
        )
        assert not consistent
        seed_triangles = toric_search.unit_triangle_circuits(seed_rows)
        assert len(seed_triangles) == 136

        # Audit the displayed human-readable odd triangle term by term.
        displayed = {
            (0, 0, 0, 0, 1, 0, 1, 0): {
                frozenset({
                    (0, 5, 0, 0), (1, 3, 0, 0),
                    (2, 7, 0, 0), (4, 6, 1, 1),
                }),
                frozenset({
                    (0, 7, 0, 0), (1, 3, 0, 0),
                    (2, 5, 0, 0), (4, 6, 1, 1),
                }),
            },
            (0, 0, 0, 2, 1, 0, 1, 2): {
                frozenset({
                    (0, 1, 0, 0), (2, 5, 0, 0),
                    (3, 7, 2, 2), (4, 6, 1, 1),
                }),
                frozenset({
                    (0, 5, 0, 0), (1, 2, 0, 0),
                    (3, 7, 2, 2), (4, 6, 1, 1),
                }),
            },
            (0, 0, 0, 2, 1, 2, 1, 0): {
                frozenset({
                    (0, 1, 0, 0), (2, 7, 0, 0),
                    (3, 5, 2, 2), (4, 6, 1, 1),
                }),
                frozenset({
                    (0, 7, 0, 0), (1, 2, 0, 0),
                    (3, 5, 2, 2), (4, 6, 1, 1),
                }),
            },
        }
        for colouring, expected in displayed.items():
            observed = {
                frozenset(decorated)
                for _number, decorated in seed_fibres[colouring]
            }
            assert observed == expected

        base46 = seed | repair.NO_SINGLETON_46_EXTRA
        base_fibres = repair.exact_fibres(search, base46)
        assert len(base46) == 46
        assert fibre_histogram(base_fibres) == {2: 224, 4: 19}
        assert tuple(
            len(base_fibres[(colour,) * repair.N])
            for colour in range(repair.Q)
        ) == (26, 2, 4)
        base_mixed, base_rows = repair.binomial_system(search, base_fibres)
        assert not toric.signed_quotient_lattice(
            base_rows, len(search.cells)
        )[0]
        assert len(toric_search.unit_triangle_circuits(base_rows)) == 7968

        found_cover = focused_seed_circuit_cover(
            search, base46, seed_mixed, seed_triangles
        )
        assert len(found_cover) == 7

        covered_fibres = repair.exact_fibres(search, base46 | SEVEN_COVER)
        assert fibre_histogram(covered_fibres)[1] == 79
        covered_mixed, covered_rows = repair.binomial_system(
            search, covered_fibres
        )
        assert not toric.signed_quotient_lattice(
            covered_rows, len(search.cells)
        )[0]
        assert len(toric_search.unit_triangle_circuits(covered_rows)) == 790

        # Every original triangle is genuinely broken by the displayed cover.
        for triangle in seed_triangles:
            assert any(
                len(covered_fibres[seed_mixed[index][0]]) >= 3
                for index in triangle
            )

        print(
            "PASS: seed census/odd triangle, base46 census/7968 circuits, "
            "and exact minimum seven-cell seed-circuit cover"
        )
    finally:
        search.delete()


if __name__ == "__main__":
    main()
