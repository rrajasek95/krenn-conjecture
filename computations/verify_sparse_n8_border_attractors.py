#!/usr/bin/env python3
"""Exact audit of the two sparse n=8 numerical border attractors.

The least-squares search in ``search_sparse_n8_q3.py`` repeatedly approaches
one of the two Laurent families below.  Each active edge has a single
same-color matrix entry.  Three perfect matchings give the constant-color
terms with coefficient one, and exactly two further perfect matchings give
distinct mixed colorings with coefficient ``t``.  Consequently these are
border degenerations, never finite exact counterexamples for ``t != 0``.

No floating-point or symbolic-algebra package is used.  Laurent monomials
are represented by their integer exponent of the indeterminate ``t``.
"""

from __future__ import annotations

from collections import Counter


N = 8


def perfect_matchings(vertices: tuple[int, ...], edges: frozenset[tuple[int, int]]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        edge = (u, v)
        if edge not in edges:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest, edges):
            yield (edge,) + tail


def audit(
    color_matchings: tuple[tuple[tuple[int, int], ...], ...],
    positive_edge: tuple[int, int],
    negative_edge: tuple[int, int],
    expected_mixed: frozenset[tuple[int, ...]],
) -> None:
    edge_data: dict[tuple[int, int], tuple[int, int]] = {}
    for color, matching in enumerate(color_matchings):
        for edge in matching:
            assert edge not in edge_data
            exponent = int(edge == positive_edge) - int(edge == negative_edge)
            edge_data[edge] = color, exponent

    assert positive_edge in edge_data and negative_edge in edge_data
    assert edge_data[positive_edge][0] == edge_data[negative_edge][0]

    coefficients: Counter[tuple[tuple[int, ...], int]] = Counter()
    matchings = tuple(
        perfect_matchings(tuple(range(N)), frozenset(edge_data))
    )
    for matching in matchings:
        coloring = [-1] * N
        exponent = 0
        for u, v in matching:
            color, local_exponent = edge_data[u, v]
            coloring[u] = coloring[v] = color
            exponent += local_exponent
        coefficients[tuple(coloring), exponent] += 1

    expected = Counter({((color,) * N, 0): 1 for color in range(3)})
    expected.update({(coloring, 1): 1 for coloring in expected_mixed})
    assert coefficients == expected
    assert len(matchings) == 5


def main() -> None:
    # Attractor selected by ``--extra 0 --seed 0``.  Taking w_36=t and
    # w_14=t^{-1} leaves the color-zero product equal to one.
    audit(
        (
            ((0, 2), (1, 4), (3, 6), (5, 7)),
            ((0, 3), (1, 5), (2, 4), (6, 7)),
            ((0, 1), (2, 3), (4, 7), (5, 6)),
        ),
        positive_edge=(3, 6),
        negative_edge=(1, 4),
        expected_mixed=frozenset(
            {
                (2, 2, 1, 0, 1, 0, 0, 0),
                (0, 1, 0, 0, 2, 1, 0, 2),
            }
        ),
    )

    # Attractor selected by ``--extra 3 --seed 0``.  Taking w_67=t and
    # w_24=t^{-1} leaves the color-one product equal to one.
    audit(
        (
            ((0, 7), (1, 4), (2, 3), (5, 6)),
            ((0, 3), (1, 5), (2, 4), (6, 7)),
            ((0, 4), (1, 6), (2, 5), (3, 7)),
        ),
        positive_edge=(6, 7),
        negative_edge=(2, 4),
        expected_mixed=frozenset(
            {
                (1, 0, 2, 1, 0, 2, 1, 1),
                (2, 1, 0, 0, 2, 1, 1, 1),
            }
        ),
    )
    print("verified two exact n=8 families: Delta_(8,3) + t(T_1 + T_2)")


if __name__ == "__main__":
    main()
