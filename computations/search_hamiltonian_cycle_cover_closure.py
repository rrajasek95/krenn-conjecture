#!/usr/bin/env python3
"""Exact bounded support closure above the 8-site Hamiltonian cover module.

The fixed 20-cell seed is the module from
``verify_hamiltonian_cubic_cycle_cover_countermodels.py``.  Optional cells
are arbitrary endpoint-coordinate cells.  By default all new monochromatic
cells are forbidden, so the three pure fibres remain literal singletons.

The lazy clauses are exact: whenever a supported mixed term is the sole term
in its fibre, at least one distinct matching with that word must be enabled.
Terms incompatible with the pure-safe restriction or the global cap are
deleted, and strict-superset mate requirements are redundant.  Exact
conjunction indicators for the remaining requirements are shared across
all learned clauses.  UNSAT therefore proves a bounded no-singleton
obstruction; a survivor is re-enumerated exactly.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations

import search_n8_sparse_triple_completion as sparse


N = 8


def cell(u: int, v: int, a: int, b: int) -> tuple[int, int, int, int]:
    return (u, v, a, b) if u < v else (v, u, b, a)


P0 = ((0, 1), (2, 3), (4, 5), (6, 7))
P1 = ((1, 2), (3, 4), (5, 6), (0, 7))
P2 = ((0, 2), (1, 4), (3, 6), (5, 7))
S = ((0, 3), (1, 5), (2, 6), (4, 7))
T = ((0, 4), (1, 6), (2, 5), (3, 7))
S_WORD = (1, 2, 0, 0, 2, 1, 1, 1)
T_WORD = (1, 1, 1, 2, 0, 0, 2, 1)

SEED = frozenset(
    cell(u, v, colour, colour)
    for colour, one_factor in enumerate((P0, P1, P2))
    for u, v in one_factor
) | frozenset(
    cell(u, v, word[u], word[v])
    for one_factor, word in ((S, S_WORD), (T, T_WORD))
    for u, v in one_factor
)

NEW_MONOCHROMATIC = frozenset(
    (u, v, colour, colour)
    for u, v in combinations(range(N), 2)
    for colour in range(3)
) - SEED


class TightCoverClosure(sparse.SparseCompletionSearch):
    """Cap-aware exact singleton closure for the fixed cover seed."""

    def __init__(self, cap: int, solver_name: str, pure_safe: bool):
        self.cell_cap = cap
        self.requirement_variables = {}
        super().__init__(
            cap,
            solver_name,
            seed_cells=SEED,
            forbidden_cells=NEW_MONOCHROMATIC if pure_safe else (),
        )

    def add_singleton_gadget(self, colouring, trigger_number):
        key = colouring, trigger_number
        if key in self.singleton_gadgets:
            return False
        trigger = frozenset(self.terms(colouring)[trigger_number])
        requirements = set()
        for number, decorated in enumerate(self.terms(colouring)):
            if number == trigger_number:
                continue
            requirement = frozenset(decorated) - trigger
            if requirement & self.forbidden:
                continue
            if len(self.seed | trigger | requirement) > self.cell_cap:
                continue
            requirements.add(requirement)
        requirements = {
            requirement
            for requirement in requirements
            if not any(smaller < requirement for smaller in requirements)
        }

        selectors = []
        new_variables = []
        for requirement in sorted(
            requirements, key=lambda value: (len(value), sorted(value))
        ):
            selector = self.requirement_variables.get(requirement)
            if selector is None:
                selector = self.pool.new()
                self.requirement_variables[requirement] = selector
                new_variables.append(selector)
                for required_cell in requirement:
                    self.solver.add_clause([-selector, self.support[required_cell]])
                self.solver.add_clause(
                    [selector]
                    + [-self.support[required_cell] for required_cell in requirement]
                )
            selectors.append(selector)
        self.solver.add_clause(
            [-self.support[required_cell] for required_cell in sorted(trigger)]
            + selectors
        )
        self.solver.set_phases([-variable for variable in new_variables])
        self.singleton_gadgets.add(key)
        return True


def search(cap: int, solver_name: str, max_rounds: int, pure_safe: bool):
    closure = TightCoverClosure(cap, solver_name, pure_safe)
    try:
        seed_fibres = sparse.exact_fibres(closure, SEED)
        seed_histogram = Counter(
            len(terms)
            for word, terms in seed_fibres.items()
            if len(set(word)) > 1
        )
        print(
            f"seed_cells={len(SEED)} mixed_histogram={dict(seed_histogram)} "
            f"cap={cap} pure_safe={pure_safe}",
            flush=True,
        )
        for round_number in range(max_rounds):
            if not closure.solver.solve():
                print(
                    f"UNSAT cap={cap} rounds={round_number} "
                    f"singleton_gadgets={len(closure.singleton_gadgets)}",
                    flush=True,
                )
                return None
            selected = closure.decode(closure.solver.get_model())
            fibres = sparse.exact_fibres(closure, selected)
            singletons = [
                (word, terms[0][0])
                for word, terms in sorted(fibres.items())
                if len(set(word)) > 1 and len(terms) == 1
            ]
            if not singletons:
                histogram = Counter(
                    len(terms)
                    for word, terms in fibres.items()
                    if len(set(word)) > 1
                )
                pure_sizes = tuple(
                    len(fibres[(colour,) * N]) for colour in range(3)
                )
                print(
                    f"NO_SINGLETON cap={cap} round={round_number} "
                    f"cells={len(selected)} pure_sizes={pure_sizes} "
                    f"histogram={dict(sorted(histogram.items()))}",
                    flush=True,
                )
                print("EXTRA", sorted(selected - SEED), flush=True)
                return selected
            added = sum(
                closure.add_singleton_gadget(word, trigger)
                for word, trigger in singletons
            )
            assert added
            if round_number < 20 or round_number % 20 == 0:
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"singletons={len(singletons)} add={added} "
                    f"gadgets={len(closure.singleton_gadgets)}",
                    flush=True,
                )
        print(
            f"BOUNDARY cap={cap} rounds={max_rounds} "
            f"singleton_gadgets={len(closure.singleton_gadgets)}",
            flush=True,
        )
        return None
    finally:
        closure.delete()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=36)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument(
        "--allow-new-monochromatic",
        action="store_true",
        help="allow added diagonal cells, so pure fibres need not stay singleton",
    )
    args = parser.parse_args()
    search(
        args.cap,
        args.solver,
        args.max_rounds,
        not args.allow_new_monochromatic,
    )


if __name__ == "__main__":
    main()
