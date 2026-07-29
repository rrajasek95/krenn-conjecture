#!/usr/bin/env python3
"""Exact relaxed PB/SAT obstruction for diagonal {0,+1,-1} data at n=8.

Every (edge, color) entry is chosen independently.  For an even vertex set
S, the script encodes the signed matching count haf(A_color[S]) exactly.
Every proper even three-way partition must select a color-class hafnian that
is zero.  The three full hafnians are allowed to be either +1 or -1, a
relaxation of the exact GHZ requirement +1.

Run with:

    uv run --with python-sat python \
      computations/search_diagonal_signed_n8_relaxed_pb.py

Cadical 1.9.5 reports UNSAT for the resulting 185391-variable,
388345-clause formula (about 92 seconds on the development machine).
"""

from __future__ import annotations

import itertools
import time

try:
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
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


EVEN_MASKS = tuple(
    mask for mask in range(1 << N) if mask.bit_count() % 2 == 0
)
MATCHINGS = {
    mask: tuple(perfect_matchings(tuple(
        vertex for vertex in VERTICES if mask >> vertex & 1
    )))
    for mask in EVEN_MASKS
}


def add_xor(clauses, pool, left, right):
    output = pool.id()
    clauses.extend((
        [left, right, -output],
        [-left, -right, -output],
        [left, -right, output],
        [-left, right, output],
    ))
    return output


def main() -> None:
    pool = IDPool()
    clauses: list[list[int]] = []
    present = [
        [pool.id(("present", color, edge)) for edge in range(len(EDGES))]
        for color in range(Q)
    ]
    negative = [
        [pool.id(("negative", color, edge)) for edge in range(len(EDGES))]
        for color in range(Q)
    ]

    positive_terms = {}
    negative_terms = {}
    for color in range(Q):
        for mask, matchings in MATCHINGS.items():
            positives = []
            negatives = []
            for matching_number, matching in enumerate(matchings):
                edge_numbers = [EDGE_INDEX[edge] for edge in matching]
                active = pool.id(("active", color, mask, matching_number))
                clauses.extend(
                    [-active, present[color][edge]] for edge in edge_numbers
                )
                clauses.append(
                    [active] + [-present[color][edge] for edge in edge_numbers]
                )

                if not edge_numbers:  # hafnian of the empty set is one
                    positive = pool.id(("positive", color, mask, matching_number))
                    negative_term = pool.id(
                        ("negative-term", color, mask, matching_number)
                    )
                    clauses.extend(([positive], [-negative_term]))
                else:
                    parity = negative[color][edge_numbers[0]]
                    for edge in edge_numbers[1:]:
                        parity = add_xor(
                            clauses, pool, parity, negative[color][edge]
                        )
                    positive = pool.id(("positive", color, mask, matching_number))
                    negative_term = pool.id(
                        ("negative-term", color, mask, matching_number)
                    )
                    # positive iff active and parity zero; negative_term iff
                    # active and parity one.
                    clauses.extend((
                        [-positive, active],
                        [-positive, -parity],
                        [-active, parity, positive],
                        [-negative_term, active],
                        [-negative_term, parity],
                        [-active, -parity, negative_term],
                    ))
                positives.append(positive)
                negatives.append(negative_term)
            positive_terms[color, mask] = positives
            negative_terms[color, mask] = negatives

    # Since the full color-0 hafnian is nonzero, its support contains a
    # perfect matching.  A common vertex relabeling sends that matching to
    # the canonical one.  We do not fix its signs.
    for edge in ((0, 1), (2, 3), (4, 5), (6, 7)):
        clauses.append([present[0][EDGE_INDEX[edge]]])

    def equality_encoding(color: int, mask: int, target: int):
        """CNF for haf(A_color[mask]) == target."""

        positives = positive_terms[color, mask]
        negatives = negative_terms[color, mask]
        matching_count = len(MATCHINGS[mask])
        # #positive - #negative = target iff
        # #positive + #(not negative) = matching_count + target.
        return CardEnc.equals(
            lits=positives + [-literal for literal in negatives],
            bound=matching_count + target,
            vpool=pool,
            encoding=EncType.seqcounter,
        ).clauses

    # A sign selector enforces one of the two exact full-hafnian values.
    # The two cardinality encodings receive disjoint fresh auxiliaries.
    for color in range(Q):
        selector = pool.id(("full-positive", color))
        clauses.extend(
            [-selector] + clause
            for clause in equality_encoding(color, FULL, 1)
        )
        clauses.extend(
            [selector] + clause
            for clause in equality_encoding(color, FULL, -1)
        )

    zero = {}
    for color in range(Q):
        for mask in EVEN_MASKS:
            if mask == FULL:
                continue
            witness = zero[color, mask] = pool.id(("zero", color, mask))
            if mask == 0:
                clauses.append([-witness])
                continue
            clauses.extend(
                [-witness] + clause
                for clause in equality_encoding(color, mask, 0)
            )

    mixed_partitions = 0
    for first in EVEN_MASKS:
        remainder = FULL ^ first
        second = remainder
        while True:
            third = remainder ^ second
            if (
                second in MATCHINGS
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
