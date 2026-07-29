#!/usr/bin/env python3
"""Exact audit for ``notes/injective-star-hessian-bridge-frontier.md``.

The script has two jobs.

* It checks the directed-deficiency double count which produces many
  unordered pairs with injective aggregate stars at both endpoints.
* It constructs the rational fourteen-site structural countermodel from
  the note and checks, for all 91 deleted pairs, aggregate injectivity,
  failure of blockwise row-fullness, and disconnection of the internal
  rank-three graph.  It also checks the pure normalization and the
  universal matching partition behind pair-chart exchange.

Only exact integer and ``Fraction`` arithmetic is used.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from itertools import combinations


N = 14
VERTICES = tuple(range(N))
COLORS = tuple(range(3))
SHORES = (tuple(range(7)), tuple(range(7, 14)))

D = (
    (Fraction(1), Fraction(1), Fraction(1)),
    (Fraction(1), Fraction(2), Fraction(4)),
    (Fraction(1), Fraction(3), Fraction(9)),
)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


CYCLE_EDGES: set[tuple[int, int]] = set()
for shore in SHORES:
    for index, u in enumerate(shore):
        CYCLE_EDGES.add(edge(u, shore[(index + 1) % len(shore)]))

ANCHOR_MATCHINGS = tuple(
    frozenset(edge(i, 7 + (i + colour) % 7) for i in range(7))
    for colour in COLORS
)
ANCHOR_COLOUR = {
    physical_edge: colour
    for colour, matching in enumerate(ANCHOR_MATCHINGS)
    for physical_edge in matching
}

assert len(CYCLE_EDGES) == 14
assert all(len(matching) == 7 for matching in ANCHOR_MATCHINGS)
assert not CYCLE_EDGES.intersection(ANCHOR_COLOUR)
assert len(ANCHOR_COLOUR) == 21


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            yield (edge(first, second),) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))
assert len(MATCHINGS) == 135_135


def zero_matrix():
    return tuple(tuple(Fraction(0) for _ in COLORS) for _ in COLORS)


def anchor_matrix(colour: int):
    return tuple(
        tuple(Fraction(int(row == colour and column == colour)) for column in COLORS)
        for row in COLORS
    )


def left_scale(matrix, scalars):
    return tuple(
        tuple(scalars[row] * matrix[row][column] for column in COLORS)
        for row in COLORS
    )


def transpose(matrix):
    return tuple(tuple(matrix[column][row] for column in COLORS) for row in COLORS)


def base_block(physical_edge: tuple[int, int]):
    if physical_edge in CYCLE_EDGES:
        return D
    if physical_edge in ANCHOR_COLOUR:
        return anchor_matrix(ANCHOR_COLOUR[physical_edge])
    return zero_matrix()


def coefficient_for_word(blocks, word: tuple[int, ...]) -> Fraction:
    total = Fraction(0)
    for matching in MATCHINGS:
        product = Fraction(1)
        for u, v in matching:
            product *= blocks[(u, v)][word[u]][word[v]]
            if product == 0:
                break
        total += product
    return total


def rank(matrix) -> int:
    values = [list(row) for row in matrix]
    if not values:
        return 0
    row_count = len(values)
    column_count = len(values[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if values[row][column]),
            None,
        )
        if pivot is None:
            continue
        values[pivot_row], values[pivot] = values[pivot], values[pivot_row]
        scale = values[pivot_row][column]
        values[pivot_row] = [entry / scale for entry in values[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or values[row][column] == 0:
                continue
            multiple = values[row][column]
            values[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(values[row], values[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def connected_components(vertices, graph_edges):
    adjacency = {vertex: set() for vertex in vertices}
    for u, v in graph_edges:
        if u in adjacency and v in adjacency:
            adjacency[u].add(v)
            adjacency[v].add(u)
    unseen = set(vertices)
    components = []
    while unseen:
        start = min(unseen)
        queue = deque([start])
        unseen.remove(start)
        component = {start}
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(frozenset(component))
    return tuple(components)


def audit_directed_deficiency_count():
    # There are at most 6N directed deficient pairs.  Each unordered pair
    # which is not good at both endpoints consumes at least one of them.
    for order in range(14, 42, 2):
        total_pairs = order * (order - 1) // 2
        guaranteed_good = total_pairs - 6 * order
        assert guaranteed_good == order * (order - 13) // 2
        assert 2 * guaranteed_good // order >= order - 13
    assert N * (N - 13) // 2 == 7


def audit_pure_normalization():
    base_blocks = {physical_edge: base_block(physical_edge) for physical_edge in combinations(VERTICES, 2)}

    # For a constant colour, the support is two seven-cycles plus the
    # corresponding cross one-factor.  The matching polynomial is
    # 1 + 7d^2 + 14d^4 + 7d^6.
    histogram = Counter()
    support = CYCLE_EDGES | set(ANCHOR_MATCHINGS[0])
    for matching in MATCHINGS:
        if all(physical_edge in support for physical_edge in matching):
            histogram[sum(physical_edge in CYCLE_EDGES for physical_edge in matching)] += 1
    assert histogram == Counter({0: 1, 2: 7, 4: 14, 6: 7})

    diagonal = tuple(D[colour][colour] for colour in COLORS)
    pure_values = tuple(
        1 + 7 * value**2 + 14 * value**4 + 7 * value**6
        for value in diagonal
    )
    assert pure_values == (Fraction(29), Fraction(701), Fraction(3_812_509))
    for colour in COLORS:
        assert coefficient_for_word(base_blocks, (colour,) * N) == pure_values[colour]

    local_scale = tuple(1 / value for value in pure_values)
    blocks = dict(base_blocks)
    for physical_edge in combinations(VERTICES, 2):
        if 0 in physical_edge:
            blocks[physical_edge] = left_scale(blocks[physical_edge], local_scale)
    for colour in COLORS:
        assert coefficient_for_word(blocks, (colour,) * N) == 1
    return blocks, pure_values


def oriented_from(blocks, endpoint: int, neighbor: int):
    physical_edge = edge(endpoint, neighbor)
    matrix = blocks[physical_edge]
    return matrix if endpoint == physical_edge[0] else transpose(matrix)


def audit_all_pair_star_and_rank_graphs(blocks):
    for p, q in combinations(VERTICES, 2):
        internal = tuple(vertex for vertex in VERTICES if vertex not in (p, q))
        for endpoint, other in ((p, q), (q, p)):
            # Rows of the aggregate map V_endpoint^* -> direct sum V_v.
            aggregate_rows = []
            for colour in COLORS:
                row = []
                for vertex in internal:
                    row.extend(oriented_from(blocks, endpoint, vertex)[colour])
                aggregate_rows.append(row)
            assert rank(aggregate_rows) == 3

            anchor_neighbors = [
                vertex
                for vertex in internal
                if edge(endpoint, vertex) in ANCHOR_COLOUR
            ]
            assert len(anchor_neighbors) >= 2
            # Every retained anchor block has two literal zero rows, so the
            # blockwise row-full hypothesis fails at this endpoint.
            assert all(
                sum(
                    all(entry == 0 for entry in oriented_from(blocks, endpoint, vertex)[colour])
                    for colour in COLORS
                )
                == 2
                for vertex in anchor_neighbors
            )

        rank_three_edges = {
            physical_edge
            for physical_edge in combinations(internal, 2)
            if rank(blocks[physical_edge]) == 3
        }
        assert rank_three_edges == CYCLE_EDGES.intersection(combinations_set(internal))
        components = connected_components(internal, rank_three_edges)
        assert len(components) >= 2
        assert any(component.issubset(SHORES[0]) for component in components)
        assert any(component.issubset(SHORES[1]) for component in components)


def combinations_set(vertices):
    return {edge(u, v) for u, v in combinations(vertices, 2)}


def audit_non_target_residual(blocks):
    # Find a supported matching which uses a cycle block, choose a mixed
    # cell on that block, and keep every anchor at its forced colour.
    witness = None
    for matching in MATCHINGS:
        if not all(physical_edge in CYCLE_EDGES or physical_edge in ANCHOR_COLOUR for physical_edge in matching):
            continue
        cycle_in_matching = [physical_edge for physical_edge in matching if physical_edge in CYCLE_EDGES]
        if not cycle_in_matching:
            continue
        word = [0] * N
        for physical_edge in matching:
            u, v = physical_edge
            if physical_edge in ANCHOR_COLOUR:
                word[u] = word[v] = ANCHOR_COLOUR[physical_edge]
            else:
                word[u], word[v] = (0, 1)
        if len(set(word)) > 1:
            witness = tuple(word)
            break
    assert witness is not None
    coefficient = coefficient_for_word(blocks, witness)
    assert coefficient > 0
    return witness, coefficient


def chart_partition(deleted_pair):
    p, q = deleted_pair
    direct = 0
    two_star = 0
    reconstructed = set()
    for matching in MATCHINGS:
        matching_set = set(matching)
        if edge(p, q) in matching_set:
            direct += 1
        else:
            p_edge = next(physical_edge for physical_edge in matching if p in physical_edge)
            q_edge = next(physical_edge for physical_edge in matching if q in physical_edge)
            p_neighbor = p_edge[0] if p_edge[1] == p else p_edge[1]
            q_neighbor = q_edge[0] if q_edge[1] == q else q_edge[1]
            assert p_neighbor != q_neighbor
            two_star += 1
        reconstructed.add(matching)
    assert reconstructed == set(MATCHINGS)
    assert (direct, two_star) == (10_395, 124_740)
    return reconstructed


def audit_pair_chart_exchange():
    # Both charts partition the same universal list of matching monomials.
    # Coloring and specializing their edge cells therefore preserves the
    # identity coefficient by coefficient, including endpoint reversal.
    first = chart_partition((0, 7))
    overlap = chart_partition((0, 1))
    assert first == overlap


def binary_perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in binary_perfect_matchings(remainder):
            yield (edge(first, second),) + tail


def audit_binary_injective_nonclean_pair():
    # Relabel the exact binary source of pair-covector-selection-obstruction
    # from 1,...,6 to 0,...,5.  Matrices are stored from the smaller to the
    # larger endpoint.
    binary_vertices = tuple(range(6))
    binary_colours = (0, 1)

    def bzero():
        return ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))

    binary_blocks = {
        physical_edge: bzero()
        for physical_edge in combinations(binary_vertices, 2)
    }

    def set_cells(physical_edge, cells):
        matrix = [list(row) for row in bzero()]
        for a, b, value in cells:
            matrix[a][b] = Fraction(value)
        binary_blocks[physical_edge] = tuple(tuple(row) for row in matrix)

    set_cells((0, 1), ((0, 0, 1), (1, 0, 1)))
    set_cells((2, 3), ((0, 0, 1),))
    set_cells((4, 5), ((0, 0, 1),))
    set_cells((1, 3), ((0, 0, 1),))
    set_cells((0, 2), ((1, 0, -1),))
    set_cells((0, 5), ((1, 1, 1),))
    set_cells((1, 2), ((1, 1, 1),))
    set_cells((3, 4), ((1, 1, Fraction(3, 4)),))
    set_cells((0, 4), ((1, 1, Fraction(1, 2)),))
    set_cells((3, 5), ((1, 1, Fraction(1, 2)),))

    binary_matchings = tuple(binary_perfect_matchings(binary_vertices))
    assert len(binary_matchings) == 15

    def binary_coefficient(word):
        total = Fraction(0)
        for matching in binary_matchings:
            product = Fraction(1)
            for u, v in matching:
                product *= binary_blocks[(u, v)][word[u]][word[v]]
            total += product
        return total

    for mask in range(1 << 6):
        word = tuple((mask >> vertex) & 1 for vertex in binary_vertices)
        expected = Fraction(int(word == (0,) * 6 or word == (1,) * 6))
        assert binary_coefficient(word) == expected

    deleted = (0, 2)
    internal = tuple(
        vertex for vertex in binary_vertices if vertex not in deleted
    )

    def binary_oriented(endpoint, neighbor):
        physical_edge = edge(endpoint, neighbor)
        matrix = binary_blocks[physical_edge]
        if endpoint == physical_edge[0]:
            return matrix
        return tuple(
            tuple(matrix[column][row] for column in binary_colours)
            for row in binary_colours
        )

    for endpoint in deleted:
        aggregate_rows = []
        for colour in binary_colours:
            row = []
            for neighbor in internal:
                row.extend(binary_oriented(endpoint, neighbor)[colour])
            aggregate_rows.append(row)
        assert rank(aggregate_rows) == 2

    # Build the effective first-jet family R_K for a general covector K.
    # A linear form in k_00,k_01,k_10,k_11 is stored as a 4-tuple.
    def linear_zero():
        return [Fraction(0)] * 4

    effective = {}
    p, q = deleted
    for u, v in combinations(internal, 2):
        matrix = [
            [linear_zero() for _ in binary_colours]
            for _ in binary_colours
        ]
        p_u = binary_oriented(p, u)
        p_v = binary_oriented(p, v)
        q_u = binary_oriented(q, u)
        q_v = binary_oriented(q, v)
        for x in binary_colours:
            for y in binary_colours:
                for a in binary_colours:
                    for b in binary_colours:
                        variable = 2 * a + b
                        matrix[x][y][variable] += (
                            p_u[a][x] * q_v[b][y]
                            + q_u[b][x] * p_v[a][y]
                        )
        effective[(u, v)] = matrix

    # Coefficient of the word (1,0,1,1) on internal sites (1,3,4,5).
    # Store its quadratic polynomial by sorted pairs of variable indices.
    target_word = {1: 1, 3: 0, 4: 1, 5: 1}
    polynomial = Counter()
    for matching in binary_perfect_matchings(internal):
        first_edge, second_edge = matching
        l1 = effective[first_edge][target_word[first_edge[0]]][
            target_word[first_edge[1]]
        ]
        l2 = effective[second_edge][target_word[second_edge[0]]][
            target_word[second_edge[1]]
        ]
        for first_variable, first_value in enumerate(l1):
            for second_variable, second_value in enumerate(l2):
                polynomial[
                    tuple(sorted((first_variable, second_variable)))
                ] += first_value * second_value
    polynomial = Counter(
        {monomial: value for monomial, value in polynomial.items() if value}
    )
    # The sole term is k_10*k_11 = -s(K)*kappa_1(K), since s(K)=-k_10.
    assert polynomial == Counter({(2, 3): Fraction(1)})


def main():
    audit_directed_deficiency_count()
    audit_binary_injective_nonclean_pair()
    blocks, pure_values = audit_pure_normalization()
    audit_all_pair_star_and_rank_graphs(blocks)
    witness, coefficient = audit_non_target_residual(blocks)
    audit_pair_chart_exchange()
    print("directed count: at least N(N-13)/2 both-injective pairs; N=14 gives 7")
    print("binary full target: both aggregate stars rank 2, clean-cap defect k_10*k_11")
    print(f"pure normalization denominators: {tuple(int(value) for value in pure_values)}")
    print("all 91 pairs: both aggregate stars rank 3, local zero rows, disconnected G_3")
    print(f"positive mixed residual: word={''.join(map(str, witness))}, coefficient={coefficient}")
    print("pair charts: 10395 direct + 124740 two-star matchings in both charts")
    print("PASS")


if __name__ == "__main__":
    main()
