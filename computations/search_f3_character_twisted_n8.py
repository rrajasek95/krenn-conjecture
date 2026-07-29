#!/usr/bin/env python3
"""Exact F_3 search with character-twisted translation symmetry on K8.

Vertices are F_2^3.  Choose one sign character ``chi_c`` for each colour.
For an oriented translate of the base edge ``(0,d)``, set

    A_(u,u+d)(a,b) = chi_a(u) chi_b(u) B_d(a,b).

Well-definedness on the unordered edge requires

    B_d(a,b) = chi_a(d) chi_b(d) B_d(b,a).

Thus every difference still has six independent entries, but reversing an
off-diagonal cell may negate it.  Translation scales a colouring coefficient
by a matching-independent sign.  Mixed target coefficients are zero and a
pure coefficient acquires ``chi_c(t)^8=1``, so 891 ordinary translation
orbits of colourings again suffice.
"""

from __future__ import annotations

import argparse

from pysat.formula import IDPool
from pysat.solvers import Solver

from search_f3_general import exactly_one, iff_and, iff_xor
from search_f3_translation_invariant_n8 import (
    MATCHINGS,
    N,
    Q,
    VERTICES,
    colouring_representatives,
)


def character(character_vector, vertex):
    return 2 if (character_vector & vertex).bit_count() % 2 else 1


def descriptor(u, v, left, right, characters):
    """Return the independent entry key and its multiplicative sign."""

    difference = u ^ v
    sign = (
        character(characters[left], u)
        * character(characters[right], u)
    ) % 3
    if left <= right:
        key = difference, left, right
    else:
        key = difference, right, left
        sign = (
            sign
            * character(characters[left], difference)
            * character(characters[right], difference)
        ) % 3
    return key, sign


def signed_row(row, sign):
    if sign == 1:
        return row
    assert sign == 2
    zero, one, two = row
    return zero, two, one


def build_formula(characters):
    pool = IDPool()
    clauses = []
    values = {}
    for difference in range(1, N):
        for left in range(Q):
            for right in range(left, Q):
                row = tuple(
                    pool.id(("entry", difference, left, right, value))
                    for value in range(3)
                )
                values[difference, left, right] = row
                exactly_one(clauses, row)

    def entry_row(u, v, left, right):
        key, sign = descriptor(u, v, left, right, characters)
        return signed_row(values[key], sign)

    representatives = colouring_representatives(False)
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
    entries = {}
    for key, row in values.items():
        selected = [value for value, literal in enumerate(row)
                    if literal in positive]
        assert len(selected) == 1
        entries[key] = selected[0]
    return entries


def verify(entries, characters):
    from itertools import product

    for colouring in product(range(Q), repeat=N):
        total = 0
        for matching in MATCHINGS:
            term = 1
            for u, v in matching:
                key, sign = descriptor(
                    u, v, colouring[u], colouring[v], characters
                )
                term = term * sign * entries[key] % 3
            total = (total + term) % 3
        expected = 1 if len(set(colouring)) == 1 else 0
        assert total == expected, (colouring, total, expected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characters", default="0,1,2")
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument("--phase", choices=("none", "sparse", "dense"),
                        default="sparse")
    args = parser.parse_args()
    characters = tuple(int(item) for item in args.characters.split(","))
    if len(characters) != Q or any(not 0 <= item < N for item in characters):
        parser.error("--characters must be three comma-separated values in 0..7")

    # Audit unordered-edge well-definedness before building the CNF.
    for u in VERTICES:
        for v in VERTICES:
            if u >= v:
                continue
            for left in range(Q):
                for right in range(Q):
                    assert descriptor(u, v, left, right, characters) == descriptor(
                        v, u, right, left, characters
                    )

    pool, clauses, values, representatives = build_formula(characters)
    print(
        f"characters={characters} entry_orbits={len(values)} "
        f"colouring_orbits={len(representatives)} matchings={len(MATCHINGS)} "
        f"variables={pool.top} clauses={len(clauses)}",
        flush=True,
    )
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        if args.phase != "none":
            phases = []
            for zero, one, two in values.values():
                phases.extend(
                    (zero, -one, -two) if args.phase == "sparse"
                    else (-zero, one, -two)
                )
            solver.set_phases(phases)
        satisfiable = solver.solve()
        print(f"SAT={satisfiable}", flush=True)
        if not satisfiable:
            return
        entries = decode(solver.get_model(), values)
    verify(entries, characters)
    print("direct all-colouring F3 verification: PASS")
    for key in sorted(entries):
        print(key, entries[key])


if __name__ == "__main__":
    main()

