#!/usr/bin/env python3
"""Exact factored SAT search for a diagonal {0,+1,-1} q=3 model on n=8.

For a diagonal edge model, the coefficient of a coloring factors as the
product of the scalar hafnians on its three color classes.  The older direct
encoding rebuilt the same subset hafnian for many different colorings.  This
version encodes each (color, even subset) once and uses a selector which may
be true only when that hafnian is exactly zero.
"""

from __future__ import annotations

import argparse
import itertools
import time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


N = 8
Q = 3
V = tuple(range(N))
EDGES = tuple(itertools.combinations(V, 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for j in range(1, len(vertices)):
        v = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def add_iff_and(cnf, output, literals):
    for literal in literals:
        cnf.append([-output, literal])
    cnf.append([output] + [-literal for literal in literals])


def add_xor2(cnf, output, left, right):
    cnf.extend(
        [
            [left, right, -output],
            [-left, -right, -output],
            [left, -right, output],
            [-left, right, output],
        ]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-entries", type=int)
    parser.add_argument("--solver", default="cadical195")
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

    # Every full hafnian is +1, hence contains a positive supported matching.
    # Relabel vertices and flip pairs of edge signs in color zero to normalize
    # one of them to the canonical all-positive matching.
    canonical = ((0, 1), (2, 3), (4, 5), (6, 7))
    for edge in canonical:
        cnf.append([present(edge, 0)])
        cnf.append([-negative(edge, 0)])

    if args.max_entries is not None:
        cnf.extend(
            CardEnc.atmost(
                lits=[present(e, r) for e in EDGES for r in range(Q)],
                bound=args.max_entries,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )

    zero = {}
    term_count = 0
    for r in range(Q):
        for size in (2, 4, 6, 8):
            for subset in itertools.combinations(V, size):
                terms = []
                for matching in perfect_matchings(subset):
                    active = pool.id(("active", r, subset, matching))
                    add_iff_and(cnf, active, [present(e, r) for e in matching])

                    parity = negative(matching[0], r)
                    for step, edge in enumerate(matching[1:], start=1):
                        new_parity = pool.id(("parity", r, subset, matching, step))
                        add_xor2(cnf, new_parity, parity, negative(edge, r))
                        parity = new_parity

                    positive = pool.id(("positive", r, subset, matching))
                    negative_term = pool.id(("negative_term", r, subset, matching))
                    cnf.extend(
                        [
                            [-positive, active],
                            [-positive, -parity],
                            [-active, parity, positive],
                            [-negative_term, active],
                            [-negative_term, parity],
                            [-active, -parity, negative_term],
                        ]
                    )
                    terms.append((positive, negative_term))
                    term_count += 1

                # Sum(pos + not neg) = m + hafnian.  A zero selector is only
                # allowed when this sum equals m.  The reverse implication is
                # unnecessary: mixed partitions explicitly require at least
                # one valid selector.
                m = len(terms)
                literals = [p for p, _ in terms] + [-n for _, n in terms]
                if size == N:
                    # The three constant coefficients must be exactly +1.
                    cnf.extend(
                        CardEnc.equals(
                            lits=literals,
                            bound=m + 1,
                            vpool=pool,
                            encoding=EncType.seqcounter,
                        ).clauses
                    )
                else:
                    z = pool.id(("zero", r, subset))
                    zero[r, frozenset(subset)] = z
                    equality = CardEnc.equals(
                        lits=literals,
                        bound=m,
                        vpool=pool,
                        encoding=EncType.seqcounter,
                    )
                    cnf.extend([[-z] + clause for clause in equality.clauses])

    # A nonconstant coloring can have a nonzero coefficient only when every
    # nonempty color class has even size.  Its coefficient is the product of
    # the corresponding subset hafnians, so require one factor to vanish.
    mixed_partitions = 0
    for coloring in itertools.product(range(Q), repeat=N):
        classes = [frozenset(v for v, c in enumerate(coloring) if c == r) for r in range(Q)]
        if any(len(s) % 2 for s in classes):
            continue
        nonempty = [(r, s) for r, s in enumerate(classes) if s]
        if len(nonempty) <= 1:
            continue
        cnf.append([zero[r, s] for r, s in nonempty])
        mixed_partitions += 1

    print(
        f"built vars={pool.top} clauses={len(cnf.clauses)} "
        f"subset_terms={term_count} mixed_partitions={mixed_partitions}",
        flush=True,
    )
    started = time.time()
    with Solver(name=args.solver, bootstrap_with=cnf) as solver:
        sat = solver.solve()
        elapsed = time.time() - started
        print(f"sat={sat} time={elapsed:.2f}s", flush=True)
        if not sat:
            return
        model = {literal for literal in solver.get_model() if literal > 0}
        entries = {}
        for edge in EDGES:
            for color in range(Q):
                if present(edge, color) in model:
                    entries[edge, color] = -1 if negative(edge, color) in model else 1
        print("entries = {")
        for key, value in sorted(entries.items()):
            print(f"    {key!r}: {value},")
        print("}")

        # Independent direct integer audit over all 3^8 colorings.
        full_matchings = tuple(perfect_matchings(V))
        for coloring in itertools.product(range(Q), repeat=N):
            total = 0
            for matching in full_matchings:
                term = 1
                for edge in matching:
                    u, v = edge
                    if coloring[u] != coloring[v]:
                        term = 0
                        break
                    term *= entries.get((edge, coloring[u]), 0)
                total += term
            expected = int(len(set(coloring)) == 1)
            assert total == expected, (coloring, total, expected)
        print("independent exact audit passed")


if __name__ == "__main__":
    main()
