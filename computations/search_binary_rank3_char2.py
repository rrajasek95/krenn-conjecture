#!/usr/bin/env python3
"""Exact SAT search for the canonical binary rank-three target over F_2.

For even ``n`` the target

    e0^n + e1^n + (e0+e1)^n

reduces to one on every nonconstant binary word and to zero on the two
constant words.  All 2x2 edge matrices are unrestricted.  This is a
fixed-order discovery tool, not a characteristic-zero certificate.
"""

from __future__ import annotations

import argparse
import itertools
import time

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def add_iff_and(cnf: CNF, output: int, literals: list[int]) -> None:
    for literal in literals:
        cnf.append([-output, literal])
    cnf.append([output] + [-literal for literal in literals])


def add_xor(
    cnf: CNF,
    pool: IDPool,
    literals: list[int],
    target: bool,
    tag: int,
) -> None:
    parity = literals[0]
    for index, literal in enumerate(literals[1:], 1):
        new = pool.id(("xor", tag, index))
        cnf.extend(
            (
                [parity, literal, -new],
                [-parity, -literal, -new],
                [parity, -literal, new],
                [-parity, literal, new],
            )
        )
        parity = new
    cnf.append([parity if target else -parity])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8, choices=(4, 6, 8))
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--canonical", action="store_true")
    args = parser.parse_args()

    n = args.n
    vertices = tuple(range(n))
    matchings = tuple(perfect_matchings(vertices))
    pool = IDPool()
    cnf = CNF()

    def entry(u: int, v: int, a: int, b: int) -> int:
        if u < v:
            return pool.id(("entry", u, v, a, b))
        return pool.id(("entry", v, u, b, a))

    # The word 10...0 has coefficient one.  If requested, select one of its
    # supported matchings and send it to the standard matching by a target
    # preserving vertex permutation fixing vertex zero.
    if args.canonical:
        coloring = (1,) + (0,) * (n - 1)
        for u, v in tuple((2 * k, 2 * k + 1) for k in range(n // 2)):
            cnf.append([entry(u, v, coloring[u], coloring[v])])

    for coloring_index, coloring in enumerate(
        itertools.product((0, 1), repeat=n)
    ):
        terms = []
        for matching_index, matching in enumerate(matchings):
            term = pool.id(("term", coloring_index, matching_index))
            add_iff_and(
                cnf,
                term,
                [entry(u, v, coloring[u], coloring[v]) for u, v in matching],
            )
            terms.append(term)
        target = coloring not in ((0,) * n, (1,) * n)
        add_xor(cnf, pool, terms, target, coloring_index)

    print(
        f"n={n} variables={pool.top} clauses={len(cnf.clauses)} "
        f"matchings={len(matchings)}",
        flush=True,
    )
    started = time.time()
    with Solver(name=args.solver, bootstrap_with=cnf) as solver:
        sat = solver.solve()
        print(f"sat={sat} seconds={time.time() - started:.2f}", flush=True)
        if not sat:
            return
        model = {literal for literal in solver.get_model() if literal > 0}
        matrices = {}
        for u, v in itertools.combinations(vertices, 2):
            matrix = tuple(
                tuple(int(entry(u, v, a, b) in model) for b in range(2))
                for a in range(2)
            )
            if any(any(row) for row in matrix):
                matrices[u, v] = matrix
        print("matrices =", matrices)


if __name__ == "__main__":
    main()
