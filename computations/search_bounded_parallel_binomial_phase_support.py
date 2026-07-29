#!/usr/bin/env python3
"""Bounded-cell CEGAR for minimum phase-consistent n=6 supports."""

from __future__ import annotations

import argparse

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import search_parallel_binomial_nonzero_constants_cegar as core
from search_parallel_binomial_nonrectangle_boundary import literal_rectangles


def run(bound, max_rounds):
    size = 6
    orbit = 10
    targets = core.target_orbits(size)[orbit]
    (
        pool,
        clauses,
        cells,
        cell_index,
        support,
        matchings,
        _term_variables,
        _term_cells,
    ) = core.build_formula(size, targets)
    cardinality = CardEnc.atmost(
        lits=[support[cell] for cell in cells],
        bound=bound,
        top_id=pool.top,
        encoding=EncType.seqcounter,
    )
    clauses.extend(cardinality.clauses)
    solver = Solver(name="cadical195", bootstrap_with=clauses)
    for round_number in range(max_rounds):
        if not solver.solve():
            solver.delete()
            print(f"bound={bound} UNSAT after {round_number} lattice cuts")
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
        if consistent:
            remainder, _classes = core.reduced_constant_product(
                size, fibres, lattice, cells, cell_index
            )
            rectangles = literal_rectangles(size, fibres)
            solver.delete()
            print(
                f"bound={bound} PHASE SAT cells={len(selected)} "
                f"product={'nonzero' if remainder else 'zero'} "
                f"rectangles={len(rectangles)} round={round_number}"
            )
            for cell in sorted(selected):
                print(" ", cell)
            return selected, fibres
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
        if round_number % 1000 == 0:
            print(
                f"bound={bound} round={round_number} cells={len(selected)} "
                f"odd_rows={len(used)}/{len(rows)}",
                flush=True,
            )
    solver.delete()
    raise RuntimeError(f"reached max_rounds={max_rounds}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, required=True)
    parser.add_argument("--max-rounds", type=int, default=100000)
    args = parser.parse_args()
    run(args.bound, args.max_rounds)


if __name__ == "__main__":
    main()
