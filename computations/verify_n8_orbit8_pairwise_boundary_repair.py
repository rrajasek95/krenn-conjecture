#!/usr/bin/env python3
"""Exact audits for the supplied orbit-8 pairwise-Hamilton boundary."""

from __future__ import annotations

from collections import Counter

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import search_n8_orbit8_pairwise_boundary_repair as repair
import search_n8_sparse_triple_completion as sparse
import search_n8_toric_binomial_lazy_cegar as toric_search
import search_parallel_binomial_nonzero_constants_cegar as toric


BALANCED_COVER = frozenset({
    (0, 4, 1, 1), (0, 5, 2, 2),
    (1, 2, 1, 1), (1, 3, 2, 2),
})


def mixed_histogram(fibres):
    return Counter(
        len(terms)
        for colouring, terms in fibres.items()
        if len(set(colouring)) > 1
    )


def minimum_triangle_cover(search, mixed, triangles):
    base = search.boundary
    optional = tuple(sorted(set(search.cells) - base))
    support = {cell: index + 1 for index, cell in enumerate(optional)}
    top = len(optional)
    clauses = []
    events = {}
    for index in {i for triangle in triangles for i in triangle}:
        colouring, pair = mixed[index]
        pair_numbers = {number for number, _decorated in pair}
        row_events = []
        for number, decorated in enumerate(search.terms(colouring)):
            if number in pair_numbers:
                continue
            missing = frozenset(decorated) - base
            top += 1
            selector = top
            row_events.append(selector)
            for cell in missing:
                clauses.append([-selector, support[cell]])
        events[index] = row_events
    clauses.extend([
        selector
        for index in triangle
        for selector in events[index]
    ] for triangle in triangles)

    witness = None
    for cap in range(1, 5):
        cardinality = CardEnc.atmost(
            lits=list(support.values()), bound=cap, top_id=top,
            encoding=EncType.kmtotalizer,
        )
        with Solver(
            name="cadical195",
            bootstrap_with=clauses + cardinality.clauses,
        ) as solver:
            satisfiable = solver.solve()
            assert satisfiable == (cap == 4)
            if satisfiable:
                positive = {literal for literal in solver.get_model() if literal > 0}
                witness = frozenset(
                    cell for cell, variable in support.items()
                    if variable in positive
                )
                assert len(witness) == 4
    return witness


def quotient_equation(remainder):
    assert len(remainder) == 2
    (left, a), (right, b) = sorted(remainder.items())
    assert abs(a) == abs(b)
    return (
        tuple(x - y for x, y in zip(left, right)),
        int((a > 0) == (b > 0)),
    )


def main():
    search = repair.Orbit8RepairSearch(None, "cadical195")
    try:
        base_fibres, base_mixed, base_rows, triangles = repair.audit_boundary(
            search
        )
        assert mixed_histogram(base_fibres) == {2: 22}
        assert tuple(
            len(base_fibres[(colour,) * sparse.N])
            for colour in range(sparse.Q)
        ) == (1, 2, 2)
        assert len(triangles) == 12
        assert len(minimum_triangle_cover(search, base_mixed, triangles)) == 4

        # The balanced four-cell cover: six quotient binomials close
        # consistently, after which the pure product is identically zero.
        balanced_fibres = sparse.exact_fibres(
            search, search.boundary | BALANCED_COVER
        )
        assert mixed_histogram(balanced_fibres) == {1: 4, 2: 40, 4: 6}
        _balanced_mixed, balanced_rows = sparse.binomial_system(
            search, balanced_fibres
        )
        consistent, lattice = toric.signed_quotient_lattice(
            balanced_rows, len(search.cells)
        )
        assert consistent
        four_remainders = [
            sparse.reduced_polynomial(search, terms, lattice)
            for colouring, terms in balanced_fibres.items()
            if len(set(colouring)) > 1 and len(terms) == 4
        ]
        assert len(four_remainders) == 6
        assert all(
            len(remainder) == 2
            and len({abs(value) for value in remainder.values()}) == 1
            for remainder in four_remainders
        )
        extra_equations = [
            quotient_equation(remainder) for remainder in four_remainders
        ]
        four_colourings = [
            colouring
            for colouring, terms in balanced_fibres.items()
            if len(set(colouring)) > 1 and len(terms) == 4
        ]
        for colouring, (row, bit) in zip(
            four_colourings, extra_equations
        ):
            one_consistent, one_lattice = toric.signed_quotient_lattice(
                balanced_rows + [row], len(search.cells),
                [1] * len(balanced_rows) + [bit],
            )
            assert one_consistent
            majority_colour = (
                1 if colouring.count(1) > colouring.count(2) else 2
            )
            one_pure, _one_classes = toric.reduced_constant_product(
                sparse.N, balanced_fibres, one_lattice,
                search.cells, search.cell_index, (majority_colour,),
            )
            assert not one_pure
        closure_rows = balanced_rows + [row for row, _bit in extra_equations]
        closure_rhs = [1] * len(balanced_rows) + [
            bit for _row, bit in extra_equations
        ]
        consistent, closure_lattice = toric.signed_quotient_lattice(
            closure_rows, len(search.cells), closure_rhs
        )
        assert consistent
        closure_pure, _classes = toric.reduced_constant_product(
            sparse.N, balanced_fibres, closure_lattice,
            search.cells, search.cell_index,
        )
        assert not closure_pure

        # First 34-cell quotient-consistent completion from the dedicated
        # CEGAR.  Its pure colour-1 fibre is killed by one mixed binomial.
        first_support = (
            search.boundary | repair.FIRST_CONSISTENT_EXTRA
        )
        first_fibres = sparse.exact_fibres(search, first_support)
        assert len(first_support) == 34
        assert mixed_histogram(first_fibres) == {2: 54, 4: 8}
        first_mixed, first_rows = sparse.binomial_system(
            search, first_fibres
        )
        consistent, first_lattice = toric.signed_quotient_lattice(
            first_rows, len(search.cells)
        )
        assert consistent
        first_pure, _classes = toric.reduced_constant_product(
            sparse.N, first_fibres, first_lattice,
            search.cells, search.cell_index,
        )
        assert not first_pure
        used_rows, colours = toric.minimize_zero_product_certificate(
            sparse.N, first_fibres, first_rows,
            search.cells, search.cell_index,
        )
        assert len(used_rows) == 1
        assert colours == (1,)
        assert first_mixed[used_rows[0]][0] == (
            1, 0, 1, 1, 2, 1, 1, 1
        )

        expected_pair = {
            frozenset({
                (0, 2, 1, 1), (1, 4, 0, 2),
                (3, 6, 1, 1), (5, 7, 1, 1),
            }),
            frozenset({
                (0, 2, 1, 1), (1, 4, 0, 2),
                (3, 7, 1, 1), (5, 6, 1, 1),
            }),
        }
        assert {
            frozenset(decorated)
            for _number, decorated
            in first_fibres[(1, 0, 1, 1, 2, 1, 1, 1)]
        } == expected_pair
        expected_pure = {
            frozenset({
                (0, 2, 1, 1), (1, 4, 1, 1),
                (3, 6, 1, 1), (5, 7, 1, 1),
            }),
            frozenset({
                (0, 2, 1, 1), (1, 4, 1, 1),
                (3, 7, 1, 1), (5, 6, 1, 1),
            }),
        }
        assert {
            frozenset(decorated)
            for _number, decorated in first_fibres[(1,) * sparse.N]
        } == expected_pure

        four_remainders = [
            sparse.reduced_polynomial(search, terms, first_lattice)
            for colouring, terms in first_fibres.items()
            if len(set(colouring)) > 1 and len(terms) == 4
        ]
        assert len(four_remainders) == 8
        assert all(
            len(remainder) == 1
            and tuple(map(abs, remainder.values())) == (2,)
            for remainder in four_remainders
        )

        print(
            "PASS: orbit8 boundary/12 triangles, minimum four-cell cover, "
            "balanced quotient closure, and 34-cell pure/monomial obstruction"
        )
    finally:
        search.delete()


if __name__ == "__main__":
    main()
