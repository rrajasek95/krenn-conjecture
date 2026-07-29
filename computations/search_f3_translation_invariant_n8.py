#!/usr/bin/env python3
"""Exact F_3 search for a translation-invariant K8 realization.

Identify the eight vertices with F_2^3.  The matrix on an edge ``{u,v}``
depends only on ``u xor v`` and is symmetric in its two colour indices.
This leaves seven symmetric 3 by 3 matrices (42 field entries).  Vertex
translation has 891 orbits on the 3^8 colourings, so one exact coefficient
equation per orbit suffices.

This is a discovery slice.  A finite-field point still needs a rigorous
characteristic-zero lift before it can refute Krenn's conjecture.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product

from pysat.formula import IDPool
from pysat.solvers import Solver

from search_f3_general import (
    exactly_one,
    iff_and,
    iff_xor,
    perfect_matchings,
)


N = 8
Q = 3
VERTICES = tuple(range(N))
MATCHINGS = tuple(perfect_matchings(VERTICES))
COLOUR_SWAP = (0, 2, 1)

# The 18 GL(3,2)-orbit representatives of scalar translation-invariant
# K8 edge weights whose full hafnian equals 1 in F_3.  Every constant-colour
# diagonal of a solution belongs to one of these orbits, so fixing one row is
# a complete symmetry branch rather than a heuristic support assumption.
PURE_ORBIT_REPS = (
    (0, 0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, 0, 0, 2),
    (0, 0, 0, 0, 0, 1, 1),
    (0, 0, 0, 0, 0, 1, 2),
    (0, 0, 0, 0, 0, 2, 2),
    (0, 0, 1, 0, 1, 1, 1),
    (0, 0, 1, 0, 1, 1, 2),
    (0, 0, 1, 0, 1, 2, 1),
    (0, 0, 1, 0, 1, 2, 2),
    (0, 0, 1, 0, 2, 2, 1),
    (0, 0, 1, 0, 2, 2, 2),
    (0, 0, 2, 0, 2, 2, 1),
    (0, 0, 2, 0, 2, 2, 2),
    (0, 1, 1, 1, 1, 1, 2),
    (0, 1, 1, 1, 2, 1, 2),
    (0, 1, 1, 1, 2, 2, 2),
    (0, 1, 2, 1, 2, 2, 2),
    (0, 1, 2, 2, 2, 2, 2),
)

# For the colour-swap-twisted action, the distinguished character is
# ``u -> u & 1``.  Its stabilizer in GL(3,2) has order 24, rather than 168.
# The following are the 36 orbits of scalar translation-invariant rows with
# full F_3 hafnian one under that stabilizer and simultaneous field negation
# (which preserves every n=8 coefficient because a matching has four edges).
# Consequently fixing one of these rows is exhaustive in the twisted slice.
TWISTED_PURE_ORBIT_REPS = (
    (0, 0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 1, 1),
    (0, 0, 0, 0, 0, 1, 2),
    (0, 0, 0, 0, 1, 0, 1),
    (0, 0, 0, 0, 1, 0, 2),
    (0, 0, 0, 1, 0, 1, 0),
    (0, 0, 0, 1, 0, 2, 0),
    (0, 0, 1, 0, 1, 1, 1),
    (0, 0, 1, 0, 1, 1, 2),
    (0, 0, 1, 0, 1, 2, 1),
    (0, 0, 1, 0, 1, 2, 2),
    (0, 0, 1, 0, 2, 1, 1),
    (0, 0, 1, 0, 2, 1, 2),
    (0, 0, 1, 1, 0, 1, 1),
    (0, 0, 1, 1, 0, 1, 2),
    (0, 0, 1, 1, 0, 2, 1),
    (0, 0, 1, 1, 0, 2, 2),
    (0, 0, 1, 1, 1, 2, 0),
    (0, 0, 1, 2, 0, 2, 1),
    (0, 1, 0, 1, 0, 1, 1),
    (0, 1, 0, 1, 0, 1, 2),
    (0, 1, 0, 1, 0, 2, 1),
    (0, 1, 0, 1, 0, 2, 2),
    (0, 1, 1, 1, 1, 1, 2),
    (0, 1, 1, 1, 1, 2, 1),
    (0, 1, 1, 1, 2, 1, 2),
    (0, 1, 1, 1, 2, 2, 1),
    (0, 1, 1, 1, 2, 2, 2),
    (0, 1, 1, 2, 1, 2, 1),
    (1, 0, 1, 1, 1, 1, 2),
    (1, 0, 1, 1, 1, 2, 1),
    (1, 0, 1, 1, 1, 2, 2),
    (1, 0, 1, 1, 2, 2, 2),
    (1, 0, 1, 2, 1, 2, 2),
    (1, 0, 2, 1, 1, 1, 2),
)


def translate_colouring(colouring, shift, twisted=False):
    image = tuple(colouring[vertex ^ shift] for vertex in VERTICES)
    if twisted and shift & 1:
        image = tuple(COLOUR_SWAP[colour] for colour in image)
    return image


def colouring_representatives(twisted=False):
    return tuple(
        colouring
        for colouring in product(range(Q), repeat=N)
        if colouring == min(
            translate_colouring(colouring, shift, twisted)
            for shift in VERTICES
        )
    )


def cell_key(difference, left, right, twisted=False):
    if twisted and difference & 1:
        opposite = (COLOUR_SWAP[right], COLOUR_SWAP[left])
    else:
        opposite = (right, left)
    return min((left, right), opposite)


def edge_key(u, v, left, right, twisted=False):
    difference = u ^ v
    if twisted and u & 1:
        left, right = COLOUR_SWAP[left], COLOUR_SWAP[right]
    return difference, *cell_key(difference, left, right, twisted)


def build_formula(pure0_orbit=None, twisted=False):
    pool = IDPool()
    clauses = []
    values = {}
    for difference in range(1, N):
        representatives = sorted({
            cell_key(difference, left, right, twisted)
            for left, right in product(range(Q), repeat=2)
        })
        assert len(representatives) == 6
        for left, right in representatives:
                row = tuple(
                    pool.id(("entry", difference, left, right, value))
                    for value in range(3)
                )
                values[difference, left, right] = row
                exactly_one(clauses, row)

    if pure0_orbit is not None:
        representatives = (
            TWISTED_PURE_ORBIT_REPS if twisted else PURE_ORBIT_REPS
        )
        if not 0 <= pure0_orbit < len(representatives):
            raise ValueError(
                f"pure0 orbit must be in range(0, {len(representatives)})"
            )
        representative = representatives[pure0_orbit]
        for difference, value in enumerate(representative, start=1):
            clauses.append([values[difference, 0, 0][value]])

    def entry_row(u, v, left, right):
        return values[edge_key(u, v, left, right, twisted)]

    representatives = colouring_representatives(twisted)
    assert len(representatives) == 891
    for colouring_number, colouring in enumerate(representatives):
        accumulator = tuple(
            pool.id(("acc", colouring_number, 0, residue))
            for residue in range(3)
        )
        clauses.extend(([accumulator[0]], [-accumulator[1]], [-accumulator[2]]))

        for matching_number, matching in enumerate(MATCHINGS, start=1):
            nonzero_literals = []
            negative_literals = []
            for u, v in matching:
                zero, _one, two = entry_row(
                    u, v, colouring[u], colouring[v]
                )
                nonzero_literals.append(-zero)
                negative_literals.append(two)

            nonzero = pool.id(("nz", colouring_number, matching_number))
            iff_and(clauses, nonzero, nonzero_literals)
            parity = negative_literals[0]
            for position, literal in enumerate(negative_literals[1:], start=1):
                nxt = pool.id(
                    ("par", colouring_number, matching_number, position)
                )
                iff_xor(clauses, nxt, parity, literal)
                parity = nxt

            plus = pool.id(("plus", colouring_number, matching_number))
            minus = pool.id(("minus", colouring_number, matching_number))
            iff_and(clauses, plus, (nonzero, -parity))
            iff_and(clauses, minus, (nonzero, parity))

            nxt_accumulator = tuple(
                pool.id(("acc", colouring_number, matching_number, residue))
                for residue in range(3)
            )
            exactly_one(clauses, nxt_accumulator)
            for residue in range(3):
                clauses.append([
                    -accumulator[residue], nonzero,
                    nxt_accumulator[residue],
                ])
                clauses.append([
                    -accumulator[residue], -plus,
                    nxt_accumulator[(residue + 1) % 3],
                ])
                clauses.append([
                    -accumulator[residue], -minus,
                    nxt_accumulator[(residue + 2) % 3],
                ])
            accumulator = nxt_accumulator

        target = 1 if len(set(colouring)) == 1 else 0
        clauses.append([accumulator[target]])

    return pool, clauses, values, representatives


def decode(model, values):
    positive = {literal for literal in model if literal > 0}
    answer = {}
    for key, row in values.items():
        selected = [value for value, literal in enumerate(row)
                    if literal in positive]
        assert len(selected) == 1
        answer[key] = selected[0]
    return answer


def verify(entries, twisted=False):
    for colouring in product(range(Q), repeat=N):
        total = 0
        for matching in MATCHINGS:
            term = 1
            for u, v in matching:
                key = edge_key(
                    u, v, colouring[u], colouring[v], twisted
                )
                term = term * entries[key] % 3
            total = (total + term) % 3
        expected = 1 if len(set(colouring)) == 1 else 0
        assert total == expected, (colouring, total, expected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument("--phase", choices=("none", "sparse", "dense"),
                        default="sparse")
    parser.add_argument("--pure0-orbit", type=int)
    parser.add_argument("--twisted", action="store_true")
    args = parser.parse_args()
    orbit_count = len(
        TWISTED_PURE_ORBIT_REPS if args.twisted else PURE_ORBIT_REPS
    )
    if (args.pure0_orbit is not None
            and not 0 <= args.pure0_orbit < orbit_count):
        parser.error(f"--pure0-orbit must be in range(0, {orbit_count})")
    pool, clauses, values, representatives = build_formula(
        args.pure0_orbit, args.twisted
    )
    print(
        f"entry_orbits={len(values)} colouring_orbits={len(representatives)} "
        f"matchings={len(MATCHINGS)} variables={pool.top} "
        f"clauses={len(clauses)} pure0_orbit={args.pure0_orbit} "
        f"twisted={args.twisted}",
        flush=True,
    )
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        if args.phase != "none":
            phase_literals = []
            for zero, one, two in values.values():
                if args.phase == "sparse":
                    phase_literals.extend((zero, -one, -two))
                else:
                    phase_literals.extend((-zero, one, -two))
            solver.set_phases(phase_literals)
        satisfiable = solver.solve()
        print(f"SAT={satisfiable}", flush=True)
        if not satisfiable:
            return
        entries = decode(solver.get_model(), values)
    verify(entries, args.twisted)
    print("direct all-colouring F3 verification: PASS")
    for key in sorted(entries):
        print(key, entries[key])


if __name__ == "__main__":
    main()
