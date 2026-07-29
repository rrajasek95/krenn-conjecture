#!/usr/bin/env python3
"""Lightweight exact audit for the Kruskal-visible Wick rank gap."""

from fractions import Fraction
from itertools import combinations, product


N = 6
VERTICES = tuple(range(N))
M0 = frozenset(((0, 1), (2, 3), (4, 5)))
M1 = frozenset(((0, 1), (2, 4), (3, 5)))
M2 = frozenset(((0, 2), (3, 4), (1, 5)))
SELECTED = (M0, M1, M2)
EDGE_COLOR = {
    **{edge: 0 for edge in ((0, 1), (2, 3), (4, 5))},
    **{edge: 1 for edge in ((2, 4), (3, 5))},
    **{edge: 2 for edge in ((0, 2), (3, 4), (1, 5))},
}
SUPPORT = frozenset(EDGE_COLOR)


def perfect_matchings(vertices):
    """Generate perfect matchings as sorted endpoint pairs."""
    vertices = tuple(vertices)
    if not vertices:
        yield frozenset()
        return
    u = vertices[0]
    for index, v in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield frozenset(((u, v),)) | tail


def rank(matrix):
    """Exact rational row rank of a small integer matrix."""
    rows = [[Fraction(value) for value in row] for row in matrix]
    if not rows:
        return 0
    height, width = len(rows), len(rows[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, height) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(height):
            if row != pivot_row and rows[row][column]:
                scale = rows[row][column]
                rows[row] = [
                    entry - scale * base
                    for entry, base in zip(rows[row], rows[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def kruskal_rank(columns):
    """Kruskal rank of a short list of column vectors."""
    for size in range(1, len(columns) + 1):
        for chosen in combinations(columns, size):
            matrix = [[column[row] for column in chosen] for row in range(3)]
            if rank(matrix) < size:
                return size - 1
    return len(columns)


def matching_word(matching):
    word = [None] * N
    for u, v in matching:
        color = EDGE_COLOR[(u, v)]
        word[u] = word[v] = color
    return tuple(word)


def flattening_rank(words, shore):
    """Rank a sparse 3|3 flattening using only the listed nonzero words."""
    shore = tuple(shore)
    other = tuple(vertex for vertex in VERTICES if vertex not in shore)
    labels = tuple(product(range(3), repeat=3))
    position = {label: index for index, label in enumerate(labels)}
    matrix = [[0] * 27 for _ in range(27)]
    for word in words:
        left = tuple(word[vertex] for vertex in shore)
        right = tuple(word[vertex] for vertex in other)
        matrix[position[left]][position[right]] += 1
    return rank(matrix)


def main():
    # Dimension alone makes the all-k_v=3 criterion exact up to S=n.
    for n in range(6, 22, 2):
        for terms in range(3, n + 1):
            assert 3 * n >= 2 * terms + n - 1
        assert 3 * n < 2 * (n + 1) + n - 1

    # Three supermodes can certify longer general-position expansions.
    def supermode_range(part_sizes):
        dimensions = tuple(3**size for size in part_sizes)
        return tuple(
            terms
            for terms in range(3, 101)
            if sum(min(terms, dimension) for dimension in dimensions)
            >= 2 * terms + 2
        )

    assert supermode_range((2, 2, 2)) == tuple(range(3, 13))
    assert supermode_range((2, 3, 3)) == tuple(range(3, 31))

    # Failure of the three-way threshold forces total Kruskal deficiency
    # at least S-1 and a circuit on one shore of the claimed maximum size.
    for terms in range(3, 101):
        maximum_sum = 2 * terms + 1
        circuit_bound = maximum_sum // 3 + 1
        assert 3 * terms - maximum_sum == terms - 1
        assert 3 * circuit_bound > maximum_sum

    # If a physical matching contributes two or three of S=3 decorated
    # terms, only one edge block can have rank >1; all other factors repeat.
    for m in range(3, 11):
        for block_ranks in product((1, 2, 3), repeat=m):
            decorated = 1
            for block_rank in block_ranks:
                decorated *= block_rank
            if 1 < decorated <= 3:
                assert sum(block_rank > 1 for block_rank in block_ranks) == 1
                assert sum(block_rank == 1 for block_rank in block_ranks) >= 2

    matchings = tuple(perfect_matchings(VERTICES))
    assert len(matchings) == 15
    supported = tuple(matching for matching in matchings if matching <= SUPPORT)
    assert set(supported) == set(SELECTED)

    # At six sites, every three pairwise disjoint one-factors already support
    # a fourth.  This is a finite boundary audit of the uniform graph lemma.
    disjoint_triples = 0
    for triple in combinations(matchings, 3):
        if any(left & right for left, right in combinations(triple, 2)):
            continue
        disjoint_triples += 1
        union = frozenset().union(*triple)
        assert sum(matching <= union for matching in matchings) >= 4
    assert disjoint_triples > 0

    words = tuple(matching_word(matching) for matching in SELECTED)
    assert words == ((0, 0, 0, 0, 0, 0),
                     (0, 0, 1, 1, 1, 1),
                     (2, 2, 2, 2, 2, 2))

    basis = tuple(tuple(int(row == color) for row in range(3)) for color in range(3))
    local_columns = [tuple(basis[word[vertex]] for word in words) for vertex in VERTICES]
    local_ranks = [rank([[column[row] for column in columns] for row in range(3)])
                   for columns in local_columns]
    local_k_ranks = [kruskal_rank(columns) for columns in local_columns]
    assert local_ranks == [2, 2, 3, 3, 3, 3]
    assert local_k_ranks == [1, 1, 3, 3, 3, 3]
    assert sum(local_k_ranks) == 14 >= 2 * 3 + (N - 1)

    for shore in combinations(VERTICES, 3):
        assert flattening_rank(words, shore) == 3

    print("Kruskal-visible Wick rank-gap audit: PASS")
    print("  threshold: all k_v=3 works exactly for S <= n")
    print("  supermodes: generic 2+2+2 and 2+3+3 reach S=12 and S=30")
    print("  S=3 multiplicities force repeated local factors unless d_M=1")
    print("  boundary modes=(2,2,3,3,3,3), all 20 balanced ranks=3")


if __name__ == "__main__":
    main()
