#!/usr/bin/env python3
"""Exact audits for two-k4-four-singular-row-obstruction.md."""

from __future__ import annotations

import itertools
from functools import reduce

import sympy as sp


SITES = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(SITES, 2))
WORDS = tuple(itertools.product(COLORS, repeat=4))


def internal_color(u, v):
    return (1, 2, 3).index(u ^ v)


def permanent(matrix):
    return sum(
        reduce(
            lambda value, i: value * matrix[i][permutation[i]],
            range(len(matrix)),
            sp.S.One,
        )
        for permutation in itertools.permutations(range(len(matrix)))
    )


def common_star_annihilator():
    # Degree-three tensors are indexed by their missing site.  Multiplication
    # by the diagonal star s_y inserts color y at that site.
    domain = []
    for hole in SITES:
        present = tuple(site for site in SITES if site != hole)
        for word in itertools.product(COLORS, repeat=3):
            domain.append((hole, dict(zip(present, word, strict=True))))

    rows = []
    for y in COLORS:
        for output in WORDS:
            rows.append([
                int(
                    output[hole] == y
                    and all(output[site] == local[site] for site in local)
                )
                for hole, local in domain
            ])
    multiplication = sp.Matrix(rows)
    assert multiplication.shape == (243, 108)
    assert multiplication.rank() == 107

    # The unique kernel is the alternating four-vector syzygy: at a hole,
    # the other three colors must be a permutation of 0,1,2.
    omega = sp.zeros(len(domain), 1)
    for index, (hole, local) in enumerate(domain):
        present = tuple(site for site in SITES if site != hole)
        permutation = tuple(local[site] for site in present)
        if set(permutation) != set(COLORS):
            continue
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        omega[index] = (-1) ** (hole + inversions)
    assert multiplication * omega == sp.zeros(243, 1)
    assert omega != sp.zeros(108, 1)

    # Every nonzero hole component is Det_3 and has all local mode ranks 3.
    for hole in SITES:
        present = tuple(site for site in SITES if site != hole)
        for selected in present:
            other = tuple(site for site in present if site != selected)
            flattening = sp.zeros(3, 9)
            for index, (stored_hole, local) in enumerate(domain):
                if stored_hole != hole:
                    continue
                column = 3 * local[other[0]] + local[other[1]]
                flattening[local[selected], column] = omega[index]
            assert flattening.rank() == 3


def full_support_linear_kernel():
    # Normalize p_i=e_0 at every site.  Audit multiplication R_2 -> R_3.
    domain = [
        (edge, left, right)
        for edge in EDGES
        for left in COLORS
        for right in COLORS
    ]
    codomain = []
    for hole in SITES:
        present = tuple(site for site in SITES if site != hole)
        for word in itertools.product(COLORS, repeat=3):
            codomain.append((hole, dict(zip(present, word, strict=True))))

    rows = []
    for hole, output in codomain:
        row = []
        for (u, v), a, b in domain:
            if hole in (u, v) or output[u] != a or output[v] != b:
                row.append(0)
                continue
            third = next(site for site in SITES if site not in (hole, u, v))
            row.append(int(output[third] == 0))
        rows.append(row)
    multiplication = sp.Matrix(rows)
    assert multiplication.shape == (108, 54)
    assert multiplication.rank() == 52

    # The exact kernel consists of q_ij=z_ij e_0 e_0 with all triangle
    # sums zero.  The scalar triangle system has dimension two.
    triangles = sp.Matrix([
        [int(edge.issubset(set(triple))) for edge in map(frozenset, EDGES)]
        for triple in itertools.combinations(SITES, 3)
    ])
    assert triangles.rank() == 4
    scalar_kernel = triangles.nullspace()
    assert len(scalar_kernel) == 2
    lifted = []
    for scalar in scalar_kernel:
        vector = sp.zeros(54, 1)
        for edge_index, value in enumerate(scalar):
            vector[edge_index * 9] = value
        assert multiplication * vector == sp.zeros(108, 1)
        lifted.append(vector)
    assert sp.Matrix.hstack(*lifted).rank() == 2


def erased_hessian_matrix(relative_stars):
    # P_i=I after independent local changes of basis.  Retain only x=1,2,
    # the two rows complementary to the exceptional input color c=0.
    domain = [
        (edge, left, right)
        for edge in EDGES
        for left in COLORS
        for right in COLORS
    ]
    rows = []
    for x in (1, 2):
        for y in COLORS:
            for output in WORDS:
                row = []
                for (u, v), a, b in domain:
                    if output[u] != a or output[v] != b:
                        row.append(0)
                        continue
                    i, j = tuple(site for site in SITES if site not in (u, v))
                    value = (
                        int(output[i] == x) * relative_stars[j][output[j], y]
                        + relative_stars[i][output[i], y] * int(output[j] == x)
                    )
                    row.append(value)
                if any(row):
                    rows.append(row)
    return sp.Matrix(rows)


def audit_erasure_specializations():
    identity = sp.eye(3)
    canonical = erased_hessian_matrix((identity,) * 4)
    assert canonical.rank() == 54

    relative = (
        sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[2, 1, 1], [1, 1, 0], [0, 1, 1]]),
        sp.Matrix([[1, 0, 1], [1, 2, 0], [0, 1, 1]]),
    )
    assert all(matrix.det() != 0 for matrix in relative)
    assert erased_hessian_matrix(relative).rank() == 54


def block_rows():
    # Only the two residual rows 2,3 are invertible.  Rows 0,1 are chosen
    # singular to emphasize that the proof imposes no hypothesis on them.
    blocks = {}
    for i in (0, 1):
        for j in SITES:
            blocks[i, j] = sp.Matrix([
                [1 + i, j + 1, 0],
                [0, 1, j + 2 + i],
                [0, 0, 0],
            ])
            assert blocks[i, j].rank() == 2
    for i in (2, 3):
        for j in SITES:
            blocks[i, j] = sp.Matrix([
                [1 + i, j, 1],
                [1, 2 + j, i],
                [j + 1, 1, 3 + i + j],
            ])
            if blocks[i, j].det() == 0:
                blocks[i, j][2, 2] += 1
            assert blocks[i, j].det() != 0
    return blocks


def beta_coefficient(q, p, s, output):
    value = 0
    for u, v in EDGES:
        i, j = tuple(site for site in SITES if site not in (u, v))
        value += q[u, v][output[u], output[v]] * (
            p[i][output[i]] * s[j][output[j]]
            + s[i][output[i]] * p[j][output[j]]
        )
    return sp.expand(value)


def audit_two_k4_sector_identity():
    blocks = block_rows()
    t, r, s = 1, 2, 3
    c = internal_color(0, t)
    assert c == 0 and internal_color(r, s) == c

    q_right = {}
    for u, v in EDGES:
        color = internal_color(u, v)
        q_right[u, v] = sp.zeros(3)
        q_right[u, v][color, color] = 1

    p0 = {j: blocks[0, j].row(c) for j in SITES}
    pt = {j: blocks[t, j].row(c) for j in SITES}
    q_effective = {}
    for u, v in EDGES:
        q_effective[u, v] = (
            q_right[u, v] + p0[u].T * pt[v] + pt[u].T * p0[v]
        )

    checked = 0
    for x, y in itertools.product(COLORS, repeat=2):
        left_word = [None] * 4
        left_word[0] = left_word[t] = c
        left_word[r], left_word[s] = x, y
        left_word = tuple(left_word)
        pr = {j: blocks[r, j].row(x) for j in SITES}
        ps = {j: blocks[s, j].row(y) for j in SITES}
        for right_word in WORDS:
            four_cross = permanent([
                [blocks[i, j][left_word[i], right_word[j]] for j in SITES]
                for i in SITES
            ])
            two_cross = 0
            for u, v in EDGES:
                color = internal_color(u, v)
                if right_word[u] != color or right_word[v] != color:
                    continue
                remaining = tuple(site for site in SITES if site not in (u, v))
                two_cross += permanent([
                    [blocks[i, j][left_word[i], right_word[j]] for j in remaining]
                    for i in (r, s)
                ])
            pulled_back = beta_coefficient(q_effective, pr, ps, right_word)
            assert sp.expand(pulled_back - four_cross - two_cross) == 0
            checked += 1
    assert checked == 9 * 81

    # If q_eff vanished, every endpoint line of the three incident right-K4
    # blocks at a site would lie in the two-plane spanned by p0 and pt there.
    # The actual three endpoint lines are the three coordinate axes.
    for site in SITES:
        incident = [
            sp.eye(3).col(internal_color(site, other))
            for other in SITES
            if other != site
        ]
        assert sp.Matrix.hstack(*incident).rank() == 3
        assert sp.Matrix.hstack(p0[site].T, pt[site].T).rank() <= 2


def main():
    common_star_annihilator()
    full_support_linear_kernel()
    audit_erasure_specializations()
    audit_two_k4_sector_identity()
    print("common invertible-star annihilator: dimension 1 (alternating Det_3)")
    print("full-support linear multiplication kernel: dimension 2")
    print("six-cell Hessian erasure maps: rank 54/54")
    print("two-K4 effective-Hessian sector identity: 729 coefficients")
    print("two completely invertible block rows obstruction: PASS")


if __name__ == "__main__":
    main()
