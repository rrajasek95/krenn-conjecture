#!/usr/bin/env python3
"""Exact two-anchor doubly-good curved-OO counterguard on an alternating C8."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product


VERTICES = tuple(range(8))
COLORS = range(3)
P, Q, R, FOURTH = 0, 2, 4, 3


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def key(u, v, i, j):
    return (u, v, i, j) if u < v else (v, u, j, i)


def add_cell(blocks, u, v, i, j, value=1):
    cell = key(u, v, i, j)
    blocks[cell] = blocks.get(cell, F(0)) + F(value)


def entry(blocks, u, v, i, j):
    return blocks.get(key(u, v, i, j), F(0))


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def matching_tensor(blocks):
    tensor = defaultdict(F)
    supported = []
    for matching in perfect_matchings(VERTICES):
        choices = []
        for u, v in matching:
            cells = [
                (i, j, value)
                for i in COLORS for j in COLORS
                if (value := entry(blocks, u, v, i, j))
            ]
            if not cells:
                choices = []
                break
            choices.append(cells)
        if not choices:
            continue
        supported.append(tuple(tuple(sorted(edge)) for edge in matching))
        for selected in product(*choices):
            word = [None] * 8
            coefficient = F(1)
            for (u, v), (i, j, value) in zip(matching, selected, strict=True):
                word[u], word[v] = i, j
                coefficient *= value
            tensor[tuple(word)] += coefficient
    return {word: value for word, value in tensor.items() if value}, supported


def rational_rank(rows):
    matrix = [[F(value) for value in row] for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot
                for value, pivot in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
    return rank


def direct_matrix(blocks, u, v):
    return [[entry(blocks, u, v, i, j) for j in COLORS] for i in COLORS]


def star_rank(blocks, endpoint, deleted_neighbor):
    residual = [v for v in VERTICES if v not in (endpoint, deleted_neighbor)]
    columns = [(v, colour) for v in residual for colour in COLORS]
    rows = [
        [entry(blocks, endpoint, v, row, colour) for v, colour in columns]
        for row in COLORS
    ]
    return rational_rank(rows)


def local_star_map(blocks, endpoint, site):
    return [
        [entry(blocks, endpoint, site, endpoint_colour, physical_colour)
         for endpoint_colour in COLORS]
        for physical_colour in COLORS
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix, strict=True)]


def matmul(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def wedge_matrix(blocks, endpoints, site, target):
    first = local_star_map(blocks, endpoints[0], site)
    second = local_star_map(blocks, endpoints[1], site)
    j = [[F(0) for _ in COLORS] for _ in COLORS]
    other = [colour for colour in COLORS if colour != target]
    i, k = other
    permutation = (i, k, target)
    inversions = sum(
        permutation[a] > permutation[b]
        for a in range(3) for b in range(a + 1, 3)
    )
    sign = -1 if inversions % 2 else 1
    j[i][k], j[k][i] = F(sign), F(-sign)
    return matmul(matmul(transpose(first), j), second)


def build_packet():
    blocks = {}
    # Alternating C8 matchings: even-start edges carry colour 0, odd-start
    # edges colour 2.
    for start in range(0, 8, 2):
        add_cell(blocks, start, (start + 1) % 8, 0, 0)
    for start in range(1, 8, 2):
        add_cell(blocks, start, (start + 1) % 8, 2, 2)

    # A triangle on one bipartition shore.  No perfect matching can use any
    # of these edges, but they carry the OO structural packet.
    add_cell(blocks, P, Q, 1, 0)
    add_cell(blocks, P, R, 1, 1)
    add_cell(blocks, Q, R, 1, 1)
    return blocks


def audit_ruling(blocks, endpoints, head):
    residual = [site for site in VERTICES if site not in endpoints]
    nonzero = []
    for site in residual:
        matrix = wedge_matrix(blocks, endpoints, site, 2)
        require(
            all(matrix[row][column] == 0 for row in COLORS for column in COLORS if column != head),
            f"target-2 RR alignment failed at {endpoints}, site {site}",
        )
        if any(matrix[row][head] for row in COLORS):
            nonzero.append(site)
    return tuple(nonzero)


def main():
    blocks = build_packet()
    tensor, supported = matching_tensor(blocks)
    require(tensor == {(0,) * 8: F(1), (2,) * 8: F(1)}, "tensor is no longer X0+X2")
    require(len(supported) == 2, "a shore-triangle edge entered a perfect matching")

    pq, pr = direct_matrix(blocks, P, Q), direct_matrix(blocks, P, R)
    require(rational_rank(pq) == rational_rank(pr) == 1, "OO arm rank changed")
    require(
        {column for row in COLORS for column in COLORS if pq[row][column]} == {0},
        "pq head changed",
    )
    require(
        {column for row in COLORS for column in COLORS if pr[row][column]} == {1},
        "pr head changed",
    )

    ranks = (
        star_rank(blocks, P, Q), star_rank(blocks, Q, P),
        star_rank(blocks, P, R), star_rank(blocks, R, P),
    )
    require(ranks == (3, 3, 3, 3), "two-anchor good-star ranks changed")

    curvature = (
        entry(blocks, P, Q, 1, 0) * entry(blocks, R, FOURTH, 1, 0)
        - entry(blocks, P, R, 1, 1) * entry(blocks, Q, FOURTH, 0, 0)
    )
    require(curvature == -1, "two-anchor curvature changed")

    pq_nonzero = audit_ruling(blocks, (P, Q), 0)
    pr_nonzero = audit_ruling(blocks, (P, R), 1)
    require(pq_nonzero == (), "pq target-2 alignment changed")
    require(pr_nonzero == (Q,), "pr target-2 alignment changed")

    # H=X0+X2 makes both diagonal rows exact and every off-diagonal row zero
    # in every pair chart.  The missing diagonal target is exactly X1.
    require((1,) * 8 not in tensor, "missing X1 anchor unexpectedly appeared")

    print("doubly-good curved OO two-anchor counterguard: PASS")
    print("matching tensor=X0+X2; exactly two supported physical matchings")
    print(f"star ranks={ranks}; curvature={curvature}")
    print(f"target-2 RR nonzero sites: pq={pq_nonzero}, pr={pr_nonzero}")
    print("all off-diagonal rows vanish; the sole missing target is X1")


if __name__ == "__main__":
    main()
