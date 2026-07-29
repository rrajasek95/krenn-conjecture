#!/usr/bin/env python3
"""Exact audit of the all-complement selector bridge countermodel.

The model is not asserted to satisfy the full eight-site GHZ identity.  It
does satisfy, exactly and simultaneously, the one-/three-cross equations
for all eight selector declarations in (18) of the accompanying note.
"""

from collections import Counter
from itertools import combinations, product


P, Q = 0, 1
R = tuple(range(2, 8))
OUTSIDE_LABEL = {vertex: vertex - 2 for vertex in R}


def zero_matrix():
    return [[0 for _ in range(3)] for _ in range(3)]


def add_cell(matrix, row, column, value=1):
    matrix[row][column] += value


def determinant3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
                        - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                          - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                          - matrix[1][1] * matrix[2][0])
    )


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(3))
             for j in range(3)] for i in range(3)]


def is_zero(matrix):
    return not any(value for row in matrix for value in row)


def matrices():
    blocks = {(u, v): zero_matrix()
              for u, v in combinations(range(8), 2)}

    # The invertible three-cycle on pq.
    blocks[P, Q] = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]

    # Conceptual outside labels 0,...,5 are actual vertices 2,...,7.
    r = {label: label + 2 for label in range(6)}
    matching_zero = ((P, r[0]), (Q, r[1]), (r[2], r[3]),
                     (r[4], r[5]))
    matching_one = ((P, r[2]), (Q, r[3]), (r[0], r[4]),
                    (r[1], r[5]))
    for u, v in matching_zero:
        edge = tuple(sorted((u, v)))
        row, column = (0, 0) if u < v else (0, 0)
        add_cell(blocks[edge], row, column)
    for u, v in matching_one:
        edge = tuple(sorted((u, v)))
        row, column = (1, 1) if u < v else (1, 1)
        add_cell(blocks[edge], row, column)

    # p and q are smaller than every outside vertex, so these are row-two
    # additions in the p/q endpoint and arbitrary rows at the outside end.
    a = (1, 1, 1)
    b = (1, 2, 4)
    for u in R:
        for column, value in enumerate(a):
            add_cell(blocks[P, u], 2, column, value)
        for column, value in enumerate(b):
            add_cell(blocks[Q, u], 2, column, value)
    return blocks


A = matrices()


def edge_matrix(u, v):
    if u < v:
        return A[u, v]
    return transpose(A[v, u])


def edge_value(u, v, color_u, color_v):
    return edge_matrix(u, v)[color_u][color_v]


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def selector_sector(s, color, crossing_number, output_word):
    shore = {P, Q, s}
    exposed = tuple(vertex for vertex in range(8) if vertex not in shore)
    coloring = {P: color, Q: color, s: color}
    coloring.update(dict(zip(exposed, output_word)))
    answer = 0
    for matching in perfect_matchings(range(8)):
        crossing = sum((u in shore) != (v in shore) for u, v in matching)
        if crossing != crossing_number:
            continue
        value = 1
        for u, v in matching:
            value *= edge_value(u, v, coloring[u], coloring[v])
        answer += value
    return answer


def full_coefficient(word):
    coloring = dict(enumerate(word))
    answer = 0
    for matching in perfect_matchings(range(8)):
        value = 1
        for u, v in matching:
            value *= edge_value(u, v, coloring[u], coloring[v])
        answer += value
    return answer


def local_l_vector(s, color, u):
    """The coordinate-selector contraction in equation (4)."""
    out = []
    for color_u in range(3):
        out.append(
            edge_value(P, Q, color, color)
            * edge_value(s, u, color, color_u)
            + edge_value(P, s, color, color)
            * edge_value(Q, u, color, color_u)
            + edge_value(Q, s, color, color)
            * edge_value(P, u, color, color_u)
        )
    return tuple(out)


K = (
    ((0, 0, 0), (0, 0, 1), (0, -1, 0)),
    ((0, 0, -1), (0, 0, 0), (1, 0, 0)),
    ((0, 1, 0), (-1, 0, 0), (0, 0, 0)),
)


def cross_matrix(u, color):
    return multiply(multiply(edge_matrix(P, u), K[color]),
                    transpose(edge_matrix(Q, u)))


def scalar_multiple(left, right):
    """Whether two integer matrices are scalar multiples over Q."""
    pairs = [(x, y) for left_row, right_row in zip(left, right)
             for x, y in zip(left_row, right_row)]
    pivot = next(((x, y) for x, y in pairs if y), None)
    if pivot is None:
        return all(x == 0 for x, _ in pairs)
    x0, y0 = pivot
    return all(x * y0 == y * x0 for x, y in pairs)


def derivative_value_on_word(w_vertices, varied_edge, variation, word):
    colors = dict(zip(w_vertices, word))
    complement = tuple(vertex for vertex in w_vertices
                       if vertex not in varied_edge)
    a, b = varied_edge
    c, d = complement
    return (variation[colors[a]][colors[b]]
            * edge_value(c, d, colors[c], colors[d]))


def main():
    assert determinant3(A[P, Q]) == 1

    conceptual = {label: label + 2 for label in range(6)}
    declarations = [
        *((conceptual[s], 0) for s in (2, 3, 4, 5)),
        *((conceptual[s], 1) for s in (0, 1, 4, 5)),
    ]
    for s, color in declarations:
        exposed = tuple(vertex for vertex in range(8)
                        if vertex not in (P, Q, s))
        for word in product(range(3), repeat=5):
            assert selector_sector(s, color, 1, word) == 0
            expected = int(all(entry == color for entry in word))
            assert selector_sector(s, color, 3, word) == expected
        for u in exposed:
            assert local_l_vector(s, color, u) == (0, 0, 0)

    constant_pair_slices = []
    for color in range(3):
        constant_pair_slices.append([
            [full_coefficient((i, j) + (color,) * 6) for j in range(3)]
            for i in range(3)
        ])
    assert constant_pair_slices == [
        [[1, 0, 1], [0, 0, 0], [1, 0, 2]],
        [[0, 0, 0], [0, 1, 2], [0, 1, 4]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ]
    residual = {}
    for word in product(range(3), repeat=8):
        value = full_coefficient(word) - int(len(set(word)) == 1)
        if value:
            residual[word] = value
    assert len(residual) == 56
    distances = Counter(
        8 - max(word.count(color) for color in range(3))
        for word in residual
    )
    assert distances == {0: 1, 1: 4, 2: 10, 3: 12, 4: 17, 5: 12}

    # The common (row 2,row 2) entry is a K-coordinate of a cross b and is
    # nonzero for every outside site and every color.
    expected_cross_entries = (2, -3, 1)
    for u in R:
        for color in range(3):
            matrix = cross_matrix(u, color)
            assert matrix[2][2] == expected_cross_entries[color]
            assert not is_zero(matrix)

    # Every four-set has an absent internal edge.  Vary the complementary
    # cell by E_01; this is killed by that absent edge and is not a gauge
    # block (the physical complementary block is 0, E_00, or E_11).
    e01 = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
    internal_support = {edge for edge in combinations(R, 2)
                        if not is_zero(edge_matrix(*edge))}
    assert len(internal_support) == 4
    audited = 0
    for w_vertices in combinations(R, 4):
        absent = next(edge for edge in combinations(w_vertices, 2)
                      if edge not in internal_support)
        complement = tuple(vertex for vertex in w_vertices
                           if vertex not in absent)
        complement = tuple(sorted(complement))
        assert not scalar_multiple(e01, edge_matrix(*complement))
        for word in product(range(3), repeat=4):
            # J_W(0,Z) has just Z_complement tensor A_absent.
            assert derivative_value_on_word(
                w_vertices, complement, e01, word) == 0
        audited += 1
    assert audited == 15

    print("PASS: eight exact termwise selectors and all 15 excess kernels audited")
    print("PASS: invertible pq and no zero-cross witness in any color")
    print("PASS: exact 56-word uncapped residual and distance profile audited")


if __name__ == "__main__":
    main()
