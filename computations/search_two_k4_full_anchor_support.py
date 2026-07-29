#!/usr/bin/env python3
"""Exact support CEGAR for the two-K4 chart with a full anchor bridge.

The two internal K4 blocks are the standard monomial Delta_4 sources.
All cells on the nine nonanchor bridges and on the anchor edge are Boolean
variables.  Every mixed coloring is required to have either zero or at
least two supported perfect-matching monomials, a necessary condition for
complex cancellation.  A surviving support is not a weighted solution;
UNSAT is an exact obstruction to the whole chart.
"""

from __future__ import annotations

import argparse
import itertools

from pysat.formula import IDPool
from pysat.solvers import Solver


N, Q = 8, 3
VARIABLE_EDGES = ((0, 4),) + tuple(
    (left, right) for left in (1, 2, 3) for right in (5, 6, 7)
)
VARIABLE_SET = set(VARIABLE_EDGES)
COLORINGS = tuple(itertools.product(range(Q), repeat=N))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))
FIXED_CELLS: set[tuple[int, int, int, int]] = set()
for offset in (0, 4):
    anchor = offset
    nonanchors = (offset + 1, offset + 2, offset + 3)
    for color in range(Q):
        partner = nonanchors[color]
        others = tuple(vertex for vertex in nonanchors if vertex != partner)
        for u, v in ((anchor, partner), tuple(sorted(others))):
            FIXED_CELLS.add((u, v, color, color))


class Formula:
    def __init__(self):
        self.pool = IDPool()
        self.clauses: list[list[int]] = []
        self.cell = {
            (u, v, a, b): self.pool.id(("cell", u, v, a, b))
            for u, v in VARIABLE_EDGES
            for a, b in itertools.product(range(Q), repeat=2)
        }
        self.encoded: set[tuple[int, ...]] = set()

    def term_literals(self, coloring, matching):
        literals = []
        for u, v in matching:
            key = (u, v, coloring[u], coloring[v])
            if key in FIXED_CELLS:
                continue
            if (u, v) not in VARIABLE_SET:
                return None
            literals.append(self.cell[key])
        return tuple(literals)

    def witness(self, coloring, matching, number):
        literals = self.term_literals(coloring, matching)
        if literals is None:
            return None
        if not literals:
            return True
        output = self.pool.id(("witness", coloring, number))
        self.clauses.extend([-output, literal] for literal in literals)
        self.clauses.append([output] + [-literal for literal in literals])
        return output

    def encode_no_singleton(self, coloring):
        if coloring in self.encoded:
            return
        self.encoded.add(coloring)
        witnesses = []
        fixed_true = False
        for number, matching in enumerate(MATCHINGS):
            witness = self.witness(coloring, matching, number)
            if witness is True:
                fixed_true = True
            elif witness is not None:
                witnesses.append(witness)
        if fixed_true:
            # The standard blocks contribute at most one fixed-only term.
            self.clauses.append(witnesses)
        else:
            for witness in witnesses:
                self.clauses.append(
                    [-witness] + [other for other in witnesses if other != witness]
                )

    def supported_count(self, coloring, positive):
        count = 0
        for matching in MATCHINGS:
            literals = self.term_literals(coloring, matching)
            if literals is not None and all(literal in positive for literal in literals):
                count += 1
        return count


def run(solver_name: str, batch: int) -> None:
    formula = Formula()
    with Solver(name=solver_name) as solver:
        installed = 0
        for iteration in range(10000):
            for clause in formula.clauses[installed:]:
                solver.add_clause(clause)
            installed = len(formula.clauses)
            if not solver.solve():
                print(
                    f"UNSAT rounds={iteration} encoded={len(formula.encoded)} "
                    f"variables={formula.pool.top} clauses={len(formula.clauses)}",
                    flush=True,
                )
                return
            positive = {literal for literal in solver.get_model() if literal > 0}
            singletons = [
                coloring
                for coloring in COLORINGS
                if len(set(coloring)) > 1
                and formula.supported_count(coloring, positive) == 1
            ]
            print(
                f"round={iteration} singleton_fibres={len(singletons)} "
                f"encoded={len(formula.encoded)} cells={sum(v in positive for v in formula.cell.values())}",
                flush=True,
            )
            if not singletons:
                print("SAT support survivor")
                for edge in VARIABLE_EDGES:
                    cells = [
                        (a, b)
                        for a, b in itertools.product(range(Q), repeat=2)
                        if formula.cell[edge + (a, b)] in positive
                    ]
                    print(edge, cells)
                return
            for coloring in singletons[:batch]:
                formula.encode_no_singleton(coloring)
    raise AssertionError("unreachable")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--batch", type=int, default=128)
    args = parser.parse_args()
    run(args.solver, args.batch)


if __name__ == "__main__":
    main()
