#!/usr/bin/env python3
"""Exact mod-2 obstruction for three diagonal edge matrices at n=8.

Reducing a diagonal {0,+1,-1} source modulo two forgets all signs.  A subset
hafnian is then the parity of its supported perfect matchings.  This SAT
instance asks for three support graphs whose full hafnians are odd but for
which every proper even three-way partition has a color class with even
hafnian.  It is UNSAT.

Run with:

    uv run --with python-sat python \
      computations/verify_diagonal_n8_mod2_sat.py
"""

from __future__ import annotations

import itertools
import time

try:
    from pysat.solvers import Solver
except ImportError as error:  # pragma: no cover - dependency diagnostic
    raise SystemExit(
        "python-sat is required; run with `uv run --with python-sat python ...`"
    ) from error


N = 8
Q = 3
FULL = (1 << N) - 1
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
EVEN_MASKS = tuple(
    mask for mask in range(1 << N) if mask.bit_count() % 2 == 0
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + matching))


MATCHINGS = {
    mask: tuple(perfect_matchings(tuple(
        vertex for vertex in VERTICES if mask >> vertex & 1
    )))
    for mask in EVEN_MASKS
}


class VariablePool:
    def __init__(self):
        self.top = 0

    def new(self):
        self.top += 1
        return self.top


def add_iff_and(clauses, output, literals):
    clauses.extend([-output, literal] for literal in literals)
    clauses.append([output] + [-literal for literal in literals])


def add_xor(clauses, pool, left, right):
    output = pool.new()
    clauses.extend((
        [left, right, -output],
        [-left, -right, -output],
        [left, -right, output],
        [-left, right, output],
    ))
    return output


def main() -> None:
    pool = VariablePool()
    clauses: list[list[int]] = []
    present = [[pool.new() for _ in EDGES] for _ in range(Q)]
    odd_hafnian = {}

    for color in range(Q):
        for mask, matchings in MATCHINGS.items():
            matching_terms = []
            for matching in matchings:
                active = pool.new()
                add_iff_and(
                    clauses,
                    active,
                    [present[color][EDGE_INDEX[edge]] for edge in matching],
                )
                matching_terms.append(active)
            parity = matching_terms[0]
            for term in matching_terms[1:]:
                parity = add_xor(clauses, pool, parity, term)
            odd_hafnian[color, mask] = parity
        clauses.append([odd_hafnian[color, FULL]])

    # A nonzero full color-0 hafnian has a supported perfect matching.  A
    # common vertex permutation sends it to this canonical matching.
    for edge in ((0, 1), (2, 3), (4, 5), (6, 7)):
        clauses.append([present[0][EDGE_INDEX[edge]]])

    zero = {}
    for color in range(Q):
        for mask in EVEN_MASKS:
            if mask == FULL:
                continue
            witness = zero[color, mask] = pool.new()
            # The witness need only imply even parity; partition coverage
            # supplies the converse existential choice when needed.
            clauses.append([-witness, -odd_hafnian[color, mask]])

    mixed_partitions = 0
    for first in EVEN_MASKS:
        remainder = FULL ^ first
        second = remainder
        while True:
            third = remainder ^ second
            if (
                second.bit_count() % 2 == 0
                and first != FULL
                and second != FULL
                and third != FULL
            ):
                clauses.append(
                    [zero[0, first], zero[1, second], zero[2, third]]
                )
                mixed_partitions += 1
            if second == 0:
                break
            second = (second - 1) & remainder

    print(
        f"built vars={pool.top} clauses={len(clauses)} "
        f"mixed_partitions={mixed_partitions}",
        flush=True,
    )
    started = time.time()
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
    print(f"sat={satisfiable} time={time.time() - started:.2f}s", flush=True)
    assert not satisfiable


if __name__ == "__main__":
    main()
