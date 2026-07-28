#!/usr/bin/env python3
"""Uniform W-structure certificates for the rank-one directions E10/E20.

For A25 = E00 + t*Ec0 (c = 1 for E10, c = 2 for E20) with all nine A23
entries and t polynomial variables, this module derives and re-verifies:

* neither C2 nor C3 involves A23, so W := C2 cap C3 is computed over Q[t];
* a constant 72x72 unit minor of the simultaneous C2/C3 representation
  matrix bounds dim W <= 12 for every complex t;
* twelve explicit members - the nine coordinate tensors e_ab = [00ab00],
  two sigma tails, and the plane tensor D - with exact representations in
  both cylinders and a constant unit independence minor, so W equals their
  span for every t;
* the tail identity H = sum x_ab e_ab + D;
* probe restriction tables proving W cap C5 = <H> and
  W cap C0 = W cap C1 = <H, D> for every X, t;
* the exact characterization D in C4  <=>  (X, t) in D_full, where

      D_full = V(t*x00 - x_move0, t*x02 - x_move2, x_other0, x_other2)

  via factored 43-minor determinants of [C4 | D] with radical-membership
  certificates and an explicit on-locus representation over the linear
  parameterization A23 = v (x) r0 + m (x) e1, v = e0 + t*e_c.

Since the four-cylinder intersection for a final cut z is literally
(W cap C_z) cap C4 and H lies in every cylinder, these facts give

    C2 cap C3 cap C4 cap C5 = <H>                       for all X, t;
    C2 cap C3 cap C4 cap C_z = <H>          (z = 0, 1)  off D_full;
    C2 cap C3 cap C4 cap C_z = <H, D>       (z = 0, 1)  on  D_full;

with no torus normalization, no charts, and no t != 0 restriction.
"""

from __future__ import annotations

import itertools

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_rank_one_directions as rankone
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


T = rankone.T
X9 = tuple(sp.Symbol(f"x{a}{b}") for a, b in full.CELLS)
A0, A1, A2, WSYM, USYM = sp.symbols("a0 a1 a2 w u")
OMIT_C2 = rankone.OMIT_C2
E_WORDS = tuple((0, 0, a, b, 0, 0) for a, b in full.CELLS)

# Probe words: the nine e-coordinates, the two-word supports of the sigma
# tails (leading words first), the D lead word, and the two C5 kill words.
SIGMA_LEAD = ((0, 0, 0, 1, 1, 0), (0, 0, 0, 1, 2, 0))
D_LEAD = (1, 2, 1, 2, 0, 0)
KILL_WORDS = ((1, 2, 1, 2, 1, 0), (1, 2, 1, 2, 2, 0))

# Exact membership representations (verified, not assumed, by the checks
# below).  C2 indices refer to the 42 retained columns after OMIT_C2.
MEMBERSHIPS = {
    "10": {
        "sigma1": {"C2": {9: 1, 23: "t"}, "C3": {25: 1}},
        "sigma2": {"C2": {10: 1, 24: "t"}, "C3": {26: 1}},
        "D": {
            "C2": {11: 1, 15: 1, 25: "t"},
            "C3": {27: 1, 35: 1},
            "C0": {19: 1, 41: 1},
            "C1": {25: 1, 38: 1},
        },
        "D_in_C4_on_locus": {
            6: -A1, 7: -A1 * T - WSYM, 8: -USYM,
            9: -A0, 11: -A2, 12: 1, 19: 1, 32: 1,
        },
    },
    "20": {
        "sigma1": {"C2": {9: 1, 37: "t"}, "C3": {25: 1}},
        "sigma2": {"C2": {10: 1, 38: "t"}, "C3": {26: 1}},
        "D": {
            "C2": {11: 1, 15: 1, 39: "t"},
            "C3": {27: 1, 35: 1},
            "C0": {19: 1, 41: 1},
            "C1": {25: 1, 38: 1},
        },
        "D_in_C4_on_locus": {
            6: -A1, 7: -USYM, 8: -A1 * T - WSYM,
            9: -A0, 11: -A2, 12: 1, 19: 1, 32: 1,
        },
    },
}

# [C4 | D] anchor points (symbol -> value, all others zero) and the
# expected factored determinants of the derived 43x43 minors.
C4_ANCHORS = {
    "10": (
        ({3: 1}, "x10**6*(t*x00 - x10)**3"),
        ({5: 1}, "-x12**6*(t*x02 - x12)**3"),
        ({6: 1}, "x20**9"),
        ({8: 1}, "-x22**9"),
        ({0: 1}, "x00**6*(t*x00 - x10)**3"),
        ({2: 1}, "-x02**6*(t*x02 - x12)**3"),
    ),
    "20": (
        ({6: 1}, "-x20**6*(t*x00 - x20)**3"),
        ({8: 1}, "x22**6*(t*x02 - x22)**3"),
        ({3: 1}, "-x10**9"),
        ({5: 1}, "x12**9"),
        ({0: 1}, "-x00**6*(t*x00 - x20)**3"),
        ({2: 1}, "x02**6*(t*x02 - x22)**3"),
    ),
}


def d_full_generators(key):
    spec = rankone.DIRECTIONS[key]
    xb = spec["x_bit"]
    if key == "10":
        others = (6, 8)
        aligned = (3, 5)
    else:
        others = (3, 5)
        aligned = (6, 8)
    assert aligned[0] == xb
    return (
        T * X9[0] - X9[aligned[0]],
        T * X9[2] - X9[aligned[1]],
        X9[others[0]],
        X9[others[1]],
    )


def nine_symbol_blocks(key):
    spec = rankone.DIRECTIONS[key]
    blocks = equations.cylinders.aggregate()
    blocks[2, 3] = {cell: X9[bit] for bit, cell in enumerate(full.CELLS)}
    block25 = dict(blocks[2, 5])
    block25[spec["t_cell"]] = (
        block25.get(spec["t_cell"], sp.Integer(0)) + T
    )
    blocks[2, 5] = block25
    return blocks


def d_full_blocks(key):
    """Blocks on the linear parameterization of D_full."""
    spec = rankone.DIRECTIONS[key]
    moved = spec["moved_colour"]
    cells = {}
    for j, parameter in enumerate((A0, A1, A2)):
        cells[0, j] = parameter
        cells[moved, j] = T * parameter
    cells[moved, 1] = cells[moved, 1] + WSYM
    cells[3 - moved, 1] = USYM
    cell_values = {
        bit: sp.expand(cells.get(full.CELLS[bit], 0)) for bit in range(9)
    }
    return rankone.blocks_for_values(key, cell_values, T)


def d_full_parameterization_matches(key):
    """The parameterization image is exactly V(d_full_generators)."""
    blocks = d_full_blocks(key)
    entries = {
        X9[bit]: blocks[2, 3].get(cell, sp.Integer(0))
        for bit, cell in enumerate(full.CELLS)
    }
    for generator in d_full_generators(key):
        assert sp.expand(generator.subs(entries)) == 0, (key, generator)
    # conversely the free coordinates recover the parameters linearly
    spec = rankone.DIRECTIONS[key]
    moved = spec["moved_colour"]
    solved = {
        A0: entries[X9[0]], A1: entries[X9[1]], A2: entries[X9[2]],
        USYM: entries[X9[3 * (3 - moved) + 1]],
        WSYM: entries[X9[3 * moved + 1]] - T * entries[X9[1]],
    }
    for symbol, value in solved.items():
        assert sp.expand(value - symbol) == 0, (key, symbol, value)


def sigma_tensors(key):
    moved = rankone.DIRECTIONS[key]["moved_colour"]
    sigma1 = {(0, 0, 0, 1, 1, 0): sp.Integer(1), (0, 0, moved, 1, 1, 0): T}
    sigma2 = {(0, 0, 0, 1, 2, 0): sp.Integer(1), (0, 0, moved, 1, 2, 0): T}
    return sigma1, sigma2


def w_members(key):
    members = [({word: sp.Integer(1)}, f"e{word[2]}{word[3]}")
               for word in E_WORDS]
    sigma1, sigma2 = sigma_tensors(key)
    d_tensor = {
        word: sp.expand(value)
        for word, value in rankone.d_plane_tensor(key, T).items()
    }
    members.append((sigma1, "sigma1"))
    members.append((sigma2, "sigma2"))
    members.append((d_tensor, "D"))
    return members


def assert_x_free(columns):
    for column in columns:
        for value in column.values():
            assert not (sp.sympify(value).free_symbols & set(X9)), value


def cylinder_columns(key, cut):
    blocks = nine_symbol_blocks(key)
    columns = rankone.raw_columns(cut, blocks)
    if cut == 2:
        assert all(
            columns[left] == columns[right]
            for left, right in ((7, 9), (22, 24), (37, 39))
        )
        columns = tuple(
            column for index, column in enumerate(columns)
            if index not in OMIT_C2
        )
    return columns


def verify_combination(columns, coefficients, target):
    accumulated = {}
    for index, coefficient in coefficients.items():
        value = T if coefficient == "t" else sp.sympify(coefficient)
        for word, entry in columns[index].items():
            equations.cylinders.add(
                accumulated, word, sp.expand(value * entry)
            )
    for word, entry in target.items():
        equations.cylinders.add(accumulated, word, -entry)
    residual = {
        word: sp.expand(value) for word, value in accumulated.items()
        if sp.expand(value) != 0
    }
    assert not residual, residual


def two_cylinder_minor(key):
    columns2 = cylinder_columns(key, 2)
    columns3 = cylinder_columns(key, 3)
    assert_x_free(columns2)
    assert_x_free(columns3)
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
    numeric = matrix.subs({T: 1})
    _rref, pivot_columns = numeric.rref()
    assert len(pivot_columns) == 72
    restricted = numeric[:, pivot_columns]
    _rref_t, pivot_rows = restricted.T.rref()
    assert len(pivot_rows) == 72
    minor = matrix.extract(tuple(pivot_rows), tuple(pivot_columns))
    determinant = sp.factor(minor.det(method="domain-ge"))
    assert determinant in (1, -1), determinant
    labels = (
        tuple(words[i] for i in pivot_rows), tuple(pivot_columns),
    )
    return determinant, len(minor.todok()), labels, columns2, columns3, words


def c2_injective(columns2):
    words = sorted(set().union(*(set(c) for c in columns2)))
    index = {word: i for i, word in enumerate(words)}
    matrix = sp.zeros(len(words), len(columns2))
    for j, column in enumerate(columns2):
        for word, value in column.items():
            matrix[index[word], j] = value
    for value in matrix:
        assert getattr(value, "free_symbols", set()) == set()
    assert matrix.rank() == 42
    return True


def w_structure(key):
    determinant, nonzeros, labels, columns2, columns3, _words = (
        two_cylinder_minor(key)
    )
    c2_injective(columns2)
    members = w_members(key)
    spec = MEMBERSHIPS[key]
    for tensor, name in members:
        if name.startswith("e"):
            unit = {word: sp.Integer(1) for word in tensor}
            assert any(column == unit for column in columns2), name
            assert any(column == unit for column in columns3), name
        else:
            data = spec[name]
            verify_combination(columns2, data["C2"], tensor)
            verify_combination(columns3, data["C3"], tensor)
    # independence: restriction to the twelve leading coordinates is the
    # identity matrix, so reading a W-vector's coefficients off these
    # coordinates is exact, and no member meets the two C5 kill words.
    private = E_WORDS + SIGMA_LEAD + (D_LEAD,)
    matrix = sp.zeros(12, 12)
    for j, (tensor, _name) in enumerate(members):
        for i, word in enumerate(private):
            matrix[i, j] = tensor.get(word, 0)
        assert not (set(tensor) & set(KILL_WORDS)), _name
    assert matrix == sp.eye(12)
    # kernel witnesses for M3 (three vectors, unit independence minor)
    blocks = nine_symbol_blocks(key)
    rankone.verify_kernel_witnesses(key, 3, blocks, T)
    return determinant, nonzeros, labels, members


def h_tensor(key):
    blocks = nine_symbol_blocks(key)
    tensor = equations.cylinders.matching_tensor(full.SIX, blocks)
    return {
        word: sp.expand(value) for word, value in tensor.items()
        if sp.expand(value) != 0
    }


def h_tail_identity(key):
    tensor = h_tensor(key)
    expected = {
        word: sp.expand(value)
        for word, value in rankone.d_plane_tensor(key, T).items()
    }
    for bit, word in enumerate(E_WORDS):
        equations.cylinders.add(expected, word, X9[bit])
    expected = {
        word: sp.expand(value) for word, value in expected.items()
        if sp.expand(value) != 0
    }
    assert tensor == expected
    assert tensor[D_LEAD] == 1


def h_in_every_cylinder(key):
    blocks = nine_symbol_blocks(key)
    tensor = h_tensor(key)
    for cut in range(6):
        columns = rankone.raw_columns(cut, blocks)
        assert rankone.direct_representation(cut, blocks, columns) == tensor
    return True


def probe_words(key):
    moved = rankone.DIRECTIONS[key]["moved_colour"]
    sigma_second = (
        (0, 0, moved, 1, 1, 0), (0, 0, moved, 1, 2, 0),
    )
    return E_WORDS + SIGMA_LEAD + sigma_second + (D_LEAD,) + KILL_WORDS


def restriction_table(key, cut):
    columns = rankone.raw_columns(cut, nine_symbol_blocks(key))
    table = {}
    for j, column in enumerate(columns):
        restriction = {
            word: sp.expand(column.get(word, 0)) for word in probe_words(key)
        }
        restriction = {
            word: value for word, value in restriction.items() if value != 0
        }
        if restriction:
            table[j] = restriction
    return table


def verify_probe_cut5(key):
    """W cap C5 = <H> for every X, t.

    On the probe coordinates, the two kill words appear only in columns 13
    and 14 with constant coefficient one, so any C5 combination lying in W
    (whose members all vanish there) has y13 = y14 = 0.  The sigma lead
    words appear only in those two columns, so the sigma components vanish.
    The e-words and the D lead word appear only in column 12, with
    restriction exactly (x_ab; 1); with H = sum x_ab e_ab + D this forces
    the vector to be a multiple of H.
    """
    moved = rankone.DIRECTIONS[key]["moved_colour"]
    table = restriction_table(key, 5)
    expected = {
        12: {**{word: X9[bit] for bit, word in enumerate(E_WORDS)},
             D_LEAD: sp.Integer(1)},
        13: {SIGMA_LEAD[0]: X9[1], (0, 0, moved, 1, 1, 0): X9[3 * moved + 1],
             KILL_WORDS[0]: sp.Integer(1)},
        14: {SIGMA_LEAD[1]: X9[1], (0, 0, moved, 1, 2, 0): X9[3 * moved + 1],
             KILL_WORDS[1]: sp.Integer(1)},
    }
    extra = {
        j: restriction for j, restriction in table.items()
        if j not in expected
    }
    for j, restriction in expected.items():
        assert table.get(j) == restriction, (key, j, table.get(j))
    banned = set(E_WORDS) | set(SIGMA_LEAD) | {D_LEAD} | set(KILL_WORDS)
    for j, restriction in extra.items():
        assert not (set(restriction) & banned), (key, j, restriction)
    return len(extra)


def verify_probe_cut01(key, cut):
    """W cap C_z = <H, D> for z in {0, 1}, for every X, t.

    No C_z column meets any sigma coordinate, so both sigma components of
    a vector in W cap C_z vanish.  The e-words are met only by column 0,
    whose restriction is exactly (x_ab); hence the e-part is y0 * x, and
    with H = sum x_ab e_ab + D the vector is y0 H + (b_D - y0) D.
    Conversely H and D lie in C_z, so the intersection is the full plane.
    """
    moved = rankone.DIRECTIONS[key]["moved_colour"]
    table = restriction_table(key, cut)
    sigma_words = set(SIGMA_LEAD) | {
        (0, 0, moved, 1, 1, 0), (0, 0, moved, 1, 2, 0),
    }
    e_expected = {word: X9[bit] for bit, word in enumerate(E_WORDS)}
    assert {w: v for w, v in table[0].items() if w in E_WORDS} == e_expected
    for j, restriction in table.items():
        assert not (set(restriction) & sigma_words), (key, cut, j)
        if j != 0:
            assert not (set(restriction) & set(E_WORDS)), (key, cut, j)
    # membership of D in this cylinder
    columns = rankone.raw_columns(cut, nine_symbol_blocks(key))
    d_tensor = {
        word: sp.expand(value)
        for word, value in rankone.d_plane_tensor(key, T).items()
    }
    verify_combination(
        columns, MEMBERSHIPS[key]["D"][f"C{cut}"], d_tensor
    )
    return len(table)


def c4_d_matrix(key):
    columns4 = rankone.raw_columns(4, nine_symbol_blocks(key))
    d_tensor = {
        word: sp.expand(value)
        for word, value in rankone.d_plane_tensor(key, T).items()
    }
    words = sorted(set().union(*(set(c) for c in columns4), set(d_tensor)))
    index = {word: i for i, word in enumerate(words)}
    matrix = sp.MutableSparseMatrix(len(words), 46, {})
    for j, column in enumerate(columns4):
        for word, value in column.items():
            matrix[index[word], j] = value
    for word, value in d_tensor.items():
        matrix[index[word], 45] = value
    return sp.ImmutableSparseMatrix(matrix), words, columns4, d_tensor


def c4_minor_determinants(key):
    matrix, words, columns4, d_tensor = c4_d_matrix(key)
    blocks = nine_symbol_blocks(key)
    rankone.verify_kernel_witnesses(key, 4, blocks, T)
    records = []
    for point, expected in C4_ANCHORS[key]:
        substitution = dict.fromkeys(list(X9) + [T], 0)
        substitution[T] = 1
        for bit, value in point.items():
            substitution[X9[bit]] = value
        numeric = matrix.subs(substitution)
        _rref, pivot_columns = numeric.rref()
        assert len(pivot_columns) == 43 and 45 in pivot_columns
        restricted = numeric[:, pivot_columns]
        _rref_t, pivot_rows = restricted.T.rref()
        assert len(pivot_rows) == 43
        minor = matrix.extract(tuple(pivot_rows), tuple(pivot_columns))
        determinant = sp.factor(minor.det(method="domain-ge"))
        assert sp.expand(determinant - sp.sympify(expected)) == 0, (
            key, point, determinant,
        )
        records.append((
            tuple(sorted(point.items())), str(determinant),
            tuple(words[i] for i in pivot_rows), tuple(pivot_columns),
        ))
    return records


def d_in_c4_on_locus(key):
    blocks = d_full_blocks(key)
    columns4 = rankone.raw_columns(4, blocks)
    d_tensor = {
        word: sp.expand(value)
        for word, value in rankone.d_plane_tensor(key, T).items()
    }
    coefficients = MEMBERSHIPS[key]["D_in_C4_on_locus"]
    accumulated = {}
    for index, coefficient in coefficients.items():
        for word, value in columns4[index].items():
            equations.cylinders.add(
                accumulated, word, sp.expand(coefficient * value)
            )
    for word, value in d_tensor.items():
        equations.cylinders.add(accumulated, word, -value)
    residual = {
        word: sp.expand(value) for word, value in accumulated.items()
        if sp.expand(value) != 0
    }
    assert not residual, residual
    return coefficients


def radical_programs(key):
    """Rabinowitsch programs: V(43-minor dets) is inside D_full."""
    names = [str(symbol) for symbol in X9] + ["t", "y"]
    determinants = [expected for _point, expected in C4_ANCHORS[key]]
    body = ",".join(
        str(sp.expand(sp.sympify(det))).replace("**", "^")
        for det in determinants
    )
    programs = []
    for generator in d_full_generators(key):
        text = str(sp.expand(generator)).replace("**", "^")
        program = "ring r=0,(" + ",".join(names) + "),dp;\n"
        program += "option(redSB);\n"
        program += f"ideal I={body},1-y*({text});\n"
        program += "ideal G=slimgb(I);\n"
        program += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
        program += 'print("GBSIZE"); size(G);\n'
        programs.append((str(generator), program))
    return programs


def main():
    for key in ("10", "20"):
        rankone.select_direction(key)
        d_full_parameterization_matches(key)
        determinant, nonzeros, _labels, members = w_structure(key)
        h_tail_identity(key)
        h_in_every_cylinder(key)
        extra5 = verify_probe_cut5(key)
        n0 = verify_probe_cut01(key, 0)
        n1 = verify_probe_cut01(key, 1)
        records = c4_minor_determinants(key)
        d_in_c4_on_locus(key)
        print(
            "W_STRUCTURE", key,
            f"det={determinant}", f"nonzeros={nonzeros}",
            f"members={len(members)}",
            f"probe5_extra={extra5}", f"probe0_cols={n0}",
            f"probe1_cols={n1}",
            f"c4_minors={len(records)}",
            flush=True,
        )
        for point, det, _rows, _cols in records:
            print("  C4_MINOR", key, point, det, flush=True)


if __name__ == "__main__":
    main()
