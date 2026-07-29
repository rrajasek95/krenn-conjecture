#!/usr/bin/env python3
"""Clean-room audit of the complete-bipartite all-pair escape family.

This script does not import the primary checker.  It reconstructs the
endpoint-oriented blocks, matching coefficients, star maps, deletion graphs,
and pair-cofactor recursion directly over the rationals.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from math import factorial
from pathlib import Path


PRIMARY_HASHES = {
    "notes/complete-bipartite-all-pair-hessian-escape-countermodel.md":
        "778e7a04ed5e0af0d69cac5b92fb0833a3903fe5e00c239d3a29715674dcb779",
    "computations/verify_complete_bipartite_all_pair_hessian_escape_countermodel.py":
        "a807dc8ab7198b4cbe730ea33f58f87062cddb804c9a8b8de3928949ebc3a191",
}

D = (
    (Fraction(1), Fraction(1), Fraction(1)),
    (Fraction(1), Fraction(2), Fraction(4)),
    (Fraction(1), Fraction(3), Fraction(9)),
)
COLOURS = range(3)


def determinant_leibniz(matrix) -> Fraction:
    total = Fraction(0)
    for permutation in permutations(range(3)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        term = Fraction((-1) ** inversions)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total += term
    return total


def rank(matrix) -> int:
    rows = [list(map(Fraction, row)) for row in matrix]
    if not rows:
        return 0
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(
                    rows[row], rows[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in COLOURS) for i in COLOURS)


def source(order: int):
    assert order >= 6 and order % 2 == 0
    shore_size = order // 2
    left = frozenset(range(shore_size))
    right = frozenset(range(shore_size, order))
    diagonal = tuple(D[c][c] for c in COLOURS)
    scale = tuple(
        Fraction(1, factorial(shore_size) * diagonal[c] ** shore_size)
        for c in COLOURS
    )
    scaled_D = tuple(
        tuple(scale[row] * D[row][column] for column in COLOURS)
        for row in COLOURS
    )
    zero = tuple(tuple(Fraction(0) for _ in COLOURS) for _ in COLOURS)

    def stored(u: int, v: int):
        assert u < v
        if u in left and v in right:
            return scaled_D if u == 0 else D
        return zero

    def oriented(u: int, v: int):
        lo, hi = sorted((u, v))
        matrix = stored(lo, hi)
        return matrix if u == lo else transpose(matrix)

    def entry(u: int, v: int, colour_u: int, colour_v: int) -> Fraction:
        return oriented(u, v)[colour_u][colour_v]

    return shore_size, left, right, scale, scaled_D, stored, oriented, entry


def matching_coefficient(vertices, word, entry, memo) -> Fraction:
    vertices = tuple(vertices)
    if not vertices:
        return Fraction(1)
    if vertices in memo:
        return memo[vertices]
    first = vertices[0]
    total = Fraction(0)
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        total += (
            entry(first, second, word[first], word[second])
            * matching_coefficient(remainder, word, entry, memo)
        )
    memo[vertices] = total
    return total


def pair_cofactor_coefficient(order, p, q, word, entry) -> Fraction:
    """Direct edge plus the two oriented stars over one common source."""
    internal = tuple(site for site in range(order) if site not in (p, q))
    memo = {}
    direct = (
        entry(p, q, word[p], word[q])
        * matching_coefficient(internal, word, entry, memo)
    )
    two_star = Fraction(0)
    for r in internal:
        for t in internal:
            if t == r:
                continue
            remainder = tuple(site for site in internal if site not in (r, t))
            two_star += (
                entry(p, r, word[p], word[r])
                * entry(q, t, word[q], word[t])
                * matching_coefficient(remainder, word, entry, memo)
            )
    return direct + two_star


def graph_connected(vertices, edges) -> bool:
    vertices = set(vertices)
    if len(vertices) <= 1:
        return True
    adjacency = {vertex: set() for vertex in vertices}
    for u, v in edges:
        if u in vertices and v in vertices:
            adjacency[u].add(v)
            adjacency[v].add(u)
    reached = set()
    stack = [next(iter(vertices))]
    while stack:
        vertex = stack.pop()
        if vertex in reached:
            continue
        reached.add(vertex)
        stack.extend(adjacency[vertex] - reached)
    return reached == vertices


def graph_bipartite(vertices, edges) -> bool:
    adjacency = {vertex: set() for vertex in vertices}
    for u, v in edges:
        if u in adjacency and v in adjacency:
            adjacency[u].add(v)
            adjacency[v].add(u)
    colour = {}
    for start in vertices:
        if start in colour:
            continue
        colour[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]
                    stack.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True


def audit_frozen_primary() -> None:
    root = Path(__file__).resolve().parents[1]
    for relative, expected in PRIMARY_HASHES.items():
        actual = sha256((root / relative).read_bytes()).hexdigest()
        assert actual == expected, (relative, expected, actual)


def audit_matrix_scaling_and_normalization() -> None:
    assert determinant_leibniz(D) == 2
    assert rank(D) == 3
    diagonal = tuple(D[c][c] for c in COLOURS)
    for shore_size in range(3, 31):
        order = 2 * shore_size
        s, left, right, scale, scaled_D, stored, oriented, entry = source(order)
        assert s == shore_size
        assert determinant_leibniz(scaled_D) != 0
        for v in right:
            assert stored(0, v) == scaled_D
            assert oriented(v, 0) == transpose(scaled_D)
        for u in left - {0}:
            for v in right:
                assert stored(u, v) == D
                assert oriented(v, u) == transpose(D)
        for u, v in combinations(range(order), 2):
            if (u in left) == (v in left):
                assert rank(stored(u, v)) == 0
        for colour in COLOURS:
            one_matching = scale[colour] * diagonal[colour] ** shore_size
            assert factorial(shore_size) * one_matching == 1

        # The off-diagonal word has one common value on every matching.
        mixed_one_matching = scale[0] * D[0][1] * D[1][1] ** (shore_size - 1)
        assert factorial(shore_size) * mixed_one_matching == 2 ** (shore_size - 1)

    # Independent permanent enumeration, including the special scaled row.
    for shore_size in range(3, 8):
        order = 2 * shore_size
        _, left, right, _, _, _, _, entry = source(order)
        for colour in COLOURS:
            word = (colour,) * order
            total = sum(
                (
                    _matching_product(left, image, word, entry)
                    for image in permutations(sorted(right))
                ),
                Fraction(0),
            )
            assert total == 1
        word = (0,) + (1,) * (order - 1)
        total = sum(
            (
                _matching_product(left, image, word, entry)
                for image in permutations(sorted(right))
            ),
            Fraction(0),
        )
        assert total == 2 ** (shore_size - 1)


def _matching_product(left, image, word, entry) -> Fraction:
    value = Fraction(1)
    for u, v in zip(sorted(left), image, strict=True):
        value *= entry(u, v, word[u], word[v])
    return value


def audit_stars_graphs_and_connectivity() -> None:
    for shore_size in range(3, 11):
        order = 2 * shore_size
        _, left, right, _, _, stored, oriented, _ = source(order)
        vertices = tuple(range(order))
        edges = {
            (u, v)
            for u, v in combinations(vertices, 2)
            if rank(stored(u, v)) == 3
        }
        expected = {(u, v) for u in left for v in right}
        assert edges == expected
        degrees = {
            u: sum(u in edge for edge in edges) for u in vertices
        }
        assert set(degrees.values()) == {shore_size}
        if shore_size >= 4:
            assert all(degree != 3 for degree in degrees.values())

        for endpoint in vertices:
            for colour in COLOURS:
                support = {
                    neighbor
                    for neighbor in vertices
                    if neighbor != endpoint
                    and any(oriented(endpoint, neighbor)[colour])
                }
                assert len(support) == shore_size

        for p, q in combinations(vertices, 2):
            internal = tuple(v for v in vertices if v not in (p, q))
            induced = {
                (u, v) for u, v in edges if u in internal and v in internal
            }
            assert graph_connected(internal, induced)
            assert graph_bipartite(internal, induced)
            left_count = len(left.intersection(internal))
            right_count = len(right.intersection(internal))
            assert induced == {
                (u, v)
                for u in left.intersection(internal)
                for v in right.intersection(internal)
            }
            assert sorted((left_count, right_count)) in (
                [shore_size - 2, shore_size],
                [shore_size - 1, shore_size - 1],
            )

            # Concatenate every retained oriented block row.  Rank three is
            # exactly injectivity of the aggregate star at that endpoint.
            for endpoint in (p, q):
                star_rows = [[], [], []]
                for neighbor in internal:
                    block = oriented(endpoint, neighbor)
                    for colour in COLOURS:
                        star_rows[colour].extend(block[colour])
                assert rank(star_rows) == 3

    # Exhaust the lower and upper bounds for vertex connectivity at orders
    # independent of the primary checker's range endpoint.
    for shore_size in range(3, 8):
        vertices = tuple(range(2 * shore_size))
        left = frozenset(range(shore_size))
        right = frozenset(range(shore_size, 2 * shore_size))
        edges = {(u, v) for u in left for v in right}
        for removed_size in range(shore_size):
            for removed in combinations(vertices, removed_size):
                remaining = tuple(v for v in vertices if v not in removed)
                assert graph_connected(remaining, edges)
        assert not graph_connected(tuple(right), edges)


def audit_literal_pair_cofactors() -> None:
    # Exhaust every colour word and every deleted pair at N=6.
    order = 6
    _, _, _, _, _, _, _, entry = source(order)
    vertices = tuple(range(order))
    for word in product(COLOURS, repeat=order):
        whole = matching_coefficient(vertices, word, entry, {})
        for p, q in combinations(vertices, 2):
            assert pair_cofactor_coefficient(order, p, q, word, entry) == whole

    # At N=8 and N=10, cover every pair, every endpoint-colour choice, and
    # several independently generated internal assignments.  Endpoint order
    # is deliberately exercised in both directions by the entry function.
    for order in (8, 10):
        _, _, _, _, _, _, _, entry = source(order)
        vertices = tuple(range(order))
        for p, q in combinations(vertices, 2):
            internal = tuple(v for v in vertices if v not in (p, q))
            patterns = {
                tuple((site + seed + site * seed) % 3 for site in internal)
                for seed in range(7)
            }
            patterns.update({(colour,) * len(internal) for colour in COLOURS})
            for internal_word in patterns:
                for colour_p, colour_q in product(COLOURS, repeat=2):
                    word = [0] * order
                    word[p], word[q] = colour_p, colour_q
                    for site, colour in zip(internal, internal_word, strict=True):
                        word[site] = colour
                    word = tuple(word)
                    whole = matching_coefficient(vertices, word, entry, {})
                    cofactor = pair_cofactor_coefficient(
                        order, p, q, word, entry
                    )
                    assert cofactor == whole

    # The named mixed equation is entirely in the two-star term because
    # sites 0 and 1 share a shore; it is nonzero at every audited order.
    for shore_size in range(3, 13):
        order = 2 * shore_size
        _, _, _, _, _, _, _, entry = source(order)
        word = (0,) + (1,) * (order - 1)
        whole = matching_coefficient(tuple(range(order)), word, entry, {})
        cofactor = pair_cofactor_coefficient(order, 0, 1, word, entry)
        assert entry(0, 1, 0, 1) == 0
        assert whole == cofactor == 2 ** (shore_size - 1)


def main() -> None:
    audit_frozen_primary()
    audit_matrix_scaling_and_normalization()
    audit_stars_graphs_and_connectivity()
    audit_literal_pair_cofactors()
    print("independent complete-bipartite all-pair escape audit: PASS")
    print("frozen primary hashes: PASS")
    print("uniform formula audit: N=6..60")
    print("exact permanent audit: N=6,8,10,12,14")
    print("all-pair star/graph audit: N=6..20")
    print("literal cofactor audit: exhaustive N=6; structured N=8,10")
    print("mixed residual audit: 2^(s-1), s=3..12")


if __name__ == "__main__":
    main()
