#!/usr/bin/env python3
"""Feasibility of symbolic-t full-cylinder minors for A25 = E00 + t*E10/E20.

For the two dependent-weight directions E10 and E20 the torus does not
normalize t independently of the A23 entries, so the E22 chart scheme
(normalize x00 = t = 1) is unavailable.  This script tests the symbolic-t
alternative on the x00-open chart: normalize x00 = 1 only, keep the other
eight A23 entries AND t symbolic, and ask whether the simultaneous
representation matrix for cylinders C2, C3, C4, C_z still admits a
full-rank minor with constant determinant +-1 over Q[x.., t].

A constant unit determinant here is a parameter-uniform certificate: it
covers every complex t (including t = 0 and the cross-ratio modulus) at
once.  This is a reconnaissance script, not a theorem certificate.
"""

from __future__ import annotations

import argparse

import sympy as sp

import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


PARAMETER_BITS = tuple(range(1, 9))
X_PARAMETERS = sp.symbols("x01 x02 x10 x11 x12 x20 x21 x22")
T = sp.Symbol("t")
ALL_PARAMETERS = X_PARAMETERS + (T,)
OMIT_C2 = (9, 24, 39)
DIRECTIONS = {"10": (1, 0), "20": (2, 0)}


def symbolic_blocks(t_cell):
    blocks = equations.cylinders.aggregate()
    blocks[2, 3] = {
        full.CELLS[0]: sp.Integer(1),
        **{
            full.CELLS[bit]: symbol
            for bit, symbol in zip(PARAMETER_BITS, X_PARAMETERS)
        },
    }
    block25 = dict(blocks[2, 5])
    block25[t_cell] = block25.get(t_cell, sp.Integer(0)) + T
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


def representation_matrix(final_cut, t_cell):
    blocks = symbolic_blocks(t_cell)
    columns = {cut: raw_columns(cut, blocks) for cut in (2, 3, 4, final_cut)}
    duplicates_ok = all(
        columns[2][left] == columns[2][right]
        for left, right in ((7, 9), (22, 24), (37, 39))
    )
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
    return sp.ImmutableSparseMatrix(matrix), row_labels, column_labels, duplicates_ok


def select_minor(matrix, t_value):
    anchor = dict.fromkeys(X_PARAMETERS, 0)
    anchor[T] = t_value
    numeric = matrix.subs(anchor)
    _rref, pivot_columns = numeric.rref()
    restricted = numeric[:, pivot_columns]
    _rref_t, pivot_rows = restricted.T.rref()
    return tuple(pivot_rows), tuple(pivot_columns)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directions", default="10,20")
    parser.add_argument("--cuts", default="0,1,5")
    parser.add_argument("--skip-det", action="store_true")
    arguments = parser.parse_args()
    for key in arguments.directions.split(","):
        t_cell = DIRECTIONS[key]
        for final_cut in tuple(int(cut) for cut in arguments.cuts.split(",")):
            matrix, row_labels, column_labels, duplicates_ok = (
                representation_matrix(final_cut, t_cell)
            )
            rows, columns = select_minor(matrix, 1)
            print(
                "FEASIBILITY", "direction", key, "cut", final_cut,
                "matrix", matrix.shape,
                "c2_duplicates_ok", duplicates_ok,
                "t1_rank", len(columns), "row_pivots", len(rows),
                flush=True,
            )
            if len(rows) != len(columns) or arguments.skip_det:
                continue
            minor = matrix.extract(rows, columns)
            determinant = sp.factor(minor.det(method="domain-ge"))
            print(
                "DETERMINANT", "direction", key, "cut", final_cut,
                "minor", minor.shape, "nonzeros", len(minor.todok()),
                "det", determinant, flush=True,
            )


if __name__ == "__main__":
    main()
