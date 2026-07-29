#!/usr/bin/env python3
"""Minimize exact no-singleton closures of the six/eight-site modules.

The seed modules are the two countermodels in
``verify_hamiltonian_cubic_cycle_cover_countermodels.py``.  Every one of the
``9*binom(n,2)`` endpoint-coordinate cells is available.  A unit soft clause
penalizes each cell outside the seed, while seed cells are hard.  Whenever an
optimal support has a mixed singleton term M, a hard lazy clause says that
either M must disappear or the cells required by some distinct matching in
the same word must all be present.  Requirement conjunctions are encoded
exactly and shared.

Consequently, when the loop returns a support, RC2 has proved that it is a
minimum-cardinality extension of the seed in which every nonempty mixed
fibre has at least two terms.  The returned support is independently
re-enumerated before it is printed.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product

from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

import search_parallel_binomial_nonzero_constants_cegar as toric


Q = 3


def cell(u: int, v: int, a: int, b: int) -> tuple[int, int, int, int]:
    return (u, v, a, b) if u < v else (v, u, b, a)


def module(order: int):
    if order == 6:
        pure = (
            ((0, 1), (2, 3), (4, 5)),
            ((1, 2), (3, 4), (0, 5)),
            ((0, 2), (1, 4), (3, 5)),
        )
        extras = (
            (((0, 3), (1, 5), (2, 4)), (0, 0, 0, 1, 2, 2)),
            (((0, 4), (1, 3), (2, 5)), (0, 2, 1, 0, 1, 0)),
        )
    elif order == 8:
        pure = (
            ((0, 1), (2, 3), (4, 5), (6, 7)),
            ((1, 2), (3, 4), (5, 6), (0, 7)),
            ((0, 2), (1, 4), (3, 6), (5, 7)),
        )
        extras = (
            (((0, 3), (1, 5), (2, 6), (4, 7)), (1, 2, 0, 0, 2, 1, 1, 1)),
            (((0, 4), (1, 6), (2, 5), (3, 7)), (1, 1, 1, 2, 0, 0, 2, 1)),
        )
    else:
        raise ValueError("the implemented modules have order 6 or 8")

    seed = frozenset(
        cell(u, v, colour, colour)
        for colour, matching in enumerate(pure)
        for u, v in matching
    ) | frozenset(
        cell(u, v, word[u], word[v])
        for matching, word in extras
        for u, v in matching
    )
    return seed


def unit_triangle_circuits(rows):
    """Return every three-row signed dependency with unit coefficients."""

    if len(rows) < 3:
        return ()
    rows = tuple(map(tuple, rows))
    locations = {}
    for index, row in enumerate(rows):
        locations.setdefault(row, []).append(index)
    circuits = set()
    for left in range(len(rows)):
        for right in range(left + 1, len(rows)):
            for left_sign in (-1, 1):
                for right_sign in (-1, 1):
                    target = tuple(
                        -(left_sign * a + right_sign * b)
                        for a, b in zip(rows[left], rows[right])
                    )
                    for third in locations.get(target, ()):
                        if third not in (left, right):
                            circuits.add(tuple(sorted((left, right, third))))
    answer = tuple(sorted(circuits))
    assert all(
        not toric.signed_quotient_lattice(
            [rows[index] for index in circuit], len(rows[0])
        )[0]
        for circuit in answer
    )
    return answer


class MinimumClosure:
    def __init__(self, order: int, solver_name: str):
        self.order = order
        self.cells = tuple(
            (u, v, a, b)
            for u, v in combinations(range(order), 2)
            for a, b in product(range(Q), repeat=2)
        )
        self.support = {
            support_cell: number + 1
            for number, support_cell in enumerate(self.cells)
        }
        self.next_external_variable = len(self.cells)
        self.seed = module(order)
        self.matchings = tuple(toric.perfect_matchings(tuple(range(order))))
        self._terms = {}
        self.requirement_variables = {}
        self.singleton_gadgets = set()
        self.phase_gadgets = set()

        formula = WCNF()
        for support_cell in sorted(self.seed):
            formula.append([self.support[support_cell]])
        for support_cell in self.cells:
            if support_cell not in self.seed:
                formula.append([-self.support[support_cell]], weight=1)
        self.optimizer = RC2(
            formula,
            solver=solver_name,
            adapt=True,
            exhaust=True,
            minz=True,
            trim=2,
        )

    def delete(self):
        self.optimizer.delete()

    def new_variable(self):
        self.next_external_variable += 1
        return self.next_external_variable

    def terms(self, colouring):
        answer = self._terms.get(colouring)
        if answer is None:
            answer = tuple(
                tuple(
                    (u, v, colouring[u], colouring[v])
                    for u, v in matching
                )
                for matching in self.matchings
            )
            self._terms[colouring] = answer
        return answer

    def decode(self, model):
        positive = {literal for literal in model if literal > 0}
        return frozenset(
            support_cell
            for support_cell in self.cells
            if self.support[support_cell] in positive
        )

    def exact_fibres(self, selected):
        return toric.exact_fibres(self.order, selected, self.matchings)

    def selector(self, requirement):
        selector = self.requirement_variables.get(requirement)
        if selector is not None:
            return selector
        selector = self.new_variable()
        self.requirement_variables[requirement] = selector
        for required_cell in requirement:
            self.optimizer.add_clause(
                [-selector, self.support[required_cell]]
            )
        self.optimizer.add_clause(
            [selector]
            + [
                -self.support[required_cell]
                for required_cell in sorted(requirement)
            ]
        )
        return selector

    def add_singleton_gadget(self, colouring, trigger_number):
        key = colouring, trigger_number
        if key in self.singleton_gadgets:
            return False

        trigger = frozenset(self.terms(colouring)[trigger_number])
        requirements = {
            frozenset(decorated) - trigger
            for number, decorated in enumerate(self.terms(colouring))
            if number != trigger_number
        }
        requirements = {
            requirement
            for requirement in requirements
            if not any(smaller < requirement for smaller in requirements)
        }
        assert requirements and frozenset() not in requirements
        self.optimizer.add_clause(
            [-self.support[trigger_cell] for trigger_cell in sorted(trigger)]
            + [
                self.selector(requirement)
                for requirement in sorted(
                    requirements, key=lambda value: (len(value), sorted(value))
                )
            ]
        )
        self.singleton_gadgets.add(key)
        return True

    def add_phase_gadget(self, mixed, row_indices):
        """Force at least one exact binomial in an odd core to change."""

        descriptions = []
        guard = set()
        for index in row_indices:
            colouring, present = mixed[index]
            assert len(present) == 2
            present_numbers = tuple(number for number, _term in present)
            pair_cells = frozenset(present[0][1]) | frozenset(present[1][1])
            guard.update(pair_cells)
            descriptions.append((colouring, present_numbers, pair_cells))
        key = tuple(
            sorted((colouring, present_numbers) for colouring, present_numbers, _ in descriptions)
        )
        if key in self.phase_gadgets:
            return False

        requirements = set()
        for colouring, present_numbers, pair_cells in descriptions:
            requirements.update(
                frozenset(decorated) - pair_cells
                for number, decorated in enumerate(self.terms(colouring))
                if number not in present_numbers
            )
        requirements = {
            requirement
            for requirement in requirements
            if not any(smaller < requirement for smaller in requirements)
        }
        assert requirements and frozenset() not in requirements
        self.optimizer.add_clause(
            [-self.support[guard_cell] for guard_cell in sorted(guard)]
            + [
                self.selector(requirement)
                for requirement in sorted(
                    requirements, key=lambda value: (len(value), sorted(value))
                )
            ]
        )
        self.phase_gadgets.add(key)
        return True


def search(
    order: int,
    solver_name: str,
    max_rounds: int,
    require_phase_consistency: bool,
):
    closure = MinimumClosure(order, solver_name)
    try:
        seed_fibres = closure.exact_fibres(closure.seed)
        seed_histogram = Counter(
            len(terms)
            for word, terms in seed_fibres.items()
            if len(set(word)) > 1
        )
        print(
            f"order={order} seed_cells={len(closure.seed)} "
            f"mixed_histogram={dict(seed_histogram)}",
            flush=True,
        )
        previous_cost = -1
        for round_number in range(max_rounds):
            model = closure.optimizer.compute()
            if model is None:
                print(
                    f"UNSAT rounds={round_number} "
                    f"singleton_gadgets={len(closure.singleton_gadgets)}",
                    flush=True,
                )
                return None
            selected = closure.decode(model)
            additions = len(selected - closure.seed)
            assert additions == closure.optimizer.cost
            fibres = closure.exact_fibres(selected)
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
                    len(fibres[(colour,) * order]) for colour in range(Q)
                )
                cells = closure.cells
                cell_index = {
                    support_cell: index
                    for index, support_cell in enumerate(cells)
                }
                mixed = [
                    (word, terms)
                    for word, terms in sorted(fibres.items())
                    if len(set(word)) > 1 and len(terms) == 2
                ]
                rows = [
                    toric.exponent_row(
                        terms[0][1], terms[1][1], cell_index, len(cells)
                    )
                    for _word, terms in mixed
                ]
                consistent, lattice = toric.signed_quotient_lattice(
                    rows, len(cells)
                )
                if require_phase_consistency and not consistent:
                    triangles = unit_triangle_circuits(rows)
                    added_phase = sum(
                        closure.add_phase_gadget(mixed, row_indices)
                        for row_indices in triangles
                    )
                    core_size = 3
                    if not added_phase:
                        relation = toric.flint_odd_relation(rows)
                        row_indices = tuple(
                            index
                            for index, coefficient in enumerate(relation or ())
                            if coefficient
                        )
                        if not row_indices:
                            row_indices = tuple(range(len(rows)))
                        assert closure.add_phase_gadget(mixed, row_indices)
                        added_phase = 1
                        core_size = len(row_indices)
                    print(
                        f"round={round_number} additions={additions} "
                        f"no_singletons histogram={dict(sorted(histogram.items()))} "
                        f"phase_inconsistent triangles={len(triangles)} "
                        f"add_phase={added_phase} fallback_core={core_size} "
                        f"phase_gadgets={len(closure.phase_gadgets)}",
                        flush=True,
                    )
                    previous_cost = additions
                    continue

                pure_product = None
                if consistent:
                    pure_product, _classes = toric.reduced_constant_product(
                        order, fibres, lattice, cells, cell_index
                    )
                print(
                    f"MINIMUM_NO_SINGLETON order={order} round={round_number} "
                    f"additions={additions} cells={len(selected)} "
                    f"pure_sizes={pure_sizes} "
                    f"histogram={dict(sorted(histogram.items()))} "
                    f"binomials={len(rows)} phase_consistent={consistent} "
                    f"pure_product_classes="
                    f"{None if pure_product is None else len(pure_product)} "
                    f"singleton_gadgets={len(closure.singleton_gadgets)} "
                    f"requirement_selectors={len(closure.requirement_variables)} "
                    f"phase_gadgets={len(closure.phase_gadgets)}",
                    flush=True,
                )
                print("EXTRA", sorted(selected - closure.seed), flush=True)
                return selected

            added = sum(
                closure.add_singleton_gadget(word, trigger)
                for word, trigger in singletons
            )
            assert added
            if (
                round_number < 20
                or round_number % 20 == 0
                or additions != previous_cost
            ):
                print(
                    f"round={round_number} additions={additions} "
                    f"singletons={len(singletons)} add={added} "
                    f"gadgets={len(closure.singleton_gadgets)}",
                    flush=True,
                )
            previous_cost = additions
        print(
            f"BOUNDARY order={order} rounds={max_rounds} "
            f"cost={closure.optimizer.cost} "
            f"singleton_gadgets={len(closure.singleton_gadgets)} "
            f"phase_gadgets={len(closure.phase_gadgets)}",
            flush=True,
        )
        return None
    finally:
        closure.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, choices=(6, 8), default=6)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument("--require-phase-consistency", action="store_true")
    args = parser.parse_args()
    search(
        args.order,
        args.solver,
        args.max_rounds,
        args.require_phase_consistency,
    )


if __name__ == "__main__":
    main()
