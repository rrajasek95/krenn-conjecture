#!/usr/bin/env python3
"""Exact audit of the adjacent-five-cut Hessian-intersection boundary.

The checker verifies two facts used in
``notes/adjacent-five-cut-hessian-intersection-countermodel.md``.

1.  For a six-set ``S`` and external pair ``R``, a common functional in all
    six lifted cofactor kernels kills the exact six-cut sum

        sum_z T_(1,z) = 6 T_0 + 2 T_2.

2.  A sparse integral six-site family gives an adjacent pair whose two
    lifted cofactor kernels have no target-active common functional, even
    though each five-set defect space is nonzero.  The two individual
    defect spaces are the different coordinate lines ``<e_2>`` and
    ``<e_1>``.
"""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


S = tuple(range(6))
COLORS = tuple(range(3))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def coordinate_cell(color):
    return tuple(
        tuple(int(i == color and j == color) for j in COLORS)
        for i in COLORS
    )


def build_source():
    matchings = (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 2), (1, 4), (3, 5)),
        ((0, 3), (1, 5), (2, 4)),
    )
    edges = {}
    for color, matching in enumerate(matchings):
        for edge in matching:
            edges[edge] = coordinate_cell(color)
    return matchings, edges


MATCHINGS_BY_COLOR, EDGES = build_source()


def edge_entry(left, right, a, b):
    if left < right:
        return EDGES.get((left, right), ((0,) * 3,) * 3)[a][b]
    return EDGES.get((right, left), ((0,) * 3,) * 3)[b][a]


def coefficient(vertices, word):
    colors = dict(zip(vertices, word, strict=True))
    value = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for left, right in matching:
            term *= edge_entry(left, right, colors[left], colors[right])
        value += term
    return value


def tensor(vertices):
    return {
        word: value
        for word in product(COLORS, repeat=len(vertices))
        if (value := coefficient(vertices, word))
    }


def word_index(word):
    value = 0
    for digit in word:
        value = 3 * value + digit
    return value


def cofactor_slice_matrix(U):
    """Columns span S_U=sum_u V_u tensor H_(U-u)."""
    columns = []
    for deleted in U:
        remaining = tuple(v for v in U if v != deleted)
        cofactor = tensor(remaining)
        for exposed_color in COLORS:
            column = [0] * (3**5)
            for remaining_word, value in cofactor.items():
                full = {deleted: exposed_color}
                full.update(zip(remaining, remaining_word, strict=True))
                word = tuple(full[v] for v in U)
                column[word_index(word)] = value
            columns.append(column)
    return sp.Matrix(3**5, 15, lambda row, col: columns[col][row])


def constant_column(length, color):
    column = sp.zeros(3**length, 1)
    column[word_index((color,) * length), 0] = 1
    return column


def audit_sparse_source_and_private_cofactors():
    assert tensor(S) == {
        (0, 0, 0, 0, 0, 0): 1,
        (0, 0, 2, 1, 2, 1): 1,
        (1, 1, 1, 1, 1, 1): 1,
        (2, 2, 2, 2, 2, 2): 1,
    }

    # Three private four-site cofactors isolate the three constant tensors.
    assert tensor((0, 1, 4, 5)) == {(0, 0, 0, 0): 1}
    assert tensor((1, 3, 4, 5)) == {(1, 1, 1, 1): 1}
    assert tensor((1, 2, 4, 5)) == {(2, 2, 2, 2): 1}

    # Therefore the edge-Hessian columns for 23:E00, 02:E11, and 03:E22
    # are exactly g_0, g_1, and g_2.  All three edges meet {2,3}.
    private = ((2, 3, 0), (0, 2, 1), (0, 3, 2))
    for left, right, color in private:
        remainder = tuple(v for v in S if v not in (left, right))
        expected = {(color,) * 4: 1}
        assert tensor(remainder) == expected


def audit_individual_defect_spaces():
    U2 = tuple(v for v in S if v != 2)
    U3 = tuple(v for v in S if v != 3)

    expected = ((U2, (0, 1), 2), (U3, (0, 2), 1))
    for U, contained_colors, missing_color in expected:
        slices = cofactor_slice_matrix(U)
        base_rank = slices.rank()
        assert base_rank == 15
        constants = [constant_column(5, color) for color in COLORS]

        for color in contained_colors:
            assert slices.row_join(constants[color]).rank() == base_rank
        assert slices.row_join(constants[missing_color]).rank() == base_rank + 1
        assert slices.row_join(sp.Matrix.hstack(*constants)).rank() == base_rank + 1

    beta2 = sp.zeros(3**5, 1)
    beta2[word_index((2, 2, 2, 2, 2)), 0] = 1
    beta2[word_index((0, 0, 1, 2, 1)), 0] = -1
    slices2 = cofactor_slice_matrix(U2)
    assert slices2.T * beta2 == sp.zeros(15, 1)
    assert [
        beta2[word_index((color,) * 5), 0] for color in COLORS
    ] == [0, 0, 1]

    beta3 = sp.zeros(3**5, 1)
    beta3[word_index((1, 1, 1, 1, 1)), 0] = 1
    beta3[word_index((0, 0, 2, 2, 1)), 0] = -1
    slices3 = cofactor_slice_matrix(U3)
    assert slices3.T * beta3 == sp.zeros(15, 1)
    assert [
        beta3[word_index((color,) * 5), 0] for color in COLORS
    ] == [0, 1, 0]

    # By annihilator duality, delta_U(ker B_U) is exactly the coordinate
    # line complementary to G_U intersect S_U.
    return U2, U3


def audit_adjacent_common_kernel_is_target_zero():
    U2, U3 = audit_individual_defect_spaces()
    assert set(U2) & set(U3) == {0, 1, 4, 5}

    # L_z = V_z^* tensor ker(B_(S-z)).  Its annihilator is the z-star
    # Hessian image V_z tensor S_(S-z).  The three private identities above
    # put every six-site constant tensor in L_2^perp + L_3^perp:
    #
    #   g0 = E00_(23) tensor H_(0145),
    #   g1 = E11_(02) tensor H_(1345),
    #   g2 = E22_(03) tensor H_(1245).
    #
    # Hence every eta in L_2 intersect L_3 kills all three constants.
    private_remainders = {
        0: (0, 1, 4, 5),
        1: (1, 3, 4, 5),
        2: (1, 2, 4, 5),
    }
    for color, remainder in private_remainders.items():
        assert tensor(remainder) == {(color,) * 4: 1}


def audit_six_cut_sector_count():
    # Fix S={0,...,5}, R={6,7}.  For U_z=S-z the complement is R+z.
    # A matching with R paired internally is one-crossing for all six z;
    # a matching with R separated is one-crossing exactly for the two z
    # matched to R.  This proves sum_z T_(1,z)=6T_0+2T_2 atomwise.
    B = tuple(range(8))
    R = {6, 7}
    for matching in perfect_matchings(B):
        even_crossings = sum(
            (left in R) != (right in R) for left, right in matching
        )
        multiplicity = 0
        for z in S:
            U = set(S) - {z}
            crossings = sum(
                (left in U) != (right in U) for left, right in matching
            )
            multiplicity += int(crossings == 1)
        assert multiplicity == (6 if even_crossings == 0 else 2)


def main():
    audit_sparse_source_and_private_cofactors()
    audit_adjacent_common_kernel_is_target_zero()
    audit_six_cut_sector_count()
    print("sparse six-site source and three private Hessian columns: PASS")
    print("individual defect spaces: W_(S-2)=<e2>, W_(S-3)=<e1>")
    print("adjacent lifted-kernel intersection is target-zero: PASS")
    print("six-cut identity sum_z T1,z = 6 T0 + 2 T2: PASS")


if __name__ == "__main__":
    main()
