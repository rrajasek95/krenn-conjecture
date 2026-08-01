#!/usr/bin/env python3
"""Exact audits for two-k4-exact-four-nonmatching-obstruction.md."""

from __future__ import annotations

import itertools

import sympy as sp

import verify_two_k4_four_singular_row_obstruction as base


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


SITES = tuple(range(4))
COLORS = tuple(range(3))
WORDS = tuple(itertools.product(COLORS, repeat=4))
EDGES = tuple(itertools.combinations(SITES, 2))


def epsilon(word):
    if len(set(word)) < 3:
        return 0
    inversions = sum(
        word[i] > word[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return (-1) ** inversions


def one_defect_annihilator_matrix(bad_map):
    """Multiplication R_3 -> Hom(C^3,R_4) by an almost-invertible star."""

    maps = (bad_map, sp.eye(3), sp.eye(3), sp.eye(3))
    domain = []
    for hole in SITES:
        present = tuple(site for site in SITES if site != hole)
        for word in itertools.product(COLORS, repeat=3):
            domain.append((hole, dict(zip(present, word, strict=True))))

    rows = []
    for beta in COLORS:
        for output in WORDS:
            rows.append([
                maps[hole][output[hole], beta]
                if all(output[site] == local[site] for site in local)
                else 0
                for hole, local in domain
            ])
    return sp.Matrix(rows), domain


def generalized_determinant_generator(bad_map, domain):
    """The unique annihilator when the exceptional component is nonzero."""

    generator = sp.zeros(len(domain), 1)
    for index, (hole, local) in enumerate(domain):
        if hole == 0:
            generator[index] = epsilon((local[1], local[2], local[3]))
            continue
        remaining = tuple(site for site in (1, 2, 3) if site != hole)
        contraction = sum(
            bad_map[local[0], color]
            * epsilon((color, local[remaining[0]], local[remaining[1]]))
            for color in COLORS
        )
        generator[index] = (-1) ** hole * contraction
    return generator


def audit_one_defect_annihilator():
    for rank in range(4):
        bad_map = sp.diag(*([1] * rank + [0] * (3 - rank)))
        multiplication, domain = one_defect_annihilator_matrix(bad_map)
        require(
            multiplication.shape == (243, 108),
            "multiplication.shape == (243, 108)",
        )
        if rank == 0:
            require(
                multiplication.rank() == 81,
                "multiplication.rank() == 81",
            )
            for index, (hole, _local) in enumerate(domain):
                if hole != 0:
                    continue
                vector = sp.zeros(108, 1)
                vector[index] = 1
                require(
                    multiplication * vector == sp.zeros(243, 1),
                    "multiplication * vector == sp.zeros(243, 1)",
                )
            continue

        require(
            multiplication.rank() == 107,
            "multiplication.rank() == 107",
        )
        generator = generalized_determinant_generator(bad_map, domain)
        require(
            generator != sp.zeros(108, 1),
            "generator != sp.zeros(108, 1)",
        )
        require(
            multiplication * generator == sp.zeros(243, 1),
            "multiplication * generator == sp.zeros(243, 1)",
        )

        # Its component missing the exceptional site is Det_3, hence has
        # rank three in every one-mode flattening.
        for selected in (1, 2, 3):
            other = tuple(site for site in (1, 2, 3) if site != selected)
            flattening = sp.zeros(3, 9)
            for index, (hole, local) in enumerate(domain):
                if hole != 0:
                    continue
                column = 3 * local[other[0]] + local[other[1]]
                flattening[local[selected], column] = generator[index]
            require(
                flattening.rank() == 3,
                "flattening.rank() == 3",
            )


def audit_three_site_plane_syzygy():
    """A two-plane diagonal star has one alternating quadratic syzygy."""

    triples = (0, 1, 2)
    edges = tuple(itertools.combinations(triples, 2))
    domain = [
        (edge, left, right)
        for edge in edges
        for left in COLORS
        for right in COLORS
    ]
    rows = []
    for alpha in (1, 2):
        for output in itertools.product(COLORS, repeat=3):
            row = []
            for (u, v), left, right in domain:
                if output[u] != left or output[v] != right:
                    row.append(0)
                    continue
                third = next(site for site in triples if site not in (u, v))
                row.append(int(output[third] == alpha))
            rows.append(row)
    multiplication = sp.Matrix(rows)
    require(
        multiplication.shape == (54, 27),
        "multiplication.shape == (54, 27)",
    )
    require(
        multiplication.rank() == 26,
        "multiplication.rank() == 26",
    )

    wedge = sp.zeros(27, 1)
    edge_sign = {(0, 1): 1, (0, 2): -1, (1, 2): 1}
    for index, (edge, left, right) in enumerate(domain):
        if (left, right) == (1, 2):
            wedge[index] = edge_sign[edge]
        elif (left, right) == (2, 1):
            wedge[index] = -edge_sign[edge]
    require(
        multiplication * wedge == sp.zeros(54, 1),
        "multiplication * wedge == sp.zeros(54, 1)",
    )


def audit_one_defect_erasure_normal_forms():
    """Direct rank audit of the four rank normal forms at every bad site."""

    identity = sp.eye(3)
    for bad_site in SITES:
        for rank in range(4):
            bad_map = sp.diag(*([1] * rank + [0] * (3 - rank)))
            stars = [identity] * 4
            stars[bad_site] = bad_map
            erased = base.erased_hessian_matrix(tuple(stars))
            require(
                erased.rank() == 54,
                "erased.rank() == 54",
            )


def p4_blocks():
    singular_positions = {(0, 0), (0, 1), (1, 0), (2, 2)}
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
                require(
                    matrix.rank() == 2,
                    "matrix.rank() == 2",
                )
            else:
                require(
                    matrix.det() != 0,
                    "matrix.det() != 0",
                )
            blocks[i, j] = matrix
    return blocks


def audit_p4_effective_hessian_identity():
    """Audit the actual mixed sector on P4 plus a disjoint edge."""

    blocks = p4_blocks()
    # Singular positions: 00,01,10,22.  Residual row 3 is invertible and
    # residual row 2 has only the exceptional block B_22.
    left_edge = (0, 1)
    r, s = 3, 2
    c = base.internal_color(*left_edge)

    q_right = {}
    for u, v in EDGES:
        color = base.internal_color(u, v)
        q_right[u, v] = sp.zeros(3)
        q_right[u, v][color, color] = 1

    p0 = {j: blocks[0, j].row(c) for j in SITES}
    p1 = {j: blocks[1, j].row(c) for j in SITES}
    q_effective = {
        (u, v): q_right[u, v] + p0[u].T * p1[v] + p1[u].T * p0[v]
        for u, v in EDGES
    }

    checked = 0
    for x, y in itertools.product(COLORS, repeat=2):
        left_word = (c, c, y, x)
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
            require(
                sp.expand(pulled_back - four_cross - two_cross) == 0,
                "sp.expand(pulled_back - four_cross - two_cross) == 0",
            )
            checked += 1
    require(
        checked == 729,
        "checked == 729",
    )


def audit_exact_four_position_boundary():
    cells = tuple(itertools.product(SITES, repeat=2))

    def degrees(positions, side):
        return tuple(
            sum(position[side] == vertex for position in positions)
            for vertex in SITES
        )

    def old_boundary(positions):
        return all(
            sum(value > 0 for value in degrees(positions, side)) >= 3
            for side in (0, 1)
        )

    def one_defect_excluded(positions):
        for side in (0, 1):
            local = degrees(positions, side)
            if 0 in local and any(value <= 1 for value in local if value != 0):
                return True
        return False

    all_supports = tuple(itertools.combinations(cells, 4))
    require(
        len(all_supports) == 1820,
        "len(all_supports) == 1820",
    )
    after_old = tuple(filter(old_boundary, all_supports))
    require(
        len(after_old) == 1032,
        "len(after_old) == 1032",
    )
    residual = tuple(
        positions
        for positions in after_old
        if not one_defect_excluded(positions)
    )
    require(
        len(residual) == 24,
        "len(residual) == 24",
    )
    require(
        all(
            sorted(degrees(positions, side)) == [1, 1, 1, 1]
            for positions in residual
            for side in (0, 1)
        ),
        "all( sorted(degrees(positions, side)) == [1, 1, 1, 1] for...",
    )


def main():
    audit_one_defect_annihilator()
    audit_three_site_plane_syzygy()
    audit_one_defect_erasure_normal_forms()
    audit_p4_effective_hessian_identity()
    audit_exact_four_position_boundary()
    print("one-defect star annihilators: dimensions 27,1,1,1")
    print("three-site two-plane syzygy: dimension 1")
    print("one-defect six-cell erasure normal forms: rank 54/54")
    print("P4-plus-edge effective-Hessian identity: 729 coefficients")
    print("exact-four position boundary: 1032 -> 24 perfect matchings")
    print("exact-four nonmatching obstruction: PASS")


if __name__ == "__main__":
    main()
