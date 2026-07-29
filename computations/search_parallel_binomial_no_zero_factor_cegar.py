#!/usr/bin/env python3
"""Search n=6 binomial supports with no identically zero pure factor.

The exact acceptance test in ``search_parallel_binomial_nonzero_constants_cegar``
asks whether the product C_0 C_1 C_2 is nonzero in the twisted group algebra.
This weaker diagnostic asks whether each C_a is nonzero there separately.
It probes whether perfect-matching incidence always kills one complete pure
fibre uniformly, or whether the product can vanish only because different
factors vanish on different torsion components.

Every learned clause is sound for this weaker property: it either removes a
mixed row from an odd phase inconsistency, or changes the exact pure fibre
and mixed rows certifying C_a=0 for one color.  ``UNSAT`` is therefore an
exhaustive result for the requested target-matching orbit.
"""

from __future__ import annotations

import argparse

from pysat.solvers import Solver

import search_parallel_binomial_nonzero_constants_cegar as core


def minimize_zero_factor(
    size, color, fibres, rows, cells, cell_index
):
    """Delta-debug mixed rows while the chosen pure factor stays zero."""

    def still_zero(indices):
        selected_rows = [rows[index] for index in indices]
        consistent, lattice = core.signed_quotient_lattice(
            selected_rows, len(cells)
        )
        assert consistent
        remainder, _classes = core.reduced_constant_product(
            size, fibres, lattice, cells, cell_index, (color,)
        )
        return not remainder

    active = list(range(len(rows)))
    assert still_zero(active)
    granularity = 2
    while len(active) >= 2:
        chunk_size = (len(active) + granularity - 1) // granularity
        removed = False
        for start in range(0, len(active), chunk_size):
            discarded = set(active[start:start + chunk_size])
            trial = [index for index in active if index not in discarded]
            if still_zero(trial):
                active = trial
                granularity = max(2, granularity - 1)
                removed = True
                break
        if removed:
            continue
        if granularity >= len(active):
            break
        granularity = min(len(active), 2 * granularity)
    assert still_zero(active)
    return tuple(active)


def run(orbit, max_rounds, verbose=False):
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
    odd_cuts = 0
    factor_cuts = 0

    for round_number in range(max_rounds):
        if not solver.solve():
            solver.delete()
            print(
                f"orbit={orbit} UNSAT rounds={round_number} "
                f"odd_cuts={odd_cuts} factor_cuts={factor_cuts}"
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
        consistent, lattice = core.signed_quotient_lattice(
            rows, len(cells)
        )
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
            odd_cuts += 1
            cut = f"odd({len(used)}/{len(rows)})"
        else:
            remainders = [
                core.reduced_constant_product(
                    size, fibres, lattice, cells, cell_index, (color,)
                )[0]
                for color in range(core.Q)
            ]
            zero_colors = [
                color for color, remainder in enumerate(remainders)
                if not remainder
            ]
            if not zero_colors:
                product_remainder, _classes = core.reduced_constant_product(
                    size, fibres, lattice, cells, cell_index
                )
                solver.delete()
                print(
                    f"orbit={orbit} SURVIVOR cells={len(selected)} "
                    f"mixed={len(mixed)} pure_sizes="
                    f"{tuple(len(fibres[(a,) * size]) for a in range(core.Q))} "
                    f"product={'nonzero' if product_remainder else 'ZERO'}"
                )
                for cell in sorted(selected):
                    print(cell)
                return selected, fibres, bool(product_remainder)

            color = min(
                zero_colors,
                key=lambda value: len(fibres[(value,) * size]),
            )
            used = minimize_zero_factor(
                size, color, fibres, rows, cells, cell_index
            )
            cut_size = core.exact_support_nogood(
                solver,
                size,
                fibres,
                mixed,
                used,
                (color,),
                term_variables,
                matchings,
            )
            factor_cuts += 1
            cut = (
                f"C_{color}=0(rows={len(used)},lits={cut_size},"
                f"zeros={tuple(zero_colors)})"
            )

        if verbose or round_number % 100 == 0:
            print(
                f"orbit={orbit} round={round_number} cells={len(selected)} "
                f"mixed={len(mixed)} cut={cut}",
                flush=True,
            )

    solver.delete()
    raise RuntimeError(f"orbit {orbit} reached max_rounds={max_rounds}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int)
    parser.add_argument("--max-rounds", type=int, default=100000)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    orbits = core.target_orbits(6)
    indices = range(len(orbits)) if args.orbit is None else (args.orbit,)
    for orbit in indices:
        result = run(orbit, args.max_rounds, args.verbose)
        if result is not None:
            return
    print("all requested target orbits UNSAT")


if __name__ == "__main__":
    main()
