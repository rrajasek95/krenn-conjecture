#!/usr/bin/env python3
"""Exact audits for the coincident-defect exact-six obstruction."""

from __future__ import annotations

import itertools

import sympy as sp

import verify_two_k4_exact_five_adjacent_centers_obstruction as exact_five
import verify_two_k4_four_singular_row_obstruction as base


SITES = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(SITES, 2))
WORDS = tuple(itertools.product(COLORS, repeat=4))
DOMAIN = exact_five.DOMAIN


def coincident_overlapping_triangle_matrix(bad_plane_map):
    """Require q p_alpha to vanish on every triple containing site zero."""

    maps = (bad_plane_map, sp.eye(3), sp.eye(3), sp.eye(3))
    rows = []
    for alpha in (1, 2):
        # Hole zero is allowed; holes 1,2,3 must vanish.
        for hole in (1, 2, 3):
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


def audit_coincident_overlapping_kernel():
    expected_nullities = (27, 0, 0)
    for plane_rank, expected in enumerate(expected_nullities):
        matrix = coincident_overlapping_triangle_matrix(
            exact_five.plane_rank_normal_form(plane_rank)
        )
        assert matrix.shape == (162, 54)
        assert 54 - matrix.rank() == expected
        if plane_rank == 0:
            for vector in matrix.nullspace():
                assert all(
                    not (coefficient and 0 in edge)
                    for coefficient, (edge, _left, _right) in zip(
                        vector, DOMAIN
                    )
                )


def audit_coincident_erasure_normal_forms():
    identity = sp.eye(3)
    expected = {
        0: (27, 1, 1, 1),
        1: (0, 0, 0, 0),
        2: (0, 0, 0, 0),
    }
    for plane_rank in range(3):
        for second_rank in range(4):
            p_maps = [identity] * 4
            s_maps = [identity] * 4
            p_maps[0] = exact_five.plane_rank_normal_form(plane_rank)
            s_maps[0] = sp.diag(
                *([1] * second_rank + [0] * (3 - second_rank))
            )
            erased = exact_five.two_defect_erasure_matrix(
                tuple(p_maps), tuple(s_maps)
            )
            nullity = 54 - erased.rank()
            assert nullity == expected[plane_rank][second_rank]
            for vector in erased.nullspace():
                assert all(
                    not (coefficient and 0 in edge)
                    for coefficient, (edge, _left, _right) in zip(
                        vector, DOMAIN
                    )
                )


def coincident_star_blocks():
    singular_positions = {
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 0),
        (2, 0),
        (3, 0),
    }
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


def audit_coincident_star_sector_identity():
    blocks = coincident_star_blocks()
    # Rows 1 and 2 have their sole singular components at the same right
    # site zero.  Their complementary internal edge is 03.
    r, s = 1, 2
    left_edge = (0, 3)
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

    incident = [
        sp.eye(3).col(base.internal_color(0, other))
        for other in (1, 2, 3)
    ]
    assert sp.Matrix.hstack(*incident).rank() == 3
    assert sp.Matrix.hstack(p0[0].T, p3[0].T).rank() <= 2


def position_orbit(representative):
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
    return orbit


def audit_exact_six_position_boundary():
    representatives = {
        "two_stars": (
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (2, 0),
            (3, 0),
        ),
        "k22_plus_two_star": (
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (2, 2),
            (2, 3),
        ),
        "six_cycle": (
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 2),
            (2, 2),
            (2, 0),
        ),
    }
    orbits = {
        name: position_orbit(representative)
        for name, representative in representatives.items()
    }
    assert {name: len(orbit) for name, orbit in orbits.items()} == {
        "two_stars": 16,
        "k22_plus_two_star": 144,
        "six_cycle": 96,
    }
    assert all(
        not orbits[first] & orbits[second]
        for first, second in itertools.combinations(orbits, 2)
    )
    assert len(set().union(*orbits.values())) == 256

    def degrees(positions, side):
        return tuple(
            sum(position[side] == vertex for position in positions)
            for vertex in SITES
        )

    def has_two_sparse_vertices(positions):
        return any(
            sum(degree <= 1 for degree in degrees(positions, side)) >= 2
            for side in (0, 1)
        )

    assert all(
        has_two_sparse_vertices(positions)
        for name in ("two_stars", "k22_plus_two_star")
        for positions in orbits[name]
    )
    assert all(
        not has_two_sparse_vertices(positions)
        for positions in orbits["six_cycle"]
    )


def main():
    exact_five.exact_four.audit_one_defect_annihilator()
    exact_five.audit_sparse_linear_kernel()
    audit_coincident_overlapping_kernel()
    audit_coincident_erasure_normal_forms()
    audit_coincident_star_sector_identity()
    audit_exact_six_position_boundary()
    print("coincident overlapping kernels: dimensions 27,0,0")
    print("coincident-defect erasure normal forms: exact 3x4 table")
    print("coincident-star effective-Hessian identity: 729 coefficients")
    print("exact-six residual orbits: 16 + 144 + 96 = 256")
    print("coincident erasure removes first two; six-cycle residual: 96")
    print("exact-six coincident-defect obstruction: PASS")


if __name__ == "__main__":
    main()
