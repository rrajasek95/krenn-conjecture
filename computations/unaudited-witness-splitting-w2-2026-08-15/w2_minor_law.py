#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- the h=2 chain IS P1's uniform minor law at h=2.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01
(re-verified against 181a4c0: only notes/2026-08-15-resolution-master-plan.md
moved; no dependency of this probe changed.)

P1's FACT 1 (h=3): the determinantal Lambda^3 x Lambda^3 pairing is the only
equivariant degree-3 obstruction, and

    D(s^{3-j} kappa_{c_1}..kappa_{c_j}) = (3-j)! * complementary minor of A_pq.

At h=2 the pairing is Lambda^2 x Lambda^2 (the nine 2x2 minors of the cap K,
whose annihilator is P2's W).  The same law predicts

    j=0  s^2                        -> all complementary 2x2 minors vanish
                                       (i.e. rank A_pq <= 1)
    j=1  s*kappa_c                  -> complementary 1x1 minors vanish, i.e.
                                       every entry off row c and column c
    j=2  kappa_c kappa_c' (c != c') -> complementary 0x0 minor = 1, never blocks
    j=2  kappa_c^2                  -> repeated index, the pairing degenerates,
                                       so the condition is unconditional

This script checks all four identifications exhaustively over the 512 zero/one
supports of a 3x3 block, against the ACTUAL W-membership computed by P2's own
`in_sym_square`.  It is therefore an independent confirmation of P1's FACT 1 in
the degree where P2 has exhaustive data.
"""
import sys
from fractions import Fraction
from itertools import product

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-witness-splitting-p2-2026-08-15")
from wsplit_core import (KAPPA_VARS, in_sym_square, lin_mul,  # noqa: E402
                         lin_zero, matrix_rank)


def s_form(matrix):
    return [matrix[i][j] for i in range(3) for j in range(3)]


def kappa_form(colour):
    form = lin_zero()
    form[KAPPA_VARS[colour]] = Fraction(1)
    return form


def main():
    counts = {"j0": 0, "j1": 0, "j2_distinct": 0, "j2_repeated": 0}
    for support in product((0, 1), repeat=9):
        matrix = [[Fraction(support[3 * i + j]) for j in range(3)]
                  for i in range(3)]
        s = s_form(matrix)
        if not any(s):
            continue
        minors_vanish = all(
            matrix[i][k] * matrix[j][l] - matrix[i][l] * matrix[j][k] == 0
            for i in range(3) for j in range(i + 1, 3)
            for k in range(3) for l in range(k + 1, 3))
        assert (in_sym_square(lin_mul(s, s)) == minors_vanish
                == (matrix_rank(matrix) <= 1)), support
        counts["j0"] += 1
        for colour in range(3):
            entries_vanish = all(matrix[i][j] == 0
                                 for i in range(3) for j in range(3)
                                 if i != colour and j != colour)
            assert in_sym_square(lin_mul(s, kappa_form(colour))) == entries_vanish
            counts["j1"] += 1
        for c in range(3):
            for d in range(3):
                value = in_sym_square(lin_mul(kappa_form(c), kappa_form(d)))
                if c != d:
                    assert value is False
                    counts["j2_distinct"] += 1
                else:
                    assert value is True
                    counts["j2_repeated"] += 1
    print("UNAUDITED PROBE (W2) -- h=2 minor-law identifications verified:",
          counts)
    print("=> the h=2 pattern chain is the h=2 case of P1 FACT 1's minor law")


if __name__ == "__main__":
    main()
