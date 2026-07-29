#!/usr/bin/env python3
"""Explore the uniform five-factor balanced support over rank-one matrices.

This is a discovery helper.  The two factors F_0,F_1 are universally
supported (all endpoint factor coordinates are nonzero), while F_2,F_3,F_4
carry the same-color labels 0,1,2.  It checks whether the colorings avoiding
all three labelled factors span the full local-character lattice, and looks
for a mixed coloring whose fiber is the two universal matchings plus exactly
one further matching.
"""

from __future__ import annotations

import itertools

import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form


def round_factor(n: int, r: int):
    modulus = n - 1
    infinity = modulus
    edges = [tuple(sorted((infinity, r % modulus)))]
    for k in range(1, n // 2):
        edges.append(tuple(sorted(((r + k) % modulus, (r - k) % modulus))))
    return tuple(sorted(edges))


def perfect_matchings_graph(n: int, edges):
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    def visit(vertices):
        if not vertices:
            yield ()
            return
        u = min(vertices)
        rest0 = vertices - {u}
        for v in sorted(adjacency[u] & rest0):
            for tail in visit(rest0 - {v}):
                yield tuple(sorted(((u, v),) + tail))

    yield from visit(set(range(n)))


def is_clean(coloring, anchors):
    return all(
        not (coloring[u] == coloring[v] == color)
        for color, matching in enumerate(anchors)
        for u, v in matching
    )


def vector(coloring):
    # Local character exponent vector after normalizing r_v(0)=1.
    return tuple(
        int(coloring[v] == color)
        for v in range(len(coloring))
        for color in (1, 2)
    )


def cycle_exponent(coloring, first, second):
    """Signed cell-exponent vector for m_first(coloring)/m_second(coloring)."""
    edges = first + second
    answer = [0] * (9 * len(edges))
    for edge_index, (u, v) in enumerate(edges):
        cell = 3 * coloring[u] + coloring[v]
        answer[9 * edge_index + cell] = 1 if edge_index < len(first) else -1
    return tuple(answer)


def cycle_features(coloring, cycle_order):
    """Standard singleton/nearest-neighbor interaction coordinates."""
    answer = []
    for v in cycle_order:
        answer.extend((int(coloring[v] == 1), int(coloring[v] == 2)))
    for index, u in enumerate(cycle_order):
        v = cycle_order[(index + 1) % len(cycle_order)]
        answer.extend(
            int(coloring[u] == a and coloring[v] == b)
            for a in (1, 2) for b in (1, 2)
        )
    return tuple(answer)


def cycle_order(first, second):
    adjacency = {}
    for edge in first + second:
        u, v = edge
        adjacency.setdefault(u, []).append(v)
        adjacency.setdefault(v, []).append(u)
    start = min(adjacency)
    order = [start]
    previous = None
    current = start
    while True:
        choices = [v for v in adjacency[current] if v != previous]
        following = choices[0]
        if following == start:
            break
        order.append(following)
        previous, current = current, following
    assert len(order) == len(adjacency)
    return tuple(order)


def supported(matching, coloring, anchors_by_edge):
    for edge in matching:
        if edge in anchors_by_edge:
            color = anchors_by_edge[edge]
            u, v = edge
            if coloring[u] != color or coloring[v] != color:
                return False
    return True


def audit(n: int):
    factors = tuple(round_factor(n, r) for r in range(5))
    assert all(len(set(factors[i]) & set(factors[j])) == 0
               for i in range(5) for j in range(i))
    universal = factors[:2]
    anchors = factors[2:]
    assert set(universal[0]) | set(universal[1])
    graph_edges = set().union(*map(set, factors))
    matchings = tuple(perfect_matchings_graph(n, graph_edges))
    anchors_by_edge = {
        edge: color for color, matching in enumerate(anchors) for edge in matching
    }

    clean = [c for c in itertools.product(range(3), repeat=n) if is_clean(c, anchors)]
    clean_set = set(clean)
    base = vector(clean[0])
    difference_rows = [
        [entry - origin for entry, origin in zip(vector(c), base)] for c in clean[1:]
    ]
    rank = sp.Matrix(difference_rows).rank()

    cycle_base = cycle_exponent(clean[0], *universal)
    cycle_rows = [
        [entry - origin for entry, origin in zip(
            cycle_exponent(c, *universal), cycle_base
        )]
        for c in clean[1:]
    ]
    cycle_rank = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(cycle_rows), len(cycle_base), cycle_rows
    ).to_field().rank()

    order = cycle_order(*universal)
    feature_base = cycle_features(clean[0], order)
    feature_columns = sp.Matrix([
        [entry - origin for entry, origin in zip(
            cycle_features(c, order), feature_base
        )]
        for c in clean[1:]
    ]).T
    hnf = hermite_normal_form(feature_columns)
    feature_index = abs(int(hnf.det())) if hnf.rows == hnf.cols else None

    rectangle_witnesses = {}
    for edge_index, u in enumerate(order):
        v = order[(edge_index + 1) % n]
        for a in (1, 2):
            for b in (1, 2):
                witness = None
                for coloring in clean:
                    background = list(coloring)
                    corners = []
                    for left in (0, a):
                        for right in (0, b):
                            corner = background.copy()
                            corner[u] = left
                            corner[v] = right
                            corners.append(tuple(corner))
                    if all(corner in clean_set for corner in corners):
                        witness = tuple(corners)
                        break
                rectangle_witnesses[u, v, a, b] = witness
    rectangle_count = sum(witness is not None for witness in rectangle_witnesses.values())

    all_base = cycle_exponent((0,) * n, *universal)
    all_rows = [
        [entry - origin for entry, origin in zip(
            cycle_exponent(c, *universal), all_base
        )]
        for c in itertools.product(range(3), repeat=n)
    ]
    all_rank = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(all_rows), len(all_base), all_rows
    ).to_field().rank()

    special = None
    fiber_sizes = {}
    for coloring in itertools.product(range(3), repeat=n):
        fiber = tuple(
            matching for matching in matchings
            if supported(matching, coloring, anchors_by_edge)
        )
        fiber_sizes[len(fiber)] = fiber_sizes.get(len(fiber), 0) + 1
        if len(set(coloring)) > 1 and len(fiber) == 3 \
                and set(universal) <= set(fiber):
            special = coloring, fiber
            break

    print(
        f"n={n}: PMs={len(matchings)}, clean={len(clean)}, "
        f"local-rank={rank}/{2*n}, cycle-rank={cycle_rank}/{all_rank}, "
        f"feature-index={feature_index}, "
        f"rectangles={rectangle_count}/{4*n}, "
        f"special={special}, "
        f"partial-fiber-sizes={fiber_sizes}"
    )


def main():
    for n in (6, 8, 10, 12):
        audit(n)


if __name__ == "__main__":
    main()
