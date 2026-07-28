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
