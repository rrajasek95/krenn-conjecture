#!/usr/bin/env python3
"""Exact CEGAR audit of K_{4,4} under all forced-anchor conditions.

It models every rank-one matrix by its exact rectangular zero/nonzero
support, permits at most one
non-rank-one incident matrix at every vertex, imposes every one-sided
coordinate anchor forced by notes/slice-cover.md, requires the three
constant fibres to be nonempty, and iteratively eliminates mixed singleton
fibres.
"""

from __future__ import annotations

from itertools import combinations, permutations, product

from pysat.solvers import Solver


Q = 3
N = 4
EDGES = tuple(product(range(N), repeat=2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
MATCHINGS = tuple(permutations(range(N)))
COLORINGS = tuple(product(range(Q), repeat=2 * N))


class Pool:
    def __init__(self):
        self.top = 0

    def new(self):
        self.top += 1
        return self.top


class Formula:
    def __init__(self):
        self.pool = Pool()
        self.clauses: list[list[int]] = []
        self.rank_one = [self.pool.new() for _edge in EDGES]
        self.left = [
            [self.pool.new() for _color in range(Q)] for _edge in EDGES
        ]
        self.right = [
            [self.pool.new() for _color in range(Q)] for _edge in EDGES
        ]
        self.cell = [
            [
                [self.pool.new() for _right_color in range(Q)]
                for _left_color in range(Q)
            ]
            for _edge in EDGES
        ]
        self.encoded_colorings: set[tuple[int, ...]] = set()
        self._build_base()

    def _equivalence_to_conjunction(self, literals):
        witness = self.pool.new()
        self.clauses.extend([-witness, literal] for literal in literals)
        self.clauses.append([witness] + [-literal for literal in literals])
        return witness

    def _build_base(self):
        for edge_number, _edge in enumerate(EDGES):
            cells = [
                self.cell[edge_number][left_color][right_color]
                for left_color in range(Q)
                for right_color in range(Q)
            ]
            self.clauses.append(cells)  # every underlying edge is nonzero
            self.clauses.append(
                [-self.rank_one[edge_number]] + self.left[edge_number]
            )
            self.clauses.append(
                [-self.rank_one[edge_number]] + self.right[edge_number]
            )
            for left_color, right_color in product(range(Q), repeat=2):
                rank = self.rank_one[edge_number]
                left = self.left[edge_number][left_color]
                right = self.right[edge_number][right_color]
                cell = self.cell[edge_number][left_color][right_color]
                # rank => (cell <=> left and right)
                self.clauses.extend(
                    (
                        [-rank, -cell, left],
                        [-rank, -cell, right],
                        [-rank, -left, -right, cell],
                    )
                )

        # The rank-at-least-two edges form a matching.
        for left_vertex in range(N):
            incident = [EDGE_INDEX[left_vertex, right] for right in range(N)]
            self.clauses.extend(
                [self.rank_one[first], self.rank_one[second]]
                for first, second in combinations(incident, 2)
            )
        for right_vertex in range(N):
            incident = [EDGE_INDEX[left, right_vertex] for left in range(N)]
            self.clauses.extend(
                [self.rank_one[first], self.rank_one[second]]
                for first, second in combinations(incident, 2)
            )

        # At a left vertex and for each target color, some rank-one edge has
        # exactly that singleton as its factor on the opposite (right) end.
        for left_vertex in range(N):
            for color in range(Q):
                witnesses = []
                for right_vertex in range(N):
                    edge = EDGE_INDEX[left_vertex, right_vertex]
                    condition = [
                        self.rank_one[edge],
                        self.right[edge][color],
                    ] + [
                        -self.right[edge][other]
                        for other in range(Q)
                        if other != color
                    ]
                    witnesses.append(self._equivalence_to_conjunction(condition))
                self.clauses.append(witnesses)

        # The symmetric condition at every right vertex.
        for right_vertex in range(N):
            for color in range(Q):
                witnesses = []
                for left_vertex in range(N):
                    edge = EDGE_INDEX[left_vertex, right_vertex]
                    condition = [
                        self.rank_one[edge],
                        self.left[edge][color],
                    ] + [
                        -self.left[edge][other]
                        for other in range(Q)
                        if other != color
                    ]
                    witnesses.append(self._equivalence_to_conjunction(condition))
                self.clauses.append(witnesses)

        for color in range(Q):
            coloring = (color,) * (2 * N)
            witnesses = self.encode_coloring(coloring, require_mate=False)
            self.clauses.append(witnesses)

    def matching_cells(self, coloring, matching):
        left_colors = coloring[:N]
        right_colors = coloring[N:]
        return [
            self.cell[EDGE_INDEX[left, right]][left_colors[left]][
                right_colors[right]
            ]
            for left, right in enumerate(matching)
        ]

    def encode_coloring(self, coloring, require_mate=True):
        if coloring in self.encoded_colorings:
            return []
        self.encoded_colorings.add(coloring)
        witnesses = [
            self._equivalence_to_conjunction(
                self.matching_cells(coloring, matching)
            )
            for matching in MATCHINGS
        ]
        if require_mate:
            self.clauses.extend(
                [-witness]
                + [other for other in witnesses if other != witness]
                for witness in witnesses
            )
        return witnesses


def singleton_colorings(formula, positive):
    answer = []
    for coloring in COLORINGS:
        if len(set(coloring)) == 1:
            continue
        supported = 0
        for matching in MATCHINGS:
            if all(
                cell in positive
                for cell in formula.matching_cells(coloring, matching)
            ):
                supported += 1
                if supported == 2:
                    break
        if supported == 1:
            answer.append(coloring)
    return answer


def print_model(formula, positive):
    for edge_number, edge in enumerate(EDGES):
        support = [
            (left_color, right_color)
            for left_color, right_color in product(range(Q), repeat=2)
            if formula.cell[edge_number][left_color][right_color] in positive
        ]
        if formula.rank_one[edge_number] in positive:
            left = [
                color
                for color in range(Q)
                if formula.left[edge_number][color] in positive
            ]
            right = [
                color
                for color in range(Q)
                if formula.right[edge_number][color] in positive
            ]
            print(edge, "rank-one", left, "x", right, support)
        else:
            print(edge, "arbitrary", support)


def run(batch_size=100):
    formula = Formula()
    solver = Solver(name="cadical195", bootstrap_with=formula.clauses)
    installed = len(formula.clauses)
    for iteration in range(10000):
        satisfiable = solver.solve()
        if not satisfiable:
            print(
                "verified UNSAT after",
                iteration,
                "CEGAR rounds;",
                f"encoded_colorings={len(formula.encoded_colorings)}",
                f"variables={formula.pool.top}",
                f"clauses={len(formula.clauses)}",
            )
            return
        positive = {literal for literal in solver.get_model() if literal > 0}
        singletons = singleton_colorings(formula, positive)
        print(
            f"round={iteration} singleton_fibres={len(singletons)} "
            f"encoded={len(formula.encoded_colorings)}"
        )
        if not singletons:
            print_model(formula, positive)
            raise AssertionError("unexpected SAT support countermodel")
        for coloring in singletons[:batch_size]:
            formula.encode_coloring(coloring)
        for clause in formula.clauses[installed:]:
            solver.add_clause(clause)
        installed = len(formula.clauses)
    raise RuntimeError("CEGAR iteration limit reached")


if __name__ == "__main__":
    run()
