#!/usr/bin/env python3
"""Exact sparse completions of the signed 16-cell n=8 near-solution.

The default mode searches for a support with no mixed singleton fibre.  It
uses the known fixed support and the cell cap to delete infeasible mate
selectors, and quotients by the sole nontrivial support automorphism.  These
are exact reductions, not heuristics.

``--full`` invokes the existing Laurent/group-algebra completion engine on
the same fixed support.  ``--structured`` instead fixes the 28-cell closure
recorded by ``verify_n8_border_seed_direct_repair.py``; this makes the exact
coefficient obstruction through the first sparse layers quick to replay.
"""

from __future__ import annotations

import argparse
from collections import Counter

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_sparse_triple_completion as sparse
from verify_n8_border_seed_direct_repair import (
    MINIMUM_REPAIR,
    SEED,
    STRUCTURED_BASE,
)


NEAR_SUPPORT = SEED | MINIMUM_REPAIR
SUPPORT_INVOLUTION = (
    (2, 4, 0, 3, 1, 7, 6, 5),
    (0, 2, 1),
)


class TightNoSingletonSearch(sparse.SparseCompletionSearch):
    """Cap-aware exact singleton completion above the 16-cell support."""

    def __init__(self, cap, solver_name):
        self.cell_cap = cap
        super().__init__(
            cap, solver_name, orbit=8, seed_cells=NEAR_SUPPORT
        )

        # Every support orbit under this involution has a lexicographically
        # least representative.  Add only support variables: the signs have
        # not yet been introduced in this support-level search.
        vertex_permutation, colour_permutation = SUPPORT_INVOLUTION
        clauses = []
        variables = [self.support[cell] for cell in self.cells]
        image_variables = [
            self.support[signed.image_cell(
                cell, vertex_permutation, colour_permutation
            )]
            for cell in self.cells
        ]
        signed.add_lex_leader(
            clauses, self.pool, variables, image_variables
        )
        for clause in clauses:
            self.solver.add_clause(clause)

    def add_singleton_gadget(self, colouring, trigger_number):
        """Encode exactly the feasible inclusion-minimal mates.

        If the trigger term remains present, a mate with requirement ``R``
        is feasible only when ``seed union trigger union R`` fits under the
        global support cap.  If ``R'`` is a strict subset of ``R``, retaining
        ``R`` is redundant because ``R'`` already supports a distinct mate.
        Both deletions therefore preserve the support projection exactly.
        """

        key = colouring, trigger_number
        if key in self.singleton_gadgets:
            return False
        trigger = frozenset(self.terms(colouring)[trigger_number])
        requirements = set()
        for number, decorated in enumerate(self.terms(colouring)):
            if number == trigger_number:
                continue
            requirement = frozenset(decorated) - trigger
            if len(self.seed | trigger | requirement) <= self.cell_cap:
                requirements.add(requirement)
        requirements = {
            requirement
            for requirement in requirements
            if not any(
                smaller < requirement for smaller in requirements
            )
        }

        selectors = []
        new_variables = []
        for requirement in sorted(
            requirements, key=lambda value: (len(value), sorted(value))
        ):
            selector = self.pool.new()
            selectors.append(selector)
            new_variables.append(selector)
            for cell in requirement:
                self.solver.add_clause([-selector, self.support[cell]])
        self.solver.add_clause(
            [-self.support[cell] for cell in sorted(trigger)] + selectors
        )
        self.solver.set_phases([-variable for variable in new_variables])
        self.singleton_gadgets.add(key)
        return True


def search_no_singleton(cap, solver_name, max_rounds):
    search = TightNoSingletonSearch(cap, solver_name)
    try:
        for round_number in range(max_rounds):
            if not search.solver.solve():
                print(
                    f"UNSAT cap={cap} rounds={round_number} "
                    f"singleton_gadgets={len(search.singleton_gadgets)}"
                )
                return None
            selected = search.decode(search.solver.get_model())
            fibres = sparse.exact_fibres(search, selected)
            singletons = [
                (colouring, terms[0][0])
                for colouring, terms in fibres.items()
                if len(set(colouring)) > 1 and len(terms) == 1
            ]
            if not singletons:
                histogram = Counter(
                    len(terms)
                    for colouring, terms in fibres.items()
                    if len(set(colouring)) > 1
                )
                print(
                    f"NO_SINGLETON cap={cap} round={round_number} "
                    f"cells={len(selected)} histogram={dict(histogram)}"
                )
                print("EXTRA", sorted(selected - NEAR_SUPPORT))
                return selected
            for colouring, trigger_number in singletons:
                assert search.add_singleton_gadget(
                    colouring, trigger_number
                )
            if round_number < 20 or round_number % 20 == 0:
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"singletons={len(singletons)} "
                    f"gadgets={len(search.singleton_gadgets)}",
                    flush=True,
                )
        print(
            f"BOUNDARY cap={cap} rounds={max_rounds} "
            f"singleton_gadgets={len(search.singleton_gadgets)}"
        )
        return None
    finally:
        search.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=25)
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--structured", action="store_true")
    args = parser.parse_args()

    if args.full:
        seed = STRUCTURED_BASE if args.structured else NEAR_SUPPORT
        sparse.run(
            args.cap,
            args.solver,
            args.max_rounds,
            512,
            False,
            1,
            orbit=8,
            seed_cells=seed,
        )
    elif args.structured:
        parser.error("--structured is meaningful only together with --full")
    else:
        search_no_singleton(args.cap, args.solver, args.max_rounds)


if __name__ == "__main__":
    main()
