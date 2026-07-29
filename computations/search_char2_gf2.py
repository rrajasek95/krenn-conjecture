#!/usr/bin/env python3
"""Exact SAT search for the six-site transverse Pfaffian identity over GF(2).

The variables are the 15 inter-site 3-by-3 blocks of an 18-by-18
alternating matrix.  In characteristic two the coefficient at a coloring is
the XOR of the 15 perfect-matching monomials.  Thus SAT is exactly a
representable-even-delta-matroid counterexample search, with no support or
sparsity ansatz.

``--fix-triple-orbit k`` exhaustively breaks vertex symmetry by fixing one
supported perfect matching in each monochromatic coefficient.  There are 16
orbits of the ordered pair (color-1 matching, color-2 matching) under the
stabilizer of the canonical color-0 matching.
"""

from __future__ import annotations

import argparse
import itertools
import time

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


N = 6
Q = 3


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def and_gate(cnf, pool, literals, tag):
    out = pool.id(("and", tag))
    for literal in literals:
        cnf.append([-out, literal])
    cnf.append([out] + [-literal for literal in literals])
    return out


def xor_gate(cnf, pool, literals, tag):
    assert literals
    if len(literals) == 1:
        return literals[0]
    value = literals[0]
    for index, literal in enumerate(literals[1:]):
        out = pool.id(("xor", tag, index))
        cnf.extend(
            (
                [value, literal, -out],
                [-value, -literal, -out],
                [value, -literal, out],
                [-value, literal, out],
            )
        )
        value = out
    return value


def matching_orbit_representatives(matchings, canonical):
    def act(matching, permutation):
        return tuple(
            sorted(
                tuple(sorted((permutation[u], permutation[v])))
                for u, v in matching
            )
        )

    stabilizer = tuple(
        permutation
        for permutation in itertools.permutations(range(N))
        if act(canonical, permutation) == canonical
    )
    remaining = {(first, second) for first in matchings for second in matchings}
    representatives = []
    while remaining:
        representative = min(remaining)
        orbit = {
            (act(representative[0], permutation), act(representative[1], permutation))
            for permutation in stabilizer
        }
        representatives.append(representative)
        remaining.difference_update(orbit)
    return tuple(representatives)


def pfaffian_f2(matrix):
    if not matrix:
        return 1
    answer = 0
    for j in range(1, len(matrix)):
        keep = [index for index in range(len(matrix)) if index not in (0, j)]
        minor = [[matrix[row][column] for column in keep] for row in keep]
        answer ^= matrix[0][j] & pfaffian_f2(minor)
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix-triple-orbit", type=int)
    parser.add_argument(
        "--fix-reference-matching",
        action="store_true",
        help="fix the entire color-0 alternating matrix to the canonical matching",
    )
    parser.add_argument(
        "--reference-mask",
        type=lambda value: int(value, 0),
        help="fix all 15 color-0 entries to this lexicographic edge bit mask",
    )
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()

    pool = IDPool()
    cnf = CNF()
    matchings = tuple(perfect_matchings())

    def entry(u, v, a, b):
        if u > v:
            u, v, a, b = v, u, b, a
        return pool.id(("entry", u, v, a, b))

    canonical = ((0, 1), (2, 3), (4, 5))
    if args.reference_mask is not None:
        if not 0 <= args.reference_mask < (1 << 15):
            parser.error("reference mask must have at most 15 bits")
        for edge_index, (u, v) in enumerate(itertools.combinations(range(N), 2)):
            literal = entry(u, v, 0, 0)
            cnf.append([literal if args.reference_mask >> edge_index & 1 else -literal])
    else:
        for u, v in canonical:
            cnf.append([entry(u, v, 0, 0)])
    if args.fix_reference_matching:
        if args.reference_mask is not None:
            parser.error("choose either --reference-mask or --fix-reference-matching")
        canonical_edges = set(canonical)
        for u, v in itertools.combinations(range(N), 2):
            if (u, v) not in canonical_edges:
                cnf.append([-entry(u, v, 0, 0)])

    representatives = matching_orbit_representatives(matchings, canonical)
    if args.fix_triple_orbit is not None:
        if not 0 <= args.fix_triple_orbit < len(representatives):
            parser.error(f"triple orbit must lie in [0,{len(representatives)-1}]")
        first, second = representatives[args.fix_triple_orbit]
        for color, matching in ((1, first), (2, second)):
            for u, v in matching:
                cnf.append([entry(u, v, color, color)])
        print(
            f"triple_orbit={args.fix_triple_orbit}/{len(representatives)} "
            f"M1={first} M2={second}",
            flush=True,
        )
    else:
        print(f"triple_orbits={len(representatives)}", flush=True)

    for coloring_index, coloring in enumerate(itertools.product(range(Q), repeat=N)):
        terms = []
        for matching_index, matching in enumerate(matchings):
            cells = tuple(entry(u, v, coloring[u], coloring[v]) for u, v in matching)
            terms.append(and_gate(cnf, pool, cells, (coloring_index, matching_index)))
        parity = xor_gate(cnf, pool, terms, ("sum", coloring_index))
        target = len(set(coloring)) == 1
        cnf.append([parity if target else -parity])

    print(f"vars={pool.top} clauses={len(cnf.clauses)}", flush=True)
    started = time.time()
    with Solver(name=args.solver, bootstrap_with=cnf) as solver:
        sat = solver.solve()
        print(f"sat={sat} time={time.time()-started:.2f}s", flush=True)
        if not sat:
            return
        model = {literal for literal in solver.get_model() if literal > 0}
        matrices = {}
        for u, v in itertools.combinations(range(N), 2):
            table = tuple(
                tuple(int(entry(u, v, a, b) in model) for b in range(Q))
                for a in range(Q)
            )
            if any(any(row) for row in table):
                matrices[u, v] = table

        # Independent exact audit of all 3^6 principal Pfaffians.
        for coloring in itertools.product(range(Q), repeat=N):
            matrix = [[0 for _ in range(N)] for _ in range(N)]
            for u, v in itertools.combinations(range(N), 2):
                value = matrices.get((u, v), ((0,) * Q,) * Q)[coloring[u]][coloring[v]]
                matrix[u][v] = matrix[v][u] = value
            assert pfaffian_f2(matrix) == int(len(set(coloring)) == 1)
        print("matrices =", matrices)


if __name__ == "__main__":
    main()
