#!/usr/bin/env python3
"""Exact SAT search for a diagonal {0,+1,-1} q=3 construction on n=8.

Every (underlying edge, color) entry is independently absent or has sign
+/-1.  For each coloring, the hafnian coefficient is encoded exactly as the
difference between positive and negative supported perfect matchings.
"""

from __future__ import annotations

import itertools
import time
import argparse

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


N = 8
Q = 3
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))


def add_iff_and(cnf, output, literals):
    for literal in literals:
        cnf.append([-output, literal])
    cnf.append([output] + [-literal for literal in literals])


def add_xor2(cnf, output, left, right):
    cnf.extend([
        [left, right, -output],
        [-left, -right, -output],
        [left, -right, output],
        [-left, right, output],
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-entries", type=int)
    args = parser.parse_args()
    pool = IDPool()
    cnf = CNF()

    def present(edge, color):
        return pool.id(("present", tuple(sorted(edge)), color))

    def negative(edge, color):
        return pool.id(("negative", tuple(sorted(edge)), color))

    for edge in EDGES:
        for color in range(Q):
            cnf.append([-negative(edge, color), present(edge, color)])

    # Any integer coefficient equal to +1 has a positive supported monomial.
    # Relabeling vertices lets us fix one such color-zero matching.
    canonical = ((0, 1), (2, 3), (4, 5), (6, 7))
    for edge in canonical:
        cnf.append([present(edge, 0)])
        cnf.append([-negative(edge, 0)])

    if args.max_entries is not None:
        constraint = CardEnc.atmost(
            lits=[present(edge, color) for edge in EDGES for color in range(Q)],
            bound=args.max_entries, vpool=pool, encoding=EncType.seqcounter,
        )
        cnf.extend(constraint.clauses)

    fibers = {}
    for coloring in itertools.product(range(Q), repeat=N):
        terms = []
        for matching in MATCHINGS:
            if not all(coloring[u] == coloring[v] for u, v in matching):
                continue
            decorated = tuple((tuple(sorted(edge)), coloring[edge[0]]) for edge in matching)
            active = pool.id(("active", coloring, matching))
            add_iff_and(cnf, active, tuple(present(edge, color) for edge, color in decorated))

            parity = negative(*decorated[0])
            for step, (edge, color) in enumerate(decorated[1:], start=1):
                next_parity = pool.id(("parity", coloring, matching, step))
                add_xor2(cnf, next_parity, parity, negative(edge, color))
                parity = next_parity

            positive = pool.id(("positive", coloring, matching))
            negative_term = pool.id(("negative_term", coloring, matching))
            cnf.extend([
                [-positive, active], [-positive, -parity], [-active, parity, positive],
                [-negative_term, active], [-negative_term, parity],
                [-active, -parity, negative_term],
            ])
            terms.append((positive, negative_term))
        if not terms:
            continue
        target = int(len(set(coloring)) == 1)
        literals = [positive for positive, _ in terms] + [-negative_term for _, negative_term in terms]
        # Sum(literals) = number_of_terms + (#positive - #negative).
        bound = len(terms) + target
        constraint = CardEnc.equals(
            lits=literals, bound=bound, vpool=pool, encoding=EncType.seqcounter
        )
        cnf.extend(constraint.clauses)
        fibers[coloring] = terms

    started = time.time()
    with Solver(name="cadical195", bootstrap_with=cnf) as solver:
        sat = solver.solve()
        elapsed = time.time() - started
        print(f"vars={pool.top} clauses={len(cnf.clauses)} fibers={len(fibers)} sat={sat} time={elapsed:.2f}s")
        if not sat:
            return
        model = set(literal for literal in solver.get_model() if literal > 0)
        entries = {}
        for edge in EDGES:
            for color in range(Q):
                if present(edge, color) in model:
                    entries[edge, color] = -1 if negative(edge, color) in model else 1
        print("entries = {")
        for key, value in sorted(entries.items()):
            print(f"    {key!r}: {value},")
        print("}")

        # Independent integer coefficient audit.
        for coloring in itertools.product(range(Q), repeat=N):
            total = 0
            for matching in MATCHINGS:
                term = 1
                for edge in matching:
                    u, v = edge
                    if coloring[u] != coloring[v]:
                        term = 0
                        break
                    term *= entries.get((tuple(sorted(edge)), coloring[u]), 0)
                total += term
            expected = int(len(set(coloring)) == 1)
            assert total == expected, (coloring, total, expected)
        print("independent exact audit passed")


if __name__ == "__main__":
    main()
