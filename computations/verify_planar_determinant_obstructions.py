#!/usr/bin/env python3
"""Exact checks for the planar cycle and homogeneous-ladder obstructions.

Only integer arithmetic and ``fractions.Fraction`` are used.  The script:

* checks an explicit Kasteleyn signing of the 2x5 ladder;
* enumerates its eight perfect matchings and the five coefficient
  polynomials used in the proof;
* checks that all-positive C10 has constant determinant sign; and
* verifies the nearest-neighbor exponent rectangle behind the arbitrary
  cycle-table obstruction.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction


Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex, str, int]
Monomial = tuple[int, int, int, int]  # exponents of V, X, H, Y
Polynomial = Counter[Monomial]


def perfect_matchings(vertices: tuple[Vertex, ...], edges: tuple[Edge, ...]):
    adjacency: dict[Vertex, list[tuple[Vertex, int]]] = {
        vertex: [] for vertex in vertices
    }
    for edge_index, (u, v, _kind, _sign) in enumerate(edges):
        adjacency[u].append((v, edge_index))
        adjacency[v].append((u, edge_index))

    def recurse(remaining: frozenset[Vertex]):
        if not remaining:
            yield ()
            return
        u = min(remaining)
        for v, edge_index in adjacency[u]:
            if v in remaining:
                for tail in recurse(remaining - {u, v}):
                    yield (edge_index,) + tail

    return tuple(recurse(frozenset(vertices)))


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant_term_signs(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    matchings: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    left = tuple(vertex for vertex in vertices if sum(vertex) % 2 == 0)
    right = tuple(vertex for vertex in vertices if sum(vertex) % 2 == 1)
    left_index = {vertex: index for index, vertex in enumerate(left)}
    right_index = {vertex: index for index, vertex in enumerate(right)}
    answer = []
    for matching in matchings:
        permutation = [-1] * len(left)
        edge_sign = 1
        for edge_index in matching:
            u, v, _kind, sign = edges[edge_index]
            edge_sign *= sign
            if u in left_index:
                permutation[left_index[u]] = right_index[v]
            else:
                permutation[left_index[v]] = right_index[u]
        answer.append(permutation_sign(tuple(permutation)) * edge_sign)
    return tuple(answer)


def ladder() -> tuple[tuple[Vertex, ...], tuple[Edge, ...]]:
    vertices = tuple((row, column) for row in range(2) for column in range(5))
    edges: list[Edge] = []
    for row in range(2):
        for column in range(4):
            # One negative edge on the boundary of every square.
            sign = -1 if row == 0 else 1
            edges.append(
                ((row, column), (row, column + 1), "horizontal", sign)
            )
    for column in range(5):
        edges.append(((0, column), (1, column), "rung", 1))
    return vertices, tuple(edges)


def entry_monomial(kind: str, equal: bool) -> Monomial:
    if kind == "rung":
        return (1, 0, 0, 0) if equal else (0, 1, 0, 0)
    assert kind == "horizontal"
    return (0, 0, 1, 0) if equal else (0, 0, 0, 1)


def add_exponents(first: Monomial, second: Monomial) -> Monomial:
    return tuple(a + b for a, b in zip(first, second))  # type: ignore[return-value]


def coefficient_polynomial(
    coloring: tuple[int, ...],
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    matchings: tuple[tuple[int, ...], ...],
) -> Polynomial:
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    polynomial: Polynomial = Counter()
    for matching in matchings:
        monomial: Monomial = (0, 0, 0, 0)
        for edge_index in matching:
            u, v, kind, _sign = edges[edge_index]
            equal = coloring[vertex_index[u]] == coloring[vertex_index[v]]
            monomial = add_exponents(monomial, entry_monomial(kind, equal))
        polynomial[monomial] += 1
    return polynomial


def coloring(top: str, bottom: str) -> tuple[int, ...]:
    assert len(top) == len(bottom) == 5
    return tuple(map(int, top + bottom))


def verify_ladder() -> None:
    vertices, edges = ladder()
    matchings = perfect_matchings(vertices, edges)
    assert len(matchings) == 8
    assert set(determinant_term_signs(vertices, edges, matchings)) == {1}

    expected = {
        ("00000", "00000"): Counter(
            {(5, 0, 0, 0): 1, (3, 0, 2, 0): 4, (1, 0, 4, 0): 3}
        ),
        ("00000", "11111"): Counter(
            {(0, 5, 0, 0): 1, (0, 3, 2, 0): 4, (0, 1, 4, 0): 3}
        ),
        ("01010", "02020"): Counter(
            {(3, 2, 0, 0): 1, (2, 1, 0, 2): 4, (1, 0, 0, 4): 3}
        ),
        ("01010", "01010"): Counter(
            {(5, 0, 0, 0): 1, (3, 0, 0, 2): 4, (1, 0, 0, 4): 3}
        ),
        ("01010", "10101"): Counter(
            {(0, 5, 0, 0): 1, (0, 3, 0, 2): 4, (0, 1, 0, 4): 3}
        ),
    }
    for words, wanted in expected.items():
        actual = coefficient_polynomial(
            coloring(*words), vertices, edges, matchings
        )
        assert actual == wanted, (words, actual, wanted)

    # Exact audit of the only possibilities left by the three factored
    # equations.  z=Y^2/V^2 and r=X/V.
    survivors: list[tuple[Fraction, Fraction]] = []
    for z in (Fraction(-1), Fraction(-1, 3)):
        for r in (-z, -3 * z):
            if (r * r + z) * (r * r + 3 * z) == 0:
                survivors.append((z, r))
    assert survivors == [(Fraction(-1), Fraction(1)),
                         (Fraction(-1, 3), Fraction(1))]


def cycle(size: int) -> tuple[tuple[Vertex, ...], tuple[Edge, ...]]:
    # Store cycle vertex k as (0,k); parity of the second coordinate gives
    # the bipartition.  For C10 all signs can be positive.
    vertices = tuple((0, index) for index in range(size))
    edges = tuple(
        (
            vertices[index],
            vertices[(index + 1) % size],
            "cycle",
            1,
        )
        for index in range(size)
    )
    return vertices, edges


def local_factor_exponents(word: tuple[int, ...]) -> Counter[tuple[int, int, int]]:
    """Exponent vector of product_i r_i(word_i, word_(i+1))."""
    return Counter(
        (index, word[index], word[(index + 1) % len(word)])
        for index in range(len(word))
    )


def verify_cycle() -> None:
    vertices, edges = cycle(10)
    matchings = perfect_matchings(vertices, edges)
    assert len(matchings) == 2
    assert set(determinant_term_signs(vertices, edges, matchings)) == {1}

    zero = (0, 0, 0, 0, 0)
    first = (1, 0, 0, 0, 0)
    second = (0, 0, 1, 0, 0)
    both = (1, 0, 1, 0, 0)
    left = local_factor_exponents(zero) + local_factor_exponents(both)
    right = local_factor_exponents(first) + local_factor_exponents(second)
    assert left == right


def main() -> None:
    verify_cycle()
    verify_ladder()
    print("C10: two matchings, all-positive Kasteleyn determinant signs agree")
    print("cycle nearest-neighbor rectangle identity verified exactly")
    print("2x5 ladder: 8 matchings, explicit Kasteleyn signs agree")
    print("five ladder coefficient polynomials and finite factor audit verified")


if __name__ == "__main__":
    main()
