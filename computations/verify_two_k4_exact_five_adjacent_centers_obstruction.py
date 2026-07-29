#!/usr/bin/env python3
"""Exact audits for the adjacent-centers exact-five obstruction."""

from __future__ import annotations

import itertools

import sympy as sp

import verify_two_k4_exact_four_nonmatching_obstruction as exact_four
import verify_two_k4_four_singular_row_obstruction as base


SITES = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(SITES, 2))
WORDS = tuple(itertools.product(COLORS, repeat=4))
DOMAIN = tuple(
    (edge, left, right)
    for edge in EDGES
    for left in COLORS
    for right in COLORS
)


def degree_three_codomain():
    answer = []
    for hole in SITES:
        present = tuple(site for site in SITES if site != hole)
        for word in itertools.product(COLORS, repeat=3):
            answer.append((hole, dict(zip(present, word, strict=True))))
    return tuple(answer)


def sparse_linear_multiplication():
    """Multiply R_2 by p with p_0=0 and p_i=e_0 otherwise."""

    rows = []
    for hole, output in degree_three_codomain():
        row = []
        for (u, v), left, right in DOMAIN:
            if hole in (u, v) or output[u] != left or output[v] != right:
                row.append(0)
                continue
            third = next(site for site in SITES if site not in (hole, u, v))
            row.append(int(third != 0 and output[third] == 0))
        rows.append(row)
    return sp.Matrix(rows)


def audit_sparse_linear_kernel():
    multiplication = sparse_linear_multiplication()
    assert multiplication.shape == (108, 54)
    assert multiplication.rank() == 46
    kernel = multiplication.nullspace()
    assert len(kernel) == 8
    for vector in kernel:
        assert all(
            not (coefficient and 0 in edge)
            for coefficient, (edge, _left, _right) in zip(vector, DOMAIN)
        )


def overlapping_triangle_matrix(bad_plane_map):
    """Require q p_alpha to vanish on triples containing site one."""

    maps = (bad_plane_map, sp.eye(3), sp.eye(3), sp.eye(3))
    rows = []
    for alpha in (1, 2):
        # Hole one is allowed; the other three components must vanish.
        for hole in (0, 2, 3):
            present = tuple(site for site in SITES if site != hole)
            for word in itertools.product(COLORS, repeat=3):
                output = dict(zip(present, word, strict=True))
                row = []
                for (u, v), left, right in DOMAIN:
                    if (
                        hole in (u, v)
                        or output[u] != left
                        or output[v] != right
                    ):
                        row.append(0)
                        continue
                    third = next(
                        site for site in SITES if site not in (hole, u, v)
                    )
                    row.append(maps[third][output[third], alpha])
                rows.append(row)
    return sp.Matrix(rows)


def plane_rank_normal_form(rank):
    matrix = sp.zeros(3)
    # Column zero is irrelevant to the erased input plane and deliberately
    # nonzero, including in the plane-rank-zero case.
    matrix[:, 0] = sp.Matrix([1, 2, 3])
    if rank >= 1:
        matrix[:, 1] = sp.Matrix([1, 0, 0])
    if rank >= 2:
        matrix[:, 2] = sp.Matrix([0, 1, 0])
    return matrix


def audit_overlapping_triangle_kernel():
    expected_nullities = (1, 0, 0)
    for rank, expected in enumerate(expected_nullities):
        matrix = overlapping_triangle_matrix(plane_rank_normal_form(rank))
        assert matrix.shape == (162, 54)
        assert 54 - matrix.rank() == expected
        if rank == 0:
            vector = matrix.nullspace()[0]
            assert all(
                not (coefficient and 0 in edge)
                for coefficient, (edge, _left, _right) in zip(vector, DOMAIN)
            )


def two_defect_erasure_matrix(p_maps, s_maps, exceptional_color=0):
    rows = []
    for alpha in COLORS:
        if alpha == exceptional_color:
            continue
        for beta in COLORS:
            for output in WORDS:
                row = []
                for (u, v), left, right in DOMAIN:
                    if output[u] != left or output[v] != right:
                        row.append(0)
                        continue
                    i, j = tuple(
                        site for site in SITES if site not in (u, v)
                    )
                    row.append(
                        p_maps[i][output[i], alpha]
                        * s_maps[j][output[j], beta]
                        + s_maps[i][output[i], beta]
                        * p_maps[j][output[j], alpha]
                    )
                if any(row):
                    rows.append(row)
    return sp.Matrix(rows)


def audit_two_defect_erasure_normal_forms():
    identity = sp.eye(3)
    for plane_rank in range(3):
        for second_rank in range(4):
            p_maps = [identity] * 4
            s_maps = [identity] * 4
            p_maps[0] = plane_rank_normal_form(plane_rank)
            s_maps[1] = sp.diag(
                *([1] * second_rank + [0] * (3 - second_rank))
            )
            erased = two_defect_erasure_matrix(tuple(p_maps), tuple(s_maps))
            nullity = 54 - erased.rank()
            assert nullity == (1 if plane_rank == 0 else 0)
            if nullity:
                vector = erased.nullspace()[0]
                assert all(
                    not (coefficient and 0 in edge)
                    for coefficient, (edge, _left, _right) in zip(
                        vector, DOMAIN
                    )
                )


def adjacent_centers_blocks():
    singular_positions = {(0, 0), (0, 1), (1, 0), (2, 2), (3, 3)}
    blocks = {}
    for i in SITES:
        for j in SITES:
            matrix = sp.Matrix([
                [i + 1, j + 1, 1],
                [0, i + j + 2, j + 2],
                [0, 0, i + 2],
            ])
            if (i, j) in singular_positions:
                matrix[2, 2] = 0
                assert matrix.rank() == 2
            else:
                assert matrix.det() != 0
            blocks[i, j] = matrix
    return blocks


def audit_adjacent_centers_sector_identity():
    blocks = adjacent_centers_blocks()
    # Rows 1 and 2 have their sole singular blocks in distinct columns 0,2.
    # Their complementary internal edge is 03.
    left_edge = (0, 3)
    r, s = 1, 2
    c = base.internal_color(*left_edge)

    q_right = {}
    for u, v in EDGES:
        color = base.internal_color(u, v)
        q_right[u, v] = sp.zeros(3)
        q_right[u, v][color, color] = 1

    p0 = {j: blocks[0, j].row(c) for j in SITES}
    p3 = {j: blocks[3, j].row(c) for j in SITES}
    q_effective = {
        (u, v): q_right[u, v] + p0[u].T * p3[v] + p3[u].T * p0[v]
        for u, v in EDGES
    }

    checked = 0
    for x, y in itertools.product(COLORS, repeat=2):
        left_word = (c, x, y, c)
        pr = {j: blocks[r, j].row(x) for j in SITES}
        ps = {j: blocks[s, j].row(y) for j in SITES}
        for right_word in WORDS:
            four_cross = base.permanent([
                [blocks[i, j][left_word[i], right_word[j]] for j in SITES]
                for i in SITES
            ])
            two_cross = 0
            for u, v in EDGES:
                color = base.internal_color(u, v)
                if right_word[u] != color or right_word[v] != color:
                    continue
                remaining = tuple(site for site in SITES if site not in (u, v))
                two_cross += base.permanent([
                    [blocks[i, j][left_word[i], right_word[j]] for j in remaining]
                    for i in (r, s)
                ])
            pulled_back = base.beta_coefficient(
                q_effective, pr, ps, right_word
            )
            assert sp.expand(pulled_back - four_cross - two_cross) == 0
            checked += 1
    assert checked == 729

    # If the erasure kernel is nonzero, all q_eff blocks incident with the
    # first exceptional column 0 vanish.  This would put all three incident
    # right-K4 endpoint colors in one two-plane.
    incident = [
        sp.eye(3).col(base.internal_color(0, other))
        for other in (1, 2, 3)
    ]
    assert sp.Matrix.hstack(*incident).rank() == 3
    assert sp.Matrix.hstack(p0[0].T, p3[0].T).rank() <= 2


def audit_position_orbit():
    representative = frozenset(
        ((0, 0), (0, 1), (1, 0), (2, 2), (3, 3))
    )
    permutations = tuple(itertools.permutations(SITES))
    orbit = set()
    for row_permutation, column_permutation in itertools.product(
        permutations, repeat=2
    ):
        image = frozenset(
            (row_permutation[row], column_permutation[column])
            for row, column in representative
        )
        orbit.add(image)
        orbit.add(frozenset((column, row) for row, column in image))
    assert len(orbit) == 288
    for positions in orbit:
        row_degrees = [
            sum(row == vertex for row, _column in positions)
            for vertex in SITES
        ]
        column_degrees = [
            sum(column == vertex for _row, column in positions)
            for vertex in SITES
        ]
        assert sorted(row_degrees) == [1, 1, 1, 2]
        assert sorted(column_degrees) == [1, 1, 1, 2]
        degree_two_row = row_degrees.index(2)
        degree_two_column = column_degrees.index(2)
        assert (degree_two_row, degree_two_column) in positions


def audit_full_exact_five_census():
    cells = tuple(itertools.product(SITES, repeat=2))

    def degrees(positions, side):
        return tuple(
            sum(position[side] == vertex for position in positions)
            for vertex in SITES
        )

    def full_occupancy(positions):
        return all(degrees(positions, 0)) and all(degrees(positions, 1))

    def has_separated_singletons(positions, side):
        local_degrees = degrees(positions, side)
        singletons = tuple(
            vertex for vertex, degree in enumerate(local_degrees) if degree == 1
        )
        exceptional_opposite_vertices = {
            next(
                position[1 - side]
                for position in positions
                if position[side] == vertex
            )
            for vertex in singletons
        }
        return len(exceptional_opposite_vertices) >= 2

    all_supports = tuple(itertools.combinations(cells, 5))
    assert len(all_supports) == 4368
    occupied = tuple(filter(full_occupancy, all_supports))
    assert len(occupied) == 432
    assert all(
        sorted(degrees(positions, side)) == [1, 1, 1, 2]
        for positions in occupied
        for side in (0, 1)
    )
    assert all(
        has_separated_singletons(positions, side)
        for positions in occupied
        for side in (0, 1)
    )


def main():
    exact_four.audit_one_defect_annihilator()
    audit_sparse_linear_kernel()
    audit_overlapping_triangle_kernel()
    audit_two_defect_erasure_normal_forms()
    audit_adjacent_centers_sector_identity()
    audit_position_orbit()
    audit_full_exact_five_census()
    print("almost-invertible star annihilator: reused exact ranks 27,1,1,1")
    print("three-site sparse multiplication kernel: dimension 8, silent bad site")
    print("overlapping triangle kernels: dimensions 1,0,0")
    print("two-defect erasure normal forms: nullities 1,0,0")
    print("adjacent-centers effective-Hessian identity: 729 coefficients")
    print("adjacent-centers position orbit: 288 labelled supports")
    print("exact-five census: 4368 total, 432 full-occupancy, 0 residual")
    print("full exact-five obstruction: PASS")


if __name__ == "__main__":
    main()
