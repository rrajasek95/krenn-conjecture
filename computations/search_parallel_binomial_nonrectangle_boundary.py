#!/usr/bin/env python3
"""Seek a phase-consistent 0/2 support not killed by a literal rectangle.

This discovery search tests the proposed strengthening that three selected
constant matchings force a two-vertex recoloring rectangle.  Odd mixed
lattice supports are cut soundly.  Phase-consistent supports with a zero
constant product are inspected for the literal four-corner pattern; those
with a rectangle are blocked exactly and search resumes.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product

from pysat.solvers import Solver

import search_parallel_binomial_nonzero_constants_cegar as core


def underlying(decorated):
    return frozenset((u, v) for u, v, _a, _b in decorated)


def literal_rectangles(size, fibres):
    answer = []
    for color in range(core.Q):
        pure_coloring = (color,) * size
        pure_terms = fibres[pure_coloring]
        for left_index, right_index in combinations(range(len(pure_terms)), 2):
            left_underlying = underlying(pure_terms[left_index][1])
            right_underlying = underlying(pure_terms[right_index][1])
            for first_vertex, second_vertex in combinations(range(size), 2):
                if any(
                    tuple(sorted((first_vertex, second_vertex))) in matching
                    for matching in (left_underlying, right_underlying)
                ):
                    continue
                for first_color in range(core.Q):
                    if first_color == color:
                        continue
                    for second_color in range(core.Q):
                        if second_color == color:
                            continue
                        corners = []
                        valid = True
                        for first_bit, second_bit in ((1, 0), (0, 1), (1, 1)):
                            coloring = [color] * size
                            if first_bit:
                                coloring[first_vertex] = first_color
                            if second_bit:
                                coloring[second_vertex] = second_color
                            coloring = tuple(coloring)
                            terms = fibres.get(coloring, ())
                            if (
                                len(terms) != 2
                                or {underlying(term[1]) for term in terms}
                                != {left_underlying, right_underlying}
                            ):
                                valid = False
                                break
                            corners.append(coloring)
                        if valid:
                            answer.append((
                                color,
                                left_index,
                                right_index,
                                first_vertex,
                                second_vertex,
                                first_color,
                                second_color,
                                tuple(corners),
                            ))
    return tuple(answer)


def add_no_rectangle_clauses(
    size, solver, term_variables, matchings
):
    """Forbid every literal two-vertex recoloring rectangle."""

    clauses = 0
    matching_sets = [frozenset(matching) for matching in matchings]
    for color in range(core.Q):
        pure = (color,) * size
        for left, right in combinations(range(len(matchings)), 2):
            for first_vertex, second_vertex in combinations(range(size), 2):
                pair = tuple(sorted((first_vertex, second_vertex)))
                if pair in matching_sets[left] or pair in matching_sets[right]:
                    continue
                for first_color in range(core.Q):
                    if first_color == color:
                        continue
                    for second_color in range(core.Q):
                        if second_color == color:
                            continue
                        corners = [pure]
                        for first_bit, second_bit in ((1, 0), (0, 1), (1, 1)):
                            coloring = [color] * size
                            if first_bit:
                                coloring[first_vertex] = first_color
                            if second_bit:
                                coloring[second_vertex] = second_color
                            corners.append(tuple(coloring))
                        solver.add_clause([
                            -term_variables[coloring, matching_number]
                            for coloring in corners
                            for matching_number in (left, right)
                        ])
                        clauses += 1
    return clauses


def run(max_rounds, orbit, forbid_rectangles=False):
    size = 6
    targets = core.target_orbits(size)[orbit]
    (
        _pool,
        clauses,
        cells,
        cell_index,
        support,
        matchings,
        term_variables,
        _term_cells,
    ) = core.build_formula(size, targets)
    solver = Solver(name="cadical195", bootstrap_with=clauses)
    if forbid_rectangles:
        number = add_no_rectangle_clauses(
            size, solver, term_variables, matchings
        )
        print(f"added {number} no-rectangle clauses", flush=True)
    consistent_seen = 0
    for round_number in range(max_rounds):
        if not solver.solve():
            solver.delete()
            print(
                f"UNSAT after {round_number} rounds and "
                f"{consistent_seen} phase-consistent supports"
            )
            return None
        selected = core.decode(solver.get_model(), support)
        fibres = core.exact_fibres(size, selected, matchings)
        mixed = [
            (coloring, terms)
            for coloring, terms in sorted(fibres.items())
            if len(set(coloring)) > 1
        ]
        rows = [
            core.exponent_row(
                terms[0][1], terms[1][1], cell_index, len(cells)
            )
            for _coloring, terms in mixed
        ]
        consistent, lattice = core.signed_quotient_lattice(rows, len(cells))
        if not consistent:
            relation = core.flint_odd_relation(rows)
            used = (
                [index for index, value in enumerate(relation) if value]
                if relation is not None else range(len(rows))
            )
            literals = {
                support[cell]
                for index in used
                for _matching_number, decorated in mixed[index][1]
                for cell in decorated
            }
            solver.add_clause([-literal for literal in literals])
            continue

        consistent_seen += 1
        remainder, _classes = core.reduced_constant_product(
            size, fibres, lattice, cells, cell_index
        )
        if remainder:
            solver.delete()
            print("FOUND ACTUAL NONZERO-CONSTANT SURVIVOR")
            return selected, fibres
        rectangles = literal_rectangles(size, fibres)
        if forbid_rectangles:
            assert not rectangles
            used_rows, used_colors = core.minimize_zero_product_certificate(
                size, fibres, rows, cells, cell_index
            )
            solver.delete()
            print(
                f"FOUND NONRECTANGLE ZERO BOUNDARY: rows={len(used_rows)} "
                f"colors={used_colors}"
            )
            for cell in sorted(selected):
                print(" ", cell)
            return selected, fibres
        if consistent_seen == 1 or consistent_seen % 100 == 0:
            print(
                f"phase support {consistent_seen}: round={round_number} "
                f"cells={len(selected)} rectangles={len(rectangles)}",
                flush=True,
            )
        if not rectangles:
            used_rows, used_colors = core.minimize_zero_product_certificate(
                size, fibres, rows, cells, cell_index
            )
            solver.delete()
            print(
                f"FOUND NONRECTANGLE ZERO BOUNDARY: rows={len(used_rows)} "
                f"colors={used_colors}"
            )
            for cell in sorted(selected):
                print(" ", cell)
            return selected, fibres

        # Discovery-only exact model block.  It changes at least one cell;
        # unlike the reusable toric cuts, it makes no theorem claim.
        solver.add_clause([
            -support[cell] if cell in selected else support[cell]
            for cell in cells
        ])

    solver.delete()
    raise RuntimeError(f"reached max_rounds={max_rounds}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rounds", type=int, default=100000)
    parser.add_argument("--orbit", type=int, default=10)
    parser.add_argument("--forbid-rectangles", action="store_true")
    args = parser.parse_args()
    run(args.max_rounds, args.orbit, args.forbid_rectangles)


if __name__ == "__main__":
    main()
