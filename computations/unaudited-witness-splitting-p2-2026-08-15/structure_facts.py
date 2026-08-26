#!/usr/bin/env python3
"""UNAUDITED PROBE (P2) -- the exact structure behind the h=2 splitting patterns.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

Two facts drive every statistic in this probe.

FACT 1 (span constraint).  For every six-site source and every pair, every one
of the 81 components of E_pq = [r^2/2]_U is a quadratic form lying in

    W = Sym^2(V_p^*) (x) Sym^2(V_q^*)   (dim 36 of the 45 quadrics),

the annihilator of the nine 2x2 minors of the cap matrix K.  Since the
degree-2 part of the error ideal is the span of those components, every
degree-2 splitting pattern must itself lie in W.

FACT 2 (which patterns can lie in W).  With L = {s, kappa_0, kappa_1, kappa_2}:
    kappa_c * kappa_c      in W  always;
    kappa_c * kappa_c'     in W  never (c != c');
    s * s                  in W  iff rank A_pq <= 1;
    s * kappa_c            in W  iff A_pq is supported in row c union column c
                                 (which forces rank A_pq <= 2).
So the plan's 10 patterns collapse at h=2 to three unconditional ones and four
that impose an exact rank/support degeneracy on the edge block itself.

This script checks Fact 1 on random sources and Fact 2 exhaustively over
supports plus randomly over values.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations_with_replacement, product
import random

from wsplit_core import (KAPPA_VARS, PAIRS, PairData, in_sym_square, lin_mul,
                         lin_zero, matrix_rank, random_source, require)


def s_form(matrix):
    return [matrix[i][j] for i in range(3) for j in range(3)]


def kappa_form(colour):
    form = lin_zero()
    form[KAPPA_VARS[colour]] = Fraction(1)
    return form


def check_fact1(trials=60):
    rng = random.Random(101)
    modes = ("generic", "sparse", "lowrank", "diagonal", "binary")
    checked = 0
    for index in range(trials):
        source = random_source(rng, modes[index % len(modes)])
        for pair in PAIRS:
            pd = PairData(source, *pair)
            for quad in pd.quadrics:
                require(in_sym_square(quad),
                        f"FACT 1 failed at {pair} of source {index}")
                checked += 1
    return checked


def check_fact2_supports():
    """Exhaustive over all 512 zero/one supports of A_pq."""
    rows = []
    for support in product((0, 1), repeat=9):
        matrix = [[Fraction(support[3 * i + j]) for j in range(3)]
                  for i in range(3)]
        s = s_form(matrix)
        rank = matrix_rank(matrix)
        for colour in range(3):
            cross = all(support[3 * i + j] == 0 for i in range(3)
                        for j in range(3) if i != colour and j != colour)
            predicted = cross
            actual = in_sym_square(lin_mul(s, kappa_form(colour)))
            require(predicted == actual,
                    f"s*kappa_{colour} criterion failed on {support}")
            if actual:
                require(rank <= 2, f"s*kappa cross with rank {rank}")
        predicted = rank <= 1
        actual = in_sym_square(lin_mul(s, s))
        require(predicted == actual, f"s*s criterion failed on {support}")
        rows.append((support, rank))
    return len(rows)


def check_fact2_values(trials=400):
    rng = random.Random(202)
    for _ in range(trials):
        rank = rng.choice([0, 1, 2, 3])
        from wsplit_core import random_rank_matrix
        matrix = random_rank_matrix(rng, rank)
        s = s_form(matrix)
        require(in_sym_square(lin_mul(s, s)) == (matrix_rank(matrix) <= 1),
                "s*s criterion failed on a random matrix")
        for colour in range(3):
            cross = all(matrix[i][j] == 0 for i in range(3) for j in range(3)
                        if i != colour and j != colour)
            require(in_sym_square(lin_mul(s, kappa_form(colour))) == cross,
                    "s*kappa criterion failed on a random matrix")
    return trials


def check_kappa_patterns():
    for a, b in combinations_with_replacement(range(3), 2):
        quad = lin_mul(kappa_form(a), kappa_form(b))
        expected = (a == b)
        require(in_sym_square(quad) == expected,
                f"kappa_{a}*kappa_{b} membership wrong")
    return 6


def main():
    print("UNAUDITED PROBE -- h=2 structure facts, HEAD 86a9479")
    print("FACT 1 components checked in W :", check_fact1())
    print("FACT 2 kappa patterns          :", check_kappa_patterns(),
          "(only the three squares lie in W)")
    print("FACT 2 exhaustive supports     :", check_fact2_supports())
    print("FACT 2 random values           :", check_fact2_values())
    print("all structure facts PASS")


if __name__ == "__main__":
    main()
