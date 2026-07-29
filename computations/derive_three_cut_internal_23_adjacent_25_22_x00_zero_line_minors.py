#!/usr/bin/env python3
"""Derive cut-0/1 full-cylinder minors off the exceptional x00=0 locus.

Work with A25=E00+E22 and x00=0.  Outside the coordinate subspace
supported on {x01,x11,x21}, one of x02,x10,x12,x20,x22 is nonzero.
The five charts below take the first such entry, normalize it to one, and
leave every later/unrestricted A23 entry symbolic.  A constant nonzero
176-by-176 simultaneous-representation minor proves that the four-cylinder
intersection is the direct-tensor line throughout a chart for final cuts
0 and 1.  Final cut 5 is handled by the separate uniform ten-space proof.
"""

from __future__ import annotations

import argparse
import hashlib

import sympy as sp

import derive_three_cut_internal_23_adjacent_25_22_x00_open_line_minors as x00_open
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


OFF_EXCEPTIONAL_BITS = (2, 3, 5, 6, 8)
OMIT_C2 = x00_open.OMIT_C2


def chart_data(pivot_bit: int):
    """Return (forced-zero bits, symbolic bits, symbolic variables)."""
    pivot_index = OFF_EXCEPTIONAL_BITS.index(pivot_bit)
    zero_bits = (0,) + OFF_EXCEPTIONAL_BITS[:pivot_index]
    parameter_bits = tuple(
        bit for bit in range(1, 9)
        if bit != pivot_bit and bit not in zero_bits
    )
    parameters = sp.symbols(" ".join(full.CELL_NAMES[bit] for bit in parameter_bits))
    if not isinstance(parameters, tuple):
        parameters = (parameters,)
    return zero_bits, parameter_bits, parameters


def symbolic_blocks(pivot_bit: int, values):
    zero_bits, parameter_bits, _parameters = chart_data(pivot_bit)
    del zero_bits
    blocks = equations.cylinders.aggregate()
    blocks[2, 3] = {
        full.CELLS[pivot_bit]: sp.Integer(1),
        **{
            full.CELLS[bit]: value
            for bit, value in zip(parameter_bits, values) if value != 0
        },
    }
    block25 = dict(blocks[2, 5])
    block25[2, 2] = sp.Integer(1)
    blocks[2, 5] = block25
    return blocks


def representation_matrix(final_cut: int, pivot_bit: int, values):
    blocks = symbolic_blocks(pivot_bit, values)
    columns = {
        cut: x00_open.raw_columns(cut, blocks)
        for cut in (2, 3, 4, final_cut)
    }
    assert all(
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
    return sp.ImmutableSparseMatrix(matrix), row_labels, column_labels


def select_minor(matrix, parameters):
    numeric = matrix.subs(dict.fromkeys(parameters, 0))
    _rref, pivot_columns = numeric.rref()
    assert len(pivot_columns) == 176, len(pivot_columns)
    restricted = numeric[:, pivot_columns]
    _rref_t, pivot_rows = restricted.T.rref()
    assert len(pivot_rows) == 176, len(pivot_rows)
    return tuple(pivot_rows), tuple(pivot_columns)


def label_hash(row_labels, column_labels, rows, columns):
    payload = repr((
        tuple(row_labels[index] for index in rows),
        tuple(column_labels[index] for index in columns),
    ))
    return hashlib.sha256(payload.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pivot", choices=tuple(full.CELL_NAMES[bit] for bit in OFF_EXCEPTIONAL_BITS),
        action="append",
    )
    parser.add_argument("--cut", choices=(0, 1), type=int, action="append")
    args = parser.parse_args()
    selected_names = set(args.pivot or ())
    for pivot_bit in OFF_EXCEPTIONAL_BITS:
        if selected_names and full.CELL_NAMES[pivot_bit] not in selected_names:
            continue
        zero_bits, parameter_bits, parameters = chart_data(pivot_bit)
        print(
            "CHART", full.CELL_NAMES[pivot_bit],
            "zero", tuple(full.CELL_NAMES[bit] for bit in zero_bits),
            "parameters", tuple(full.CELL_NAMES[bit] for bit in parameter_bits),
            flush=True,
        )
        for final_cut in tuple(args.cut or (0, 1)):
            matrix, row_labels, column_labels = representation_matrix(
                final_cut, pivot_bit, parameters
            )
            rows, columns = select_minor(matrix, parameters)
            minor = matrix.extract(rows, columns)
            determinant = sp.factor(minor.det(method="domain-ge"))
            print(
                "MINOR", "pivot", full.CELL_NAMES[pivot_bit],
                "cut", final_cut, "matrix", matrix.shape,
                "minor", minor.shape, "nonzeros", len(minor.todok()),
                "det", determinant,
                "labels_sha256", label_hash(
                    row_labels, column_labels, rows, columns
                ),
                flush=True,
            )


if __name__ == "__main__":
    main()
