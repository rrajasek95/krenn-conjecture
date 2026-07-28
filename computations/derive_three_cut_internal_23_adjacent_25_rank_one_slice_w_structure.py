#!/usr/bin/env python3
"""W-structure certificates for the rank-one slice A25 = E00 + t*E10 + s*E20.

The moving block (e0 + t*e1 + s*e2) (x) e0 is rank one for every complex
(t, s), and this module certifies, with all nine A23 entries and both
parameters polynomial variables over Q:

* combined four-term kernel relations giving dim ker M3, dim ker M4 >= 3;
* W := C2 cap C3 = span(e_ab, sigma1, sigma2, D) with a constant unit
  72-minor over Q[t, s], exact memberships, and an identity restriction
  matrix, where

      sigma1 = [000110] + t[001110] + s[002110],
      sigma2 = [000120] + t[001120] + s[002120],
      D      = [111110] + [121200] + [220220] + t[221220] + s[222220];

* the tail identity H = sum x_ab e_ab + D and H in all six cylinders;
* probe identities: W cap C5 = <H> and W cap C0 = W cap C1 = <H, D> for
  every X, t, s;
* D in C4 exactly on the degenerate locus

      D_ts = V(t x00 - x10, t x02 - x12, s x00 - x20, s x02 - x22)
           = { A23 = v (x) r0 + m (x) e1 },   v = e0 + t e1 + s e2,

  via ten factored 43-minors of [C4 | D] with radical certificates and an
  explicit on-locus representation over (a0, a1, a2, w1, w2, t, s).

Specializing (t, s) to (t, 0) or (0, s) recovers the two single-direction
theorems; the slice theorem closes the whole rank-one family
A25 = v (x) e0 with leading coefficient one.
"""

from __future__ import annotations

import itertools

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_rank_one_directions as rankone
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


T = rankone.T
S = sp.Symbol("s")
X9 = tuple(sp.Symbol(f"x{a}{b}") for a, b in full.CELLS)
A0, A1, A2, W1, W2 = sp.symbols("a0 a1 a2 w1 w2")
OMIT_C2 = rankone.OMIT_C2
E_WORDS = tuple((0, 0, a, b, 0, 0) for a, b in full.CELLS)
SIGMA_LEAD = ((0, 0, 0, 1, 1, 0), (0, 0, 0, 1, 2, 0))
D_LEAD = (1, 2, 1, 2, 0, 0)
KILL_WORDS = ((1, 2, 1, 2, 1, 0), (1, 2, 1, 2, 2, 0))

MEMBERSHIPS = {
    "sigma1": {"C2": {9: 1, 23: "t", 37: "s"}, "C3": {25: 1}},
    "sigma2": {"C2": {10: 1, 24: "t", 38: "s"}, "C3": {26: 1}},
    "D": {
        "C2": {11: 1, 15: 1, 25: "t", 39: "s"},
        "C3": {27: 1, 35: 1},
        "C0": {19: 1, 41: 1},
        "C1": {25: 1, 38: 1},
    },
    "D_in_C4_on_locus": {
        6: -A1, 7: -A1 * T - W1, 8: -A1 * S - W2,
        9: -A0, 11: -A2, 12: 1, 19: 1, 32: 1,
    },
}

# [C4 | D] anchor points (bit -> value; t = 1, s = 2 at the anchor) and
# expected factored determinants.  The four mixed anchors cover partial
# alignment patterns that the six one-cell anchors miss.
C4_ANCHORS = (
    ({3: 1}, "x10**6*(t*x00 - x10)**3"),
    ({5: 1}, "-x12**6*(t*x02 - x12)**3"),
    ({6: 1}, "-x20**6*(s*x00 - x20)**3"),
    ({8: 1}, "x22**6*(s*x02 - x22)**3"),
    ({0: 1}, "x00**6*(t*x00 - x10)**3"),
    ({2: 1}, "-x02**6*(t*x02 - x12)**3"),
    ({0: 1, 3: 1}, "-x00**6*(s*x00 - x20)**3"),
    ({0: 1, 6: 2}, "x00**6*(t*x00 - x10)**3"),
    ({2: 1, 5: 1}, "x02**6*(s*x02 - x22)**3"),
    ({2: 1, 8: 2}, "-x02**6*(t*x02 - x12)**3"),
)


def d_locus_generators():
    return (
        T * X9[0] - X9[3],
        T * X9[2] - X9[5],
        S * X9[0] - X9[6],
        S * X9[2] - X9[8],
    )


def slice_blocks(with_x=True):
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


def locus_blocks():
    cells = {}
    for j, parameter in enumerate((A0, A1, A2)):
        cells[0, j] = parameter
        cells[1, j] = T * parameter
        cells[2, j] = S * parameter
    cells[1, 1] = cells[1, 1] + W1
    cells[2, 1] = cells[2, 1] + W2
    cell_values = {
        bit: sp.expand(cells.get(full.CELLS[bit], 0)) for bit in range(9)
    }
    blocks = equations.cylinders.aggregate()
    blocks[2, 3] = {
        full.CELLS[bit]: value
        for bit, value in cell_values.items() if value != 0
    }
    block25 = dict(blocks[2, 5])
    block25[1, 0] = block25.get((1, 0), sp.Integer(0)) + T
    block25[2, 0] = block25.get((2, 0), sp.Integer(0)) + S
    blocks[2, 5] = block25
    return blocks


def locus_parameterization_matches():
    blocks = locus_blocks()
    entries = {
        X9[bit]: blocks[2, 3].get(cell, sp.Integer(0))
        for bit, cell in enumerate(full.CELLS)
    }
    for generator in d_locus_generators():
        assert sp.expand(generator.subs(entries)) == 0, generator
    solved = {
        A0: entries[X9[0]], A1: entries[X9[1]], A2: entries[X9[2]],
        W1: entries[X9[4]] - T * entries[X9[1]],
        W2: entries[X9[7]] - S * entries[X9[1]],
    }
    for symbol, value in solved.items():
        assert sp.expand(value - symbol) == 0, (symbol, value)


def d_plane_tensor():
    return {
        (1, 1, 1, 1, 1, 0): sp.Integer(1),
        (1, 2, 1, 2, 0, 0): sp.Integer(1),
        (2, 2, 0, 2, 2, 0): sp.Integer(1),
        (2, 2, 1, 2, 2, 0): T,
        (2, 2, 2, 2, 2, 0): S,
    }


def sigma_tensors():
    sigma1 = {
        (0, 0, 0, 1, 1, 0): sp.Integer(1),
        (0, 0, 1, 1, 1, 0): T, (0, 0, 2, 1, 1, 0): S,
    }
    sigma2 = {
        (0, 0, 0, 1, 2, 0): sp.Integer(1),
        (0, 0, 1, 1, 2, 0): T, (0, 0, 2, 1, 2, 0): S,
    }
    return sigma1, sigma2


def w_members():
    members = [({word: sp.Integer(1)}, f"e{word[2]}{word[3]}")
               for word in E_WORDS]
    sigma1, sigma2 = sigma_tensors()
    members.append((sigma1, "sigma1"))
    members.append((sigma2, "sigma2"))
    members.append((d_plane_tensor(), "D"))
    return members


def kernel_witnesses(cut):
    """Four-term relations C(2,0) + t C(2,1) + s C(2,2) = fixed columns."""
    five = tuple(site for site in full.SIX if site != cut)

    def index(a, hole, colour):
        return 15 * a + 3 * five.index(hole) + colour

    witnesses = []
    for cut_colour in full.COLOURS:
        vector = {
            index(cut_colour, 2, 0): -sp.Integer(1),
            index(cut_colour, 2, 1): -T,
            index(cut_colour, 2, 2): -S,
        }
        if cut == 3:
            vector[index(cut_colour, 4, 0)] = sp.Integer(1)
            private = index(cut_colour, 4, 0)
        elif cut == 4:
            vector[index(cut_colour, 3, 1)] = sp.Integer(1)
            private = index(cut_colour, 3, 1)
        else:
            raise ValueError(cut)
        witnesses.append((vector, private))
    return witnesses


def verify_kernel_witnesses(cut, blocks):
    columns = rankone.raw_columns(cut, blocks)
    privates = set()
    for vector, private in kernel_witnesses(cut):
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
        assert not residual, (cut, residual)
        privates.add(private)
    assert len(privates) == 3


def cylinder_columns(cut):
    blocks = slice_blocks()
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


def assert_symbol_free(columns, banned):
    for column in columns:
        for value in column.values():
            assert not (sp.sympify(value).free_symbols & set(banned)), value


def verify_combination(columns, coefficients, target):
    accumulated = {}
    for index, coefficient in coefficients.items():
        if coefficient == "t":
            value = T
        elif coefficient == "s":
            value = S
        else:
            value = sp.sympify(coefficient)
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


def two_cylinder_minor():
    columns2 = cylinder_columns(2)
    columns3 = cylinder_columns(3)
    assert_symbol_free(columns2, set(X9) | {T, S})
    assert_symbol_free(columns3, set(X9))
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
    assert len(pivot_columns) == 72
    restricted = numeric[:, pivot_columns]
    _rref_t, pivot_rows = restricted.T.rref()
    assert len(pivot_rows) == 72
    minor = matrix.extract(tuple(pivot_rows), tuple(pivot_columns))
    determinant = sp.factor(minor.det(method="domain-ge"))
    assert determinant in (1, -1), determinant
    labels = (tuple(words[i] for i in pivot_rows), tuple(pivot_columns))
    return determinant, len(minor.todok()), labels, columns2, columns3


def c2_injective(columns2):
    words = sorted(set().union(*(set(c) for c in columns2)))
    index = {word: i for i, word in enumerate(words)}
    matrix = sp.zeros(len(words), len(columns2))
    for j, column in enumerate(columns2):
        for word, value in column.items():
            matrix[index[word], j] = value
    assert matrix.rank() == 42
    return True


def w_structure():
    determinant, nonzeros, labels, columns2, columns3 = two_cylinder_minor()
    c2_injective(columns2)
    members = w_members()
    for tensor, name in members:
        if name.startswith("e"):
            unit = {word: sp.Integer(1) for word in tensor}
            assert any(column == unit for column in columns2), name
            assert any(column == unit for column in columns3), name
        else:
            data = MEMBERSHIPS[name]
            verify_combination(columns2, data["C2"], tensor)
            verify_combination(columns3, data["C3"], tensor)
    private = E_WORDS + SIGMA_LEAD + (D_LEAD,)
    matrix = sp.zeros(12, 12)
    for j, (tensor, name) in enumerate(members):
        for i, word in enumerate(private):
            matrix[i, j] = tensor.get(word, 0)
        assert not (set(tensor) & set(KILL_WORDS)), name
    assert matrix == sp.eye(12)
    blocks = slice_blocks()
    verify_kernel_witnesses(3, blocks)
    verify_kernel_witnesses(4, blocks)
    return determinant, nonzeros, labels, members


def h_tensor():
    blocks = slice_blocks()
    tensor = equations.cylinders.matching_tensor(full.SIX, blocks)
    return {
        word: sp.expand(value) for word, value in tensor.items()
        if sp.expand(value) != 0
    }


def h_tail_identity():
    tensor = h_tensor()
    expected = dict(d_plane_tensor())
    for bit, word in enumerate(E_WORDS):
        equations.cylinders.add(expected, word, X9[bit])
    expected = {
        word: sp.expand(value) for word, value in expected.items()
        if sp.expand(value) != 0
    }
    assert tensor == expected
    assert tensor[D_LEAD] == 1


def h_in_every_cylinder():
    blocks = slice_blocks()
    tensor = h_tensor()
    for cut in range(6):
        columns = rankone.raw_columns(cut, blocks)
        assert rankone.direct_representation(cut, blocks, columns) == tensor
    return True


def probe_words():
    sigma1, sigma2 = sigma_tensors()
    return (
        E_WORDS + tuple(sigma1) + tuple(sigma2) + (D_LEAD,) + KILL_WORDS
    )


def restriction_table(cut):
    columns = rankone.raw_columns(cut, slice_blocks())
    table = {}
    for j, column in enumerate(columns):
        restriction = {
            word: sp.expand(column.get(word, 0)) for word in probe_words()
        }
        restriction = {
            word: value for word, value in restriction.items() if value != 0
        }
        if restriction:
            table[j] = restriction
    return table


def verify_probe_cut5():
    table = restriction_table(5)
    expected = {
        12: {**{word: X9[bit] for bit, word in enumerate(E_WORDS)},
             D_LEAD: sp.Integer(1)},
        13: {(0, 0, 0, 1, 1, 0): X9[1], (0, 0, 1, 1, 1, 0): X9[4],
             (0, 0, 2, 1, 1, 0): X9[7], KILL_WORDS[0]: sp.Integer(1)},
        14: {(0, 0, 0, 1, 2, 0): X9[1], (0, 0, 1, 1, 2, 0): X9[4],
             (0, 0, 2, 1, 2, 0): X9[7], KILL_WORDS[1]: sp.Integer(1)},
    }
    assert table == expected, table
    return len(table)


def verify_probe_cut01(cut):
    table = restriction_table(cut)
    sigma1, sigma2 = sigma_tensors()
    sigma_words = set(sigma1) | set(sigma2)
    e_expected = {word: X9[bit] for bit, word in enumerate(E_WORDS)}
    assert {w: v for w, v in table[0].items() if w in E_WORDS} == e_expected
    for j, restriction in table.items():
        assert not (set(restriction) & sigma_words), (cut, j)
        if j != 0:
            assert not (set(restriction) & set(E_WORDS)), (cut, j)
    columns = rankone.raw_columns(cut, slice_blocks())
    verify_combination(
        columns, MEMBERSHIPS["D"][f"C{cut}"], d_plane_tensor()
    )
    return len(table)


def c4_d_matrix():
    columns4 = rankone.raw_columns(4, slice_blocks())
    d_tensor = d_plane_tensor()
    words = sorted(set().union(*(set(c) for c in columns4), set(d_tensor)))
    index = {word: i for i, word in enumerate(words)}
    matrix = sp.MutableSparseMatrix(len(words), 46, {})
    for j, column in enumerate(columns4):
        for word, value in column.items():
            matrix[index[word], j] = value
    for word, value in d_tensor.items():
        matrix[index[word], 45] = value
    return sp.ImmutableSparseMatrix(matrix), words


def c4_minor_determinants():
    matrix, words = c4_d_matrix()
    records = []
    for point, expected in C4_ANCHORS:
        substitution = dict.fromkeys(list(X9) + [T, S], 0)
        substitution[T] = 1
        substitution[S] = 2
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
            point, determinant,
        )
        records.append((
            tuple(sorted(point.items())), str(determinant),
            tuple(words[i] for i in pivot_rows), tuple(pivot_columns),
        ))
    return records


def d_in_c4_on_locus():
    blocks = locus_blocks()
    columns4 = rankone.raw_columns(4, blocks)
    d_tensor = d_plane_tensor()
    coefficients = MEMBERSHIPS["D_in_C4_on_locus"]
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


def radical_programs():
    names = [str(symbol) for symbol in X9] + ["t", "s", "y"]
    determinants = [expected for _point, expected in C4_ANCHORS]
    body = ",".join(
        str(sp.expand(sp.sympify(det))).replace("**", "^")
        for det in determinants
    )
    programs = []
    for generator in d_locus_generators():
        text = str(sp.expand(generator)).replace("**", "^")
        program = "ring r=0,(" + ",".join(names) + "),dp;\n"
        program += "option(redSB);\n"
        program += f"ideal I={body},1-y*({text});\n"
        program += "ideal G=slimgb(I);\n"
        program += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
        program += 'print("GBSIZE"); size(G);\n'
        programs.append((str(generator), program))
    return programs


def no_mixed_terms():
    """Every matching-tensor coefficient has total degree at most one in
    the eleven parameters (x_ab, t, s): edges 23 and 25 share site 2, so
    no matching uses an A23 cell and a moving A25 cell simultaneously."""
    tensor = equations.cylinders.matching_tensor(full.SIX, slice_blocks())
    for value in tensor.values():
        polynomial = sp.Poly(sp.expand(value), *(list(X9) + [T, S]))
        for monomial in polynomial.monoms():
            assert sum(monomial) <= 1, monomial
    return True


def main():
    rankone.select_direction("10")
    no_mixed_terms()
    locus_parameterization_matches()
    determinant, nonzeros, _labels, members = w_structure()
    h_tail_identity()
    h_in_every_cylinder()
    n5 = verify_probe_cut5()
    n0 = verify_probe_cut01(0)
    n1 = verify_probe_cut01(1)
    records = c4_minor_determinants()
    d_in_c4_on_locus()
    print(
        "SLICE_W_STRUCTURE",
        f"det={determinant}", f"nonzeros={nonzeros}",
        f"members={len(members)}",
        f"probe5_cols={n5}", f"probe0_cols={n0}", f"probe1_cols={n1}",
        f"c4_minors={len(records)}",
        flush=True,
    )
    for point, det, _rows, _cols in records:
        print("  C4_MINOR", point, det, flush=True)


if __name__ == "__main__":
    main()
