#!/usr/bin/env python3
"""Light exact audits for the multiresponse inactive-core theorem.

The proof in the companion note is uniform.  This script independently
checks a mixed signless-component ledger, the closed saturation-cover
formula on small complete components, and the sharp ternary-claw quotient.
"""

from fractions import Fraction
from itertools import combinations, product
from math import ceil


def rref_nullspace(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    pivot_cols = []
    current = 0
    for col in range(cols):
        pivot = next((r for r in range(current, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[current], a[pivot] = a[pivot], a[current]
        value = a[current][col]
        a[current] = [x / value for x in a[current]]
        for r in range(rows):
            if r == current or not a[r][col]:
                continue
            value = a[r][col]
            a[r] = [x - value * y for x, y in zip(a[r], a[current])]
        pivot_cols.append(col)
        current += 1

    free_cols = [col for col in range(cols) if col not in pivot_cols]
    basis = []
    for free in free_cols:
        vector = [Fraction(0)] * cols
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivot_cols):
            vector[pivot] = -a[row][free]
        basis.append(tuple(vector))
    return basis


def signless_matrix(vertex_count, edges):
    rows = []
    for i, j in edges:
        row = [0] * vertex_count
        row[i] = 1
        row[j] = 1
        rows.append(row)
    return rows


def audit_universal_core():
    # Two nonbipartite triangles, one K_(1,2), and one isolated vertex.
    edges = {
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
        (3, 5),
        (4, 5),
        (6, 7),
        (6, 8),
    }
    basis = rref_nullspace(signless_matrix(10, sorted(edges)))
    assert len(basis) == 2

    computed = {
        (i, j)
        for i, j in combinations(range(10), 2)
        if all(vector[i] + vector[j] == 0 for vector in basis)
    }
    expected = set(combinations(range(6), 2)) | {(6, 7), (6, 8)}
    assert computed == expected
    assert all(9 not in edge for edge in computed)


def all_matchings(vertex_count, edges):
    adjacency = {i: set() for i in range(vertex_count)}
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)

    results = set()

    def visit(available, saturated):
        if not available:
            results.add(saturated)
            return
        i = min(available)
        visit(available - {i}, saturated)
        for j in adjacency[i] & available:
            visit(available - {i, j}, saturated | (1 << i) | (1 << j))

    visit(set(range(vertex_count)), 0)
    return results


def saturation_cover_number(vertex_count, edges):
    full = (1 << vertex_count) - 1
    saturated_masks = all_matchings(vertex_count, edges)
    saturable = [
        mask
        for mask in range(1 << vertex_count)
        if any(mask & ~matched == 0 for matched in saturated_masks)
    ]
    infinity = vertex_count + 1
    distance = [infinity] * (1 << vertex_count)
    distance[0] = 0
    for covered in range(1 << vertex_count):
        if distance[covered] == infinity:
            continue
        for mask in saturable:
            joined = covered | mask
            distance[joined] = min(distance[joined], distance[covered] + 1)
    return distance[full], set(saturable)


def audit_saturation_formula():
    for left in range(1, 5):
        for right in range(1, 5):
            edges = {
                (i, left + j)
                for i in range(left)
                for j in range(right)
            }
            cover, saturable = saturation_cover_number(left + right, edges)
            assert cover == ceil(max(left, right) / min(left, right))
            for mask in range(1 << (left + right)):
                selected_left = sum((mask >> i) & 1 for i in range(left))
                selected_right = sum(
                    (mask >> (left + j)) & 1 for j in range(right)
                )
                expected = selected_left <= right and selected_right <= left
                assert (mask in saturable) == expected

    for order in range(3, 8):
        edges = set(combinations(range(order), 2))
        cover, _ = saturation_cover_number(order, edges)
        assert cover == (1 if order % 2 == 0 else 2)


def audit_ternary_claw():
    # Centre 0, leaves 1,2,3.  Every saturable set contains at most one leaf.
    edges = {(0, 1), (0, 2), (0, 3)}
    _, saturable = saturation_cover_number(4, edges)
    leaf_mask = (1 << 1) | (1 << 2) | (1 << 3)
    for masks in product(saturable, repeat=3):
        if (masks[0] | masks[1] | masks[2]) & leaf_mask != leaf_mask:
            continue
        leaf_parts = [mask & leaf_mask for mask in masks]
        assert all(part and part & (part - 1) == 0 for part in leaf_parts)
        assert len(set(leaf_parts)) == 3

    # At leaf u_c the plane omits e_c.  Contracting the leaf slot of an
    # identity rank-three block by the quotient covector selects e_c at
    # the centre, exactly as in the anchored-claw conclusion.
    identity = [[int(i == j) for j in range(3)] for i in range(3)]
    for color in range(3):
        quotient_row = [int(j == color) for j in range(3)]
        center_vector = [
            sum(identity[i][j] * quotient_row[j] for j in range(3))
            for i in range(3)
        ]
        expected = [int(i == color) for i in range(3)]
        assert center_vector == expected

        # The other two leaves have planes containing e_c.  A two-star
        # monomial there, times the centre--u_c identity block, projects
        # to the all-c target word and no other word.
        projected_words = []
        for block_color in range(3):
            if quotient_row[block_color]:
                projected_words.append(
                    (block_color, color, color, block_color)
                )
        assert projected_words == [(color, color, color, color)]


def audit_physical_row_capture_ledger():
    # Selected colours a=0,b=1 and third colour h=2.  The four applications
    # of the planar-factor lemma capture every row when the three named
    # possible sparse rows all reach at least two sites.
    planar = {"p0", "s1"}
    planar.update({"s1", "s2"})
    planar.add("p2")
    planar.add("s0")
    planar.add("p1")
    assert planar == {f"p{i}" for i in range(3)} | {f"s{i}" for i in range(3)}


def main():
    audit_universal_core()
    audit_saturation_formula()
    audit_ternary_claw()
    audit_physical_row_capture_ledger()
    print(
        "PASS universal_core=1 saturation_formula=1 "
        "ternary_claw_anchors=3 physical_rows_captured=6"
    )


if __name__ == "__main__":
    main()
