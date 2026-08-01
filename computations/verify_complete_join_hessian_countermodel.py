#!/usr/bin/env python3
"""Exact n=8 countermodel to endpoint-line injectivity from Hessians.

The rank-at-least-two graph is K4 disjoint union K4.  Every cross block is
rank one and has full coordinate support at both endpoints, while the
endpoint-4 factors on 04 and 14 are the same projective line.  Nevertheless
all 28 pair-deleted six-site Hessians have rank 130 in a 135-dimensional
domain modulo 1,000,003.  The five universal gauges are independent and
killed, proving exact characteristic-zero gauge rigidity.
"""

from __future__ import annotations

from itertools import combinations, product


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


PRIME = 1_000_003
VERTICES = tuple(range(8))
LEFT = frozenset(range(4))
RIGHT = frozenset(range(4, 8))
COLORS = range(3)

CROSS_FACTORS = {
    (0, 4): ((18, 1, 28), (1, 1, 1)),
    (0, 5): ((9, 6, 34), (10, 29, 1)),
    (0, 6): ((10, 16, 19), (12, 34, 9)),
    (0, 7): ((3, 28, 35), (30, 34, 5)),
    (1, 4): ((21, 12, 22), (1, 1, 1)),
    (1, 5): ((38, 37, 25), (33, 17, 31)),
    (1, 6): ((30, 4, 29), (7, 30, 21)),
    (1, 7): ((28, 28, 29), (36, 32, 31)),
    (2, 4): ((12, 14, 33), (29, 39, 31)),
    (2, 5): ((20, 39, 2), (6, 15, 18)),
    (2, 6): ((28, 19, 32), (36, 20, 17)),
    (2, 7): ((17, 12, 8), (31, 31, 32)),
    (3, 4): ((2, 7, 22), (32, 34, 18)),
    (3, 5): ((15, 37, 35), (39, 9, 22)),
    (3, 6): ((14, 35, 19), (38, 25, 39)),
    (3, 7): ((14, 3, 38), (38, 8, 34)),
}

INTERNAL_BLOCKS = {
    (0, 1): ((17, 9, 1), (35, 19, 30), (17, 11, 9)),
    (0, 2): ((4, 20, 4), (36, 13, 37), (31, 15, 25)),
    (0, 3): ((5, 18, 38), (17, 28, 21), (1, 28, 9)),
    (1, 2): ((15, 2, 34), (10, 29, 31), (11, 10, 21)),
    (1, 3): ((33, 39, 18), (13, 19, 5), (28, 6, 32)),
    (2, 3): ((4, 7, 35), (7, 8, 21), (35, 7, 29)),
    (4, 5): ((20, 10, 8), (27, 39, 18), (31, 23, 33)),
    (4, 6): ((4, 17, 2), (6, 35, 23), (11, 9, 4)),
    (4, 7): ((27, 12, 3), (16, 16, 28), (36, 6, 29)),
    (5, 6): ((33, 23, 14), (18, 11, 10), (15, 25, 28)),
    (5, 7): ((28, 36, 38), (28, 39, 12), (19, 33, 9)),
    (6, 7): ((8, 23, 7), (27, 31, 34), (3, 26, 25)),
}


def outer(left, right):
    return tuple(tuple(x * y % PRIME for y in right) for x in left)


BLOCKS = dict(INTERNAL_BLOCKS)
BLOCKS.update({
    edge: outer(left, right)
    for edge, (left, right) in CROSS_FACTORS.items()
})


def determinant(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % PRIME


def rank_mod(rows):
    values = [[entry % PRIME for entry in row] for row in rows]
    rank = 0
    for column in range(len(values[0])):
        pivot = next(
            (row for row in range(rank, len(values)) if values[row][column]),
            None,
        )
        if pivot is None:
            continue
        values[rank], values[pivot] = values[pivot], values[rank]
        inverse = pow(values[rank][column], PRIME - 2, PRIME)
        for row in range(rank + 1, len(values)):
            if not values[row][column]:
                continue
            multiple = values[row][column] * inverse % PRIME
            values[row] = [
                (entry - multiple * pivot_entry) % PRIME
                for entry, pivot_entry in zip(
                    values[row], values[rank], strict=True
                )
            ]
        rank += 1
        if rank == len(values):
            break
    return rank


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(remainder):
            yield ((min(first, second), max(first, second)),) + matching


def block_entry(left, left_color, right, right_color):
    edge = (min(left, right), max(left, right))
    if left < right:
        return BLOCKS[edge][left_color][right_color]
    return BLOCKS[edge][right_color][left_color]


def hessian_columns(remaining):
    """Columns of Z -> Z q^2/2 on the named six sites."""
    remaining = tuple(remaining)
    local_index = {vertex: index for index, vertex in enumerate(remaining)}
    words = tuple(product(COLORS, repeat=6))
    word_index = {word: index for index, word in enumerate(words)}
    labels = tuple(
        (left, right, a, b)
        for left, right in combinations(remaining, 2)
        for a, b in product(COLORS, repeat=2)
    )
    columns = []
    for left, right, a, b in labels:
        rest = tuple(
            vertex for vertex in remaining if vertex not in (left, right)
        )
        column = [0] * len(words)
        for matching in perfect_matchings(rest):
            for rest_colors in product(COLORS, repeat=4):
                coloring = dict(zip(rest, rest_colors, strict=True))
                value = 1
                for first, second in matching:
                    value *= block_entry(
                        first, coloring[first], second, coloring[second]
                    )
                    value %= PRIME
                word = [0] * 6
                word[local_index[left]] = a
                word[local_index[right]] = b
                for vertex in rest:
                    word[local_index[vertex]] = coloring[vertex]
                index = word_index[tuple(word)]
                column[index] = (column[index] + value) % PRIME
        columns.append(column)
    return labels, columns


def gauge_vectors(remaining, labels):
    remaining = tuple(remaining)
    vectors = []
    for distinguished in remaining[:-1]:
        alpha = {vertex: 0 for vertex in remaining}
        alpha[distinguished] = 1
        alpha[remaining[-1]] = -1
        vector = []
        for left, right, a, b in labels:
            scalar = alpha[left] + alpha[right]
            vector.append(scalar * block_entry(left, a, right, b) % PRIME)
        vectors.append(vector)
    return vectors


def apply_columns(columns, coefficients):
    output = [0] * len(columns[0])
    for coefficient, column in zip(coefficients, columns, strict=True):
        if not coefficient:
            continue
        for index, entry in enumerate(column):
            output[index] = (output[index] + coefficient * entry) % PRIME
    return output


def coloring_coefficient(word):
    total = 0
    for matching in perfect_matchings(VERTICES):
        value = 1
        for left, right in matching:
            value *= block_entry(left, word[left], right, word[right])
        total += value
    return total


def main():
    require(
        set(BLOCKS) == set(combinations(VERTICES, 2)),
        "set(BLOCKS) == set(combinations(VERTICES, 2))",
    )
    require(
        all(determinant(matrix) for matrix in INTERNAL_BLOCKS.values()),
        "all(determinant(matrix) for matrix in INTERNAL_BLOCKS.val...",
    )
    require(
        all(
            (edge[0] in LEFT) != (edge[1] in LEFT)
            for edge in CROSS_FACTORS
        ),
        "all( (edge[0] in LEFT) != (edge[1] in LEFT) for edge in C...",
    )
    require(
        all(
            all(entry for entry in factor)
            for factors in CROSS_FACTORS.values()
            for factor in factors
        ),
        "all( all(entry for entry in factor) for factors in CROSS_...",
    )

    # The fixed-mask conclusion holds with the full mask at every endpoint.
    # The endpoint-4 lines of 04 and 14 actually coincide.
    require(
        CROSS_FACTORS[0, 4][1] == CROSS_FACTORS[1, 4][1] == (1, 1, 1),
        "CROSS_FACTORS[0, 4][1] == CROSS_FACTORS[1, 4][1] == (1, 1...",
    )

    ranks = []
    for deleted in combinations(VERTICES, 2):
        remaining = tuple(vertex for vertex in VERTICES if vertex not in deleted)
        labels, columns = hessian_columns(remaining)
        gauges = gauge_vectors(remaining, labels)
        require(
            len(columns) == 135,
            "len(columns) == 135",
        )
        require(
            rank_mod(columns) == 130,
            "rank_mod(columns) == 130",
        )
        require(
            rank_mod(gauges) == 5,
            "rank_mod(gauges) == 5",
        )
        require(
            all(not any(apply_columns(columns, gauge)) for gauge in gauges),
            "all(not any(apply_columns(columns, gauge)) for gauge in g...",
        )
        ranks.append(130)
    require(
        len(ranks) == 28,
        "len(ranks) == 28",
    )

    mixed_coefficient = coloring_coefficient((1, 0, 0, 0, 0, 0, 0, 0))
    require(
        mixed_coefficient > 0,
        "mixed_coefficient > 0",
    )

    print("verified S=K4 disjoint-union K4 with a complete full-mask rank-one join")
    print("verified repeated endpoint line on 04 and 14")
    print("verified 28/28 Hessians: rank 130/135, gauge dimension 5")
    print(f"non-target mixed coefficient={mixed_coefficient}")
    print("PASS: gauge rigidity does not force complete-join line injectivity")


if __name__ == "__main__":
    main()
