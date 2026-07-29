#!/usr/bin/env python3
"""Exact audit for the three-cut CP-uniqueness tight boundary."""

from itertools import combinations, permutations, product

import sympy as sp


N = 6
COLORS = range(3)
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))

M0 = frozenset(((0, 1), (2, 3), (4, 5)))
M1 = frozenset(((0, 1), (2, 4), (3, 5)))
M2 = frozenset(((0, 2), (3, 4), (1, 5)))
SELECTED = (M0, M1, M2)
SUPPORT = frozenset().union(*SELECTED)


def perfect_matchings(vertices=VERTICES):
    vertices = tuple(vertices)
    if not vertices:
        yield frozenset()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remaining):
            yield frozenset(((u, v),)) | tail


PM = tuple(perfect_matchings())


def edge_matrix(edge, add_inactive=False):
    if edge in ((0, 1), (2, 3), (4, 5)):
        return sp.diag(1, 0, 0)
    if edge in ((2, 4), (3, 5)):
        return sp.diag(0, 1, 0)
    if edge in ((0, 2), (3, 4), (1, 5)):
        return sp.diag(0, 0, 1)
    if add_inactive and edge == (0, 5):
        return sp.eye(3)
    return sp.zeros(3)


def matching_tensor(add_inactive=False):
    tensor = {}
    for coloring in product(COLORS, repeat=N):
        value = 0
        for matching in PM:
            term = 1
            for u, v in matching:
                term *= edge_matrix((u, v), add_inactive)[coloring[u], coloring[v]]
            value += term
        if value:
            tensor[coloring] = value
    return tensor


def flatten(tensor, shore):
    shore = tuple(shore)
    other = tuple(v for v in VERTICES if v not in shore)
    rows = tuple(product(COLORS, repeat=len(shore)))
    cols = tuple(product(COLORS, repeat=len(other)))
    matrix = sp.zeros(len(rows), len(cols))
    for i, left in enumerate(rows):
        for j, right in enumerate(cols):
            coloring = [None] * N
            for vertex, color in zip(shore, left):
                coloring[vertex] = color
            for vertex, color in zip(other, right):
                coloring[vertex] = color
            matrix[i, j] = tensor.get(tuple(coloring), 0)
    return matrix


def crossing_count(matching, shore):
    shore = frozenset(shore)
    return sum((u in shore) != (v in shore) for u, v in matching)


def constructive_tight_three_shore(matchings, vertices):
    """The shore constructed in the uniform proof of Lemma 4.1."""
    multiplicity = {}
    for matching in matchings:
        for edge in matching:
            multiplicity[edge] = multiplicity.get(edge, 0) + 1

    twice = next((edge for edge, count in multiplicity.items() if count == 2), None)
    if twice is not None:
        u, v = twice
        omitted = next(matching for matching in matchings if twice not in matching)
        ux = next(edge for edge in omitted if u in edge)
        x = next(vertex for vertex in ux if vertex != u)
        shore = frozenset((u, v, x))
    else:
        common = next(
            (edge for edge, count in multiplicity.items() if count == 3), None
        )
        # If there is no common edge either, the three matchings are pairwise
        # edge-disjoint; the standard three-one-factors lemma supplies a
        # fourth supported perfect matching for |V| >= 6.
        assert common is not None
        u, v = common
        x = next(vertex for vertex in vertices if vertex not in common)
        shore = frozenset((u, v, x))

    assert len(shore) == 3
    assert all(crossing_count(matching, shore) == 1 for matching in matchings)
    return shore


def audit_exactly_three_supports(n):
    """Exhaust all triples whose edge union supports exactly that triple."""
    vertices = tuple(range(n))
    matchings = tuple(perfect_matchings(vertices))
    edges = tuple(combinations(vertices, 2))
    edge_bit = {edge: 1 << index for index, edge in enumerate(edges)}
    masks = tuple(
        sum(edge_bit[edge] for edge in matching) for matching in matchings
    )

    count = 0
    supports = set()
    for indices in combinations(range(len(matchings)), 3):
        union_mask = masks[indices[0]] | masks[indices[1]] | masks[indices[2]]
        supported_indices = tuple(
            index
            for index, mask in enumerate(masks)
            if mask & ~union_mask == 0
        )
        if len(supported_indices) != 3:
            continue
        assert set(supported_indices) == set(indices)
        selected = tuple(matchings[index] for index in supported_indices)
        constructive_tight_three_shore(selected, vertices)
        supports.add(union_mask)
        count += 1

    # A union supporting exactly three matchings determines its triple.
    assert count == len(supports)
    return count


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return True
    reached = {next(iter(vertices))}
    changed = True
    while changed:
        changed = False
        for u, v in edges:
            if u in reached and v in vertices and v not in reached:
                reached.add(v)
                changed = True
            if v in reached and u in vertices and u not in reached:
                reached.add(u)
                changed = True
    return reached == vertices


def canonical(edge_set):
    return min(
        tuple(
            sorted(
                tuple(sorted((permutation[u], permutation[v])))
                for u, v in edge_set
            )
        )
        for permutation in permutations(VERTICES)
    )


def main():
    assert len(PM) == 15
    supported = tuple(matching for matching in PM if matching <= SUPPORT)
    assert set(supported) == set(SELECTED)
    assert set.intersection(*(set(matching) for matching in SELECTED)) == set()

    tensor = matching_tensor()
    expected = {
        (0, 0, 0, 0, 0, 0): 1,
        (0, 0, 1, 1, 1, 1): 1,
        (2, 2, 2, 2, 2, 2): 1,
    }
    assert tensor == expected

    # Every balanced flattening has rank exactly three.
    for shore in combinations(VERTICES, 3):
        assert flatten(tensor, shore).rank() == 3, shore

    # The local factor matrices have Kruskal ranks 1,1,3,3,3,3.
    local_factors = []
    words = tuple(expected)
    for vertex in VERTICES:
        matrix = sp.Matrix.hstack(
            *(sp.eye(3)[:, word[vertex]] for word in words)
        )
        k_rank = 0
        for size in range(1, 4):
            if all(matrix[:, cols].rank() == size for cols in combinations(range(3), size)):
                k_rank = size
            else:
                break
        local_factors.append(k_rank)
    assert local_factors == [1, 1, 3, 3, 3, 3]
    assert sum(local_factors) == 14 >= 2 * 3 + (N - 1)

    # Exact one-cross / three-cross contamination on the named cut.
    shore = frozenset((0, 3, 5))
    counts = tuple(crossing_count(matching, shore) for matching in SELECTED)
    assert counts == (3, 1, 3)
    one_cross = {tuple(expected)[1]: 1}
    three_cross = {tuple(expected)[0]: 1, tuple(expected)[2]: 1}
    assert {**one_cross, **three_cross} == expected
    assert flatten(one_cross, shore).rank() == 1
    assert flatten(three_cross, shore).rank() == 2

    # Every support edge is active; the graph is bridgeless and has no
    # articulation vertex.
    assert all(any(edge in matching for matching in SELECTED) for edge in SUPPORT)
    for edge in SUPPORT:
        assert connected(VERTICES, SUPPORT - {edge})
    for vertex in VERTICES:
        remaining = set(VERTICES) - {vertex}
        remaining_edges = {
            edge for edge in SUPPORT if vertex not in edge
        }
        assert connected(remaining, remaining_edges)

    tight = frozenset((0, 1, 2))
    assert all(crossing_count(matching, tight) == 1 for matching in SELECTED)

    # Edge 05 can carry a full-rank invisible matrix: its complement has no
    # matching, and the complete output is unchanged.
    complement = frozenset((1, 2, 3, 4))
    assert not any(matching <= SUPPORT for matching in perfect_matchings(complement))
    assert edge_matrix((0, 5), add_inactive=True).rank() == 3
    assert matching_tensor(add_inactive=True) == tensor

    # Label-free six-site audit and an eight-site audit of the constructive
    # uniform proof of Lemma 4.1.
    supports = set()
    for matching_triple in combinations(PM, 3):
        edge_union = frozenset().union(*matching_triple)
        if sum(matching <= edge_union for matching in PM) == 3:
            supports.add(edge_union)
    assert len(supports) == 375

    orbit_representatives = {}
    for edge_union in supports:
        supported_matchings = tuple(
            matching for matching in PM if matching <= edge_union
        )
        assert any(
            all(crossing_count(matching, shore) == 1 for matching in supported_matchings)
            for shore in map(frozenset, combinations(VERTICES, 3))
        )
        orbit_representatives.setdefault(canonical(edge_union), edge_union)
    assert len(orbit_representatives) == 3
    assert sorted(len(edge_union) for edge_union in orbit_representatives.values()) == [
        7,
        7,
        8,
    ]
    assert all(
        constructive_tight_three_shore(
            tuple(matching for matching in PM if matching <= edge_union),
            VERTICES,
        )
        for edge_union in supports
    )

    n8_count = audit_exactly_three_supports(8)
    assert n8_count > 0

    print("three-cut CP uniqueness tight boundary: PASS")
    print("all 20 balanced flattenings have rank 3; Kruskal sum is 14")
    print("named cut has one-cross rank 1 and three-cross rank 2")
    print("all 375 six-site three-matching supports have a tight three-cut (3 orbits)")
    print(f"all {n8_count} eight-site exactly-three supports pass the constructive lemma")


if __name__ == "__main__":
    main()
