#!/usr/bin/env python3
"""Exact audit for the two-K4 matching-number-at-most-three obstruction."""

from __future__ import annotations

import itertools

import sympy as sp


COLORS = tuple(range(3))
LOCAL_VERTICES = tuple(range(4))
GLOBAL_VERTICES = tuple(range(8))
FACTORS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
EDGE_COLOR = {
    tuple(sorted(edge)): color
    for color, factor in enumerate(FACTORS)
    for edge in factor
}


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(GLOBAL_VERTICES))
COLORINGS = tuple(itertools.product(COLORS, repeat=8))


def is_cross(edge: tuple[int, int]) -> bool:
    return edge[0] < 4 <= edge[1]


def local_internal_color(edge: tuple[int, int]) -> int:
    u, v = edge
    if u >= 4:
        u -= 4
        v -= 4
    return EDGE_COLOR[tuple(sorted((u, v)))]


def physical_matching_count(cross_graph: frozenset[tuple[int, int]]):
    counts = {0: 0, 2: 0, 4: 0}
    for matching in MATCHINGS:
        cross = tuple(edge for edge in matching if is_cross(edge))
        if all(edge in cross_graph for edge in cross):
            counts[len(cross)] += 1
    return counts


def two_cross_monomials(
    cross_graph: frozenset[tuple[int, int]], coloring: tuple[int, ...]
) -> tuple[tuple[tuple[int, int, int, int], ...], ...]:
    """Return cross-cell monomials compatible with a fixed coloring."""
    answer = []
    for matching in MATCHINGS:
        cross = tuple(edge for edge in matching if is_cross(edge))
        if len(cross) != 2 or any(edge not in cross_graph for edge in cross):
            continue
        internal = tuple(edge for edge in matching if not is_cross(edge))
        if any(
            coloring[u] != local_internal_color(edge)
            or coloring[v] != local_internal_color(edge)
            for edge in internal
            for u, v in (edge,)
        ):
            continue
        answer.append(
            tuple(
                sorted(
                    (left, right - 4, coloring[left], coloring[right])
                    for left, right in cross
                )
            )
        )
    return tuple(answer)


def induced_word(
    matching: tuple[tuple[int, int], ...],
    cross_cells: dict[tuple[int, int], tuple[int, int]],
) -> tuple[int, ...]:
    word = [-1] * 8
    for edge in matching:
        u, v = edge
        if is_cross(edge):
            left_color, right_color = cross_cells[edge]
            word[u], word[v] = left_color, right_color
        else:
            color = local_internal_color(edge)
            word[u] = word[v] = color
    assert all(color >= 0 for color in word)
    return tuple(word)


def audit_two_star() -> None:
    graph = frozenset(
        {(0, 5 + color) for color in COLORS}
        | {(1 + color, 4) for color in COLORS}
    )
    assert physical_matching_count(graph) == {0: 9, 2: 9, 4: 0}
    assert max(len(two_cross_monomials(graph, word)) for word in COLORINGS) == 1

    for r, s in itertools.product(COLORS, repeat=2):
        word = (r,) * 4 + (s,) * 4
        monomials = two_cross_monomials(graph, word)
        assert monomials == (
            tuple(sorted(((0, 1 + s, r, s), (1 + r, 0, r, s)))),
        )

    # A nonzero off-diagonal correction forces U_s to have only its
    # (r,s) cell: varying either endpoint produces a mixed word with the
    # same unique matching and the other nonzero target cell unchanged.
    for s in COLORS:
        forced_units = []
        for r in COLORS:
            if r == s:
                continue
            matching = (
                (0, 5 + s),
                (1 + r, 4),
                tuple(sorted(({1, 2, 3} - {1 + r}))),
                tuple(sorted(({5, 6, 7} - {5 + s}))),
            )
            target_cells = {(0, 5 + s): (r, s), (1 + r, 4): (r, s)}
            for a, b in itertools.product(COLORS, repeat=2):
                if (a, b) == (r, s):
                    continue
                cells = dict(target_cells)
                cells[0, 5 + s] = (a, b)
                word = induced_word(matching, cells)
                assert len(set(word)) > 1
                assert len(two_cross_monomials(graph, word)) == 1
            forced_units.append((r, s))
        assert len(forced_units) == 2 and forced_units[0] != forced_units[1]


def audit_ferrers_certificate() -> None:
    # L_*,L_0 only see R_*; L_1,L_2 see the whole right shore.
    graph = frozenset(
        {(0, 4), (1, 4)}
        | {(left, right) for left in (2, 3) for right in range(4, 8)}
    )
    assert physical_matching_count(graph) == {0: 9, 2: 24, 4: 0}

    target_01 = (0, 0, 0, 0, 1, 1, 1, 1)
    target_10 = (1, 1, 1, 1, 0, 0, 0, 0)
    zero_words = (
        (1, 1, 1, 0, 0, 1, 1, 1),
        (2, 1, 0, 2, 0, 2, 2, 1),
        (2, 1, 0, 2, 0, 1, 1, 1),
        (2, 1, 0, 2, 0, 1, 0, 0),
        (1, 2, 2, 0, 0, 1, 1, 1),
        (1, 1, 0, 1, 0, 2, 2, 1),
        (1, 1, 0, 1, 0, 1, 1, 1),
        (1, 1, 0, 1, 0, 1, 0, 0),
    )

    u = (0, 0, 1, 0)
    v = (1, 0, 1, 0)
    p = (2, 1, 1, 0)
    q = (3, 1, 1, 0)
    k = (
        (3, 2, 0, 1),
        (2, 3, 0, 1),
        (2, 2, 0, 1),
        (2, 1, 0, 1),
    )
    h = (
        (2, 0, 0, 1),
        (3, 1, 0, 1),
        (3, 0, 0, 1),
        (3, 3, 0, 1),
    )

    assert set(two_cross_monomials(graph, target_10)) == {
        tuple(sorted((u, p))),
        tuple(sorted((v, q))),
    }
    assert set(two_cross_monomials(graph, target_01)) == {
        tuple(sorted((k[index], h[index]))) for index in range(4)
    }
    expected_zeros = {
        tuple(sorted((endpoint, k[index])))
        for endpoint in (u, v)
        for index in range(4)
    }
    actual_zeros = {
        monomial
        for word in zero_words
        for monomial in two_cross_monomials(graph, word)
    }
    assert all(len(two_cross_monomials(graph, word)) == 1 for word in zero_words)
    assert actual_zeros == expected_zeros

    # A literal polynomial certificate.  A=sum k_i h_i and I=up+vq
    # must both equal -1, while all u*k_i and v*k_i vanish.
    symbols = sp.symbols("u v p q k0:4 h0:4")
    su, sv, spp, sq, *tail = symbols
    sk = tail[:4]
    sh = tail[4:]
    a_coefficient = sum(sk[index] * sh[index] for index in range(4))
    i_coefficient = su * spp + sv * sq
    zero_certificate = sum(
        spp * sh[index] * (su * sk[index])
        + sq * sh[index] * (sv * sk[index])
        for index in range(4)
    )
    nullstellensatz = (
        zero_certificate
        - a_coefficient * (i_coefficient + 1)
        + (a_coefficient + 1)
    )
    assert sp.expand(nullstellensatz) == 1


def neighbor(vertex: int, color: int) -> int:
    return next(
        other
        for other in LOCAL_VERTICES
        if other != vertex
        and EDGE_COLOR[tuple(sorted((vertex, other)))] == color
    )


def audit_single_slice_normal_form() -> None:
    # General characteristic-zero normal form for r=0 and center w=0.
    a, b, c = sp.symbols("a b c", nonzero=True)
    d = -b * c / a
    h_s = sp.Matrix([a, b])
    h_t = sp.Matrix([c, d])
    h_basis = sp.Matrix.hstack(h_s, h_t)
    exchange = sp.Matrix([[0, 1], [1, 0]])
    basis = sp.eye(3)
    center = sp.Matrix.hstack(-basis[:, 1], -basis[:, 2]) * h_basis.inv() * exchange
    matrices = [sp.zeros(3, 2) for _ in LOCAL_VERTICES]
    matrices[0] = center
    matrices[neighbor(0, 1)] = basis[:, 1] * h_s.T
    matrices[neighbor(0, 2)] = basis[:, 2] * h_t.T
    assert matrices[neighbor(0, 0)] == sp.zeros(3, 2)

    for u, v in itertools.combinations(LOCAL_VERTICES, 2):
        product = sp.simplify(matrices[u] * exchange * matrices[v].T)
        expected = sp.zeros(3)
        if {u, v} == {0, neighbor(0, 1)}:
            expected[1, 1] = -1
        elif {u, v} == {0, neighbor(0, 2)}:
            expected[2, 2] = -1
        assert sp.simplify(product - expected) == sp.zeros(3)

    for column in range(2):
        assert sp.simplify(center[0, column]) == 0
        assert sp.simplify(center[1, column]) != 0
        assert sp.simplify(center[2, column]) != 0
        assert sp.simplify(h_s[column]) != 0
        assert sp.simplify(h_t[column]) != 0


def normal_support(target_color: int, center: int) -> tuple[frozenset[int], ...]:
    support = [frozenset() for _ in LOCAL_VERTICES]
    other_colors = tuple(color for color in COLORS if color != target_color)
    support[center] = frozenset(other_colors)
    for color in other_colors:
        support[neighbor(center, color)] = frozenset({color})
    assert not support[neighbor(center, target_color)]
    return tuple(support)


def response_support_counts(
    first: tuple[frozenset[int], ...],
    second: tuple[frozenset[int], ...],
) -> dict[tuple[int, ...], int]:
    counts: dict[tuple[int, ...], int] = {}
    for u, v in itertools.combinations(LOCAL_VERTICES, 2):
        color = EDGE_COLOR[u, v]
        remainder = tuple(site for site in LOCAL_VERTICES if site not in (u, v))
        for left, right in ((first, second), (second, first)):
            for a, b in itertools.product(left[u], right[v]):
                word = [-1] * 4
                word[u], word[v] = a, b
                word[remainder[0]] = word[remainder[1]] = color
                key = tuple(word)
                counts[key] = counts.get(key, 0) + 1
    return counts


def audit_k34_compatibility() -> None:
    graph = frozenset(
        (left, right) for left in (1, 2, 3) for right in range(4, 8)
    )
    assert physical_matching_count(graph) == {0: 9, 2: 36, 4: 0}

    cases = 0
    for first_color, second_color in itertools.combinations(COLORS, 2):
        remaining_color = next(
            color for color in COLORS if color not in (first_color, second_color)
        )
        for first_center, second_center in itertools.product(
            LOCAL_VERTICES, repeat=2
        ):
            counts = response_support_counts(
                normal_support(first_color, first_center),
                normal_support(second_color, second_center),
            )
            unique = sum(multiplicity == 1 for multiplicity in counts.values())
            if first_center == second_center:
                expected = 9
            elif EDGE_COLOR[tuple(sorted((first_center, second_center)))] == remaining_color:
                expected = 9
            else:
                expected = 13
            assert unique == expected
            cases += 1
    assert cases == 48


def audit_hall_envelopes() -> None:
    edges = tuple(itertools.product(LOCAL_VERTICES, repeat=2))
    permutations = tuple(itertools.permutations(LOCAL_VERTICES))
    covered = 0
    envelope_types = set()
    for mask in range(1 << len(edges)):
        graph = {
            edge for index, edge in enumerate(edges) if mask & (1 << index)
        }
        if any(all((left, permutation[left]) in graph for left in LOCAL_VERTICES)
               for permutation in permutations):
            continue
        covered += 1
        for size in range(1, 5):
            witness = None
            for shore in itertools.combinations(LOCAL_VERTICES, size):
                neighborhood = {
                    right for left in shore for right in LOCAL_VERTICES
                    if (left, right) in graph
                }
                if len(neighborhood) < size:
                    witness = (set(shore), neighborhood)
                    break
            if witness is not None:
                break
        assert witness is not None
        shore, neighborhood = witness
        extra = [right for right in LOCAL_VERTICES if right not in neighborhood]
        target_neighbors = set(neighborhood)
        target_neighbors.update(extra[: size - 1 - len(neighborhood)])
        envelope = {
            (left, right)
            for left in LOCAL_VERTICES
            for right in LOCAL_VERTICES
            if left not in shore or right in target_neighbors
        }
        assert graph <= envelope
        if size in (1, 4):
            envelope_types.add("k34")
        else:
            envelope_types.add("ferrers")
    assert covered > 0
    assert envelope_types == {"k34", "ferrers"}


def main() -> None:
    assert len(MATCHINGS) == 105
    audit_two_star()
    audit_ferrers_certificate()
    audit_single_slice_normal_form()
    audit_k34_compatibility()
    audit_hall_envelopes()
    print("Two-K4 low-matching cross obstruction: PASS")


if __name__ == "__main__":
    main()
