#!/usr/bin/env python3
"""Reconnaissance: the two-parameter rank-one slice A25 = E00 + t*E10 + s*E20.

The moving block (e0 + t*e1 + s*e2) (x) e0 is still rank one, so the whole
chart-free W-structure of the single-direction theorem is expected to
generalize: combined three-term kernel relations, a constant unit
72-minor for C2/C3 over Q[t, s], and the tail identity

    H = sum x_ab e_ab + D(t, s),
    D(t, s) = [111110] + [121200] + [220220] + t[221220] + s[222220].

This script verifies exactly those three facts.  It is reconnaissance for
the next theorem after the E10/E20 closure, not a certificate: the probe
arguments, the D-in-C4 characterization of the degenerate locus, and the
Q[x.., t, s] star packets remain to be built.

Further recorded reconnaissance (exact, run separately):

* the probe tables match the single-direction pattern exactly: cuts 0, 1
  have no sigma-word hits and only column 0 on the e-words; cut 5 has
  exactly columns 12, 13, 14 with the same restrictions;
* D(t, s) keeps the same two-column representations col19+col41 in C0
  and col25+col38 in C1;
* six 43-minors of [C4 | D(t, s)] factor as
  x10^6 (t x00 - x10)^3, -x12^6 (t x02 - x12)^3,
  -x20^6 (s x00 - x20)^3, x22^6 (s x02 - x22)^3,
  x00^6 (t x00 - x10)^3, -x02^6 (t x02 - x12)^3,
  so the candidate degenerate locus is
  V(t x00 - x10, t x02 - x12, s x00 - x20, s x02 - x22) - both moved
  rows aligned with v - whose s = 0 slice is the E10 locus; more
  anchors are needed for full radical coverage of mixed alignment
  patterns;
* on the locus X = v (x) r0 + m (x) e1 (m = (0, w1, w2) spread over
  rows 1, 2), D(t, s) is in C4 with coefficients
  {6: -a1, 7: -a1 t - w1, 8: -a1 s - w2, 9: -a0, 11: -a2,
   12: 1, 19: 1, 32: 1}, unifying both single-direction
  representations;
* the W members have the unified representations
  sigma1 = col9 + t col23 + s col37, sigma2 = col10 + t col24 + s col38,
  D = col11 + col15 + t col25 + s col39 in C2 (retained-column indexing)
  and sigma1 = col25, sigma2 = col26, D = col27 + col35 in C3;
* ten [C4|D] anchors (six one-cell, four mixed such as {x00, x10} and
  {x02, x22}) yield determinants covering all four locus generators, and
  the four Rabinowitsch radical checks
  1 in (dets, 1 - y g) over Q[x.., t, s, y] are all unit, so
  V(dets) lies inside V(t x00 - x10, t x02 - x12, s x00 - x20,
  s x02 - x22) with no residual component.

With these, every geometric certificate of the slice theorem is verified;
only the Q[x.., t, s] star packets (line, split for Groebner time, and the
seven-parameter plane packet) remain to be run before a verifier and note
can be assembled.
"""

from __future__ import annotations

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_rank_one_directions as rankone
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


T = rankone.T
S = sp.Symbol("s")
X9 = tuple(sp.Symbol(f"x{a}{b}") for a, b in full.CELLS)


def blocks_ts(with_x=True):
    blocks = equations.cylinders.aggregate()
    if with_x:
        blocks[2, 3] = {cell: X9[bit] for bit, cell in enumerate(full.CELLS)}
    else:
        blocks[2, 3] = {}
    block25 = dict(blocks[2, 5])
    block25[1, 0] = block25.get((1, 0), sp.Integer(0)) + T
    block25[2, 0] = block25.get((2, 0), sp.Integer(0)) + S
    blocks[2, 5] = block25
    return blocks


def combined_kernel_relations():
    blocks = blocks_ts()
    for cut, extra in ((3, (4, 0)), (4, (3, 1))):
        columns = rankone.raw_columns(cut, blocks)
        five = tuple(site for site in range(6) if site != cut)

        def index(a, hole, colour):
            return 15 * a + 3 * five.index(hole) + colour

        for a in range(3):
            accumulated = {}
            combination = {
                index(a, 2, 0): -sp.Integer(1),
                index(a, 2, 1): -T,
                index(a, 2, 2): -S,
                index(a, extra[0], extra[1]): sp.Integer(1),
            }
            for j, coefficient in combination.items():
                for word, value in columns[j].items():
                    equations.cylinders.add(
                        accumulated, word, sp.expand(coefficient * value)
                    )
            residual = {
                word: sp.expand(value)
                for word, value in accumulated.items() if sp.expand(value) != 0
            }
            assert not residual, (cut, a, residual)
    return True


def two_cylinder_minor():
    columns2 = tuple(
        column for i, column in enumerate(
            rankone.raw_columns(2, blocks_ts(False))
        ) if i not in rankone.OMIT_C2
    )
    columns3 = rankone.raw_columns(3, blocks_ts(False))
    words = sorted(set().union(*(set(c) for c in columns2 + columns3)))
    index = {word: i for i, word in enumerate(words)}
    matrix = sp.MutableSparseMatrix(len(words), 87, {})
    for j, column in enumerate(columns2):
        for word, value in column.items():
            matrix[index[word], j] = value
    for j, column in enumerate(columns3):
        for word, value in column.items():
            matrix[index[word], 42 + j] = -value
    matrix = sp.ImmutableSparseMatrix(matrix)
    numeric = matrix.subs({T: 1, S: 1})
    _rref, pivot_columns = numeric.rref()
    restricted = numeric[:, pivot_columns]
    _rref_t, pivot_rows = restricted.T.rref()
    minor = matrix.extract(tuple(pivot_rows), tuple(pivot_columns))
    determinant = sp.factor(minor.det(method="domain-ge"))
    assert len(pivot_columns) == 72
    assert determinant in (1, -1), determinant
    return determinant


def d_plane_tensor_ts():
    return {
        (1, 1, 1, 1, 1, 0): sp.Integer(1),
        (1, 2, 1, 2, 0, 0): sp.Integer(1),
        (2, 2, 0, 2, 2, 0): sp.Integer(1),
        (2, 2, 1, 2, 2, 0): T,
        (2, 2, 2, 2, 2, 0): S,
    }


def tail_identity():
    tensor = equations.cylinders.matching_tensor(full.SIX, blocks_ts())
    tensor = {
        word: sp.expand(value) for word, value in tensor.items()
        if sp.expand(value) != 0
    }
    expected = dict(d_plane_tensor_ts())
    for bit, cell in enumerate(full.CELLS):
        a, b = cell
        equations.cylinders.add(expected, (0, 0, a, b, 0, 0), X9[bit])
    expected = {
        word: sp.expand(value) for word, value in expected.items()
        if sp.expand(value) != 0
    }
    assert tensor == expected
    return True


def main():
    print("combined_kernel_relations", combined_kernel_relations(), flush=True)
    print("two_cylinder_72_minor_det", two_cylinder_minor(), flush=True)
    print("tail_identity", tail_identity(), flush=True)


if __name__ == "__main__":
    main()
