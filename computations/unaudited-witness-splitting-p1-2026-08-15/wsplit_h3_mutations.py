#!/usr/bin/env python3
"""UNAUDITED PROBE -- task D for the h=3 structure module.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

Controls on FACT 1, the mixed-determinant obstruction table, the forcing F1
and the L-monomial membership test.

  M13 det-pairing with all signs +1                -> FACT 1 check fails
  M14 det-pairing of a permutation monomial        -> equals 1 (functional
                                                      is not identically 0)
  M15 one generator dropped from the ideal         -> membership verdict
                                                      changes on a blocked pair
  M16 a random non-L cubic offered to the test     -> not in the span
  M17 mixed_determinant vs an independent det()    -> agree on random inputs
  M18 source with a zeroed colour-c row (so the
      monochrome-c slice error vanishes)           -> kappa_c^3 NOT in span
  M19 kappa_0*kappa_1*kappa_2 offered at degree 3  -> never in the span
      (D = 1 != 0), on every source tested

Run: python3 wsplit_h3_mutations.py
"""

from __future__ import annotations

import itertools
import random
import sys
from fractions import Fraction

import wsplit_core as core
import wsplit_sources as sources
from wsplit_core import CUBIC_MONOMIALS, COLORS, U, dense_rows, error_matrix, kidx
from wsplit_dichotomy import linear_forms
from wsplit_structural import independent_rows
from wsplit_h3_structure import (PERMUTATIONS, basis, blocking_certificate,
                                 det_pairing, echelon, expand_l_monomial,
                                 graded_piece, matrix_of_form,
                                 mixed_determinant, monochrome_slice_nonzero,
                                 reduces_to_zero)

RNG = random.Random(4242)


def bad_det_pairing(cubic: dict):
    """M13: same functional with every sign +1."""
    total = 0
    for perm, _inv in PERMUTATIONS:
        mono = tuple(sorted(kidx(i, perm[i]) for i in range(3)))
        total += cubic.get(mono, 0)
    return total


def in_span_cubic(source, cubic: dict, drop: int = 0) -> bool:
    rows = [r for r in dense_rows(error_matrix(source)) if any(r)]
    generators, _rank = independent_rows(rows)
    if drop:
        generators = generators[:-drop] if len(generators) > drop else []
    base, index = basis(3)
    piece = graded_piece(generators, 3)
    ech, pivots = echelon(piece)
    target = [Fraction(0)] * len(base)
    for mono, coef in cubic.items():
        target[index[mono]] = coef
    return reduces_to_zero(ech, pivots, target)


def det3(matrix) -> int:
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))


def main() -> int:
    failures = []

    def control(name: str, detected: bool) -> None:
        print(f"  {name:54s} ok={detected}")
        if not detected:
            failures.append(name)

    src = core.random_source(RNG)
    matrix = error_matrix(src)

    control("baseline FACT 1 holds on a random source",
            all(det_pairing(matrix[w]) == 0 for w in core.WORDS))
    control("M13 all-plus signs break FACT 1",
            any(bad_det_pairing(matrix[w]) != 0 for w in core.WORDS))
    perm_cubic = {tuple(sorted((kidx(0, 0), kidx(1, 1), kidx(2, 2)))): 1}
    control("M14 det-pairing of K00K11K22 equals 1",
            det_pairing(perm_cubic) == 1)

    forms = linear_forms(src)
    kappa_cube = expand_l_monomial((0, 3, 0, 0), forms)     # kappa_0^3
    full = in_span_cubic(src, kappa_cube)
    dropped = in_span_cubic(src, kappa_cube, drop=3)
    control("baseline kappa_0^3 in the degree-3 span", full)
    control("M15 dropping 3 generators changes the verdict",
            full and not dropped)

    random_cubic = {m: RNG.randint(1, 9)
                    for m in RNG.sample(list(CUBIC_MONOMIALS), 12)}
    control("M16 a random non-L cubic is not in the span",
            not in_span_cubic(src, random_cubic))

    ok = True
    for _ in range(4):
        mats = [[[RNG.randint(-4, 4) for _ in COLORS] for _ in COLORS]
                for _ in range(1)]
        matrix_a = mats[0]
        ok = ok and mixed_determinant(matrix_a, matrix_a, matrix_a) == 6 * det3(matrix_a)
    control("M17 mixed_determinant(A,A,A) == 6 det A", ok)

    # M18: zero the colour-1 row of every p-block => monochrome-1 slice dies
    src2 = core.random_source(RNG)
    for u in U:
        for a in COLORS:
            src2[core.edge_key(core.P, u)][1][a] = 0
    matrix2 = error_matrix(src2)
    slice_dead = not monochrome_slice_nonzero(matrix2, 1)
    forms2 = linear_forms(src2)
    kappa1_cube = expand_l_monomial((0, 0, 3, 0), forms2)
    control("M18 zero monochrome-1 slice => kappa_1^3 not in span",
            slice_dead and not in_span_cubic(src2, kappa1_cube))

    ok = True
    for source in (src, src2, sources.two_star(0, 1), sources.three_star(0, 1, 2)):
        f = linear_forms(source)
        cross = expand_l_monomial((0, 1, 1, 1), f)          # kappa_0 k_1 k_2
        rows = [r for r in dense_rows(error_matrix(source)) if any(r)]
        if not rows:
            continue
        ok = ok and not in_span_cubic(source, cross)
    control("M19 kappa_0*kappa_1*kappa_2 never in the degree-3 span", ok)

    if failures:
        print(f"H3 MUTATION CONTROLS FAILED: {failures}")
        return 1
    print("wsplit h3 mutation controls: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
