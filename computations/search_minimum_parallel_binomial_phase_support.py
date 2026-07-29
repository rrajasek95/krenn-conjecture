#!/usr/bin/env python3
"""Minimum-cell phase-consistent parallel-binomial supports at n=6.

The hard support conditions and exact toric sign audit are imported from
``search_parallel_binomial_nonzero_constants_cegar.py``.  RC2 minimizes the
number of nonzero aggregate cells.  Every learned odd-lattice clause is a
sound hard clause, so the first phase-consistent survivor has globally
minimum cell count in its selected constant-matching orbit.
"""

from __future__ import annotations

import argparse
from collections import Counter

from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

import search_parallel_binomial_nonzero_constants_cegar as core


def run(orbit, max_rounds):
    size = 6
    targets = core.target_orbits(size)[orbit]
    (
        _pool,
        clauses,
        cells,
        cell_index,
        support,
        matchings,
        _term_variables,
        _term_cells,
    ) = core.build_formula(size, targets)
    formula = WCNF()
    for clause in clauses:
        formula.append(clause)
    for cell in cells:
        formula.append([-support[cell]], weight=1)

    optimizer = RC2(
        formula,
        solver="cadical195",
        adapt=False,
        verbose=0,
    )
    for round_number in range(max_rounds):
        model = optimizer.compute()
        if model is None:
            optimizer.delete()
            print(f"orbit={orbit} UNSAT after {round_number} cuts")
            return None
        selected = core.decode(model, support)
        assert optimizer.cost == len(selected)
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
            remainder, classes = core.reduced_constant_product(
                size, fibres, lattice, cells, cell_index
            )
            optimizer.delete()
            print(
                f"orbit={orbit} MINIMUM phase-consistent cells={len(selected)} "
                f"round={round_number} fibres="
                f"{dict(sorted(Counter(map(len, fibres.values())).items()))} "
                f"constant_product={'NONZERO' if remainder else 'zero'} "
                f"classes={len(classes)}"
            )
            print("targets=", targets)
            for cell in sorted(selected):
                print(" ", cell)
            return selected, fibres, remainder

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
        optimizer.add_clause([-literal for literal in literals])
        if round_number % 25 == 0:
            print(
                f"orbit={orbit} round={round_number} lower_bound={len(selected)} "
                f"odd_rows={len(used)}/{len(rows)}",
                flush=True,
            )

    optimizer.delete()
    raise RuntimeError(f"reached max_rounds={max_rounds}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, default=10)
    parser.add_argument("--max-rounds", type=int, default=10000)
    args = parser.parse_args()
    run(args.orbit, args.max_rounds)


if __name__ == "__main__":
    main()
