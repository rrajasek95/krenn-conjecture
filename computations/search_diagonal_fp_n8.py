#!/usr/bin/env python3
"""Exact diagonal n=8 search over a small prime field F_p.

This is the generic-prime companion to ``search_diagonal_f3_n8.py``.
One-hot finite-field gates compute every principal hafnian of three scalar
edge matrices, after which 1,638 even-partition clauses impose ternary GHZ.
A SAT result is only a finite-field discovery point until separately lifted.
"""

from __future__ import annotations

import argparse
from itertools import combinations

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

from search_f3_general import exactly_one, perfect_matchings


N = 8
Q = 3
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))
EVEN_MASKS = tuple(
    mask for mask in range(1 << N) if mask.bit_count() % 2 == 0
)


def build(prime, max_nonzero=None):
    pool = IDPool()
    clauses = []

    def state(tag):
        values = tuple(pool.id((tag, value)) for value in range(prime))
        exactly_one(clauses, values)
        return values

    def constant(tag, value):
        values = state(tag)
        clauses.append([values[value % prime]])
        return values

    def gate(tag, left, right, operation):
        output = state(tag)
        for a in range(prime):
            for b in range(prime):
                clauses.append([
                    -left[a], -right[b], output[operation(a, b) % prime]
                ])
        return output

    entries = {}
    for colour in range(Q):
        for edge in EDGES:
            entries[colour, edge] = state(("entry", colour, edge))

    canonical = ((0, 1), (2, 3), (4, 5), (6, 7))
    for index, edge in enumerate(canonical):
        values = entries[0, edge]
        clauses.append(list(values[1:]))
        if index < len(canonical) - 1:
            clauses.append([values[1]])

    haf = {}
    for colour in range(Q):
        for mask in EVEN_MASKS:
            subset = tuple(v for v in VERTICES if mask >> v & 1)
            accumulator = constant(("sum0", colour, mask), 0)
            for matching_number, matching in enumerate(
                perfect_matchings(subset), start=1
            ):
                if not matching:
                    term = constant(("empty", colour, mask), 1)
                else:
                    first, *tail = matching
                    term = entries[colour, tuple(sorted(first))]
                    for step, edge in enumerate(tail, start=1):
                        term = gate(
                            ("product", colour, mask, matching_number, step),
                            term,
                            entries[colour, tuple(sorted(edge))],
                            lambda a, b: a * b,
                        )
                accumulator = gate(
                    ("sum", colour, mask, matching_number),
                    accumulator,
                    term,
                    lambda a, b: a + b,
                )
            haf[colour, mask] = accumulator

    full = (1 << N) - 1
    for colour in range(Q):
        clauses.append([haf[colour, full][1]])

    partitions = 0
    for mask0 in EVEN_MASKS:
        complement0 = full ^ mask0
        mask1 = complement0
        while True:
            mask2 = complement0 ^ mask1
            if mask1.bit_count() % 2 == 0:
                if sum(mask != 0 for mask in (mask0, mask1, mask2)) >= 2:
                    clauses.append([
                        haf[0, mask0][0],
                        haf[1, mask1][0],
                        haf[2, mask2][0],
                    ])
                    partitions += 1
            if mask1 == 0:
                break
            mask1 = (mask1 - 1) & complement0
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
    return pool, clauses, entries


def scalar_hafnian(matrix, subset, prime):
    total = 0
    for matching in perfect_matchings(tuple(subset)):
        term = 1
        for edge in matching:
            term = term * matrix[tuple(sorted(edge))] % prime
        total = (total + term) % prime
    return total


def verify(model, entries, prime):
    positive = {literal for literal in model if literal > 0}
    matrices = []
    for colour in range(Q):
        matrix = {}
        for edge in EDGES:
            chosen = [
                value
                for value, variable in enumerate(entries[colour, edge])
                if variable in positive
            ]
            assert len(chosen) == 1
            matrix[edge] = chosen[0]
        matrices.append(matrix)
    cache = {
        (colour, mask): scalar_hafnian(
            matrices[colour],
            tuple(v for v in VERTICES if mask >> v & 1),
            prime,
        )
        for colour in range(Q)
        for mask in EVEN_MASKS
    }
    full = (1 << N) - 1
    assert all(cache[colour, full] == 1 for colour in range(Q))
    for mask0 in EVEN_MASKS:
        complement0 = full ^ mask0
        mask1 = complement0
        while True:
            mask2 = complement0 ^ mask1
            if mask1.bit_count() % 2 == 0:
                if sum(mask != 0 for mask in (mask0, mask1, mask2)) >= 2:
                    assert (
                        cache[0, mask0]
                        * cache[1, mask1]
                        * cache[2, mask2]
                    ) % prime == 0
            if mask1 == 0:
                break
            mask1 = (mask1 - 1) & complement0
    return matrices


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, choices=(3, 5, 7), default=5)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--max-nonzero", type=int)
    args = parser.parse_args()
    pool, clauses, entries = build(args.prime, args.max_nonzero)
    print(
        f"p={args.prime} variables={pool.top} clauses={len(clauses)} "
        f"max_nonzero={args.max_nonzero}",
        flush=True,
    )
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
        print(f"SAT={satisfiable}", flush=True)
        if not satisfiable:
            return
        matrices = verify(solver.get_model(), entries, args.prime)
    print(f"direct diagonal F_{args.prime} verification: PASS", flush=True)
    for colour, matrix in enumerate(matrices):
        for edge in EDGES:
            if matrix[edge]:
                print(colour, edge, matrix[edge], flush=True)


if __name__ == "__main__":
    main()
