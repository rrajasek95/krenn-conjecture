#!/usr/bin/env python3
"""Hit every odd Laurent triangle of the 28-cell orbit-40 boundary.

This is a discovery subproblem for multi-term repairs.  The original support
has 48 exact three-binomial contradictions.  Extra aggregate cells may turn
at least one fibre in each triangle into a three-or-more-term equation.  The
SAT model chooses such cells and minimizes only their number; a returned set
is subsequently audited against the full matching enumeration.
"""

from __future__ import annotations

import argparse

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as toric_search
import search_parallel_binomial_nonzero_constants_cegar as toric
from verify_n8_toric_orbit40_boundary import boundary_support


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=12)
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()

    search = signed.LazySearch(40, "cadical195", unique_constants=False)
    try:
        base = set(boundary_support())
        fibres = toric.exact_fibres(8, base, search.matchings)
        mixed, rows = toric_search.exponent_rows(search, fibres)
        circuits = toric_search.unit_triangle_circuits(rows)
        assert len(circuits) == 48

        optional = tuple(cell for cell in search.cells if cell not in base)
        support_variable = {
            cell: index + 1 for index, cell in enumerate(optional)
        }
        top = len(optional)
        clauses = []
        term_variable = {}

        for circuit in circuits:
            alternatives = set()
            for row_index in circuit:
                colouring, terms = mixed[row_index]
                old = {matching_number for matching_number, _term in terms}
                for matching_number, matching in enumerate(search.matchings):
                    if matching_number in old:
                        continue
                    decorated = frozenset(
                        (u, v, colouring[u], colouring[v])
                        for u, v in matching
                    )
                    missing = tuple(sorted(decorated - base))
                    assert missing
                    key = colouring, matching_number
                    variable = term_variable.get(key)
                    if variable is None:
                        top += 1
                        variable = term_variable[key] = top
                        for cell in missing:
                            clauses.append(
                                [-variable, support_variable[cell]]
                            )
                        clauses.append(
                            [variable]
                            + [-support_variable[cell] for cell in missing]
                        )
                    alternatives.add(variable)
            clauses.append(sorted(alternatives))

        encoding = CardEnc.atmost(
            lits=list(support_variable.values()),
            bound=args.cap,
            top_id=top,
            encoding=EncType.kmtotalizer,
        )
        clauses.extend(encoding.clauses)
        print(
            f"built variables={encoding.nv} clauses={len(clauses)} "
            f"circuits={len(circuits)} alternative_terms={len(term_variable)}",
            flush=True,
        )
        with Solver(name=args.solver, bootstrap_with=clauses) as solver:
            satisfiable = solver.solve()
            print(f"SAT={satisfiable} cap={args.cap}", flush=True)
            if not satisfiable:
                return
            positive = {literal for literal in solver.get_model() if literal > 0}
        added = frozenset(
            cell
            for cell, variable in support_variable.items()
            if variable in positive
        )
        assert len(added) <= args.cap
        repaired = base | added
        repaired_fibres = toric.exact_fibres(
            8, repaired, search.matchings
        )
        remaining_binomial = [
            (colouring, terms)
            for colouring, terms in sorted(repaired_fibres.items())
            if len(set(colouring)) > 1 and len(terms) == 2
        ]
        remaining_rows = [
            toric.exponent_row(
                terms[0][1],
                terms[1][1],
                search.cell_index,
                len(search.cells),
            )
            for _colouring, terms in remaining_binomial
        ]
        consistent = toric.signed_quotient_lattice(
            remaining_rows, len(search.cells)
        )[0]
        singletons = sum(
            len(terms) == 1
            for colouring, terms in repaired_fibres.items()
            if len(set(colouring)) > 1
        )
        print(
            f"added={len(added)} mixed_singletons={singletons} "
            f"remaining_binomials={len(remaining_rows)} "
            f"binomial_lattice_consistent={consistent}",
            flush=True,
        )
        for cell in sorted(added):
            print(" ", cell, flush=True)
    finally:
        search.delete()


if __name__ == "__main__":
    main()
