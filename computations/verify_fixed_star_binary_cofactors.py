#!/usr/bin/env python3
"""Audit the actual common-cofactor star in the binary cancellation source.

This is the example in ``notes/fixed-star-common-cofactor-rigidity.md``.
All cofactors are recomputed from one shared edge dictionary; they are not
supplied as independent star slices.
"""

from __future__ import annotations

from itertools import product


VERTICES = tuple(range(1, 7))
COLORS = (0, 1)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


# Endpoint colors are listed in increasing-vertex order.
EDGES = {
    (1, 2): {(0, 0): 1, (1, 0): 1},
    (3, 4): {(0, 0): 1},
    (5, 6): {(0, 0): 1},
    (1, 3): {(1, 0): -1},
    (2, 4): {(0, 0): 1},
    (1, 6): {(1, 1): 1},
    (2, 3): {(1, 1): 1},
    (4, 5): {(1, 1): 1},
}


def edge_value(edges, u, v, coloring):
    if u > v:
        u, v = v, u
    return edges.get((u, v), {}).get((coloring[u], coloring[v]), 0)


def coefficient(edges, vertices, coloring_tuple):
    coloring = dict(zip(vertices, coloring_tuple))
    total = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for u, v in matching:
            term *= edge_value(edges, u, v, coloring)
        total += term
    return total


def induced_tensor(edges, vertices):
    return {
        coloring: value
        for coloring in product(COLORS, repeat=len(vertices))
        if (value := coefficient(edges, vertices, coloring)) != 0
    }


def supported_matchings(edges):
    answer = []
    for matching in perfect_matchings(VERTICES):
        if all(tuple(sorted(edge)) in edges for edge in matching):
            answer.append(tuple(tuple(sorted(edge)) for edge in matching))
    return answer


def verify_full_tensor(edges):
    for coloring in product(COLORS, repeat=len(VERTICES)):
        expected = int(len(set(coloring)) == 1)
        actual = coefficient(edges, VERTICES, coloring)
        assert actual == expected, (coloring, actual, expected)


def verify_common_cofactor_star():
    p = 1
    remainder = tuple(v for v in VERTICES if v != p)
    cofactors = {
        j: induced_tensor(EDGES, tuple(v for v in remainder if v != j))
        for j in remainder
    }

    assert cofactors[2] == {(0, 0, 0, 0): 1}
    assert cofactors[3] == {(0, 0, 0, 0): 1}
    assert cofactors[6] == {(1, 1, 1, 1): 1}

    # Reassemble each contracted p-row from those actual cofactors.
    for p_color in COLORS:
        for remainder_coloring in product(COLORS, repeat=len(remainder)):
            colors = dict(zip(remainder, remainder_coloring))
            total = 0
            for j in remainder:
                cell = EDGES.get((p, j), {}).get((p_color, colors[j]), 0)
                complement = tuple(v for v in remainder if v != j)
                complement_coloring = tuple(colors[v] for v in complement)
                total += cell * cofactors[j].get(complement_coloring, 0)
            expected = int(all(color == p_color for color in remainder_coloring))
            assert total == expected, (p_color, remainder_coloring, total)

    # The two wrong-color derivative tensors have the same singleton color
    # and the same pure complementary tensor.  Their current weights +1,-1
    # cancel in the row-one equation.
    assert EDGES[(1, 2)][(1, 0)] == 1
    assert EDGES[(1, 3)][(1, 0)] == -1
    assert cofactors[2] == cofactors[3]


def verify_support_reduction():
    reduced = {edge: dict(cells) for edge, cells in EDGES.items()}
    del reduced[(1, 2)][(1, 0)]
    del reduced[(1, 3)]
    verify_full_tensor(reduced)
    assert supported_matchings(reduced) == [
        ((1, 2), (3, 4), (5, 6)),
        ((1, 6), (2, 3), (4, 5)),
    ]


def main():
    verify_full_tensor(EDGES)
    assert supported_matchings(EDGES) == [
        ((1, 2), (3, 4), (5, 6)),
        ((1, 3), (2, 4), (5, 6)),
        ((1, 6), (2, 3), (4, 5)),
    ]
    verify_common_cofactor_star()
    verify_support_reduction()
    print("verified all 64 binary coefficients from one edge system")
    print("verified common cofactors C2=C3=e0^4 and C6=e1^4")
    print("verified both fixed-star row equations and support reduction")


if __name__ == "__main__":
    main()
