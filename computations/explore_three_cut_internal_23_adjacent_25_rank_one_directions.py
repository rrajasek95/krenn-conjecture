#!/usr/bin/env python3
"""Shared machinery for the rank-one adjacent directions E10 and E20.

For A25 = E00 + t*Ec0 with c in {1,2} the moving block stays rank one:
site 5 always receives colour 0.  The torus weight of t is then dependent,
wt(t) = wt(xc0) - wt(x00), so no chart can normalize t independently of the
A23 entries.  This module keeps t symbolic on the x00-open chart, records
the first-nonzero torus chart scheme, the three rank-one column relations
of every affected cylinder, and the exact degenerate locus

    D_full = V(t*x00 - x_c0, t*x02 - x_c2, x_other0, x_other2)
           = { A23 = v (x) r0 + m (x) e1 },  v = e0 + t*e_c,

on which the four-cylinder intersection for final cuts 0 and 1 becomes the
plane spanned by the direct tensor H and one explicit extra tensor.  The
proof machinery itself lives in
derive_three_cut_internal_23_adjacent_25_rank_one_w_structure; the torus
chart data recorded here is exploratory only and is not used by the
verifier.

This is exploration machinery, not a theorem certificate; the consolidated
verifier re-derives and checks everything it uses.
"""

from __future__ import annotations

import itertools

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


Q = full.Q
T = sp.Symbol("t")
X_SYMBOLS = tuple(
    sp.Symbol(f"x{a}{b}") for a, b in full.CELLS
)
OMIT_C2 = (9, 24, 39)
ACTIVE = (0, 1)
EXCEPTIONAL_BITS = (1, 4, 7)
H_PROBE = (1, 2, 1, 2, 0, 0)

DIRECTIONS = {
    "10": {
        "t_cell": (1, 0),
        "moved_colour": 1,
        "x_bit": 3,
        "rescue_bits": (2, 5, 6, 8),
        "deficient_pair": (1, 4),
        "d_word": (2, 2, 1, 2, 2, 0),
    },
    "20": {
        "t_cell": (2, 0),
        "moved_colour": 2,
        "x_bit": 6,
        "rescue_bits": (2, 3, 5, 8),
        "deficient_pair": (1, 7),
        "d_word": (2, 2, 2, 2, 2, 0),
    },
}


def select_direction(key):
    spec = DIRECTIONS[key]
    adjacent.T_CELL = spec["t_cell"]
    adjacent.T_BLOCK, adjacent.T_DETAILS = adjacent.variable_coordinate_block(
        adjacent.T_EDGE, spec["t_cell"]
    )
    return spec


def chart_cell_values(chart_bit):
    """First-nonzero chart: earlier cells zero, pivot one, later symbolic.

    On chart 0 the parameter t stays symbolic; on every other chart the
    residual torus normalizes t to one (each pair (x_row_b, t_row) has
    rank two), so t is literally 1 there.
    """
    values = {}
    for bit in range(9):
        if bit < chart_bit:
            values[bit] = sp.Integer(0)
        elif bit == chart_bit:
            values[bit] = sp.Integer(1)
        else:
            values[bit] = X_SYMBOLS[bit]
    t_value = T if chart_bit == 0 else sp.Integer(1)
    return values, t_value


def blocks_for_values(key, cell_values, t_value):
    spec = DIRECTIONS[key]
    blocks = equations.cylinders.aggregate()
    blocks[2, 3] = {
        full.CELLS[bit]: value
        for bit, value in cell_values.items() if value != 0
    }
    block25 = dict(blocks[2, 5])
    if t_value != 0:
        block25[spec["t_cell"]] = (
            block25.get(spec["t_cell"], sp.Integer(0)) + t_value
        )
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


def representation_matrix(final_cut, blocks):
    columns = {cut: raw_columns(cut, blocks) for cut in (2, 3, 4, final_cut)}
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


def local_index(cut, cut_colour, hole, hole_colour):
    five_sites = tuple(site for site in full.SIX if site != cut)
    return 15 * cut_colour + 3 * five_sites.index(hole) + hole_colour


def kernel_witnesses(key, cut, t_value):
    """Three exact column relations of the raw cylinder map at cut.

    Each relation replaces the site-2 insertion of v = e0 + t*e_c by the
    unique fixed-cell expansions producing the same tensor; the three
    relations live in disjoint cut-colour blocks, so the identity minor on
    their private columns certifies independence for every parameter value.
    """
    moved = DIRECTIONS[key]["moved_colour"]
    witnesses = []
    for cut_colour in full.COLOURS:
        vector = {}
        if cut == 3:
            vector[local_index(cut, cut_colour, 2, 0)] = -sp.Integer(1)
            vector[local_index(cut, cut_colour, 2, moved)] = -t_value
            vector[local_index(cut, cut_colour, 4, 0)] = sp.Integer(1)
            private = local_index(cut, cut_colour, 4, 0)
        elif cut == 4:
            vector[local_index(cut, cut_colour, 2, 0)] = -sp.Integer(1)
            vector[local_index(cut, cut_colour, 2, moved)] = -t_value
            vector[local_index(cut, cut_colour, 3, 1)] = sp.Integer(1)
            private = local_index(cut, cut_colour, 3, 1)
        elif cut == 0:
            vector[local_index(cut, cut_colour, 2, 0)] = -sp.Integer(1)
            vector[local_index(cut, cut_colour, 2, moved)] = -t_value
            vector[local_index(cut, cut_colour, 3, 1)] = sp.Integer(1)
            vector[local_index(cut, cut_colour, 4, 0)] = sp.Integer(1)
            private = local_index(cut, cut_colour, 4, 0)
        elif cut == 1:
            vector[local_index(cut, cut_colour, 2, 0)] = sp.Integer(1)
            vector[local_index(cut, cut_colour, 2, moved)] = t_value
            vector[local_index(cut, cut_colour, 3, 1)] = -sp.Integer(1)
            vector[local_index(cut, cut_colour, 4, 0)] = sp.Integer(1)
            private = local_index(cut, cut_colour, 4, 0)
        else:
            raise ValueError(cut)
        witnesses.append((vector, private))
    return witnesses


def verify_kernel_witnesses(key, cut, blocks, t_value):
    columns = raw_columns(cut, blocks)
    privates = set()
    for vector, private in kernel_witnesses(key, cut, t_value):
        accumulated = {}
        for index, coefficient in vector.items():
            for word, value in columns[index].items():
                equations.cylinders.add(
                    accumulated, word, sp.expand(coefficient * value)
                )
        residual = {
            word: sp.expand(value)
            for word, value in accumulated.items() if sp.expand(value) != 0
        }
        assert not residual, (key, cut, residual)
        assert vector[private] == 1 or vector[private] == sp.Integer(1)
        privates.add(private)
    assert len(privates) == 3
    return privates


def direct_representation(cut, blocks, columns):
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
                    for word, value in columns[index].items():
                        equations.cylinders.add(
                            answer, word, coefficient * value
                        )
                index += 1
    assert index == 45
    return {
        word: sp.expand(value) for word, value in answer.items()
        if sp.expand(value) != 0
    }


def d_locus_generators(key, cell_values, t_value):
    """Generators of the degenerate locus D_full inside a chart.

    D_full is the set of A23 lying in v (x) C^3 + C^3 (x) e1 with
    v = e0 + t*e_c: both the 0-column pair and the 2-column pair of the
    rows (0, c) align with v, and the remaining row vanishes outside the
    middle column.
    """
    spec = DIRECTIONS[key]
    moved = spec["moved_colour"]
    other = 3 - moved
    generators = [
        t_value * cell_values[0] - cell_values[3 * moved],
        t_value * cell_values[2] - cell_values[3 * moved + 2],
        cell_values[3 * other],
        cell_values[3 * other + 2],
    ]
    return [sp.expand(generator) for generator in generators]


def d_plane_tensor(key, t_value):
    """The extra plane generator on D for final cuts 0 and 1."""
    tensor = {
        (1, 1, 1, 1, 1, 0): sp.Integer(1),
        (1, 2, 1, 2, 0, 0): sp.Integer(1),
        (2, 2, 0, 2, 2, 0): sp.Integer(1),
    }
    tensor[DIRECTIONS[key]["d_word"]] = t_value
    return tensor


def stabilizer_data(key):
    fixed = (
        ((0, 1), (0, 0)), ((4, 5), (0, 0)),
        ((0, 2), (1, 1)), ((1, 4), (1, 1)),
        ((0, 4), (2, 2)), ((1, 3), (2, 2)),
        ((2, 5), (0, 0)), ((3, 5), (1, 0)),
    )
    constraints = sp.Matrix.vstack(*(
        adjacent.cell_weight(edge, cell) for edge, cell in fixed
    ))
    assert constraints.rank() == 8
    kernel = sp.Matrix.hstack(*constraints.nullspace())
    assert kernel.shape == (18, 10)
    x_rows = tuple(
        adjacent.cell_weight((2, 3), cell) * kernel for cell in full.CELLS
    )
    t_row = adjacent.cell_weight((2, 5), DIRECTIONS[key]["t_cell"]) * kernel
    return x_rows, t_row


def torus_cover_audit(key):
    """Chart scheme and D normalizations for one direction.

    * every single cell character is nontrivial: first-nonzero charts cover
      every nonzero A23;
    * every (pivot, t) pair is independent: charts 1..8 normalize t = 1;
    * the dependence wt(t) = wt(x_move) - wt(x00) holds exactly;
    * on D the five relevant characters have rank four with the recorded
      relation, so supports off the deficient pair normalize to exact
      points and the deficient supports keep exactly one modulus.
    """
    spec = DIRECTIONS[key]
    x_rows, t_row = stabilizer_data(key)
    assert sp.Matrix.vstack(*x_rows).rank() == 5
    assert t_row.rank() == 1
    for bit in range(9):
        assert x_rows[bit].rank() == 1
        assert sp.Matrix.vstack(x_rows[bit], t_row).rank() == 2
    dependence = t_row - x_rows[spec["x_bit"]] + x_rows[0]
    assert dependence.is_zero_matrix
    base = (x_rows[0], x_rows[spec["x_bit"]])
    assert sp.Matrix.vstack(*base).rank() == 2
    for size in (1, 2, 3):
        for support in itertools.combinations(EXCEPTIONAL_BITS, size):
            rows = list(base) + [x_rows[bit] for bit in support]
            expected = 2 + size
            if set(spec["deficient_pair"]) <= set(support):
                expected -= 1
            assert sp.Matrix.vstack(*rows).rank() == expected, (key, support)
            rows_b = [t_row] + [x_rows[bit] for bit in support]
            expected_b = 1 + size
            if set(spec["deficient_pair"]) <= set(support):
                expected_b -= 1
            assert sp.Matrix.vstack(*rows_b).rank() == expected_b, (key, support)
    counts = tuple(1 << (8 - bit) for bit in range(9))
    assert sum(counts) == 511
    return counts


def main():
    for key in ("10", "20"):
        spec = select_direction(key)
        adjacent.no_mixed_x_t_terms()
        counts = torus_cover_audit(key)
        print(
            "DIRECTION", key, "t_cell", spec["t_cell"],
            "chart_support_counts", counts,
            "t_block", len(adjacent.T_BLOCK),
        )
        for chart_bit in range(9):
            cell_values, t_value = chart_cell_values(chart_bit)
            blocks = blocks_for_values(key, cell_values, t_value)
            for cut in (0, 1, 3, 4):
                verify_kernel_witnesses(key, cut, blocks, t_value)
            hs = equations.cylinders.matching_tensor(full.SIX, blocks)
            probe = sp.expand(hs.get(H_PROBE, 0))
            assert probe == 1, (key, chart_bit, probe)
            print(
                " chart", full.CELL_NAMES[chart_bit],
                "witnesses cuts 0,1,3,4 exact; H probe", probe,
                "D generators", d_locus_generators(key, cell_values, t_value),
            )


if __name__ == "__main__":
    main()
