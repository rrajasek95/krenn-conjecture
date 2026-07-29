#!/usr/bin/env python3
"""Exact F_3 search for a diagonal three-colour realization at n=8.

For same-colour aggregate cells, a colouring with even colour classes
``S_0,S_1,S_2`` has coefficient

    haf(A_0[S_0]) haf(A_1[S_1]) haf(A_2[S_2]).

Thus only the principal hafnians of three scalar 8 by 8 matrices are
needed.  This encoding computes every one of them exactly modulo three and
requires the three full hafnians to be one while every proper even ordered
partition has a zero factor.  Any SAT point is directly re-enumerated.

This is a discovery calculation: an F_3 point becomes a complex
counterexample only after a separate characteristic-zero lifting audit.
"""

from __future__ import annotations

import argparse
from itertools import combinations

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

from search_f3_general import exactly_one, iff_and, iff_xor, perfect_matchings


N = 8
Q = 3
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))


def even_masks():
    return tuple(mask for mask in range(1 << N) if mask.bit_count() % 2 == 0)


def build(max_nonzero=None):
    pool = IDPool()
    clauses = []
    entries = {}
    for colour in range(Q):
        for edge in EDGES:
            row = tuple(
                pool.id(("entry", colour, edge, value)) for value in range(3)
            )
            entries[colour, edge] = row
            exactly_one(clauses, row)

    canonical = ((0, 1), (2, 3), (4, 5), (6, 7))
    for index, edge in enumerate(canonical):
        zero, one, two = entries[0, edge]
        clauses.append([one, two])
        if index < len(canonical) - 1:
            clauses.append([one])

    haf = {}
    for colour in range(Q):
        for mask in even_masks():
            subset = tuple(v for v in VERTICES if mask >> v & 1)
            accumulator = tuple(
                pool.id(("acc", colour, mask, 0, residue))
                for residue in range(3)
            )
            clauses.append([accumulator[0]])
            clauses.extend([[-accumulator[1]], [-accumulator[2]]])

            for matching_number, matching in enumerate(
                perfect_matchings(subset), start=1
            ):
                if not matching:
                    # The empty matching is the multiplicative unit.
                    nonzero = pool.id(("empty-nz", colour, mask))
                    plus = pool.id(("empty-plus", colour, mask))
                    clauses.extend(([nonzero], [plus]))
                    minus = pool.id(("empty-minus", colour, mask))
                    clauses.append([-minus])
                else:
                    nonzero_literals = []
                    negative_literals = []
                    for edge in matching:
                        zero, _one, two = entries[colour, tuple(sorted(edge))]
                        nonzero_literals.append(-zero)
                        negative_literals.append(two)
                    nonzero = pool.id(
                        ("term-nz", colour, mask, matching_number)
                    )
                    iff_and(clauses, nonzero, nonzero_literals)
                    parity = negative_literals[0]
                    for step, literal in enumerate(negative_literals[1:], 1):
                        nxt = pool.id(
                            ("term-parity", colour, mask, matching_number, step)
                        )
                        iff_xor(clauses, nxt, parity, literal)
                        parity = nxt
                    plus = pool.id(
                        ("term-plus", colour, mask, matching_number)
                    )
                    minus = pool.id(
                        ("term-minus", colour, mask, matching_number)
                    )
                    iff_and(clauses, plus, (nonzero, -parity))
                    iff_and(clauses, minus, (nonzero, parity))

                nxt_accumulator = tuple(
                    pool.id(
                        ("acc", colour, mask, matching_number, residue)
                    )
                    for residue in range(3)
                )
                exactly_one(clauses, nxt_accumulator)
                for residue in range(3):
                    clauses.append(
                        [-accumulator[residue], nonzero,
                         nxt_accumulator[residue]]
                    )
                    clauses.append(
                        [-accumulator[residue], -plus,
                         nxt_accumulator[(residue + 1) % 3]]
                    )
                    clauses.append(
                        [-accumulator[residue], -minus,
                         nxt_accumulator[(residue + 2) % 3]]
                    )
                accumulator = nxt_accumulator
            haf[colour, mask] = accumulator

    full = (1 << N) - 1
    for colour in range(Q):
        clauses.append([haf[colour, full][1]])

    partitions = 0
    for mask0 in even_masks():
        complement0 = full ^ mask0
        submask = complement0
        while True:
            mask1 = submask
            mask2 = complement0 ^ mask1
            if mask1.bit_count() % 2 == 0:
                nonempty = sum(mask != 0 for mask in (mask0, mask1, mask2))
                if nonempty >= 2:
                    clauses.append([
                        haf[0, mask0][0],
                        haf[1, mask1][0],
                        haf[2, mask2][0],
                    ])
                    partitions += 1
            if submask == 0:
                break
            submask = (submask - 1) & complement0
    assert partitions == 1638

    if max_nonzero is not None:
        encoding = CardEnc.atmost(
            lits=[-entries[colour, edge][0]
                  for colour in range(Q) for edge in EDGES],
            bound=max_nonzero,
            top_id=pool.top,
            encoding=EncType.kmtotalizer,
        )
        clauses.extend(encoding.clauses)
        if encoding.nv > pool.top:
            pool.occupy(pool.top + 1, encoding.nv)
    return pool, clauses, entries, haf


def scalar_hafnian(matrix, subset):
    total = 0
    for matching in perfect_matchings(tuple(subset)):
        term = 1
        for edge in matching:
            term = term * matrix[tuple(sorted(edge))] % 3
        total = (total + term) % 3
    return total


def verify(model, entries):
    positive = {literal for literal in model if literal > 0}
    matrices = []
    for colour in range(Q):
        matrix = {}
        for edge in EDGES:
            values = entries[colour, edge]
            chosen = [value for value, variable in enumerate(values)
                      if variable in positive]
            assert len(chosen) == 1
            matrix[edge] = chosen[0]
        matrices.append(matrix)

    full = (1 << N) - 1
    cache = {}
    for colour in range(Q):
        for mask in even_masks():
            subset = tuple(v for v in VERTICES if mask >> v & 1)
            cache[colour, mask] = scalar_hafnian(matrices[colour], subset)
        assert cache[colour, full] == 1
    for mask0 in even_masks():
        complement0 = full ^ mask0
        submask = complement0
        while True:
            mask1 = submask
            mask2 = complement0 ^ mask1
            if mask1.bit_count() % 2 == 0:
                nonempty = sum(mask != 0 for mask in (mask0, mask1, mask2))
                if nonempty >= 2:
                    assert (
                        cache[0, mask0]
                        * cache[1, mask1]
                        * cache[2, mask2]
                    ) % 3 == 0
            if submask == 0:
                break
            submask = (submask - 1) & complement0
    return matrices, cache


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--max-nonzero", type=int)
    args = parser.parse_args()
    pool, clauses, entries, _haf = build(args.max_nonzero)
    print(
        f"variables={pool.top} clauses={len(clauses)} "
        f"max_nonzero={args.max_nonzero}",
        flush=True,
    )
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
        print(f"SAT={satisfiable}", flush=True)
        if not satisfiable:
            return
        matrices, _cache = verify(solver.get_model(), entries)
    print("direct diagonal F3 verification: PASS", flush=True)
    for colour, matrix in enumerate(matrices):
        for edge in EDGES:
            if matrix[edge]:
                print(colour, edge, matrix[edge], flush=True)


if __name__ == "__main__":
    main()
