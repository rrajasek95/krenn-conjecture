#!/usr/bin/env python3
"""Uniform full-cylinder proof that the E22 final-cut-5 normal is a line.

Normalize the E22 coefficient on edge 25 to one and leave all nine entries
of A23 symbolic.  The intersection C2 cap C3 is the fixed ten-space W
spanned by the nine words (0,0,a,b,0,0) and a fixed four-word tail.  A
constant rank-77 minor proves there is no additional vector in C2 cap C3.

On the ten probe coordinates consisting of those nine words and
(1,2,1,2,0,0), exactly one raw C5 column is nonzero.  Its restriction is
(x00,...,x22,1).  Thus a vector in W cap C5 must be a scalar multiple of
the full direct matching tensor.  This avoids all rank jumps in the raw C5
presentation and proves C2 cap C3 cap C5 is that line for every A23.
"""

from __future__ import annotations

import hashlib

import sympy as sp

import derive_three_cut_internal_23_adjacent_25_22_x00_open_line_minors as raw
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


PARAMETERS = sp.symbols("x00 x01 x02 x10 x11 x12 x20 x21 x22")
OMIT_C2 = raw.OMIT_C2
E_WORDS = tuple((0, 0, a, b, 0, 0) for a, b in full.CELLS)
TAIL_PROBE = (1, 2, 1, 2, 0, 0)


def symbolic_blocks():
    blocks = equations.cylinders.aggregate()
    blocks[2, 3] = {
        cell: parameter for cell, parameter in zip(full.CELLS, PARAMETERS)
    }
    block25 = dict(blocks[2, 5])
    block25[2, 2] = sp.Integer(1)
    blocks[2, 5] = block25
    return blocks


def add_scaled(target, source, scalar):
    for word, coefficient in source.items():
        equations.cylinders.add(target, word, scalar * coefficient)


def direct_representation(cut, blocks, columns):
    """Expand H by the edge incident to cut in the ordered raw columns."""
    five_sites = tuple(site for site in full.SIX if site != cut)
    answer = {}
    index = 0
    for cut_colour in full.COLOURS:
        for hole in five_sites:
            edge = tuple(sorted((cut, hole)))
            for hole_colour in full.COLOURS:
                cell = (
                    (cut_colour, hole_colour)
                    if cut < hole else (hole_colour, cut_colour)
                )
                coefficient = blocks.get(edge, {}).get(cell, 0)
                if coefficient:
                    add_scaled(answer, columns[index], coefficient)
                index += 1
    assert index == 45
    return answer


def two_cylinder_matrix(blocks):
    columns2 = raw.raw_columns(2, blocks)
    columns3 = raw.raw_columns(3, blocks)
    assert all(
        columns2[left] == columns2[right]
        for left, right in ((7, 9), (22, 24), (37, 39))
    )
    selected2 = tuple(index for index in range(45) if index not in OMIT_C2)
    column_labels = tuple((2, index) for index in selected2) + tuple(
        (3, index) for index in range(45)
    )
    row_labels = tuple(sorted(
        set().union(*(set(column) for column in columns2 + columns3))
    ))
    row_index = {word: index for index, word in enumerate(row_labels)}
    matrix = sp.MutableSparseMatrix(len(row_labels), len(column_labels), {})
    for column_index, (cut, local_index) in enumerate(column_labels):
        vector = (columns2 if cut == 2 else columns3)[local_index]
        sign = 1 if cut == 2 else -1
        for word, coefficient in vector.items():
            matrix[row_index[word], column_index] = sign * coefficient
    return (
        sp.ImmutableSparseMatrix(matrix), row_labels, column_labels,
        columns2, columns3,
    )


def select_minor(matrix):
    numeric = matrix.subs(dict.fromkeys(PARAMETERS, 0))
    _rref, pivot_columns = numeric.rref()
    assert len(pivot_columns) == 77, len(pivot_columns)
    restricted = numeric[:, pivot_columns]
    _rref_t, pivot_rows = restricted.T.rref()
    assert len(pivot_rows) == 77, len(pivot_rows)
    return tuple(pivot_rows), tuple(pivot_columns)


def tail_and_direct_tensor(blocks):
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    zero_blocks = symbolic_blocks()
    zero_blocks[2, 3] = {}
    tail = equations.cylinders.matching_tensor(full.SIX, zero_blocks)
    expected = dict(tail)
    for word, parameter in zip(E_WORDS, PARAMETERS):
        equations.cylinders.add(expected, word, parameter)
    assert hs == expected
    assert tail[TAIL_PROBE] == 1
    assert not set(E_WORDS) & set(tail)
    return tail, hs


def audit_common_ten_space(blocks, tail, hs, columns2, columns3):
    # The nine coordinate vectors are literal raw columns in both cylinders.
    hits = {}
    for cut, columns in ((2, columns2), (3, columns3)):
        hits[cut] = []
        for word in E_WORDS:
            unit = {word: 1}
            indices = tuple(index for index, column in enumerate(columns) if column == unit)
            assert indices
            hits[cut].append(indices[0])
        assert direct_representation(cut, blocks, columns) == hs

    # Since H and all coordinate vectors are common, subtracting their
    # symbolic combination shows the fixed tail is common as well.
    reconstructed_tail = dict(hs)
    for word, parameter in zip(E_WORDS, PARAMETERS):
        equations.cylinders.add(reconstructed_tail, word, -parameter)
    assert reconstructed_tail == tail
    return hits


def audit_cut5_probe(blocks, hs):
    columns5 = raw.raw_columns(5, blocks)
    assert direct_representation(5, blocks, columns5) == hs
    probe = E_WORDS + (TAIL_PROBE,)
    restrictions = tuple(
        {word: column[word] for word in probe if word in column}
        for column in columns5
    )
    nonzero = tuple(index for index, value in enumerate(restrictions) if value)
    assert nonzero == (12,), nonzero
    expected = {
        **{word: parameter for word, parameter in zip(E_WORDS, PARAMETERS)},
        TAIL_PROBE: sp.Integer(1),
    }
    assert restrictions[12] == expected
    return nonzero, expected


def main():
    blocks = symbolic_blocks()
    tail, hs = tail_and_direct_tensor(blocks)
    matrix, row_labels, column_labels, columns2, columns3 = two_cylinder_matrix(
        blocks
    )
    rows, columns = select_minor(matrix)
    minor = matrix.extract(rows, columns)
    determinant = sp.factor(minor.det(method="domain-ge"))
    assert determinant in (1, -1), determinant
    labels_payload = repr((
        tuple(row_labels[index] for index in rows),
        tuple(column_labels[index] for index in columns),
    ))
    hits = audit_common_ten_space(blocks, tail, hs, columns2, columns3)
    nonzero, _expected = audit_cut5_probe(blocks, hs)
    print(
        "C2_C3_TEN_SPACE", f"matrix={matrix.shape}",
        f"minor={minor.shape}", f"nonzeros={len(minor.todok())}",
        f"det={determinant}",
        "labels_sha256=" + hashlib.sha256(labels_payload.encode()).hexdigest(),
    )
    print("E_WORD_COLUMN_HITS", hits)
    print(
        "C5_PROBE", "coordinates=10", f"nonzero_columns={nonzero}",
        "column12=(x00,x01,x02,x10,x11,x12,x20,x21,x22,1)",
    )
    print("CUT5_NORMAL_LINE all_A23=1 direct_tensor_nonzero=1")


if __name__ == "__main__":
    main()
