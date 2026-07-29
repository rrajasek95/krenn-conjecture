#!/usr/bin/env python3
"""Exact probes of generic diagonal n=6 collision bases with one y factor."""

from __future__ import annotations

import argparse
import itertools
import random
from fractions import Fraction

import verify_dense_diagonal_collision_obstruction as audit


def permanent_zero_matrix(rng):
    a, b, c = (Fraction(rng.choice((-3, -2, -1, 1, 2, 3))) for _ in range(3))
    return ((a, b), (c, -b * c / a))


def build(seed):
    rng = random.Random(seed)
    blocks = ((0, 1), (2, 3), (4, 5))
    matrices = [permanent_zero_matrix(rng) for _ in range(3)]
    q0 = {}
    for matrix, (left, right) in zip(matrices, itertools.combinations(blocks, 2)):
        for i, u in enumerate(left):
            for j, v in enumerate(right):
                q0[(u, v, audit.X, audit.X)] = matrix[i][j]
    for edge in blocks:
        q0[edge + (audit.Y, audit.Y)] = Fraction(1)
    hafnian = audit.output_coefficient(q0, (audit.X,) * audit.N)
    if not hafnian:
        return None
    # Every full x matching uses one edge from each block pair.
    left, right = blocks[0], blocks[1]
    scalar = Fraction(2) / hafnian
    for u in left:
        for v in right:
            q0[(u, v, audit.X, audit.X)] *= scalar
    return q0


def polynomial_string(row):
    terms = []
    offset = len(audit.EDGES)
    for i, value in enumerate(row[offset : offset + audit.N]):
        if value:
            terms.append(f"({value})t{i}")
    offset += audit.N
    for (i, j), value in zip(audit.PAIRS, row[offset : offset + len(audit.PAIRS)]):
        if value:
            terms.append(f"({value})t{i}t{j}")
    if row[-1]:
        terms.append(f"({row[-1]})")
    return " + ".join(terms) or "0"


def run(seed):
    q0 = build(seed)
    if q0 is None:
        print(f"seed={seed}: zero full hafnian")
        return
    for coloring in itertools.product((audit.X, audit.Y), repeat=audit.N):
        target = 2 if coloring == (audit.X,) * audit.N else int(
            coloring == (audit.Y,) * audit.N
        )
        assert audit.output_coefficient(q0, coloring) == target
    variables, particular, basis = audit.first_family(q0)
    rows = audit.quadratic_rows(q0, variables, particular, basis)
    reduced, _ = audit.rref(rows)
    eliminated = [row for row in reduced if not any(row[: len(audit.EDGES)])]
    print(
        f"seed={seed}: first_nullity={len(basis)} second_rank={len(reduced)} "
        f"eliminated={len(eliminated)}"
    )
    for row in eliminated:
        print("  ", polynomial_string(row))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=10)
    parser.add_argument("--starts", type=int, default=3)
    args = parser.parse_args()
    for offset in range(args.starts):
        run(args.seed + offset)


if __name__ == "__main__":
    main()
