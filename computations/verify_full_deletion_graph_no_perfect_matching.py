#!/usr/bin/env python3
"""Audit the minimal recurrence model whose full deletion graph is a star."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations


N = 6
FULL = (1 << N) - 1


def pair_mask(u: int, v: int) -> int:
    return (1 << u) | (1 << v)


STAR_EDGES = {pair_mask(0, i) for i in range(1, N)}
FEASIBLE = (
    {0, FULL}
    | {pair_mask(u, v) for u, v in combinations(range(N), 2)}
    | {FULL ^ selected_edge for selected_edge in STAR_EDGES}
)


def supported_terms(mask: int, pivot: int) -> int:
    """Count supported edge/cofactor products at one recurrence pivot."""
    assert mask & (1 << pivot)
    return sum(
        pair_mask(pivot, other) in FEASIBLE
        and (mask ^ pair_mask(pivot, other)) in FEASIBLE
        for other in range(N)
        if other != pivot and mask & (1 << other)
    )


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            yield (pair_mask(first, second),) + matching


def audit_recurrence() -> None:
    even_masks = [
        mask for mask in range(1 << N) if mask.bit_count() % 2 == 0
    ]
    for mask in even_masks:
        if mask == 0:
            continue
        for pivot in range(N):
            if not mask & (1 << pivot):
                continue
            count = supported_terms(mask, pivot)
            # Nonzero parent: some recurrence summand must be supported.
            if mask in FEASIBLE:
                assert count >= 1, (mask, pivot, count)
            # Zero parent: a unique supported summand cannot cancel.
            else:
                assert count != 1, (mask, pivot, count)


def audit_deletion_graph() -> None:
    deletion_edges = {
        selected_edge
        for selected_edge in (
            pair_mask(u, v) for u, v in combinations(range(N), 2)
        )
        if selected_edge in FEASIBLE
        and (FULL ^ selected_edge) in FEASIBLE
    }
    assert deletion_edges == STAR_EDGES
    assert all(
        any(selected_edge & (1 << vertex) for selected_edge in deletion_edges)
        for vertex in range(N)
    )
    assert not any(
        set(matching) <= deletion_edges
        for matching in perfect_matchings(tuple(range(N)))
    )


def audit_genuine_rational_hafnian_module() -> None:
    n = 6
    full = (1 << n) - 1
    left = {0, 1, 2}
    right = {3, 4, 5}
    weights = {
        (u, v): Fraction(-2 if u in right and v in right else 1)
        for u, v in combinations(range(n), 2)
    }

    @cache
    def hafnian(mask: int) -> Fraction:
        if mask == 0:
            return Fraction(1)
        first_bit = mask & -mask
        u = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        answer = Fraction(0)
        while remainder:
            next_bit = remainder & -remainder
            v = next_bit.bit_length() - 1
            answer += weights[tuple(sorted((u, v)))] * hafnian(
                mask ^ first_bit ^ next_bit
            )
            remainder ^= next_bit
        return answer

    assert hafnian(full) == -12
    cofactor_edges = set()
    deletion_edges = set()
    recurrence_terms = {}
    for u, v in combinations(range(n), 2):
        selected_edge = pair_mask(u, v)
        cofactor = hafnian(full ^ selected_edge)
        term = weights[u, v] * cofactor
        recurrence_terms[u, v] = term
        if cofactor:
            cofactor_edges.add((u, v))
        if weights[u, v] and cofactor:
            deletion_edges.add((u, v))

        if (u in left) != (v in left):
            assert cofactor == 0
        elif u in left:
            assert cofactor == -6 and term == -6
        else:
            assert cofactor == 3 and term == -6

    two_triangles = set(combinations(sorted(left), 2)) | set(
        combinations(sorted(right), 2)
    )
    assert cofactor_edges == deletion_edges == two_triangles
    deletion_masks = {pair_mask(u, v) for u, v in deletion_edges}
    assert not any(
        set(matching) <= deletion_masks
        for matching in perfect_matchings(tuple(range(n)))
    )
    for pivot in range(n):
        assert sum(
            term
            for edge, term in recurrence_terms.items()
            if pivot in edge
        ) == hafnian(full)


def audit_four_vertex_minimality() -> None:
    vertices = tuple(range(4))
    full = (1 << 4) - 1
    edges = tuple(pair_mask(u, v) for u, v in combinations(vertices, 2))
    matchings = tuple(perfect_matchings(vertices))

    # Enumerate every possible feasible edge support.  Whenever the full
    # recurrence is supported at every pivot, the corresponding deletion
    # graph contains a complementary edge pair, hence a perfect matching.
    for choice in range(1 << len(edges)):
        feasible_edges = {
            selected_edge
            for index, selected_edge in enumerate(edges)
            if choice & (1 << index)
        }
        deletion_edges = {
            selected_edge
            for selected_edge in feasible_edges
            if (full ^ selected_edge) in feasible_edges
        }
        full_supported = all(
            any(edge & (1 << vertex) for edge in deletion_edges)
            for vertex in vertices
        )
        if full_supported:
            assert any(
                set(matching) <= deletion_edges for matching in matchings
            )


# Bit position ``mask`` records feasibility of that subset.  These three
# n=8 families were extracted once by SAT, but everything used below is
# audited directly and has no solver dependency.
PRIVATE_N8_SUPPORTS = (
    int(
        "8020491201920449000000000000000000000000000000008020491201920449",
        16,
    ),
    int(
        "8409011601161600611696499249490021161249964948161600681649009249",
        16,
    ),
    int(
        "8000200001009200008000200001009249001200040049000049001200040049",
        16,
    ),
)

EXPECTED_PRIVATE_COFACTOR_GRAPHS = (
    {(0, 4), (1, 3), (2, 4), (3, 5), (6, 7)},
    {
        (0, 2),
        (0, 6),
        (1, 6),
        (1, 7),
        (2, 3),
        (4, 6),
        (5, 6),
        (5, 7),
    },
    {(0, 7), (1, 4), (2, 7), (3, 6), (4, 5)},
)

EXPECTED_PRIVATE_DELETION_GRAPHS = (
    {(0, 4), (1, 3), (2, 4), (3, 5), (6, 7)},
    {
        (0, 6),
        (1, 6),
        (2, 3),
        (4, 6),
        (5, 6),
        (5, 7),
    },
    {(0, 7), (1, 4), (2, 7), (3, 6), (4, 5)},
)


def in_support(encoded: int, mask: int) -> bool:
    return bool((encoded >> mask) & 1)


def odd_components_after_deletion(
    edges: set[tuple[int, int]], deleted: set[int], n: int
) -> int:
    unseen = set(range(n)) - deleted
    odd_components = 0
    while unseen:
        component = {unseen.pop()}
        changed = True
        while changed:
            changed = False
            for u, v in edges:
                if u in component and v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    changed = True
                if v in component and u in unseen:
                    unseen.remove(u)
                    component.add(u)
                    changed = True
        odd_components += len(component) % 2
    return odd_components


def audit_three_private_n8_families() -> None:
    n = 8
    full = (1 << n) - 1
    vertices = tuple(range(n))
    edges = tuple(combinations(vertices, 2))
    matchings = tuple(perfect_matchings(vertices))
    cofactor_graphs = []
    deletion_graphs = []

    for color, encoded in enumerate(PRIVATE_N8_SUPPORTS):
        assert in_support(encoded, 0)
        assert in_support(encoded, full)

        # Audit both exact support implications of every diagonal recurrence.
        for mask in range(1 << n):
            if mask.bit_count() % 2 or mask == 0:
                continue
            for pivot in vertices:
                if not mask & (1 << pivot):
                    continue
                count = sum(
                    in_support(encoded, pair_mask(pivot, other))
                    and in_support(
                        encoded, mask ^ pair_mask(pivot, other)
                    )
                    for other in vertices
                    if other != pivot and mask & (1 << other)
                )
                if in_support(encoded, mask):
                    assert count >= 1, (color, mask, pivot, count)
                else:
                    assert count != 1, (color, mask, pivot, count)

        edge_graph = {
            (u, v)
            for u, v in edges
            if in_support(encoded, pair_mask(u, v))
        }
        cofactor_graph = {
            (u, v)
            for u, v in edges
            if in_support(encoded, full ^ pair_mask(u, v))
        }
        deletion_graph = edge_graph & cofactor_graph
        assert cofactor_graph == EXPECTED_PRIVATE_COFACTOR_GRAPHS[color]
        assert deletion_graph == EXPECTED_PRIVATE_DELETION_GRAPHS[color]
        cofactor_masks = {pair_mask(u, v) for u, v in cofactor_graph}
        assert not any(set(matching) <= cofactor_masks for matching in matchings)
        deletion_masks = {pair_mask(u, v) for u, v in deletion_graph}
        assert not any(set(matching) <= deletion_masks for matching in matchings)
        cofactor_graphs.append(cofactor_graph)
        deletion_graphs.append(deletion_graph)

    # Strong no-cover consequence: a cofactor edge of one color is not a
    # feasible edge in either other color.
    for color, cofactor_graph in enumerate(cofactor_graphs):
        for other_color, encoded in enumerate(PRIVATE_N8_SUPPORTS):
            if color == other_color:
                continue
            assert all(
                not in_support(encoded, pair_mask(u, v))
                for u, v in cofactor_graph
            )

    # Tiny Tutte barriers: C0 and C2 already have two odd components, while
    # deleting vertex 6 from C1 leaves three odd components.
    for graph, barrier, expected in zip(
        cofactor_graphs, (set(), {6}, set()), (2, 3, 2)
    ):
        assert odd_components_after_deletion(graph, barrier, n) == expected

    # The old deletion-graph-only privacy follows automatically, but is
    # strictly weaker than the cofactor assertion checked above.
    for color, deletion_graph in enumerate(deletion_graphs):
        for other_color, encoded in enumerate(PRIVATE_N8_SUPPORTS):
            if color == other_color:
                continue
            assert all(
                not in_support(encoded, pair_mask(u, v))
                for u, v in deletion_graph
            )

    # Record which feasible cover types survive cofactor privacy.
    proper_covers = 0
    cover_types: dict[tuple[int, int, int], int] = {}
    for coloring in range(3**n):
        code = coloring
        masks = [0, 0, 0]
        for vertex in vertices:
            masks[code % 3] |= 1 << vertex
            code //= 3
        if any(mask.bit_count() % 2 for mask in masks) or full in masks:
            continue
        if all(
            in_support(PRIVATE_N8_SUPPORTS[color], masks[color])
            for color in range(3)
        ):
            proper_covers += 1
            cover_type = tuple(sorted(mask.bit_count() for mask in masks))
            cover_types[cover_type] = cover_types.get(cover_type, 0) + 1
    assert proper_covers == 97
    assert cover_types == {(0, 4, 4): 18, (2, 2, 4): 79}
def main() -> None:
    audit_recurrence()
    audit_deletion_graph()
    audit_genuine_rational_hafnian_module()
    audit_four_vertex_minimality()
    audit_three_private_n8_families()
    print(
        "full deletion graph: n=6 shadow D=K_1,5, rational hafnian "
        "D=C=K3+K3, "
        "n=8 three strongly private C's all lack matchings; 97 covers: PASS"
    )


if __name__ == "__main__":
    main()
