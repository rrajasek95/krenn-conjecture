#!/usr/bin/env python3
"""Derive uniform full-cylinder rank minors on the E22 x00-open chart.

In the chart x00*t != 0, normalize x00=t=1 and leave the other eight
A23 entries symbolic.  The script forms the simultaneous-representation
matrix for the four cylinders C2,C3,C4,Cz.  Three literal duplicate columns
in C2 are omitted.  A rank-176 minor then proves that their common
intersection is at most a line; the direct matching tensor supplies that
line.
"""

from __future__ import annotations

import sympy as sp

import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


PARAMETER_BITS = tuple(range(1, 9))
PARAMETERS = sp.symbols("x01 x02 x10 x11 x12 x20 x21 x22")
OMIT_C2 = (9, 24, 39)


def symbolic_blocks(values):
    blocks = equations.cylinders.aggregate()
    blocks[2, 3] = {
        full.CELLS[0]: sp.Integer(1),
        **{
            full.CELLS[bit]: value
            for bit, value in zip(PARAMETER_BITS, values) if value != 0
        },
    }
    block25 = dict(blocks[2, 5])
    block25[2, 2] = sp.Integer(1)
    blocks[2, 5] = block25
    return blocks


def raw_columns(cut, blocks):
    five_sites = tuple(site for site in full.SIX if site != cut)
    columns = []
    for cut_colour in full.COLOURS:
        for hole in five_sites:
            rest = tuple(site for site in five_sites if site != hole)
            cofactor = equations.cylinders.matching_tensor(rest, blocks)
            for hole_colour in full.COLOURS:
                vector = {}
                for rest_word, coefficient in cofactor.items():
                    assignment = dict(zip(rest, rest_word))
                    assignment[hole] = hole_colour
                    assignment[cut] = cut_colour
                    equations.cylinders.add(
                        vector,
                        tuple(assignment[site] for site in full.SIX),
                        coefficient,
                    )
                columns.append(vector)
    assert len(columns) == 45
    return tuple(columns)


def representation_matrix(final_cut, values):
    blocks = symbolic_blocks(values)
    columns = {cut: raw_columns(cut, blocks) for cut in (2, 3, 4, final_cut)}
    assert all(columns[2][left] == columns[2][right]
               for left, right in ((7, 9), (22, 24), (37, 39)))
    selected2 = tuple(index for index in range(45) if index not in OMIT_C2)
    column_labels = tuple((2, index) for index in selected2) + tuple(
        (cut, index) for cut in (3, 4, final_cut) for index in range(45)
    )
    row_labels = tuple(
        (cut, word)
        for cut in (3, 4, final_cut)
        for word in sorted(set().union(
            *(set(column) for column in columns[2]),
            *(set(column) for column in columns[cut]),
        ))
    )
    matrix = sp.MutableSparseMatrix(len(row_labels), len(column_labels), {})
    row_index = {label: index for index, label in enumerate(row_labels)}
    for column_index, (cut, local_index) in enumerate(column_labels):
        if cut == 2:
            vector = columns[2][local_index]
            for comparison in (3, 4, final_cut):
                for word, coefficient in vector.items():
                    matrix[row_index[comparison, word], column_index] = coefficient
        else:
            for word, coefficient in columns[cut][local_index].items():
                matrix[row_index[cut, word], column_index] = -coefficient
    return sp.ImmutableSparseMatrix(matrix), row_labels, column_labels


def select_minor(matrix):
    numeric = matrix.subs(dict.fromkeys(PARAMETERS, 0))
    _rref, pivot_columns = numeric.rref()
    assert len(pivot_columns) == 176, len(pivot_columns)
    restricted = numeric[:, pivot_columns]
    _rref_t, pivot_rows = restricted.T.rref()
    assert len(pivot_rows) == 176, len(pivot_rows)
    return tuple(pivot_rows), tuple(pivot_columns)


def main():
    for final_cut in (0, 1, 5):
        matrix, row_labels, column_labels = representation_matrix(
            final_cut, PARAMETERS
        )
        rows, columns = select_minor(matrix)
        minor = matrix.extract(rows, columns)
        print(
            "MINOR", "cut", final_cut, "matrix", matrix.shape,
            "minor", minor.shape, "nonzeros", len(minor.todok()), flush=True,
        )
        determinant = sp.factor(minor.det(method="domain-ge"))
        print("DETERMINANT", "cut", final_cut, determinant, flush=True)
        print("ROW_SHA_INPUT", tuple(row_labels[index] for index in rows), flush=True)
        print("COLUMN_SHA_INPUT", tuple(column_labels[index] for index in columns), flush=True)


if __name__ == "__main__":
    main()
